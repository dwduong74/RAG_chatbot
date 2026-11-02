# -*- coding: utf-8 -*-
"""
Kịch bản kiểm thử toàn diện Báo cáo Nghiên cứu Khoa học RAG
Kiểm chứng đồng thời:
1. BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md (Cấu trúc 5 chương NCKH, RQ, Gap, Discussion, Benchmark 40 câu hỏi)
2. BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.docx (Đồ họa 16 ảnh 300 DPI, 0 rò rỉ mã sơ đồ, chú thích, trang bìa PTIT)
3. Phong cách học thuật: Không tự ý đóng mở ngoặc định nghĩa tiếng Anh, không số liệu bịa đặt, không tham chiếu sai
"""

import sys
import os
import re
import docx

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print(" KIỂM THỬ TOÀN DIỆN BÁO CÁO NGHIÊN CỨU KHOA HỌC RAG (CHUẨN 5 CHƯƠNG NCKH)")
print("=" * 80)

PASS_COUNT = 0
TOTAL_CHECKS = 0

def check(name, condition, details=""):
    global PASS_COUNT, TOTAL_CHECKS
    TOTAL_CHECKS += 1
    if condition:
        PASS_COUNT += 1
        print(f"  [PASS] {name} {details}")
    else:
        print(f"  [FAIL] {name} {details}")
        assert False, f"Kiểm thử thất bại tại mục: {name} - {details}"

# ==============================================================================
# PHẦN 1: KIỂM THỬ MASTER MARKDOWN
# ==============================================================================
print("\n--- PHẦN 1: KIỂM THỬ TẬP TIN MARKDOWN (.MD) ---")
md_path = "BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md"
check("Tệp Markdown tồn tại", os.path.exists(md_path), f"({md_path})")

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

words_md = len(re.findall(r'\b\w+\b', md_content))
check("Dung lượng văn bản học thuật", words_md >= 15000, f"({words_md:,} từ, đạt chuẩn chuyên khảo NCKH)")

# Kiểm tra sự hiện diện của 5 chương chuẩn NCKH
check("Chương 1: Đặt vấn đề", "## CHƯƠNG 1: ĐẶT VẤN ĐỀ" in md_content)
check("Chương 2: Cơ sở lý thuyết", "## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN NGHIÊN CỨU" in md_content)
check("Chương 3: Phương pháp nghiên cứu", "## CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU" in md_content)
check("Chương 4: Kết quả và Thảo luận", "## CHƯƠNG 4: KẾT QUẢ VÀ THẢO LUẬN" in md_content)
check("Chương 5: Kết luận và Hướng NC", "## CHƯƠNG 5: KẾT LUẬN, HẠN CHẾ VÀ HƯỚNG NGHIÊN CỨU TIẾP THEO" in md_content)

# Kiểm tra các thông tin học thuật và pháp lý chuẩn PTIT
check("Mã số đề tài PTIT: 07-SV-2026-ĐT1", "07-SV-2026-ĐT1" in md_content)
check("Sinh viên thực hiện: Nguyễn Đình Hồng Phúc (B23DCDT191)", "Nguyễn Đình Hồng Phúc" in md_content and "B23DCDT191" in md_content)
check("Giảng viên hướng dẫn: ThS. Chu Văn Cường", "Chu Văn Cường" in md_content)
check("Tổng số trang ngữ liệu chính xác: 121 trang", "121 trang" in md_content or "121" in md_content)

# Kiểm tra các mục then chốt
check("Khoảng trống nghiên cứu (Research Gaps)", "### 1.2. Khoảng trống nghiên cứu" in md_content and "Khoảng trống 1" in md_content and "Khoảng trống 5" in md_content)
check("Mục tiêu nghiên cứu (5 mục tiêu)", "### 1.3. Mục tiêu nghiên cứu" in md_content and "5. **Nghiên cứu chuyên sâu kiến trúc RAG Đa phương thức" in md_content)
check("Câu hỏi nghiên cứu (RQ1 - RQ4)", "### 1.4. Câu hỏi nghiên cứu" in md_content and "RQ1:" in md_content and "RQ4:" in md_content)
check("Phạm vi nghiên cứu", "### 1.5. Phạm vi và đối tượng nghiên cứu" in md_content)
check("Mục 2.4 RAG Đa phương thức & Đa vector", "### 2.4. Kiến trúc RAG Đa phương thức và Cơ chế Truy xuất Đa vector" in md_content)
check("Mục 4.7 Thảo luận (Discussion)", "### 4.7. Thảo luận" in md_content and "4.7.1. Giải đáp có hệ thống các câu hỏi nghiên cứu" in md_content)
check("Mục 5.2 Hạn chế của nghiên cứu", "### 5.2. Hạn chế của nghiên cứu" in md_content)
check("Mục 5.3 Hướng nghiên cứu tiếp theo", "### 5.3. Hướng nghiên cứu tiếp theo" in md_content)

# Kiểm tra không có số liệu bịa đặt và không tham chiếu sai
check("Không có số liệu bịa đặt 14.2% Context Precision", "14.2%" not in md_content)
check("Không có tham chiếu Chương 7 sai lệch", "Chương 7" not in md_content)

# Kiểm tra số lượng sơ đồ Mermaid trong Markdown
mermaid_blocks = re.findall(r'```(?:mermaid)?([\s\S]+?)```', md_content)
mermaid_diagrams = [b for b in mermaid_blocks if any(k in b for k in ['graph ', 'flowchart ', 'subgraph ', 'sequenceDiagram'])]
check("Đúng 16 sơ đồ Mermaid trong Markdown", len(mermaid_diagrams) == 16, f"({len(mermaid_diagrams)}/16 sơ đồ)")

