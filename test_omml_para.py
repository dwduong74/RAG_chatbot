# -*- coding: utf-8 -*-
import docx
import lxml.etree as etree
from latex2mathml.converter import convert

XSLT_PATH = r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL"
xslt_doc = etree.parse(XSLT_PATH)
transform = etree.XSLT(xslt_doc)

def latex_to_omml(latex_code):
    try:
        mathml = convert(latex_code)
        tree = etree.fromstring(mathml)
        omml = transform(tree)
        return omml.getroot()
    except Exception as e:
        print(f"Error converting '{latex_code}': {e}")
        return None

doc = docx.Document()
p = doc.add_paragraph()
p.add_run("Phương trình biên: ")

# Convert inline math
omml_elem = latex_to_omml(r"P(y \mid x) = \sum_{z \in \text{top-}k} P(z \mid x)")
if omml_elem is not None:
    p._p.append(omml_elem)

p.add_run(" là công thức nền tảng.")

# Display math
p2 = doc.add_paragraph()
omml_block = latex_to_omml(r"\frac{\vec{q} \cdot \vec{d}_i}{\|\vec{q}\|_2 \|\vec{d}_i\|_2}")
if omml_block is not None:
    # Wrap in oMathPara
    omathpara = etree.Element("{http://schemas.openxmlformats.org/officeDocument/2006/math}oMathPara")
    omathpara.append(omml_block)
    p2._p.append(omathpara)

doc.save("test_equation.docx")
print("Saved test_equation.docx successfully!")
