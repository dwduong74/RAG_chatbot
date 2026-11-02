# -*- coding: utf-8 -*-
"""
Mã nguồn Xây dựng Cơ sở Dữ liệu Tri thức Vector RAG (ChromaDB + FastEmbed)
Cập nhật chuẩn mực theo khuyến nghị thẩm định:
- Khống chế kích thước chunk: 250 từ (~350 token, dưới ngưỡng 512 token của BGE)
- Phân đoạn liên tục xuyên trang, lưu dải trang chính xác
- Sử dụng phương thức upsert để bảo đảm khả năng cập nhật lại không lỗi
- Hỗ trợ chạy trên cả Linux và Windows
"""

import os
import sys
import glob
import re
import fitz  # PyMuPDF
import chromadb
from fastembed import TextEmbedding

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_chunks_continuous(pdf_path, chunk_words=250, overlap_words=50):
    """
    Trích xuất toàn văn liên tục xuyên trang và phân đoạn có vùng gối đầu
    """
    doc = fitz.open(pdf_path)
    file_name = os.path.basename(pdf_path)
    
    # Gom toàn bộ từ và số trang tương ứng
    tokens_with_pages = []
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        text = page.get_text("text").strip()
        if not text:
            continue
        text = re.sub(r'\s+', ' ', text)
        words = text.split()
        for w in words:
            tokens_with_pages.append((w, page_idx + 1))
    doc.close()
    
    chunks = []
    i = 0
    chunk_num = 0
    step = chunk_words - overlap_words
    total_tokens = len(tokens_with_pages)
    
    while i < total_tokens:
        slice_tokens = tokens_with_pages[i : i + chunk_words]
        chunk_text = " ".join([w for w, _ in slice_tokens])
        pages_set = sorted(list(set([p for _, p in slice_tokens])))
        page_str = f"{pages_set[0]}-{pages_set[-1]}" if len(pages_set) > 1 else str(pages_set[0])
        
        chunk_id = f"{file_name}_c{chunk_num:04d}_p{page_str}"
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "file_name": file_name,
            "pages": page_str,
            "start_page": pages_set[0],
            "end_page": pages_set[-1],
            "word_count": len(slice_tokens)
        })
        chunk_num += 1
        i += step
        if i >= total_tokens:
            break
            
    return chunks

def build_vector_store(pdf_dir="papers", persist_dir="./chroma_db_papers", model_name="BAAI/bge-small-en-v1.5"):
    print(f"[*] Khởi tạo mô hình FastEmbed: {model_name}...")
    embed_model = TextEmbedding(model_name=model_name)
    
    print(f"[*] Kết nối cơ sở dữ liệu ChromaDB tại: {persist_dir}...")
    client = chromadb.PersistentClient(path=persist_dir)
    collection_name = "nckh_rag_papers"
    
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))
    if not pdf_files:
        print(f"[!] Không tìm thấy tệp PDF nào trong {pdf_dir}")
        return
        
    all_chunks = []
    for pdf_path in pdf_files:
        file_chunks = extract_chunks_continuous(pdf_path, chunk_words=250, overlap_words=50)
        print(f"[*] Đã trích xuất {len(file_chunks)} chunks từ {os.path.basename(pdf_path)}")
        all_chunks.extend(file_chunks)
        
    print(f"[*] Tổng số đoạn trích đoạn cần nhúng: {len(all_chunks)} chunks.")
    
    # Nạp theo lô và sử dụng upsert
    batch_size = 16
    for idx in range(0, len(all_chunks), batch_size):
        batch = all_chunks[idx : idx + batch_size]
        texts = [item["text"] for item in batch]
        ids = [item["chunk_id"] for item in batch]
        metadatas = [{
            "file_name": item["file_name"],
            "pages": item["pages"],
            "word_count": item["word_count"]
        } for item in batch]
        
        # Sinh vector nhúng
        embeddings = [emb.tolist() for emb in embed_model.embed(texts, batch_size=batch_size)]
        
        # Dùng upsert thay vì add để chống lỗi trùng lặp khi chạy lại
        collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"    [+] Đã lập chỉ mục lô {idx // batch_size + 1} / {(len(all_chunks) + batch_size - 1) // batch_size}")
        
    print(f"[✓] Lập chỉ mục thành công {len(all_chunks)} đoạn vào ChromaDB collection `{collection_name}`!")

if __name__ == "__main__":
    build_vector_store()
