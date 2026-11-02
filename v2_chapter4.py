# -*- coding: utf-8 -*-
"""
Chương 4: Kết quả và Thảo luận
Báo cáo Nghiên cứu Khoa học: Hệ thống Trí tuệ Nhân tạo có Tri thức và Kiến trúc RAG
"""
import sys

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from v2_discussion_conclusion import DISCUSSION_SECTION

CHAPTER_4_BASE = r"""## CHƯƠNG 4: KẾT QUẢ VÀ THẢO LUẬN

Chương này trình bày toàn bộ các kết quả thu được từ hai trụ cột nghiên cứu: kết quả tổng quan tài liệu có chọn lọc theo chủ đề và kết quả thực nghiệm định lượng trên đường ống RAG thực tế xây dựng trên tập ngữ liệu 121 trang tài liệu khoa học chuẩn mực. Tiếp đó, chương tiến hành phân tích ma trận đối sánh thực nghiệm giữa ba chiến lược cắt đoạn và ba thuật toán truy xuất thông tin trên bộ 40 câu hỏi kiểm thử chân lý thực tế, khảo sát đặc tả kỹ thuật các hệ quản trị cơ sở dữ liệu vector, trước khi đi vào phần thảo luận chuyên sâu nhằm giải đáp toàn diện bốn câu hỏi nghiên cứu cốt lõi của đề tài.

---

### 4.1. Kết quả Tổng quan Tài liệu có Chọn lọc theo Chủ đề

Quá trình sàng lọc theo quy trình bốn giai đoạn có định hướng hệ thống (đã trình bày tại Chương 3) từ 280 tài liệu ban đầu đã chọn lọc được 15 công trình khoa học tiêu biểu nhất định hình sự phát triển của kiến trúc RAG từ năm 2020 đến 2024.

*Bảng 4.1: Tổng hợp phân loại 15 công trình khoa học tiêu biểu theo thế hệ kiến trúc RAG*

| STT | Công trình nghiên cứu | Năm | Nơi công bố | Phân loại thế hệ RAG | Đóng góp khoa học cốt lõi |
| :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | Lewis et al. | 2020 | NeurIPS 2020 | Khởi nguyên / Naive RAG | Khởi xướng RAG, mô hình hóa toán học RAG-Sequence và RAG-Token |
| 2 | Karpukhin et al. | 2020 | EMNLP 2020 | Nền tảng truy xuất | Đề xuất Dense Passage Retrieval (DPR) với kiến trúc Bi-encoder |
| 3 | Petroni et al. | 2021 | NAACL 2021 | Chuẩn mực đánh giá | Xây dựng KILT Benchmark hợp nhất và tiêu chuẩn Provenance |
| 4 | Gao et al. (HyDE) | 2022 | ACL 2023 | Advanced RAG | Kỹ thuật sinh văn bản giả định nâng cao độ nhạy so khớp vector |
| 5 | Liu et al. | 2023 | TACL 2024 | Phân tích điểm nghẽn | Khám phá hiện tượng suy giảm chú ý Lost in the Middle của LLM |
| 6 | Gao et al. (Survey) | 2023 | arXiv:2312.10997 | Khảo sát toàn diện | Hệ thống hóa phân loại ba thế hệ Naive, Advanced và Modular RAG |
| 7 | Es et al. (RAGAS) | 2023 | arXiv:2309.15217 | Khung đo lường | Bộ khung 4 chỉ số tự động: Faithfulness, Relevance, Precision, Recall |
| 8 | Asai et al. (Self-RAG) | 2023 | ICLR 2024 | Modular RAG | Cơ chế tự phản chiếu thích ứng qua 4 loại Reflection Tokens |
| 9 | Yan et al. (CRAG) | 2024 | arXiv:2401.15884 | Modular RAG | Bộ đánh giá độ tin cậy và tự kích hoạt tìm kiếm internet thay thế |
| 10 | Saad-Falcon et al. (ARES)| 2024 | NAACL 2024 | Khung đo lường | Đánh giá tự động với khoảng tin cậy thống kê và mô hình DeBERTa |
| 11 | Chen et al. (RGB) | 2024 | AAAI 2024 | Khung đo lường | Benchmark kiểm thử 4 kịch bản kháng ứng suất trong RAG |
| 12 | Zhao et al. | 2024 | arXiv:2402.19473 | Multimodal RAG | Khảo sát RAG cho AIGC đa phương thức với 4 tầng tăng cường |
| 13 | Huang và Huang | 2024 | arXiv:2404.10981 | Khảo sát chuyên sâu | Phân loại toàn diện các kỹ thuật tăng cường văn bản cho LLM |
| 14 | Edge et al. (GraphRAG) | 2024 | arXiv:2404.16130 | Đột phá thế hệ mới | Kết hợp Đồ thị Tri thức và phân cụm Leiden cho tóm tắt toàn cục |
| 15 | Longpre et al. | 2021 | EMNLP 2021 | Phân tích điểm nghẽn | Nghiên cứu xung đột giữa tri thức nội tại LLM và tài liệu truy xuất |

*Các phát hiện học thuật chính từ tổng quan*:
1. **Sự chuyển dịch từ tĩnh sang động**: Kiến trúc RAG chuyển biến từ đường ống một chiều cố định (Retrieve-and-Read) sang các kiến trúc lặp, đệ quy có khả năng tự đánh giá và thích ứng theo ngữ cảnh (Self-RAG, CRAG).
2. **Xu hướng phân tầng tối ưu hóa**: Đa số các hệ thống triển khai thực tế hiện đại đều tích hợp các tầng tối ưu kết hợp (tìm kiếm lai Hybrid Search và Cross-Encoder Re-ranking) để nâng cao độ tin cậy dữ kiện.
3. **Mở rộng không gian ứng dụng**: RAG không còn giới hạn ở văn bản thuần túy mà đã mở rộng sang sinh mã nguồn, hình ảnh, video và đồ thị tri thức.

---

### 4.2. Kết quả Xây dựng Đường ống RAG Thực nghiệm

Kế thừa ngăn xếp công nghệ từ dự án tham chiếu `vibecoding-sunflower`, chúng tôi đã hiện thực hóa một đường ống RAG hoàn chỉnh trên nền tảng Python 3.11 với các module mã nguồn tại [`build_rag_db.py`](file:///c:/project/NCKH/RAG/build_rag_db.py) và [`query_rag.py`](file:///c:/project/NCKH/RAG/query_rag.py).

#### 4.2.1. Kết quả trích xuất và phân đoạn tập ngữ liệu khoa học
Quy trình tiền xử lý sử dụng thư viện `PyMuPDF` trên 5 bài báo khoa học hạt nhân với tổng quy mô chính xác **121 trang tài liệu**. Ba chiến lược phân đoạn văn bản được triển khai và ghi nhận số lượng đoạn trích cụ thể:

*Bảng 4.2: Thống kê định lượng quá trình trích xuất và phân đoạn tập dữ liệu khoa học*:

| STT | Tên tài liệu khoa học | Số trang thực tế | Cố định 250 từ (0ov) | Cửa sổ trượt 250 từ (50ov) | Đệ quy cấu trúc (≤250 từ) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | Lewis et al. (NeurIPS 2020) | 19 | 49 | 50 | 58 |
| 2 | Gao et al. (arXiv:2312.10997) | 21 | 63 | 79 | 75 |
| 3 | Zhao et al. (arXiv:2402.19473) | 22 | 56 | 102 | 67 |
| 4 | Huang và Huang (arXiv:2404.10981) | 37 | 93 | 103 | 111 |
| 5 | Petroni et al. (NAACL 2021) | 22 | 57 | 64 | 68 |
| **Tổng** | **5 bài báo khoa học hạt nhân** | **121** | **318 chunks** | **398 chunks** | **379 chunks** |

Mỗi đoạn văn bản đều được gắn kèm cấu trúc siêu dữ liệu tường minh gồm `file_name`, `pages`, `chunk_id`, bảo đảm khả năng truy vết nguồn gốc tri thức theo chuẩn Provenance của KILT. Việc khống chế kích thước đoạn ở mức 250 từ (tương đương khoảng 330–360 tokens) bảo đảm toàn bộ các đoạn văn bản đều nằm an toàn dưới giới hạn 512 tokens của mô hình nhúng BGE-small-en-v1.5, hạn chế rủi ro bị cắt cụt đuôi ngữ cảnh.

#### 4.2.2. Kết quả lập chỉ mục và hiệu năng trên phần cứng CPU
Thực nghiệm đo đạc thời gian lập chỉ mục được tiến hành trên môi trường phần cứng kiểm soát: Vi xử lý Intel Core i7-7700HQ @ 2.80GHz (4 nhân / 8 luồng), 16 GB DDR4 RAM, hệ điều hành Windows 11 và Ubuntu 22.04 LTS (WSL2), môi trường Python 3.11.

- **Mô hình BAAI/bge-small-en-v1.5** (384 chiều, ONNX Runtime CPU AVX2, batch_size=16):
  - Cấu hình Cửa sổ trượt (398 chunks): Tổng thời gian mã hóa và lập chỉ mục HNSW là **90.89 giây** (trung bình **228.38 ms/chunk**).
  - Cấu hình Cố định (318 chunks): Tổng thời gian mã hóa là **70.63 giây** (trung bình **222.11 ms/chunk**).
  - Cấu hình Đệ quy (379 chunks): Tổng thời gian mã hóa là **74.09 giây** (trung bình **195.49 ms/chunk**).
- **Mô hình all-MiniLM-L6-v2** (384 chiều, 6 tầng Transformer):
  - Cấu hình Cửa sổ trượt (398 chunks): Tổng thời gian mã hóa là **20.69 giây** (trung bình **51.97 ms/chunk**).
  - Cấu hình Cố định (318 chunks): Tổng thời gian mã hóa là **17.48 giây** (trung bình **54.95 ms/chunk**).
- **Thuật toán từ khóa BM25**:
  - Tách từ và xây dựng chỉ mục nghịch đảo toàn bộ 121 trang tài liệu hoàn tất trong **chưa đầy 0.1 giây** (~70–100 ms).

Kết quả cho thấy: Quá trình lập chỉ mục cho tập tài liệu chuyên khảo quy mô hơn 100 trang hoàn tất trong vòng 1.5 phút trên vi xử lý CPU thông thường mà không nhất thiết phải có hạ tầng GPU chuyên dụng.

---

### 4.3. Kết quả Thực nghiệm Định lượng Toàn trình trên Bộ dữ liệu 40 Câu hỏi

Để đánh giá khách quan năng lực của hệ thống, chúng tôi đã tiến hành đo đạc thực nghiệm toàn trình trên bộ dữ liệu gồm **40 câu hỏi kiểm thử chân lý thực tế (Ground-Truth QA)**, phân bổ đồng đều cho 5 bài báo khoa học hạt nhân (8 câu hỏi cho mỗi bài báo, bao gồm công thức toán, kiến trúc mô hình, dữ kiện thực nghiệm và chuẩn đo lường).

Cần lưu ý rằng trong thiết kế thực nghiệm này, nhãn chân lý được xác định ở **cấp độ bài báo mục tiêu** (mỗi câu hỏi có 1 bài báo hạt nhân tương ứng đóng vai trò là tài liệu nguồn gốc chính). Do đó:
- Một đoạn trích được tính là trúng đích khi và chỉ khi nó xuất phát từ bài báo mục tiêu.
- Chỉ số Recall@5 trong thiết lập này (với 1 tài liệu đích duy nhất cần tìm) có giá trị đồng nhất với Hit@5, do đó cột Recall@5 được lược bỏ để tránh trùng lặp thông tin.
- Đường cơ sở ngẫu nhiên (Random Baseline): Nếu chọn ngẫu nhiên $k$ đoạn trích từ tập 398 đoạn văn bản, xác suất trúng ngẫu nhiên ước tính đạt khoảng **~20.0%** cho Hit@1 và khoảng **~67.2%** cho Hit@5 (theo tỷ lệ số đoạn trích bình quân giữa các tài liệu).

Hệ thống đánh giá ma trận đối sánh $3 \times 3$ giữa ba chiến lược phân đoạn văn bản và ba thuật toán truy xuất thông tin với tham số $k = 5$. Toàn bộ số liệu được ghi nhận từ tệp log thực nghiệm [`benchmark_results.json`](file:///c:/project/NCKH/RAG/benchmark_results.json).

*Bảng 4.3: Kết quả thực nghiệm đối sánh định lượng toàn trình trên bộ dữ liệu 40 câu hỏi kiểm thử*:

| Chiến lược phân đoạn | Thuật toán truy xuất | Hit@1 | Hit@3 | Hit@5 | MRR@5 | nDCG@5 | Độ trễ (ms) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Cố định 250 từ** (318 chunks) | **BM25 (Từ vựng thưa)** | **0.675** (27/40) | 0.850 | 0.925 | 0.756 | 0.798 | **3.82** |
| | all-MiniLM-L6-v2 | 0.625 (25/40) | 0.875 | 0.875 | 0.729 | 0.766 | 10.35 |
| | BGE-small-en-v1.5 | 0.525 (21/40) | 0.800 | 0.900 | 0.670 | 0.727 | 42.49 |
| **Cửa sổ trượt 250w/50ov** (398 chunks) | BM25 (Từ vựng thưa) | 0.575 (23/40) | 0.850 | 0.900 | 0.699 | 0.749 | **5.33** |
| | all-MiniLM-L6-v2 | 0.575 (23/40) | 0.775 | 0.900 | 0.693 | 0.744 | 7.69 |
| | **BGE-small-en-v1.5** | **0.650** (26/40) | **0.875** | **0.950** | **0.763** | **0.810** | 40.31 |
| **Đệ quy theo cấu trúc** (379 chunks) | BM25 (Từ vựng thưa) | 0.625 (25/40) | 0.825 | 0.900 | 0.734 | 0.776 | **4.11** |
| | all-MiniLM-L6-v2 | 0.575 (23/40) | 0.850 | 0.925 | 0.700 | 0.756 | 7.44 |
| | BGE-small-en-v1.5 | 0.600 (24/40) | **0.900** | 0.925 | 0.734 | 0.783 | 37.95 |

*Phân tích khoa học đa chiều từ kết quả thực nghiệm*:

1. **Hiệu năng của mô hình BGE-small với cửa sổ trượt**: 
   Khi kết hợp với Cửa sổ trượt (250 từ / 50 từ gối đầu), mô hình BGE-small đạt **Hit@5 = 0.950 (38/40 câu hỏi)** và **nDCG@5 = 0.810**. Tuy nhiên, mức tăng Hit@1 từ 0.525 (21/40) lên 0.650 (26/40) thực chất tương ứng với **5 câu hỏi trên tổng số 40 câu** (+12.5 điểm phần trăm). Khoảng tin cậy 95% Wilson cho hai tỷ lệ này lần lượt là $[0.375, 0.671]$ và $[0.495, 0.779]$, có sự chồng lấn đáng kể. Do đó, đây là một xu hướng cải thiện quan sát được trên mẫu thực nghiệm chứ chưa thể khái quát hóa thành kết luận bất biến.
   
2. **Hiện tượng đối kháng của vùng gối đầu (Overlap)**:
   Vùng gối đầu không mang lại sự cải thiện đồng đều cho mọi thuật toán. Trong khi BGE-small tăng hiệu năng, thuật toán từ vựng BM25 lại bị suy giảm: Hit@1 giảm từ **0.675 xuống 0.575** (mất 4 câu), và nDCG@5 giảm từ 0.798 xuống 0.749. Mô hình MiniLM-L6-v2 cũng giảm Hit@1 từ 0.625 xuống 0.575. Cấu hình đạt **Hit@1 cao nhất toàn bộ bảng thực nghiệm chính là BM25 kết hợp Cắt cố định (0.675)**, cao hơn cả cấu hình BGE + Cửa sổ trượt (0.650). Điều này cho thấy với các câu hỏi học thuật chứa thuật ngữ định danh hiếm (như KILT-AC, FEVER, DPR, BART), phương pháp từ khóa thưa vẫn duy trì độ nhạy rất cao ngay cả khi ranh giới câu bị ngắt đoạn.
   
3. **Yếu tố quy mô đoạn trích (Confounder)**:
   Cần ghi nhận rằng hai chiến lược Cố định và Cửa sổ trượt không chỉ khác nhau về vùng chồng lắp, mà còn khác nhau về tổng số lượng đoạn văn bản sinh ra (**318 đoạn so với 398 đoạn**, chênh lệch 25% dung lượng chỉ mục). Việc tăng số lượng đoạn trích tạo ra mật độ điểm dữ liệu dày hơn trong không gian vector, điều này cũng có thể đóng góp một phần vào việc nâng cao chỉ số Hit@5 của BGE-small.

---

### 4.4. Phân tích Chi tiết Truy vấn Mẫu từ Dữ liệu Log Thực tế

Để minh chứng tính xác thực và khả năng truy vết nguồn gốc của kết quả thực nghiệm, Bảng 4.4 trích xuất nguyên văn dữ liệu đo đạc thực tế từ đường ống truy xuất cho ba câu hỏi đại diện trong bộ 40 câu hỏi chân lý:

*Bảng 4.4: Dữ liệu thực nghiệm chi tiết cho ba câu hỏi đại diện (trích xuất trực tiếp từ log hệ thống)*:

| Mã Q | Nội dung câu hỏi kiểm thử | Tài liệu đích chuẩn | Thứ hạng | Điểm Cosine | Tài liệu trích xuất | Dải trang | Nội dung dữ kiện cốt lõi trích xuất được |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| **Q01** | *"What is the mathematical formulation of the marginal probability for RAG-Sequence model?"* | Lewis et al. (2020) | **Hạng 1** | **0.7906** | Lewis et al. | Trang 2-3 | `distributions over text passages given a query x and (ii) a generator pθ(yi\|x, z, y1:i−1)...` |
| | | | Hạng 2 | 0.7359 | Lewis et al. | Trang 3 | `to get the seq2seq probability p(y\|x) via a top-K approximation. Concretely, the top K documents...` |
| | | | Hạng 3 | 0.7267 | Zhao et al. | Trang 2-3 | `We conduct a comprehensive review of RAG, and distill the abstractions...` |
| | | | Hạng 4 | 0.7229 | Lewis et al. | Trang 3-4 | `minimize the negative marginal log-likelihood of each target...` |
| | | | Hạng 5 | 0.7225 | Zhao et al. | Trang 6 | `Typically, the logits are combined through simple summation or models to compute...` |
| **Q04** | *"Which pretrained bi-encoder architecture and generator model are used in the original RAG paper?"* | Lewis et al. (2020) | **Hạng 1** | **0.7553** | **Zhao et al.** | **Trang 3** | `Section VI discusses current limitations... II. PRELIMINARY In this section, we provide an overview...` |
| | | | Hạng 2 | 0.7300 | Zhao et al. | Trang 1 | `survey on practical applications of RAG across different modalities and tasks...` |
| | | | Hạng 3 | 0.7217 | Zhao et al. | Trang 10-11 | `chooses to use different types of retrievers in different datasets to enhance the generator...` |
| | | | **Hạng 4** | **0.7197** | **Lewis et al.** | **Trang 2-3** | `distributions over text passages given a query x and (ii) a generator pθ(yi\|x, z, y1:i−1)...` |
| | | | Hạng 5 | 0.7180 | Zhao et al. | Trang 11 | `Re2Com [101] and EditSum [98] retrieve similar codes using BM25 and generate summary...` |
| **Q33** | *"What is the structure of the KILT benchmark and how many tasks across how many domains does it include?"* | Petroni et al. (2021) | **Hạng 1** | **0.7683** | Petroni et al. | Trang 2-3 | `The KILT benchmark consists of eleven datasets spanning five distinct tasks...` |
| | | | Hạng 2 | 0.7637 | Petroni et al. | Trang 1-2 | `Figure 1: Common KILT interface for knowledge intensive language tasks...` |
| | | | Hạng 3 | 0.7624 | Petroni et al. | Trang 3 | `award points only if systems find provenance Wikipedia pages for the output given...` |
| | | | Hạng 4 | 0.7575 | Petroni et al. | Trang 9 | `Table 5: KILT scores on the test data: BART + DPR ... RAG ...` |
| | | | Hạng 5 | 0.7536 | Petroni et al. | Trang 1 | `KILT: a Benchmark for Knowledge Intensive Language Tasks (Petroni et al.)...` |

*Phân tích nguyên nhân hiện tượng trượt Hit@1 tại câu hỏi Q04*:
- Tại câu hỏi Q04, người dùng hỏi về kiến trúc bi-encoder và generator được sử dụng trong bài báo RAG khởi nguyên của Lewis et al. Kết quả thực nghiệm cho thấy đoạn trích đạt vị trí Hạng 1 (Top-1) với điểm số Cosine **0.7553** lại xuất phát từ bài báo tổng quan của **Zhao et al. (Trang 3)**, trong khi đoạn văn bản gốc của **Lewis et al. (Trang 2-3)** xuất hiện ở vị trí Hạng 4 với điểm số **0.7197** (Hit@1 = 0.0, Hit@4 = 1.0).
- Khi mở trực tiếp nội dung các đoạn trích liên quan: Đoạn trích tại Trang 3 của Zhao et al. nằm ở phần mở đầu của Mục II (Preliminary), trong đó tác giả tóm tắt lại bài toán RAG kinh điển và giới thiệu cấu trúc các tầng tăng cường. Sự đồng xuất hiện của các từ khóa tổng quan liên quan đến bài toán RAG ban đầu trong ngữ cảnh giới thiệu bài báo đã làm tăng điểm số tương đồng cosine của đoạn trích này.
- Hiện tượng này chứng minh thực tế rằng: **Điểm tương đồng Cosine trong không gian vector dày chỉ phản ánh mức độ trùng khớp hình học giữa các biểu diễn ngữ nghĩa, không phản ánh nguồn gốc tác giả hay tính khởi nguyên của tri thức**. Đây là minh chứng rõ ràng cho thấy trong các kho tài liệu học thuật có nhiều bài báo trích dẫn lẫn nhau, hệ thống RAG cần được bổ sung bộ lọc siêu dữ liệu (Metadata Filtering) và mô hình tái xếp hạng Cross-Encoder để phân định chính xác giữa tài liệu gốc và tài liệu trích dẫn lại.

---

### 4.5. Phân tích Hiện tượng Trượt Hit@1 và Giới hạn của Ngưỡng Cosine

Phân tích sâu hơn trên toàn bộ 40 câu hỏi kiểm thử đã làm sáng tỏ hai khía cạnh học thuật quan trọng:

#### 4.5.1. Bản chất của 14 trường hợp không đạt Hit@1 ở mô hình BGE-small
Trong cấu hình Cửa sổ trượt kết hợp BGE-small, hệ thống có **26/40 câu hỏi đạt Hit@1 (65.0%)** và **14/40 câu hỏi không đạt Hit@1 (35.0%)**:
- **12 trong số 14 trường hợp trượt (chiếm 85.7%)** là sự nhầm lẫn giữa các bài báo khảo sát tổng quan với nhau (giữa Gao et al., Zhao et al. và Huang et al.). Cụ thể, các câu hỏi về *Self-RAG (Q26)*, *Corrective RAG (Q27)*, *Khung đánh giá RAGAS (Q12)*, *Truy xuất đa bước (Q14, Q25)*, hay *So sánh Long-Context (Q30)* đều được cả ba bài báo tổng quan trình bày chi tiết. Do đó, việc hệ thống truy xuất đoạn trích từ bài khảo sát này thay vì bài khảo sát kia phản ánh tính chất **mơ hồ của nhãn gán chân lý ở cấp độ bài báo tổng quan** hơn là lỗi truy xuất ngữ nghĩa sai lệch.
- **2 trường hợp còn lại (Q04, Q05)** là hiện tượng bài báo tổng quan trích dẫn lại công trình gốc của Lewis et al. và được xếp trên bài gốc như đã phân tích tại Mục 4.4.

#### 4.5.2. Sự dồn dập của phân bố điểm số Cosine và bác bỏ ngưỡng cố định $\tau = 0.75$
Thống kê điểm số Cosine của đoạn trích Hạng 1 (Top-1) trên 40 câu hỏi ghi nhận:
- Khi đoạn trích Top-1 **đúng tài liệu mục tiêu** (26 câu): Điểm số Cosine trung bình là **$0.7939 \pm 0.0486$** (dao động từ 0.7228 đến 0.8641).
- Khi đoạn trích Top-1 **không trùng tài liệu mục tiêu** (14 câu): Điểm số Cosine trung bình là **$0.7773 \pm 0.0404$** (dao động từ 0.6704 đến 0.8363).

Chênh lệch giữa điểm trung bình đúng (0.7939) và điểm trung bình sai (0.7773) chỉ là **0.0166**. Hai phân bố điểm số này gần như trùng lấn hoàn toàn trong dải từ 0.75 đến 0.85. Điều này cung cấp bằng chứng thực nghiệm rõ ràng bác bỏ việc sử dụng một ngưỡng tương đồng Cosine cố định (chẳng hạn $\tau = 0.75$) để quyết định tính tin cậy của dữ kiện, khẳng định rằng điểm số tương đồng hình học trong Bi-encoder không thể thay thế cho cơ chế kiểm chứng chéo thông tin.

---

### 4.6. Khảo sát và Đối sánh Đặc tả Kỹ thuật Bốn Hệ Quản trị CSDL Vector

Dựa trên ngăn xếp công nghệ tham chiếu từ dự án thực tế `vibecoding-sunflower`, chúng tôi tiến hành đánh giá so sánh chuyên sâu giữa bốn hệ quản trị CSDL vector hàng đầu hiện nay dựa trên đặc tả kỹ thuật và kiến trúc phần mềm:

*Bảng 4.5: So sánh toàn diện đặc tính kỹ thuật của bốn hệ quản trị cơ sở dữ liệu vector*:

| Tiêu chí so sánh | ChromaDB | Qdrant | MongoDB Vector Search (Atlas) | Milvus |
| :--- | :--- | :--- | :--- | :--- |
| **Ngôn ngữ cốt lõi** | Python / Rust (hnswlib C++) | Rust | C++ | Go / C++ |
| **Cấu trúc chỉ mục** | HNSW (đồ thị phân tầng) | HNSW tùy biến tối ưu | HNSW / IVF phân vùng | HNSW, IVF_FLAT, SCaNN, DiskANN |
| **Cơ chế lưu trữ** | SQLite cục bộ / Parquet | Bộ nhớ / Mmap bền vững | BSON Document (WiredTiger) | Phân tán Object Storage / S3 |
| **Mô hình triển khai** | Nhúng trực tiếp trong ứng dụng | Client-Server độc lập / Cụm | Cụm dịch vụ đám mây phân tán | Cụm phân tán microservices hướng mây |
| **Lọc siêu dữ liệu** | Hậu lọc / Tiền lọc cơ bản | Tiền lọc đồng thời cấp Payload | MQL Aggregation Pipeline | Biểu thức điều kiện Boolean Scalar |
| **Tối ưu hóa phần cứng** | Tốt (đa luồng CPU) | Rất tốt (SIMD AVX-512) | Tận dụng tài nguyên máy chủ | Hỗ trợ GPU, SIMD, phân tán |
| **Kịch bản tối ưu nhất** | Thử nghiệm, nghiên cứu, ứng dụng cục bộ | Doanh nghiệp tải cao, yêu cầu độ trễ | Ứng dụng Fullstack Web có sẵn MongoDB | Kho tri thức quy mô hàng tỷ vector |

*Nhận định thực tiễn*:
- **ChromaDB**: Là lựa chọn phù hợp cho nghiên cứu học thuật và thử nghiệm nhanh nhờ khả năng chạy nhúng trực tiếp không cần cấu hình cụm máy chủ hay container Docker phức tạp.
- **Qdrant**: Là lựa chọn phù hợp cho môi trường sản xuất của doanh nghiệp nhờ hiệu năng của ngôn ngữ Rust và khả năng tiền lọc siêu dữ liệu đồng thời trong quá trình duyệt đồ thị HNSW.
- **MongoDB Vector Search**: Tối ưu khi hệ thống nghiệp vụ đã có sẵn hạ tầng MongoDB Atlas trên đám mây, giúp giảm bớt chi phí đồng bộ hóa dữ liệu giữa hai hệ cơ sở dữ liệu riêng biệt.
- **Milvus**: Thích hợp cho các kho dữ liệu lớn đòi hỏi kiến trúc điều phối phân tán trên nền tảng Kubernetes.

---

"""

CHAPTER_4 = CHAPTER_4_BASE + "\n" + DISCUSSION_SECTION
