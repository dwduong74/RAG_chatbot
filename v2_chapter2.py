# -*- coding: utf-8 -*-
"""
Chương 2: Cơ sở Lý thuyết và Tổng quan Nghiên cứu
Báo cáo Nghiên cứu Khoa học: Hệ thống Trí tuệ Nhân tạo có Tri thức và Kiến trúc RAG
"""
import sys

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

CHAPTER_2 = r"""## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN NGHIÊN CỨU

Chương này thiết lập nền tảng lý thuyết vững chắc và cung cấp cái nhìn tổng quan có hệ thống về toàn bộ hệ sinh thái của các hệ thống trí tuệ nhân tạo có tri thức. Nội dung chương đi từ bản chất của việc phân tách bộ nhớ, phân tích mô hình toán học xác suất trong công trình khởi nguyên của Lewis et al. (2020), khảo sát sự tiến hóa qua ba thế hệ kiến trúc RAG, mở rộng sang lĩnh vực đa phương thức, hệ thống hóa các khung đo lường đánh giá hiệu năng tiên tiến, và phân tích các xu hướng đột phá đang định hình tương lai.

---

### 2.1. Bản chất của Hệ thống Trí tuệ Nhân tạo có Tri thức và Chuẩn mực Đánh giá KILT

#### 2.1.1. Định nghĩa chuẩn tắc về tác vụ đòi hỏi tri thức chuyên sâu
Trong lý thuyết khoa học nhận thức và xử lý ngôn ngữ tự nhiên, các tác vụ tính toán được phân chia thành hai nhóm ranh giới cơ bản:
1. **Tác vụ dựa trên kỹ năng ngôn ngữ và cấu trúc**: Bao gồm phân tích cú pháp, gán nhãn từ loại, nhận diện thực thể tên cơ bản, hoặc sửa lỗi chính tả. Các tác vụ này chỉ đòi hỏi mô hình nắm vững quy luật ngữ pháp và ngữ nghĩa cấu trúc câu, vốn có thể tổng quát hóa tốt qua quá trình học thống kê.
2. **Tác vụ đòi hỏi tri thức chuyên sâu**: Được định nghĩa chuẩn tắc bởi Petroni et al. (2020) và Lewis et al. (2020) là:
> *"Những tác vụ mà một con người thông minh, có học thức thông thường cũng không thể kỳ vọng hoàn thành chính xác nếu không được cung cấp hoặc chủ động tra cứu một kho tài liệu tri thức bên ngoài đáng tin cậy."*

Các nhóm bài toán tiêu biểu thuộc diện này bao gồm:
- **Hỏi đáp miền mở**: Trả lời các câu hỏi về sự kiện lịch sử, công thức khoa học hay dữ kiện địa lý mà không có ngữ cảnh cung cấp sẵn; hệ thống phải tự tìm kiếm trong kho tri thức toàn diện.
- **Kiểm chứng sự thật**: Xác định một phát biểu là đúng, sai hay không đủ căn cứ, đồng thời chỉ ra đoạn văn bản bằng chứng chứng minh cho kết luận đó.
- **Hội thoại đòi hỏi tri thức**: Trợ lý ảo tương tác chuyên sâu với chuyên gia về các chủ đề học thuật hoặc nghiệp vụ phức tạp.
- **Điền khuyết thực thể**: Dự đoán mối quan hệ giữa các thực thể dựa trên kho dữ liệu thực tế liên tục cập nhật.

#### 2.1.2. Lý thuyết phân tách bộ nhớ: Bộ nhớ tham số và Bộ nhớ phi tham số
Kiến trúc AI truyền thống gộp chung năng lực tính toán và dữ liệu vào cùng một khối tham số mạng nơ-ron. Ngược lại, kiến trúc AI có tri thức hiện đại vận hành dựa trên nguyên lý phân tách tường minh giữa hai loại bộ nhớ:

```mermaid
graph TD
    Root["HỆ THỐNG TRÍ TUỆ NHÂN TẠO CÓ TRI THỨC"] --> PM["BỘ NHỚ THAM SỐ<br/>• Trọng số ma trận mạng nơ-ron Transformer<br/>• Học qua giải thuật Lan truyền ngược<br/>• Năng lực: Cú pháp, Ngữ nghĩa và Suy luận<br/>• Chi phí cập nhật: Rất cao khi tái huấn luyện<br/>• Tính giải thích: Hộp đen nơ-ron phức tạp"]
    Root --> NPM["BỘ NHỚ PHI THAM SỐ<br/>• Cơ sở dữ liệu Vector và Chỉ mục HNSW<br/>• Kho tri thức tài liệu rời rạc như PDF và CSDL<br/>• Cập nhật động theo thời gian thực<br/>• Chi phí cập nhật: Cực thấp khi cập nhật dữ liệu<br/>• Tính giải thích: Truy vết nguồn gốc minh bạch"]
```

*Hình 2.1: Sơ đồ phân tách bộ nhớ trong hệ thống trí tuệ nhân tạo có tri thức*

*Bảng 2.1: So sánh chi tiết đặc tính kỹ thuật giữa hai loại bộ nhớ*:

| Đặc tính so sánh | Bộ nhớ tham số | Bộ nhớ phi tham số |
| :--- | :--- | :--- |
| **Bản chất vật lý** | Trọng số ma trận liên tục ($W \in \mathbb{R}^{d \times d}$) | Kho vector rời rạc, bảng dữ liệu, đồ thị tri thức |
| **Cơ chế cập nhật** | Tối ưu hóa lan truyền ngược gradient | Thêm, sửa, xóa bản ghi trực tiếp trong CSDL |
| **Thời gian cập nhật** | Vài giờ đến vài tháng (đòi hỏi siêu máy tính) | Thời gian thực (vài phần nghìn giây) |
| **Khả năng kiểm chứng** | Khó giải thích (hộp đen mạng nơ-ron) | Truy vết trực tiếp về văn bản gốc, trang sách, URL |
| **Kiểm soát quyền truy cập** | Bất khả thi (không thể che giấu một phần tham số) | Phân quyền chi tiết theo vai trò người dùng |
| **Nguy cơ lỗi** | Ảo giác, nhầm lẫn dữ kiện, tự tin thái quá | Truy xuất sai tài liệu (nhưng phát hiện và sửa được ngay) |

Sự phân tách này mang lại lợi thế chiến lược: Chúng ta có thể đóng băng hoàn toàn tham số của mô hình ngôn ngữ lớn (tiết kiệm chi phí phần cứng khổng lồ), trong khi kho dữ liệu tri thức bên ngoài có thể liên tục được mở rộng, cập nhật và làm sạch mỗi ngày.

#### 2.1.3. Bộ chuẩn Benchmark KILT và Tiêu chuẩn Thẩm định Nguồn gốc Tri thức
Nhằm chuẩn hóa việc đánh giá năng lực của các mô hình AI có tri thức, Petroni et al. (2021) tại Facebook AI Research và University College London đã công bố bộ chuẩn KILT tại hội nghị NAACL-HLT 2021.

KILT giải quyết tình trạng phân mảnh dữ liệu bằng cách:
1. **Neo vào một kho tri thức chuẩn duy nhất**: Sử dụng bản chụp Wikipedia thống nhất gồm hơn **5.9 triệu bài viết** (phân rã thành hơn 35 triệu đoạn văn bản 100 từ).
2. **Quy tụ 11 bộ dữ liệu chuẩn mực thuộc 5 miền tác vụ**:
   - *Fact Checking*: FEVER
   - *Open-Domain QA*: Natural Questions (NQ), TriviaQA, HotpotQA (đòi hỏi suy luận đa bước), ELI5 (trả lời câu hỏi mở dài)
   - *Slot Filling*: T-REx, Zero-Shot RE
   - *Entity Linking*: AIDA CoNLL-YAGO, WNED-WIKI, WNED-CWEB
   - *Dialogue*: Wizard of Wikipedia (WoW)

Đóng góp học thuật quan trọng nhất của KILT là việc thiết lập tiêu chuẩn đánh giá kép: **Độ chính xác nội dung** kết hợp chặt chẽ với **Độ chính xác nguồn gốc** (Provenance). KILT đưa ra chỉ số KILT-AC:

$$\text{KILT-AC} = \text{Accuracy} \times \text{Provenance Success}$$

Trong đó, một câu trả lời chỉ được tính điểm khi và chỉ khi:
1. Nội dung câu trả lời sinh ra khớp với nhãn thực tế.
2. Đoạn văn bản bằng chứng trích dẫn phải nằm trong tập các đoạn văn bản chứng minh hợp lệ được chuyên gia thẩm định.

Khái niệm Provenance khẳng định nguyên lý: *Một phát biểu của trí tuệ nhân tạo chỉ có giá trị khi nó có thể truy nguyên nguồn gốc về một văn bản có thẩm quyền trong thế giới thực.*

---

### 2.2. Bài báo Khởi nguyên và Mô hình Hóa Toán học của RAG (Lewis et al., 2020)

Tại hội nghị NeurIPS 2020, nhóm nghiên cứu tại Facebook AI Research do Patrick Lewis dẫn đầu đã công bố công trình lịch sử: *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"*. Đây là bài báo đầu tiên chính thức đặt tên và mô hình hóa toán học xác suất cho thuật ngữ RAG.

```mermaid
flowchart LR
    Q["Truy vấn x"] --> DPR["Bộ truy xuất DPR (Bi-Encoder BERT)"]
    KB[("Kho tri thức Ngoài\n(Wikipedia MIPS/FAISS)")] --> DPR
    DPR --> TOPK["Top-k Đoạn trích z_i"]
    Q --> COMB["Ghép nối ngữ cảnh [x ; z_i]"]
    TOPK --> COMB
    COMB --> BART["Bộ sinh Seq2Seq (BART-Large)"]
    BART --> ANS["Câu trả lời y"]
```

*Hình 2.2: Sơ đồ kiến trúc RAG khởi nguyên của Lewis et al. (NeurIPS 2020)*

#### 2.2.1. Kiến trúc hai khối nơ-ron ghép nối
Kiến trúc RAG của Lewis et al. bao gồm hai thành phần nơ-ron chính:
1. **Bộ truy xuất nơ-ron Dense Passage Retriever (DPR)**: Dựa trên mô hình Bi-encoder (Karpukhin et al., 2020):
   - Bộ mã hóa câu hỏi $E_Q(x)$ chuyển câu hỏi $x$ thành vector đặc trưng 768 chiều.
   - Bộ mã hóa đoạn văn $E_D(z)$ chuyển từng đoạn văn $z$ thành vector đặc trưng 768 chiều.
   - Điểm số liên quan giữa câu hỏi $x$ và tài liệu $z$ được tính bằng tích vô hướng:
     $$p_\eta(z \mid x) \propto \exp\left(E_Q(x)^T E_D(z)\right)$$
   - Thuật toán Tìm kiếm Tích vô hướng Cực đại (MIPS) qua thư viện FAISS giúp tìm top-$k$ tài liệu nhanh chóng trong vài mili-giây trên hàng chục triệu vector.
2. **Bộ sinh chuỗi (BART-Large)**: Mô hình Seq2Seq với 400 triệu tham số. BART tiếp nhận đầu vào là chuỗi nối tiếp câu hỏi $x$ và tài liệu $z$, sau đó giải mã sinh chuỗi mục tiêu $y$ từng token.

#### 2.2.2. Mô hình toán học RAG-Sequence
Trong RAG-Sequence, hệ thống giả định toàn bộ chuỗi đầu ra $y$ được điều kiện hóa trên cùng một tài liệu truy xuất $z$. Xác suất sinh ra chuỗi $y$ được tính bằng cách lấy kỳ vọng trên tập hợp top-$k$ tài liệu có xác suất truy xuất cao nhất:

$$p_{\text{RAG-Seq}}(y \mid x) = \sum_{z \in \text{top-}k} p_\eta(z \mid x) \cdot p_\theta(y \mid x, z) = \sum_{z \in \text{top-}k} p_\eta(z \mid x) \prod_{i=1}^N p_\theta(y_i \mid x, z, y_{1:i-1})$$

Trong đó:
- $p_\eta(z \mid x)$ là xác suất tiên nghiệm truy xuất tài liệu $z$ từ bộ truy xuất DPR (với tham số $\eta$).
- $p_\theta(y_i \mid x, z, y_{1:i-1})$ là xác suất sinh ra token thứ $i$ của bộ sinh BART (với tham số $\theta$), có điều kiện trên câu hỏi gốc $x$, tài liệu $z$, và các token đã sinh trước đó $y_{1:i-1}$.
- $N$ là độ dài của chuỗi đầu ra $y$.

*Ý nghĩa của RAG-Sequence*: Rất phù hợp khi câu trả lời đòi hỏi tính nhất quán cao và toàn bộ thông tin câu trả lời nằm trọn vẹn trong một đoạn văn bản duy nhất.

#### 2.2.3. Mô hình toán học RAG-Token
RAG-Token mang tính linh hoạt hơn: Việc lựa chọn tài liệu được giải phóng ở cấp độ từng token. Mỗi token sinh ra có thể được điều kiện hóa trên một tài liệu khác nhau:

$$p_{\text{RAG-Token}}(y \mid x) = \prod_{i=1}^N \sum_{z \in \text{top-}k} p_\eta(z \mid x) \cdot p_\theta(y_i \mid x, z, y_{1:i-1})$$

*Phân tích bản chất toán học*:
Tại mỗi bước giải mã $i$, mô hình tính toán một phân phối xác suất hỗn hợp cho token kế tiếp bằng cách tính tổng trọng số xác suất sinh từ $k$ tài liệu khác nhau. Điều này cho phép bộ sinh:
- Lấy một phần thông tin từ tài liệu $z_1$.
- Lấy một phần thông tin khác từ tài liệu $z_2$.
- Tổng hợp thành một câu trả lời hoàn chỉnh mang tính đa nguồn.

#### 2.2.4. Cơ chế huấn luyện End-to-End coi tài liệu là biến tiềm ẩn
Điểm sáng tạo học thuật vượt bậc của Lewis et al. là huấn luyện đầu-cuối mà không cần dữ liệu gán nhãn thủ công về việc câu hỏi nào phải đi với tài liệu nào. Tài liệu được truy xuất $z$ được xem là một **biến tiềm ẩn** trong không gian xác suất.

Hàm mục tiêu huấn luyện cực tiểu hóa hàm mất mát đối số logarit âm của chuỗi đích $y$:

$$\mathcal{L}_{\text{RAG}}(\theta, \eta) = - \sum_{(x, y) \in \mathcal{D}} \log p(y \mid x)$$

Trong quá trình tối ưu hóa bằng thuật toán Adam, đạo hàm riêng được truyền qua cả hai khối:
- Cập nhật tham số bộ sinh $\theta$ để sinh câu trả lời đúng hơn khi có tài liệu hỗ trợ.
- Cập nhật tham số bộ mã hóa truy vấn $\eta$ của DPR: Nếu tài liệu $z$ giúp bộ sinh đưa ra xác suất cho $y$ cao hơn, gradient sẽ tự động điều chỉnh bộ mã hóa truy vấn để kéo vector của câu hỏi $x$ lại gần hơn với vector của tài liệu $z$ trong không gian nhúng.

#### 2.2.5. Thuật toán giải mã: Thorough Decoding và Fast Decoding
Đối với mô hình RAG-Token, phân phối chuyển tiếp token $p'(y_i \mid y_{1:i-1}, x) = \sum_{z \in \text{top-}k} p_\eta(z \mid x) p_\theta(y_i \mid x, z, y_{1:i-1})$ có thể được đưa trực tiếp vào thuật toán Beam Search chuẩn mực để sinh từng token tự hồi quy.

Ngược lại, đối với mô hình RAG-Sequence, xác suất biên $p(y \mid x)$ không phân rã thành tích của các phân phối độc lập từng token, khiến việc tìm kiếm chuỗi cực đại $\arg\max_y p(y \mid x)$ đòi hỏi kỹ thuật giải mã xấp xỉ. Lewis et al. (2020) đề xuất phương pháp tiếp cận dựa trên việc chạy Beam Search độc lập cho từng tài liệu $z$ để thu được tập hợp các chuỗi giả thuyết ứng viên $\mathcal{Y}_z$, sau đó hợp lại thành không gian ứng viên $\mathcal{Y} = \bigcup_z \mathcal{Y}_z$. Để ước tính chuỗi tối ưu trong $\mathcal{Y}$, hai giải thuật xấp xỉ được thiết kế:

1. **Thorough Decoding**: Với mỗi chuỗi ứng viên $y \in \mathcal{Y}$, mô hình tính toán xác suất có điều kiện $p(y \mid x, z)$ trên toàn bộ $k$ tài liệu, ngay cả với những tài liệu $z$ mà chuỗi $y$ không lọt vào beam search cục bộ của tài liệu đó. Phương pháp này bảo đảm tính hội tụ xác suất biên chính xác nhưng đòi hỏi thêm nhiều lượt lan truyền tiến qua mạng nơ-ron cho từng tài liệu.

2. **Fast Decoding**: Để tối ưu hóa tốc độ suy luận, giải thuật Fast Decoding đưa ra giả định xấp xỉ rằng nếu một chuỗi $y$ không được sinh ra trong chùm tia beam search của tài liệu $z$, thì xác suất điều kiện tương ứng xấp xỉ bằng không: $p(y \mid x, z) \approx 0$. Do đó, mô hình chỉ tính tổng xác suất biên trên tập hợp các tài liệu đã thực sự sinh ra $y$ trong beam search cục bộ, loại bỏ hoàn toàn các lượt forward pass bổ sung tốn kém và đạt tốc độ đáp ứng nhanh trong các hệ thống thực tế.

---

### 2.3. Khảo sát và Phân loại Tiến trình Tiến hóa của Kiến trúc RAG

Dựa trên các khảo sát quy mô lớn của Gao et al. (2023b) và Huang & Huang (2024), kiến trúc RAG đã trải qua ba thế hệ tiến hóa chính thức: **Naive RAG**, **Advanced RAG**, và **Modular RAG**.

```mermaid
flowchart LR
    A["<b>KIẾN TRÚC NAIVE RAG</b><br/>• Quy trình tuần tự một chiều<br/>• Cơ chế Truy xuất và Đọc<br/>• Tìm kiếm vector tương đồng thô<br/>• Ghép chuỗi câu lệnh thô"] --> B["<b>KIẾN TRÚC ADVANCED RAG</b><br/>• Tối ưu hóa Tiền truy xuất<br/>• Tìm kiếm lai kết hợp từ khóa<br/>• Tái xếp hạng chéo nơ-ron<br/>• Nén ngữ cảnh chọn lọc"]
    B --> C["<b>KIẾN TRÚC MODULAR RAG</b><br/>• Phân tách các module độc lập<br/>• Định tuyến ngữ nghĩa động<br/>• Luồng điều khiển lặp và đệ quy<br/>• Tự phản chiếu và hiệu chỉnh"]
```

*Hình 2.3: Sơ đồ tiến trình tiến hóa của các thế hệ kiến trúc RAG*

#### 2.3.1. Kiến trúc Naive RAG và các điểm nghẽn cố hữu
Naive RAG đại diện cho mô hình sơ khởi theo quy trình Retrieve-and-Read một chiều, vận hành theo hai giai đoạn độc lập:
1. **Giai đoạn nạp và phân giải dữ liệu (Data Ingestion)**: Văn bản thô được phân chia thành các đoạn có kích thước đồng đều (Even Chunks), sau đó mô hình nhúng chuyển đổi từng đoạn thành vector đặc trưng và lưu trữ vào CSDL vector.
2. **Giai đoạn truy vấn thời gian thực (Querying)**: Bao gồm hai pha nối tiếp: pha truy xuất (Retrieval) tìm kiếm top-$k$ đoạn văn bản có độ tương đồng Cosine cao nhất, và pha tổng hợp (Synthesis) ghép nối các đoạn trích này vào câu hỏi để mô hình ngôn ngữ lớn đọc hiểu và sinh câu trả lời.

```mermaid
flowchart TD
    subgraph Ingestion["Giai đoạn 1: Nạp và Phân giải Dữ liệu (Data Ingestion)"]
        PDF["Tài liệu PDF / Docs"] --> Chunks["Phân đoạn văn bản thành các khối đều đặn (Even Chunks)"]
        Chunks --> Embed["Mã hóa tạo Vector nhúng ngữ nghĩa"]
        Embed --> VDB1["Lưu trữ vào Cơ sở dữ liệu Vector - Chỉ mục HNSW"]
    end

    subgraph Querying["Giai đoạn 2: Truy vấn và Tổng hợp (Querying: Retrieval & Synthesis)"]
        UserQ["Truy vấn người dùng"] --> VDB2["Tìm kiếm Top-k đoạn tương đồng (Pha Retrieval)"]
        VDB2 --> TopChunks["Top-k Đoạn văn bản trích chọn"]
        TopChunks --> LLM["Mô hình ngôn ngữ lớn (Pha Synthesis)"]
        UserQ --> LLM
        LLM --> FinalAns["Câu trả lời chính xác có trích dẫn nguồn"]
    end
```

*Hình 2.4: Sơ đồ quy trình hệ thống hỏi đáp RAG hai giai đoạn: Nạp dữ liệu và Truy vấn trực tiếp*

*Các điểm nghẽn cố tử của Naive RAG*:
- **Độ nhạy thấp**: Tìm kiếm vector đơn thuần chỉ dựa vào khoảng cách ngữ nghĩa bề mặt, thường bỏ sót các từ khóa chuyên ngành chính xác (mã sản phẩm, thuật ngữ y khoa, điều luật).
- **Hiện tượng suy giảm chú ý ở giữa dòng ngữ cảnh (Lost in the Middle - Liu et al., 2024)**: Các mô hình ngôn ngữ lớn có xu hướng chú ý nhiều hơn vào phần đầu và phần cuối của prompt, trong khi bỏ quên thông tin nằm ở vị trí chính giữa. Nếu tài liệu quan trọng nhất rơi vào giữa danh sách top-$k$, mô hình sẽ không trả lời được.
- **Nhiễu loạn ngữ cảnh**: Cắt đoạn thô chứa nhiều câu rác làm cạn kiệt cửa sổ ngữ cảnh và gây nhiễu cơ chế Attention.
- **Ảo giác khi có xung đột dữ kiện**: Khi hai đoạn trích có mâu thuẫn thông tin, Naive RAG không có cơ chế phân xử, khiến mô hình tự sinh câu trả lời sai lệch.

#### 2.3.2. Kiến trúc Advanced RAG: Tối ưu hóa Ba Tầng Toàn Diện
Nhằm khắc phục các hạn chế cốt lõi của Naive RAG, thế hệ Advanced RAG thiết lập quy trình tối ưu hóa trên ba tầng:

```mermaid
flowchart TD
    subgraph S1["TẦNG 1: TIỀN TRUY XUẤT"]
        direction TB
        A1["Phân đoạn ngữ nghĩa phân tầng"]
        A2["Trích xuất và làm giàu siêu dữ liệu"]
        A3["Viết lại và mở rộng câu hỏi truy vấn"]
        A4["Tạo văn bản giả định phục vụ tìm kiếm"]
    end

    subgraph S2["TẦNG 2: TRONG TRUY XUẤT"]
        direction TB
        B1["Tìm kiếm lai kết hợp từ khóa và vector"]
        B2["Thuật toán hợp nhất thứ hạng tương hỗ"]
        B3["Sử dụng mô hình nhúng đa ngôn ngữ tiên tiến"]
    end

    subgraph S3["TẦNG 3: HẬU TRUY XUẤT"]
        direction TB
        C1["Tái xếp hạng chéo nơ-ron"]
        C2["Nén ngữ cảnh và trích lọc dữ kiện cốt lõi"]
        C3["Tái cấu trúc vị trí tài liệu"]
    end

    S1 --> S2
    S2 --> S3
```

*Hình 2.5: Sơ đồ kiến trúc Advanced RAG toàn diện ba tầng*

##### 1. Tầng 1: Tối ưu hóa Tiền truy xuất
- **Cắt đoạn phân tầng Parent-Child**: Chia tài liệu thành các khối lớn chứa ngữ cảnh hoàn chỉnh, sau đó chia nhỏ thành các đoạn con 100-200 từ. Khi tìm kiếm, so sánh vector trên các đoạn con để đạt độ nhạy cao, nhưng khi gửi cho LLM thì nạp toàn bộ khối cha tương ứng.
- **Sinh văn bản giả định (HyDE - Gao et al., 2023a)**: Dùng LLM sinh ra câu trả lời giả lập cho câu hỏi, sau đó dùng vector của câu trả lời giả lập này để tìm kiếm trong CSDL. Kỹ thuật này chuyển đổi bài toán từ so khớp câu hỏi-tài liệu sang so khớp tài liệu-tài liệu, tăng vọt độ chính xác.
- **Phân rã và mở rộng truy vấn**: Tự động phân tách câu hỏi phức tạp thành 3-5 câu hỏi con để tìm kiếm dữ kiện đa chiều.

##### 2. Tầng 2: Tối ưu hóa Trong truy xuất - Tìm kiếm Lai
Advanced RAG kết hợp hai trường phái tìm kiếm bổ trợ:
- **Dense Vector Search**: Bắt trọn ý đồ câu hỏi dù người dùng dùng từ đồng nghĩa hoặc cách diễn đạt khác.
- **Sparse Lexical Search (BM25)**: Bắt chính xác các từ khóa hiếm, mã SKU, ký hiệu hóa học, tên riêng người hoặc điều luật.

Kết quả hai luồng tìm kiếm được hợp nhất thông qua thuật toán Reciprocal Rank Fusion:

$$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Trong đó $r_m(d)$ là thứ hạng của tài liệu $d$ trong hệ thống tìm kiếm $m$, và $k$ là hằng số làm mượt (chuẩn đặt $k=60$).

##### 3. Tầng 3: Tối ưu hóa Hậu truy xuất
- **Tái xếp hạng bằng Cross-Encoder**: Khác với Bi-encoder mã hóa câu hỏi và tài liệu độc lập, Cross-Encoder tiếp nhận đồng thời cả cặp (Câu hỏi, Đoạn trích) và cho phép cơ chế Attention tương tác toàn phần giữa từng từ của câu hỏi với từng từ của văn bản, mang lại điểm số liên quan chính xác hơn.
- **Nén ngữ cảnh**: Loại bỏ các câu văn không chứa thông tin trả lời, chỉ giữ lại những câu mang dữ kiện cốt lõi, giảm đáng kể số lượng token đưa vào LLM.
- **Tái sắp xếp vị trí tài liệu**: Đặt tài liệu có điểm liên quan cao nhất ở đầu prompt, tài liệu cao thứ nhì ở cuối prompt, và tài liệu phụ ở giữa để triệt tiêu hiệu ứng Lost in the Middle.

#### 2.3.3. Kiến trúc Modular RAG: Linh hoạt, Động và Tự phản chiếu
Modular RAG bứt phá khỏi đường ống tuyến tính, tổ chức hệ thống thành các module chức năng chuyên biệt có thể cấu hình linh hoạt:
1. **Module Định tuyến**: Phân loại câu hỏi của người dùng để quyết định: câu hỏi có cần tra cứu không? Nếu có, tra cứu vào CSDL Vector, CSDL quan hệ SQL, hay tìm kiếm ngoài?
2. **Module Bộ nhớ**: Duy trì lịch sử tương tác và dữ kiện tra cứu trước đó cho các phiên hội thoại dài.
3. **Module Kiểm chứng Sự thật**: Kiểm tra chéo câu khẳng định do LLM sinh ra với tài liệu gốc trước khi gửi cho người dùng.
4. **Cơ chế Tự phản chiếu (Self-RAG - Asai et al., 2024)**: Mô hình học cách tự sinh ra 4 loại token phản chiếu đặc biệt:
   - `[Retrieve]`: Quyết định xem có cần tra cứu thêm tài liệu không.
   - `[IsRel]`: Đánh giá tài liệu tìm về có thực sự liên quan không.
   - `[IsSup]`: Đánh giá câu trả lời có được tài liệu chứng minh không.
   - `[IsUse]`: Đánh giá mức độ hữu ích của câu trả lời.
5. **Cơ chế Tự hiệu chỉnh (Corrective RAG - CRAG - Yan et al., 2024)**: Đánh giá độ tin cậy của tài liệu: nếu tin cậy cao, tiếp tục sinh; nếu mơ hồ, kết hợp tìm kiếm ngoài; nếu sai hoàn toàn, hủy bỏ tài liệu và kích hoạt tìm kiếm internet thay thế.

---

### 2.4. Kiến trúc RAG Đa phương thức và Cơ chế Truy xuất Đa vector

Trong kỷ nguyên bùng nổ của các mô hình ngôn ngữ lớn đa phương thức, việc tăng cường tri thức không còn bị giới hạn trong phạm vi văn bản thuần túy. Tài liệu khoa học, báo cáo kỹ thuật và ấn phẩm chuyên ngành thực tế luôn truyền tải tri thức thông qua sự kết hợp chặt chẽ giữa văn bản với hình ảnh minh họa, đồ thị so sánh, bảng số liệu và sơ đồ quy trình.

#### 2.4.1. Động lực khoa học và tính tất yếu của RAG Đa phương thức
Hầu hết các hệ thống RAG truyền thống dựa trên văn bản thuần đều bỏ qua những thông tin giá trị ẩn chứa trong hình ảnh và cấu trúc bảng biểu. Việc áp dụng kiến trúc RAG Đa phương thức đem lại bốn lợi thế học thuật và thực tiễn cốt lõi:
1. **Gia tăng độ chính xác và mức độ liên quan dữ kiện**: Cho phép mô hình dựa trên các bằng chứng thị giác trực tiếp từ sơ đồ và bảng số liệu thực tế, đặc biệt hữu ích trong các báo cáo khoa học đòi hỏi số liệu chính xác cao.
2. **Hạn chế hiện tượng ảo giác thị giác**: Khi người dùng hỏi về thông tin trong biểu đồ hoặc hình vẽ, việc truy xuất đúng hình ảnh gốc giúp mô hình xác minh trực tiếp, loại bỏ việc đoán mò hay suy diễn sai lệch.
3. **Mở rộng khả năng thích ứng miền**: Giúp hệ thống dễ dàng tiếp nhận các dạng tài liệu chuyên ngành phức tạp như y văn (hình ảnh chẩn đoán X-quang, MRI kèm báo cáo xét nghiệm), viễn thông (sơ đồ mạch kèm đặc tả kỹ thuật), hoặc tài chính (bảng cân đối kế toán kèm đồ thị nến).
4. **Nâng cao trải nghiệm người dùng**: Cung cấp câu trả lời giàu thông tin, kèm theo khả năng trích dẫn trực tiếp hình ảnh minh họa hoặc bảng biểu gốc để người dùng đối chiếu nguồn gốc.

#### 2.4.2. Hai trường phái kiến trúc cốt lõi của RAG Đa phương thức
Dựa trên khảo cứu các chuẩn mực công nghệ hàng đầu hiện nay, tiêu biểu là khung giải pháp của Google, RAG Đa phương thức được triển khai theo hai trường phái kiến trúc chính:

##### 1. Trường phái 1: Nhúng đa phương thức không gian đồng nhất
- **Bản chất kỹ thuật**: Sử dụng mô hình nhúng đa phương thức chuyên biệt để tạo ra các vector đặc trưng có số chiều lớn, tiêu biểu là vector **1408 chiều** của Google.
- **Nguyên lý không gian chung**: Điểm đột phá cốt lõi là vector nhúng của hình ảnh và vector nhúng của văn bản cùng nằm trong một không gian ngữ nghĩa thống nhất với cùng một số chiều. Nhờ đó, hệ thống hỗ trợ tìm kiếm chéo phương thức một cách tự nhiên:
  - *Dùng văn bản tìm hình ảnh*: Nhập câu hỏi dạng chữ để truy xuất các sơ đồ, biểu đồ minh họa có ý nghĩa liên quan nhất.
  - *Dùng hình ảnh tìm văn bản*: Đưa vào một sơ đồ kiến trúc hoặc hình chụp lỗi để truy xuất đoạn tài liệu giải thích cơ chế tương ứng.
- **Quy trình tổng hợp**: Sau khi truy xuất, hệ thống truyền đồng thời cả **hình ảnh gốc thô** và **các đoạn văn bản liên quan** vào mô hình ngôn ngữ lớn đa phương thức (như Gemini 1.5 Pro) để phân tích và tổng hợp câu trả lời toàn diện.

##### 2. Trường phái 2: Nhúng văn bản qua tóm tắt tri thức thị giác
- **Bản chất kỹ thuật**: Tận dụng năng lực đọc hiểu thị giác của một mô hình ngôn ngữ lớn đa phương thức tiền trạm để tự động sinh bản tóm tắt mô tả bằng văn bản cho từng hình ảnh, biểu đồ và bảng biểu trong tài liệu.
- **Quy trình vận hành**:
  1. Sử dụng LLM đa phương thức tiền xử lý toàn bộ hình ảnh và bảng biểu thành các đoạn văn mô tả chi tiết.
  2. Dùng mô hình nhúng văn bản thông thường (như bge-small) để vector hóa các bản tóm tắt này và lưu vào CSDL vector.
  3. Khi có truy vấn từ người dùng, hệ thống chỉ cần tìm kiếm tương đồng trên các vector tóm tắt văn bản.
  4. Nạp các khối văn bản đã trích xuất vào LLM để tổng hợp câu trả lời cuối cùng.
- **Ưu điểm**: Tương thích hoàn toàn với hạ tầng CSDL vector văn bản sẵn có mà không đòi hỏi mô hình nhúng đa phương thức chuyên dụng, dù chi phí tính toán ở khâu tiền xử lý tăng lên.

#### 2.4.3. Cơ chế Truy xuất Đa vector cho dữ liệu bán cấu trúc
Kỹ thuật Truy xuất Đa vector (Multi-Vector Retriever) là một bước đột phá quan trọng của thế hệ RAG hiện đại nhằm xử lý các thành phần dữ liệu bán cấu trúc như bảng biểu phức tạp và sơ đồ kỹ thuật:

- **Nghịch lý của phương pháp cắt đoạn truyền thống**:
  - Nếu nhúng toàn bộ một bảng số liệu lớn thành một vector duy nhất, thông tin của từng ô dữ liệu sẽ bị pha loãng nghiêm trọng trong không gian vector.
  - Nếu chia nhỏ bảng thành từng dòng hoặc từng đoạn ngắn, mối quan hệ cấu trúc giữa tiêu đề cột và giá trị dòng sẽ bị đứt gãy hoàn toàn.
- **Nguyên lý phân tách hai tầng của Truy xuất Đa vector**:
  1. **Tầng chỉ mục tìm kiếm**: Dùng LLM sinh một bản tóm tắt súc tích giải thích nội dung, ý nghĩa của bảng biểu hoặc hình ảnh, sau đó chuyển bản tóm tắt này thành vector để lập chỉ mục trong CSDL vector.
  2. **Tầng kho lưu trữ gốc**: Lưu trữ trọn vẹn dữ liệu nguyên bản (bảng số liệu định dạng HTML hoặc Markdown nguyên vẹn, hoặc tệp hình ảnh độ phân giải cao) trong một kho dữ liệu tài liệu song song (Docstore), được liên kết bằng định danh ID duy nhất.
- **Quy trình truy xuất**: Khi người dùng đặt câu hỏi, hệ thống so khớp vector trên bản tóm tắt để định vị chính xác ID của bảng biểu, nhưng khi gửi ngữ cảnh cho LLM, hệ thống sẽ lấy dữ liệu bảng thô nguyên vẹn đưa vào prompt. Điều này bảo đảm LLM nhận được đầy đủ cấu trúc ma trận hàng-cột để thực hiện các phép suy luận logic và tính toán số học chuẩn xác.

```mermaid
flowchart TD
    subgraph Paradigm1["Trường phái 1: Nhúng Đa phương thức Đồng nhất (Google Gemini)"]
        MultiDoc1["Tài liệu đa phương thức (Văn bản + Hình ảnh)"] --> MultiEmb["Mô hình nhúng đa phương thức 1408 chiều"]
        MultiEmb --> JointSpace["Không gian vector đồng nhất 1408 chiều"]
        JointSpace --> CrossSearch["Tìm kiếm chéo: Chữ tìm ảnh, ảnh tìm chữ"]
        CrossSearch --> GeminiLLM["LLM đa phương thức: Nhận cả ảnh thô và văn bản"]
    end

    subgraph Paradigm2["Trường phái 2: Truy xuất Đa vector (Multi-Vector Retriever)"]
        RawContent["Dữ liệu bán cấu trúc: Bảng biểu thô + Ảnh gốc"] --> LLMSummary["LLM đa phương thức tạo bản tóm tắt văn bản"]
        LLMSummary --> SummaryEmb["Vector hóa bản tóm tắt làm chỉ mục tìm kiếm"]
        SummaryEmb -.->|Ánh xạ ID| DocStore["Kho lưu trữ dữ liệu nguyên bản"]
        DocStore --> HighPrecAns["Gửi bảng biểu và ảnh gốc nguyên vẹn cho LLM"]
    end
```

*Hình 2.6: Kiến trúc RAG Đa phương thức và cơ chế Truy xuất Đa vector cho dữ liệu bán cấu trúc*

#### 2.4.4. Khảo sát mở rộng RAG cho các định dạng nội dung tạo sinh khác (Zhao et al., 2024)
Bên cạnh văn bản và hình ảnh tĩnh, khảo sát toàn diện của Zhao et al. (2024) phân loại kiến trúc RAG theo bốn giai đoạn can thiệp tăng cường cốt lõi trong vòng đời sinh nội dung AIGC:
1. **Query-based RAG (Tăng cường tầng truy vấn)**: Tối ưu hóa câu hỏi hoặc ngữ cảnh đầu vào trước khi đưa vào mô hình, bao gồm các kỹ thuật viết lại câu lệnh (Query Rewriting), sinh văn bản giả định (HyDE), và mở rộng truy vấn đa chiều.
2. **Latent representation-based RAG (Tăng cường không gian ẩn)**: Bơm trực tiếp các vector biểu diễn tiềm ẩn của tài liệu truy xuất vào các tầng ẩn của mô hình ngôn ngữ thông qua cơ chế Cross-Attention, tiêu biểu như kiến trúc Fusion-in-Decoder (FiD - Izacard & Grave, 2021) và RETRO (Borgeaud et al., 2022).
3. **Logit-based RAG (Tăng cường tầng giải mã logit)**: Can thiệp trực tiếp vào phân phối xác suất token tại bước giải mã đầu ra, kết hợp phân phối softmax của mô hình ngôn ngữ với phân phối khoảng cách láng giềng gần nhất $k$NN trên kho ngữ liệu ngoài (như mô hình kNN-LM).
4. **Speculative RAG (Tăng cường suy đoán song song)**: Sử dụng một mô hình chuyên gia nhỏ gọn để tạo đồng thời nhiều bản nháp phản hồi dựa trên các tài liệu truy xuất độc lập, sau đó để mô hình lớn thẩm định và chọn lọc bản nháp tối ưu, vừa giảm độ trễ vừa nâng cao độ chính xác.

Ngoài ra, khảo sát của Zhao et al. (2024) còn mở rộng sang các miền dữ liệu chuyên biệt: RAG cho sinh mã nguồn (Code Generation), RAG cho hoạt họa và video (Video Diffusion), và RAG cho lưới đa giác mô hình 3D.

---

### 2.5. Khung Đánh giá Hiệu năng và Tiêu chuẩn Đo lường Khoa học

Đánh giá một hệ thống RAG đòi hỏi tách rời hai nguyên nhân độc lập: thất bại ở khâu truy xuất (không tìm thấy tài liệu) và thất bại ở khâu sinh (tìm đúng nhưng LLM đọc hiểu sai hoặc bịa đặt).

```mermaid
flowchart TD
    subgraph RET["ĐO LƯỜNG KHÂU TRUY XUẤT"]
        direction TB
        CP["<b>Chỉ số Context Precision</b><br/>Đo mức độ xếp hạng tài liệu phù hợp ở đầu danh sách"]
        CR["<b>Chỉ số Context Recall</b><br/>Đo tỷ lệ bao phủ dữ kiện cần thiết từ tài liệu chuẩn"]
        CP --> CR
    end

    subgraph GEN["ĐO LƯỜNG KHÂU SINH"]
        direction TB
        F["<b>Chỉ số Faithfulness</b><br/>Đo độ trung thực, kháng ảo giác từ ngữ cảnh truy xuất"]
        AR["<b>Chỉ số Answer Relevance</b><br/>Đo độ bám sát trọng tâm câu hỏi của người dùng"]
        F --> AR
    end

    RET <--> GEN
```

*Hình 2.7: Sơ đồ bốn trụ cột đo lường đánh giá của khung RAGAS*

#### 2.5.1. Khung đánh giá 4 trụ cột RAGAS (Es et al., 2023)
RAGAS là chuẩn mực học thuật phổ biến nhất để đo lường chất lượng hệ thống RAG mà không cần dữ liệu ground-truth do con người gắn nhãn:
1. **Độ trung thực Faithfulness**: Đo lường mức độ các câu khẳng định trong câu trả lời $A$ được suy ra trực tiếp từ ngữ cảnh $C$ nhằm kháng hiện tượng ảo giác:
   $$F(A, C) = \frac{|\{s \in S(A) : C \models s\}|}{|S(A)|}$$
   Trong đó $S(A)$ là tập các câu khẳng định đơn lẻ của câu trả lời. Điểm $1.0$ thể hiện 100% nội dung đều có căn cứ từ tài liệu.
2. **Độ liên quan Answer Relevance**: Đo mức độ bám sát câu hỏi $q$, tính bằng độ tương đồng Cosine giữa vector câu hỏi gốc và vector các câu hỏi được sinh ngược $q_i'$ từ câu trả lời $A$:
   $$AR(q, A) = \frac{1}{n} \sum_{i=1}^n \frac{E(q) \cdot E(q_i')}{\|E(q)\| \|E(q_i')\|}$$
3. **Độ chính xác ngữ cảnh Context Precision**: Đo mức độ các đoạn văn bản hữu ích được xếp hạng ở đầu danh sách top-$k$:
   $$\text{Context Precision@k} = \frac{\sum_{r=1}^k \text{Precision@}r \times v_r}{\sum_{r=1}^k v_r}$$
4. **Độ bao phủ ngữ cảnh Context Recall**: Đo tỷ lệ dữ kiện trong câu trả lời chuẩn xuất hiện trong tập ngữ cảnh $C$:
   $$CR = \frac{|\text{Dữ kiện trong Ground Truth xuất hiện trong } C|}{|\text{Tổng số dữ kiện trong Ground Truth}|}$$

#### 2.5.2. Khung đánh giá tự động ARES (Saad-Falcon et al., 2024)
ARES sử dụng LLM sinh dữ liệu tổng hợp để tinh chỉnh các bộ phân loại nhẹ (như DeBERTa), kết hợp mẫu nhỏ gán nhãn thủ công với kỹ thuật thống kê để tính toán khoảng tin cậy chính xác, giảm thiểu chi phí gọi API thương mại.

#### 2.5.3. Bộ tiêu chuẩn kiểm thử kháng ứng suất RGB (Chen et al., 2024)
RGB kiểm thử hệ thống RAG trên 4 kịch bản thách thức: (1) Khả năng chống nhiễu khi lẫn 80% tài liệu rác; (2) Khả năng từ chối trả lời khi không có thông tin; (3) Khả năng tích hợp dữ kiện từ nhiều tài liệu; (4) Khả năng chống tri thức phản thực tế có chủ đích.

---

### 2.6. Các Hướng Tiếp cận Đột phá Mới: GraphRAG và Agentic RAG

#### 2.6.1. GraphRAG: Kết hợp Đồ thị Tri thức và Vector Search (Microsoft Research, 2024)
Vector Search truyền thống giải quyết tốt câu hỏi cục bộ như: *"Ai là tác giả của bài báo X?"*, nhưng gặp khó khăn trước các câu hỏi tổng hợp toàn cục như: *"Các chủ đề chính trong kho tài liệu 10.000 trang này là gì?"*.

GraphRAG giải quyết điểm nghẽn này bằng cách dùng LLM trích xuất toàn bộ Thực thể và Mối quan hệ để xây dựng Đồ thị Tri thức, sau đó áp dụng giải thuật phân cụm cộng đồng Leiden để tóm tắt đồ thị từ dưới lên trên:

```mermaid
flowchart TD
    Raw["Tài liệu thô ban đầu"] --> Ext["Trích xuất Thực thể và Mối quan hệ"]
    Ext --> KG["Xây dựng Đồ thị Tri thức"]
    Ext --> Vec["Lập chỉ mục Vector"]
    
    KG --> Cluster["Phân cụm cộng đồng"]
    Cluster --> GlobSum["Tóm tắt toàn cục"]
    
    Vec --> LocalQA["Hỏi đáp cục bộ"]
    
    GlobSum --> Ans["CÂU TRẢ LỜI TOÀN DIỆN VÀ ĐA CHIỀU"]
    LocalQA --> Ans
```

*Hình 2.8: Sơ đồ quy trình kết hợp GraphRAG giữa đồ thị tri thức và vector*

#### 2.6.2. Agentic RAG: Tác tử Tự hành Đa bước
Thay vì một đường ống một chiều, Agentic RAG trao quyền cho một tác tử AI tự chủ: Tự lên kế hoạch giải quyết câu hỏi, gọi nhiều công cụ như cơ sở dữ liệu vector, SQL, API hoặc tìm kiếm internet, và lặp lại quá trình tìm kiếm nếu thông tin chưa đủ tin cậy.

#### 2.6.3. Chu trình tự phản chiếu trong Self-RAG
Khác với RAG thông thường luôn truy xuất thụ động, Self-RAG huấn luyện mô hình sinh ra các token phản chiếu để kiểm soát chu trình suy luận:

```mermaid
flowchart TD
    Q["Câu hỏi người dùng đầu vào"] --> Dec1{"Cần tra cứu tri thức ngoài?"}
    
    Dec1 -- "Không tra cứu" --> GenDirect["Sinh đáp án trực tiếp từ Bộ nhớ tham số"]
    Dec1 -- "Cần tra cứu" --> RetTopK["Truy xuất tập tài liệu liên quan"]
    
    RetTopK --> EvalRel{"Đánh giá độ liên quan từng tài liệu"}
    EvalRel -- "Tài liệu nhiễu" --> DropDoc["Loại bỏ tài liệu nhiễu"]
    EvalRel -- "Tài liệu đúng" --> GenStep["Sinh câu trả lời từng phân đoạn"]
    
    GenStep --> EvalSup{"Kiểm chứng tính trung thực"}
    EvalSup -- "Có căn cứ" --> EvalUse{"Chấm điểm mức độ hữu ích"}
    EvalSup -- "Không có căn cứ" --> WarnHalluc["Hiệu chỉnh và lọc bỏ ảo giác"]
    
    EvalUse --> FinalResp["CÂU TRẢ LỜI ĐẠT CHUẨN"]
```

*Hình 2.9: Sơ đồ chu trình tự phản chiếu trong kiến trúc Self-RAG*

Thực nghiệm công bố của Asai et al. (ICLR 2024, Bảng 2) chứng minh chu trình tự phản chiếu đem lại bước tiến vượt bậc về độ chính xác xác minh dữ kiện: Trên tập dữ liệu PubHealth, mô hình Self-RAG 7B đạt độ chính xác 72.4% và Self-RAG 13B đạt 74.5% (vượt trội đáng kể so với 43.7% của Llama2-chat 7B không truy xuất và 48.7% của mô hình Llama2-chat 7B có tăng cường truy xuất tiêu chuẩn). Trên tác vụ hỏi đáp PopQA, Self-RAG 7B đạt 54.9% và Self-RAG 13B đạt 55.8% (so với 29.2% của Llama2-chat 7B và 43.1% của Ret-Llama2-chat 7B). Đồng thời trên tác vụ viết tiểu sử dài (Biography), chỉ số FactScore đo độ chính xác dữ kiện của Self-RAG 7B đạt 76.3% (so với 52.6% của Llama2-7B) và Self-RAG 13B đạt 81.2% (so với 65.3% của Llama2-13B), khẳng định năng lực kiểm soát ảo giác hiệu quả.

---

### 2.7. Phân tích So sánh Chiến lược: RAG Đối chiếu với Long-Context LLMs

Trước sự xuất hiện của các mô hình ngôn ngữ lớn hỗ trợ cửa sổ ngữ cảnh mở rộng lên tới hàng trăm nghìn hoặc hàng triệu token (như Gemini 1.5 Pro, LLaMA-3.1), câu hỏi học thuật quan trọng được đặt ra trong cộng đồng nghiên cứu: *Liệu RAG có bị thay thế hoàn toàn bởi các mô hình có cửa sổ ngữ cảnh siêu dài?*

Các công trình thực nghiệm đối chứng gần đây của Li et al. (2024) và Xu et al. (2023) đã chỉ ra rằng hai cách tiếp cận này sở hữu những ưu thế và ranh giới kỹ thuật mang tính bổ trợ sâu sắc:

*Bảng 2.2: So sánh kỹ thuật đa chiều giữa Long-Context LLMs và Kiến trúc RAG*:

| Tiêu chí So sánh | Long-Context LLMs (Nhồi toàn bộ tài liệu vào Prompt) | Kiến trúc RAG (Truy xuất đoạn trích có chọn lọc) | Phân tích Học thuật và Thực nghiệm |
| :--- | :--- | :--- | :--- |
| **Chi phí Tính toán và Token** | Chi phí tăng theo chiều dài chuỗi; tuy nhiên các cơ chế Prompt Caching hiện đại giúp giảm đáng kể chi phí khi tái sử dụng tiền tố cố định | Tiết kiệm chi phí suy luận vì chỉ nạp các đoạn trích liên quan nhất (thường từ 2k–8k token) | RAG có lợi thế chi phí rõ rệt khi truy vấn trên kho tài liệu khổng lồ biến động liên tục |
| **Độ trễ Suy luận (Latency)** | Thời gian tạo token đầu tiên (TTFT) tăng tuyến tính theo độ dài ngữ cảnh ngữ liệu | Độ trễ truy vấn thấp và ổn định (đạt mức mili-giây với CSDL vector cục bộ) | RAG vượt trội về độ phản hồi nhanh trong các kịch bản tương tác thời gian thực |
| **Độ chính xác và Hiện tượng Nhiễu** | Dễ bị phân tâm hoặc suy giảm độ tập trung ở vùng giữa văn bản (Lost in the Middle) khi ngữ cảnh quá dài | Hạn chế nhiễu nhờ các tầng lọc và tái xếp hạng; nhưng phụ thuộc vào chất lượng truy xuất | Long-Context mạnh về tổng hợp liên tài liệu; RAG mạnh về trích xuất dữ kiện định vị |
| **Khả năng Quản trị và Bảo mật Dữ liệu** | Dữ liệu nạp nguyên khối vào prompt, khó phân quyền chi tiết theo từng người dùng | Quản trị quyền truy cập chặt chẽ tại tầng cơ sở dữ liệu vector thông qua siêu dữ liệu | RAG đáp ứng tốt hơn các yêu cầu bảo mật thông tin nội bộ của tổ chức |
| **Khả năng Cập nhật Tri thức** | Phải đọc lại toàn bộ tài liệu khi có dữ liệu mới phát sinh | Cập nhật tức thời thông qua việc nạp và lập chỉ mục bổ sung các vector mới | RAG linh hoạt vượt trội trong quản lý dữ liệu động |

*Kết luận học thuật*: Như Li et al. (2024) và Xu et al. (2023) đã chứng minh, Long-Context LLMs và RAG không triệt tiêu lẫn nhau mà hình thành mối quan hệ cộng sinh tối ưu: RAG đóng vai trò là tầng truy xuất động nhằm thu hẹp không gian dữ liệu hàng chục nghìn trang về tập tài liệu ứng viên có mật độ thông tin cao nhất, sau đó chuyển cho Long-Context LLMs thực hiện suy luận đa bước và tổng hợp ngữ nghĩa toàn diện.
"""
