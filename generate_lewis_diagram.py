# -*- coding: utf-8 -*-
"""
Tạo sơ đồ Kiến trúc RAG Khởi nguyên của Lewis et al. (NeurIPS 2020) thay thế cho sơ đồ ASCII.
Lưu tại: diagrams/diagram_lewis_rag_origin.png (300 DPI)
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

def create_diagram_lewis():
    fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=300)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Main Title
    ax.text(5.75, 5.85, "KIẾN TRÚC RAG KHỞI NGUYÊN (LEWIS ET AL., NEURIPS 2020)",
            ha="center", va="center", color="#1B365D", fontsize=12.5, fontweight="bold")
    ax.text(5.75, 5.5, "Mô hình Xác suất Biên Kết hợp Khối Truy xuất DPR và Khối Sinh Seq2Seq BART",
            ha="center", va="center", color="#4B5563", fontsize=9.5, fontstyle="italic")

    # 1. Truy vấn x (Input Query)
    b_q = patches.FancyBboxPatch((0.5, 3.4), 1.6, 1.2, boxstyle="round,pad=0.1",
                                ec="#2563EB", fc="#EFF6FF", lw=1.8)
    ax.add_patch(b_q)
    ax.text(1.3, 4.2, "Truy vấn x", ha="center", va="center", color="#1E40AF", fontsize=10.5, fontweight="bold")
    ax.text(1.3, 3.7, "(Câu hỏi của\nngười dùng)", ha="center", va="center", color="#3B82F6", fontsize=8.5)

    # 2. Khối DPR Bi-Encoder (Bộ truy xuất nơ-ron)
    b_dpr_container = patches.FancyBboxPatch((2.7, 2.7), 3.4, 2.4, boxstyle="round,pad=0.1",
                                            ec="#059669", fc="#F0FDF4", lw=1.8)
    ax.add_patch(b_dpr_container)
    ax.text(4.4, 4.85, "BỘ TRUY XUẤT DENSE PASSAGE RETRIEVER (DPR)", ha="center", va="center",
            color="#065F46", fontsize=9.5, fontweight="bold")

    # Sub-boxes inside DPR
    b_eq = patches.FancyBboxPatch((2.9, 4.0), 3.0, 0.6, boxstyle="round,pad=0.08",
                                 ec="#10B981", fc="#FFFFFF", lw=1.2)
    ax.add_patch(b_eq)
    ax.text(4.4, 4.3, "Bộ mã hóa câu hỏi: E_Q(x) (BERT)", ha="center", va="center", color="#047857", fontsize=8.5, fontweight="bold")

    b_mips = patches.FancyBboxPatch((2.9, 2.9), 3.0, 0.85, boxstyle="round,pad=0.08",
                                   ec="#10B981", fc="#FFFFFF", lw=1.2)
    ax.add_patch(b_mips)
    ax.text(4.4, 3.5, "Tìm kiếm Tích vô hướng Cực đại (MIPS / FAISS)", ha="center", va="center", color="#047857", fontsize=8.5, fontweight="bold")
    ax.text(4.4, 3.15, "p_η(z | x) ~ exp(E_Q(x)^T · E_D(z))", ha="center", va="center", color="#065F46", fontsize=8, fontstyle="italic")

    # Kho tri thức ngoài (Wikipedia)
    b_kb = patches.FancyBboxPatch((2.9, 0.6), 3.0, 1.3, boxstyle="round,pad=0.08",
                                 ec="#7C3AED", fc="#F5F3FF", lw=1.5)
    ax.add_patch(b_kb)
    ax.text(4.4, 1.45, "Kho Tri thức Ngoài (Non-Parametric Memory)", ha="center", va="center", color="#5B21B6", fontsize=9, fontweight="bold")
    ax.text(4.4, 1.1, "Wikipedia 21 Triệu Đoạn (DPR Chunks)", ha="center", va="center", color="#6D28D9", fontsize=8)
    ax.text(4.4, 0.8, "Mã hóa trước bởi E_D(z) (768 chiều)", ha="center", va="center", color="#8B5CF6", fontsize=7.5)

    # Mũi tên từ Kho tri thức vào MIPS
    ax.annotate("", xy=(4.4, 2.9), xytext=(4.4, 1.9),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=1.5))
    ax.text(4.7, 2.35, "Chỉ mục Vector", color="#7C3AED", fontsize=8)

    # Mũi tên từ Query vào DPR
    ax.annotate("", xy=(2.7, 4.0), xytext=(2.1, 4.0),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.8))

    # 3. Top-k Tài liệu z_i
    b_topk = patches.FancyBboxPatch((6.6, 3.1), 1.6, 1.6, boxstyle="round,pad=0.1",
                                   ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b_topk)
    ax.text(7.4, 4.35, "Top-k Đoạn Trích", ha="center", va="center", color="#92400E", fontsize=9.5, fontweight="bold")
    ax.text(7.4, 3.95, "Tài liệu {z_1, ..., z_k}", ha="center", va="center", color="#B45309", fontsize=8.5, fontweight="bold")
    ax.text(7.4, 3.5, "Biến tiềm ẩn\nngữ cảnh z", ha="center", va="center", color="#78350F", fontsize=8)

    # Mũi tên từ DPR sang Top-k
    ax.annotate("", xy=(6.6, 3.9), xytext=(6.1, 3.9),
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=1.8))

    # 4. Bộ sinh Seq2Seq (BART-Large)
    b_gen = patches.FancyBboxPatch((8.7, 2.7), 2.3, 2.4, boxstyle="round,pad=0.1",
                                  ec="#DC2626", fc="#FEF2F2", lw=1.8)
    ax.add_patch(b_gen)
    ax.text(9.85, 4.85, "BỘ SINH SEQ2SEQ (BART)", ha="center", va="center", color="#991B1B", fontsize=9.5, fontweight="bold")
    ax.text(9.85, 4.45, "Mô hình BART-Large (400M)", ha="center", va="center", color="#B91C1C", fontsize=8.5)
    
    # Sub-box RAG variants
    b_var = patches.FancyBboxPatch((8.85, 2.9), 2.0, 1.25, boxstyle="round,pad=0.08",
                                  ec="#EF4444", fc="#FFFFFF", lw=1.2)
    ax.add_patch(b_var)
    ax.text(9.85, 3.85, "1. RAG-Sequence:", ha="center", va="center", color="#991B1B", fontsize=8, fontweight="bold")
    ax.text(9.85, 3.55, "p(y|x) = Σ p(z|x)·p(y|x,z)", ha="center", va="center", color="#7F1D1D", fontsize=7.5, fontstyle="italic")
    ax.text(9.85, 3.25, "2. RAG-Token:", ha="center", va="center", color="#991B1B", fontsize=8, fontweight="bold")
    ax.text(9.85, 2.98, "p(y|x) = Π Σ p(z|x)·p(y_i|...)", ha="center", va="center", color="#7F1D1D", fontsize=7.5, fontstyle="italic")

    # Mũi tên từ Top-k sang BART
    ax.annotate("", xy=(8.7, 3.9), xytext=(8.2, 3.9),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=1.8))
    ax.text(8.45, 4.15, "z_i", color="#D97706", fontsize=9, fontweight="bold")

    # Mũi tên trực tiếp từ Query x xuống BART (ghép nối [x ; z_i])
    ax.annotate("", xy=(8.7, 4.4), xytext=(1.3, 4.6),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.4, linestyle="--",
                                connectionstyle="arc3,rad=-0.18"))
    ax.text(5.0, 5.2, "Truy vấn x được ghép nối cùng tài liệu z_i: [x ; z_i]", color="#2563EB", fontsize=8.5, fontstyle="italic")

    # 5. Câu trả lời y (Output Response)
    b_out = patches.FancyBboxPatch((9.0, 0.6), 1.8, 1.3, boxstyle="round,pad=0.1",
                                  ec="#16A34A", fc="#F0FDF4", lw=1.8)
    ax.add_patch(b_out)
    ax.text(9.9, 1.5, "Câu trả lời y", ha="center", va="center", color="#15803D", fontsize=10.5, fontweight="bold")
    ax.text(9.9, 1.15, "Dẫn nguồn xác thực\nMinh bạch tri thức", ha="center", va="center", color="#166534", fontsize=8)
    ax.text(9.9, 0.8, "Khắc phục ảo giác", ha="center", va="center", color="#15803D", fontsize=7.5, fontstyle="italic")

    # Mũi tên từ BART xuống Câu trả lời
    ax.annotate("", xy=(9.9, 1.9), xytext=(9.9, 2.7),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=1.8))

    # Mũi tên lan truyền ngược Gradient End-to-End
    ax.annotate("", xy=(4.4, 2.7), xytext=(9.85, 2.7),
                arrowprops=dict(arrowstyle="-|>", color="#EA580C", lw=1.4, linestyle=":",
                                connectionstyle="arc3,rad=0.22"))
    ax.text(7.1, 1.95, "Lan truyền ngược Gradient grad_η L_RAG (End-to-End Training)",
            ha="center", va="center", color="#EA580C", fontsize=8.5, fontweight="bold")

    plt.tight_layout()
    output_path = "diagrams/diagram_lewis_rag_origin.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[✓] Đã tạo thành công sơ đồ đồ họa 300 DPI: {output_path}")

if __name__ == "__main__":
    create_diagram_lewis()
