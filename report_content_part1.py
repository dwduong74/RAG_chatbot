# -*- coding: utf-8 -*-
"""
Bộ tạo nội dung học thuật cho Báo cáo Nghiên cứu Khoa học RAG
Chương 1 đến Chương 3
"""

CHAPTERS_PART_1 = r"""# BÁO CÁO NGHIÊN CỨU KHOA HỌC

## ĐỀ TÀI: NGHIÊN CỨU TOÀN DIỆN VỀ HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC VÀ KIẾN TRÚC SINH TĂNG CƯỜNG TRUY XUẤT

---

### THÔNG TIN ĐỀ TÀI VÀ NHÓM NGHIÊN CỨU
- **Lĩnh vực nghiên cứu**: Khoa học Máy tính / Xử lý Ngôn ngữ Tự nhiên / Trí tuệ Nhân tạo
- **Chuyên ngành**: Mô hình Ngôn ngữ Lớn, Kỹ thuật Tri thức & Hệ thống Truy xuất Thông tin
- **Đơn vị thực hiện**: Nhóm Nghiên cứu Khoa học Công nghệ Trí tuệ Nhân tạo
- **Hệ thống tham chiếu thực nghiệm**: Nền tảng Sunflower RAG Platform (`c:\\project\\vibecoding-sunflower`)
- **Thời gian hoàn thành**: Năm 2026

---

### TÓM TẮT NGHIÊN CỨU

#### Tóm tắt tiếng Việt
Sự phát triển đột phá của các Mô hình Ngôn ngữ Lớn như GPT-4, LLaMA, PaLM và Gemini đã mở ra một kỷ nguyên mới cho trí tuệ nhân tạo tạo sinh. Tuy nhiên, các mô hình này dựa hoàn toàn vào bộ nhớ tham số được tích lũy trong quá trình tiền huấn luyện trên các tập dữ liệu khổng lồ, dẫn đến ba khiếm khuyết mang tính bản chất: hiện tượng ảo giác thông tin, sự lạc hậu của tri thức do giới hạn điểm dừng dữ liệu, và sự bất lực trong việc tiếp cận các kho dữ liệu nội bộ, bảo mật của doanh nghiệp. Để giải quyết triệt để bài toán này, kiến trúc Sinh Tăng cường Truy xuất đã được đề xuất như một bước chuyển dịch mô hình căn bản, kết hợp sức mạnh suy luận ngôn ngữ của mạng nơ-ron với khả năng lưu trữ, cập nhật động của bộ nhớ phi tham số bên ngoài.

Bản báo cáo nghiên cứu khoa học này cung cấp một cái nhìn toàn diện, thấu đáo và có hệ thống về hệ thống trí tuệ nhân tạo có tri thức và kiến trúc RAG từ lý thuyết nền tảng đến hiện thực hóa kỹ thuật. Chúng tôi đi sâu phân tích bài báo khởi nguyên của Lewis et al. (NeurIPS 2020), giải phẫu mô hình toán học xác suất biên của hai cơ chế RAG-Sequence và RAG-Token. Tiếp đó, báo cáo khảo sát và hệ thống hóa sự tiến hóa của RAG qua ba thế hệ: Naive RAG, Advanced RAG và Modular RAG, đồng thời mở rộng sang mô hình RAG cho nội dung đa phương thức. Trên cơ sở thực nghiệm tham chiếu từ dự án thực tế `vibecoding-sunflower`, chúng tôi phân tích chi tiết quy trình xây dựng đường ống RAG hoàn chỉnh sử dụng ChromaDB, FastEmbed và mô hình nhúng BGE. Cuối cùng, báo cáo phân tích sâu sắc các khung đánh giá hiệu năng tiên tiến nhất hiện nay và thảo luận các định hướng tương lai mang tính đột phá như GraphRAG, Agentic RAG và cuộc đối đầu giữa RAG với các LLM có cửa sổ ngữ cảnh siêu dài.

*Từ khóa*: Retrieval-Augmented Generation, RAG, Hệ thống Trí tuệ Nhân tạo có Tri thức, Knowledge-Intensive NLP, Mô hình Ngôn ngữ Lớn, Vector Database, ChromaDB, FastEmbed, RAGAS, Đánh giá LLM.

---

#### English Abstract
The rapid emergence of Large Language Models (LLMs) has revolutionized generative artificial intelligence. Nevertheless, relying solely on parametric memory accumulated during pre-training imposes fundamental boundaries: persistent factual hallucinations, knowledge obsolescence caused by training cut-off dates, and an inability to access private, domain-specific enterprise knowledge bases. To fundamentally resolve these bottlenecks, Retrieval-Augmented Generation (RAG) was introduced as a foundational paradigm shift, synergizing the linguistic reasoning power of parametric neural networks with the dynamic, verifiable factual groundings of external non-parametric memory stores.

This scientific research report provides a comprehensive, systematic, and rigorous study of Knowledge-Intensive AI Systems and RAG architectures, spanning theoretical foundations to engineering implementations. We thoroughly analyze the seminal work by Lewis et al. (NeurIPS 2020), detailing the mathematical formulations of marginal probability for RAG-Sequence and RAG-Token models. We then trace the evolutionary trajectory of RAG paradigms across three generations: Naive RAG, Advanced RAG, and Modular RAG, while extending into Multimodal RAG for AI-Generated Content (AIGC). Grounded in the empirical architecture of the `vibecoding-sunflower` project, we present an end-to-end technical implementation utilizing ChromaDB, FastEmbed (ONNX runtime), and state-of-the-art embedding models. Finally, we examine standardized evaluation frameworks (RAGAS, ARES, RGB benchmarks) and critically explore emergent frontiers, including GraphRAG, Agentic RAG, and the strategic trade-offs between RAG and Long-Context LLMs.

*Keywords*: Retrieval-Augmented Generation, RAG, Knowledge-Intensive NLP, Large Language Models, Parametric vs Non-parametric Memory, Vector Database, ChromaDB, FastEmbed, RAGAS, Hallucination Mitigation.

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
| **BM25** | Best Matching 25 | Thuật toán xếp hạng truy xuất thông tin cổ điển dựa trên tần suất từ (sparse) |

---

## LỜI MỞ ĐẦU VÀ TÍNH CẤP THIẾT CỦA ĐỀ TÀI

### 1. Sự bùng nổ của Mô hình Ngôn ngữ Lớn và bài toán Tri thức
Trong thập kỷ qua, lĩnh vực Xử lý Ngôn ngữ Tự nhiên đã chứng kiến sự chuyển dịch mang tính cách mạng từ các mô hình n-gram thống kê và mô hình mạng tái hồi sang kiến trúc Transformer (Vaswani et al., 2017). Với cơ chế tự chú ý cho phép mô hình hóa các phụ thuộc ngữ cảnh dài một cách hiệu quả và khả năng song song hóa vượt trội trên các phần cứng tăng tốc, các mô hình ngôn ngữ tiền huấn luyện tự giám sát đã liên tục phá vỡ các giới hạn về quy mô tham số và năng lực tổng quát.

Khi quy mô mô hình vượt qua ngưỡng hàng chục tỷ tham số, hiện tượng "năng lực đột sinh" xuất hiện: mô hình không chỉ thể hiện khả năng hiểu và sinh ngôn ngữ tự nhiên lưu loát mà còn có khả năng suy luận logic nhiều bước, viết mã lập trình phức tạp, và giải quyết các bài toán trừu tượng chỉ thông qua chỉ dẫn mà không cần huấn luyện lại trọng số.

Tuy nhiên, đằng sau sự thành công rực rỡ đó là một nghịch lý căn bản về bản chất lưu trữ tri thức:**Mô hình Ngôn ngữ thuần túy lưu trữ toàn bộ hiểu biết về thế giới dưới dạng các giá trị trọng số liên tục phân tán trên hàng trăm lớp mạng nơ-ron.** Cách thức lưu trữ này, được gọi là**Bộ nhớ Tham số**, đã bộc lộ những điểm yếu chí tử khi đối mặt với các ứng dụng thực tế đòi hỏi độ chính xác tuyệt đối và tính cập nhật liên tục:

1.**Hiện tượng Ảo giác Tri thức**:
 Mục tiêu tối ưu hóa cơ bản của các mô hình ngôn ngữ tự hồi quy là cực đại hóa xác suất hợp lý của token kế tiếp $P(w_t | w_{<t})$ dựa trên phân phối thống kê của tập dữ liệu huấn luyện. Mô hình được thiết kế để tạo ra các chuỗi từ ngữ có vẻ "hợp lý nhất về mặt ngôn ngữ học" chứ không có bất kỳ cơ chế nào đảm bảo tính "đúng đắn về mặt dữ kiện khách quan". Khi đối mặt với các câu hỏi về thực thể hiếm, các dữ kiện chi tiết hoặc các miền tri thức phức tạp, mô hình thường tự tin đưa ra những câu trả lời sai sự thật nhưng được diễn đạt cực kỳ trôi chảy và thuyết phục. Trong các lĩnh vực quan trọng như y tế, pháp luật, tài chính hay nghiên cứu khoa học, ảo giác là mối nguy cơ nghiêm trọng không thể chấp nhận.

2.**Điểm nghẽn Thời gian và Sự Lạc hậu Tri thức**:
 Quá trình tiền huấn luyện một mô hình ngôn ngữ lớn đòi hỏi hàng triệu đô la chi phí điện toán và hàng tháng trời vận hành cụm máy chủ siêu máy tính. Do đó, tri thức lưu trữ trong trọng số mô hình bị "đóng băng" tại thời điểm hoàn tất thu thập dữ liệu. Mô hình hoàn toàn "mù thông tin" trước các sự kiện thời sự, các phát minh khoa học mới, các thay đổi chính sách pháp luật vừa ban hành hay các cập nhật giá cả thị trường hàng ngày.

3.**Rào cản Tiếp cận Tri thức Nội bộ và Dữ liệu Riêng tư**:
 Các tập dữ liệu tiền huấn luyện công khai (như Common Crawl, Wikipedia, C4) không chứa các tài liệu kinh doanh nội bộ, hồ sơ bệnh án, quy trình vận hành bảo mật hay cơ sở dữ liệu khách hàng của doanh nghiệp. Việc đưa toàn bộ dữ liệu nhạy cảm này vào quy trình Fine-tuning mô hình không chỉ tốn kém chi phí mà còn tiềm ẩn nguy cơ rò rỉ dữ liệu nghiêm trọng thông qua các cuộc tấn công trích xuất dữ liệu.

4.**Chi phí và Rủi ro khi Tái huấn luyện**:
 Mỗi khi có dữ liệu mới phát sinh, việc tái huấn luyện định kỳ là bất khả thi về mặt kinh tế. Ngay cả phương pháp vi chỉnh tham số cũng gặp phải hiện tượng "Quên thảm khốc" - khi mô hình tiếp thu tri thức mới sẽ làm suy giảm nghiêm trọng khả năng suy luận trên các tác vụ đã học trước đó.

### 2. Sự trỗi dậy của Kiến trúc RAG như một Bước Chuyển Dịch Mô Hình
Đứng trước những thách thức trên, cộng đồng khoa học nhận ra rằng:**Không nên bắt ép mô hình ngôn ngữ phải đóng vai trò là một "Bách khoa toàn thư chứa mọi dữ kiện", mà nên coi mô hình ngôn ngữ là một "Bộ não suy luận" có khả năng đọc hiểu, tổng hợp và xử lý thông tin.**

Để thực hiện triết lý này, kiến trúc**Sinh Tăng cường Truy xuất** ra đời. RAG thiết lập một sự kết hợp cộng sinh hoàn hảo giữa hai thành phần:
- Một**Hệ thống Truy xuất Thông tin** đảm nhiệm vai trò truy quét trong kho tài liệu khổng lồ để tìm ra những đoạn văn bản chứa dữ kiện chính xác và cập nhật nhất liên quan đến truy vấn của người dùng.
- Một**Mô hình Ngôn ngữ Sinh** đảm nhiệm vai trò tiếp nhận truy vấn kết hợp cùng các đoạn tài liệu vừa truy xuất được, đọc hiểu ngữ cảnh và tổng hợp thành câu trả lời hoàn chỉnh, chính xác, có căn cứ rõ ràng và có thể kiểm chứng nguồn gốc.

### 3. Mục tiêu và Bố cục Báo cáo Nghiên cứu
Bản báo cáo này được xây dựng với mục tiêu cung cấp một tài liệu nghiên cứu khoa học có chiều sâu học thuật và giá trị thực tiễn cao, đóng vai trò là cẩm nang toàn diện cho các nhà nghiên cứu, kỹ sư AI và nhà phát triển hệ thống tri thức. Báo cáo được cấu trúc thành các chương chính như sau:
- **Chương 1**: Cơ sở lý thuyết về Hệ thống AI có Tri thức và Chuẩn mực KILT.
- **Chương 2**: Bài báo khởi nguyên và Mô hình hóa toán học xác suất của RAG (Lewis et al., 2020).
- **Chương 3**: Khảo sát và Phân loại toàn diện các thế hệ kiến trúc RAG: Naive RAG, Advanced RAG, Modular RAG và Multimodal AIGC RAG.
- **Chương 4**: Thiết kế và Hiện thực hóa Hệ thống RAG thực tế (kết hợp phân tích mã nguồn và thực nghiệm trên tập 5 bài báo khoa học).
- **Chương 5**: Khung đánh giá hiệu năng và Tiêu chuẩn đo lường khoa học.
- **Chương 6**: Thách thức khoa học, Xu hướng mới và So sánh với Long-Context LLMs.
- **Kết luận và Tài liệu tham khảo**.

---

## CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VỀ HỆ THỐNG AI CÓ TRI THỨC

### 1.1. Định nghĩa Chuẩn tắc về Tác vụ Đòi hỏi Tri thức
Trong lý thuyết khoa học nhận thức và xử lý ngôn ngữ tự nhiên, các tác vụ xử lý ngôn ngữ được phân chia thành hai nhóm cơ bản:
1.**Tác vụ Dựa trên Kỹ năng Ngôn ngữ và Cấu trúc**: Ví dụ như phân tích cú pháp, nhận diện thực thể tên (NER cơ bản), dịch máy các câu giao tiếp hàng ngày, hoặc sửa lỗi chính tả. Các tác vụ này chủ yếu đòi hỏi mô hình nắm vững ngữ pháp, ngữ nghĩa và cấu trúc câu.
2.**Tác vụ Đòi hỏi Tri thức Chuyên sâu**: Được định nghĩa chính thức bởi Petroni et al. (2020) và Lewis et al. (2020) là:
 > *"Những tác vụ mà một con người thông minh, có học thức thông thường cũng không thể kỳ vọng hoàn thành chính xác nếu không được cung cấp hoặc chủ động tra cứu một kho tài liệu tri thức bên ngoài đáng tin cậy."*

Các ví dụ điển hình của Knowledge-Intensive Tasks bao gồm:
- **Hỏi đáp Miền mở**: Người dùng đặt ra câu hỏi về bất kỳ sự kiện, nhân vật lịch sử, công thức khoa học hay dữ kiện địa lý nào (ví dụ: *"Ai là người phát minh ra kính hiển vi điện tử quét và vào năm nào?"*). Hệ thống không có ngữ cảnh cung cấp sẵn mà phải tự tìm kiếm trong kho tri thức toàn cầu.
- **Kiểm chứng Sự thật**: Đánh giá xem một phát biểu bất kỳ là "Đúng", "Sai" hay "Không đủ thông tin", đồng thời phải chỉ ra chính xác bằng chứng tài liệu hỗ trợ cho kết luận đó.
- **Hội thoại Đòi hỏi Tri thức**: Các trợ lý ảo trò chuyện chuyên sâu với chuyên gia hoặc người dùng về một chủ đề học thuật hoặc nghiệp vụ phức tạp.
- **Điền khuyết Thực thể**: Xác định mối quan hệ giữa các thực thể dựa trên kho dữ liệu thực tế.

### 1.2. Lý thuyết Phân tách Bộ nhớ: Parametric Memory vs. Non-Parametric Memory
Kiến trúc của các hệ thống AI truyền thống thường gộp chung khả năng tính toán và dữ liệu vào cùng một khối tham số mạng nơ-ron. Ngược lại, kiến trúc AI có tri thức hiện đại áp dụng nguyên lý phân tách tường minh giữa hai loại bộ nhớ:

```mermaid
graph TD
    Root["HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC"] --> PM["BỘ NHỚ THAM SỐ<br/>• Trọng số mạng nơ-ron Transformer<br/>• Học qua giải thuật Lan truyền ngược<br/>• Năng lực: Cú pháp, Ngữ nghĩa và Suy luận<br/>• Chi phí cập nhật: Rất cao khi tái huấn luyện<br/>• Tính giải thích: Hộp đen nơ-ron phức tạp"]
    Root --> NPM["BỘ NHỚ PHI THAM SỐ<br/>• Cơ sở dữ liệu Vector và Chỉ mục HNSW<br/>• Kho tri thức tài liệu rời rạc như PDF và CSDL<br/>• Cập nhật động theo thời gian thực<br/>• Chi phí cập nhật: Cực thấp khi cập nhật dữ liệu<br/>• Tính giải thích: Truy vết nguồn gốc minh bạch"]
```

*Hình 1: Sơ đồ phân tách bộ nhớ trong hệ thống trí tuệ nhân tạo có tri thức*

*Bảng so sánh chi tiết hai loại bộ nhớ*:

| Đặc tính so sánh | Parametric Memory (Bộ nhớ tham số) | Non-Parametric Memory (Bộ nhớ phi tham số) |
| :--- | :--- | :--- |
|**Bản chất vật lý** | Trọng số ma trận liên tục ($W \in \mathbb{R}^{d \times d}$) | Kho vector rời rạc, bảng dữ liệu, đồ thị tri thức |
|**Cơ chế cập nhật** | Tối ưu hóa lan truyền ngược | Thêm, sửa, xóa bản ghi trong CSDL |
|**Thời gian cập nhật** | Vài giờ đến vài tháng (đòi hỏi tính toán lớn) | Thời gian thực (vài phần nghìn giây) |
|**Khả năng kiểm chứng** | Khó giải thích (Hộp đen nơ-ron) | Truy vết trực tiếp về văn bản gốc, trang sách, URL |
|**Kiểm soát quyền truy cập**| Bất khả thi (không thể che giấu một phần tham số)| Phân quyền chi tiết theo vai trò|
|**Nguy cơ lỗi** | Ảo giác, nhầm lẫn dữ kiện, tự tin thái quá | Truy xuất sai tài liệu (nhưng phát hiện được ngay) |

Sự phân tách này mang lại lợi thế chiến lược: Chúng ta có thể đóng băng hoàn toàn các tham số của mô hình ngôn ngữ lớn (tiết kiệm hàng triệu USD chi phí hạ tầng), trong khi kho dữ liệu tri thức bên ngoài có thể liên tục được mở rộng, cập nhật và làm sạch mỗi ngày.

### 1.3. Bộ chuẩn Benchmark KILT (Petroni et al., 2020)
Để đánh giá một cách công bằng và có hệ thống năng lực của các mô hình AI có tri thức, Petroni et al. (Facebook AI Research, UCL) đã công bố bộ chuẩn**KILT** tại hội nghị NAACL-HLT 2021. 

Trước khi KILT ra đời, các bài toán NLP có tri thức bị phân mảnh nghiêm trọng: mỗi bộ dữ liệu (như Natural Questions, TriviaQA, FEVER, HotpotQA) lại sử dụng một phiên bản tài liệu tham khảo khác nhau (các bản chụp Wikipedia ở các năm khác nhau, các trang web không đồng nhất), khiến cho việc so sánh năng lực thực sự của các kiến trúc mô hình trở nên bất khả thi.

KILT đã thực hiện một bước đột phá bằng cách:
1.**Hợp nhất kho tri thức chuẩn duy nhất**: Toàn bộ các tác vụ trong KILT đều được neo vào một bản chụp Wikipedia thống nhất gồm hơn**5.9 triệu bài viết** (được chia nhỏ thành hơn 35 triệu đoạn văn bản 100 từ).
2.**Quy tụ 11 bộ dữ liệu chuẩn mực thuộc 5 miền tác vụ lớn**:
 - *Fact Checking*: FEVER
 - *Open-Domain QA*: Natural Questions (NQ), TriviaQA, HotpotQA (đòi hỏi suy luận đa bước - Multi-hop), ELI5 (Explain Like I'm 5 - trả lời câu hỏi mở dài)
 - *Slot Filling*: T-REx, Zero-Shot RE
 - *Entity Linking*: AIDA CoNLL-YAGO, WNED-WIKI, WNED-CWEB
 - *Dialogue*: Wizard of Wikipedia (WoW)

### 1.4. Khái niệm Provenance và Tiêu chuẩn Thẩm định Nguồn gốc Tri thức
Đóng góp học thuật quan trọng nhất của KILT là việc thiết lập tiêu chuẩn đánh giá kép:**Độ chính xác nội dung** kết hợp với**Độ chính xác nguồn gốc**.

Trong các hệ thống học máy truyền thống, một mô hình trả lời đúng kết quả cuối cùng sẽ được điểm tối đa. Tuy nhiên, trong các hệ thống AI có tri thức, điều này là chưa đủ: mô hình có thể đoán mò đúng do may mắn hoặc do học vẹt trong tập huấn luyện. KILT đưa ra chỉ số**KILT-AC**:
$$\text{KILT-AC} = \text{Accuracy} \times \text{Provenance Success}$$

Trong đó, một dự đoán chỉ được coi là thành công trọn vẹn khi và chỉ khi:
1. Câu trả lời sinh ra khớp với nhãn thực tế.
2. Đoạn văn bản bằng chứng mà hệ thống trích dẫn phải nằm trong tập các đoạn văn bản chứng minh hợp lệ được gán nhãn bởi các chuyên gia.

Khái niệm Provenance chính là nền móng triết học cho RAG:**Một phát biểu của trí tuệ nhân tạo chỉ có giá trị khi nó có thể truy nguyên nguồn gốc về một văn bản có thẩm quyền trong thế giới thực.**

---

## CHƯƠNG 2: BÀI BÁO KHỞI NGUYÊN VÀ MÔ HÌNH HÓA TOÁN HỌC CỦA RAG (LEWIS ET AL., 2020)

### 2.1. Kiến trúc Tổng thể của Lewis et al. (NeurIPS 2020)
Tại hội nghị NeurIPS 2020, nhóm nghiên cứu tại Facebook AI Research (FAIR) do Patrick Lewis dẫn đầu đã công bố bài báo mang tính bước ngoặt: *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"*. Đây là công trình đầu tiên chính thức đặt tên và mô hình hóa toán học cho thuật ngữ**RAG**.

Kiến trúc RAG của Lewis et al. bao gồm hai khối nơ-ron chính kết nối với nhau:
1.**Bộ truy xuất nơ-ron**: Sử dụng mô hình**Dense Passage Retrieval** (Karpukhin et al., 2020). DPR sử dụng kiến trúc Bi-encoder dựa trên BERT:
 - Một bộ mã hóa truy vấn $E_Q(x)$ biến đổi câu hỏi đầu vào $x$ thành vector đặc trưng dày đặc 768 chiều.
 - Một bộ mã hóa đoạn văn $E_D(z)$ biến đổi từng đoạn văn bản $z$ trong kho dữ liệu thành vector 768 chiều.
 - Điểm số liên quan giữa câu hỏi $x$ và tài liệu $z$ được tính bằng tích vô hướng:
 $$p_\eta(z|x) \propto \exp(E_Q(x)^T E_D(z))$$
 - Việc tìm kiếm top-$k$ tài liệu có điểm số cao nhất được thực hiện bằng thuật toán MIPS thông qua thư viện FAISS trên quy mô hàng chục triệu vector với độ trễ tính bằng mili-giây.
2.**Bộ sinh chuỗi**: Sử dụng mô hình tuần tự sang tuần tự**BART-large** (Lewis et al., 2019) với 400 triệu tham số. BART tiếp nhận đầu vào là sự kết hợp nối tiếp giữa văn bản truy vấn $x$ và đoạn tài liệu truy xuất được $z$, sau đó sinh ra chuỗi token mục tiêu $y$ từng bước một.

### 2.2. Mô hình Toán học RAG-Sequence
Lewis et al. đề xuất hai cách tiếp cận khác nhau để tích hợp tài liệu truy xuất vào quá trình sinh văn bản. Cách tiếp cận thứ nhất là**RAG-Sequence**.

Trong mô hình RAG-Sequence, hệ thống giả định rằng**toàn bộ chuỗi đầu ra $y$ được điều kiện hóa trên cùng một tài liệu truy xuất $z$**. Xác suất sinh ra chuỗi $y$ được tính bằng cách lấy kỳ vọng trên tập hợp top-$k$ tài liệu có xác suất truy xuất cao nhất:

$$p_{\text{RAG-Seq}}(y|x) = \sum_{z \in \text{top-}k} p_\eta(z|x) \cdot p_\theta(y|x, z) = \sum_{z \in \text{top-}k} p_\eta(z|x) \prod_{i=1}^N p_\theta(y_i|x, z, y_{1:i-1})$$

Trong đó:
- $p_\eta(z|x)$ là xác suất tiên nghiệm truy xuất tài liệu $z$ từ bộ truy xuất DPR (với tham số $\eta$).
- $p_\theta(y_i|x, z, y_{1:i-1})$ là xác suất sinh ra token thứ $i$ của bộ sinh BART (với tham số $\theta$), có điều kiện trên câu hỏi gốc $x$, tài liệu $z$, và các token đã sinh trước đó $y_{1:i-1}$.
- $N$ là độ dài của chuỗi đầu ra $y$.

*Ý nghĩa của RAG-Sequence*: Mô hình này đặc biệt phù hợp khi câu trả lời đòi hỏi tính nhất quán cao và toàn bộ thông tin câu trả lời nằm trọn vẹn trong một đoạn văn bản duy nhất.

### 2.3. Mô hình Toán học RAG-Token
Cách tiếp cận thứ hai mang tính đột phá và linh hoạt hơn là**RAG-Token**. Trong mô hình này, việc lựa chọn tài liệu được giải phóng ở cấp độ từng token:**Mỗi token sinh ra có thể được điều kiện hóa trên một tài liệu khác nhau.**

Công thức xác suất của RAG-Token được xây dựng như sau:

$$p_{\text{RAG-Token}}(y|x) = \prod_{i=1}^N \sum_{z \in \text{top-}k} p_\eta(z|x) \cdot p_\theta(y_i|x, z, y_{1:i-1})$$

*Phân tích bản chất toán học*:
Trong RAG-Token, tại mỗi bước giải mã $i$, mô hình tính toán một phân phối xác suất hỗn hợp cho token kế tiếp bằng cách tính tổng trọng số xác suất sinh từ $k$ tài liệu khác nhau. Điều này cho phép bộ sinh:
- Lấy một phần thông tin (ví dụ: tên một địa danh) từ tài liệu $z_1$.
- Lấy một phần thông tin khác (ví dụ: mốc thời gian diễn ra sự kiện) từ tài liệu $z_2$.
- Tổng hợp thành một câu trả lời hoàn chỉnh mang tính đa nguồn.

### 2.4. Cơ chế Huấn luyện End-to-End coi Tài liệu là Biến Tiềm ẩn
Một điểm sáng tạo học thuật vượt bậc trong công trình của Lewis et al. là**phương pháp huấn luyện đầu-cuối mà không cần dữ liệu gán nhãn về việc câu hỏi nào phải đi với tài liệu nào.**

Trong thực tế, việc gán nhãn thủ công từng cặp (câu hỏi, tài liệu đúng) là vô cùng đắt đỏ. Nhóm tác giả giải quyết vấn đề này bằng cách coi tài liệu được truy xuất $z$ là một**Biến tiềm ẩn**. 

Hàm mục tiêu huấn luyện là cực tiểu hóa hàm mất mát đối số logarit âm của chuỗi đích $y$:
$$\mathcal{L}_{\text{RAG}}(\theta, \eta) = - \sum_{(x, y) \in \mathcal{D}} \log p(y|x)$$

Trong quá trình tối ưu hóa bằng thuật toán Adam, đạo hàm riêng được truyền qua cả hai khối:
- Cập nhật tham số bộ sinh $\theta$ để sinh câu trả lời đúng hơn khi có tài liệu.
- Cập nhật tham số bộ mã hóa truy vấn $\eta$ của DPR! Nếu một tài liệu $z$ giúp bộ sinh đưa ra xác suất cho $y$ cao hơn, gradient sẽ tự động điều chỉnh bộ mã hóa truy vấn để kéo vector của câu hỏi $x$ lại gần hơn với vector của tài liệu $z$ trong không gian embedding.

### 2.5. Thuật toán Giải mã: Thorough Decoding vs. Fast Decoding
Đối với RAG-Sequence, việc tìm kiếm chuỗi $y^* = \arg\max_y p(y|x)$ là một bài toán NP-khó vì nó đòi hỏi tính toán trên không gian tổ hợp của tất cả các chuỗi có thể. Lewis et al. đề xuất hai giải thuật:

1.**Thorough Decoding**:
 Chạy thuật toán Beam Search độc lập cho từng tài liệu $z \in \text{top-}k$, thu được tập hợp các giả thuyết ứng viên $\mathcal{Y}_z$. Sau đó, tập hợp các ứng viên $\mathcal{Y} = \bigcup_z \mathcal{Y}_z$ được gom lại và chấm điểm lại bằng cách tính tổng xác suất biên trên toàn bộ $k$ tài liệu. Phương pháp này cho chất lượng cực cao nhưng chi phí tính toán tỷ lệ thuận với số lượng tài liệu $k$.
2.**Fast Decoding**:
 Chỉ chạy Beam Search trên tài liệu có xác suất $p_\eta(z|x)$ cao nhất để tạo ra các chuỗi ứng viên, sau đó mới tính xấp xỉ xác suất biên. Giải thuật này giảm thiểu đáng kể thời gian đáp ứng, phù hợp cho các hệ thống ứng dụng thời gian thực.
"""

print("[*] Chapter 1-2 content prepared successfully.")
