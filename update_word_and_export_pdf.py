# -*- coding: utf-8 -*-
import os
import sys
import win32com.client

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

docx_path = os.path.abspath("BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.docx")
pdf_path = os.path.abspath("BAO_CAO_NGHIEN_CUU_KHOA_HOC_RAG.pdf")

print(f"[*] Đang khởi tạo ứng dụng Microsoft Word để cập nhật các trường và xuất PDF...")
word = win32com.client.Dispatch("Word.Application")
word.Visible = False

try:
    doc = word.Documents.Open(docx_path)
    
    # Cập nhật toàn bộ các trường trong văn bản (Mục lục, số trang)
    print("[*] Đang cập nhật toàn bộ Fields (Mục lục, tham chiếu)...")
    doc.Fields.Update()
    for toc in doc.TablesOfContents:
        toc.Update()
    
    # Lấy thông tin thống kê số trang thực tế
    page_count = doc.ComputeStatistics(2)  # 2 = wdStatisticPages
    print(f"[OK] Tổng số trang Word thực tế: {page_count} trang.")
    
    # Xuất file PDF chất lượng cao (17 = wdExportFormatPDF)
    print(f"[*] Đang xuất báo cáo sang PDF: {pdf_path}...")
    doc.ExportAsFixedFormat(pdf_path, 17)
    print(f"[OK] Xuất PDF thành công tại: {pdf_path}")
    
    # Lưu lại file Word với các trường đã cập nhật
    doc.Save()
    print("[OK] Đã lưu cập nhật trường trong Word.")
    doc.Close()
except Exception as e:
    print(f"[ERROR] Lỗi khi xử lý Word: {e}")
finally:
    word.Quit()

print("[DONE] Hoàn tất toàn bộ quy trình cập nhật và xuất bản.")
