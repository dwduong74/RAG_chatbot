# -*- coding: utf-8 -*-
"""
Kịch bản thực nghiệm đối chứng toàn diện cho Báo cáo Nghiên cứu Khoa học RAG
- Ngữ liệu: 5 bài báo khoa học chuẩn trong papers/
- 3 Chiến lược phân đoạn: Fixed-size, Sliding Window, Recursive Structure-aware (chunk_size <= 250 từ ~ 350 token < 512 token limit của BGE)
- 3 Phương pháp truy xuất: BM25 (Lexical), MiniLM-L6-v2 (Dense), BGE-small-en-v1.5 (Dense + Instruction)
- Bộ dữ liệu đánh giá: 40 câu hỏi truy vấn chuyên sâu có gán nhãn ground-truth
- Đo lường: Hit@1, Hit@3, Hit@5, MRR@5, Recall@5, nDCG@5, Thời gian nhúng, Độ trễ truy vấn trung bình
"""

import os
import sys
import glob
import time
import math
import json
import re
from collections import Counter
import fitz  # PyMuPDF
import numpy as np

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print(" CHẠY THỰC NGHIỆM ĐỐI CHỨNG HỆ THỐNG TRUY XUẤT RAG TRÊN NGỮ LIỆU KHOA HỌC")
print("=" * 80)

# ------------------------------------------------------------------------------
# 1. TRÍCH XUẤT TOÀN VĂN VÀ GIỮ VẾT TRANG
# ------------------------------------------------------------------------------
PAPERS_METADATA = {
    "1_Lewis_2020_Retrieval_Augmented_Generation.pdf": {
        "short_name": "Lewis et al. (2020)",
        "doc_id": "lewis2020"
    },
    "2_Gao_2023_RAG_for_LLMs_Survey.pdf": {
        "short_name": "Gao et al. (2023b)",
        "doc_id": "gao2023"
    },
    "3_Zhao_2024_RAG_for_AIGC_Survey.pdf": {
        "short_name": "Zhao et al. (2024)",
        "doc_id": "zhao2024"
    },
    "4_Huang_2024_Retrieval_Augmented_Text_Generation_Survey.pdf": {
        "short_name": "Huang & Huang (2024)",
        "doc_id": "huang2024"
    },
    "5_Petroni_2020_KILT_Benchmark_Knowledge_Intensive_NLP.pdf": {
        "short_name": "Petroni et al. (2021)",
        "doc_id": "petroni2021"
    }
}

def load_documents(papers_dir="papers"):
    documents = {}
    total_pages = 0
    pdf_files = sorted(glob.glob(os.path.join(papers_dir, "*.pdf")))
    for pdf_path in pdf_files:
        fname = os.path.basename(pdf_path)
        if fname not in PAPERS_METADATA:
            continue
        meta = PAPERS_METADATA[fname]
        doc = fitz.open(pdf_path)
        pages_content = []
        for p_idx in range(len(doc)):
            txt = doc[p_idx].get_text("text").strip()
            # Clean repetitive whitespaces
            txt = re.sub(r'\s+', ' ', txt)
            pages_content.append({"page_num": p_idx + 1, "text": txt})
        total_pages += len(doc)
        documents[meta["doc_id"]] = {
            "file_name": fname,
            "short_name": meta["short_name"],
            "page_count": len(doc),
            "pages": pages_content
        }
        doc.close()
    print(f"[*] Đã nạp thành công {len(documents)} tài liệu PDF, tổng số trang: {total_pages} trang.")
    return documents

# ------------------------------------------------------------------------------
# 2. BA CHIẾN LƯỢC PHÂN ĐOẠN VĂN BẢN (CHUNKING) DƯỚI 512 TOKEN
# ------------------------------------------------------------------------------
# Giả định trung bình 1 từ tiếng Anh = 1.33 token -> 250 từ ~ 332 token (an toàn tuyệt đối < 512 token)

def chunk_fixed_size(documents, chunk_words=250):
    chunks = []
    chunk_idx = 0
    for doc_id, doc_data in documents.items():
        # Nối toàn văn có đánh dấu vị trí trang
        full_tokens = []
        for p in doc_data["pages"]:
            words = p["text"].split()
            for w in words:
                full_tokens.append((w, p["page_num"]))
        
        i = 0
        while i < len(full_tokens):
            chunk_slice = full_tokens[i : i + chunk_words]
            chunk_text = " ".join([w for w, _ in chunk_slice])
            pages_in_chunk = sorted(list(set([p for _, p in chunk_slice])))
            chunks.append({
                "id": f"{doc_id}_fixed_{chunk_idx}",
                "doc_id": doc_id,
                "short_name": doc_data["short_name"],
                "text": chunk_text,
                "pages": pages_in_chunk,
                "word_count": len(chunk_slice)
            })
            chunk_idx += 1
            i += chunk_words
    return chunks

