# -*- coding: utf-8 -*-
import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md', encoding='utf-8') as f:
    text = f.read()

def should_remove_parenthesis(before_text, inside_text):
    inside = inside_text.strip()
    
    # 1. Math formulas / equations
    if any(c in inside for c in ['$', '\\', '=', '+', '<', '>', '{', '}', '^', '_', '\u2208', '\u2211', '\u2248', '|', '%']):
        return False
        
    # 2. Numbering / enumerations
    if re.match(r'^(?:[0-9]+|[a-z]|[ivxIVX]+|\d+\.\d+|Trang \d+|v\d+(\.\d+)?)$', inside):
        return False
        
    # 3. Academic citations (author names, years, venues)
    if re.search(r'\b(19\d\d|20\d\d)\b', inside) or 'et al' in inside or any(v in inside for v in ['NeurIPS', 'NAACL', 'EMNLP', 'ICLR', 'AAAI', 'ACL', 'TACL', 'FAIR', 'UCL']):
        return False
        
    # 4. File names or code identifiers
    if any(inside.endswith(ext) for ext in ['.pdf', '.md', '.docx', '.py']) or inside.startswith('c:') or inside.startswith('file:'):
        return False
        
    # 5. In English Abstract section, don't remove standard English parentheses
    if 'rapid emergence' in before_text or 'solely on parametric' in before_text:
        return False
        
    # 6. Table of acronyms / Abbreviations list
    if 'Thuật ngữ Tiếng Anh đầy đủ' in before_text or '| **' in before_text:
        return False

    # Check if preceding text has Vietnamese characters (e.g., 'Tối ưu hóa Hậu truy xuất')
    has_vietnamese = bool(re.search(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', before_text, re.IGNORECASE))
    is_cap_heading = bool(re.search(r'#+\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s\d\.:]+$', before_text))
    
    # Check if inside is English phrase definition
    is_english_phrase = bool(re.match(r'^[A-Za-z0-9\s\-–—/&,\']+$', inside)) and not re.search(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', inside)
    
    # Exclude common single acronyms like (RAG), (LLM), (ODQA), (FEVER) if desired, BUT the user says:
    # "sửa lại file không tự ý dóng mở ngoạc định nghĩa ví dụ như 'Tối ưu hóa Hậu truy xuất (Post-Retrieval Optimization)' là không được"
    # Notice: Multi-word English definitions like 'Post-Retrieval Optimization', 'Parametric Memory', 'Large Language Models - LLMs'
    # are definitely unwanted.
    if (has_vietnamese or is_cap_heading) and is_english_phrase:
        return True
        
    return False

# Search for patterns: before_text (inside_text)
lines = text.split('\n')
removed_count = 0
cleaned_lines = []

for line in lines:
    # If line is in English Abstract or References, skip modifying
    if '#### English Abstract' in line:
        cleaned_lines.append(line)
        continue
        
    # Regex to find (something)
    # We replace matching parentheses
    def replacer(match):
        global removed_count
        full = match.group(0)
        before = match.group(1)
        inside = match.group(2)
        if should_remove_parenthesis(before, inside):
            removed_count += 1
            print(f"[{removed_count}] REMOVED: '{before.strip()}' + '({inside.strip()})'")
            return before.rstrip()
        return full

    new_line = re.sub(r'([^\n()]{2,60}?)\s*\(([^()\n]{2,80}?)\)', replacer, line)
    cleaned_lines.append(new_line)

print(f"\n[DONE] Total redundant parenthetical definitions removed: {removed_count}")
