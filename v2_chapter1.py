# -*- coding: utf-8 -*-
"""
Chương 1: Đặt vấn đề - Báo cáo Nghiên cứu Khoa học RAG
Được biên soạn chuẩn mực theo phong cách học thuật NCKH Việt Nam.
"""
import sys

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

CHAPTER_1 = r"""## CHƯƠNG 1: ĐẶT VẤN ĐỀ

### 1.1. Bối cảnh và tính cấp thiết của đề tài

#### 1.1.1. Sự bùng nổ của mô hình ngôn ngữ lớn và kiến trúc Transformer
Trong thập kỷ qua, lĩnh vực Trí tuệ Nhân tạo và Xử lý Ngôn ngữ Tự nhiên đã chứng kiến bước chuyển mình mang tính cách mạng, khởi nguồn từ sự đột phá của kiến trúc mạng Transformer (Vaswani et al., 2017). Nhờ cơ chế tự chú ý đa chỏm loại bỏ các hạn chế tính toán tuần tự của các mạng nơ-ron hồi quy truyền thống, Transformer mở đường cho việc tiền huấn luyện tự giám sát trên quy mô dữ liệu khổng lồ. Sự phát triển này thúc đẩy sự ra đời của hàng loạt mô hình ngôn ngữ lớn (LLM) tiêu biểu như GPT-4 (OpenAI, 2023), PaLM (Chowdhery et al., 2023), LLaMA (Touvron et al., 2023) và Gemini (Google, 2023). Khi quy mô tham số vượt ngưỡng hàng chục tỷ, các mô hình bộc lộ năng lực đột sinh vượt bậc: hiểu và sinh ngôn ngữ tự nhiên trôi chảy, suy luận nhiều bước theo ngữ cảnh và giải quyết các tác vụ phức tạp mà không cần cập nhật trọng số. Các mô hình ngôn ngữ lớn nhanh chóng trở thành giao diện tương tác tri thức chủ đạo trong đời sống học thuật và công nghiệp.

#### 1.1.2. Nghịch lý căn bản của bộ nhớ tham số
Tuy nhiên, đằng sau sự thành công đó là một nghịch lý căn bản: các mô hình ngôn ngữ thuần túy lưu trữ toàn bộ tri thức nhân loại dưới dạng các ma trận trọng số thực liên tục phân tán trên hàng trăm lớp mạng nơ-ron, được gọi là **bộ nhớ tham số**. Quá trình học của mô hình dựa trên hàm mục tiêu cực đại hóa xác suất hợp lý có điều kiện của chuỗi từ:

$$\mathcal{L}_{LM}(\theta) = \sum_{t=1}^{T} \log P(w_t \mid w_{<t}; \theta)$$

Trong đó $w_t$ biểu diễn token tại bước $t$, $w_{<t}$ là ngữ cảnh đứng trước, và $\theta$ là không gian tham số của mô hình.

Hàm mất mát này tối ưu hóa độ hợp lý thống kê về mặt ngôn ngữ học thay vì bảo đảm tính xác thực của dữ kiện khách quan. Khi đối mặt với các tác vụ đòi hỏi tri thức chuyên sâu (Petroni et al., 2020; Petroni et al., 2021) — nơi câu trả lời phụ thuộc chặt chẽ vào các sự kiện, số liệu hay định lý khoa học cụ thể — bộ nhớ tham số bộc lộ bốn điểm nghẽn nghiêm trọng:

1. **Hiện tượng ảo giác tri thức**: Do tối ưu hóa phân phối $P(w_t \mid w_{<t})$ nhằm đạt sự trôi chảy ngôn ngữ, mô hình hoàn toàn không có cơ chế vật lý nào bắt buộc chuỗi sinh ra phải đúng đắn về mặt dữ kiện thực tế. Khi gặp câu hỏi về thực thể hiếm hoặc nằm ngoài miền dữ liệu huấn luyện, mô hình thường tự tin bịa đặt thông tin sai lệch nhưng diễn đạt rất thuyết phục. Trong các lĩnh vực y tế, pháp lý hay nghiên cứu khoa học, ảo giác là rủi ro nguy hiểm không thể chấp nhận.

2. **Sự lạc hậu của tri thức do điểm dừng dữ liệu**: Việc tiền huấn luyện tiêu tốn hàng triệu đô la điện toán, khiến tri thức trong bộ nhớ tham số bị đóng băng tại thời điểm chốt dữ liệu. Sau mốc này, mô hình hoàn toàn mù thông tin trước các sự kiện thời sự, phát minh khoa học mới hay các sửa đổi pháp lý vừa ban hành.

3. **Rào cản tiếp cận dữ liệu bảo mật và nội bộ doanh nghiệp**: Dữ liệu tiền huấn luyện chỉ gồm dữ liệu công cộng mở. Mô hình không thể truy cập tài liệu kỹ thuật nội bộ, hồ sơ bệnh án hay cơ sở dữ liệu chuyên ngành của tổ chức. Việc đưa dữ liệu riêng tư vào mô hình công cộng tiềm ẩn nguy cơ vi phạm quyền riêng tư và rò rỉ dữ liệu qua tấn công trích xuất tham số.

4. **Hiện tượng quên thảm khốc khi tinh chỉnh tham số**: Khi thực hiện vi chỉnh mô hình trên tập dữ liệu mới, quá trình lan truyền ngược gradient thường làm suy giảm cấu trúc trọng số đã học trước đó, làm mất đi các năng lực tổng quát hóa và gây tốn kém chi phí tính toán không bền vững.

#### 1.1.3. Sự trỗi dậy của kiến trúc RAG như một bước chuyển dịch mô hình
Trước những giới hạn nội tại của bộ nhớ tham số, cộng đồng khoa học nhận thấy không nên bắt ép mô hình ngôn ngữ lớn đóng vai trò kho lưu trữ dữ kiện tĩnh, mà nên xem nó là một **bộ não suy luận** kết hợp cùng một **bộ nhớ phi tham số bên ngoài**. Nghiên cứu khởi nguyên của Lewis et al. (2020) tại NeurIPS đã chính thức đề xuất kiến trúc **Sinh Tăng cường Truy xuất** (RAG). RAG thiết lập sự kết hợp cộng sinh giữa hai thành phần:
- Mô hình ngôn ngữ đóng vai trò bộ não suy luận tham số, đọc hiểu ngữ cảnh và tổng hợp câu trả lời.
- Cơ sở dữ liệu bên ngoài đóng vai trò bộ nhớ phi tham số, lưu trữ kho tài liệu cập nhật động và cho phép truy xuất dữ kiện minh bạch.

Mô hình xác suất biên của RAG liên kết hai thành phần qua biến ẩn tài liệu $z$:

$$P(y \mid x) = \sum_{z \in \text{top-}k} P(z \mid x) \cdot P(y \mid x, z)$$

Trong đó $x$ là truy vấn đầu vào, $z$ là đoạn văn bản được truy xuất với xác suất $P(z \mid x)$, và $y$ là câu trả lời được sinh ra có căn cứ rõ ràng từ ngữ cảnh $P(y \mid x, z)$ (Gao et al., 2023).

| Tiêu chí So sánh | Mô hình Thuần Tham số | Kiến trúc RAG |
| :--- | :--- | :--- |
| **Cơ chế lưu trữ** | Toàn bộ dữ kiện nén trong ma trận trọng số $\theta$ | Tách biệt: Trọng số suy luận + Kho tài liệu ngoài |
| **Độ chính xác dữ kiện** | Dễ xuất hiện ảo giác do tối ưu $P(w_t \mid w_{<t})$ | Ràng buộc trực tiếp trên ngữ cảnh được truy xuất |
| **Khả năng cập nhật** | Phải tái huấn luyện hoặc tinh chỉnh tốn kém | Cập nhật tức thời thông qua việc nạp tài liệu mới |
| **Khả năng kiểm chứng** | Hộp đen, khó truy nguyên nguồn gốc suy luận | Cung cấp trích dẫn nguồn gốc đoạn văn minh bạch |
| **Bảo mật dữ liệu** | Nguy cơ rò rỉ tri thức qua tấn công trích xuất | Kiểm soát quyền truy cập trực tiếp tại tầng truy xuất |
| **Chi phí vận hành** | Đắt đỏ khi phải tái huấn luyện định kỳ | Tiết kiệm chi phí, sử dụng mô hình cố định |

```mermaid
flowchart TD
    subgraph Thuần_Tham_Số["Mô hình Ngôn ngữ Thuần Tham số"]
        Q1["Truy vấn Người dùng"] --> LLM1["Mô hình Ngôn ngữ"]
        M1["Bộ nhớ Tham số Đóng"] --> LLM1
        LLM1 --> R1["Nguy cơ Ảo giác và Lạc hậu Dữ kiện"]
    end

    subgraph Tang_Cuong_Truy_Xuat["Kiến trúc Sinh Tăng cường Truy xuất"]
        Q2["Truy vấn Người dùng"] --> RET["Hệ thống Truy xuất"]
        DB["Bộ nhớ Phi tham số Ngoài"] --> RET
        RET --> CTX["Ngữ cảnh Dữ kiện Xác thực"]
        Q2 --> GEN["Bộ não Suy luận"]
        CTX --> GEN
        GEN --> R2["Câu trả lời Chính xác có Trích dẫn Minh bạch"]
    end
```

*Hình 1.1: Sơ đồ so sánh cơ chế vận hành giữa mô hình ngôn ngữ thuần tham số và kiến trúc RAG*

#### 1.1.4. Tình hình nghiên cứu trong nước, ngoài nước và nhu cầu thực tiễn theo Đề cương nghiên cứu
Theo tinh thần xác lập trong Đề cương Nghiên cứu Khoa học Sinh viên số 07-SV-2026-ĐT1 do Khoa Kỹ thuật Điện tử 1 (Học viện Công nghệ Bưu chính Viễn thông) phê duyệt, bối cảnh thực tiễn của đề tài được định vị rõ nét:

- **Tình hình nghiên cứu và ứng dụng trong nước**: Trong những năm gần đây, trí tuệ nhân tạo và các mô hình ngôn ngữ lớn nhận được sự quan tâm sâu rộng tại Việt Nam trên nhiều lĩnh vực trọng yếu như giáo dục, hành chính công, y tế, tài chính và quản lý tri thức. Hàng loạt ứng dụng trợ lý ảo và chatbot hỏi đáp đã được triển khai. Tuy nhiên, rào cản lớn nhất hiện nay là mô hình ngôn ngữ thông thường không thể giải đáp chính xác dữ liệu nội bộ, giáo trình, văn bản hành chính hay tài liệu kỹ thuật chuyên ngành do dữ liệu biến động theo thời gian hoặc chưa từng xuất hiện trong tập tiền huấn luyện, dẫn tới nguy cơ sinh câu trả lời sai lệch không có trích dẫn kiểm chứng. Nhu cầu xây dựng các hệ thống AI có khả năng khai thác kho tài liệu nội bộ tại các trường đại học và cơ quan là vô cùng cấp bách.
- **Ý nghĩa đào tạo đối với sinh viên khối ngành Kỹ thuật**: Đối với sinh viên chuyên ngành Kỹ thuật Điện tử, Viễn thông, IoT và Công nghệ Thông tin tại Học viện Công nghệ Bưu chính Viễn thông, việc nghiên cứu kiến trúc RAG mang lại cơ hội tiếp cận trực tiếp các kỹ nghệ AI hiện đại nhất: từ xử lý ngôn ngữ tự nhiên, biểu diễn vector nhúng, cơ sở dữ liệu vector, kỹ thuật truy xuất ngữ nghĩa đến tích hợp mô hình ngôn ngữ vào môi trường ứng dụng thực tế.
- **Tình hình nghiên cứu trên thế giới**: RAG đã phát triển thành một hướng nghiên cứu mũi nhọn với sự hỗ trợ của các khung công cụ tiên tiến như LangChain, LlamaIndex, FAISS, ChromaDB và Qdrant. Xu thế hiện đại không chỉ dừng ở việc giải đáp văn bản đơn thuần mà chuyển dịch mạnh mẽ sang kiểm soát độ tin cậy, truy xuất trích dẫn đa vector, xử lý dữ liệu bán cấu trúc (bảng biểu, sơ đồ) và bảo đảm tính tương thích cao trên các môi trường máy chủ Linux.
- **Nhu cầu thực tế**: Trong thực tiễn, việc tra cứu thủ công đòi hỏi người dùng tốn hàng giờ đọc nhiều tài liệu, trong khi các công cụ tìm kiếm từ khóa cổ điển chỉ trả về tài liệu liên quan mà không có khả năng tổng hợp câu trả lời theo đúng ngữ cảnh. Đề tài giải quyết vấn đề này bằng cách cho phép người dùng đặt câu hỏi bằng ngôn ngữ tự nhiên và nhận được câu trả lời tổng hợp súc tích, có cơ sở dữ liệu dựa trên nguồn tri thức tin cậy được nạp vào hệ thống.

### 1.2. Khoảng trống nghiên cứu

Mặc dù kiến trúc RAG đã phát triển mạnh mẽ trên trường quốc tế (Gao et al., 2023; Zhao et al., 2024; Huang et al., 2024), việc áp dụng vào khai phá tài liệu khoa học chuyên sâu vẫn bộc lộ năm khoảng trống nghiên cứu cốt lõi:

**Khoảng trống 1: Thiếu vắng các tổng quan học thuật tiếng Việt có hệ thống về ba thế hệ RAG.** Hầu hết các công trình tổng quan hiện nay được công bố bằng tiếng Anh (Gao et al., 2023; Zhao et al., 2024). Tại Việt Nam, tài liệu kỹ thuật về RAG chủ yếu mang tính thực hành ngắn hạn, thiếu đi các công trình học thuật chuẩn mực có khả năng tổng hợp, giải phẫu toán học và phân loại chuyên sâu sự tiến hóa qua ba thế hệ: Naive RAG, Advanced RAG và Modular RAG dưới một khung phân tích lý thuyết nhất quán.

**Khoảng trống 2: Thiếu thực nghiệm đối chứng trực tiếp giữa các chiến lược phân đoạn văn bản trên cùng tập ngữ liệu chuẩn.** Các khảo sát hiện hữu (Gao et al., 2023; Zhao et al., 2024) chủ yếu đưa ra hệ thống phân loại lý thuyết diện rộng, thiếu các thực nghiệm kiểm chứng có kiểm soát đối sánh các chiến lược phân đoạn văn bản và giải pháp cơ sở dữ liệu vector trên cùng một tập dữ liệu chuẩn. Trong khi đó, tài liệu khoa học có cấu trúc logic đa tầng phức tạp gồm công thức toán học, bảng biểu và cây phân cấp đề mục, đòi hỏi phải có đánh giá thực chứng độc lập.

**Khoảng trống 3: Chưa có nghiên cứu định lượng về mô hình nhúng siêu nhẹ cục bộ trên văn bản khoa học.** Phần lớn các triển khai thực tế phụ thuộc vào API nhúng từ xa của các nhà cung cấp thương mại đám mây hoặc mô hình nhúng khổng lồ đòi hỏi máy chủ GPU đắt đỏ. Sự xuất hiện của các mô hình nhúng siêu nhẹ vận hành trên nền tảng FastEmbed và ONNX Runtime mang lại tiềm năng triển khai cục bộ an toàn và tiết kiệm. Tuy nhiên, hiệu năng truy xuất ngữ nghĩa của các mô hình nhúng nhẹ như BAAI/bge-small-en-v1.5 trên tài liệu khoa học chuyên sâu vẫn chưa được lượng hóa thực nghiệm đầy đủ.

**Khoảng trống 4: Thiếu định lượng thực chứng về sự đánh đổi kỹ thuật giữa RAG và các mô hình có cửa sổ ngữ cảnh siêu dài.** Sự ra đời của các mô hình ngôn ngữ hỗ trợ cửa sổ ngữ cảnh lên tới hàng triệu token làm dấy lên giả thuyết rằng RAG có thể bị thay thế. Tuy nhiên, các luận điểm hiện có chủ yếu mang tính định tính, chưa có các đo lường chi tiết về độ trễ, chi phí tính toán theo bước sinh và hiện tượng suy giảm chú ý ở vùng giữa ngữ cảnh đối với các tác vụ tra cứu tài liệu khoa học.

**Khoảng trống 5: Thách thức xử lý dữ liệu đa phương thức và bán cấu trúc trong tài liệu khoa học.** Tài liệu nghiên cứu khoa học thực tế luôn kết hợp văn bản với các bảng biểu số liệu thí nghiệm, đồ thị so sánh và hình vẽ sơ đồ. Hầu hết các hệ thống RAG thực nghiệm hiện hành mới chỉ xử lý văn bản thô, làm mất hoàn toàn ngữ cảnh thị giác và phá vỡ cấu trúc bảng biểu. Các giải pháp RAG đa phương thức hiện đại với mô hình nhúng không gian đồng nhất 1408 chiều và cơ chế Truy xuất Đa vector (Multi-Vector Retriever) chưa được hệ thống hóa và phân tích tường minh trong y văn tiếng Việt.

*Bảng 1.1: Tổng hợp các khoảng trống nghiên cứu và đóng góp của đề tài*:

| Khoảng trống Nghiên cứu | Giới hạn của Y văn Hiện tại | Đóng góp của Đề tài Này |
| :--- | :--- | :--- |
| **Tổng quan hệ thống** | Phân tán, thiếu công trình tiếng Việt chuẩn mực | Xây dựng khung phân tích thống nhất 3 thế hệ RAG |
| **Chiến lược phân đoạn** | Thử nghiệm rời rạc, chưa khống chế dưới 512 token | Thực nghiệm đối chứng 3 chiến lược trên ngữ liệu khoa học (318–398 chunks) |
| **Mô hình nhúng nhẹ** | Phụ thuộc dịch vụ đám mây, thiếu đo lường cục bộ | Đo lường hiệu năng FastEmbed BGE-small qua Hit@k, MRR, nDCG trên CPU |
| **Đánh đổi ngữ cảnh** | Thảo luận định tính, thiếu căn cứ số liệu | Phân tích toàn diện dựa trên tài liệu thực chứng, độ phức tạp và chi phí |
| **RAG Đa phương thức** | Bỏ qua dữ liệu thị giác và bảng biểu bán cấu trúc | Phân tích 2 trường phái kiến trúc và Multi-Vector Retriever |

### 1.3. Mục tiêu nghiên cứu

Xuất phát từ Đề cương Nghiên cứu Khoa học Sinh viên số 07-SV-2026-ĐT1 được Khoa Kỹ thuật Điện tử 1 (Học viện Công nghệ Bưu chính Viễn thông) chính thức thông qua ngày 03 tháng 4 năm 2026, mục tiêu tổng quát của đề tài được xác định: **Nghiên cứu và xây dựng một hệ thống trí tuệ nhân tạo có khả năng hỏi đáp dựa trên nguồn tri thức được cung cấp, sử dụng phương pháp Retrieval-Augmented Generation — RAG nhằm nâng cao độ chính xác, khả năng kiểm chứng thông tin và tính phù hợp của câu trả lời, đồng thời cung cấp luận cứ định lượng tin cậy cho cộng đồng nghiên cứu.**

Năm mục tiêu cụ thể được lượng hóa rõ ràng như sau:

1. **Tổng quan và phân loại hệ thống ba thế hệ kiến trúc RAG**: Hệ thống hóa tiến trình tiến hóa của RAG qua ba thế hệ: Naive RAG, Advanced RAG và Modular RAG dựa trên tập 5 công trình khoa học nền tảng: Lewis et al. (2020), Gao et al. (2023b), Zhao et al. (2024), Huang & Huang (2024) và Petroni et al. (2021).

2. **Hiện thực hóa và kiểm chứng đường ống RAG trên ngữ liệu khoa học chuẩn**: Xây dựng hoàn chỉnh đường ống RAG cục bộ hiệu năng cao kết hợp cơ sở dữ liệu vector ChromaDB, mô hình nhúng FastEmbed dựa trên ONNX Runtime và thư viện PyMuPDF, thực nghiệm khép kín trên ngữ liệu 5 bài báo khoa học chuẩn (121 trang), bảo đảm khả năng vận hành ổn định trên cả môi trường Linux và Windows.

3. **Thực nghiệm đối sánh ba chiến lược phân đoạn văn bản và phương pháp truy xuất**: Thực hiện các thử nghiệm có kiểm soát nhằm đo lường và đánh giá so sánh tác động của 3 chiến lược phân đoạn văn bản (độ dài cố định 250 từ, trượt có độ gối đầu 50 từ, và đệ quy theo cấu trúc) khống chế dưới 512 token kết hợp đối chứng với baseline BM25 và mô hình all-MiniLM-L6-v2 trên bộ 40 câu hỏi ground-truth.

4. **Phân tích và vận dụng các khung tiêu chuẩn đánh giá RAG hiện đại**: Nghiên cứu bản chất giải thuật của các bộ tiêu chuẩn đo lường tiên tiến (RAGAS, ARES, RGB), thiết lập quy trình đánh giá dựa trên các chỉ số: độ trung thực, độ liên quan, độ chính xác ngữ cảnh và độ bao phủ trích dẫn.

5. **Nghiên cứu chuyên sâu kiến trúc RAG Đa phương thức và kỹ thuật Truy xuất Đa vector**: Phân tích hai trường phái kiến trúc RAG Đa phương thức (mô hình nhúng đa phương thức đồng nhất 1408 chiều và nhúng văn bản qua tóm tắt) kết hợp cơ chế Multi-Vector Retriever của LangChain, làm rõ giải pháp kỹ thuật bảo toàn cấu trúc bảng biểu và hình ảnh thị giác trong tài liệu khoa học.

### 1.4. Câu hỏi nghiên cứu

Đề tài tập trung giải quyết bốn câu hỏi nghiên cứu cốt lõi:

- **RQ1: Kiến trúc RAG đã tiến hóa qua những giai đoạn nào và đâu là bước đột phá cốt lõi ở mỗi thế hệ?**
  *Trọng tâm*: Phân tích sự chuyển dịch từ đường ống tuần tự của Naive RAG sang mô hình ba pha tối ưu hóa của Advanced RAG và cấu trúc module hóa linh hoạt của Modular RAG.

- **RQ2: Khả năng truy xuất và xếp hạng của mô hình nhúng siêu nhẹ BAAI/bge-small-en-v1.5 trên tài liệu khoa học đạt mức nào khi đo bằng các chỉ số retrieval chuẩn mực (Hit@k, MRR@k, nDCG@k) so sánh với baseline từ vựng BM25 và mô hình all-MiniLM-L6-v2?**
  *Trọng tâm*: Xác định tính khả thi và độ chính xác toán học của mô hình nhúng siêu nhẹ khi triển khai cục bộ với FastEmbed và ONNX Runtime trong việc phân tách các khái niệm học thuật chuyên sâu.

- **RQ3: Chiến lược phân đoạn văn bản nào trong ba cấu hình (phân đoạn cố định, phân đoạn trượt có gối đầu, phân đoạn đệ quy theo cấu trúc) mang lại hiệu quả cân bằng nhất giữa tính toàn vẹn ngữ cảnh và độ chính xác xếp hạng truy xuất khi khống chế độ dài chunk dưới giới hạn 512 token?**
  *Trọng tâm*: Kiểm chứng giả thuyết rằng chiến lược phân đoạn trượt có vùng gối đầu ngữ cảnh bảo toàn các thuật ngữ và công thức ở ranh giới cắt, giúp nâng cao thứ hạng tài liệu mục tiêu so với phân đoạn tĩnh.

- **RQ4: Kiến trúc RAG có bị thay thế bởi các LLM có cửa sổ ngữ cảnh siêu dài hay chúng bổ trợ lẫn nhau?**
  *Trọng tâm*: Phân tích sự đánh đổi kỹ thuật giữa hai tiếp cận dưới góc độ lý thuyết độ phức tạp tính toán, hiện tượng mất tập trung ở vùng giữa ngữ cảnh, cơ chế Prompt Caching, độ trễ và chi phí vận hành.

| Câu hỏi | Giả thuyết Khoa học | Phương pháp Tiếp cận | Tiêu chí Đánh giá |
| :--- | :--- | :--- | :--- |
| **RQ1** | Mỗi thế hệ RAG khắc phục trực tiếp điểm nghẽn kiến trúc của thế hệ tiền nhiệm | Khảo cứu y văn và giải phẫu mô hình toán học | Tính bao quát và chiều sâu lý thuyết |
| **RQ2** | Mô hình nhúng siêu nhẹ kết hợp query instruction đạt hiệu năng truy xuất cạnh tranh | Xây dựng chỉ mục ChromaDB và chạy thực nghiệm đối chứng | Hit@1, Hit@5, MRR@5, nDCG@5 và độ trễ (ms) |
| **RQ3** | Phân đoạn trượt có độ gối đầu bảo toàn ngữ cảnh khoa học tốt nhất | Thực nghiệm đối chứng 3 chiến lược trên 40 câu hỏi ground-truth | Hit@k, MRR@5 và nDCG@5 |
| **RQ4** | RAG và Cửa sổ dài không triệt tiêu mà bổ trợ hiệp đồng trong kiến trúc phân tầng | Khảo sát nghiên cứu thực nghiệm và phân tích lý thuyết | Độ trễ suy luận, chi phí token và độ chính xác dữ kiện |

### 1.5. Phạm vi và đối tượng nghiên cứu

#### 1.5.1. Đối tượng nghiên cứu
Đối tượng nghiên cứu trọng tâm của đề tài là bản chất cấu trúc và cơ chế toán học của kiến trúc RAG, phương pháp biểu diễn vector nhúng ngữ nghĩa dày đặc, giải thuật tìm kiếm láng giềng gần nhất xấp xỉ HNSW, kỹ thuật phân đoạn tài liệu khoa học và các tiêu chuẩn đánh giá định lượng hệ thống RAG.

#### 1.5.2. Ngữ liệu thực nghiệm
Nghiên cứu tập trung vào văn bản học thuật tiếng Anh chuyên ngành Trí tuệ Nhân tạo. Tập ngữ liệu bao gồm toàn văn 5 bài báo khoa học nền tảng với tổng cộng **121 trang PDF**:
1. Lewis et al. (2020) - *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (NeurIPS 2020, 19 trang).
2. Gao et al. (2023b) - *Retrieval-Augmented Generation for Large Language Models: A Survey* (arXiv:2312.10997, 21 trang).
3. Zhao et al. (2024) - *Retrieval-Augmented Generation for AI-Generated Content: A Survey* (arXiv:2402.19473, 22 trang).
4. Huang & Huang (2024) - *A Survey on Retrieval-Augmented Text Generation for Large Language Models* (arXiv:2404.10981, 37 trang).
5. Petroni et al. (2021) - *KILT: a Benchmark for Knowledge Intensive Language Tasks* (NAACL-HLT 2021, 22 trang).

#### 1.5.3. Ngăn xếp công nghệ thực nghiệm
- **Ngôn ngữ và môi trường**: Python 3.11 với kiến trúc module hóa.
- **Cơ sở dữ liệu vector**: ChromaDB, sử dụng chỉ mục đồ thị Hierarchical Navigable Small World (HNSW).
- **Mô hình nhúng**: FastEmbed tích hợp mô hình BAAI/bge-small-en-v1.5 tối ưu hóa bằng ONNX Runtime.
- **Trích xuất dữ liệu**: Thư viện PyMuPDF cho văn bản PDF khoa học.
- **Tham chiếu ứng dụng**: Dự án thực tế vibecoding-sunflower.

#### 1.5.4. Ranh giới loại trừ của đề tài
Đề tài xác định rõ các ranh giới loại trừ nhằm tập trung nguồn lực:
- Không hiện thực hóa mô hình RAG đa phương thức cho dữ liệu video, âm thanh phức tạp; chỉ tập trung vào văn bản khoa học có cấu trúc.
- Không tích hợp và không phụ thuộc vào các API mô hình tạo sinh thương mại trả phí (như GPT-4) cho khâu tạo văn bản cuối cùng, bảo đảm tính khách quan, khả năng tái lập độc lập và bảo mật nội bộ trong môi trường học thuật.

| Ranh giới Phạm vi | Thuộc Phạm vi Nghiên cứu | Nằm Ngoài Phạm vi (Loại trừ) |
| :--- | :--- | :--- |
| **Loại hình dữ liệu** | Tài liệu khoa học có cấu trúc dạng văn bản | Dữ liệu đa phương thức video, âm thanh thời gian thực |
| **Tập dữ liệu kiểm thử** | 5 bài báo khoa học kinh điển về RAG | Dữ liệu đàm thoại mở, mạng xã hội hoặc tin tức |
| **Tầng công nghệ** | ChromaDB, FastEmbed, ONNX, PyMuPDF | Dịch vụ cơ sở dữ liệu vector đám mây thương mại |
| **Khâu tạo sinh** | Phân tích cơ chế giải mã và đánh giá ngữ cảnh | Gọi API mô hình ngôn ngữ thương mại có trả phí |

```mermaid
flowchart TD
    subgraph Pham_Vi_Nghien_Cuu["Phạm vi Nghiên cứu"]
        A1["Dữ liệu: 5 Bài báo Khoa học Nền tảng"]
        A2["Tác vụ: Truy xuất Ngữ nghĩa và Phân đoạn Văn bản"]
        A3["Công nghệ: ChromaDB kết hợp FastEmbed và ONNX"]
    end
    
    subgraph Gioi_Han_Loai_Tru["Giới hạn Loại trừ"]
        B1["Không triển khai RAG Đa phương thức Video và Âm thanh"]
        B2["Không phụ thuộc API Mô hình Thương mại Đóng"]
        B3["Không thực hiện Tinh chỉnh Toàn phần Trọng số LLM"]
    end
    
    Pham_Vi_Nghien_Cuu -.->|Tập trung Tối ưu| RAG_Focus["Hệ thống RAG Cục bộ Hiệu năng cao cho Tài liệu Khoa học"]
```

*Hình 1.2: Sơ đồ xác định phạm vi nghiên cứu trọng tâm và các giới hạn loại trừ*

### 1.6. Cấu trúc báo cáo

Báo cáo nghiên cứu khoa học được cấu trúc thành 5 chương chính, thiết lập mạch lập luận xuyên suốt từ cơ sở lý thuyết đến thực nghiệm kiểm chứng:

- **Chương 1: Đặt vấn đề**: Thiết lập bối cảnh bùng nổ của mô hình ngôn ngữ lớn, chỉ ra bốn điểm nghẽn nội tại của bộ nhớ tham số, giới thiệu bước chuyển dịch mô hình của RAG, xác định năm khoảng trống nghiên cứu, năm mục tiêu cụ thể, bốn câu hỏi nghiên cứu, phạm vi và ranh giới đề tài.

- **Chương 2: Cơ sở lý thuyết và Tổng quan tài liệu**: Phân tích lý thuyết về hệ thống AI có tri thức và chuẩn KILT. Giải phẫu toán học bài báo khởi nguyên của Lewis et al. (2020) với hai biến thể mô hình RAG-Sequence và RAG-Token. Khảo sát toàn diện ba thế hệ kiến trúc RAG: Naive RAG, Advanced RAG và Modular RAG; phân tích chuyên sâu hai trường phái kiến trúc RAG Đa phương thức và kỹ thuật Truy xuất Đa vector (Multi-Vector Retriever); khảo cứu các khung đo lường (RAGAS, ARES, RGB), GraphRAG và Agentic RAG.

- **Chương 3: Phương pháp nghiên cứu và Thiết kế hệ thống RAG**: Chi tiết hóa kiến trúc đường ống RAG thực nghiệm dựa trên ChromaDB, FastEmbed và ONNX Runtime. Trình bày phương pháp tiền xử lý văn bản liên tục xuyên trang bằng PyMuPDF, giải thuật chỉ mục HNSW, quy trình chuyển đổi vector nhúng của mô hình BGE và thiết kế chi tiết 3 chiến lược phân đoạn văn bản thực nghiệm khống chế dưới 512 token.

- **Chương 4: Kết quả thực nghiệm và Thảo luận**: Công bố các số liệu thực nghiệm đo lường trên ngữ liệu 5 bài báo khoa học (121 trang). So sánh định lượng hiệu năng của 3 chiến lược phân đoạn và 3 phương pháp truy xuất (BM25, all-MiniLM-L6-v2, BAAI/bge-small-en-v1.5) theo các chỉ số Hit@k, MRR@5 và nDCG@5. Phân tích các thất bại truy xuất thực tế và giải đáp toàn diện 4 câu hỏi nghiên cứu.

- **Chương 5: Kết luận và Hướng phát triển**: Tổng kết toàn bộ các đóng góp học thuật và phát hiện then chốt. Đánh giá sự tương hỗ giữa RAG và các mô hình có cửa sổ ngữ cảnh siêu dài. Giới thiệu các hướng mở rộng đột phá như GraphRAG, Agentic RAG; nêu rõ hạn chế và kiến nghị nghiên cứu tiếp theo.

Nhằm bảo đảm tính kế thừa chặt chẽ và tuân thủ nghiêm ngặt các mục tiêu đã đăng ký, đề tài thiết lập bảng đối chiếu chi tiết giữa bốn nội dung trong Đề cương NCKH số 07-SV-2026-ĐT1 với cấu trúc năm chương của báo cáo toàn văn:

*Bảng 1.2: Bảng đối chiếu giữa 4 Nội dung nghiên cứu của Đề cương NCKH số 07-SV-2026-ĐT1 với Cấu trúc 5 Chương của Báo cáo*:

| Nội dung theo Đề cương (07-SV-2026-ĐT1) | Cấu trúc Chương tương ứng | Trọng tâm Triển khai và Sản phẩm Đầu ra |
| :--- | :--- | :--- |
| **Nội dung 1**: Nghiên cứu tổng quan về trí tuệ nhân tạo, mô hình ngôn ngữ lớn và RAG | **Chương 1** (Đặt vấn đề) & **Chương 2** (Cơ sở lý thuyết và Tổng quan) | Khảo cứu y văn quốc tế, giải phẫu toán học Lewis et al. (2020), phân loại 3 thế hệ RAG (Naive, Advanced, Modular) và RAG Đa phương thức. |
| **Nội dung 2**: Khảo sát và lựa chọn kiến trúc hệ thống RAG | **Chương 2** (Mục 2.3, 2.4) & **Chương 3** (Mục 3.3, 3.5, 3.7) | Khảo sát các giải pháp công nghệ, lựa chọn ngăn xếp kỹ thuật: PyMuPDF, FastEmbed BGE-small, ChromaDB HNSW, tối ưu hoá chi phí điện toán. |
| **Nội dung 3**: Xây dựng hệ thống | **Chương 3** (Mục 3.3) & **Phụ lục B, Phụ lục C** | Hiện thực hóa mã nguồn hệ thống hoàn chỉnh, hỗ trợ môi trường Linux và Windows, thiết lập đường ống nạp dữ liệu và truy vấn thời gian thực. |
| **Nội dung 4**: Thử nghiệm và đánh giá | **Chương 4** (Kết quả và Thảo luận) | Thực nghiệm khép kín trên ngữ liệu 5 bài báo khoa học, đối sánh 3 chiến lược phân đoạn, phân tích thất bại và giải đáp 4 câu hỏi nghiên cứu. |
| **Nghiệm thu & Đề xuất**: Tổng kết đánh giá và định hướng phát triển | **Chương 5** (Kết luận, Hạn chế và Hướng nghiên cứu tiếp theo) | Đối chiếu mức độ hoàn thành so với đề cương, chỉ rõ các giới hạn khách quan, đề xuất lộ trình mở rộng GraphRAG và Agentic RAG. |

```mermaid
flowchart TD
    C1["Chương 1: Đặt vấn đề và Khoảng trống Nghiên cứu"] --> C2["Chương 2: Cơ sở Lý thuyết và Phân loại Ba Thế hệ RAG"]
    C2 --> C3["Chương 3: Phương pháp và Thiết kế Hệ thống Thực nghiệm"]
    C3 --> C4["Chương 4: Kết quả Thực nghiệm, Đối sánh và Thảo luận"]
    C4 --> C5["Chương 5: Xu hướng Đột phá, Giới hạn và Kết luận"]
```

*Hình 1.3: Cấu trúc năm chương và luồng triển khai của đề tài nghiên cứu*

---

*Chương 1 đã thiết lập toàn bộ nền tảng luận điểm, xác định rõ tính cấp thiết của đề tài và định vị các đóng góp khoa học chính của nghiên cứu. Tiếp theo, Chương 2 sẽ đi sâu phân tích cơ sở lý thuyết toán học và khảo cứu có hệ thống sự tiến hóa của các thế hệ kiến trúc RAG trong kho tàng y văn thế giới.*
"""

if __name__ == '__main__':
    print("Length of CHAPTER_1 string:", len(CHAPTER_1))
    print("Word count estimate:", len(CHAPTER_1.split()))
