# -*- coding: utf-8 -*-
"""
Script biên dịch toàn văn Báo cáo Nghiên cứu Khoa học RAG
Tạo ra đồng thời:
1. BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md (Master Markdown)
2. BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.docx (Word chuẩn NCKH Học viện Công nghệ Bưu chính Viễn thông)
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import lxml.etree as etree
try:
    from latex2mathml.converter import convert
except ImportError:
    convert = None

XSLT_PATH = r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL"
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
    # Chuẩn hóa các chuỗi escape
    s = s.replace('\x0crac', r'\frac')
    return re.sub(r' +', ' ', s).strip()

def latex_to_omml(latex_code):
    if _omml_transform is None or convert is None:
        return None
    clean_s = clean_formula_str(latex_code)
    try:
        mathml = convert(clean_s)
        tree = etree.fromstring(mathml)
        omml = _omml_transform(tree)
        return omml.getroot()
    except Exception:
        try:
            simplified = re.sub(r'\\text\{([^}]+)\}', lambda m: m.group(1).replace(' ', '~'), clean_s)
            mathml = convert(simplified)
            tree = etree.fromstring(mathml)
            omml = _omml_transform(tree)
            return omml.getroot()
        except Exception:
            return None

from v2_meta_references import REPORT_META_AND_ABSTRACT, REPORT_REFERENCES_AND_APPENDICES
from v2_chapter1 import CHAPTER_1
from v2_chapter2 import CHAPTER_2
from v2_chapter3 import CHAPTER_3
from v2_chapter4 import CHAPTER_4
from v2_discussion_conclusion import CHAPTER_5

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def sanitize_xml(text):
    if not text:
        return ""
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', str(text))

def format_inline_math_text(math_str):
    """Làm sạch ký tự LaTeX trong công thức nội dòng để hiển thị rõ ràng trên Word khi không thể chuyển sang OMML"""
    res = math_str
    res = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1) / (\2)', res)
    res = re.sub(r'\\vec\{([^}]+)\}', r'\1', res)
    res = re.sub(r'\\mathbf\{([^}]+)\}', r'\1', res)
    res = re.sub(r'\\mathit\{([^}]+)\}', r'\1', res)
    replacements = [
        (r'\tau', 'τ'),
        (r'\theta', 'θ'),
        (r'\eta', 'η'),
        (r'\mathbb{R}', 'ℝ'),
        (r'\mathcal{C}', '𝓒'),
        (r'\mathcal{E}', '𝓔'),
        (r'\mathcal{O}', '𝒪'),
        (r'\mathcal{L}', '𝓛'),
        (r'\mathcal{D}', '𝒟'),
        (r'\mid', '|'),
        (r'\in', '∈'),
        (r'\le', '≤'),
        (r'\ge', '≥'),
        (r'\times', '×'),
        (r'\cdot', '·'),
        (r'\approx', '≈'),
        (r'\neq', '≠'),
        (r'\to', '→'),
        (r'\dots', '…'),
        (r'\_', '_'),
        (r'\sum', '∑'),
        (r'\prod', '∏'),
        (r'\text{Hit}', 'Hit'),
        (r'\text{MRR}', 'MRR'),
        (r'\text{nDCG}', 'nDCG'),
        (r'\text{Recall}', 'Recall'),
        (r'\text{Context Precision}', 'Context Precision'),
        (r'\text{Similarity Score}', 'Similarity Score'),
        (r'\text{cosine}', 'cosine'),
        (r'\text', ''),
        ('{', ''),
        ('}', ''),
        ('\\', '')
    ]
    for old, new in replacements:
        res = res.replace(old, new)
    return res.strip()

def add_formatted_runs(p, text):
    """
    Phân tích chuỗi văn bản và chèn các run tương ứng với định dạng:
    - In đậm: **text**
    - In nghiêng: *text*
    - Mã nội dòng: `code`
    - Công thức nội dòng: $math$ (chuyển đổi thành Office Math OMML thực sự)
    - Liên kết markdown: [text](url) -> text
    """
    clean_t = sanitize_xml(text)
    
    # Loại bỏ cú pháp link markdown [label](url) -> label
    clean_t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean_t)
    
    # Tách token đa định dạng: **bold**, *italic*, `code`, $math$
    pattern = re.compile(r'(\*\*.*?\*\*|\*[^*]+?\*|`[^`]+?`|\$[^$\n]+?\$)')
    parts = pattern.split(clean_t)
    
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) >= 4:
            r = p.add_run(part[2:-2])
            r.bold = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(12.5)
        elif part.startswith('*') and part.endswith('*') and len(part) >= 2:
            r = p.add_run(part[1:-1])
            r.italic = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(12.5)
        elif part.startswith('`') and part.endswith('`') and len(part) >= 2:
            r = p.add_run(part[1:-1])
            r.font.name = "Consolas"
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(0x9C, 0x27, 0xB0)
        elif part.startswith('$') and part.endswith('$') and len(part) >= 2:
            math_code = part[1:-1]
            omml_elem = latex_to_omml(math_code)
            if omml_elem is not None:
                p._p.append(omml_elem)
            else:
                math_content = format_inline_math_text(math_code)
                r = p.add_run(math_content)
                r.italic = True
                r.font.name = "Cambria Math"
                r.font.size = Pt(12)
                r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        else:
            r = p.add_run(part)
            r.font.name = "Times New Roman"
            r.font.size = Pt(12.5)

def add_footer_page_number(run):
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def create_formal_cover_page(doc):
    """
    Kiến tạo Trang bìa chính thức và Trang bìa phụ chuẩn quy định NCKH Sinh viên
    của Học viện Công nghệ Bưu chính Viễn thông - Khoa Kỹ thuật Điện tử 1.
    Có khung viền trang bìa (page borders) trang trọng và bố cục chuẩn mực.
    """
    sect = doc.sections[0]
    
    # Thiết lập khung viền đôi cho trang bìa đầu tiên
    sectPr = sect._sectPr
    pgBorders = parse_xml(f'''
        <w:pgBorders {nsdecls("w")} w:offsetFrom="page" w:display="firstPage">
            <w:top w:val="double" w:sz="12" w:space="24" w:color="1B365D"/>
            <w:left w:val="double" w:sz="12" w:space="24" w:color="1B365D"/>
            <w:bottom w:val="double" w:sz="12" w:space="24" w:color="1B365D"/>
            <w:right w:val="double" w:sz="12" w:space="24" w:color="1B365D"/>
        </w:pgBorders>
    ''')
    sectPr.append(pgBorders)
    
    # 1. Cơ quan chủ quản
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("BỘ THÔNG TIN VÀ TRUYỀN THÔNG\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    r2 = p.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(14)
    r2.bold = True
    r2.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    r3 = p.add_run("KHOA KỸ THUẬT ĐIỆN TỬ 1")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(13)
    r3.bold = True
    r3.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

    # Đường kẻ phân cách
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(4)
    p_line.paragraph_format.space_after = Pt(36)
    r_line = p_line.add_run("———————————————")
    r_line.font.name = "Times New Roman"
    r_line.font.size = Pt(12)
    r_line.font.color.rgb = RGBColor(0xBD, 0xC3, 0xC7)

    # Tiêu đề báo cáo
    p_title_sub = doc.add_paragraph()
    p_title_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title_sub.paragraph_format.space_before = Pt(20)
    p_title_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_title_sub.add_run("BÁO CÁO KẾT QUẢ NGHIÊN CỨU KHOA HỌC CỦA SINH VIÊN")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(15)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B)

    # Tên đề tài
    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_before = Pt(12)
    p_topic.paragraph_format.space_after = Pt(12)
    r_topic = p_topic.add_run("ĐỀ TÀI:\nNGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC (RAG)")
    r_topic.font.name = "Times New Roman"
    r_topic.font.size = Pt(18)
    r_topic.bold = True
    r_topic.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    # Mã số đề tài
    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_code.paragraph_format.space_before = Pt(4)
    p_code.paragraph_format.space_after = Pt(48)
    r_code = p_code.add_run("MÃ SỐ ĐỀ TÀI: 07-SV-2026-ĐT1")
    r_code.font.name = "Times New Roman"
    r_code.font.size = Pt(13.5)
    r_code.bold = True
    r_code.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

    # Bảng thông tin sinh viên và giảng viên
    tbl = doc.add_table(rows=5, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    info_data = [
        ("Sinh viên thực hiện:", "NGUYỄN ĐÌNH HỒNG PHÚC"),
        ("Mã số sinh viên:", "B23DCDT191"),
        ("Lớp / Ngành đào tạo:", "D23CQDT01-B / Kỹ thuật Điện tử Viễn thông"),
        ("Giảng viên hướng dẫn:", "ThS. CHU VĂN CƯỜNG"),
        ("Đơn vị phê duyệt đề cương:", "Khoa Kỹ thuật Điện tử 1 (TS. Nguyễn Trung Hiếu)")
    ]
    
    for r_idx, (col1, col2) in enumerate(info_data):
        row = tbl.rows[r_idx]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = Inches(2.3)
        c2.width = Inches(3.8)
        set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
        set_cell_margins(c2, top=60, bottom=60, left=80, right=80)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(col1)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
        r1.bold = True
        r1.font.color.rgb = RGBColor(0x34, 0x49, 0x5E)
        
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(1)
        p2.paragraph_format.space_after = Pt(1)
        r2 = p2.add_run(col2)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(12)
        r2.bold = (r_idx in [0, 3])
        r2.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D) if (r_idx in [0, 3]) else RGBColor(0x22, 0x22, 0x22)

    # Địa điểm và năm
    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_before = Pt(56)
    p_bot.paragraph_format.space_after = Pt(0)
    r_bot = p_bot.add_run("HÀ NỘI - NĂM 2026")
    r_bot.font.name = "Times New Roman"
    r_bot.font.size = Pt(13)
    r_bot.bold = True
    r_bot.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    # Sang trang mới cho nội dung tiếp theo (Không tạo đoạn trắng thừa)
    doc.add_page_break()

def build_docx(full_markdown_text, docx_path):
    print(f"[*] Generating Word document: {docx_path}...")
    doc = docx.Document()
    
    # Khổ giấy A4 và căn lề chuẩn văn bản học thuật NCKH (Trên 2cm, Dưới 2cm, Trái 3cm, Phải 2cm)
    for section in doc.sections:
        section.top_margin = Inches(0.79)     # 2.0 cm
        section.bottom_margin = Inches(0.79)  # 2.0 cm
        section.left_margin = Inches(1.18)    # 3.0 cm
        section.right_margin = Inches(0.79)   # 2.0 cm
        
        # Đánh số trang tự động ở chân trang phía bên phải
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("Trang ")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(10)
        f_run.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)
        add_footer_page_number(f_run)

    # Cấu hình phong cách mặc định (Normal Style)
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12.5)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.3
    normal_style.paragraph_format.space_after = Pt(6)

    # 1. Tạo trang bìa chính thức chuẩn PTIT
    create_formal_cover_page(doc)

    lines = full_markdown_text.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []
    in_toc_section = False
    in_lot_section = False
    in_lof_section = False

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            return
        
        # Lọc bỏ các dòng định dạng căn chỉnh (|:---|:---|)
        filtered_rows = []
        for row in table_rows:
            if all(set(c.strip()).issubset({'-', ':', '|'}) for c in row if c.strip()):
                continue
            filtered_rows.append(row)
            
        if not filtered_rows:
            table_rows = []
            in_table = False
            return
            
        cols_count = max(len(r) for r in filtered_rows)
        tbl = doc.add_table(rows=len(filtered_rows), cols=cols_count)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        for r_idx, row in enumerate(filtered_rows):
            is_header = (r_idx == 0)
            for c_idx in range(cols_count):
                cell_text = row[c_idx] if c_idx < len(row) else ""
                cell = tbl.cell(r_idx, c_idx)
                set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
                
                # Viền bảng tinh tế
                tcPr = cell._tc.get_or_add_tcPr()
                borders = parse_xml(f'''
                    <w:tcBorders {nsdecls("w")}>
                        <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                        <w:left w:val="none"/>
                        <w:right w:val="none"/>
                        <w:bottom w:val="single" w:sz="{'12' if is_header else '4'}" w:space="0" w:color="{'1B365D' if is_header else 'CCCCCC'}"/>
                    </w:tcBorders>
                ''')
                tcPr.append(borders)
                
                if is_header:
                    set_cell_background(cell, "1B365D")
                elif r_idx % 2 == 1:
                    set_cell_background(cell, "F8F9FA")
                else:
                    set_cell_background(cell, "FFFFFF")
                    
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                
                # Format cell runs
                cleaned_cell = sanitize_xml(cell_text.strip())
                if is_header:
                    run = p.add_run(cleaned_cell.replace('**', ''))
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(11)
                    run.bold = True
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                else:
                    add_formatted_runs(p, cleaned_cell)
                    for r in p.runs:
                        r.font.size = Pt(11)
                        if not r.bold:
                            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                    
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(4)
        table_rows = []
        in_table = False

    def flush_code():
        nonlocal in_code_block, code_lines
        if not code_lines:
            return
        code_text = "\n".join(code_lines)
        full_c = code_text.lower()
        is_mermaid = any("graph " in l or "flowchart " in l or "subgraph " in l for l in code_lines[:3]) or (code_lines and code_lines[0].strip().startswith("mermaid"))
        
        if is_mermaid:
            # Nhận diện chính xác 16 sơ đồ đồ họa chất lượng cao (300 DPI)
            img_path = None
            if "giai đoạn 1: mở rộng dữ liệu" in full_c or "lộ trình các định hướng" in full_c or "lộ trình nghiên cứu" in full_c:
                img_path = os.path.join("diagrams", "diagram_8_roadmap.png")
            elif "bộ lọc thông minh rag" in full_c or "kiến trúc cộng sinh" in full_c or ("long-context llm" in full_c and "truy vấn người dùng" in full_c):
                img_path = os.path.join("diagrams", "diagram_7_symbiotic.png")
            elif "chu trình tự phản chiếu" in full_c or "cần tra cứu tri thức ngoài" in full_c or "loại bỏ tài liệu nhiễu" in full_c or "self-rag" in full_c:
                img_path = os.path.join("diagrams", "diagram_6_self_rag.png")
            elif "đồ thị tri thức" in full_c or "graphrag" in full_c or "leiden" in full_c or "tài liệu thô ban đầu" in full_c:
                img_path = os.path.join("diagrams", "diagram_5_graphrag.png")
            elif "bốn chỉ số cốt lõi của khung đánh giá ragas" in full_c or "đo lường khâu truy xuất" in full_c or "context precision" in full_c or "faithfulness" in full_c or "ragas" in full_c:
                img_path = os.path.join("diagrams", "diagram_4_ragas.png")
            elif "trường phái 1: nhúng đa phương thức" in full_c or "1408 chiều" in full_c or "multi-vector retriever" in full_c or "truy xuất đa vector" in full_c:
                img_path = os.path.join("diagrams", "diagram_multimodal_rag.png")
            elif "giai đoạn 1: nạp và phân giải dữ liệu" in full_c or "even chunks" in full_c or ("ingestion" in full_c and "querying" in full_c):
                img_path = os.path.join("diagrams", "diagram_qa_workflow.png")
            elif "tầng 1: tiền truy xuất" in full_c or "phân đoạn ngữ nghĩa phân tầng" in full_c or "tầng 2: trong truy xuất" in full_c:
                img_path = os.path.join("diagrams", "diagram_3_advanced_rag.png")
            elif "kiến trúc naive rag" in full_c or "thế hệ kiến trúc rag" in full_c or ("naive rag" in full_c and "modular" in full_c):
                img_path = os.path.join("diagrams", "diagram_2_evolution.png")
            elif ("dpr" in full_c and "bart" in full_c) or "lewis et al." in full_c or "rag-sequence" in full_c or "rag-token" in full_c or "nguyên lý mô hình rag khởi nguyên" in full_c:
                img_path = os.path.join("diagrams", "diagram_lewis_rag_origin.png")
            elif "hệ thống trí tuệ nhân tạo có tri thức" in full_c and "bộ nhớ phi tham số" in full_c:
                img_path = os.path.join("diagrams", "diagram_1_memory.png")
            elif "giai đoạn 1: xác định nguồn" in full_c or "thu thập ban đầu: 280" in full_c or "quy trình tổng quan tài liệu" in full_c:
                img_path = os.path.join("diagrams", "diagram_prisma.png")
            elif "bước 1: trích xuất tài liệu" in full_c or ("bước 1" in full_c and "pymupdf" in full_c):
                img_path = os.path.join("diagrams", "diagram_pipeline.png")
            elif "mô hình ngôn ngữ thuần tham số" in full_c or "thuần_tham_số" in full_c:
                img_path = os.path.join("diagrams", "diagram_parametric_vs_rag.png")
            elif "pham_vi_nghien_cuu" in full_c or "phạm vi nghiên cứu" in full_c or "trọng tâm nghiên cứu" in full_c:
                img_path = os.path.join("diagrams", "diagram_scope.png")
            elif "chương 1: đặt vấn đề" in full_c and "chương 2: cơ sở lý thuyết" in full_c:
                img_path = os.path.join("diagrams", "diagram_structure.png")

            if img_path and os.path.exists(img_path):
                # Chèn hình ảnh trực quan chất lượng cao 300 DPI
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(14)
                p_img.paragraph_format.space_after = Pt(3)
                r_img = p_img.add_run()
                r_img.add_picture(img_path, width=Inches(5.8))
            else:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(sanitize_xml(code_text))
                r.font.name = "Consolas"
                r.font.size = Pt(9.5)
        else:
            # Khối mã nguồn lập trình
            tbl = doc.add_table(rows=1, cols=1)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = tbl.cell(0, 0)
            set_cell_background(cell, "2D3748")
            set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            run = p.add_run(sanitize_xml(code_text))
            run.font.name = "Courier New"
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0xED, 0xF2, 0xF7)
            doc.add_paragraph()
        
        code_lines = []
        in_code_block = False

    # Bỏ qua phần bìa dạng text ở đầu markdown vì đã tạo trang bìa chính thức
    skip_initial_cover = True

    while i < len(lines):
        line = lines[i]
        
        # Bỏ qua phần header bìa text cũ đến khi gặp THÔNG TIN ĐỀ TÀI hoặc LỜI CAM ĐOAN
        if skip_initial_cover:
            if line.startswith("### THÔNG TIN ĐỀ TÀI") or line.startswith("### LỜI CAM ĐOAN"):
                skip_initial_cover = False
            else:
                i += 1
                continue

        # Code block handler
        if line.startswith("```"):
            if in_code_block:
                flush_code()
            else:
                if in_table:
                    flush_table()
                in_code_block = True
                code_lines = []
            i += 1
            continue
            
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
            
        # Table handler
        if line.strip().startswith("|") and line.strip().endswith("|"):
            if not in_table:
                in_table = True
                table_rows = []
            cols = [c.strip() for c in line.strip()[1:-1].split("|")]
            table_rows.append(cols)
            i += 1
            continue
        else:
            if in_table:
                flush_table()
                
        # Ngắt trang trước các chương và các phần lớn
        clean_line = line.strip()
        page_break_triggers = [
            "## CHƯƠNG 1:", "## CHƯƠNG 2:", "## CHƯƠNG 3:", "## CHƯƠNG 4:", "## CHƯƠNG 5:",
            "## TÀI LIỆU THAM KHẢO", "## PHỤ LỤC",
            "### LỜI CAM ĐOAN", "### LỜI CẢM ƠN", "### MỤC LỤC",
            "### DANH MỤC TỪ VIẾT TẮT", "### DANH MỤC CÁC BẢNG BIỂU",
            "### DANH MỤC CÁC HÌNH VẼ", "### TÓM TẮT NGHIÊN CỨU"
        ]
        if any(clean_line.startswith(trigger) for trigger in page_break_triggers):
            doc.add_page_break()

        # Heading 1 (#)
        if clean_line.startswith("# ") and not clean_line.startswith("# -*-"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(12)
            run = p.add_run(sanitize_xml(clean_line[2:].strip()))
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(20)
            run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            i += 1
            continue
            
        # Heading 2 (##)
        if clean_line.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(sanitize_xml(clean_line[3:].strip()))
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(15.5)
            run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            i += 1
            continue
            
        # Theo dõi các phần Mục lục và Danh mục
        if clean_line.startswith("### MỤC LỤC"):
            in_toc_section = True
            in_lot_section = False
            in_lof_section = False
        elif clean_line.startswith("### DANH MỤC CÁC BẢNG BIỂU"):
            in_toc_section = False
            in_lot_section = True
            in_lof_section = False
        elif clean_line.startswith("### DANH MỤC CÁC HÌNH VẼ"):
            in_toc_section = False
            in_lot_section = False
            in_lof_section = True
        elif clean_line in ["---", "***", "___"] or clean_line.startswith("### DANH MỤC TỪ VIẾT TẮT") or clean_line.startswith("### TÓM TẮT") or clean_line.startswith("## CHƯƠNG"):
            in_toc_section = False
            in_lot_section = False
            in_lof_section = False

        if clean_line == "### MỤC LỤC":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(12)
            run = p.add_run("MỤC LỤC")
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(15.5)
            run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            
            # Chèn trường mục lục tự động của Word (Native Word TOC Field)
            p_toc_fld = doc.add_paragraph()
            p_toc_fld.paragraph_format.space_after = Pt(6)
            fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="TOC \\o &quot;1-3&quot; \\h \\z \\u"/>')
            p_toc_fld._p.append(fld)
            
            in_toc_section = True
            i += 1
            continue

        # Heading 3 (###)
        if clean_line.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(sanitize_xml(clean_line[4:].strip()))
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(13.5)
            run.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
            i += 1
            continue

        # Heading 4 (####)
        if clean_line.startswith("#### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(sanitize_xml(clean_line[5:].strip()))
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(12.5)
            run.font.color.rgb = RGBColor(0x34, 0x49, 0x5E)
            i += 1
            continue

        # Heading 5 (#####)
        if clean_line.startswith("##### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(sanitize_xml(clean_line[6:].strip()))
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
            i += 1
            continue

        # Horizontal line (---)
        if clean_line in ["---", "***", "___"]:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run("—" * 45)
            run.font.name = "Times New Roman"
            run.font.color.rgb = RGBColor(0xBD, 0xC3, 0xC7)
            i += 1
            continue
            
        # Blockquote (>)
        if clean_line.startswith("> "):
            tbl = doc.add_table(rows=1, cols=1)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = tbl.cell(0, 0)
            set_cell_background(cell, "F0F4F8")
            set_cell_margins(cell, top=100, bottom=100, left=180, right=180)
            
            tcPr = cell._tc.get_or_add_tcPr()
            borders = parse_xml(f'''
                <w:tcBorders {nsdecls("w")}>
                    <w:left w:val="single" w:sz="30" w:space="0" w:color="1B365D"/>
                    <w:top w:val="none"/>
                    <w:right w:val="none"/>
                    <w:bottom w:val="none"/>
                </w:tcBorders>
            ''')
            tcPr.append(borders)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.2
            add_formatted_runs(p, clean_line[2:].strip())
            i += 1
            continue

        # Display Math ($$...$$)
        if clean_line.startswith("$$") and clean_line.endswith("$$") and len(clean_line) > 4:
            math_code = clean_line[2:-2].strip()
            math_code = clean_formula_str(math_code)
            
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(8)
            
            omml_elem = latex_to_omml(math_code)
            if omml_elem is not None:
                omathpara = etree.Element("{http://schemas.openxmlformats.org/officeDocument/2006/math}oMathPara")
                omathpara.append(omml_elem)
                p._p.append(omathpara)
            else:
                formatted_math = format_inline_math_text(math_code)
                r = p.add_run(formatted_math)
                r.font.name = "Cambria Math"
                r.font.size = Pt(12)
                r.italic = True
                r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            i += 1
            continue

        # Bullet list (- or *) hoặc Mục lục / Danh mục có Tab căn lề phải
        if clean_line.startswith("- ") or clean_line.startswith("* "):
            raw_line = line.rstrip()
            if in_toc_section:
                p = doc.add_paragraph()
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
                if raw_line.strip().startswith("- **"):
                    p.paragraph_format.left_indent = Inches(0)
                    p.paragraph_format.space_before = Pt(3)
                    p.paragraph_format.space_after = Pt(2)
                    content = raw_line.strip()[4:-2] if raw_line.strip().endswith("**") else raw_line.strip()[4:]
                    r = p.add_run(content)
                    r.bold = True
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(12)
                    r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
                    p.add_run("\t")
                else:
                    p.paragraph_format.left_indent = Inches(0.25)
                    p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.space_after = Pt(1)
                    content = raw_line.strip()[2:]
                    r = p.add_run(content)
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)
                    p.add_run("\t")
                i += 1
                continue
            elif in_lot_section or in_lof_section:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
                content = raw_line.strip()[2:]
                r = p.add_run(content)
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
                p.add_run("\t")
                i += 1
                continue
            else:
                p = doc.add_paragraph(style='List Bullet')
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.25
                content = clean_line[2:]
                add_formatted_runs(p, content)
                i += 1
                continue

        # Figure caption (*Hình X: ...*)
        if re.match(r'^\*?Hình \d+(\.\d+)?:', clean_line):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(14)
            p.paragraph_format.keep_with_next = False
            cap_text = clean_line.strip('*').strip()
            r = p.add_run(sanitize_xml(cap_text))
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            r.italic = True
            r.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
            i += 1
            continue

        # Regular paragraph
        if clean_line:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.3
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_formatted_runs(p, clean_line)
                
        i += 1

    if in_table:
        flush_table()
    if in_code_block:
        flush_code()

    doc.save(docx_path)
    print(f"[OK] Word document successfully saved to: {docx_path}")

def main():
    print("[*] Merging full academic research report (5-Chapter NCKH Structure)...")
    full_markdown = "\n\n".join([
        REPORT_META_AND_ABSTRACT,
        CHAPTER_1,
        CHAPTER_2,
        CHAPTER_3,
        CHAPTER_4,
        CHAPTER_5,
        REPORT_REFERENCES_AND_APPENDICES
    ])
    
    md_path = "BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)
    print(f"[OK] Master Markdown report saved to: {md_path}")
    
    docx_path = "BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.docx"
    build_docx(full_markdown, docx_path)

if __name__ == "__main__":
    main()
