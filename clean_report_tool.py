# -*- coding: utf-8 -*-
"""
Tool lọc tự động các đóng mở ngoặc định nghĩa dịch tiếng Anh thừa trong tài liệu NCKH.
Tác vụ:
1. Quét và loại bỏ các định nghĩa mở ngoặc tiếng Anh kèm theo thuật ngữ tiếng Việt
   (Ví dụ: 'Tối ưu hóa Hậu truy xuất (Post-Retrieval Optimization)' -> 'Tối ưu hóa Hậu truy xuất')
2. Chuẩn hóa các đề mục tiếng Anh kèm mở ngoặc tiếng Việt thành tiếng Việt học thuật
   (Ví dụ: '#### 1. Faithfulness (Độ trung thực của câu trả lời)' -> '#### 1. Độ trung thực của câu trả lời')
3. Bảo toàn 100% trích dẫn học thuật (Lewis et al., 2020), công thức toán ($W$), số thứ tự (1, 2, a, b),
   danh mục từ viết tắt và phần tóm tắt tiếng Anh (English Abstract).
"""

import sys
import os
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Các trường hợp trích dẫn học thuật, hội nghị, công thức toán hoặc cấu trúc cần giữ nguyên
CITATION_PATTERNS = [
    r'\b(19\d\d|20\d\d)\b',
    r'et al',
    r'NeurIPS', r'NAACL', r'EMNLP', r'ICLR', r'AAAI', r'ACL', r'TACL',
    r'FAIR', r'UCL', r'Stanford', r'Microsoft Research'
]

def is_citation_or_math(inside_text):
    s = inside_text.strip()
    # Công thức toán / ký hiệu LaTeX
    if any(c in s for c in ['$', '\\', '=', '+', '<', '>', '{', '}', '^', '_', '\u2208', '\u2211', '\u2248', '|', '%']):
        return True
    # Đánh số thứ tự: (1), (2), (a), (b), (i), (Trang 9), v.v.
    if re.match(r'^(?:[0-9]+|[a-z]|[ivxIVX]+|\d+\.\d+|Trang \d+|v\d+(\.\d+)?)$', s):
        return True
    # Trích dẫn bài báo / tác giả / năm
    if any(re.search(pat, s, re.IGNORECASE) for pat in CITATION_PATTERNS):
        return True
    # Tên file / đường dẫn
    if any(s.endswith(ext) for ext in ['.pdf', '.md', '.docx', '.py', '.txt']) or s.startswith('c:') or s.startswith('file:'):
        return True
    return False

