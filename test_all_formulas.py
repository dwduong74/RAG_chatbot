# -*- coding: utf-8 -*-
import sys
import re
import lxml.etree as etree
from latex2mathml.converter import convert

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

XSLT_PATH = r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL"
xslt_doc = etree.parse(XSLT_PATH)
transform = etree.XSLT(xslt_doc)

def clean_formula_str(s):
    if not s:
        return ""
    # DO NOT replace \t with space!
    s = s.replace('\x0crac', r'\frac')
    return re.sub(r' +', ' ', s).strip()

def latex_to_omml(latex_code):
    clean_s = clean_formula_str(latex_code)
    try:
        mathml = convert(clean_s)
        tree = etree.fromstring(mathml)
        omml = transform(tree)
        return omml.getroot()
    except Exception as e:
        # Retry with text simplifications
        try:
            # Replace Vietnamese in \text{} or similar if any
            simplified = re.sub(r'\\text\{([^}]+)\}', lambda m: m.group(1).replace(' ', '~'), clean_s)
            mathml = convert(simplified)
            tree = etree.fromstring(mathml)
            omml = transform(tree)
            return omml.getroot()
        except Exception as e2:
            return None

with open('BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md', 'r', encoding='utf-8') as f:
    text = f.read()

display_formulas = re.findall(r'\$\$([^\$]+)\$\$', text)
print(f"=== TESTING {len(display_formulas)} DISPLAY FORMULAS ===")
failed_display = []
for i, f in enumerate(display_formulas):
    res = latex_to_omml(f)
    if res is None:
        print(f"FAILED Display [{i+1}]: {f}")
        failed_display.append((i+1, f))
    else:
        print(f"OK Display [{i+1}]")

print(f"Display formulas success: {len(display_formulas) - len(failed_display)}/{len(display_formulas)}")

inline_formulas = re.findall(r'\$([^\$\n]+)\$', text)
print(f"\n=== TESTING {len(inline_formulas)} INLINE FORMULAS ===")
failed_inline = []
for i, f in enumerate(inline_formulas):
    res = latex_to_omml(f)
    if res is None:
        failed_inline.append((i+1, f))

print(f"Inline formulas success: {len(inline_formulas) - len(failed_inline)}/{len(inline_formulas)}")
if failed_inline:
    print(f"Sample failed inlines (first 10):")
    for idx, f in failed_inline[:10]:
        print(f"  [{idx}] {repr(f)}")
