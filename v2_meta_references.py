# -*- coding: utf-8 -*-
"""
Phần Mở đầu (Bìa, Cam đoan, Cảm ơn, Mục lục, Danh mục Bảng, Danh mục Hình, Tóm tắt, Từ viết tắt)
và Phần Kết thúc (Tài liệu tham khảo, Phụ lục A, B, C, D)
Báo cáo Nghiên cứu Khoa học RAG - Chuẩn mực Học thuật NCKH Học viện Công nghệ Bưu chính Viễn thông
"""
import sys

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPORT_META_AND_ABSTRACT = r"""# BỘ THÔNG TIN VÀ TRUYỀN THÔNG
## HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
### KHOA KỸ THUẬT ĐIỆN TỬ 1
***

# BÁO CÁO KẾT QUẢ NGHIÊN CỨU KHOA HỌC CỦA SINH VIÊN

## ĐỀ TÀI: NGHIÊN CỨU VÀ XÂY DỰNG HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC (RAG)
### MÃ SỐ ĐỀ TÀI: 07-SV-2026-ĐT1

---

### THÔNG TIN ĐỀ TÀI VÀ HỘI ĐỒNG NGHIÊN CỨU
- **Đơn vị chủ trì**: Khoa Kỹ thuật Điện tử 1 (Khoa KTĐT1) — Học viện Công nghệ Bưu chính Viễn thông
- **Chủ trì đề tài (Sinh viên thực hiện)**: Nguyễn Đình Hồng Phúc — Mã sinh viên: B23DCDT191 — Lớp: D23CQDT01-B
- **Giáo viên hướng dẫn khoa học**: ThS. Chu Văn Cường
- **Lãnh đạo đơn vị phê duyệt**: TS. Nguyễn Trung Hiếu — Trưởng Khoa Kỹ thuật Điện tử 1
- **Lĩnh vực khoa học công nghệ**: Trí tuệ Nhân tạo, Xử lý Ngôn ngữ Tự nhiên, Hệ thống Thông tin & Kỹ thuật Viễn thông
- **Căn cứ pháp lý**: Đề cương Nghiên cứu Khoa học Sinh viên số 07-SV-2026-ĐT1 phê duyệt ngày 03 tháng 4 năm 2026
- **Thời gian thực hiện**: Tháng 04/2026 – Tháng 11/2026
- **Sản phẩm giao nộp theo đề cương**:
  1. 03 quyển Báo cáo kết quả nghiên cứu khoa học của sinh viên
  2. Mã nguồn phần mềm của hệ thống RAG hoạt động hoàn chỉnh trên môi trường Linux và Windows
  3. Tài liệu hướng dẫn cụ thể các bước cài đặt và vận hành hệ thống RAG (Phụ lục C)
- **Hệ thống tham chiếu thực nghiệm**: Nền tảng Sunflower RAG Platform
- **Địa điểm & Thời gian hoàn thành**: Hà Nội, Tháng 11 năm 2026

---

### LỜI CAM ĐOAN

Tôi xin cam đoan báo cáo nghiên cứu khoa học *"Nghiên cứu và xây dựng hệ thống trí tuệ nhân tạo có tri thức (RAG)"* là công trình nghiên cứu khoa học độc lập của bản thân, được thực hiện dưới sự hướng dẫn khoa học tận tình của ThS. Chu Văn Cường và sự tạo điều kiện của Khoa Kỹ thuật Điện tử 1, Học viện Công nghệ Bưu chính Viễn thông.

Toàn bộ các số liệu thực nghiệm, kết quả đo lường định lượng và mã nguồn trình bày trong báo cáo là trung thực, khách quan và được thu thập trực tiếp từ các thử nghiệm có thể tái lập trên ngữ liệu khoa học thực tế. Các kết quả nghiên cứu, khảo cứu y văn và trích dẫn lý thuyết từ các tác giả khác trong và ngoài nước đều được ghi chú xuất xứ và liệt kê tường minh trong danh mục Tài liệu tham khảo theo đúng chuẩn mực học thuật quốc tế.

*Hà Nội, ngày 10 tháng 11 năm 2026*  
**Sinh viên thực hiện đề tài**  
*Nguyễn Đình Hồng Phúc*

---

### LỜI CẢM ƠN

Để hoàn thành công trình nghiên cứu khoa học này, tôi xin bày tỏ lòng biết ơn chân thành và sâu sắc nhất tới **ThS. Chu Văn Cường** — Giảng viên hướng dẫn khoa học. Thầy đã dành nhiều thời gian định hướng học thuật, chỉ dẫn phương pháp luận nghiên cứu chặt chẽ và tận tình động viên tôi trong suốt quá trình triển khai đề tài.

Tôi xin trân trọng gửi lời cảm ơn tới Ban Chủ nhiệm Khoa Kỹ thuật Điện tử 1, các thầy cô giáo trong Bộ môn và Học viện Công nghệ Bưu chính Viễn thông đã tạo môi trường học thuật thuận lợi, hỗ trợ cơ sở vật chất và phê duyệt đề cương nghiên cứu khoa học sinh viên số 07-SV-2026-ĐT1.

Cuối cùng, tôi xin chân thành cảm ơn gia đình, bạn bè và các bạn sinh viên cùng khóa D23 đã luôn đồng hành, chia sẻ và khích lệ tôi hoàn thành tốt nhiệm vụ nghiên cứu này.

---

### MỤC LỤC

- **THÔNG TIN ĐỀ TÀI VÀ HỘI ĐỒNG NGHIÊN CỨU**
- **LỜI CAM ĐOAN**
- **LỜI CẢM ƠN**
- **MỤC LỤC**
- **DANH MỤC TỪ VIẾT TẮT VÀ THUẬT NGỮ KHOA HỌC**
- **DANH MỤC CÁC BẢNG BIỂU**
- **DANH MỤC CÁC HÌNH VẼ VÀ SƠ ĐỒ**
- **TÓM TẮT NGHIÊN CỨU (TIẾNG VIỆT & ENGLISH ABSTRACT)**
- **CHƯƠNG 1: ĐẶT VẤN ĐỀ**
  - 1.1. Bối cảnh và tính cấp thiết của đề tài
  - 1.2. Khoảng trống nghiên cứu
  - 1.3. Mục tiêu nghiên cứu
  - 1.4. Câu hỏi nghiên cứu
  - 1.5. Phạm vi và đối tượng nghiên cứu
  - 1.6. Cấu trúc báo cáo và ánh xạ đề cương
- **CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN NGHIÊN CỨU**
  - 2.1. Bản chất của Hệ thống Trí tuệ Nhân tạo có Tri thức và Chuẩn mực Đánh giá KILT
  - 2.2. Bài báo Khởi nguyên và Mô hình Hóa Toán học của RAG (Lewis et al., 2020)
  - 2.3. Khảo sát và Phân loại Tiến trình Tiến hóa của Kiến trúc RAG
  - 2.4. Kiến trúc RAG Đa phương thức và Cơ chế Truy xuất Đa vector
  - 2.5. Khung Đánh giá Hiệu năng và Tiêu chuẩn Đo lường Khoa học
  - 2.6. Các Hướng Tiếp cận Đột phá Mới: GraphRAG và Agentic RAG
  - 2.7. Phân tích So sánh Chiến lược: RAG Đối chiếu với Long-Context LLMs
- **CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU VÀ THIẾT KẾ THỰC NGHIỆM**
  - 3.1. Loại hình nghiên cứu
  - 3.2. Quy trình tổng quan tài liệu có chọn lọc theo chủ đề
  - 3.3. Thiết kế thực nghiệm
  - 3.4. Dữ liệu thực nghiệm trên 5 bài báo khoa học chuẩn
  - 3.5. Công cụ và môi trường thực nghiệm
  - 3.6. Tiêu chí đo lường định lượng
  - 3.7. Thiết kế các thực nghiệm đối sánh
- **CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM VÀ THẢO LUẬN**
  - 4.1. Kết quả Tổng quan Tài liệu có Chọn lọc theo Chủ đề
  - 4.2. Kết quả Xây dựng Đường ống RAG Thực nghiệm
  - 4.3. Kết quả Thực nghiệm Định lượng Toàn trình trên Bộ dữ liệu 40 Câu hỏi
  - 4.4. Phân tích Chi tiết Truy vấn Mẫu từ Dữ liệu Log Thực tế
  - 4.5. Phân tích Hiện tượng Trượt Hit@1 và Giới hạn của Ngưỡng Cosine
  - 4.6. Khảo sát và Đối sánh Đặc tả Kỹ thuật Bốn Hệ Quản trị CSDL Vector
  - 4.7. Thảo luận
- **CHƯƠNG 5: KẾT LUẬN, HẠN CHẾ VÀ HƯỚNG NGHIÊN CỨU TIẾP THEO**
  - 5.1. Kết luận
  - 5.2. Hạn chế của nghiên cứu
  - 5.3. Hướng nghiên cứu tiếp theo
- **TÀI LIỆU THAM KHẢO**
- **PHỤ LỤC**
  - Phụ lục A: Bộ Template Prompt Chuẩn mực cho Hệ thống RAG
  - Phụ lục B: Mã nguồn Cốt lõi của Hệ thống RAG Thực nghiệm
  - Phụ lục C: Tài liệu Hướng dẫn Cài đặt và Vận hành Hệ thống trên Linux và Windows
  - Phụ lục D: Kịch bản Đánh giá Đối chứng và Bộ 40 Câu hỏi Ground-Truth

---

### DANH MỤC TỪ VIẾT TẮT VÀ THUẬT NGỮ KHOA HỌC

| Viết tắt | Thuật ngữ Tiếng Anh đầy đủ | Định nghĩa / Ý nghĩa khoa học |
| :--- | :--- | :--- |
| **RAG** | Retrieval-Augmented Generation | Mô hình sinh ngôn ngữ được tăng cường bằng cơ chế truy xuất thông tin |
| **LLM** | Large Language Model | Mô hình ngôn ngữ lớn dựa trên kiến trúc Transformer với hàng tỷ tham số |
| **DPR** | Dense Passage Retrieval | Kỹ thuật truy xuất đoạn văn bản dày đặc sử dụng mạng nơ-ron bi-encoder |
| **MIPS** | Maximum Inner Product Search | Thuật toán tìm kiếm tích vô hướng cực đại trong không gian vector đa chiều |
| **FAISS** | Facebook AI Similarity Search | Thư viện tối ưu hóa tìm kiếm độ tương đồng vector hiệu năng cao |
| **HNSW** | Hierarchical Navigable Small World | Cấu trúc đồ thị phân tầng dùng cho tìm kiếm láng giềng gần nhất (ANN) |
| **KILT** | Knowledge Intensive Language Tasks | Bộ chuẩn đánh giá chuẩn hóa cho các tác vụ ngôn ngữ đòi hỏi tri thức |
| **AIGC** | AI-Generated Content | Nội dung được tạo ra bởi trí tuệ nhân tạo (văn bản, ảnh, mã nguồn, video) |
| **HyDE** | Hypothetical Document Embeddings | Kỹ thuật tạo văn bản giả định để cải thiện độ tương đồng vector truy xuất |
| **RAGAS** | Retrieval Augmented Generation Assessment | Bộ khung đo lường tự động chất lượng hệ thống RAG qua 4 chỉ số cốt lõi |
| **ARES** | Automated RAG Evaluation System | Hệ thống đánh giá RAG tự động dựa trên học máy và khoảng tin cậy thống kê |
| **CRAG** | Corrective Retrieval-Augmented Generation | RAG có cơ chế tự hiệu chỉnh và kích hoạt tìm kiếm ngoài khi phát hiện sai lệch |
| **BM25** | Best Matching 25 | Thuật toán xếp hạng truy xuất thông tin cổ điển dựa trên tần suất từ thưa |
| **MRR** | Mean Reciprocal Rank | Nghịch đảo thứ hạng trung bình của tài liệu đúng đầu tiên trong danh sách kết quả |
| **nDCG** | Normalized Discounted Cumulative Gain | Thước đo chất lượng xếp hạng có chiết khấu độ lợi theo vị trí |

---

### DANH MỤC CÁC BẢNG BIỂU

- Bảng 1.1: Tổng hợp các khoảng trống nghiên cứu và đóng góp của đề tài
- Bảng 1.2: Bảng đối chiếu giữa 4 Nội dung nghiên cứu của Đề cương NCKH số 07-SV-2026-ĐT1 với Cấu trúc 5 Chương của Báo cáo
- Bảng 2.1: So sánh chi tiết đặc tính kỹ thuật giữa hai loại bộ nhớ
- Bảng 2.2: So sánh kỹ thuật đa chiều giữa Long-Context LLMs và Kiến trúc RAG
- Bảng 3.1: Thống kê chi tiết các công trình khoa học trong tập ngữ liệu thực nghiệm (121 trang)
- Bảng 3.2: Ma trận thiết kế thực nghiệm đo đạc đối sánh 3x3 giữa ba chiến lược cắt đoạn và ba thuật toán truy xuất
- Bảng 3.3: Đối sánh đặc tả kỹ thuật toàn diện giữa bốn hệ quản trị cơ sở dữ liệu vector
- Bảng 3.4: Bảng đặc tả mẫu bộ câu hỏi kiểm thử thực nghiệm toàn trình (trích 8 câu hỏi đại diện)
- Bảng 4.1: Tổng hợp phân loại 15 công trình khoa học tiêu biểu theo thế hệ kiến trúc RAG
- Bảng 4.2: Thống kê định lượng quá trình trích xuất và phân đoạn tập dữ liệu khoa học
- Bảng 4.3: Kết quả thực nghiệm đối sánh định lượng toàn trình trên bộ dữ liệu 40 câu hỏi kiểm thử
- Bảng 4.4: Dữ liệu thực nghiệm chi tiết cho ba câu hỏi đại diện (trích xuất trực tiếp từ log hệ thống)
- Bảng 4.5: So sánh toàn diện đặc tính kỹ thuật của bốn hệ quản trị cơ sở dữ liệu vector
- Bảng 4.6: Bảng đối chiếu kết quả nghiên cứu với các công bố khoa học tiền đề

---

### DANH MỤC CÁC HÌNH VẼ VÀ SƠ ĐỒ

- Hình 1.1: Sơ đồ so sánh cơ chế vận hành giữa mô hình ngôn ngữ thuần tham số và kiến trúc RAG
- Hình 1.2: Sơ đồ xác định phạm vi nghiên cứu trọng tâm và các giới hạn loại trừ
- Hình 1.3: Cấu trúc năm chương và luồng triển khai của đề tài nghiên cứu
- Hình 2.1: Sơ đồ phân tách bộ nhớ trong hệ thống trí tuệ nhân tạo có tri thức
- Hình 2.2: Sơ đồ kiến trúc RAG khởi nguyên của Lewis et al. (NeurIPS 2020)
- Hình 2.3: Sơ đồ tiến trình tiến hóa của các thế hệ kiến trúc RAG
- Hình 2.4: Sơ đồ quy trình hệ thống hỏi đáp RAG hai giai đoạn: Nạp dữ liệu và Truy vấn trực tiếp
- Hình 2.5: Sơ đồ kiến trúc Advanced RAG toàn diện ba tầng
- Hình 2.6: Kiến trúc RAG Đa phương thức và cơ chế Truy xuất Đa vector cho dữ liệu bán cấu trúc
- Hình 2.7: Sơ đồ bốn trụ cột đo lường đánh giá của khung RAGAS
- Hình 2.8: Sơ đồ quy trình kết hợp GraphRAG giữa đồ thị tri thức và vector
- Hình 2.9: Sơ đồ chu trình tự phản chiếu trong kiến trúc Self-RAG
- Hình 3.1: Sơ đồ luồng quy trình tổng quan tài liệu có chọn lọc và lựa chọn ngữ liệu thực nghiệm
- Hình 3.2: Quy trình năm bước của đường ống thực nghiệm RAG
- Hình 4.1: Sơ đồ kiến trúc cộng sinh giữa RAG và Long-Context LLM
- Hình 5.1: Sơ đồ lộ trình các định hướng nghiên cứu và phát triển tiếp theo của đề tài

---

### TÓM TẮT NGHIÊN CỨU

#### Tóm tắt tiếng Việt
Sự phát triển của các Mô hình Ngôn ngữ Lớn (LLM) mở ra bước đột phá cho trí tuệ nhân tạo tạo sinh, nhưng cũng bộc lộ những ranh giới nội tại của bộ nhớ tham số: hiện tượng ảo giác tri thức, sự lạc hậu dữ liệu do điểm dừng huấn luyện, và rào cản tiếp cận kho tài liệu nội bộ bảo mật. Nhằm khắc phục các hạn chế này, kiến trúc Sinh Tăng cường Truy xuất (RAG) được đề xuất như một bước chuyển dịch mô hình căn bản, kết hợp năng lực suy luận của mô hình ngôn ngữ với kho tri thức cập nhật động của bộ nhớ phi tham số bên ngoài.

Báo cáo nghiên cứu khoa học này cung cấp khảo cứu có hệ thống về hệ thống AI có tri thức và các thế hệ kiến trúc RAG, đồng thời hiện thực hóa thực nghiệm một đường ống truy xuất vector ngữ nghĩa cục bộ hoàn chỉnh theo cấu trúc năm chương chuẩn mực: (1) Đặt vấn đề, phân tích khoảng trống và xác lập bốn câu hỏi nghiên cứu; (2) Cơ sở lý thuyết, mô hình hóa xác suất biên của Lewis et al. (2020) và phân loại ba thế hệ RAG: Naive RAG, Advanced RAG, Modular RAG cùng RAG Đa phương thức; (3) Phương pháp nghiên cứu kết hợp tổng quan tài liệu có chọn lọc theo chủ đề và thiết kế thực nghiệm đường ống; (4) Kết quả thực nghiệm đối chứng trên ngữ liệu 5 bài báo khoa học chuẩn (121 trang PDF, 398 đoạn trích) với bộ 40 câu hỏi truy vấn có gán nhãn ground-truth, đo lường các chỉ số Hit@k, MRR@k, nDCG@k và độ trễ trên CPU Intel Core i7-7700HQ; (5) Kết luận, đối chiếu mục tiêu đề cương NCKH số 07-SV-2026-ĐT1, chỉ rõ các hạn chế và đề xuất lộ trình phát triển tiếp theo. Kết quả thực nghiệm khẳng định chiến lược phân đoạn trượt có vùng gối đầu kết hợp mô hình BGE-small-en-v1.5 đạt Hit@5 = 95.0% và nDCG@5 = 0.810; đồng thời hiện tượng tài liệu khảo sát thứ cấp vượt hạng tài liệu gốc phản ánh rõ ràng sự cần thiết của các tầng xử lý nâng cao.

*Từ khóa*: Retrieval-Augmented Generation, RAG, Hệ thống Trí tuệ Nhân tạo có Tri thức, Mô hình Ngôn ngữ Lớn, Vector Database, ChromaDB, FastEmbed, Hit@k, MRR, nDCG.

---

#### English Abstract
The rapid emergence of Large Language Models (LLMs) has revolutionized generative artificial intelligence, yet reliance solely on parametric memory introduces persistent challenges: factual hallucinations, knowledge obsolescence, and inaccessibility to private, domain-specific documents. Retrieval-Augmented Generation (RAG) addresses these bottlenecks by synergizing the neural reasoning capacity of LLMs with dynamic, verifiable external non-parametric knowledge stores.

This scientific research report presents a systematic investigation of Knowledge-Intensive AI Systems and RAG architectures alongside an end-to-end local empirical pipeline structured into five standard academic chapters: (1) Problem statement, research gap identification, and formulation of four core research questions; (2) Theoretical foundations, mathematical marginal probability formulations of Lewis et al. (2020), and classification across three RAG generations (Naive, Advanced, Modular) and Multimodal RAG; (3) Methodology combining selective narrative literature review and experimental pipeline design; (4) Controlled empirical evaluation on a benchmark corpus of five seminal papers (121 pages, 398 chunks) using 40 ground-truth academic queries, reporting Hit@k, MRR@k, nDCG@k, and inference latency on an Intel Core i7-7700HQ CPU; (5) Conclusions, validation against research proposal 07-SV-2026-ĐT1, disclosure of limitations, and future roadmaps. Empirical findings demonstrate that sliding window chunking with overlap paired with BGE-small-en-v1.5 achieves Hit@5 = 95.0% and nDCG@5 = 0.810, while source attribution nuances underscore the critical need for advanced post-retrieval reranking.

*Keywords*: Retrieval-Augmented Generation, RAG, Knowledge-Intensive AI, Large Language Models, Vector Database, ChromaDB, FastEmbed, Hit@k, MRR, nDCG.

---
"""

