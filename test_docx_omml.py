# -*- coding: utf-8 -*-
import docx
import lxml.etree as etree
from latex2mathml.converter import convert

xslt_path = r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL"
xslt_doc = etree.parse(xslt_path)
transform = etree.XSLT(xslt_doc)

doc = docx.Document()
p = doc.add_paragraph()

latex = r"p_{\text{RAG-Token}}(y|x) = \prod_{i=1}^N \sum_{z \in \text{top-}k} p_\eta(z|x) \cdot p_\theta(y_i|x, z, y_{1:i-1})"
mathml = convert(latex)
tree = etree.fromstring(mathml)
omml = transform(tree)

# In OMML transform, the root element might be <m:oMath> or document
omml_element = omml.getroot()
# Append to paragraph XML element
p._p.append(omml_element)

test_docx = "test_math_output.docx"
doc.save(test_docx)
print(f"[OK] Successfully saved {test_docx} with native OMML equation!")
