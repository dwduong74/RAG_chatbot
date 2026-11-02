# -*- coding: utf-8 -*-
import sys, re
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.md', encoding='utf-8') as f:
    text = f.read()

# Find English word followed by (Vietnamese text)
matches = re.findall(r'(\b[A-Za-z\s]{3,40}?)\s*\(([^\n()]*?[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ][^\n()]*?)\)', text)
print(f"Total English followed by (Vietnamese): {len(matches)}")
for b, ins in matches:
    print(f"\"{b.strip()}\" ---> \"({ins.strip()})\"")
