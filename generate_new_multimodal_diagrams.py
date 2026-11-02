# -*- coding: utf-8 -*-
"""
Tạo 2 sơ đồ học thuật bổ sung cho RAG Đa phương thức và Quy trình QA System (300 DPI)
1. diagram_qa_workflow.png: Quy trình 2 giai đoạn Ingestion & Querying (Retrieval & Synthesis)
2. diagram_multimodal_rag.png: 2 trường phái Multimodal RAG & Multi-Vector Retriever
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

os.makedirs("diagrams", exist_ok=True)
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Calibri', 'Segoe UI']
plt.rcParams['axes.unicode_minus'] = False

def create_diagram_qa_workflow():
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.8)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Main Title
    ax.text(5.75, 6.5, "QUY TRÌNH HỆ THỐNG HỎI ĐÁP RAG HAI GIAI ĐOẠN",
            ha="center", va="center", color="#1B365D", fontsize=13, fontweight="bold")

    # Divider line between Ingestion and Querying
    ax.plot([0.5, 11.0], [3.35, 3.35], color="#CBD5E1", lw=1.5, linestyle="--")

    # ==================== TẦNG 1: DATA INGESTION / PARSING ====================
    # Label
    ax.text(0.6, 5.95, "GIAI ĐOẠN 1: NẠP VÀ PHÂN GIẢI DỮ LIỆU (DATA INGESTION & PARSING)",
            ha="left", va="center", color="#1E40AF", fontsize=10.5, fontweight="bold")

    # PDF Icon / Box
    b_pdf = patches.FancyBboxPatch((0.6, 4.2), 1.1, 1.2, boxstyle="round,pad=0.1",
                                  ec="#DC2626", fc="#FEF2F2", lw=1.8)
    ax.add_patch(b_pdf)
    ax.text(1.15, 4.9, "Tài liệu", ha="center", va="center", color="#991B1B", fontsize=9.5, fontweight="bold")
    ax.text(1.15, 4.5, "PDF / Docs", ha="center", va="center", color="#B91C1C", fontsize=8.5)

    # Chunks
    chunk_y = [5.1, 4.6, 4.1, 3.6]
    for i, cy in enumerate(chunk_y, 1):
        b_c = patches.FancyBboxPatch((2.2, cy), 1.2, 0.38, boxstyle="round,pad=0.08",
                                     ec="#D97706", fc="#FEF3C7", lw=1.2)
        ax.add_patch(b_c)
        ax.text(2.8, cy + 0.19, f"Đoạn {i} (Chunk)", ha="center", va="center", color="#92400E", fontsize=8)

        # Arrow from PDF to chunk
        ax.annotate("", xy=(2.2, cy + 0.19), xytext=(1.7, 4.8),
                    arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=1.2))

    # Vector DB (Cylinder representation)
    b_vdb = patches.FancyBboxPatch((4.2, 3.8), 1.8, 1.7, boxstyle="round,pad=0.15",
                                   ec="#2563EB", fc="#EFF6FF", lw=2)
    ax.add_patch(b_vdb)
    ax.text(5.1, 4.85, "Cơ sở dữ liệu\nVector (ChromaDB)", ha="center", va="center",
            color="#1E40AF", fontsize=9.5, fontweight="bold")
    ax.text(5.1, 4.25, "• Không gian nhúng\n• Chỉ mục HNSW", ha="center", va="center",
            color="#1D4ED8", fontsize=8, linespacing=1.3)

    for cy in chunk_y:
        ax.annotate("", xy=(4.2, 4.65), xytext=(3.4, cy + 0.19),
                    arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.1))

    # Notes for Ingestion
    note_ingest = (
        "Quy trình Tiền xử lý & Lập chỉ mục:\n"
        "• Phân chia tài liệu thành các đoạn đều đặn (Even Chunks)\n"
        "• Mỗi khối đại diện cho một phân đoạn văn bản thô\n"
        "• Tạo vector nhúng ngữ nghĩa (FastEmbed / ONNX Runtime)\n"
        "• Lưu trữ vector và siêu dữ liệu nguồn vào CSDL Vector"
    )
    b_note1 = patches.FancyBboxPatch((6.4, 3.75), 4.6, 1.8, boxstyle="round,pad=0.12",
                                    ec="#93C5FD", fc="#F8FAFC", lw=1)
    ax.add_patch(b_note1)
    ax.text(6.6, 4.65, note_ingest, ha="left", va="center", color="#334155", fontsize=8.5, linespacing=1.5)

    # ==================== TẦNG 2: QUERYING ====================
    # Label
    ax.text(0.6, 3.0, "GIAI ĐOẠN 2: TRUY VẤN VÀ TỔNG HỢP (QUERYING: RETRIEVAL & SYNTHESIS)",
            ha="left", va="center", color="#0F766E", fontsize=10.5, fontweight="bold")

    # User Query Box
    b_query = patches.FancyBboxPatch((0.6, 1.1), 1.2, 1.3, boxstyle="round,pad=0.1",
                                     ec="#4F46E5", fc="#EEF2FF", lw=1.5)
    ax.add_patch(b_query)
    ax.text(1.2, 1.85, "Truy vấn", ha="center", va="center", color="#3730A3", fontsize=9.5, fontweight="bold")
    ax.text(1.2, 1.45, "Người dùng\n(User Query)", ha="center", va="center", color="#4338CA", fontsize=8, linespacing=1.2)

    # Vector DB in query
    b_vdb2 = patches.FancyBboxPatch((2.4, 0.9), 1.7, 1.7, boxstyle="round,pad=0.15",
                                    ec="#2563EB", fc="#EFF6FF", lw=1.8)
    ax.add_patch(b_vdb2)
    ax.text(3.25, 1.95, "Cơ sở dữ liệu\nVector", ha="center", va="center",
            color="#1E40AF", fontsize=9.5, fontweight="bold")
    ax.text(3.25, 1.35, "Tìm Top-k\nCosine Distance", ha="center", va="center",
            color="#1D4ED8", fontsize=8, linespacing=1.2)

    ax.annotate("", xy=(2.4, 1.75), xytext=(1.8, 1.75),
                arrowprops=dict(arrowstyle="-|>", color="#4F46E5", lw=1.5))

    # Top-k retrieved chunks
    b_topk = patches.FancyBboxPatch((4.7, 1.1), 1.4, 1.3, boxstyle="round,pad=0.1",
                                    ec="#D97706", fc="#FEF3C7", lw=1.5)
    ax.add_patch(b_topk)
    ax.text(5.4, 1.85, "Top-k Đoạn", ha="center", va="center", color="#92400E", fontsize=9.5, fontweight="bold")
    ax.text(5.4, 1.45, "Ngữ cảnh trích chọn\nchính xác nhất", ha="center", va="center", color="#B45309", fontsize=8, linespacing=1.2)

    ax.annotate("", xy=(4.7, 1.75), xytext=(4.1, 1.75),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.5))

    # Phase 1 bracket: Retrieval
    ax.plot([2.4, 6.1], [0.65, 0.65], color="#2563EB", lw=2)
    ax.plot([2.4, 2.4], [0.65, 0.75], color="#2563EB", lw=2)
    ax.plot([6.1, 6.1], [0.65, 0.75], color="#2563EB", lw=2)
    ax.text(4.25, 0.45, "Pha 1: Truy xuất Ngữ nghĩa (Retrieval)", ha="center", va="center",
            color="#1E40AF", fontsize=8.5, fontweight="bold")

    # LLM Box
    b_llm = patches.FancyBboxPatch((6.7, 1.0), 1.5, 1.5, boxstyle="round,pad=0.15",
                                   ec="#7C3AED", fc="#F5F3FF", lw=2)
    ax.add_patch(b_llm)
    ax.text(7.45, 1.9, "Mô hình\nNgôn ngữ Lớn", ha="center", va="center",
            color="#5B21B6", fontsize=9.5, fontweight="bold")
    ax.text(7.45, 1.35, "LLM Synthesis\nĐọc & Suy luận", ha="center", va="center",
            color="#6D28D9", fontsize=8, linespacing=1.2)

    ax.annotate("", xy=(6.7, 1.75), xytext=(6.1, 1.75),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=1.5))

    # Connect original query to LLM as well
    ax.annotate("", xy=(6.7, 2.2), xytext=(1.2, 2.4),
                arrowprops=dict(arrowstyle="-|>", color="#6366F1", lw=1.2,
                                connectionstyle="arc3,rad=-0.15"))

    # Phase 2 bracket: Synthesis
    ax.plot([6.7, 8.2], [0.65, 0.65], color="#7C3AED", lw=2)
    ax.plot([6.7, 6.7], [0.65, 0.75], color="#7C3AED", lw=2)
    ax.plot([8.2, 8.2], [0.65, 0.75], color="#7C3AED", lw=2)
    ax.text(7.45, 0.45, "Pha 2: Tổng hợp (Synthesis)", ha="center", va="center",
            color="#5B21B6", fontsize=8.5, fontweight="bold")

    # Output Answer Box
    b_ans = patches.FancyBboxPatch((8.8, 1.1), 2.2, 1.3, boxstyle="round,pad=0.1",
                                   ec="#16A34A", fc="#DCFCE7", lw=1.8)
    ax.add_patch(b_ans)
    ax.text(9.9, 1.9, "CÂU TRẢ LỜI ĐÍCH", ha="center", va="center", color="#15803D", fontsize=9.5, fontweight="bold")
    ax.text(9.9, 1.45, "Chính xác, có căn cứ dữ kiện,\ntrích dẫn trang gốc minh bạch", ha="center", va="center",
            color="#166534", fontsize=8, linespacing=1.2)

    ax.annotate("", xy=(8.8, 1.75), xytext=(8.2, 1.75),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=1.8))

    out_path = os.path.join("diagrams", "diagram_qa_workflow.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")


def create_diagram_multimodal_rag():
    fig, ax = plt.subplots(figsize=(12.0, 7.2), dpi=300)
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 7.2)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Main Title
    ax.text(6.0, 6.9, "HAI TRƯỜNG PHÁI KIẾN TRÚC RAG ĐA PHƯƠNG THỨC VÀ KỸ THUẬT MULTI-VECTOR RETRIEVER",
            ha="center", va="center", color="#1B365D", fontsize=12.5, fontweight="bold")

    # Divider between 2 paradigms
    ax.plot([6.0, 6.0], [0.4, 6.5], color="#CBD5E1", lw=1.5, linestyle="--")

    # ==================== TRƯỜNG PHÁI 1: JOINT EMBEDDING ====================
    ax.text(3.0, 6.4, "TRƯỜNG PHÁI 1: NHÚNG ĐA PHƯƠNG THỨC ĐỒNG NHẤT\n(MULTIMODAL JOINT EMBEDDING - GOOGLE GEMINI)",
            ha="center", va="center", color="#1E40AF", fontsize=9.5, fontweight="bold", linespacing=1.3)

    # Input: Multi-modal Data
    b_input1 = patches.FancyBboxPatch((0.5, 4.8), 5.0, 1.1, boxstyle="round,pad=0.1",
                                      ec="#2563EB", fc="#EFF6FF", lw=1.5)
    ax.add_patch(b_input1)
    ax.text(3.0, 5.5, "TÀI LIỆU KHOA HỌC ĐA PHƯƠNG THỨC", ha="center", va="center",
            color="#1E40AF", fontsize=9.5, fontweight="bold")
    ax.text(3.0, 5.1, "Đoạn văn bản + Hình ảnh thí nghiệm + Đồ thị + Bảng biểu số liệu",
            ha="center", va="center", color="#1F2937", fontsize=8.5)

    # Embedding Model Box
    b_model1 = patches.FancyBboxPatch((0.8, 3.4), 4.4, 0.95, boxstyle="round,pad=0.1",
                                      ec="#7C3AED", fc="#F5F3FF", lw=1.5)
    ax.add_patch(b_model1)
    ax.text(3.0, 4.0, "MÔ HÌNH NHÚNG ĐA PHƯƠNG THỨC (MULTIMODAL EMBEDDING)",
            ha="center", va="center", color="#5B21B6", fontsize=9, fontweight="bold")
    ax.text(3.0, 3.65, "Tạo vector nhúng 1408 chiều trong không gian ngữ nghĩa chung",
            ha="center", va="center", color="#6D28D9", fontsize=8)

    ax.annotate("", xy=(3.0, 4.35), xytext=(3.0, 4.8),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.5))

    # Shared Vector Space Box
    b_space = patches.FancyBboxPatch((0.8, 2.0), 4.4, 0.95, boxstyle="round,pad=0.1",
                                     ec="#0D9488", fc="#F0FDFA", lw=1.5)
    ax.add_patch(b_space)
    ax.text(3.0, 2.6, "KHÔNG GIAN VECTOR ĐỒNG NHẤT 1408 CHIỀU",
            ha="center", va="center", color="#0F766E", fontsize=9, fontweight="bold")
    ax.text(3.0, 2.25, "Tìm kiếm chéo phương thức: Dùng chữ tìm ảnh, dùng ảnh tìm chữ",
            ha="center", va="center", color="#115E59", fontsize=8)

    ax.annotate("", xy=(3.0, 2.95), xytext=(3.0, 3.4),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=1.5))

    # Output to Multimodal LLM
    b_mllm1 = patches.FancyBboxPatch((0.5, 0.6), 5.0, 0.95, boxstyle="round,pad=0.1",
                                     ec="#16A34A", fc="#DCFCE7", lw=1.8)
    ax.add_patch(b_mllm1)
    ax.text(3.0, 1.2, "MÔ HÌNH NGÔN NGỮ ĐA PHƯƠNG THỨC (GEMINI 1.5 PRO)",
            ha="center", va="center", color="#15803D", fontsize=9.5, fontweight="bold")
    ax.text(3.0, 0.85, "Tiếp nhận đồng thời Ảnh gốc thô + Đoạn văn bản truy xuất để tổng hợp",
            ha="center", va="center", color="#166534", fontsize=8)

    ax.annotate("", xy=(3.0, 1.55), xytext=(3.0, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#0D9488", lw=1.5))

    # ==================== TRƯỜNG PHÁI 2: MULTI-VECTOR RETRIEVER ====================
    ax.text(9.0, 6.4, "TRƯỜNG PHÁI 2: TRUY XUẤT ĐA VECTOR CHO DỮ LIỆU BÁN CẤU TRÚC\n(MULTI-VECTOR RETRIEVER - LANGCHAIN)",
            ha="center", va="center", color="#B45309", fontsize=9.5, fontweight="bold", linespacing=1.3)

    # Raw structured elements
    b_raw = patches.FancyBboxPatch((6.5, 5.0), 5.0, 0.9, boxstyle="round,pad=0.1",
                                   ec="#EA580C", fc="#FFF7ED", lw=1.5)
    ax.add_patch(b_raw)
    ax.text(9.0, 5.55, "DỮ LIỆU NGUYÊN BẢN (RAW CONTENT)", ha="center", va="center",
            color="#C2410C", fontsize=9.5, fontweight="bold")
    ax.text(9.0, 5.25, "Bảng biểu HTML/Markdown + Biểu đồ kỹ thuật số + Hình minh họa gốc",
            ha="center", va="center", color="#9A3412", fontsize=8)

    # LLM Summarizer
    b_sum = patches.FancyBboxPatch((6.8, 3.8), 4.4, 0.8, boxstyle="round,pad=0.1",
                                   ec="#7C3AED", fc="#FAF5FF", lw=1.3)
    ax.add_patch(b_sum)
    ax.text(9.0, 4.3, "LLM ĐA PHƯƠNG THỨC TẠO TÓM TẮT VĂN BẢN", ha="center", va="center",
            color="#6B21A8", fontsize=9, fontweight="bold")
    ax.text(9.0, 4.0, "Trích xuất ý nghĩa cốt lõi của bảng và biểu đồ thành văn bản súc tích",
            ha="center", va="center", color="#7E22CE", fontsize=8)

    ax.annotate("", xy=(9.0, 4.6), xytext=(9.0, 5.0),
                arrowprops=dict(arrowstyle="-|>", color="#EA580C", lw=1.3))

    # Multi-Vector Architecture Box
    b_mv = patches.FancyBboxPatch((6.5, 2.0), 5.0, 1.4, boxstyle="round,pad=0.12",
                                  ec="#0284C7", fc="#F0F9FF", lw=1.8)
    ax.add_patch(b_mv)
    ax.text(9.0, 3.15, "CƠ CHẾ ÁNH XẠ ĐA VECTOR (MULTI-VECTOR MAPPING)",
            ha="center", va="center", color="#0369A1", fontsize=9.5, fontweight="bold")

    # Two sub-boxes inside
    b_sub1 = patches.FancyBboxPatch((6.7, 2.2), 2.1, 0.65, boxstyle="round,pad=0.08",
                                    ec="#0284C7", fc="#FFFFFF", lw=1)
    ax.add_patch(b_sub1)
    ax.text(7.75, 2.6, "Chỉ mục Tìm kiếm", ha="center", va="center", color="#0369A1", fontsize=8, fontweight="bold")
    ax.text(7.75, 2.35, "Vector của bản tóm tắt", ha="center", va="center", color="#0284C7", fontsize=7.5)

    b_sub2 = patches.FancyBboxPatch((9.2, 2.2), 2.1, 0.65, boxstyle="round,pad=0.08",
                                    ec="#EA580C", fc="#FFFFFF", lw=1)
    ax.add_patch(b_sub2)
    ax.text(10.25, 2.6, "Kho Lưu trữ Gốc", ha="center", va="center", color="#C2410C", fontsize=8, fontweight="bold")
    ax.text(10.25, 2.35, "Bảng thô / Ảnh gốc", ha="center", va="center", color="#EA580C", fontsize=7.5)

    # Pointer arrow between index and docstore
    ax.annotate("", xy=(9.2, 2.5), xytext=(8.8, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#0D9488", lw=1.5))
    ax.text(9.0, 2.7, "Ánh xạ ID", ha="center", va="center", color="#0D9488", fontsize=7.5, fontweight="bold")

    ax.annotate("", xy=(9.0, 3.4), xytext=(9.0, 3.8),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=1.3))

    # Output Synthesis
    b_out2 = patches.FancyBboxPatch((6.5, 0.6), 5.0, 0.95, boxstyle="round,pad=0.1",
                                    ec="#16A34A", fc="#DCFCE7", lw=1.8)
    ax.add_patch(b_out2)
    ax.text(9.0, 1.2, "TỔNG HỢP CÂU TRẢ LỜI ĐỘ CHÍNH XÁC CAO",
            ha="center", va="center", color="#15803D", fontsize=9.5, fontweight="bold")
    ax.text(9.0, 0.85, "LLM nhận bảng biểu gốc nguyên vẹn $\\rightarrow$ Triệt tiêu sai số dữ liệu số",
            ha="center", va="center", color="#166534", fontsize=8)

    ax.annotate("", xy=(9.0, 1.55), xytext=(9.0, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#0284C7", lw=1.5))

    out_path = os.path.join("diagrams", "diagram_multimodal_rag.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

if __name__ == '__main__':
    create_diagram_qa_workflow()
    create_diagram_multimodal_rag()
