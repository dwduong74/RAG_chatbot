# -*- coding: utf-8 -*-
"""
Tool tự động chuyển đổi toàn bộ sơ đồ khung ASCII text sang mã Mermaid Diagram chuẩn quốc tế.
Các sơ đồ được chuyển đổi:
1. Sơ đồ Phân tách Bộ nhớ: Parametric Memory vs Non-Parametric Memory (Chương 1)
2. Sơ đồ Tiến trình Tiến hóa của Kiến trúc RAG (Chương 3)
3. Sơ đồ Kiến trúc Advanced RAG Toàn diện 3 Tầng (Chương 3 - Ví dụ của User)
4. Sơ đồ 4 Trụ cột Đánh giá của RAGAS (Chương 5)
5. Sơ đồ Quy trình Kết hợp GraphRAG: Đồ thị Tri thức & Vector (Chương 6)
6. Bảng so sánh CSDL Vector chuyển thành bảng Markdown chuẩn (Chương 7)
7. Sơ đồ Chu trình Tự phản chiếu trong Self-RAG (Chương 7)
"""

import sys
import os
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Sơ đồ 1 (Chương 1)
MERMAID_DIAGRAM_1 = """```mermaid
graph TD
    Root["HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC"] --> PM["BỘ NHỚ THAM SỐ (PARAMETRIC MEMORY)<br/>• Trọng số mạng nơ-ron Transformer<br/>• Học qua giải thuật Gradient Descent<br/>• Năng lực: Cú pháp, Ngữ nghĩa & Suy luận<br/>• Chi phí cập nhật: Rất cao (Tái huấn luyện)<br/>• Tính giải thích: Hộp đen nơ-ron"]
    Root --> NPM["BỘ NHỚ PHI THAM SỐ (NON-PARAMETRIC MEMORY)<br/>• Cơ sở dữ liệu Vector / Chỉ mục HNSW<br/>• Kho tri thức tài liệu rời rạc (PDF, CSDL)<br/>• Cập nhật động theo thời gian thực<br/>• Chi phí cập nhật: Cực thấp (CRUD)<br/>• Tính giải thích: Truy vết nguồn gốc rõ ràng"]
```"""

# Sơ đồ 2 (Chương 3)
MERMAID_DIAGRAM_2 = """```mermaid
flowchart LR
    A["<b>NAIVE RAG</b><br/>• Quy trình tuần tự thô<br/>• Cơ chế Retrieve & Read<br/>• Tìm kiếm Vector Top-k<br/>• Ghép chuỗi Prompt thô"] --> B["<b>ADVANCED RAG</b><br/>• Tối ưu Tiền truy xuất<br/>• Tìm kiếm lai Hybrid Search<br/>• Tái xếp hạng Re-ranking<br/>• Nén ngữ cảnh chọn lọc"]
    B --> C["<b>MODULAR RAG</b><br/>• Phân tách Module độc lập<br/>• Định tuyến Routing động<br/>• Vòng lặp Iterative / Recursive<br/>• Tự phản chiếu Self-Reflective"]
```"""

# Sơ đồ 3 (Chương 3 - Ví dụ trực tiếp của người dùng)
MERMAID_DIAGRAM_3 = """```mermaid
flowchart TD
    subgraph S1["TẦNG 1: TIỀN TRUY XUẤT (PRE-RETRIEVAL)"]
        direction TB
        A1["Cắt đoạn ngữ nghĩa (Semantic & Parent-Child Chunking)"]
        A2["Làm giàu siêu dữ liệu (Metadata Extraction: thời gian, tác giả, chuyên mục)"]
        A3["Viết lại & mở rộng truy vấn (Query Rewriting, Multi-Query)"]
        A4["Tạo văn bản giả định HyDE (Hypothetical Document Embeddings)"]
    end

    subgraph S2["TẦNG 2: TRONG TRUY XUẤT (RETRIEVAL)"]
        direction TB
        B1["Tìm kiếm lai (Hybrid Search: Dense Vector + BM25 Sparse Lexical)"]
        B2["Hợp nhất xếp hạng tương hỗ (Reciprocal Rank Fusion - RRF)"]
        B3["Mô hình nhúng đa ngôn ngữ tiên tiến (BGE-M3, GTE)"]
    end

    subgraph S3["TẦNG 3: HẬU TRUY XUẤT (POST-RETRIEVAL)"]
        direction TB
        C1["Tái xếp hạng chéo nơ-ron (Cross-Encoder Re-ranking)"]
        C2["Nén ngữ cảnh & trích lọc câu chọn lọc (Contextual Compression)"]
        C3["Tái cấu trúc vị trí tài liệu (Prompt Reordering chống Lost in the Middle)"]
    end

    S1 --> S2
    S2 --> S3
```"""

