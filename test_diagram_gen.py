# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("diagrams", exist_ok=True)

plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Calibri']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# Root box
bbox_root = patches.FancyBboxPatch((2.5, 4.8), 5.0, 0.9, boxstyle="round,pad=0.2",
                                   ec="#1B365D", fc="#1B365D", lw=2)
ax.add_patch(bbox_root)
ax.text(5.0, 5.25, "HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC",
        ha="center", va="center", color="white", fontsize=13, fontweight="bold")

# Parametric Box
bbox_pm = patches.FancyBboxPatch((0.5, 0.5), 4.2, 3.5, boxstyle="round,pad=0.2",
                                ec="#2563EB", fc="#EFF6FF", lw=1.5)
ax.add_patch(bbox_pm)
ax.text(2.6, 3.6, "BỘ NHỚ THAM SỐ", ha="center", va="center",
        color="#1E40AF", fontsize=12, fontweight="bold")

pm_text = (
    "• Trọng số mạng nơ-ron Transformer\n"
    "• Học qua giải thuật Lan truyền ngược\n"
    "• Năng lực: Cú pháp, Ngữ nghĩa & Suy luận\n"
    "• Chi phí cập nhật: Rất cao (Tái huấn luyện)\n"
    "• Tính giải thích: Hộp đen nơ-ron phức tạp"
)
ax.text(0.8, 2.0, pm_text, ha="left", va="center", color="#1F2937", fontsize=10.5, linespacing=1.8)

# Non-Parametric Box
bbox_npm = patches.FancyBboxPatch((5.3, 0.5), 4.2, 3.5, boxstyle="round,pad=0.2",
                                 ec="#0D9488", fc="#F0FDFA", lw=1.5)
ax.add_patch(bbox_npm)
ax.text(7.4, 3.6, "BỘ NHỚ PHI THAM SỐ", ha="center", va="center",
        color="#0F766E", fontsize=12, fontweight="bold")

npm_text = (
    "• Cơ sở dữ liệu Vector và Chỉ mục HNSW\n"
    "• Kho tri thức tài liệu rời rạc (PDF, CSDL)\n"
    "• Cập nhật động theo thời gian thực\n"
    "• Chi phí cập nhật: Cực thấp\n"
    "• Tính giải thích: Truy vết nguồn gốc rõ ràng"
)
ax.text(5.6, 2.0, npm_text, ha="left", va="center", color="#1F2937", fontsize=10.5, linespacing=1.8)

# Arrows
ax.annotate("", xy=(2.6, 4.1), xytext=(4.0, 4.8),
            arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))
ax.annotate("", xy=(7.4, 4.1), xytext=(6.0, 4.8),
            arrowprops=dict(arrowstyle="-|>", color="#1B365D", lw=2, mutation_scale=15))

out_path = os.path.join("diagrams", "diagram_1_memory.png")
plt.tight_layout()
plt.savefig(out_path, bbox_inches='tight', dpi=300)
plt.close()

print(f"[OK] Diagram 1 saved to: {out_path} ({os.path.getsize(out_path)} bytes)")
