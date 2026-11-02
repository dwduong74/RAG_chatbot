import json
import numpy as np

with open("benchmark_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

logs = data["sample_query_logs"]

correct_scores = []
incorrect_scores = []
misses = []

for q in logs:
    score = q["bge_top1_score"]
    if q["bge_hit@1"] == 1.0:
        correct_scores.append(score)
    else:
        incorrect_scores.append(score)
        misses.append(q)

print(f"Total queries: {len(logs)}")
print(f"Correct Hit@1: {len(correct_scores)} (Mean: {np.mean(correct_scores):.4f}, Std: {np.std(correct_scores):.4f})")
print(f"Incorrect Hit@1 (Misses): {len(incorrect_scores)} (Mean: {np.mean(incorrect_scores):.4f}, Std: {np.std(incorrect_scores):.4f})")
print("-" * 60)
print(f"All {len(misses)} Misses at Hit@1:")
for m in misses:
    print(f"  {m['qid']}: Target={m['target']} -> Top1={m['bge_top1_doc']} (score={m['bge_top1_score']:.4f})")
    print(f"     Query: {m['query']}")
    print(f"     Ranks: {m['bge_top_ranks']}")