# Sơ đồ 4 (Chương 5)
MERMAID_DIAGRAM_4 = """```mermaid
flowchart TD
    subgraph RET["ĐO LƯỜNG KHÂU TRUY XUẤT"]
        direction TB
        CP["<b>CONTEXT PRECISION</b><br/>Đo mức độ xếp hạng tài liệu phù hợp ở đầu danh sách"]
        CR["<b>CONTEXT RECALL</b><br/>Đo tỷ lệ bao phủ dữ kiện cần thiết từ tài liệu chuẩn"]
        CP --> CR
    end

    subgraph GEN["ĐO LƯỜNG KHÂU SINH"]
        direction TB
        F["<b>FAITHFULNESS</b><br/>Đo độ trung thực, kháng ảo giác từ ngữ cảnh truy xuất"]
        AR["<b>ANSWER RELEVANCE</b><br/>Đo độ bám sát trọng tâm câu hỏi của người dùng"]
        F --> AR
    end

    RET <--> GEN
```"""

# Sơ đồ 5 (Chương 6)
MERMAID_DIAGRAM_5 = """```mermaid
flowchart TD
    Raw["Tài liệu thô ban đầu"] --> Ext["Trích xuất Thực thể & Mối quan hệ"]
    Ext --> KG["Xây dựng Đồ thị Tri thức (Knowledge Graph)"]
    Ext --> Vec["Lập chỉ mục Vector (Vector Database)"]
    
    KG --> Cluster["Phân cụm cộng đồng (Leiden Clustering)"]
    Cluster --> GlobSum["Tóm tắt toàn cục (Global Summarization)"]
    
    Vec --> LocalQA["Hỏi đáp cục bộ (Local QA Search)"]
    
    GlobSum --> Ans["CÂU TRẢ LỜI TOÀN DIỆN & ĐA CHIỀU"]
    LocalQA --> Ans
```"""

# Bảng so sánh CSDL Vector (Chương 7)
MARKDOWN_TABLE_VECTOR_DB = """| Tiêu chí so sánh | ChromaDB | Qdrant | MongoDB Vector Search | Milvus |
| :--- | :--- | :--- | :--- | :--- |
| **Ngôn ngữ cốt lõi** | Python / C++ | Rust | C++ | Go / C++ |
| **Cấu trúc chỉ mục** | HNSW (hnswlib) | HNSW tùy biến | HNSW (Lucene) | HNSW, IVF_FLAT |
| **Cơ chế lưu trữ** | SQLite / Parquet | Bộ nhớ / Mmap | BSON Document CSDL | Phân tán Object Storage |
| **Mô hình triển khai** | Nhúng (Embedded) | Client-Server | Managed Atlas / Replica | Cluster phân tán |
| **Lọc siêu dữ liệu** | Hậu lọc / Tiền lọc | Tiền lọc đồng thời (Payload) | Aggregation Stage | Boolean Scalar Filtering |
| **Tối ưu hóa CPU** | Tốt | Cực tốt (SIMD AVX-512) | Trung bình | Rất tốt |
| **Kịch bản tối ưu** | PoC, Nghiên cứu, Desktop | Doanh nghiệp lớn, Hiệu năng cao | Ứng dụng Fullstack Web | Kho tri thức quy mô hàng tỷ |"""

# Sơ đồ 7 (Chương 7)
MERMAID_DIAGRAM_7 = """```mermaid
flowchart TD
    Q["Câu hỏi người dùng x"] --> Dec1{"Cần tra cứu tri thức ngoài?"}
    
    Dec1 -- "Retrieve = NO" --> GenDirect["Sinh đáp án trực tiếp từ Bộ nhớ tham số"]
    Dec1 -- "Retrieve = YES" --> RetTopK["Truy xuất tập top-k tài liệu D"]
    
    RetTopK --> EvalRel{"Đánh giá độ liên quan từng tài liệu"}
    EvalRel -- "IsRel = Irrelevant" --> DropDoc["Loại bỏ tài liệu nhiễu"]
    EvalRel -- "IsRel = Relevant" --> GenStep["Sinh câu trả lời từng phân đoạn y_t"]
    
    GenStep --> EvalSup{"Kiểm chứng tính trung thực"}
    EvalSup -- "IsSup = Supported" --> EvalUse{"Chấm điểm mức độ hữu ích (IsUse)"}
    EvalSup -- "IsSup = No Support" --> WarnHalluc["Hiệu chỉnh / Lọc bỏ ảo giác"]
    
    EvalUse --> FinalResp["CÂU TRẢ LỜI ĐẠT CHUẨN"]
```"""

