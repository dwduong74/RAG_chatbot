# -*- coding: utf-8 -*-
"""
Tool cập nhật và làm sạch 100% sơ đồ Mermaid, loại bỏ hoàn toàn các mở ngoặc định nghĩa tiếng Anh,
và cấu hình compile_research_report.py để chèn trực tiếp HÌNH ẢNH SƠ ĐỒ ĐỒ HỌA (PNG 300 DPI)
vào tệp Word (.docx) kèm chú thích chuẩn NCKH.
"""

import sys
import os
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Sơ đồ 1 sạch 100% không còn mở ngoặc tiếng Anh
CLEAN_MERMAID_1 = """*Hình 1: Sơ đồ phân tách bộ nhớ trong hệ thống trí tuệ nhân tạo có tri thức*

```mermaid
graph TD
    Root["HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC"] --> PM["BỘ NHỚ THAM SỐ<br/>• Trọng số mạng nơ-ron Transformer<br/>• Học qua giải thuật Lan truyền ngược<br/>• Năng lực: Cú pháp, Ngữ nghĩa và Suy luận<br/>• Chi phí cập nhật: Rất cao khi tái huấn luyện<br/>• Tính giải thích: Hộp đen nơ-ron phức tạp"]
    Root --> NPM["BỘ NHỚ PHI THAM SỐ<br/>• Cơ sở dữ liệu Vector và Chỉ mục HNSW<br/>• Kho tri thức tài liệu rời rạc như PDF và CSDL<br/>• Cập nhật động theo thời gian thực<br/>• Chi phí cập nhật: Cực thấp khi cập nhật dữ liệu<br/>• Tính giải thích: Truy vết nguồn gốc minh bạch"]
```"""

# Sơ đồ 2 sạch 100%
CLEAN_MERMAID_2 = """*Hình 2: Sơ đồ tiến trình tiến hóa của các thế hệ kiến trúc RAG*

```mermaid
flowchart LR
    A["<b>KIẾN TRÚC NAIVE RAG</b><br/>• Quy trình tuần tự một chiều<br/>• Cơ chế Truy xuất và Đọc<br/>• Tìm kiếm vector tương đồng thô<br/>• Ghép chuỗi câu lệnh thô"] --> B["<b>KIẾN TRÚC ADVANCED RAG</b><br/>• Tối ưu hóa Tiền truy xuất<br/>• Tìm kiếm lai kết hợp từ khóa<br/>• Tái xếp hạng chéo nơ-ron<br/>• Nén ngữ cảnh chọn lọc"]
    B --> C["<b>KIẾN TRÚC MODULAR RAG</b><br/>• Phân tách các module độc lập<br/>• Định tuyến ngữ nghĩa động<br/>• Luồng điều khiển lặp và đệ quy<br/>• Tự phản chiếu và hiệu chỉnh"]
```"""

# Sơ đồ 3 sạch 100% (Khắc phục triệt để ví dụ của User)
CLEAN_MERMAID_3 = """*Hình 3: Sơ đồ kiến trúc Advanced RAG toàn diện ba tầng*

```mermaid
flowchart TD
    subgraph S1["TẦNG 1: TIỀN TRUY XUẤT"]
        direction TB
        A1["Phân đoạn ngữ nghĩa phân tầng"]
        A2["Trích xuất và làm giàu siêu dữ liệu"]
        A3["Viết lại và mở rộng câu hỏi truy vấn"]
        A4["Tạo văn bản giả định phục vụ tìm kiếm"]
    end

    subgraph S2["TẦNG 2: TRONG TRUY XUẤT"]
        direction TB
        B1["Tìm kiếm lai kết hợp từ khóa và vector"]
        B2["Thuật toán hợp nhất thứ hạng tương hỗ"]
        B3["Sử dụng mô hình nhúng đa ngôn ngữ tiên tiến"]
    end

    subgraph S3["TẦNG 3: HẬU TRUY XUẤT"]
        direction TB
        C1["Tái xếp hạng chéo nơ-ron"]
        C2["Nén ngữ cảnh và trích lọc dữ kiện cốt lõi"]
        C3["Tái cấu trúc vị trí tài liệu"]
    end

    S1 --> S2
    S2 --> S3
```"""

# Sơ đồ 4 sạch 100%
CLEAN_MERMAID_4 = """*Hình 4: Sơ đồ bốn trụ cột đo lường đánh giá của khung RAGAS*

```mermaid
flowchart TD
    subgraph RET["ĐO LƯỜNG KHÂU TRUY XUẤT"]
        direction TB
        CP["<b>Chỉ số Context Precision</b><br/>Đo mức độ xếp hạng tài liệu phù hợp ở đầu danh sách"]
        CR["<b>Chỉ số Context Recall</b><br/>Đo tỷ lệ bao phủ dữ kiện cần thiết từ tài liệu chuẩn"]
        CP --> CR
    end

    subgraph GEN["ĐO LƯỜNG KHÂU SINH"]
        direction TB
        F["<b>Chỉ số Faithfulness</b><br/>Đo độ trung thực, kháng ảo giác từ ngữ cảnh truy xuất"]
        AR["<b>Chỉ số Answer Relevance</b><br/>Đo độ bám sát trọng tâm câu hỏi của người dùng"]
        F --> AR
    end

    RET <--> GEN
```"""

