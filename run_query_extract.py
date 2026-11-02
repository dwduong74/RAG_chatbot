import sys
from query_rag import PaperRAGRetriever

retriever = PaperRAGRetriever()

queries = [
    ("Q01", "What is the mathematical formulation of the marginal probability for RAG-Sequence model?"),
    ("Q04", "Which pretrained bi-encoder architecture and generator model are used in the original RAG paper?"),
    ("Q33", "What is the structure of the KILT benchmark and how many tasks across how many domains does it include?")
]

print("=" * 80)
print("EXTRACTING DETAILED RETRIEVAL RESULTS FOR TABLE 4.4")
print("=" * 80)

for qid, qtext in queries:
    print(f"\n[{qid}] Query: '{qtext}'")
    hits = retriever.search(qtext, top_k=5)
    for idx, hit in enumerate(hits, 1):
        fn = hit['metadata'].get('file_name', 'N/A')
        pages = hit['metadata'].get('pages', 'N/A')
        score = hit['score']
        cid = hit['id']
        snippet = hit['text'][:220].replace('\n', ' ')
        print(f"  Rank {idx}: Score={score:.4f} | File={fn} (Trang {pages}) | ID={cid}")
        print(f"    Text: {snippet}...")
