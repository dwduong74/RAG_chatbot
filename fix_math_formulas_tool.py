# -*- coding: utf-8 -*-
"""
Tool tự động sửa lỗi công thức toán học và tích hợp OMML Equation cho Microsoft Word 2016.
Các chức năng cốt lõi:
1. Khắc phục triệt để lỗi ký tự thoát (Escape Characters) trong chuỗi Python:
   - '\t' + 'ext' -> '\\text'
   - '\t' + 'heta' -> '\\theta'
   - '\t' + 'au' -> '\\tau'
   - '\x0c' + 'rac' (FormFeed) -> '\\frac'
2. Chuyển đổi định nghĩa chuỗi trong các file mã nguồn sang raw string r\"\"\"...\"\"\"
3. Tích hợp bộ chuyển đổi LaTeX -> MathML -> OMML (Office Math Markup Language)
   thông qua MML2OMML.XSL chính hãng của Microsoft Word 2016 để hiển thị phương trình toán học
   chuẩn bản quyền (Native Equation) trong file .docx.
"""

import sys
import os
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def clean_math_text(s):
    """
    Sửa triệt để các ký tự tab và formfeed trong công thức.
    """
    # Thay thế formfeed \x0crac -> \frac
    s = s.replace('\x0crac', r'\frac')
    # Thay thế tab \text -> \text
    s = s.replace('\text', r'\text')
    # Thay thế tab \theta -> \theta
    s = s.replace('\theta', r'\theta')
    # Thay thế tab \tau -> \tau
    s = s.replace('\tau', r'\tau')
    return s

def fix_content_file(filepath, var_name):
    print(f"[*] Fixing math escapes in: {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    # Sửa các chuỗi lỗi
    code = code.replace('\x0crac', r'\frac')
    code = code.replace('\text', r'\text')
    code = code.replace('\theta', r'\theta')
    code = code.replace('\tau', r'\tau')

    # Đảm bảo dùng raw string r"""
    pattern = rf'({var_name}\s*=\s*)"""'
    if re.search(pattern, code):
        code = re.sub(pattern, r'\1r"""', code)
        print(f"    [+] Ensured {var_name} uses raw string r\"\"\"")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"    [OK] File {filepath} updated successfully.")

def update_compiler_with_omml():
    print("[*] Integrating OMML Math engine into compile_research_report.py...")
    
    with open("compile_research_report.py", "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Thêm import và cấu hình OMML nếu chưa có
    if "latex_to_omml" not in code:
        omml_header = """import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import lxml.etree as etree
from latex2mathml.converter import convert

XSLT_PATH = r"C:\\Program Files\\Microsoft Office\\Office16\\MML2OMML.XSL"
_omml_transform = None
if os.path.exists(XSLT_PATH):
    try:
        _xslt_doc = etree.parse(XSLT_PATH)
        _omml_transform = etree.XSLT(_xslt_doc)
    except Exception:
        _omml_transform = None

def clean_formula_str(s):
    if not s:
        return ""
    s = s.replace('\\x0crac', r'\\frac')
    s = s.replace('\\text', r'\\text')
    s = s.replace('\\theta', r'\\theta')
    s = s.replace('\\tau', r'\\tau')
    s = s.replace('\\t', ' ')
    return re.sub(r' +', ' ', s).strip()

def latex_to_omml(latex_code):
    if _omml_transform is None:
        return None
    clean_s = clean_formula_str(latex_code)
    try:
        mathml = convert(clean_s)
        tree = etree.fromstring(mathml)
        omml = _omml_transform(tree)
        return omml.getroot()
    except Exception:
        try:
            # Fallback đơn giản hóa thẻ \\text
            simplified = re.sub(r'\\\\text\\{([^}]+)\\}', r'\\1', clean_s)
            mathml = convert(simplified)
            tree = etree.fromstring(mathml)
            omml = _omml_transform(tree)
            return omml.getroot()
        except Exception:
            return None
"""
        # Thay thế khối import đầu file
        old_import_block = """import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn"""

        code = code.replace(old_import_block, omml_header)

    # 2. Xử lý đoạn hiển thị Display Math $$...$$ trong vòng lặp parse lines
    if "# Display Math ($$...$$)" not in code:
        # Tìm vị trí trước # Bullet list
        bullet_marker = "# Bullet list (- or *)"
        display_math_handler = """        # Display Math ($$...$$)
        clean_strip = line.strip()
        if clean_strip.startswith("$$") and clean_strip.endswith("$$") and len(clean_strip) > 4:
            math_code = clean_strip[2:-2].strip()
            math_code = clean_formula_str(math_code)
            
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(8)
            
            omml_elem = latex_to_omml(math_code)
            if omml_elem is not None:
                p._p.append(omml_elem)
            else:
                # Fallback định dạng Cambria Math
                r = p.add_run(math_code)
                r.font.name = "Cambria Math"
                r.font.size = Pt(12)
                r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            i += 1
            continue

        """ + bullet_marker
        code = code.replace(bullet_marker, display_math_handler)

    # 3. Làm sạch công thức trong đoạn văn thông thường
    code = code.replace("clean_part = sanitize_xml(part)", "clean_part = clean_formula_str(sanitize_xml(part))")

    with open("compile_research_report.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("    [OK] compile_research_report.py successfully updated with OMML Math engine.")

def main():
    print("=" * 70)
    print(" CÔNG CỤ SỬA LỖI CÔNG THỨC TOÁN & TÍCH HỢP OMML EQUATION WORD 2016")
    print("=" * 70)

    # Bước 1: Sửa các ký tự escape trong các file nguồn
    fix_content_file("report_content_part1.py", "CHAPTERS_PART_1")
    fix_content_file("report_content_part2.py", "CHAPTERS_PART_2")
    fix_content_file("report_content_part3.py", "CHAPTERS_PART_3")
    fix_content_file("report_content_appendices.py", "APPENDICES_AND_EXTENSIONS")

    # Bước 2: Nâng cấp script biên dịch Word với engine OMML
    update_compiler_with_omml()

    # Bước 3: Tái biên dịch toàn bộ báo cáo
    print("\n[*] Re-compiling report into Markdown and Word .docx...")
    import importlib
    import report_content_part1
    import report_content_part2
    import report_content_part3
    import report_content_appendices
    import compile_research_report

    importlib.reload(report_content_part1)
    importlib.reload(report_content_part2)
    importlib.reload(report_content_part3)
    importlib.reload(report_content_appendices)
    importlib.reload(compile_research_report)

    compile_research_report.main()
    print("\n[✓] Hoàn tất quá trình sửa lỗi công thức toán và xuất bản!")

if __name__ == "__main__":
    main()
