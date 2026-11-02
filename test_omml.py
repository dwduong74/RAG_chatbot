# -*- coding: utf-8 -*-
import sys
import lxml.etree as etree
import latex2mathml.commands
from latex2mathml.converter import convert

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

xslt_path = r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL"
xslt_doc = etree.parse(xslt_path)
transform = etree.XSLT(xslt_doc)

latex = r"p_{\text{RAG-Token}}(y|x) = \prod_{i=1}^N \sum_{z \in \text{top-}k} p_\eta(z|x) \cdot p_\theta(y_i|x, z, y_{1:i-1})"
print("Testing LaTeX:", latex)

mathml = convert(latex)
print("\nGenerated MathML:\n", mathml[:200], "...")

tree = etree.fromstring(mathml)
omml = transform(tree)
print("\nGenerated OMML:\n", etree.tostring(omml, encoding='unicode')[:300], "...")
print("\n[OK] OMML transformation works perfectly!")
