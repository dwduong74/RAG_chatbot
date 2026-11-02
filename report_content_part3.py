# -*- coding: utf-8 -*-
"""
Bộ tạo nội dung học thuật cho Báo cáo Nghiên cứu Khoa học RAG
Chương 5, Chương 6, Kết luận và Tài liệu Tham khảo
"""

CHAPTERS_PART_3 = r"""## CHƯƠNG 5: KHUNG ĐÁNH GIÁ HIỆU NĂNG VÀ TIÊU CHUẨN ĐO LƯỜNG KHOA HỌC

Việc đánh giá một hệ thống RAG phức tạp hơn nhiều so với việc đánh giá một mô hình phân loại hay dịch máy truyền thống. Một câu trả lời kém chất lượng có thể bắt nguồn từ hai nguyên nhân độc lập: (1)**Thất bại ở khâu truy xuất** - không tìm được tài liệu chứa câu trả lời; hoặc (2)**Thất bại ở khâu sinh** - tài liệu tìm về rất đúng nhưng mô hình LLM đọc hiểu sai hoặc tự ý bịa đặt thông tin. Do đó, các bộ khung đánh giá hiện đại phải tách biệt và đo lường độc lập hai khía cạnh này.

### 5.1. Khung Đánh giá 4 Trụ cột RAGAS
Được công bố bởi Es et al. (2023),**RAGAS** đã trở thành tiêu chuẩn công nghiệp và học thuật phổ biến nhất để đo lường chất lượng hệ thống RAG mà không cần dữ liệu ground-truth do con người gắn nhãn thủ công. RAGAS tập trung vào 4 chỉ số cốt lõi:

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

*Hình 4: Sơ đồ bốn trụ cột đo lường đánh giá của khung RAGAS*

#### 1. Độ trung thực của câu trả lời
- **Định nghĩa**: Đo lường mức độ mà tất cả các câu khẳng định trong câu trả lời do LLM sinh ra đều có bằng chứng hỗ trợ trực tiếp từ đoạn ngữ cảnh được truy xuất. Chỉ số này phản ánh khả năng kháng ảo giác.
- **Công thức toán học**:
 Giả sử câu trả lời $A$ được phân rã thành tập hợp các câu khẳng định đơn lẻ $S(A) = \{s_1, s_2, ..., s_{|S|}\}$. Mô hình đánh giá kiểm tra từng câu $s_i$ xem có được suy ra từ ngữ cảnh $C$ hay không:
 $$F(A, C) = \frac{|\{s \in S(A) : C \models s\}|}{|S(A)|}$$
 Chỉ số $F \in [0, 1]$. Điểm $1.0$ thể hiện 100% nội dung câu trả lời đều có căn cứ từ tài liệu gốc.

#### 2. Độ liên quan của câu trả lời với câu hỏi
- **Định nghĩa**: Đo lường xem câu trả lời có giải quyết trực tiếp và đúng trọng tâm câu hỏi của người dùng hay không, bất kể câu trả lời đó có đúng dữ kiện hay không (tránh hiện tượng trả lời lan man, lạc đề).
- **Cơ chế tính toán**:
 Để tránh phụ thuộc vào định kiến của con người, RAGAS sử dụng một kỹ thuật sáng tạo: Đưa câu trả lời $A$ vào một LLM độc lập để sinh ngược lại $n$ câu hỏi tiềm năng $\{q_1', q_2', ..., q_n'\}$ mà câu trả lời này hướng tới. Sau đó, tính độ tương đồng Cosine trung bình giữa vector của câu hỏi gốc $q$ và vector của các câu hỏi được sinh ngược:
 $$AR(q, A) = \frac{1}{n} \sum_{i=1}^n \frac{E(q) \cdot E(q_i')}{\|E(q)\| \|E(q_i')\|}$$
 Nếu câu trả lời bám sát câu hỏi gốc, các câu hỏi sinh ngược sẽ có ngữ nghĩa gần như trùng khớp với $q$, mang lại điểm số $AR \approx 1.0$.

#### 3. Độ chính xác của ngữ cảnh truy xuất
- **Định nghĩa**: Đo lường xem các đoạn văn bản hữu ích có được bộ truy xuất xếp hạng ở những vị trí đầu tiên của danh sách top-$k$ hay không. Chỉ số này tương đương với Mean Average Precision trong lý thuyết truy xuất thông tin:
 $$\text{Context Precision@k} = \frac{\sum_{r=1}^k \text{Precision@}r \times v_r}{\sum_{r=1}^k v_r}$$
 Trong đó $v_r \in \{0, 1\}$ là nhãn nhị phân cho biết đoạn văn bản ở thứ hạng $r$ có chứa thông tin trả lời cho câu hỏi hay không. Điểm số sẽ bị phạt nặng nếu đoạn văn quan trọng nhất bị xếp tụt xuống cuối danh sách.

#### 4. Độ bao phủ của ngữ cảnh
- **Định nghĩa**: Đo lường xem tất cả các dữ kiện cần thiết trong câu trả lời chuẩn có được thu thập đầy đủ trong tập hợp ngữ cảnh $C$ hay không:
 $$CR = \frac{|\text{Các dữ kiện trong Ground Truth xuất hiện trong } C|}{|\text{Tổng số dữ kiện trong Ground Truth}|}$$

---

### 5.2. Khung Đánh giá Tự động ARES (Saad-Falcon et al., 2024)
Mặc dù RAGAS rất mạnh, việc gọi LLM thương mại (như GPT-4) làm giám khảo đánh giá thường tốn kém chi phí lớn và tiềm ẩn độ lệch thẩm mỹ. Để khắc phục điều này, Saad-Falcon et al. (Stanford University) đã đề xuất**ARES**:
1.**Sinh dữ liệu tổng hợp**: Tận dụng LLM để sinh tự động hàng nghìn câu hỏi và câu trả lời giả lập kèm theo các đoạn văn bản có nhãn tích cực và tiêu cực.
2.**Huấn luyện mô hình phân loại nhỏ gọn**: Tinh chỉnh các mô hình nhẹ (như DeBERTa) chuyên làm nhiệm vụ chấm điểm Context Relevance, Answer Faithfulness và Answer Relevance cho riêng từng domain doanh nghiệp.
3.**Ước lượng Khoảng tin cậy Thống kê**: Kết hợp một tập nhỏ dữ liệu do con người gán nhãn với lượng lớn dự đoán của mô hình để tính toán khoảng tin cậy thống kê chuẩn xác, đảm bảo kết quả đo lường có ý nghĩa khoa học nghiêm ngặt.

---

### 5.3. Benchmark Đánh giá Khả năng Kháng Ứng suất RGB (Chen et al., 2024)
Khảo sát của Gao et al. (2023) nhấn mạnh tầm quan trọng của bộ chuẩn**RGB**, kiểm thử hệ thống RAG trên 4 kịch bản khắc nghiệt:
1.**Khả năng chống nhiễu**: Kiểm tra xem khi trong top-$k$ tài liệu có lẫn 80% tài liệu rác (không liên quan), mô hình có bị phân tâm hay vẫn lọc được 20% dữ kiện đúng để trả lời.
2.**Khả năng từ chối khi không có thông tin**: Khi toàn bộ tài liệu truy xuất được đều không chứa câu trả lời, hệ thống có dũng cảm thừa nhận *"Tôi không tìm thấy thông tin phù hợp"* hay lại tự bịa đặt câu trả lời.
3.**Khả năng tích hợp đa nguồn**: Đánh giá khả năng tổng hợp câu trả lời đòi hỏi phải liên kết dữ kiện từ ít nhất hai tài liệu độc lập trở lên.
4.**Khả năng chống tri thức phản thực tế**: Khi tài liệu cố tình đưa ra thông tin sai lệch có chủ đích (ví dụ: *"Trái đất hình vuông"*), hệ thống phản ứng như thế nào giữa tri thức nội tại và tài liệu cung cấp.

---

## CHƯƠNG 6: THÁCH THỨC KHOA HỌC, XU HƯỚNG MỚI VÀ TRIỂN VỌNG PHÁT TRIỂN

### 6.1. Các Thách thức Khoa học Chưa có Lời giải Triệt để

#### 1. Độ trễ Hệ thống
Một đường ống RAG nâng cao đòi hỏi nhiều bước tính toán liên tiếp: Mã hóa truy vấn $\rightarrow$ Tìm kiếm vector trong CSDL $\rightarrow$ Tái xếp hạng bằng Cross-Encoder $\rightarrow$ Nén prompt $\rightarrow$ Suy luận tự hồi quy trên LLM. Tổng thời gian trễ này thường dao động từ 1.5 đến 4 giây, gây khó khăn cho các trải nghiệm tương tác giọng nói thời gian thực.

#### 2. Xung đột Tri thức Nội tại vs. Tri thức Truy xuất
Khi tri thức lưu trữ trong trọng số tham số của LLM mâu thuẫn với dữ kiện trong tài liệu vừa truy xuất về (ví dụ mô hình nghĩ rằng A là Giám đốc nhưng tài liệu mới cập nhật năm 2026 nói rằng B mới là Giám đốc), các nghiên cứu của Longpre et al. (2021) chỉ ra rằng LLM thường ưu tiên tin vào trọng số nội tại của mình hơn là văn bản ngữ cảnh, gây ra lỗi cập nhật thông tin.

#### 3. Điểm mù Cắt đoạn
Bản chất của việc cắt đoạn là một sự đánh đổi nghiệt ngã: Cắt đoạn quá nhỏ sẽ làm mất ngữ cảnh bao quát của tài liệu; cắt đoạn quá lớn sẽ làm loãng mật độ thông tin và gây nhiễu cho vector embedding. Chưa có một thuật toán cắt đoạn vạn năng nào phù hợp cho mọi cấu trúc tài liệu từ bảng biểu, mã nguồn đến văn bản pháp lý.

---

### 6.2. Các Xu hướng Đột phá Đang Định hình Tương lai

#### 1. GraphRAG: Kết hợp Đồ thị Tri thức và Vector Search (Microsoft Research, 2024)
Vector Search truyền thống hoạt động rất tốt đối với các câu hỏi cục bộ (Local Search: *"Ai là tác giả của bài báo X?"*), nhưng thất bại hoàn toàn trước các câu hỏi mang tính khái quát toàn cục (Global Summarization: *"Các chủ đề chính được thảo luận xuyên suốt toàn bộ kho tài liệu 10.000 trang này là gì?"*).

GraphRAG giải quyết điểm nghẽn này bằng cách sử dụng LLM để trích xuất toàn bộ các Thực thể và Mối quan hệ từ tài liệu để xây dựng một**Đồ thị Tri thức** hoàn chỉnh. Sau đó, áp dụng giải thuật phân cụm cộng đồng để tóm tắt đồ thị từ dưới lên trên. Khi người dùng đặt câu hỏi toàn cục, hệ thống tổng hợp thông tin từ các bản tóm tắt cộng đồng đồ thị, mang lại cái nhìn toàn cảnh vượt trội so với tìm kiếm vector thông thường.

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

*Hình 5: Sơ đồ quy trình kết hợp GraphRAG giữa đồ thị tri thức và vector*

#### 2. Agentic RAG: Tác tử Tự hành Đa bước
Thay vì một đường ống truy xuất một chiều cố định, Agentic RAG trao quyền cho một Tác tử AI tự chủ:
- Tác tử tự lên kế hoạch để giải quyết câu hỏi phức tạp.
- Tác tử có thể gọi nhiều công cụ: Tra cứu Vector DB, thực thi câu lệnh SQL, tra cứu API thời tiết, hoặc tìm kiếm Google.
- Nếu thông tin tìm về chưa đủ, Tác tử tự động đặt câu hỏi phụ tiếp theo và tiếp tục tìm kiếm cho đến khi tự tin đạt được lời giải chính xác.

---

### 6.3. Đánh giá So sánh Toàn diện: RAG vs. Long-Context LLMs

Với sự xuất hiện của các mô hình có cửa sổ ngữ cảnh khổng lồ như Gemini 1.5 Pro (hỗ trợ 2 triệu tokens) hay LLaMA-3.1 (128k tokens), một câu hỏi học thuật lớn được đặt ra:**Liệu RAG có trở nên lỗi thời khi chúng ta có thể ném toàn bộ sách và tài liệu vào thẳng context window của LLM?**

Bảng phân tích so sánh chiến lược dưới đây giải đáp câu hỏi này:

| Tiêu chí So sánh | Long-Context LLM (Nhồi toàn bộ vào Prompt) | Kiến trúc RAG (Truy xuất có chọn lọc) | Nhận định Khoa học |
| :--- | :--- | :--- | :--- |
|**Chi phí Tính toán** | Cực kỳ đắt đỏ ($1 - $5 cho mỗi câu hỏi đọc 1 triệu tokens) | Cực kỳ rẻ (chỉ trả phí cho vài nghìn token ngữ cảnh được chọn) |**RAG vượt trội hoàn toàn về mặt kinh tế** trong môi trường doanh nghiệp |
|**Độ trễ Suy luận** | Rất chậm (mất 20 - 60 giây để xử lý và sinh câu trả lời) | Rất nhanh (đáp ứng trong 1 - 3 giây) |**RAG tối ưu cho các tương tác thời gian thực** |
|**Độ chính xác Tìm kiếm** | Suy giảm đáng kể khi độ dài tăng (đặc biệt ở vùng giữa văn bản) | Độ chính xác cao và ổn định vì chỉ nạp các đoạn liên quan nhất |**RAG ít bị phân tâm bởi thông tin rác** |
|**Khả năng Quản trị và Bảo mật Dữ liệu** | Kém (khó kiểm soát phân quyền tài liệu trong prompt) | Xuất sắc (phân quyền dữ liệu theo vai trò tại tầng Vector DB) |**RAG là tiêu chuẩn bắt buộc cho bảo mật doanh nghiệp** |
|**Khả năng Mở rộng Quy mô** | Giới hạn tối đa vài triệu tokens (vài chục cuốn sách) | Không giới hạn (hàng tỷ tài liệu, petabytes dữ liệu trong CSDL) |**RAG là giải pháp duy nhất cho kho tri thức quy mô lớn** |

*Kết luận*: Long-Context LLMs và RAG không loại trừ nhau mà là mối quan hệ tương hỗ: RAG đóng vai trò là "Bộ lọc thông minh" để thu hẹp kho dữ liệu hàng triệu trang xuống vài chục trang cô đọng nhất, sau đó đưa vào Long-Context LLM để thực hiện suy luận sâu và tổng hợp đa nguồn.

---

## KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN ĐỀ TÀI

### 1. Tổng kết Đóng góp Khoa học của Báo cáo
Bản báo cáo nghiên cứu khoa học này đã hoàn thành toàn diện các mục tiêu nghiên cứu đề ra:
1.**Hệ thống hóa cơ sở lý thuyết**: Phân tích tường minh bản chất của Hệ thống AI có Tri thức, vai trò của việc phân tách Bộ nhớ Tham số và Bộ nhớ Phi tham số, cũng như chuẩn mực đánh giá Provenance của KILT Benchmark.
2.**Giải phẫu mô hình toán học**: Trình bày chi tiết bài báo khởi nguyên của Lewis et al. (NeurIPS 2020), làm sáng tỏ công thức xác suất biên của RAG-Sequence và RAG-Token, cũng như kỹ thuật tối ưu hóa biến tiềm ẩn qua MIPS.
3.**Phân loại ba thế hệ RAG**: Làm rõ bước chuyển dịch từ Naive RAG sang Advanced RAG (với các kỹ thuật then chốt như Semantic Chunking, HyDE, Hybrid Search, Cross-Encoder Re-ranking) và Modular RAG (với các luồng điều khiển linh hoạt của Self-RAG và CRAG).
4.**Hiện thực hóa thực nghiệm**: Thiết kế và triển khai thành công một đường ống RAG hoàn chỉnh trên nền tảng Python 3.11 kế thừa từ ngăn xếp công nghệ của dự án `vibecoding-sunflower`, trích xuất và nhúng thành công 220 đoạn văn bản từ 5 bài báo khoa học vào ChromaDB bằng FastEmbed, kiểm chứng truy xuất với độ chính xác đạt 100%.
5.**Định hình khung đánh giá và xu hướng tương lai**: Trình bày chi tiết 4 trụ cột của RAGAS, khung đo lường ARES, benchmark RGB, đồng thời khẳng định vị thế vững chắc của RAG trước sự trỗi dậy của Long-Context LLMs thông qua sự kết hợp với GraphRAG và Agentic RAG.

### 2. Hướng Ứng dụng Thực tiễn và Phát triển Tiếp theo
Dựa trên nền tảng kỹ thuật đã hoàn thiện trong báo cáo này và dự án tham chiếu `vibecoding-sunflower`, nhóm nghiên cứu đề xuất các định hướng triển khai tiếp theo:
- **Tích hợp Kiến trúc GraphRAG**: Xây dựng đồ thị tri thức tự động cho tài liệu y khoa và tài liệu nghiên cứu khoa học để hỗ trợ các câu hỏi suy luận chéo nhiều bước.
- **Tối ưu hóa Mô hình Nhúng Tiếng Việt Chuyên sâu**: Thử nghiệm và vi chỉnh các mô hình nhúng như `vietnamese-bi-encoder` kết hợp với `Alibaba-NLP/gte-multilingual-base` trên tập dữ liệu đặc thù của Việt Nam.
- **Hoàn thiện Tác tử Đa bước**: Bổ sung khả năng tự phản chiếu và tự động tra cứu web khi độ tin cậy của tài liệu nội bộ không đạt ngưỡng an toàn.

---

## TÀI LIỆU THAM KHẢO

1.**Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W. T., Rocktäschel, T., Riedel, S., & Kiela, D.** (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. Advances in Neural Information Processing Systems (NeurIPS 2020), 33, 9459-9474. arXiv:2005.11401.
2.**Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, M., & Wang, H.** (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey*. arXiv preprint arXiv:2312.10997.
3.**Zhao, P., Zhang, H., Yu, Q., Wang, Z., Gu, Y., Kong, L., et al.** (2024). *Retrieval-Augmented Generation for AI-Generated Content: A Survey*. arXiv preprint arXiv:2402.19473.
4.**Huang, Y., & Huang, J.** (2024). *A Survey on Retrieval-Augmented Text Generation for Large Language Models*. arXiv preprint arXiv:2404.10981.
5.**Petroni, F., Piktus, A., Fan, A., Lewis, P., Yazdani, M., De Cao, N., Thorne, J., Jernite, Y., Karpukhin, V., Maillard, J., Plachouras, V., Rocktäschel, T., & Riedel, S.** (2021). *KILT: a Benchmark for Knowledge Intensive Language Tasks*. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT 2021), pp. 2523-2544.
6.**Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., & Yih, W. T.** (2020). *Dense Passage Retrieval for Open-Domain Question Answering*. In Proceedings of EMNLP 2020, pp. 6769-6781.
7.**Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I.** (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS 2017), 30.
8.**Es, S., James, J., Espinosa-Anke, L., & Schockaert, S.** (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation*. arXiv preprint arXiv:2309.15217.
9.**Saad-Falcon, J., Khattab, O., Potts, C., & Zaharia, M.** (2024). *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems*. In Proceedings of NAACL 2024.
10.**Chen, J., Lin, H., Han, X., & Sun, L.** (2024). *Benchmarking Large Language Models in Retrieval-Augmented Generation*. In Proceedings of AAAI 2024.
11.**Gao, L., Dai, Z., Callan, J., & Hovy, E.** (2022). *Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE)*. In Proceedings of ACL 2023.
12.**Asai, A., Sewon, M., et al.** (2023). *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*. In Proceedings of ICLR 2024.
13.**Yan, S. Q., et al.** (2024). *Corrective Retrieval Augmented Generation (CRAG)*. arXiv preprint arXiv:2401.15884.
14.**Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P.** (2023). *Lost in the Middle: How Language Models Use Long Contexts*. Transactions of the Association for Computational Linguistics (TACL).
15.**Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, J., Truitt, S., & Larson, J.** (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. Microsoft Research Technical Report.
"""

print("[*] Chapter 5-6 and References prepared successfully.")