# Sơ đồ 5 sạch 100% (Khắc phục triệt để ví dụ GraphRAG của User)
CLEAN_MERMAID_5 = """*Hình 5: Sơ đồ quy trình kết hợp GraphRAG giữa đồ thị tri thức và vector*

```mermaid
flowchart TD
    Raw["Tài liệu thô ban đầu"] --> Ext["Trích xuất Thực thể và Mối quan hệ"]
    Ext --> KG["Xây dựng Đồ thị Tri thức"]
    Ext --> Vec["Lập chỉ mục Vector"]
    
    KG --> Cluster["Phân cụm cộng đồng"]
    Cluster --> GlobSum["Tóm tắt toàn cục"]
    
    Vec --> LocalQA["Hỏi đáp cục bộ"]
    
    GlobSum --> Ans["CÂU TRẢ LỜI TOÀN DIỆN VÀ ĐA CHIỀU"]
    LocalQA --> Ans
```"""

# Sơ đồ 6 sạch 100%
CLEAN_MERMAID_6 = """*Hình 6: Sơ đồ chu trình tự phản chiếu trong kiến trúc Self-RAG*

```mermaid
flowchart TD
    Q["Câu hỏi người dùng đầu vào"] --> Dec1{"Cần tra cứu tri thức ngoài?"}
    
    Dec1 -- "Không tra cứu" --> GenDirect["Sinh đáp án trực tiếp từ Bộ nhớ tham số"]
    Dec1 -- "Cần tra cứu" --> RetTopK["Truy xuất tập tài liệu liên quan"]
    
    RetTopK --> EvalRel{"Đánh giá độ liên quan từng tài liệu"}
    EvalRel -- "Tài liệu nhiễu" --> DropDoc["Loại bỏ tài liệu nhiễu"]
    EvalRel -- "Tài liệu đúng" --> GenStep["Sinh câu trả lời từng phân đoạn"]
    
    GenStep --> EvalSup{"Kiểm chứng tính trung thực"}
    EvalSup -- "Có căn cứ" --> EvalUse{"Chấm điểm mức độ hữu ích"}
    EvalSup -- "Không có căn cứ" --> WarnHalluc["Hiệu chỉnh và lọc bỏ ảo giác"]
    
    EvalUse --> FinalResp["CÂU TRẢ LỜI ĐẠT CHUẨN"]
```"""

def update_source_files():
    # Part 1
    print("[*] Updating report_content_part1.py...")
    with open("report_content_part1.py", "r", encoding="utf-8") as f:
        c1 = f.read()
    c1 = re.sub(r'```mermaid\s*graph TD\s*Root\["HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC"\][\s\S]+?```', CLEAN_MERMAID_1, c1)
    with open("report_content_part1.py", "w", encoding="utf-8") as f:
        f.write(c1)
    print("    [OK] Part 1 updated.")

    # Part 2
    print("[*] Updating report_content_part2.py...")
    with open("report_content_part2.py", "r", encoding="utf-8") as f:
        c2 = f.read()
    c2 = re.sub(r'```mermaid\s*flowchart LR\s*A\["<b>NAIVE RAG</b>[\s\S]+?```', CLEAN_MERMAID_2, c2)
    c2 = re.sub(r'```mermaid\s*flowchart TD\s*subgraph S1\["TẦNG 1: TIỀN TRUY XUẤT[\s\S]+?```', CLEAN_MERMAID_3, c2)
    with open("report_content_part2.py", "w", encoding="utf-8") as f:
        f.write(c2)
    print("    [OK] Part 2 updated.")

    # Part 3
    print("[*] Updating report_content_part3.py...")
    with open("report_content_part3.py", "r", encoding="utf-8") as f:
        c3 = f.read()
    c3 = re.sub(r'```mermaid\s*flowchart TD\s*subgraph RET\["ĐO LƯỜNG KHÂU TRUY XUẤT"\][\s\S]+?```', CLEAN_MERMAID_4, c3)
    c3 = re.sub(r'```mermaid\s*flowchart TD\s*Raw\["Tài liệu thô ban đầu"\][\s\S]+?```', CLEAN_MERMAID_5, c3)
    with open("report_content_part3.py", "w", encoding="utf-8") as f:
        f.write(c3)
    print("    [OK] Part 3 updated.")

    # Appendices
    print("[*] Updating report_content_appendices.py...")
    with open("report_content_appendices.py", "r", encoding="utf-8") as f:
        c4 = f.read()
    c4 = re.sub(r'```mermaid\s*flowchart TD\s*Q\["Câu hỏi người dùng x"\][\s\S]+?```', CLEAN_MERMAID_6, c4)
    with open("report_content_appendices.py", "w", encoding="utf-8") as f:
        f.write(c4)
    print("    [OK] Appendices updated.")

