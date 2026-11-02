# -*- coding: utf-8 -*-
"""
Tạo 6 sơ đồ học thuật dạng hình ảnh PNG độ phân giải cao (300 DPI)
để chèn trực tiếp vào tài liệu Word (.docx), đảm bảo:
1. Hiển thị sơ đồ đồ họa trực quan (không phải code text).
2. Tuyệt đối không chứa bất kỳ đóng mở ngoặc định nghĩa tiếng Anh thừa nào.
"""

import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("diagrams", exist_ok=True)

plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Calibri', 'Segoe UI']
plt.rcParams['axes.unicode_minus'] = False

def create_diagram_1():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Root
    bbox_root = patches.FancyBboxPatch((2.2, 5.0), 5.6, 0.9, boxstyle="round,pad=0.2",
                                       ec="#1B365D", fc="#1B365D", lw=2)
    ax.add_patch(bbox_root)
    ax.text(5.0, 5.45, "HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC",
            ha="center", va="center", color="white", fontsize=13, fontweight="bold")

    # Parametric
    bbox_pm = patches.FancyBboxPatch((0.5, 0.6), 4.2, 3.8, boxstyle="round,pad=0.2",
                                    ec="#2563EB", fc="#EFF6FF", lw=1.5)
    ax.add_patch(bbox_pm)
    ax.text(2.6, 3.9, "BỘ NHỚ THAM SỐ", ha="center", va="center",
            color="#1E40AF", fontsize=12, fontweight="bold")

    pm_text = (
        "• Trọng số ma trận mạng nơ-ron Transformer\n"
        "• Học qua giải thuật tối ưu hóa Lan truyền ngược\n"
        "• Năng lực: Cú pháp, Ngữ nghĩa và Suy luận\n"
        "• Chi phí cập nhật: Rất cao (Tái huấn luyện)\n"
        "• Tính giải thích: Hộp đen nơ-ron phức tạp\n"
        "• Kiểm soát quyền: Rất khó phân quyền dữ liệu"
    )
    ax.text(0.8, 2.2, pm_text, ha="left", va="center", color="#1F2937", fontsize=10.5, linespacing=1.8)

    # Non-Parametric
    bbox_npm = patches.FancyBboxPatch((5.3, 0.6), 4.2, 3.8, boxstyle="round,pad=0.2",
                                     ec="#0D9488", fc="#F0FDFA", lw=1.5)
    ax.add_patch(bbox_npm)
    ax.text(7.4, 3.9, "BỘ NHỚ PHI THAM SỐ", ha="center", va="center",
            color="#0F766E", fontsize=12, fontweight="bold")

    npm_text = (
        "• Cơ sở dữ liệu Vector và Không gian chỉ mục\n"
        "• Kho tri thức tài liệu rời rạc (PDF, CSDL)\n"
        "• Cập nhật động theo thời gian thực\n"
        "• Chi phí cập nhật: Cực thấp (Thêm, sửa, xóa)\n"
        "• Tính giải thích: Truy vết nguồn gốc minh bạch\n"
        "• Kiểm soát quyền: Phân quyền truy cập theo vai trò"
    )
    ax.text(5.6, 2.2, npm_text, ha="left", va="center", color="#1F2937", fontsize=10.5, linespacing=1.8)

    # Arrows
    ax.annotate("", xy=(2.6, 4.5), xytext=(4.0, 5.0),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(7.4, 4.5), xytext=(6.0, 5.0),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))

    out_path = os.path.join("diagrams", "diagram_1_memory.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_2():
    fig, ax = plt.subplots(figsize=(10.5, 4.5), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    stages = [
        ("KIẾN TRÚC NAIVE RAG", "#EFF6FF", "#2563EB", "#1E40AF", [
            "• Quy trình tuần tự một chiều",
            "• Cơ chế Truy xuất và Đọc",
            "• Tìm kiếm vector tương đồng thô",
            "• Ghép chuỗi câu lệnh thô"
        ], 0.4),
        ("KIẾN TRÚC ADVANCED RAG", "#F0FDFA", "#0D9488", "#0F766E", [
            "• Tối ưu hóa Tiền truy xuất",
            "• Tìm kiếm lai kết hợp từ khóa",
            "• Tái xếp hạng chéo nơ-ron",
            "• Nén ngữ cảnh chọn lọc"
        ], 3.8),
        ("KIẾN TRÚC MODULAR RAG", "#FEF3C7", "#D97706", "#B45309", [
            "• Phân tách các module độc lập",
            "• Định tuyến ngữ nghĩa động",
            "• Luồng điều khiển lặp và đệ quy",
            "• Tự phản chiếu và hiệu chỉnh"
        ], 7.2)
    ]

    for title, bg_col, border_col, text_col, bullets, x_pos in stages:
        box = patches.FancyBboxPatch((x_pos, 0.4), 2.9, 3.6, boxstyle="round,pad=0.15",
                                     ec=border_col, fc=bg_col, lw=1.8)
        ax.add_patch(box)
        ax.text(x_pos + 1.45, 3.6, title, ha="center", va="center",
                color=text_col, fontsize=11, fontweight="bold")
        
        bullet_str = "\n".join(bullets)
        ax.text(x_pos + 0.25, 2.0, bullet_str, ha="left", va="center",
                color="#1F2937", fontsize=10, linespacing=1.9)

    # Arrows between stages
    ax.annotate("", xy=(3.7, 2.2), xytext=(3.4, 2.2),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2.5, mutation_scale=18))
    ax.annotate("", xy=(7.1, 2.2), xytext=(6.8, 2.2),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2.5, mutation_scale=18))

    out_path = os.path.join("diagrams", "diagram_2_evolution.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_3():
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    tiers = [
        ("TẦNG 1: TIỀN TRUY XUẤT", "#EFF6FF", "#2563EB", "#1E40AF", [
            "• Phân đoạn ngữ nghĩa phân tầng",
            "• Trích xuất và gắn siêu dữ liệu (thời gian, tác giả, chuyên mục)",
            "• Viết lại và mở rộng câu hỏi truy vấn",
            "• Tạo văn bản giả định phục vụ tìm kiếm chính xác"
        ], 5.8),
        ("TẦNG 2: TRONG TRUY XUẤT", "#F0FDFA", "#0D9488", "#0F766E", [
            "• Tìm kiếm lai kết hợp vector dày đặc và từ khóa",
            "• Thuật toán hợp nhất thứ hạng tương hỗ",
            "• Sử dụng mô hình nhúng đa ngôn ngữ tiên tiến"
        ], 3.2),
        ("TẦNG 3: HẬU TRUY XUẤT", "#FEF3C7", "#D97706", "#B45309", [
            "• Tái xếp hạng chéo nơ-ron độ chính xác cao",
            "• Nén ngữ cảnh và trích lọc các câu mang dữ kiện cốt lõi",
            "• Tái cấu trúc vị trí tài liệu chống suy giảm chú ý"
        ], 0.6)
    ]

    for title, bg_col, border_col, text_col, bullets, y_pos in tiers:
        box = patches.FancyBboxPatch((0.8, y_pos), 8.4, 2.1, boxstyle="round,pad=0.2",
                                     ec=border_col, fc=bg_col, lw=1.8)
        ax.add_patch(box)
        ax.text(1.2, y_pos + 1.7, title, ha="left", va="center",
                color=text_col, fontsize=12, fontweight="bold")
        
        bullet_str = "\n".join(bullets)
        ax.text(1.4, y_pos + 0.85, bullet_str, ha="left", va="center",
                color="#1F2937", fontsize=10.5, linespacing=1.8)

    # Downward connecting arrows
    ax.annotate("", xy=(5.0, 5.4), xytext=(5.0, 5.7),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2.5, mutation_scale=18))
    ax.annotate("", xy=(5.0, 2.8), xytext=(5.0, 3.1),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2.5, mutation_scale=18))

    out_path = os.path.join("diagrams", "diagram_3_advanced_rag.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_4():
    fig, ax = plt.subplots(figsize=(10.5, 6.5), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Title header
    box_header = patches.FancyBboxPatch((2.0, 5.4), 6.5, 0.8, boxstyle="round,pad=0.15",
                                        ec="#1B365D", fc="#1B365D", lw=2)
    ax.add_patch(box_header)
    ax.text(5.25, 5.8, "BỐN TRỤ CỘT ĐO LƯỜNG ĐÁNH GIÁ CHẤT LƯỢNG RAGAS",
            ha="center", va="center", color="white", fontsize=12, fontweight="bold")

    # Column Left: Retrieval
    box_ret = patches.FancyBboxPatch((0.5, 0.6), 4.4, 4.4, boxstyle="round,pad=0.2",
                                     ec="#2563EB", fc="#EFF6FF", lw=1.6)
    ax.add_patch(box_ret)
    ax.text(2.7, 4.6, "ĐO LƯỜNG KHÂU TRUY XUẤT", ha="center", va="center",
            color="#1E40AF", fontsize=12, fontweight="bold")

    cp_box = patches.FancyBboxPatch((0.8, 2.8), 3.8, 1.4, boxstyle="round,pad=0.1",
                                    ec="#93C5FD", fc="#FFFFFF", lw=1.2)
    ax.add_patch(cp_box)
    ax.text(1.0, 3.8, "Chỉ số Context Precision", ha="left", va="center",
            color="#1E3A8A", fontsize=11, fontweight="bold")
    ax.text(1.0, 3.2, "Đo mức độ ưu tiên xếp hạng tài liệu\nchứa câu trả lời đúng ở đầu danh sách",
            ha="left", va="center", color="#374151", fontsize=9.5, linespacing=1.5)

    cr_box = patches.FancyBboxPatch((0.8, 0.9), 3.8, 1.4, boxstyle="round,pad=0.1",
                                    ec="#93C5FD", fc="#FFFFFF", lw=1.2)
    ax.add_patch(cr_box)
    ax.text(1.0, 1.9, "Chỉ số Context Recall", ha="left", va="center",
            color="#1E3A8A", fontsize=11, fontweight="bold")
    ax.text(1.0, 1.3, "Đo tỷ lệ bao phủ tất cả dữ kiện cần\nthiết có mặt trong tập ngữ cảnh tìm về",
            ha="left", va="center", color="#374151", fontsize=9.5, linespacing=1.5)

    # Column Right: Generation
    box_gen = patches.FancyBboxPatch((5.6, 0.6), 4.4, 4.4, boxstyle="round,pad=0.2",
                                     ec="#0D9488", fc="#F0FDFA", lw=1.6)
    ax.add_patch(box_gen)
    ax.text(7.8, 4.6, "ĐO LƯỜNG KHÂU SINH", ha="center", va="center",
            color="#0F766E", fontsize=12, fontweight="bold")

    f_box = patches.FancyBboxPatch((5.9, 2.8), 3.8, 1.4, boxstyle="round,pad=0.1",
                                   ec="#99F6E4", fc="#FFFFFF", lw=1.2)
    ax.add_patch(f_box)
    ax.text(6.1, 3.8, "Chỉ số Faithfulness", ha="left", va="center",
            color="#115E59", fontsize=11, fontweight="bold")
    ax.text(6.1, 3.2, "Đo độ trung thực, đảm bảo câu trả lời\nđều có căn cứ từ tài liệu (chống ảo giác)",
            ha="left", va="center", color="#374151", fontsize=9.5, linespacing=1.5)

    ar_box = patches.FancyBboxPatch((5.9, 0.9), 3.8, 1.4, boxstyle="round,pad=0.1",
                                    ec="#99F6E4", fc="#FFFFFF", lw=1.2)
    ax.add_patch(ar_box)
    ax.text(6.1, 1.9, "Chỉ số Answer Relevance", ha="left", va="center",
            color="#115E59", fontsize=11, fontweight="bold")
    ax.text(6.1, 1.3, "Đo mức độ bám sát trọng tâm câu hỏi,\ntránh trả lời lan man hoặc lạc đề",
            ha="left", va="center", color="#374151", fontsize=9.5, linespacing=1.5)

    # Connecting arrow between columns
    ax.annotate("", xy=(5.5, 2.8), xytext=(5.0, 2.8),
                arrowprops=dict(arrowstyle="<|-|>", color="#1B365D", lw=2, mutation_scale=15))

    out_path = os.path.join("diagrams", "diagram_4_ragas.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_5():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Top: Raw Doc
    b_doc = patches.FancyBboxPatch((3.0, 6.2), 4.0, 0.8, boxstyle="round,pad=0.15",
                                   ec="#475569", fc="#F1F5F9", lw=1.5)
    ax.add_patch(b_doc)
    ax.text(5.0, 6.6, "Tài liệu văn bản thô ban đầu", ha="center", va="center",
            color="#1E293B", fontsize=11.5, fontweight="bold")

    # Step 1: Extraction
    b_ext = patches.FancyBboxPatch((2.4, 4.8), 5.2, 0.8, boxstyle="round,pad=0.15",
                                   ec="#2563EB", fc="#EFF6FF", lw=1.5)
    ax.add_patch(b_ext)
    ax.text(5.0, 5.2, "Trích xuất Thực thể và Mối quan hệ bằng LLM", ha="center", va="center",
            color="#1E40AF", fontsize=11, fontweight="bold")

    # Fork Left: KG
    b_kg = patches.FancyBboxPatch((0.5, 3.4), 4.2, 0.8, boxstyle="round,pad=0.15",
                                  ec="#7C3AED", fc="#F5F3FF", lw=1.5)
    ax.add_patch(b_kg)
    ax.text(2.6, 3.8, "Xây dựng Đồ thị Tri thức", ha="center", va="center",
            color="#6D28D9", fontsize=11, fontweight="bold")

    b_comm = patches.FancyBboxPatch((0.5, 2.1), 4.2, 0.8, boxstyle="round,pad=0.15",
                                    ec="#7C3AED", fc="#F5F3FF", lw=1.5)
    ax.add_patch(b_comm)
    ax.text(2.6, 2.5, "Phân cụm cộng đồng và tóm tắt toàn cục", ha="center", va="center",
            color="#6D28D9", fontsize=10.5, fontweight="bold")

    # Fork Right: Vector
    b_vec = patches.FancyBboxPatch((5.3, 3.4), 4.2, 0.8, boxstyle="round,pad=0.15",
                                   ec="#0D9488", fc="#F0FDFA", lw=1.5)
    ax.add_patch(b_vec)
    ax.text(7.4, 3.8, "Lập chỉ mục Không gian Vector", ha="center", va="center",
            color="#0F766E", fontsize=11, fontweight="bold")

    b_loc = patches.FancyBboxPatch((5.3, 2.1), 4.2, 0.8, boxstyle="round,pad=0.15",
                                   ec="#0D9488", fc="#F0FDFA", lw=1.5)
    ax.add_patch(b_loc)
    ax.text(7.4, 2.5, "Hỏi đáp cục bộ dựa trên dữ kiện cụ thể", ha="center", va="center",
            color="#0F766E", fontsize=10.5, fontweight="bold")

    # Bottom: Merged
    b_ans = patches.FancyBboxPatch((1.8, 0.5), 6.4, 0.9, boxstyle="round,pad=0.2",
                                   ec="#1B365D", fc="#1B365D", lw=2)
    ax.add_patch(b_ans)
    ax.text(5.0, 0.95, "CÂU TRẢ LỜI TOÀN DIỆN VÀ ĐA CHIỀU", ha="center", va="center",
            color="white", fontsize=12, fontweight="bold")

    # Connecting arrows
    ax.annotate("", xy=(5.0, 5.7), xytext=(5.0, 6.1),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(2.6, 4.3), xytext=(4.0, 4.7),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(7.4, 4.3), xytext=(6.0, 4.7),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(2.6, 3.0), xytext=(2.6, 3.3),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=1.8, mutation_scale=15))
    ax.annotate("", xy=(7.4, 3.0), xytext=(7.4, 3.3),
                arrowprops=dict(arrowstyle="-|>", color="#0D9488", lw=1.8, mutation_scale=15))
    ax.annotate("", xy=(4.0, 1.5), xytext=(2.6, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(6.0, 1.5), xytext=(7.4, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))

    out_path = os.path.join("diagrams", "diagram_5_graphrag.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_6():
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Step 1: Input Query
    b_q = patches.FancyBboxPatch((2.8, 7.4), 4.4, 0.75, boxstyle="round,pad=0.15",
                                 ec="#475569", fc="#F8FAFC", lw=1.5)
    ax.add_patch(b_q)
    ax.text(5.0, 7.78, "Câu hỏi người dùng đầu vào", ha="center", va="center",
            color="#1E293B", fontsize=11, fontweight="bold")

    # Decision 1
    b_dec1 = patches.FancyBboxPatch((2.2, 5.9), 5.6, 0.8, boxstyle="round,pad=0.15",
                                    ec="#2563EB", fc="#EFF6FF", lw=1.8)
    ax.add_patch(b_dec1)
    ax.text(5.0, 6.3, "Mô hình tự đánh giá: Có cần tra cứu tri thức ngoài?", ha="center", va="center",
            color="#1E40AF", fontsize=10.5, fontweight="bold")

    # Side branch NO
    b_no = patches.FancyBboxPatch((7.6, 5.0), 2.1, 0.7, boxstyle="round,pad=0.1",
                                  ec="#94A3B8", fc="#F1F5F9", lw=1.2)
    ax.add_patch(b_no)
    ax.text(8.65, 5.35, "Sinh đáp án trực tiếp\ntừ Bộ nhớ tham số", ha="center", va="center",
            color="#475569", fontsize=9)

    # Retrieval
    b_ret = patches.FancyBboxPatch((2.5, 4.6), 5.0, 0.75, boxstyle="round,pad=0.15",
                                   ec="#0D9488", fc="#F0FDFA", lw=1.5)
    ax.add_patch(b_ret)
    ax.text(5.0, 4.98, "Truy xuất tập tài liệu liên quan", ha="center", va="center",
            color="#0F766E", fontsize=11, fontweight="bold")

    # Decision 2: Relevance
    b_dec2 = patches.FancyBboxPatch((2.0, 3.3), 6.0, 0.75, boxstyle="round,pad=0.15",
                                    ec="#D97706", fc="#FEF3C7", lw=1.5)
    ax.add_patch(b_dec2)
    ax.text(5.0, 3.68, "Đánh giá mức độ liên quan của từng tài liệu tìm về", ha="center", va="center",
            color="#B45309", fontsize=10.5, fontweight="bold")

    # Step 3: Generation & Support
    b_gen = patches.FancyBboxPatch((2.2, 2.0), 5.6, 0.75, boxstyle="round,pad=0.15",
                                   ec="#2563EB", fc="#EFF6FF", lw=1.5)
    ax.add_patch(b_gen)
    ax.text(5.0, 2.38, "Sinh câu trả lời và kiểm chứng tính xác thực", ha="center", va="center",
            color="#1E40AF", fontsize=10.5, fontweight="bold")

    # Output
    b_out = patches.FancyBboxPatch((2.4, 0.6), 5.2, 0.85, boxstyle="round,pad=0.2",
                                   ec="#16A34A", fc="#DCFCE7", lw=2)
    ax.add_patch(b_out)
    ax.text(5.0, 1.02, "CÂU TRẢ LỜI ĐẠT CHUẨN ĐÃ ĐƯỢC XÁC THỰC", ha="center", va="center",
            color="#15803D", fontsize=11.5, fontweight="bold")

    # Connecting arrows
    ax.annotate("", xy=(5.0, 6.8), xytext=(5.0, 7.3),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(7.5, 5.4), xytext=(6.5, 5.9),
                arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=1.5, mutation_scale=12))
    ax.annotate("", xy=(5.0, 5.5), xytext=(5.0, 5.8),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(5.0, 4.2), xytext=(5.0, 4.5),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(5.0, 2.9), xytext=(5.0, 3.2),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(5.0, 1.6), xytext=(5.0, 1.9),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=2.2, mutation_scale=15))

    out_path = os.path.join("diagrams", "diagram_6_self_rag.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_7():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # Header
    box_header = patches.FancyBboxPatch((2.2, 4.4), 6.6, 0.8, boxstyle="round,pad=0.15",
                                        ec="#1B365D", fc="#1B365D", lw=2)
    ax.add_patch(box_header)
    ax.text(5.5, 4.8, "KIẾN TRÚC CỘNG SINH: RAG VÀ LONG-CONTEXT LLM",
            ha="center", va="center", color="white", fontsize=12, fontweight="bold")

    # Step 1: User Query
    b_q = patches.FancyBboxPatch((0.5, 2.2), 2.2, 1.4, boxstyle="round,pad=0.15",
                                ec="#475569", fc="#F8FAFC", lw=1.5)
    ax.add_patch(b_q)
    ax.text(1.6, 3.1, "TRUY VẤN", ha="center", va="center", color="#1E293B", fontsize=11, fontweight="bold")
    ax.text(1.6, 2.5, "Câu hỏi nghiên cứu\nphức tạp của người dùng", ha="center", va="center", color="#64748B", fontsize=9)

    # Step 2: RAG Filter
    b_rag = patches.FancyBboxPatch((3.4, 0.8), 3.8, 3.0, boxstyle="round,pad=0.2",
                                  ec="#2563EB", fc="#EFF6FF", lw=1.8)
    ax.add_patch(b_rag)
    ax.text(5.3, 3.4, "BỘ LỌC THÔNG MINH RAG", ha="center", va="center", color="#1E40AF", fontsize=11.5, fontweight="bold")
    rag_info = (
        "• Tìm kiếm trong hàng triệu tài liệu\n"
        "• Lọc bỏ 99.9% dữ liệu rác, không liên quan\n"
        "• Định vị cực nhanh trong vài mili-giây\n"
        "• Tiết kiệm 95% chi phí điện toán gọi API\n"
        "• Phân quyền bảo mật tại tầng CSDL Vector"
    )
    ax.text(3.7, 2.0, rag_info, ha="left", va="center", color="#1F2937", fontsize=9.5, linespacing=1.6)

    # Step 3: Long Context LLM
    b_llm = patches.FancyBboxPatch((7.9, 0.8), 2.8, 3.0, boxstyle="round,pad=0.2",
                                   ec="#0D9488", fc="#F0FDFA", lw=1.8)
    ax.add_patch(b_llm)
    ax.text(9.3, 3.4, "LONG-CONTEXT LLM", ha="center", va="center", color="#0F766E", fontsize=11.5, fontweight="bold")
    llm_info = (
        "• Nhận 20-30 trang tinh chọn\n"
        "• Suy luận sâu sắc nhiều bước\n"
        "• Tổng hợp tri thức đa nguồn\n"
        "• Loại bỏ suy giảm chú ý\n"
        "• Sinh phản hồi chính xác"
    )
    ax.text(8.1, 2.0, llm_info, ha="left", va="center", color="#1F2937", fontsize=9.5, linespacing=1.6)

    # Arrows
    ax.annotate("", xy=(3.3, 2.9), xytext=(2.8, 2.9),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(7.8, 2.3), xytext=(7.3, 2.3),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))

    out_path = os.path.join("diagrams", "diagram_7_symbiotic.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_8():
    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Header
    box_header = patches.FancyBboxPatch((1.8, 6.4), 6.9, 0.8, boxstyle="round,pad=0.15",
                                        ec="#1B365D", fc="#1B365D", lw=2)
    ax.add_patch(box_header)
    ax.text(5.25, 6.8, "LỘ TRÌNH NGHIÊN CỨU VÀ PHÁT TRIỂN TIẾP THEO",
            ha="center", va="center", color="white", fontsize=12, fontweight="bold")

    phases = [
        ("GIAI ĐOẠN 1: MỞ RỘNG DỮ LIỆU VÀ MÔ HÌNH NHÚNG", "#EFF6FF", "#2563EB", "#1E40AF", [
            "• Thu thập và chuẩn hóa tập ngữ liệu 100+ bài báo khoa học toàn văn",
            "• Vi chỉnh mô hình nhúng tiếng Việt chuyên biệt với hàm mất mát InfoNCE",
            "• Đánh giá và kiểm chuẩn mô hình nhúng trên bảng xếp hạng MTEB tiếng Việt"
        ], 4.4),
        ("GIAI ĐOẠN 2: TÁC TỬ TỰ HÀNH VÀ ĐỒ THỊ TRI THỨC", "#F0FDFA", "#0D9488", "#0F766E", [
            "• Tích hợp GraphRAG với thuật toán phân cụm cộng đồng Leiden cho câu hỏi toàn cục",
            "• Xây dựng Tác tử Agentic RAG đa công cụ kết hợp tự phản chiếu và tìm kiếm internet",
            "• Hiện thực hóa cơ chế kiểm định ngưỡng tin cậy dữ kiện theo Corrective RAG"
        ], 2.4),
        ("GIAI ĐOẠN 3: ĐO KIỂM TOÀN TRÌNH VÀ CỤM PHÂN TÁN", "#FEF3C7", "#D97706", "#B45309", [
            "• Tích hợp mô hình ngôn ngữ lớn đầu cuối và vận hành đo kiểm toàn diện bằng RAGAS",
            "• Chuyển dịch hệ thống lưu trữ sang cụm máy chủ phân tán Qdrant hiệu năng cao",
            "• Kiểm thử tải nặng đo lường thông lượng QPS và độ trễ phân vị p95/p99"
        ], 0.4)
    ]

    for title, bg_col, border_col, text_col, bullets, y_pos in phases:
        box = patches.FancyBboxPatch((0.8, y_pos), 8.9, 1.7, boxstyle="round,pad=0.15",
                                     ec=border_col, fc=bg_col, lw=1.6)
        ax.add_patch(box)
        ax.text(1.2, y_pos + 1.35, title, ha="left", va="center",
                color=text_col, fontsize=11, fontweight="bold")
        bullet_str = "\n".join(bullets)
        ax.text(1.4, y_pos + 0.65, bullet_str, ha="left", va="center",
                color="#1F2937", fontsize=9.5, linespacing=1.6)

    # Downward connecting arrows
    ax.annotate("", xy=(5.25, 4.15), xytext=(5.25, 4.35),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2.2, mutation_scale=15))
    ax.annotate("", xy=(5.25, 2.15), xytext=(5.25, 2.35),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2.2, mutation_scale=15))

    out_path = os.path.join("diagrams", "diagram_8_roadmap.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_prisma():
    fig, ax = plt.subplots(figsize=(10.5, 6.0), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.0)
    ax.axis('off')

    stages = [
        ("GIAI ĐOẠN 1: XÁC ĐỊNH NGUỒN", "#EFF6FF", "#2563EB", "#1E40AF", [
            "• Truy vấn arXiv, ACL, NeurIPS",
            "• Thu thập ban đầu: 280 tài liệu"
        ], 0.4),
        ("GIAI ĐOẠN 2: SÀNG LỌC SƠ BỘ", "#FEF3C7", "#D97706", "#B45309", [
            "• Đọc tiêu đề và tóm tắt",
            "• Loại bỏ 195 bài không phù hợp",
            "• Còn lại 85 bài vào vòng thẩm định"
        ], 2.9),
        ("GIAI ĐOẠN 3: ĐÁNH GIÁ TOÀN VĂN", "#F0FDFA", "#0D9488", "#0F766E", [
            "• Đọc toàn văn chuyên sâu",
            "• Kiểm tra số trích dẫn và uy tín",
            "• Chọn lọc 15 bài phân tích kỹ"
        ], 5.5),
        ("GIAI ĐOẠN 4: TẬP NGỮ LIỆU", "#DCFCE7", "#16A34A", "#15803D", [
            "• 5 công trình hạt nhân",
            "• Trích xuất thành 220 đoạn trích",
            "• Chuẩn hóa dữ liệu thực nghiệm"
        ], 8.0)
    ]

    for title, bg_col, border_col, text_col, bullets, x_pos in stages:
        box = patches.FancyBboxPatch((x_pos, 0.8), 2.2, 4.2, boxstyle="round,pad=0.15",
                                     ec=border_col, fc=bg_col, lw=1.6)
        ax.add_patch(box)
        ax.text(x_pos + 1.1, 4.6, title, ha="center", va="center",
                color=text_col, fontsize=9.5, fontweight="bold")
        bullet_str = "\n".join(bullets)
        ax.text(x_pos + 0.15, 2.6, bullet_str, ha="left", va="center",
                color="#1F2937", fontsize=9, linespacing=1.7)

    # Arrows between stages
    ax.annotate("", xy=(2.85, 2.8), xytext=(2.65, 2.8),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(5.45, 2.8), xytext=(5.25, 2.8),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
    ax.annotate("", xy=(7.95, 2.8), xytext=(7.75, 2.8),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))

    out_path = os.path.join("diagrams", "diagram_prisma.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_pipeline():
    fig, ax = plt.subplots(figsize=(10.5, 6.8), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.8)
    ax.axis('off')

    steps = [
        ("BƯỚC 1: TRÍCH XUẤT TÀI LIỆU PDF", "#F8FAFC", "#475569", "#1E293B",
         "Sử dụng PyMuPDF trích xuất văn bản từng trang riêng biệt từ 5 bài báo khoa học", 5.6),
        ("BƯỚC 2: PHÂN ĐOẠN VĂN BẢN CỬA SỔ TRƯỢT", "#EFF6FF", "#2563EB", "#1E40AF",
         "Kích thước 600 từ, độ gối đầu 100 từ bảo đảm tính toàn vẹn công thức và ngữ cảnh logic", 4.3),
        ("BƯỚC 3: MÃ HÓA VECTOR VÀ NHÚNG NGỮ NGHĨA", "#F0FDFA", "#0D9488", "#0F766E",
         "Mô hình BAAI/bge-small-en-v1.5 qua FastEmbed trên ONNX Runtime CPU (384 chiều, 15ms/đoạn)", 3.0),
        ("BƯỚC 4: LẬP CHỈ MỤC VÀ LƯU TRỮ TRONG CHROMADB", "#FEF3C7", "#D97706", "#B45309",
         "Lập chỉ mục đồ thị phân tầng HNSW với không gian Cosine, lưu trữ 220 đoạn văn bản bền vững", 1.7),
        ("BƯỚC 5: TRUY VẤN VÀ CHUẨN HÓA ĐIỂM TƯƠNG ĐỒNG", "#DCFCE7", "#16A34A", "#15803D",
         "Mã hóa câu hỏi, tìm kiếm top-k láng giềng gần nhất, tính Similarity Score = 1.0 - Cosine Distance", 0.4)
    ]

    for title, bg_col, border_col, text_col, desc, y_pos in steps:
        box = patches.FancyBboxPatch((1.0, y_pos), 8.5, 0.95, boxstyle="round,pad=0.15",
                                     ec=border_col, fc=bg_col, lw=1.5)
        ax.add_patch(box)
        ax.text(1.3, y_pos + 0.65, title, ha="left", va="center",
                color=text_col, fontsize=10.5, fontweight="bold")
        ax.text(1.3, y_pos + 0.28, desc, ha="left", va="center",
                color="#374151", fontsize=9)

    for y in [5.55, 4.25, 2.95, 1.65]:
        ax.annotate("", xy=(5.25, y - 0.25), xytext=(5.25, y),
                    arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=1.8, mutation_scale=12))

    out_path = os.path.join("diagrams", "diagram_pipeline.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_parametric_vs_rag():
    fig, ax = plt.subplots(figsize=(11, 5.0), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.0)
    ax.axis('off')

    # Left: Parametric
    b1 = patches.FancyBboxPatch((0.5, 0.6), 4.6, 3.8, boxstyle="round,pad=0.2",
                                ec="#EF4444", fc="#FEF2F2", lw=1.6)
    ax.add_patch(b1)
    ax.text(2.8, 3.9, "MÔ HÌNH THUẦN THAM SỐ", ha="center", va="center", color="#B91C1C", fontsize=11.5, fontweight="bold")
    t1 = (
        "• Truy vấn người dùng gửi thẳng vào LLM\n"
        "• Dựa 100% vào trọng số ma trận đóng băng\n"
        "• Tối ưu hóa xác suất lưu loát ngôn từ\n"
        "• Nguy cơ cao xuất hiện ảo giác tri thức\n"
        "• Mù thông tin sự kiện sau điểm dừng dữ liệu\n"
        "• Bất khả thi truy cập tài liệu nội bộ"
    )
    ax.text(0.8, 2.2, t1, ha="left", va="center", color="#1F2937", fontsize=9.5, linespacing=1.6)

    # Right: RAG
    b2 = patches.FancyBboxPatch((5.9, 0.6), 4.6, 3.8, boxstyle="round,pad=0.2",
                                ec="#10B981", fc="#ECFDF5", lw=1.6)
    ax.add_patch(b2)
    ax.text(8.2, 3.9, "KIẾN TRÚC RAG (CỘNG SINH)", ha="center", va="center", color="#047857", fontsize=11.5, fontweight="bold")
    t2 = (
        "• Truy vấn kích hoạt tìm kiếm tài liệu liên quan\n"
        "• Bộ nhớ phi tham số lưu kho tri thức ngoài\n"
        "• Cung cấp dữ kiện chính xác và cập nhật động\n"
        "• LLM đóng vai trò bộ não suy luận ngữ cảnh\n"
        "• Câu trả lời có căn cứ minh chứng rõ ràng\n"
        "• Phân quyền bảo mật tại tầng CSDL Vector"
    )
    ax.text(6.2, 2.2, t2, ha="left", va="center", color="#1F2937", fontsize=9.5, linespacing=1.6)

    # Center arrow
    ax.annotate("", xy=(5.8, 2.5), xytext=(5.2, 2.5),
                arrowprops=dict(arrowstyle="<|-|>", color="#1B365D", lw=2, mutation_scale=15))

    out_path = os.path.join("diagrams", "diagram_parametric_vs_rag.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_scope():
    fig, ax = plt.subplots(figsize=(11, 5.0), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.0)
    ax.axis('off')

    # Left: Scope
    b1 = patches.FancyBboxPatch((0.5, 1.4), 4.6, 3.0, boxstyle="round,pad=0.15",
                                ec="#2563EB", fc="#EFF6FF", lw=1.6)
    ax.add_patch(b1)
    ax.text(2.8, 3.9, "PHẠM VI NGHIÊN CỨU", ha="center", va="center", color="#1E40AF", fontsize=11, fontweight="bold")
    t1 = (
        "• Dữ liệu: 5 bài báo khoa học nền tảng\n"
        "• Tác vụ: Truy xuất ngữ nghĩa và phân đoạn\n"
        "• Công nghệ: ChromaDB + FastEmbed (ONNX)\n"
        "• Ngữ liệu: Tài liệu học thuật tiếng Anh chuẩn"
    )
    ax.text(0.8, 2.6, t1, ha="left", va="center", color="#1F2937", fontsize=9.5, linespacing=1.6)

    # Right: Exclusions
    b2 = patches.FancyBboxPatch((5.9, 1.4), 4.6, 3.0, boxstyle="round,pad=0.15",
                                ec="#64748B", fc="#F8FAFC", lw=1.6)
    ax.add_patch(b2)
    ax.text(8.2, 3.9, "GIỚI HẠN LOẠI TRỪ", ha="center", va="center", color="#475569", fontsize=11, fontweight="bold")
    t2 = (
        "• Không triển khai RAG video, âm thanh đa phương\n"
        "• Không phụ thuộc API mô hình thương mại đóng\n"
        "• Không thực hiện tinh chỉnh toàn phần trọng số LLM\n"
        "• Không thử nghiệm dữ liệu mạng xã hội mở"
    )
    ax.text(6.2, 2.6, t2, ha="left", va="center", color="#1F2937", fontsize=9.5, linespacing=1.6)

    # Bottom focus
    bf = patches.FancyBboxPatch((2.2, 0.2), 6.6, 0.8, boxstyle="round,pad=0.15",
                                ec="#1B365D", fc="#1B365D", lw=2)
    ax.add_patch(bf)
    ax.text(5.5, 0.6, "HỆ THỐNG RAG CỤC BỘ HIỆU NĂNG CAO CHO TÀI LIỆU KHOA HỌC",
            ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")

    ax.annotate("", xy=(4.0, 1.0), xytext=(2.8, 1.3),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=1.6, mutation_scale=12))
    ax.annotate("", xy=(7.0, 1.0), xytext=(8.2, 1.3),
                arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=1.6, mutation_scale=12))

    out_path = os.path.join("diagrams", "diagram_scope.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

def create_diagram_structure():
    fig, ax = plt.subplots(figsize=(11, 2.8), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 2.8)
    ax.axis('off')

    chapters = [
        ("Chương 1", "Đặt vấn đề\n& Khoảng trống", 0.3, "#EFF6FF", "#2563EB", "#1E40AF"),
        ("Chương 2", "Cơ sở lý thuyết\n& Ba thế hệ", 2.5, "#F0FDFA", "#0D9488", "#0F766E"),
        ("Chương 3", "Phương pháp\n& Thiết kế HT", 4.7, "#FEF3C7", "#D97706", "#B45309"),
        ("Chương 4", "Kết quả thực nghiệm\n& Thảo luận", 6.9, "#DCFCE7", "#16A34A", "#15803D"),
        ("Chương 5", "Kết luận, Hạn chế\n& Lộ trình", 9.1, "#FAF5FF", "#9333EA", "#7E22CE")
    ]

    for ch_title, ch_desc, x, bg_col, b_col, t_col in chapters:
        b = patches.FancyBboxPatch((x, 0.4), 1.6, 1.9, boxstyle="round,pad=0.1",
                                   ec=b_col, fc=bg_col, lw=1.5)
        ax.add_patch(b)
        ax.text(x + 0.8, 1.85, ch_title, ha="center", va="center", color=t_col, fontsize=10, fontweight="bold")
        ax.text(x + 0.8, 1.05, ch_desc, ha="center", va="center", color="#1F2937", fontsize=8.5, linespacing=1.4)

    for x in [1.95, 4.15, 6.35, 8.55]:
        ax.annotate("", xy=(x + 0.5, 1.35), xytext=(x, 1.35),
                    arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=14))

    out_path = os.path.join("diagrams", "diagram_structure.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[OK] Saved {out_path}")

from generate_new_multimodal_diagrams import create_diagram_qa_workflow, create_diagram_multimodal_rag

def main():
    print("=" * 70)
    print(" KHỞI TẠO BỘ 15 HÌNH ẢNH SƠ ĐỒ HỌC THUẬT ĐỘ PHÂN GIẢI CAO (300 DPI)")
    print("=" * 70)
    create_diagram_1()
    create_diagram_2()
    create_diagram_3()
    create_diagram_4()
    create_diagram_5()
    create_diagram_6()
    create_diagram_7()
    create_diagram_8()
    create_diagram_prisma()
    create_diagram_pipeline()
    create_diagram_parametric_vs_rag()
    create_diagram_scope()
    create_diagram_structure()
    create_diagram_qa_workflow()
    create_diagram_multimodal_rag()
    print("\n[✓] Toàn bộ 15 sơ đồ hình ảnh PNG đã được tạo thành công trong thư mục diagrams/")

if __name__ == "__main__":
    main()