def replace_block(filepath, start_indicator, end_indicator, replacement):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    s_idx = text.find(start_indicator)
    if s_idx == -1:
        print(f"    [!] Start indicator not found: '{start_indicator[:30]}...' in {filepath}")
        return False
        
    e_idx = text.find(end_indicator, s_idx)
    if e_idx == -1:
        print(f"    [!] End indicator not found: '{end_indicator[:30]}...' in {filepath}")
        return False
        
    e_idx += len(end_indicator)
    # Tìm xem có kết thúc bằng ``` không
    closing_ticks = text.find("```", e_idx - len(end_indicator))
    if closing_ticks != -1 and closing_ticks < e_idx + 10:
        full_end = closing_ticks + 3
    else:
        full_end = e_idx
        
    # Tìm ``` mở đầu trước s_idx
    opening_ticks = text.rfind("```", 0, s_idx)
    if opening_ticks != -1 and s_idx - opening_ticks < 20:
        full_start = opening_ticks
    else:
        full_start = s_idx

    new_text = text[:full_start] + replacement + text[full_end:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"    [OK] Successfully replaced block in {filepath}")
    return True

def main():
    print("=" * 70)
    print(" TOOL TỰ ĐỘNG CHUYỂN ĐỔI SƠ ĐỒ ASCII SANG MERMAID DIAGRAM")
    print("=" * 70)

    # 1. Diagram 1 in report_content_part1.py
    print("[*] Processing Diagram 1 in report_content_part1.py...")
    replace_block(
        "report_content_part1.py",
        "+-------------------------------------------------------------------------+\n| HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC |",
        "+-------------------------------+ +-------------------------------+\n```",
        MERMAID_DIAGRAM_1
    )

    # 2. Diagram 2 in report_content_part2.py
    print("[*] Processing Diagram 2 in report_content_part2.py...")
    replace_block(
        "report_content_part2.py",
        "TIẾN TRÌNH TIẾN HÓA CỦA KIẾN TRÚC RAG",
        "+------------------+ +-------------------+ +--------------------+\n```",
        MERMAID_DIAGRAM_2
    )

    # 3. Diagram 3 in report_content_part2.py (User exact example)
    print("[*] Processing Diagram 3 in report_content_part2.py...")
    replace_block(
        "report_content_part2.py",
        "+--------------------------------------------------------------------------+\n| KIẾN TRÚC ADVANCED RAG TOÀN DIỆN |",
        "└── Sắp xếp lại tài liệu (Prompt Reordering: tài liệu tốt nhất ở đầu và cuối)\n```",
        MERMAID_DIAGRAM_3
    )

    # 4. Diagram 4 in report_content_part3.py
    print("[*] Processing Diagram 4 in report_content_part3.py...")
    replace_block(
        "report_content_part3.py",
        "4 TRỤ CỘT ĐÁNH GIÁ CỦA RAGAS",
        "+-------------------------+ +-------------------------+\n```",
        MERMAID_DIAGRAM_4
    )

    # 5. Diagram 5 in report_content_part3.py
    print("[*] Processing Diagram 5 in report_content_part3.py...")
    replace_block(
        "report_content_part3.py",
        "QUY TRÌNH KẾT HỢP GRAPHRAG (KNOWLEDGE GRAPH + VECTOR)",
        "CÂU TRẢ LỜI TOÀN DIỆN\n```",
        MERMAID_DIAGRAM_5
    )

    # 6. Diagram 6 in report_content_appendices.py
    print("[*] Processing Diagram 6 (Vector DB Table) in report_content_appendices.py...")
    replace_block(
        "report_content_appendices.py",
        "+---------------------------------------------------------------------------------------------------+\n| BẢNG SO SÁNH ĐẶC TÍNH KỸ THUẬT CÁC HỆ QUẢN TRỊ CƠ SỞ DỮ LIỆU VECTOR |",
        "+-------------------+--------------------+--------------------+--------------------+----------------+\n```",
        MARKDOWN_TABLE_VECTOR_DB
    )

    # 7. Diagram 7 in report_content_appendices.py
    print("[*] Processing Diagram 7 (Self-RAG) in report_content_appendices.py...")
    replace_block(
        "report_content_appendices.py",
        "[ Câu hỏi người dùng x ]",
        "└── [IsUse = 1..5] (Chấm điểm hữu ích của câu trả lời)\n```",
        MERMAID_DIAGRAM_7
    )

    # Re-compile
    print("\n[*] Re-compiling full research report (Markdown & Word docx)...")
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
    print("\n[✓] Hoàn tất quá trình chuyển đổi toàn bộ sơ đồ sang Mermaid chuẩn!")

if __name__ == "__main__":
    main()