def update_compiler_for_images():
    print("[*] Updating compile_research_report.py to insert PNG DIAGRAM IMAGES into Word .docx...")
    with open("compile_research_report.py", "r", encoding="utf-8") as f:
        code = f.read()

    # Tạo hàm chèn hình ảnh sơ đồ thay vì chèn code mermaid
    new_flush_code = """    def flush_code():
        nonlocal in_code_block, code_lines
        if not code_lines:
            return
        code_text = "\\n".join(code_lines)
        is_mermaid = any("graph " in l or "flowchart " in l or "subgraph " in l for l in code_lines[:3]) or (code_lines and code_lines[0].strip().startswith("mermaid"))
        
        if is_mermaid:
            # Nhận diện sơ đồ để chèn đúng hình ảnh đồ họa chất lượng cao
            img_path = None
            caption = ""
            full_c = code_text.lower()
            
            if "hệ thống trí tuệ nhân tạo có tri thức" in full_c or "bộ nhớ tham số" in full_c:
                img_path = os.path.join("diagrams", "diagram_1_memory.png")
                caption = "Hình 1: Sơ đồ phân tách bộ nhớ trong hệ thống trí tuệ nhân tạo có tri thức"
            elif "kiến trúc naive rag" in full_c or "naive rag" in full_c and "modular" in full_c:
                img_path = os.path.join("diagrams", "diagram_2_evolution.png")
                caption = "Hình 2: Sơ đồ tiến trình tiến hóa của các thế hệ kiến trúc RAG"
            elif "tầng 1: tiền truy xuất" in full_c or "tầng 2: trong truy xuất" in full_c:
                img_path = os.path.join("diagrams", "diagram_3_advanced_rag.png")
                caption = "Hình 3: Sơ đồ kiến trúc Advanced RAG toàn diện ba tầng"
            elif "context precision" in full_c or "đo lường khâu truy xuất" in full_c:
                img_path = os.path.join("diagrams", "diagram_4_ragas.png")
                caption = "Hình 4: Sơ đồ bốn trụ cột đo lường đánh giá của khung RAGAS"
            elif "đồ thị tri thức" in full_c or "graphrag" in full_c or "leiden" in full_c:
                img_path = os.path.join("diagrams", "diagram_5_graphrag.png")
                caption = "Hình 5: Sơ đồ quy trình kết hợp GraphRAG giữa đồ thị tri thức và vector"
            elif "cần tra cứu tri thức ngoài" in full_c or "self-rag" in full_c or "tri thức ngoài" in full_c:
                img_path = os.path.join("diagrams", "diagram_6_self_rag.png")
                caption = "Hình 6: Sơ đồ chu trình tự phản chiếu trong kiến trúc Self-RAG"

            if img_path and os.path.exists(img_path):
                # Chèn hình ảnh thực tế chất lượng cao
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(12)
                p_img.paragraph_format.space_after = Pt(4)
                r_img = p_img.add_run()
                r_img.add_picture(img_path, width=Inches(5.8))
                
                # Chú thích hình ảnh thuần Việt chuẩn NCKH
                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_before = Pt(2)
                p_cap.paragraph_format.space_after = Pt(12)
                r_cap = p_cap.add_run(caption)
                r_cap.font.name = "Times New Roman"
                r_cap.font.size = Pt(10.5)
                r_cap.italic = True
                r_cap.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
            else:
                # Nếu không tìm thấy file ảnh, fallback
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(sanitize_xml(code_text))
                r.font.name = "Consolas"
                r.font.size = Pt(9.5)
        else:
            # Khối mã nguồn lập trình thông thường
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
        in_code_block = False"""

    # Thay thế hàm flush_code trong compiler
    old_def_marker = "    def flush_code():"
    end_def_marker = "        in_code_block = False"
    
    s_idx = code.find(old_def_marker)
    if s_idx != -1:
        e_idx = code.find(end_def_marker, s_idx)
        if e_idx != -1:
            e_idx += len(end_def_marker)
            code = code[:s_idx] + new_flush_code + code[e_idx:]
            with open("compile_research_report.py", "w", encoding="utf-8") as f:
                f.write(code)
            print("    [OK] compile_research_report.py updated to insert images!")
        else:
            print("    [!] Could not locate end of flush_code.")
    else:
        print("    [!] Could not locate start of flush_code.")

def main():
    print("=" * 70)
    print(" TOOL HOÀN THIỆN SƠ ĐỒ ĐỒ HỌA THỰC TẾ & KHỬ SẠCH NGOẶC ĐỊNH NGHĨA")
    print("=" * 70)

    # 1. Cập nhật các tệp nội dung nguồn với Mermaid sạch 100%
    update_source_files()

    # 2. Cập nhật script biên dịch để chèn ảnh thực tế
    update_compiler_for_images()

    # 3. Tái biên dịch
    print("\n[*] Re-compiling full report...")
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
    print("\n[✓] Hoàn tất quá trình cập nhật sơ đồ đồ họa và xuất bản Word!")

if __name__ == "__main__":
    main()
