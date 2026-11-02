# -*- coding: utf-8 -*-
"""
Script phân đoạn văn bản và lập chỉ mục Vector cho dữ liệu Khoa KTĐT1 (SEA - PTIT)
Lưu trữ vào ChromaDB cục bộ: ./chroma_db_sea_ptit
Mô hình nhúng đa ngôn ngữ: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
"""

import os
import sys
import glob
import re
import time
import json
import chromadb
from fastembed import TextEmbedding

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATA_DIR = os.path.join("data_sea_ptit", "documents")
CHROMA_DIR = os.path.abspath("chroma_db_sea_ptit")
COLLECTION_NAME = "sea_ptit_ktdt1"
EMBED_MODEL_NAME = "minishlab/potion-multilingual-128M"

CHUNK_SIZE = 300   # 300 từ mỗi đoạn
CHUNK_OVERLAP = 50 # 50 từ chồng lấn (vùng gối đầu)

def parse_markdown_doc(filepath):
    """Phân tách metadata frontmatter và nội dung Markdown"""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
        
    meta = {}
    content = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            content = parts[2].strip()
            for line in fm_text.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
                    
    # Lấy thông tin cơ bản
    meta.setdefault("id", "0")
    meta.setdefault("type", "document")
    meta.setdefault("title", "Khoa Kỹ thuật Điện tử 1 - PTIT")
    meta.setdefault("url", "https://sea.ptit.edu.vn/")
    meta.setdefault("category", "Thông tin chung")
    meta.setdefault("date", "")
    
    return meta, content

def chunk_text(content, meta, chunk_words=CHUNK_SIZE, overlap_words=CHUNK_OVERLAP):
    """Phân đoạn văn bản bằng cửa sổ trượt liên tục kèm nhúng Header ngữ cảnh"""
    # Chuẩn hóa khoảng trắng
    clean_c = re.sub(r'\s+', ' ', content).strip()
    words = clean_c.split()
    total_words = len(words)
    
    if total_words == 0:
        return []
        
    chunks = []
    step = max(1, chunk_words - overlap_words)
    i = 0
    chunk_idx = 0
    
    doc_id = meta.get("id", "0")
    doc_type = meta.get("type", "doc")
    title = meta.get("title", "")
    category = meta.get("category", "")
    url = meta.get("url", "")
    date_str = meta.get("date", "")
    
    # Header ngữ cảnh định danh
    header_prefix = f"[Khoa KTĐT1 - PTIT | Phân loại: {category} | Tiêu đề: {title} | Link: {url}]\n"
    
    while i < total_words:
        slice_words = words[i : i + chunk_words]
        slice_text = " ".join(slice_words)
        
        chunk_full_text = f"{header_prefix}\n{slice_text}"
        chunk_id = f"{doc_type}_{doc_id}_c{chunk_idx:03d}"
        
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_full_text,
            "metadata": {
                "doc_id": str(doc_id),
                "doc_type": doc_type,
                "title": title[:200],
                "category": category[:150],
                "url": url,
                "date": date_str,
                "chunk_index": chunk_idx,
                "word_count": len(slice_words)
            }
        })
        
        chunk_idx += 1
        i += step
        if i >= total_words:
            break
            
    return chunks

def build_sea_vector_db():
    print("=" * 80)
    print(" XÂY DỰNG CƠ SỞ DỮ LIỆU VECTOR RAG KHOA KTĐT1 (SEA - PTIT)")
    print("=" * 80)
    print(f"[*] Thư mục dữ liệu nguồn: {os.path.abspath(DATA_DIR)}")
    print(f"[*] Thư mục CSDL ChromaDB: {CHROMA_DIR}")
    print(f"[*] Tên Collection: {COLLECTION_NAME}")
    print(f"[*] Mô hình nhúng đa ngôn ngữ: {EMBED_MODEL_NAME} (FastEmbed ONNX)")
    print(f"[*] Cấu hình phân đoạn: Kích thước = {CHUNK_SIZE} từ, Gối đầu = {CHUNK_OVERLAP} từ")
    
    # 1. Đọc tất cả các tệp Markdown
    md_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.md")))
    if not md_files:
        print("[!] Không tìm thấy tệp markdown nào trong thư mục dữ liệu!")
        return
        
    print(f"\n[*] Đang đọc và phân đoạn {len(md_files)} tài liệu...")
    all_chunks = []
    for filepath in md_files:
        meta, content = parse_markdown_doc(filepath)
        chunks = chunk_text(content, meta)
        all_chunks.extend(chunks)
        
    print(f"[OK] Tổng số chunks sinh ra: {len(all_chunks)} chunks.")
    avg_words = sum(c["metadata"]["word_count"] for c in all_chunks) / len(all_chunks) if all_chunks else 0
    print(f"[*] Dung lượng trung bình: {avg_words:.1f} từ/chunk.")
    
    # 2. Khởi tạo mô hình nhúng
    print(f"\n[*] Đang nạp mô hình nhúng FastEmbed: {EMBED_MODEL_NAME}...")
    t0 = time.time()
    embed_model = TextEmbedding(model_name=EMBED_MODEL_NAME)
    print(f"[OK] Nạp mô hình nhúng hoàn tất ({time.time() - t0:.2f}s).")
    
    # 3. Khởi tạo ChromaDB
    print(f"\n[*] Khởi tạo kết nối ChromaDB tại: {CHROMA_DIR}...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    
    # Xóa collection cũ nếu tồn tại để tái lập sạch sẽ
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        print(f"[*] Đang làm mới collection '{COLLECTION_NAME}'...")
        client.delete_collection(COLLECTION_NAME)
        
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"[OK] Đã tạo mới collection '{COLLECTION_NAME}' với metric Cosine.")
    
    # 4. Mã hóa vector và nạp dữ liệu theo lô (Batch)
    batch_size = 64
    total_chunks = len(all_chunks)
    print(f"\n[*] Đang mã hóa vector và nạp vào ChromaDB (Batch size = {batch_size})...")
    
    t_start = time.time()
    for start_idx in range(0, total_chunks, batch_size):
        end_idx = min(start_idx + batch_size, total_chunks)
        batch = all_chunks[start_idx:end_idx]
        
        batch_texts = [item["text"] for item in batch]
        batch_ids = [item["chunk_id"] for item in batch]
        batch_metadatas = [item["metadata"] for item in batch]
        
        # FastEmbed batch inference
        batch_embeddings = [emb.tolist() for emb in embed_model.embed(batch_texts, batch_size=batch_size)]
        
        # Upsert to ChromaDB
        collection.upsert(
            ids=batch_ids,
            documents=batch_texts,
            embeddings=batch_embeddings,
            metadatas=batch_metadatas
        )
        
        elapsed = time.time() - t_start
        rate = end_idx / elapsed if elapsed > 0 else 0
        print(f"  -> Tiến độ: {end_idx}/{total_chunks} chunks ({end_idx*100.0/total_chunks:.1f}%) - {rate:.1f} chunks/giây")
        
    total_time = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"[THÀNH CÔNG] Lập chỉ mục Vector hoàn tất:")
    print(f" - Tổng số đoạn văn bản được nhúng: {collection.count()} chunks")
    print(f" - Tổng thời gian: {total_time:.2f} giây ({total_chunks / total_time:.1f} chunks/giây)")
    print(f" - CSDL Vector sẵn sàng phục vụ tại: {CHROMA_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    build_sea_vector_db()