def clean_content_text(text, filename=""):
    lines = text.split('\n')
    cleaned_lines = []
    in_english_abstract = False
    in_abbreviations_table = False
    total_removed = 0
    
    # Danh sách các thay đổi mẫu cụ thể cho các tiêu đề lớn
    SPECIFIC_HEADER_REPLACEMENTS = {
        r'TỐI ƯU HÓA HẬU TRUY XUẤT\s*\([^)]+\)': 'TỐI ƯU HÓA HẬU TRUY XUẤT',
        r'Tối ưu hóa Hậu truy xuất\s*\([^)]+\)': 'Tối ưu hóa Hậu truy xuất',
        r'Tối ưu hóa Tiền truy xuất\s*\([^)]+\)': 'Tối ưu hóa Tiền truy xuất',
        r'Tối ưu hóa Trong truy xuất: Tìm kiếm Lai\s*\([^)]+\)': 'Tối ưu hóa Trong truy xuất: Tìm kiếm Lai',
        r'Naive RAG\s*\(Thế hệ 1:[^)]+\)': 'Kiến trúc Naive RAG',
        r'Advanced RAG\s*\(Thế hệ 2:[^)]+\)': 'Kiến trúc Advanced RAG',
        r'Modular RAG\s*\(Thế hệ 3:[^)]+\)': 'Kiến trúc Modular RAG',
        r'Faithfulness\s*\(Độ trung thực của câu trả lời\)': 'Độ trung thực của câu trả lời',
        r'Answer Relevance\s*\(Độ liên quan của câu trả lời với câu hỏi\)': 'Độ liên quan của câu trả lời với câu hỏi',
        r'Context Precision\s*\(Độ chính xác của ngữ cảnh truy xuất\)': 'Độ chính xác của ngữ cảnh truy xuất',
        r'Context Recall\s*\(Độ bao phủ của ngữ cảnh\)': 'Độ bao phủ của ngữ cảnh',
        r'Noise Robustness\s*\(Khả năng chống nhiễu\)': 'Khả năng chống nhiễu',
        r'Negative Rejection\s*\(Khả năng từ chối khi không có thông tin\)': 'Khả năng từ chối khi không có thông tin',
        r'Information Integration\s*\(Khả năng tích hợp đa nguồn\)': 'Khả năng tích hợp đa nguồn',
        r'Counterfactual Robustness\s*\(Khả năng chống tri thức phản thực tế\)': 'Khả năng chống tri thức phản thực tế',
        r'Fixed-Size Chunking\s*\(Cắt đoạn theo kích thước cố định\)': 'Cắt đoạn theo kích thước cố định',
        r'Sentence-Window Chunking\s*\(Cắt đoạn theo cửa sổ câu trượt\)': 'Cắt đoạn theo cửa sổ câu trượt',
        r'Semantic Chunking\s*\(Cắt đoạn dựa trên biến thiên ngữ nghĩa\)': 'Cắt đoạn dựa trên biến thiên ngữ nghĩa',
        r'Recursive Character Chunking\s*\(Cắt đệ quy theo dấu phân cách tự nhiên\)': 'Cắt đệ quy theo dấu phân cách tự nhiên',
        r'Long-Context LLMs\s*\(Cửa sổ 1M - 2M Tokens\)': 'Long-Context LLMs',
    }

    for line in lines:
        # Nhận diện vùng English Abstract để không lọc nhầm tiếng Anh gốc
        if '#### English Abstract' in line:
            in_english_abstract = True
            cleaned_lines.append(line)
            continue
        if in_english_abstract and line.startswith('### '):
            in_english_abstract = False

        if in_english_abstract:
            cleaned_lines.append(line)
            continue

        # Nhận diện bảng danh mục từ viết tắt
        if 'DANH MỤC TỪ VIẾT TẮT' in line:
            in_abbreviations_table = True
            cleaned_lines.append(line)
            continue
        if in_abbreviations_table and line.startswith('## '):
            in_abbreviations_table = False

        if in_abbreviations_table:
            cleaned_lines.append(line)
            continue

        # Áp dụng các thay thế tiêu đề cụ thể trước
        current_line = line
        for pat, repl in SPECIFIC_HEADER_REPLACEMENTS.items():
            if re.search(pat, current_line):
                current_line = re.sub(pat, repl, current_line)

        # Lọc mẫu chung: Cụm từ tiếng Việt theo sau là mở ngoặc định nghĩa tiếng Anh
        # Ví dụ: "bộ nhớ tham số (Parametric Memory)" -> "bộ nhớ tham số"
        def filter_paren(match):
            nonlocal total_removed
            full_match = match.group(0)
            before = match.group(1)
            inside = match.group(2)
            
            # Nếu chứa citation hoặc math -> giữ nguyên
            if is_citation_or_math(inside):
                return full_match

            # Kiểm tra xem trước ngoặc có tiếng Việt không
            has_vietnamese = bool(re.search(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', before, re.IGNORECASE))
            is_cap_heading = bool(re.search(r'#+\s+[A-ZÀ-Ỹ0-9\s\.:\-]+$', before))

            # Kiểm tra xem trong ngoặc có phải cụm từ tiếng Anh / định nghĩa thuần Latinh không
            is_english_phrase = bool(re.match(r'^[A-Za-z0-9\s\-–—/&,\']+$', inside.strip())) and not re.search(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', inside)

            if (has_vietnamese or is_cap_heading) and is_english_phrase:
                total_removed += 1
                # Nếu ngoặc nằm sát dấu in đậm **, xử lý chuẩn xác
                clean_before = before.rstrip()
                return clean_before

            return full_match

        # Thực thi lọc
        # Cấu trúc: [văn bản trước] ( [định nghĩa tiếng Anh] )
        new_line = re.sub(r'([^\n()]{2,60}?)\s*\(([^()\n]{2,80}?)\)', filter_paren, current_line)
        
        # Dọn dẹp khoảng trắng trước dấu in đậm ** nếu có
        new_line = re.sub(r'\s+\*\*', '**', new_line)
        # Khôi phục khoảng cách chuẩn cho gạch đầu dòng Markdown: "- **"
        new_line = re.sub(r'^-(\*\*)', r'- \1', new_line)
        # Dọn dẹp khoảng trắng đôi thừa
        new_line = re.sub(r'  +', ' ', new_line)

        cleaned_lines.append(new_line)

    result_text = '\n'.join(cleaned_lines)
    return result_text, total_removed

def process_file(filepath):
    print(f"[*] Processing file: {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaned, count = clean_content_text(content, os.path.basename(filepath))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
        
    print(f"    [OK] Filtered and removed {count} redundant parenthetical definitions.")
    return count

def main():
    print("=" * 70)
    print(" TOOL TỰ ĐỘNG LỌC ĐỊNH NGHĨA ĐÓNG MỞ NGOẶC THỪA TRONG BÁO CÁO NCKH RAG")
    print("=" * 70)
    
    target_files = [
        "report_content_part1.py",
        "report_content_part2.py",
        "report_content_part3.py",
        "report_content_appendices.py"
    ]
    
    total_all = 0
    for target in target_files:
        if os.path.exists(target):
            total_all += process_file(target)
            
    print("-" * 70)
    print(f"[✓] Tổng số định nghĩa mở ngoặc thừa đã được lọc sạch: {total_all}")
    print("[*] Tái biên dịch toàn bộ Báo cáo NCKH (Markdown & Word docx)...")
    
    # Re-run compiler
    import compile_research_report
    # Reload modules
    import importlib
    import report_content_part1
    import report_content_part2
    import report_content_part3
    import report_content_appendices
    importlib.reload(report_content_part1)
    importlib.reload(report_content_part2)
    importlib.reload(report_content_part3)
    importlib.reload(report_content_appendices)
    importlib.reload(compile_research_report)
    
    compile_research_report.main()
    print("[✓] Hoàn tất toàn bộ quy trình lọc và xuất bản!")

if __name__ == "__main__":
    main()