def chunk_sliding_window(documents, chunk_words=250, overlap_words=50):
    chunks = []
    chunk_idx = 0
    for doc_id, doc_data in documents.items():
        full_tokens = []
        for p in doc_data["pages"]:
            words = p["text"].split()
            for w in words:
                full_tokens.append((w, p["page_num"]))
        
        i = 0
        step = chunk_words - overlap_words
        while i < len(full_tokens):
            chunk_slice = full_tokens[i : i + chunk_words]
            chunk_text = " ".join([w for w, _ in chunk_slice])
            pages_in_chunk = sorted(list(set([p for _, p in chunk_slice])))
            chunks.append({
                "id": f"{doc_id}_sliding_{chunk_idx}",
                "doc_id": doc_id,
                "short_name": doc_data["short_name"],
                "text": chunk_text,
                "pages": pages_in_chunk,
                "word_count": len(chunk_slice)
            })
            chunk_idx += 1
            i += step
            if i >= len(full_tokens):
                break
    return chunks

def chunk_recursive(documents, max_words=250):
    chunks = []
    chunk_idx = 0
    for doc_id, doc_data in documents.items():
        # Gom các trang thành các đoạn văn (paragraphs) dựa trên dấu xuống dòng hoặc chấm câu
        for p in doc_data["pages"]:
            page_text = p["text"]
            # Tách theo đoạn văn hoặc câu
            raw_sentences = re.split(r'(?<=[.!?])\s+', page_text)
            current_chunk_words = []
            
            for sentence in raw_sentences:
                words = sentence.split()
                if not words:
                    continue
                if len(current_chunk_words) + len(words) <= max_words:
                    current_chunk_words.extend(words)
                else:
                    if current_chunk_words:
                        chunk_text = " ".join(current_chunk_words)
                        chunks.append({
                            "id": f"{doc_id}_rec_{chunk_idx}",
                            "doc_id": doc_id,
                            "short_name": doc_data["short_name"],
                            "text": chunk_text,
                            "pages": [p["page_num"]],
                            "word_count": len(current_chunk_words)
                        })
                        chunk_idx += 1
                    current_chunk_words = list(words)
                    
            if current_chunk_words:
                chunk_text = " ".join(current_chunk_words)
                chunks.append({
                    "id": f"{doc_id}_rec_{chunk_idx}",
                    "doc_id": doc_id,
                    "short_name": doc_data["short_name"],
                    "text": chunk_text,
                    "pages": [p["page_num"]],
                    "word_count": len(current_chunk_words)
                })
                chunk_idx += 1
    return chunks

# ------------------------------------------------------------------------------
# 3. THUẬT TOÁN BM25 THUẦN PYTHON
# ------------------------------------------------------------------------------
class NativeBM25:
    def __init__(self, corpus_texts, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus_texts)
        self.doc_lens = []
        self.doc_freqs = []
        self.nd = {}
        
        for text in corpus_texts:
            tokens = self._tokenize(text)
            self.doc_lens.append(len(tokens))
            freqs = Counter(tokens)
            self.doc_freqs.append(freqs)
            for token in freqs.keys():
                self.nd[token] = self.nd.get(token, 0) + 1
                
        self.avgdl = sum(self.doc_lens) / (self.corpus_size + 1e-9)
        self.idf = {}
        for token, freq in self.nd.items():
            self.idf[token] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)
            
    def _tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())
        
    def score(self, query):
        q_tokens = self._tokenize(query)
        scores = np.zeros(self.corpus_size)
        for q in q_tokens:
            if q not in self.idf:
                continue
            idf_val = self.idf[q]
            for i, freqs in enumerate(self.doc_freqs):
                if q in freqs:
                    tf = freqs[q]
                    doc_len = self.doc_lens[i]
                    num = tf * (self.k1 + 1)
                    denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
                    scores[i] += idf_val * (num / denom)
        return scores

