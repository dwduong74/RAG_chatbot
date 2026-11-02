# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Scanning BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md for parenthetical English...")

# Match patterns where Vietnamese text is immediately followed by (English text)
# e.g., "Bộ nhớ tham số (Parametric Memory)"
pattern = re.compile(r'([A-ZÀ-Ỹa-zà-ỹ\s]{3,})\(([A-Za-z\s\-_/]{4,})\)')

hits = []
for idx, line in enumerate(lines):
    line_clean = line.strip()
    if line_clean.startswith('```') or line_clean.startswith('$$') or line_clean.startswith('|'):
        continue
    for m in pattern.finditer(line):
        vn_part = m.group(1).strip()
        en_part = m.group(2).strip()
        # ignore authors/citations
        if any(w in en_part.lower() for w in ['et al', 'lewis', 'gao', 'zhao', 'huang', 'petroni', 'khattab', 'vaswani', 'devlin', 'brown']):
            continue
        # ignore formula symbols or abbreviations like PDF, CPU, GPU, API
        if en_part.upper() in ['PDF', 'CSDL', 'CPU', 'GPU', 'TPU', 'API', 'JSON', 'REST', 'SQL', 'HNSW', 'BM25']:
            continue
        hits.append((idx + 1, vn_part, en_part, line.strip()))

print(f"Total suspect parenthetical hits: {len(hits)}")
for h in hits[:30]:
    print(f"Line {h[0]}: ...{h[1][-25:]} ({h[2]})")
