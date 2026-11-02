# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md', 'r', encoding='utf-8') as f:
    text = f.read()

formulas = re.findall(r'\$\$([^\$]+)\$\$', text)
print(f"Total $$ formulas: {len(formulas)}")
for i, f in enumerate(formulas):
    has_tab = '\t' in f
    print(f"[{i+1}] Has Tab: {has_tab}")
    print(repr(f))

inline_formulas = re.findall(r'\$([^\$\n]+)\$', text)
print(f"\nTotal $ inline formulas: {len(inline_formulas)}")
tab_inlines = [f for f in inline_formulas if '\t' in f]
print(f"Inline formulas with tab: {len(tab_inlines)}")
for f in tab_inlines:
    print(repr(f))
