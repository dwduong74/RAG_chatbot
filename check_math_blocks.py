import re
import lxml.etree as etree
from latex2mathml.converter import convert

xslt_path = r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL"
xslt_doc = etree.parse(xslt_path)
transform = etree.XSLT(xslt_doc)

with open("BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md", "r", encoding="utf-8") as f:
    text = f.read()

display_maths = re.findall(r"\$\$(.*?)\$\$", text, re.DOTALL)
print(f"Total display math blocks: {len(display_maths)}")

success = 0
failed = []
for idx, m in enumerate(display_maths, 1):
    cleaned = m.strip()
    try:
        mathml = convert(cleaned)
        tree = etree.fromstring(mathml)
        omml = transform(tree)
        root = omml.getroot()
        if root is not None:
            success += 1
        else:
            failed.append((idx, cleaned, "Root is None"))
    except Exception as e:
        failed.append((idx, cleaned, str(e)))

print(f"Converted: {success}/{len(display_maths)}")
if failed:
    print("Failed blocks:")
    for idx, c, err in failed:
        print(f"  [{idx}] {err}: {c[:60]}...")
