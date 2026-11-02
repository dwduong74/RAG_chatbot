# -*- coding: utf-8 -*-
"""
Module truy vấn hỏi đáp RAG trên dữ liệu Khoa Kỹ thuật Điện tử 1 (SEA - PTIT)
CSDL: ./chroma_db_sea_ptit (Collection: sea_ptit_ktdt1)
Mô hình nhúng: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
"""

import os
import sys
import time
import chromadb
from fastembed import TextEmbedding

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CHROMA_DIR = os.path.abspath("chroma_db_sea_ptit")
COLLECTION_NAME = "sea_ptit_ktdt1"
EMBED_MODEL_NAME = "minishlab/potion-multilingual-128M"

class SeaPTITRAGRetriever:
    def __init__(self, persist_dir=CHROMA_DIR, model_name=EMBED_MODEL_NAME):
        self.persist_dir = persist_dir
        self.model_name = model_name
        
        if not os.path.exists(persist_dir):
            raise FileNotFoundError(f"Không tìm thấy CSDL ChromaDB tại: {persist_dir}. Hãy chạy build_sea_rag_db.py trước!")
            
        print(f"[*] Nạp mô hình nhúng: {model_name}...")
        self.embed_model = TextEmbedding(model_name=model_name)
        
        print(f"[*] Kết nối CSDL ChromaDB: {persist_dir}...")
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_collection(name=COLLECTION_NAME)
        print(f"[OK] Đã kết nối Collection '{COLLECTION_NAME}' (Tổng số: {self.collection.count()} chunks).\n")

    def search(self, query: str, top_k: int = 5):
        t0 = time.time()
        # Mã hóa câu hỏi thành vector
        query_emb = list(self.embed_model.embed([query]))[0].tolist()
        
        # Truy vấn độ tương đồng cosine trong ChromaDB
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )
        latency_ms = (time.time() - t0) * 1000.0
        
        hits = []
        if results and "ids" in results and len(results["ids"]) > 0:
            for i in range(len(results["ids"][0])):
                distance = results["distances"][0][i]
                score = 1.0 - distance # Cosine similarity
                doc_text = results["documents"][0][i]
                metadata = results["metadatas"][0][i]
                chunk_id = results["ids"][0][i]
                
                hits.append({
                    "rank": i + 1,
                    "score": score,
                    "chunk_id": chunk_id,
                    "title": metadata.get("title", ""),
                    "category": metadata.get("category", ""),
                    "url": metadata.get("url", ""),
                    "date": metadata.get("date", ""),
                    "text": doc_text
                })
                
        return hits, latency_ms

def format_search_results(query, hits, latency_ms):
    lines = []
    lines.append("=" * 80)
    lines.append(f" CÂU HỎI TRUY VẤN: {query}")
    lines.append(f" Thời gian truy xuất: {latency_ms:.2f} ms | Tìm thấy: {len(hits)} đoạn liên quan nhất")
    lines.append("=" * 80)
    
    for hit in hits:
        lines.append(f"\n[Hạng {hit['rank']}] Điểm tương đồng: {hit['score']:.4f}")
        lines.append(f"  • Tiêu đề: {hit['title']}")
        lines.append(f"  • Chuyên mục: {hit['category']}")
        lines.append(f"  • Ngày đăng/cập nhật: {hit['date']}")
        lines.append(f"  • Liên kết gốc: {hit['url']}")
        lines.append(f"  • Trích đoạn nội dung:")
        
        # Hiển thị trích đoạn ngắn gọn nhưng đủ ý
        text = hit['text']
        # Tách bỏ header nếu có để hiển thị nội dung chính
        content_only = text.split("\n\n", 1)[-1] if "\n\n" in text else text
        sample = content_only[:350].strip() + ("..." if len(content_only) > 350 else "")
        for sub_line in sample.split("\n"):
            if sub_line.strip():
                lines.append(f"    | {sub_line.strip()}")
        lines.append("-" * 80)
        
    return "\n".join(lines)

def run_verification_benchmark(retriever):
    """Bộ câu hỏi kiểm thử thực tế về Khoa KTĐT1 (SEA - PTIT)"""
    test_queries = [
        "Phó Giáo sư Phạm Minh Triển nghiên cứu về những lĩnh vực nào và email liên hệ là gì?",
        "Chương trình đào tạo ngành Công nghệ kỹ thuật Điện - Điện tử của Khoa năm 2023 có những thông tin gì?",
        "Chính sách học bổng theo Nghị định 179 của Chính phủ dành cho sinh viên Khoa như thế nào?",
        "Câu lạc bộ Điện tử PTIT thuộc Liên chi đoàn Khoa có hoạt động gì nổi bật?",
        "Các doanh nghiệp đối tác hợp tác với Khoa gồm những đơn vị nào?",
        "TS. Nguyễn Trung Hiếu - Trưởng khoa Kỹ thuật Điện tử 1 nghiên cứu hướng nào?",
        "Khoa KTĐT1 có những phòng thí nghiệm và trang thiết bị thực hành nào?"
    ]
    
    print("\n" + "=" * 80)
    print(" CHẠY KIỂM THỬ THỰC NGHIỆM TRÊN CSDL TRI THỨC KHOA KTĐT1")
    print("=" * 80)
    
    for idx, q in enumerate(test_queries, 1):
        print(f"\n>>> [TEST {idx}/{len(test_queries)}] Đang truy vấn: '{q}'...")
        hits, lat = retriever.search(q, top_k=3)
        print(format_search_results(q, hits, lat))

def main():
    retriever = SeaPTITRAGRetriever()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test" or sys.argv[1] == "-t":
            run_verification_benchmark(retriever)
        else:
            q = " ".join(sys.argv[1:])
            hits, lat = retriever.search(q, top_k=5)
            print(format_search_results(q, hits, lat))
    else:
        # Chạy kiểm thử tự động nếu không truyền tham số
        print("[*] Không có câu hỏi chỉ định, tự động kích hoạt bộ câu hỏi kiểm chứng đối sánh...")
        run_verification_benchmark(retriever)

if __name__ == "__main__":
    main()