REPORT_REFERENCES_AND_APPENDICES = r"""---

## TÀI LIỆU THAM KHẢO

1. **Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W. T., Rocktäschel, T., Riedel, S., & Kiela, D.** (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. Advances in Neural Information Processing Systems (NeurIPS 2020), 33, 9459-9474. arXiv:2005.11401.
2. **Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., & Yih, W. T.** (2020). *Dense Passage Retrieval for Open-Domain Question Answering*. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020), pp. 6769-6781.
3. **Petroni, F., Piktus, A., Fan, A., Lewis, P., Yazdani, M., De Cao, N., Thorne, J., Jernite, Y., Karpukhin, V., Maillard, J., Plachouras, V., Rocktäschel, T., & Riedel, S.** (2021). *KILT: a Benchmark for Knowledge Intensive Language Tasks*. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT 2021), pp. 2523-2544.
4. **Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I.** (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 5998-6008.
5. **Gao, L., Ma, X., Lin, J., & Callan, J.** (2023a). *Precise Zero-Shot Dense Retrieval without Relevance Labels*. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023), pp. 1762-1777.
6. **Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, M., & Wang, H.** (2023b). *Retrieval-Augmented Generation for Large Language Models: A Survey*. arXiv preprint arXiv:2312.10997.
7. **Zhao, P., Zhang, H., Yu, Q., Wang, Z., Geng, Y., Fu, F., Yang, L., Zhang, W., Jiang, J., & Cui, B.** (2024). *Retrieval-Augmented Generation for AI-Generated Content: A Survey*. arXiv preprint arXiv:2402.19473.
8. **Huang, Y., & Huang, J.** (2024). *A Survey on Retrieval-Augmented Text Generation for Large Language Models*. arXiv preprint arXiv:2404.10981.
9. **Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P.** (2024). *Lost in the Middle: How Language Models Use Long Contexts*. Transactions of the Association for Computational Linguistics (TACL), 12, 157-173.
10. **Es, S., James, J., Espinosa-Anke, L., & Schockaert, S.** (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation*. arXiv preprint arXiv:2309.15217.
11. **Saad-Falcon, J., Khattab, O., Potts, C., & Zaharia, M.** (2024). *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems*. In Proceedings of NAACL 2024.
12. **Chen, J., Lin, H., Han, X., & Sun, L.** (2024). *Benchmarking Large Language Models in Retrieval-Augmented Generation*. In Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2024).
13. **Asai, A., Wu, Z., Wang, Y., Sil, A., & Hajishirzi, H.** (2024). *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*. In Proceedings of the International Conference on Learning Representations (ICLR 2024).
14. **Yan, S. Q., Gu, J. C., Zhu, Y., & Ling, Z. H.** (2024). *Corrective Retrieval Augmented Generation (CRAG)*. arXiv preprint arXiv:2401.15884.
15. **Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, J., Truitt, S., & Larson, J.** (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. Microsoft Research Technical Report.
16. **Longpre, S., Peris, C., Turner, A., Ravichander, A., Gaur, N., Murtadha, A., Mousavi, S. A., Wang, F. S., & Lu, Z.** (2021). *Entity-Based Knowledge Conflicts in Question Answering: An Empirical Study*. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP 2021), pp. 3701-3714.
17. **OpenAI.** (2023). *GPT-4 Technical Report*. arXiv preprint arXiv:2303.08774.
18. **Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A., et al.** (2023). *PaLM: Scaling Language Modeling with Pathways*. Journal of Machine Learning Research (JMLR), 24(240), 1-113.
19. **Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M. A., et al.** (2023). *LLaMA: Open and Efficient Foundation Language Models*. arXiv preprint arXiv:2302.13971.
20. **Gemini Team, Google.** (2023). *Gemini: A Family of Highly Capable Multimodal Models*. arXiv preprint arXiv:2312.11805.
21. **Borgeaud, S., Mensch, A., Hoffmann, J., Cai, T., Rutherford, E., Millican, K., et al.** (2022). *Improving Language Models by Retrieving from Trillions of Tokens (RETRO)*. In Proceedings of the 39th International Conference on Machine Learning (ICML 2022), pp. 2206-2240.
22. **Izacard, G., & Grave, E.** (2021). *Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering (Fusion-in-Decoder)*. In Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2021), pp. 874-880.
23. **Muennighoff, N., Tazi, N., Magne, L., & Reimers, N.** (2023). *MTEB: Massive Text Embedding Benchmark*. In Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2023), pp. 2014-2037.
24. **Xiao, S., Liu, Z., Zhang, P., & Muennighoff, N.** (2023). *C-Pack: Packaged Resources to Advance General Chinese Embedding*. arXiv preprint arXiv:2309.07597.
25. **Li, T., Zhang, G., Do, Q. D., Peng, B., & Yu, D.** (2024). *Retrieval Meets Long Context: Finding the Sweet Spot for Large Language Models*. arXiv preprint arXiv:2410.02660.
26. **Xu, P., Ping, W., Wu, X., McAfee, L., Shen, C., Bakhtin, A., et al.** (2023). *Retrieval Meets Long-Context Large Language Models*. arXiv preprint arXiv:2310.03025.

---

## PHỤ LỤC A: BỘ TEMPLATE PROMPT CHUẨN MỰC CHO HỆ THỐNG RAG

### A.1. Prompt Truy xuất và Tổng hợp Tri thức có Dẫn nguồn
```text
Bạn là một chuyên gia nghiên cứu khoa học chuyên sâu về Trí tuệ Nhân tạo và Hệ thống RAG.
Nhiệm vụ của bạn là trả lời câu hỏi của người dùng CHỈ DỰA TRÊN các đoạn văn bản ngữ cảnh được cung cấp dưới đây.

[CÁC NGUYÊN TẮC BẮT BUỘC]:
1. Không tự ý bổ sung các thông tin ngoài đời thực nếu không có trong ngữ cảnh nhằm phòng tránh hiện tượng ảo giác.
2. Với mỗi khẳng định hoặc số liệu khoa học đưa ra, bạn PHẢI trích dẫn rõ nguồn theo định dạng: [Tên tài liệu, Trang X].
3. Nếu các đoạn tài liệu cung cấp không chứa đủ thông tin để trả lời câu hỏi, bạn phải trả lời thành thật: "Dựa trên các tài liệu được cung cấp, không có đủ dữ kiện để khẳng định vấn đề này", không suy đoán ngoài dữ kiện được cấp.

[NGỮ CẢNH TRUY XUẤT ĐƯỢC]:
{context}

[CÂU HỎI CỦA NGƯỜI DÙNG]:
{question}

CÂU TRẢ LỜI CỦA BẠN (KÈM TRÍCH DẪN NGUỒN):
```

### A.2. Prompt Tự phản chiếu Đánh giá Độ trung thực RAGAS Faithfulness Evaluator
```text
Bạn là một thẩm định viên khoa học độc lập. Nhiệm vụ của bạn là kiểm tra xem CÂU TRẢ LỜI có được hỗ trợ hoàn toàn bởi NGỮ CẢNH hay không.

[NGỮ CẢNH CUNG CẤP]:
{context}

[CÂU HỎI]:
{question}

[CÂU TRẢ LỜI CẦN ĐÁNH GIÁ]:
{answer}

Hãy thực hiện phân tích theo các bước:
Bước 1: Phân rã CÂU TRẢ LỜI thành danh sách các khẳng định dữ kiện đơn lẻ (claims).
Bước 2: Với từng khẳng định, đối chiếu xem khẳng định đó có thể được suy ra một cách trực tiếp từ NGỮ CẢNH hay không (ĐÚNG / SAI).
Bước 3: Tính toán chỉ số Faithfulness Score = (Số khẳng định ĐÚNG) / (Tổng số khẳng định).

ĐỊNH DẠNG ĐẦU RA JSON:
{
  "claims": [
    {"statement": "Khẳng định 1", "supported": true, "citation_excerpt": "Trích dẫn chứng minh"},
    {"statement": "Khẳng định 2", "supported": false, "citation_excerpt": "Không tìm thấy trong ngữ cảnh"}
  ],
  "faithfulness_score": 0.5
}
```

---

## PHỤ LỤC B: MÃ NGUỒN CỐT LÕI CỦA HỆ THỐNG RAG THỰC NGHIỆM

### B.1. Mã nguồn Trích xuất và Lập chỉ mục Vector (`build_rag_db.py`)
```python
# -*- coding: utf-8 -*-
import os
import glob
import re
import fitz  # PyMuPDF
import chromadb
from fastembed import TextEmbedding

def extract_chunks_continuous(pdf_path, chunk_words=250, overlap_words=50):
    doc = fitz.open(pdf_path)
    file_name = os.path.basename(pdf_path)
    tokens_with_pages = []
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        text = page.get_text("text").strip()
        if not text:
            continue
        text = re.sub(r'\s+', ' ', text)
        words = text.split()
        for w in words:
            tokens_with_pages.append((w, page_idx + 1))
    doc.close()
    
    chunks = []
    i = 0
    chunk_num = 0
    step = chunk_words - overlap_words
    total_tokens = len(tokens_with_pages)
    while i < total_tokens:
        slice_tokens = tokens_with_pages[i : i + chunk_words]
        chunk_text = " ".join([w for w, _ in slice_tokens])
        pages_set = sorted(list(set([p for _, p in slice_tokens])))
        page_str = f"{pages_set[0]}-{pages_set[-1]}" if len(pages_set) > 1 else str(pages_set[0])
        chunk_id = f"{file_name}_c{chunk_num:04d}_p{page_str}"
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "file_name": file_name,
            "pages": page_str,
            "word_count": len(slice_tokens)
        })
        chunk_num += 1
        i += step
        if i >= total_tokens:
            break
    return chunks

def build_vector_store(pdf_dir="papers", persist_dir="./chroma_db_papers", model_name="BAAI/bge-small-en-v1.5"):
    embed_model = TextEmbedding(model_name=model_name)
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name="nckh_rag_papers", metadata={"hnsw:space": "cosine"})
    
    pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))
    all_chunks = []
    for pdf_path in pdf_files:
        all_chunks.extend(extract_chunks_continuous(pdf_path, chunk_words=250, overlap_words=50))
        
    batch_size = 16
    for idx in range(0, len(all_chunks), batch_size):
        batch = all_chunks[idx : idx + batch_size]
        texts = [item["text"] for item in batch]
        ids = [item["chunk_id"] for item in batch]
        metadatas = [{"file_name": item["file_name"], "pages": item["pages"], "word_count": item["word_count"]} for item in batch]
        embeddings = [emb.tolist() for emb in embed_model.embed(texts, batch_size=batch_size)]
        collection.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)
    print(f"[OK] Đã lập chỉ mục {len(all_chunks)} chunks vào ChromaDB.")

if __name__ == "__main__":
    build_vector_store()
```

### B.2. Mã nguồn Module Truy xuất Ngữ nghĩa (`query_rag.py`)
```python
# -*- coding: utf-8 -*-
import sys
import chromadb
from fastembed import TextEmbedding

class PaperRAGRetriever:
    def __init__(self, persist_dir="./chroma_db_papers", model_name="BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.embed_model = TextEmbedding(model_name=model_name)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_collection(name="nckh_rag_papers")

    def search(self, query: str, top_k: int = 5):
        if "bge" in self.model_name.lower():
            formatted_query = f"Represent this sentence for searching relevant passages: {query}"
        else:
            formatted_query = query
            
        query_embedding = list(self.embed_model.embed([formatted_query]))[0].tolist()
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        
        hits = []
        if results and "ids" in results and len(results["ids"]) > 0:
            for i in range(len(results["ids"][0])):
                distance = results["distances"][0][i]
                hits.append({
                    "id": results["ids"][0][i],
                    "score": 1.0 - distance,
                    "metadata": results["metadatas"][0][i],
                    "text": results["documents"][0][i]
                })
        return hits

if __name__ == "__main__":
    retriever = PaperRAGRetriever()
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is the mathematical formulation of the marginal probability for RAG-Sequence model?"
    print(f"=== ĐẶT CÂU HỎI TRUY VẤN: {q} ===")
    hits = retriever.search(q, top_k=5)
    for idx, hit in enumerate(hits):
        pages = hit['metadata'].get('pages', hit['metadata'].get('page', 'N/A'))
        print(f"\n--- [Hạng {idx+1}] Điểm tương đồng: {hit['score']:.4f} | Nguồn: {hit['metadata']['file_name']} (Trang {pages}) ---")
        print(hit['text'][:300] + "...")
```

---

## PHỤ LỤC C: TÀI LIỆU HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH HỆ THỐNG RAG TRÊN MÔI TRƯỜNG LINUX VÀ WINDOWS

*(Đáp ứng yêu cầu sản phẩm Dạng III theo Đề cương NCKH số 07-SV-2026-ĐT1)*

### C.1. Yêu cầu hệ thống phần cứng và phần mềm
- **Hệ điều hành**:
  - Linux: Ubuntu 22.04 LTS / 24.04 LTS, Debian 12 (Đạt chuẩn yêu cầu đề cương)
  - Windows: Windows 10 / Windows 11 64-bit
- **Phần cứng kiểm thử**:
  - Vi xử lý: Intel Core i7-7700HQ @ 2.80GHz (4 lõi / 8 luồng, tập lệnh AVX2)
  - Bộ nhớ RAM: 16 GB DDR4
  - Ổ đĩa: Tối thiểu 5 GB dung lượng trống
- **Môi trường thực thi**: Python phiên bản 3.10 hoặc 3.11

### C.2. Các bước cài đặt trên môi trường Linux (Ubuntu / Debian)

#### Bước 1: Cập nhật hệ thống và cài đặt Python 3.11
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip git build-essential
```

#### Bước 2: Thiết lập thư mục làm việc và môi trường ảo
```bash
git clone https://github.com/nckh-ptit/rag-knowledge-system.git
cd rag-knowledge-system

python3.11 -m venv venv
source venv/bin/activate
```

#### Bước 3: Cài đặt các thư viện phụ thuộc (`requirements.txt`)
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Bước 4: Khởi chạy quá trình lập chỉ mục vector
```bash
python3 build_rag_db.py
```

#### Bước 5: Thực thi truy vấn thử nghiệm
```bash
python3 query_rag.py "What is the mathematical formulation of the marginal probability for RAG-Sequence model?"
```

### C.3. Các bước cài đặt trên môi trường Windows

#### Bước 1: Khởi tạo môi trường ảo trên PowerShell
```powershell
Set-Location -Path "C:\project\NCKH\RAG"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Bước 2: Cài đặt thư viện phụ thuộc
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### Bước 3: Vận hành hệ thống
```powershell
python build_rag_db.py
python query_rag.py
```

---

## PHỤ LỤC D: KỊCH BẢN ĐÁNH GIÁ ĐỐI CHỨNG VÀ BỘ 40 CÂU HỎI GROUND-TRUTH

Mã nguồn thực nghiệm đối chứng toàn diện được đóng gói hoàn chỉnh trong tệp kịch bản `experiment_benchmark.py`. Kịch bản thực hiện nạp toàn bộ 121 trang văn bản từ 5 bài báo khoa học, phân đoạn theo 3 cấu hình (Fixed-size 250w, Sliding Window 250w/50ov, Recursive Structure-aware), tính toán chỉ số cho 3 phương pháp (BM25, all-MiniLM-L6-v2, BAAI/bge-small-en-v1.5) và xuất kết quả đo lường định lượng ra tệp `benchmark_results.json`.

Lệnh thực thi chạy lại toàn bộ thực nghiệm:
```bash
python experiment_benchmark.py
```
"""
