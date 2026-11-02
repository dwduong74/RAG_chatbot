# -*- coding: utf-8 -*-
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER

doc = docx.Document()
p = doc.add_paragraph()
p.paragraph_format.tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
r1 = p.add_run("CHƯƠNG 1: ĐẶT VẤN ĐỀ")
r1.bold = True
r2 = p.add_run("\tTrang 1")
doc.save("test_toc.docx")
print("Saved test_toc.docx successfully!")
