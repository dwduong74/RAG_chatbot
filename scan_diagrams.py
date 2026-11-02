# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Match code blocks: ```...``` or un-fenced ASCII art
code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
print(f"Total code blocks: {len(code_blocks)}")

ascii_diagrams = []
for i, b in enumerate(code_blocks):
    is_ascii = any(char in b for char in ['+--', '├──', '└──', '──>', '+====', '|    NAIVE RAG'])
    if is_ascii:
        ascii_diagrams.append((i, b.strip()))

print(f"Total ASCII diagrams in code blocks: {len(ascii_diagrams)}")
for idx, (i, content) in enumerate(ascii_diagrams):
    print(f"\n==================== DIAGRAM {idx+1} (Block #{i+1}) ====================")
    lines = content.split('\n')
    for l in lines[:15]:
        print(l)
    if len(lines) > 15:
        print(f"... ({len(lines) - 15} more lines)")