# ------------------------------------------------------------------------------
# 4. BỘ 40 CÂU HỎI TRUY VẤN CÓ GÁN NHÃN GROUND-TRUTH
# ------------------------------------------------------------------------------
GROUND_TRUTH_BENCHMARK = [
    # Lewis et al. (2020) - 8 câu
    {"qid": "Q01", "target_doc": "lewis2020", "query": "What is the mathematical formulation of the marginal probability for RAG-Sequence model?"},
    {"qid": "Q02", "target_doc": "lewis2020", "query": "How does RAG-Token marginalize over retrieved documents at each target token generation step?"},
    {"qid": "Q03", "target_doc": "lewis2020", "query": "What is the fast decoding approximation technique for RAG-Sequence proposed by Lewis et al.?"},
    {"qid": "Q04", "target_doc": "lewis2020", "query": "Which pretrained bi-encoder architecture and generator model are used in the original RAG paper?"},
    {"qid": "Q05", "target_doc": "lewis2020", "query": "How does Lewis et al. train the retriever and generator components jointly using backpropagation?"},
    {"qid": "Q06", "target_doc": "lewis2020", "query": "What are the benchmark performance results of RAG on Open-Domain QA tasks such as Natural Questions and CuratedTREC?"},
    {"qid": "Q07", "target_doc": "lewis2020", "query": "How does RAG perform on the Jeopardy question generation task compared to pure BART?"},
    {"qid": "Q08", "target_doc": "lewis2020", "query": "What is the effect of varying the number of retrieved documents k during inference in Lewis et al.?"},
    
    # Gao et al. (2023b) - 8 câu
    {"qid": "Q09", "target_doc": "gao2023", "query": "What are the structural differences between Naive RAG, Advanced RAG, and Modular RAG paradigms?"},
    {"qid": "Q10", "target_doc": "gao2023", "query": "What are the core pre-retrieval optimization techniques in Advanced RAG such as query rewriting and HyDE?"},
    {"qid": "Q11", "target_doc": "gao2023", "query": "How does post-retrieval processing optimize context using cross-encoder reranking and context compression?"},
    {"qid": "Q12", "target_doc": "gao2023", "query": "What are the core evaluation metrics of the RAGAS framework including Faithfulness and Answer Relevance?"},
    {"qid": "Q13", "target_doc": "gao2023", "query": "How does Modular RAG incorporate specialized modules like Search, Memory, and Predict?"},
    {"qid": "Q14", "target_doc": "gao2023", "query": "What are the multi-hop reasoning challenges and iterative retrieval strategies in RAG systems?"},
    {"qid": "Q15", "target_doc": "gao2023", "query": "What are the trade-offs between dense retrieval, sparse retrieval, and hybrid retrieval mentioned by Gao et al.?"},
    {"qid": "Q16", "target_doc": "gao2023", "query": "How does external retrieval augment the training and fine-tuning phases of LLMs according to the survey?"},

    # Zhao et al. (2024) - 8 câu
    {"qid": "Q17", "target_doc": "zhao2024", "query": "What is the four-stage classification of RAG based on augmentation stages: query-based, latent-based, logit-based, and speculative?"},
    {"qid": "Q18", "target_doc": "zhao2024", "query": "How does latent representation-based RAG fuse retrieved representations into hidden states?"},
    {"qid": "Q19", "target_doc": "zhao2024", "query": "What is logit-based RAG and how does it adjust output probability distributions using kNN-LM?"},
    {"qid": "Q20", "target_doc": "zhao2024", "query": "What is Speculative RAG and how does it utilize a smaller drafter model with parallel verification?"},
    {"qid": "Q21", "target_doc": "zhao2024", "query": "How is RAG extended to multimodal AI-generated content including images, code, and audio generation?"},
    {"qid": "Q22", "target_doc": "zhao2024", "query": "What are the common retrieval objects in multimodal RAG such as image patches and audio spectrograms?"},
    {"qid": "Q23", "target_doc": "zhao2024", "query": "What evaluation benchmarks and metrics are surveyed for AI-Generated Content in Zhao et al.?"},
    {"qid": "Q24", "target_doc": "zhao2024", "query": "What are the prospective future challenges for RAG in long-form generation and dynamic knowledge updates?"},

    # Huang & Huang (2024) - 8 câu
    {"qid": "Q25", "target_doc": "huang2024", "query": "What are the multi-step interaction paradigms between retriever and generator: iterative, recursive, and adaptive?"},
    {"qid": "Q26", "target_doc": "huang2024", "query": "How does Self-RAG train reflection tokens to decide when to retrieve and critique output quality?"},
    {"qid": "Q27", "target_doc": "huang2024", "query": "What is Corrective RAG (CRAG) and how does it evaluate retrieval confidence with web fallback?"},
    {"qid": "Q28", "target_doc": "huang2024", "query": "What are the typical retrieval failure modes analyzed: retrieval noise, negative rejection, and false negative errors?"},
    {"qid": "Q29", "target_doc": "huang2024", "query": "How do active retrieval mechanisms decide when retrieval is necessary during text generation?"},
    {"qid": "Q30", "target_doc": "huang2024", "query": "What is the comparison between RAG and long-context language models in terms of cost, latency, and memory?"},
    {"qid": "Q31", "target_doc": "huang2024", "query": "How does prompt compression reduce token cost and eliminate distracting information before generation?"},
    {"qid": "Q32", "target_doc": "huang2024", "query": "What are the security vulnerabilities of RAG such as prompt injection and corpus poisoning attacks?"},

    # Petroni et al. (2021) - 8 câu
    {"qid": "Q33", "target_doc": "petroni2021", "query": "What is the structure of the KILT benchmark and how many tasks across how many domains does it include?"},
    {"qid": "Q34", "target_doc": "petroni2021", "query": "How does KILT map disparate knowledge-intensive NLP tasks to a single unified Wikipedia knowledge source?"},
    {"qid": "Q35", "target_doc": "petroni2021", "query": "What is the KILT-AC provenance-aware evaluation metric that requires both task accuracy and correct provenance citation?"},
    {"qid": "Q36", "target_doc": "petroni2021", "query": "What Wikipedia snapshot version is used as the standardized non-parametric memory in KILT?"},
    {"qid": "Q37", "target_doc": "petroni2021", "query": "How does KILT define provenance tracking at the document, section, and paragraph levels?"},
    {"qid": "Q38", "target_doc": "petroni2021", "query": "What are the baseline model architectures evaluated on the KILT leaderboard including DPR, RAG, and BART?"},
    {"qid": "Q39", "target_doc": "petroni2021", "query": "What are the findings regarding the discrepancy between task accuracy and provenance accuracy on KILT?"},
    {"qid": "Q40", "target_doc": "petroni2021", "query": "How does the FEVER fact-checking dataset adapt to the KILT unified formulation?"}
]

