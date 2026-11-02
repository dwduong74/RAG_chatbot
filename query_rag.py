# -*- coding: utf-8 -*-
"""
Module Truy xuất Ngữ nghĩa RAG (PaperRAGRetriever)
- Sử dụng mô hình nhúng BAAI/bge-small-en-v1.5
- Tích hợp Query Instruction chuẩn mực của BGE
- Truy xuất láng giềng gần nhất trên chỉ mục HNSW Cosine của ChromaDB
"""

import sys
import chromadb
from fastembed import TextEmbedding

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class PaperRAGRetriever:
    def __init__(self, persist_dir="./chroma_db_papers", model_name="BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.embed_model = TextEmbedding(model_name=model_name)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_collection(name="nckh_rag_papers")

    def search(self, query: str, top_k: int = 5):
        # Đối với các mô hình dòng BGE, truy vấn cần tiền tố instruction để tối ưu hóa biểu diễn
        if "bge" in self.model_name.lower():
            formatted_query = f"Represent this sentence for searching relevant passages: {query}"
        else:
            formatted_query = query
            
        query_embedding = list(self.embed_model.embed([formatted_query]))[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        parsed_results = []
        if results and "ids" in results and len(results["ids"]) > 0:
            for i in range(len(results["ids"][0])):
                distance = results["distances"][0][i]
                similarity = 1.0 - distance
                parsed_results.append({
                    "id": results["ids"][0][i],
                    "score": similarity,
                    "metadata": results["metadatas"][0][i],
                    "text": results["documents"][0][i]
                })
        return parsed_results

if __name__ == "__main__":
    retriever = PaperRAGRetriever()
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is the mathematical formulation of the marginal probability for RAG-Sequence model?"
    print(f"=== ĐẶT CÂU HỎI TRUY VẤN: {q} ===")
    hits = retriever.search(q, top_k=5)
    for idx, hit in enumerate(hits):
        pages = hit['metadata'].get('pages', hit['metadata'].get('page', 'N/A'))
        print(f"\n--- [Hạng {idx+1}] Điểm tương đồng: {hit['score']:.4f} | Nguồn: {hit['metadata']['file_name']} (Trang {pages}) ---")
        print(hit['text'][:300] + "...")
