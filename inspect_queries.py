import json

with open("benchmark_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for q in data["sample_query_logs"]:
    if q["qid"] in ["Q01", "Q04", "Q33"]:
        print(f"QID: {q['qid']}")
        print(f"  Query: {q['query']}")
        print(f"  Target: {q['target']}")
        print(f"  Top-1 Doc: {q['bge_top1_doc']}")
        print(f"  Top-1 Score: {q['bge_top1_score']}")
        print(f"  Ranks: {q['bge_top_ranks']}")
        print(f"  Hit@1: {q['bge_hit@1']}, Hit@5: {q['bge_hit@5']}")
        print("-" * 50)