# ------------------------------------------------------------------------------
# 5. HÀM TÍNH TOÁN CÁC CHỈ SỐ ĐỊNH LƯỢNG (HIT@K, MRR@K, RECALL@K, NDCG@K)
# ------------------------------------------------------------------------------
def evaluate_retrieval(ranked_doc_ids, target_doc, top_k=5):
    """
    ranked_doc_ids: list các doc_id trả về theo thứ tự từ hạng 1 đến k
    target_doc: doc_id đúng
    """
    top_ranks = ranked_doc_ids[:top_k]
    
    # Hit@k
    hit_1 = 1.0 if len(top_ranks) > 0 and top_ranks[0] == target_doc else 0.0
    hit_3 = 1.0 if target_doc in top_ranks[:3] else 0.0
    hit_5 = 1.0 if target_doc in top_ranks[:5] else 0.0
    
    # MRR@k
    mrr_5 = 0.0
    for rank_idx, doc_id in enumerate(top_ranks, 1):
        if doc_id == target_doc:
            mrr_5 = 1.0 / rank_idx
            break
            
    # Recall@5: Trong bài toán này mỗi câu hỏi có 1 target_doc chủ đạo
    recall_5 = 1.0 if target_doc in top_ranks[:5] else 0.0
    
    # nDCG@5
    dcg = 0.0
    idcg = 1.0  # Vì chỉ có 1 ground truth rank 1 lý tưởng
    for rank_idx, doc_id in enumerate(top_ranks, 1):
        if doc_id == target_doc:
            dcg = 1.0 / math.log2(rank_idx + 1)
            break
    ndcg_5 = dcg / idcg
    
    return {
        "hit@1": hit_1,
        "hit@3": hit_3,
        "hit@5": hit_5,
        "mrr@5": mrr_5,
        "recall@5": recall_5,
        "ndcg@5": ndcg_5
    }