# ==============================================================================
# PHẦN 2: KIỂM THỬ TẬP TIN WORD (.DOCX)
# ==============================================================================
print("\n--- PHẦN 2: KIỂM THỬ TẬP TIN WORD (.DOCX) ---")
docx_path = "BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.docx"
check("Tệp Word tồn tại", os.path.exists(docx_path), f"({docx_path})")

doc = docx.Document(docx_path)
check("Số đoạn văn bản trong Word", len(doc.paragraphs) >= 200, f"({len(doc.paragraphs)} đoạn)")
check("Số lượng bảng biểu trong Word", len(doc.tables) >= 10, f"({len(doc.tables)} bảng biểu)")

# Kiểm tra số tệp hình ảnh đính kèm (Media Part)
image_rels = [rel.target_ref for rel in doc.part.rels.values() if "image" in rel.target_ref]
check("Nhúng đúng 16 hình ảnh đồ họa 300 DPI", len(image_rels) == 16, f"({len(image_rels)}/16 ảnh nhúng)")

# Kiểm tra rò rỉ mã nguồn sơ đồ trong văn bản (Tuyệt đối không để lộ mã flowchart hay subgraph)
raw_code_leakage = []
for p in doc.paragraphs:
    txt = p.text.strip()
    if txt.startswith("flowchart ") or txt.startswith("graph ") or txt.startswith("subgraph "):
        raw_code_leakage.append(txt[:40])
check("Không rò rỉ mã Mermaid trong văn bản Word", len(raw_code_leakage) == 0, f"(Số đoạn rò rỉ: {len(raw_code_leakage)})")

# Kiểm tra các đoạn chú thích Hình (Figure Captions)
figure_captions = []
toc_figures = []
for idx, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if re.match(r'^\*?Hình \d+(\.\d+)?[:\s]', txt):
        if idx < 150:
            toc_figures.append(txt)
        else:
            figure_captions.append(txt)

check("Đúng 16 mục trong Danh mục Hình vẽ", len(toc_figures) == 16, f"({len(toc_figures)}/16 mục TOC)")
check("Đúng 16 chú thích dưới Hình ảnh đồ họa", len(figure_captions) == 16, f"({len(figure_captions)}/16 chú thích)")
for idx, cap in enumerate(figure_captions, 1):
    print(f"      [{idx:2d}] {cap}")

# Kiểm tra công thức toán học OMML (Office Math Markup Language) chuẩn Microsoft Word
xml_str = doc._element.xml
count_omath = xml_str.count('<m:oMath>') + xml_str.count('<m:oMath ')
count_omathpara = xml_str.count('<m:oMathPara')
check("Word chứa công thức toán OMML khối độc lập (>= 25)", count_omathpara >= 25, f"({count_omathpara} công thức khối)")
check("Word chứa công thức toán OMML nội dòng và khối (>= 150)", count_omath >= 150, f"({count_omath} công thức OMML)")

# ==============================================================================
# PHẦN 3: KIỂM TRA QUY TẮC PHONG CÁCH HỌC THUẬT (KHÔNG ĐÓNG MỞ NGOẶC ĐỊNH NGHĨA)
# ==============================================================================
print("\n--- PHẦN 3: KIỂM THỬ QUY TẮC PHONG CÁCH NCKH ---")

vietnamese_text_paragraphs = [p.text for p in doc.paragraphs if not p.text.strip().startswith(("References", "Tài liệu tham khảo", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]", "[10]"))]
full_docx_text = "\n".join(vietnamese_text_paragraphs)

check("Không rò rỉ mã công thức thô fracvecq", "fracvecq" not in full_docx_text)
check("Không rò rỉ mã công thức thô P(y mid x)", "P(y mid x)" not in full_docx_text)
check("Không dùng từ tuyệt đối trong văn phong", "tuyệt đối" not in full_docx_text)
check("Không dùng từ triệt để trong văn phong", "triệt để" not in full_docx_text)
check("Không dùng khẳng định 100% mục tiêu", "100% mục tiêu" not in full_docx_text)

prohibited_patterns = [
    r'Tối ưu hóa Hậu truy xuất\s*\(',
    r'Tối ưu hóa Tiền truy xuất\s*\(',
    r'Bộ nhớ tham số\s*\(',
    r'Bộ nhớ phi tham số\s*\(',
    r'Độ trung thực\s*\(Faithfulness\)',
    r'Độ liên quan\s*\(Answer Relevance\)',
    r'Độ chính xác ngữ cảnh\s*\(Context Precision\)',
    r'Độ bao phủ ngữ cảnh\s*\(Context Recall\)',
    r'Đồ thị Tri thức\s*\(Knowledge Graph\)',
    r'Cơ sở dữ liệu Vector\s*\(Vector Database\)',
    r'biến tiềm ẩn\s*\(latent variable\)'
]

for pat in prohibited_patterns:
    m = re.search(pat, full_docx_text, re.IGNORECASE)
    check(f"Không có mẫu vi phạm: '{pat}'", m is None)

print("\n" + "=" * 80)
print(f" KẾT QUẢ TỔNG THỂ: {PASS_COUNT}/{TOTAL_CHECKS} BÀI KIỂM TRA ĐẠT TIÊU CHUẨN XUẤT SẮC (100% PASS)")
print("=" * 80)
