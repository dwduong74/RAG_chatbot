import math
import numpy as np
from experiment_benchmark import load_documents, chunk_sliding_window, FastEmbedWrapper, GROUND_TRUTH_BENCHMARK

print("Loading documents and sliding window chunks...")
docs = load_documents()
chunks = chunk_sliding_window(docs, chunk_words=250, overlap_words=50)

print(f"Total chunks: {len(chunks)}")
chunk_texts = [c["text"] for c in chunks]

print("Initializing BGE embedder...")
bge_embedder = FastEmbedWrapper("BAAI/bge-small-en-v1.5")
chunk_embeddings = bge_embedder.embed(chunk_texts, batch_size=16)

queries_to_extract = ["Q01", "Q04", "Q33"]

for q in GROUND_TRUTH_BENCHMARK:
    if q["qid"] in queries_to_extract:
        qid = q["qid"]
        query_text = q["query"]
        target_doc = q["target_doc"]
        
        # BGE query prefix
        prefixed_q = "Represent this sentence for searching relevant passages: " + query_text
        q_vec = bge_embedder.embed([prefixed_q], batch_size=1)[0]
        
        # Cosine similarity
        scores = np.dot(chunk_embeddings, q_vec)
        top5_indices = np.argsort(scores)[::-1][:5]
        
        print("\n" + "=" * 80)
        print(f"QUERY {qid}: {query_text}")
        print(f"Target Document: {target_doc}")
        print("=" * 80)
        
        for rank, idx in enumerate(top5_indices, 1):
            c = chunks[idx]
            sim = float(scores[idx])
            pages_str = ", ".join(str(p) for p in c["pages"])
            text_preview = c["text"][:180].replace("\n", " ")
            print(f"Rank {rank}:")
            print(f"  Doc: {c['short_name']} ({c['doc_id']})")
            print(f"  Pages: {pages_str}")
            print(f"  Cosine Score: {sim:.4f}")
            print(f"  Excerpt: {text_preview}...")