# ------------------------------------------------------------------------------
# 6. QUY TRÌNH THỰC THI THỰC NGHIỆM
# ------------------------------------------------------------------------------
def run_all_experiments():
    from fastembed import TextEmbedding
    
    docs = load_documents("papers")
    
    chunk_strategies = {
        "Fixed-size (250w, 0ov)": chunk_fixed_size(docs, chunk_words=250),
        "Sliding Window (250w, 50ov)": chunk_sliding_window(docs, chunk_words=250, overlap_words=50),
        "Recursive Structure-aware": chunk_recursive(docs, max_words=250)
    }
    
    for strat_name, chks in chunk_strategies.items():
        print(f"[*] Chiến lược '{strat_name}': sinh {len(chks)} chunks.")
        
    # Khởi tạo mô hình nhúng
    print("\n[*] Nạp mô hình FastEmbed: BAAI/bge-small-en-v1.5...")
    bge_embed = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    print("[*] Nạp mô hình FastEmbed: sentence-transformers/all-MiniLM-L6-v2...")
    minilm_embed = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    final_results = {}
    detailed_query_log = []
    
    for strat_name, chunks in chunk_strategies.items():
        print(f"\n" + "=" * 60)
        print(f" THỰC NGHIỆM TRÊN CHIẾN LƯỢC: {strat_name} (Tổng {len(chunks)} chunks)")
        print("=" * 60)
        
        chunk_texts = [c["text"] for c in chunks]
        chunk_doc_ids = [c["doc_id"] for c in chunks]
        
        # 1. Đo lường BM25
        t0 = time.perf_counter()
        bm25 = NativeBM25(chunk_texts)
        t_bm25_index = (time.perf_counter() - t0) * 1000
        
        # 2. Đo lường Nhúng BGE
        print(f"  [*] Bắt đầu sinh vector nhúng BGE-small (batch_size=1)...")
        t0 = time.perf_counter()
        bge_embeddings = []
        for c_idx, chunk_t in enumerate(chunk_texts):
            emb = list(bge_embed.embed([chunk_t], batch_size=1))[0]
            bge_embeddings.append(emb)
            if (c_idx + 1) % 100 == 0 or (c_idx + 1) == len(chunk_texts):
                print(f"      -> BGE đã nhúng {c_idx + 1}/{len(chunk_texts)} chunks...")
        bge_emb_mat = np.array(bge_embeddings, dtype=np.float32)
        # Normalize
        bge_norms = np.linalg.norm(bge_emb_mat, axis=1, keepdims=True) + 1e-9
        bge_emb_norm = bge_emb_mat / bge_norms
        t_bge_index = time.perf_counter() - t0
        
        # 3. Đo lường Nhúng MiniLM
        print(f"  [*] Bắt đầu sinh vector nhúng MiniLM-L6 (batch_size=1)...")
        t0 = time.perf_counter()
        minilm_embeddings = []
        for c_idx, chunk_t in enumerate(chunk_texts):
            emb = list(minilm_embed.embed([chunk_t], batch_size=1))[0]
            minilm_embeddings.append(emb)
            if (c_idx + 1) % 100 == 0 or (c_idx + 1) == len(chunk_texts):
                print(f"      -> MiniLM đã nhúng {c_idx + 1}/{len(chunk_texts)} chunks...")
        minilm_emb_mat = np.array(minilm_embeddings, dtype=np.float32)
        minilm_norms = np.linalg.norm(minilm_emb_mat, axis=1, keepdims=True) + 1e-9
        minilm_emb_norm = minilm_emb_mat / minilm_norms
        t_minilm_index = time.perf_counter() - t0
        
        print(f"  [+] Thời gian lập chỉ mục BM25: {t_bm25_index:.1f} ms")
        print(f"  [+] Thời gian nhúng BGE-small: {t_bge_index:.2f} s ({t_bge_index/len(chunks)*1000:.2f} ms/chunk)")
        print(f"  [+] Thời gian nhúng MiniLM-L6: {t_minilm_index:.2f} s ({t_minilm_index/len(chunks)*1000:.2f} ms/chunk)")
        
        # Chạy kiểm thử trên 40 câu hỏi
        methods = ["BM25", "MiniLM-L6-v2", "BGE-small-v1.5"]
        metrics_by_method = {m: {"hit@1": [], "hit@3": [], "hit@5": [], "mrr@5": [], "recall@5": [], "ndcg@5": [], "latency_ms": []} for m in methods}
        
        for q_item in GROUND_TRUTH_BENCHMARK:
            query = q_item["query"]
            target = q_item["target_doc"]
            qid = q_item["qid"]
            
            # --- BM25 ---
            tq0 = time.perf_counter()
            bm25_scores = bm25.score(query)
            top_bm25_indices = np.argsort(bm25_scores)[::-1][:5]
            lat_bm25 = (time.perf_counter() - tq0) * 1000
            bm25_ranked_docs = [chunk_doc_ids[idx] for idx in top_bm25_indices]
            res_bm25 = evaluate_retrieval(bm25_ranked_docs, target, top_k=5)
            for k_m, v_m in res_bm25.items():
                metrics_by_method["BM25"][k_m].append(v_m)
            metrics_by_method["BM25"]["latency_ms"].append(lat_bm25)
            
            # --- MiniLM ---
            tq0 = time.perf_counter()
            q_emb_m = list(minilm_embed.embed([query]))[0]
            q_emb_m = q_emb_m / (np.linalg.norm(q_emb_m) + 1e-9)
            sims_m = np.dot(minilm_emb_norm, q_emb_m)
            top_m_indices = np.argsort(sims_m)[::-1][:5]
            lat_m = (time.perf_counter() - tq0) * 1000
            m_ranked_docs = [chunk_doc_ids[idx] for idx in top_m_indices]
            res_m = evaluate_retrieval(m_ranked_docs, target, top_k=5)
            for k_m, v_m in res_m.items():
                metrics_by_method["MiniLM-L6-v2"][k_m].append(v_m)
            metrics_by_method["MiniLM-L6-v2"]["latency_ms"].append(lat_m)
            
            # --- BGE with Instruction ---
            tq0 = time.perf_counter()
            bge_query_text = f"Represent this sentence for searching relevant passages: {query}"
            q_emb_b = list(bge_embed.embed([bge_query_text]))[0]
            q_emb_b = q_emb_b / (np.linalg.norm(q_emb_b) + 1e-9)
            sims_b = np.dot(bge_emb_norm, q_emb_b)
            top_b_indices = np.argsort(sims_b)[::-1][:5]
            lat_b = (time.perf_counter() - tq0) * 1000
            b_ranked_docs = [chunk_doc_ids[idx] for idx in top_b_indices]
            res_b = evaluate_retrieval(b_ranked_docs, target, top_k=5)
            for k_m, v_m in res_b.items():
                metrics_by_method["BGE-small-v1.5"][k_m].append(v_m)
            metrics_by_method["BGE-small-v1.5"]["latency_ms"].append(lat_b)
            
            if strat_name == "Sliding Window (250w, 50ov)":
                detailed_query_log.append({
                    "qid": qid,
                    "query": query,
                    "target": target,
                    "bge_top1_doc": b_ranked_docs[0],
                    "bge_top1_score": float(sims_b[top_b_indices[0]]),
                    "bge_top_ranks": b_ranked_docs,
                    "bge_hit@1": res_b["hit@1"],
                    "bge_hit@5": res_b["hit@5"]
                })
                
        # Tổng hợp chỉ số trung bình
        strat_summary = {}
        for m in methods:
            strat_summary[m] = {
                "hit@1": float(np.mean(metrics_by_method[m]["hit@1"])),
                "hit@3": float(np.mean(metrics_by_method[m]["hit@3"])),
                "hit@5": float(np.mean(metrics_by_method[m]["hit@5"])),
                "mrr@5": float(np.mean(metrics_by_method[m]["mrr@5"])),
                "recall@5": float(np.mean(metrics_by_method[m]["recall@5"])),
                "ndcg@5": float(np.mean(metrics_by_method[m]["ndcg@5"])),
                "latency_ms": float(np.mean(metrics_by_method[m]["latency_ms"]))
            }
            print(f"  -> Phương pháp [{m:15s}]: Hit@1={strat_summary[m]['hit@1']:.3f} | Hit@5={strat_summary[m]['hit@5']:.3f} | MRR@5={strat_summary[m]['mrr@5']:.3f} | nDCG@5={strat_summary[m]['ndcg@5']:.3f} | Latency={strat_summary[m]['latency_ms']:.2f}ms")
            
        final_results[strat_name] = {
            "chunk_count": len(chunks),
            "bge_index_time_s": t_bge_index,
            "minilm_index_time_s": t_minilm_index,
            "summary": strat_summary
        }

    # Lưu kết quả thực nghiệm ra JSON
    out_file = "benchmark_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "hardware": {
                "cpu": "Intel Core i7-7700HQ @ 2.80GHz",
                "cores": "4 cores / 8 threads",
                "ram": "16 GB DDR4",
                "runtime": "ONNX Runtime CPU Execution Provider (AVX2)"
            },
            "benchmark_results": final_results,
            "sample_query_logs": detailed_query_log
        }, f, indent=2, ensure_ascii=False)
        
    print(f"\n[OK] Toàn bộ kết quả thực nghiệm thực tế đã được lưu tại: {out_file}")

if __name__ == "__main__":
    run_all_experiments()
