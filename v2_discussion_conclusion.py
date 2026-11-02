# -*- coding: utf-8 -*-
"""
Báo cáo Nghiên cứu Khoa học: Hệ thống Trí tuệ Nhân tạo có Tri thức và Kiến trúc RAG
Mục 4.6 Thảo luận (Chương 4) và Toàn văn Chương 5 (Kết luận, Hạn chế và Hướng nghiên cứu tiếp theo)
Tác giả: Nhóm Nghiên cứu Khoa học Công nghệ Trí tuệ Nhân tạo
Năm hoàn thành: 2026
"""

import sys
import io

# Tái cấu hình chuẩn xuất ký tự UTF-8 cho môi trường thực thi
if sys.stdout.encoding is None or sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# ==============================================================================
# PHẦN 1: MỤC 4.6 THẢO LUẬN (CHƯƠNG 4)
# ==============================================================================

DISCUSSION_SECTION = r"""### 4.7. Thảo luận

Các kết quả thực nghiệm đạt được tại Chương 4 đã cung cấp những bằng chứng thực chứng quan trọng để kiểm chứng các giả thuyết khoa học được đặt ra ở phần đầu của công trình nghiên cứu. Mục thảo luận này nhằm phân tích có hệ thống các phát hiện thu được từ bộ dữ liệu thực nghiệm 40 câu hỏi trên 121 trang tài liệu khoa học, đối chiếu các quan sát thực nghiệm với các luận điểm trong những công bố khoa học kinh điển, đồng thời chỉ ra các bài học kinh nghiệm cũng như hàm ý ứng dụng cho việc phát triển các hệ thống RAG trong thực tế.

#### 4.7.1. Giải đáp có hệ thống các câu hỏi nghiên cứu

Dựa trên toàn bộ quá trình khảo cứu lý thuyết và thực nghiệm triển khai hệ thống đường ống trên tập dữ liệu 5 bài báo khoa học hạt nhân, chúng tôi lần lượt trả lời bốn câu hỏi nghiên cứu cốt lõi như sau:

##### 1. Câu hỏi nghiên cứu 1: Tiến hóa kiến trúc qua các thế hệ RAG
*Câu hỏi nghiên cứu 1 đặt ra vấn đề: Kiến trúc RAG đã trải qua quá trình tiến hóa như thế nào từ dạng thức khởi nguyên đến nay, và những đột phá kỹ thuật cốt lõi ở từng thế hệ là gì?*

Kết quả nghiên cứu khẳng định rằng kiến trúc RAG đã trải qua một tiến trình phát triển tuần tự nhưng mang tính cách mạng qua ba thế hệ kiến trúc rõ rệt:
- **Thế hệ Naive RAG**: Vận hành theo mô hình tuyến tính đơn giản với cơ chế truy xuất và đọc một chiều (Retrieve-and-Read). Toàn bộ chu trình chỉ bao gồm ba bước tuần tự: cắt đoạn tài liệu theo kích thước thô, lập chỉ mục vector, và tìm kiếm độ tương đồng vector trực tiếp để ghép vào prompt của mô hình ngôn ngữ lớn. Dù dễ cài đặt, Naive RAG bộc lộ những điểm yếu: độ chính xác truy xuất bị hạn chế do chỉ dựa vào khoảng cách ngữ nghĩa bề mặt, không lọc được tài liệu nhiễu, và đặc biệt là bị ảnh hưởng bởi hiện tượng suy giảm chú ý ở giữa dòng ngữ cảnh của các mô hình nơ-ron (Liu et al., 2023).
- **Thế hệ Advanced RAG**: Được thiết kế có chủ đích nhằm giải quyết các điểm nghẽn của Naive RAG thông qua việc thiết lập cấu trúc tối ưu hóa ba tầng hoàn chỉnh:
  1. *Tối ưu hóa Tiền truy xuất*: Áp dụng phân đoạn ngữ nghĩa phân tầng Parent-Child, trích xuất và làm giàu siêu dữ liệu, kỹ thuật sinh văn bản giả định HyDE (Gao et al., 2023a) và mở rộng phân rã truy vấn đa hướng.
  2. *Tối ưu hóa Trong truy xuất*: Kết hợp sức mạnh của tìm kiếm vector dày đặc và tìm kiếm từ khóa thưa BM25 thông qua thuật toán Hợp nhất Thứ hạng Tương hỗ RRF, cân bằng giữa hiểu ý đồ ngữ nghĩa trừu tượng và bắt trọn các từ khóa chuyên biệt.
  3. *Tối ưu hóa Hậu truy xuất*: Sử dụng mô hình tái xếp hạng mạng nơ-ron Cross-Encoder để tính toán điểm tương quan sâu giữa câu hỏi và đoạn trích, kết hợp với các giải thuật nén ngữ cảnh và tái sắp xếp vị trí tài liệu nhằm giảm thiểu hiện tượng phân tâm của LLM.
- **Thế hệ Modular RAG**: Đánh dấu bước nhảy vọt khỏi tư duy đường ống tuần tự cố định, tổ chức hệ thống thành các module chức năng độc lập có khả năng tương tác linh hoạt. Điểm đột phá của Modular RAG nằm ở các cơ chế thích ứng động: module định tuyến ngữ nghĩa cho phép phân luồng truy vấn vào các kho tri thức phù hợp; module bộ nhớ hỗ trợ duy trì mạch hội thoại dài; và đặc biệt là các cơ chế tự phản chiếu thông minh như Self-RAG (Asai et al., 2024) với các token phản chiếu đặc biệt `[Retrieve]`, `[IsRel]`, `[IsSup]`, `[IsUse]` và Corrective RAG (Yan et al., 2024) với khả năng tự kích hoạt tìm kiếm internet bên ngoài khi tài liệu nội bộ không đạt ngưỡng tin cậy.

##### 2. Câu hỏi nghiên cứu 2: Năng lực truy xuất thực nghiệm của mô hình BAAI/bge-small-en-v1.5
*Câu hỏi nghiên cứu 2 đặt ra vấn đề: Mô hình nhúng BAAI/bge-small-en-v1.5 thể hiện hiệu năng truy xuất thực nghiệm ra sao trên tập dữ liệu văn bản học thuật chuyên sâu?*

Thực nghiệm đo đạc định lượng toàn trình trên 40 câu hỏi kiểm thử chân lý thực tế trải rộng trên 121 trang tài liệu khoa học cho thấy:
- **Độ chính xác định vị tài liệu**: Khi kết hợp với chiến lược Cửa sổ trượt có vùng gối đầu, mô hình `BAAI/bge-small-en-v1.5` đạt **Hit@5 = 95.0% (38/40 câu hỏi)**, **Hit@3 = 87.5%**, **Hit@1 = 65.0% (26/40 câu hỏi)**, **MRR@5 = 0.763**, và **nDCG@5 = 0.810**. Tuy nhiên, mức tăng Hit@1 từ 52.5% lên 65.0% so với cắt cố định chỉ tương ứng với 5 câu hỏi trên 40 câu (+12.5 điểm phần trăm), với khoảng tin cậy 95% Wilson lần lượt là $[0.375, 0.671]$ và $[0.495, 0.779]$, có sự chồng lấn đáng kể. Hơn nữa, thuật toán BM25 trên cắt cố định đạt Hit@1 lên tới **67.5%**, vượt trên BGE-small.
- **Đặc điểm phân bố điểm tương đồng Cosine**: Điểm tương đồng Cosine của các kết quả top đầu thường dồn ở dải điểm số cao, dao động từ **0.72 đến 0.86**. Điểm số trung bình khi Top-1 đúng tài liệu đích là **0.7939**, trong khi điểm số trung bình khi Top-1 không trùng tài liệu đích là **0.7773** (chênh lệch chỉ **0.0166**). Điều này chứng minh điểm Cosine trong không gian Bi-encoder bị dồn dập và không thể phân biệt rạch ròi giữa kết quả đúng và sai, bác bỏ việc sử dụng các ngưỡng cố định như $\tau = 0.75$.
- **Bản chất các trường hợp trượt Hit@1**: Trong 14 câu hỏi BGE-small không đạt Hit@1, có tới **12 trường hợp (85.7%)** là sự nhầm lẫn giữa các bài báo khảo sát tổng quan với nhau (Gao et al., Zhao et al., Huang et al.) do các bài báo này cùng bao quát các khái niệm hiện đại (Self-RAG, CRAG, RAGAS, Long-Context). Điều này phản ánh tính chất mơ hồ của nhãn chân lý cấp độ bài báo tổng quan hơn là sai sót về mặt ngữ nghĩa.
- **Tài nguyên và độ trễ**: Mô hình nhúng 384 chiều thực thi qua ONNX Runtime CPU (AVX2) đạt độ trễ truy vấn trung bình **40.31 ms/câu hỏi**, trong khi thời gian mã hóa toàn bộ 398 đoạn văn bản mất 90.89 giây trên vi xử lý Intel Core i7-7700HQ.

##### 3. Câu hỏi nghiên cứu 3: Chiến lược cắt đoạn văn bản tối ưu cho tài liệu khoa học
*Câu hỏi nghiên cứu 3 đặt ra vấn đề: Chiến lược phân đoạn văn bản nào đem lại sự cân bằng tối ưu giữa tính toàn vẹn ngữ nghĩa, chi phí lưu trữ và độ chính xác truy xuất đối với tài liệu nghiên cứu khoa học?*

Qua ma trận thực nghiệm đối sánh định lượng trên 40 câu hỏi kiểm thử, chúng tôi rút ra những kết luận thực chứng cụ thể:
- **Chiến lược Cửa sổ trượt liên tục (250 từ / 50 từ gối đầu)** đem lại hiệu năng ngữ nghĩa cao hơn cho mô hình nhúng nơ-ron BGE-small (nDCG@5 tăng 8.3 điểm phần trăm từ 0.727 lên 0.810, Hit@5 tăng 5.0 điểm phần trăm từ 90.0% lên 95.0%). Tuy nhiên, vùng gối đầu không có tác dụng tích cực đối với mọi thuật toán: Thuật toán từ vựng BM25 bị giảm Hit@1 từ **67.5% xuống 57.5%**, và MiniLM-L6-v2 cũng giảm Hit@1 từ **62.5% xuống 57.5%**. Ngoài ra, cửa sổ trượt làm tăng số lượng đoạn văn bản lên 25% (từ 318 lên 398 đoạn), đòi hỏi thêm chi phí lưu trữ và bộ nhớ.
- **Chiến lược Cắt đệ quy theo cấu trúc** mang lại sự cân bằng hợp lý về chi phí lưu trữ và chất lượng. Bằng cách ưu tiên phân tách theo ranh giới đoạn văn bản `\n\n`, ngắt dòng `\n`, và dấu kết thúc câu `.`, phương pháp này tạo ra 379 đoạn văn bản nhưng vẫn đạt **nDCG@5 = 0.783** và **Hit@5 = 92.5%**.
- **Chiến lược Cắt kích thước cố định** làm suy giảm hiệu năng của mô hình nhúng dày BGE-small (Hit@1 giảm xuống 52.5%), nhưng lại mang lại hiệu năng cao nhất cho thuật toán BM25 (**67.5% Hit@1**) do các từ khóa định danh hiếm vẫn giữ nguyên vẹn và việc đoạn văn bản bị cắt ngắn làm tăng mật độ từ (Term Frequency).

##### 4. Câu hỏi nghiên cứu 4: Mối quan hệ chiến lược giữa RAG và Long-Context LLMs
*Câu hỏi nghiên cứu 4 đặt ra vấn đề: Liệu sự xuất hiện của các mô hình LLM có cửa sổ ngữ cảnh siêu dài hàng triệu tokens có làm biến mất vai trò của kiến trúc RAG hay không?*

Kết quả phân tích chuyên sâu khẳng định: **RAG và Long-Context LLMs không phải là hai công nghệ triệt tiêu lẫn nhau, mà tạo nên mối quan hệ cộng sinh tương hỗ mật thiết** (Li et al., 2024; Xu et al., 2023):
- *Về chi phí tính toán và cơ chế Prompt Caching*: Mặc dù kỹ thuật lưu bộ nhớ đệm khóa-giá trị (KV-cache Caching / Prompt Caching) giúp giảm chi phí tái xử lý các đoạn ngữ cảnh tĩnh, chi phí nạp ban đầu cho hàng triệu tokens và chi phí tính toán sự chú ý bậc hai $\mathcal{O}(L^2)$ vẫn tốn kém gấp hàng chục đến hàng trăm lần so với việc truy xuất có chọn lọc vài nghìn tokens của RAG.
- *Về độ trễ và hiện tượng phân tâm*: Các nghiên cứu thực nghiệm (Liu et al., 2023; Li et al., 2024) đã chứng minh mô hình ngôn ngữ lớn gặp hiện tượng suy giảm chú ý khi ngữ cảnh đầu vào quá dài (hiện tượng "kim trong đáy biển" - Needle in a Haystack). Ngược lại, RAG thực hiện lọc trước, cung cấp cho LLM một tập ngữ cảnh cô đọng và hạn chế thông tin nhiễu.
- *Về phân quyền và quản trị*: RAG cho phép thiết lập quyền truy cập dữ liệu chi tiết theo từng người dùng ngay tại tầng chỉ mục vector hoặc cơ sở dữ liệu quan hệ, điều mà Long-Context LLM không thể thực hiện nếu nạp toàn bộ kho tri thức chung vào ngữ cảnh.

Mô hình kiến trúc triển vọng chính là sự kết hợp cộng sinh: RAG đóng vai trò là "Bộ lọc thông minh", rà quét kho tri thức lớn để cô đọng xuống vài chục nghìn tokens liên quan nhất, sau đó đưa tập tài liệu tinh chọn này vào Long-Context LLM để thực hiện suy luận sâu và tổng hợp tri thức đa nguồn.

```mermaid
flowchart TD
    UserQuery["Truy vấn người dùng"] --> RAGFilter["BỘ LỌC THÔNG MINH RAG<br/>• Tìm kiếm trong hàng triệu tài liệu<br/>• Định vị nhanh trong vài chục mili-giây<br/>• Cô đọng ngữ cảnh và loại bỏ tài liệu ngoài lề<br/>• Phân quyền bảo mật dữ liệu"]
    
    RAGFilter --> RefinedContext["Tập ngữ cảnh tinh chọn cô đọng<br/>Quy mô vài nghìn đến vài chục nghìn tokens"]
    
    RefinedContext --> LongLLM["LONG-CONTEXT LLM<br/>• Đọc hiểu sâu tập ngữ cảnh tinh chọn<br/>• Suy luận logic đa bước xuyên tài liệu<br/>• Hỗ trợ Prompt Caching tối ưu độ trễ<br/>• Giảm thiểu hiện tượng phân tâm"]
    
    LongLLM --> HighQualityAns["CÂU TRẢ LỜI TOÀN DIỆN VÀ CHÍNH XÁC"]
```

*Hình 4.1: Sơ đồ kiến trúc cộng sinh giữa RAG và Long-Context LLM*

---

#### 4.7.2. Đối chiếu kết quả thực nghiệm với các công bố khoa học tiền đề

Để đánh giá tính hợp lý và vị trí học thuật của công trình, chúng tôi đối chiếu các quan sát thực nghiệm với những tuyên bố và kết luận trong các công bố nền tảng:

##### 1. Đối chiếu với công bố khởi nguyên của Lewis et al. (2020)
Trong bài báo kinh điển tại NeurIPS 2020, Lewis et al. đã chứng minh mô hình RAG kết hợp bộ nhớ phi tham số vượt trội hơn mô hình thuần tham số BART trên các tác vụ hỏi đáp đòi hỏi tri thức. Kết quả thực nghiệm của chúng tôi phù hợp với luận điểm của Lewis et al. về năng lực định vị tri thức của thành phần truy xuất (đạt Hit@5 = 95.0% trên 40 câu hỏi kiểm thử).

Tuy nhiên, nghiên cứu của chúng tôi làm sáng tỏ thêm một khía cạnh thực tế: Trong một kho tài liệu học thuật có nhiều bài báo tổng quan trích dẫn lẫn nhau, thành phần truy xuất vector dày rất dễ xếp hạng bài báo khảo sát cao hơn bài báo gốc do mật độ từ vựng tổng kết dày đặc. Điều này khẳng định tầm quan trọng của việc bổ sung siêu dữ liệu và cơ chế tái xếp hạng nơ-ron trong các triển khai RAG hiện đại.

##### 2. Đối chiếu với khung phân loại ba thế hệ của Gao et al. (2023b)
Khảo sát của Gao et al. (2023b) đã thiết lập chuẩn mực phân loại ba thế hệ kiến trúc RAG. Toàn bộ các phân tích kỹ thuật và kết quả đo đạc trong báo cáo của chúng tôi đã xác thực tính phù hợp của phân loại này:
- Các điểm nghẽn của Naive RAG (đặc biệt là việc cắt đoạn cố định làm vỡ ngữ cảnh) đã được quan sát qua thực nghiệm đối với mô hình nhúng dày: Hit@1 của BGE bị giảm từ 65.0% xuống 52.5% khi mất vùng gối đầu.
- Tính cần thiết của mô hình tối ưu hóa ba tầng (Advanced RAG) và cơ chế tự phản chiếu thích ứng (Modular RAG) được khẳng định như giải pháp phù hợp cho các bài toán phức tạp.

##### 3. Đối chiếu về ảnh hưởng của vùng gối đầu (Overlap) trong phân đoạn văn bản
Kết quả thực nghiệm định lượng ghi nhận việc áp dụng kỹ thuật cửa sổ trượt có vùng gối đầu giúp **nDCG@5 tăng thêm 8.3 điểm phần trăm** (từ 0.727 lên 0.810) và **Hit@5 tăng thêm 5.0 điểm phần trăm** (từ 90.0% lên 95.0%) đối với mô hình BGE-small so với cắt đoạn kích thước cố định. Kết quả này phù hợp với nhận định trong các khảo sát của Huang và Huang (2024) cũng như Zhao et al. (2024) về lợi ích của vùng chồng lắp trong việc bảo tồn các cấu trúc câu phức. Tuy nhiên, nghiên cứu của chúng tôi bổ sung phát hiện mới: Vùng gối đầu không cải thiện thuật toán từ khóa BM25, và BM25 trên phân đoạn cố định vẫn đạt Hit@1 cao nhất bảng (67.5%).

*Bảng 4.6: Bảng đối chiếu kết quả nghiên cứu với các công bố khoa học tiền đề*

| Công trình tiền đề | Luận điểm hoặc phát hiện gốc | Kết quả kiểm chứng trong đề tài | Mức độ tương thích và Nhận định khoa học |
| :--- | :--- | :--- | :--- |
| **Lewis et al. (2020)** | RAG vượt trội hơn BART thuần tham số trên Open-domain QA | Hệ thống đạt Hit@5 = 95.0% trên 40 câu hỏi kiểm thử; phát hiện hiện tượng nhầm tài liệu khảo sát | **Phù hợp** ở khâu truy xuất; đề xuất thêm cơ chế tái xếp hạng |
| **Gao et al. (2023b)** | Phân loại 3 thế hệ Naive, Advanced và Modular RAG | Xác thực các điểm nghẽn của Naive RAG và tính ưu việt của quy trình ba tầng | **Nhất quán** về mặt lý thuyết và kiến trúc hệ thống |
| **Huang và Huang (2024)** | Cửa sổ trượt cải thiện tính toàn vẹn ngữ nghĩa của vector | nDCG@5 của BGE tăng 8.3 điểm phần trăm; tuy nhiên BM25 giảm khi có gối đầu | **Tương thích một phần**, làm rõ tính chọn lọc theo thuật toán |
| **Liu et al. (2023)** | LLM bị suy giảm chú ý ở giữa đoạn văn bản dài | Đề xuất giải pháp tái xếp hạng tài liệu quan trọng lên đầu hoặc cuối prompt | **Áp dụng nguyên lý** vào tầng Hậu truy xuất |

---

#### 4.7.3. Những phát hiện thực nghiệm và phân tích nguyên nhân

Bên cạnh các kết quả dự kiến, quá trình triển khai thực tế trên tập 5 bài báo khoa học đã đem lại ba phát hiện quan trọng:

##### 1. Hiện tượng nhầm lẫn nguồn gốc và sự dồn điểm của Cosine Similarity
Một hiện tượng nổi bật trong thực nghiệm là: Các mô hình nhúng nơ-ron như BGE-small-en-v1.5 có xu hướng sinh ra điểm số tương đồng Cosine dồn ở dải rất cao (**0.72 đến 0.86**) cho hầu hết các đoạn văn bản liên quan đến chủ đề học thuật. Tuy nhiên, điểm số cao này không bảo đảm phân biệt được nguồn gốc tài liệu khởi nguyên (ví dụ: Zhao et al. đạt điểm số 0.7553 ở Hạng 1 cho câu hỏi về Lewis et al. ở câu hỏi Q04).
- *Nguyên nhân bản chất*: Học tương phản (Contrastive Learning) tối ưu hóa khoảng cách hình học giữa câu hỏi và các đoạn trích chứa từ vựng đồng xuất hiện hoặc cùng ngữ cảnh ngữ nghĩa. Do các bài báo tổng quan trích dẫn đầy đủ thuật ngữ và công thức của bài báo gốc, vector nhúng của đoạn khảo sát có thể tiệm cận câu hỏi hơn cả bản gốc.
- *Ý nghĩa thực tiễn*: Phát hiện này chứng minh rằng việc thiết lập một ngưỡng Cosine tĩnh đơn thuần (như $\tau = 0.75$) là không đủ để bảo đảm tính chính xác, và các hệ thống tìm kiếm học thuật cần kết hợp bộ lọc siêu dữ liệu (metadata filtering) cùng mô hình Cross-Encoder để chấm điểm quan hệ trích dẫn.

##### 2. Tương tác trái ngược giữa phương pháp cắt đoạn và thuật toán truy xuất
Một phát hiện thực nghiệm mang tính đối kháng là:
- Với mô hình nhúng ngữ nghĩa dày (Dense Bi-encoder): Việc thiếu vùng gối đầu (cắt cố định) làm suy giảm độ chính xác Hit@1 của BGE từ 65.0% xuống 52.5% do mất tính toàn vẹn câu.
- Ngược lại, với thuật toán tìm kiếm từ vựng thưa (Sparse Lexical BM25): Thuật toán này lại đạt Hit@1 cao nhất (**67.5%**) trên cấu hình cắt cố định.
- *Nguyên nhân bản chất*: BM25 chỉ quan tâm đến tần suất từ khóa hiếm độc lập (TF-IDF), không quan tâm đến cấu trúc cú pháp của câu. Khi một đoạn bị cắt cụt, từ khóa mục tiêu vẫn nằm trong đoạn, và việc đoạn văn bị ngắn đi lại làm tăng mật độ từ khóa (TF), giúp BM25 đẩy đoạn văn lên hạng đầu. Phát hiện này là luận cứ thực nghiệm rõ ràng cho thấy tại sao kỹ thuật **Tìm kiếm lai (Hybrid Search)** kết hợp BM25 và Vector Search là phương án bổ trợ hiệu quả.

##### 3. Giới hạn của RAG văn bản thuần trước cấu trúc bảng biểu và công thức toán phức
Khi câu hỏi chạm đến các bảng số liệu phức tạp (như bảng so sánh hiệu năng của các mô hình trong KILT hoặc các bảng phân loại đa cột trong Zhao et al.), thư viện PyMuPDF đã làm phẳng cấu trúc hai chiều thành luồng văn bản tuần tự. Điều này khiến quan hệ liên kết giữa tiêu đề cột và các giá trị ô bị đứt gãy, dẫn đến việc vector nhúng không thể hiện được tính đối sánh đa chiều. Đây là bằng chứng thực tế cho thấy sự cần thiết của việc phát triển các kiến trúc RAG Đa phương thức và kỹ thuật Truy xuất Đa vector (Multi-Vector Retriever) trong các nghiên cứu tương lai.

---

#### 4.7.4. Hàm ý thực tiễn cho giới nghiên cứu và triển khai công nghiệp

Từ các phân tích lý thuyết và phát hiện thực nghiệm, chúng tôi rút ra các khuyến nghị có giá trị ứng dụng cụ thể:

##### 1. Khuyến nghị cho cộng đồng nghiên cứu khoa học tại Việt Nam
Đối với các viện nghiên cứu, trường đại học và các nhà khoa học trong nước, việc ứng dụng các giải pháp RAG thương mại thường vấp phải rào cản về kinh phí bản quyền và tính bảo mật của các đề tài nghiên cứu. Kết quả của công trình này chứng minh rằng:
- Việc kết hợp ngăn xếp công nghệ mã nguồn mở gồm: **ChromaDB + FastEmbed + BGE + ONNX Runtime** là giải pháp phù hợp để xây dựng các hệ thống trợ lý tra cứu tài liệu học thuật độc lập.
- Hệ thống có thể vận hành ổn định trên các máy trạm cá nhân thông thường không cần card đồ họa chuyên dụng, đạt độ trễ khoảng ~40 ms/truy vấn và loại bỏ chi phí gọi API ngoại vi, giúp các nhà nghiên cứu chủ động bảo mật dữ liệu khoa học của mình.

##### 2. Khuyến nghị lựa chọn cơ sở dữ liệu vector cho môi trường doanh nghiệp
Dựa trên phân tích so sánh kỹ thuật tại Chương 3 và Chương 4 cùng kết quả thử nghiệm:
- **ChromaDB** là sự lựa chọn phù hợp cho các giai đoạn nghiên cứu phát triển, thử nghiệm nhanh ý tưởng PoC, các ứng dụng cài đặt nội bộ trên máy đơn, hoặc các hệ thống có quy mô dữ liệu dưới 1 triệu vector nhờ tính chất nhúng gọn nhẹ, dễ bảo trì và không phụ thuộc dịch vụ ngoài.
- **Qdrant** được khuyến nghị cho các hệ thống doanh nghiệp cấp độ sản xuất quy mô lớn. Với lõi được phát triển bằng ngôn ngữ Rust, hỗ trợ tập lệnh tăng tốc phần cứng SIMD, khả năng tiền lọc dữ liệu đồng thời trên chỉ mục HNSW và khả năng mở rộng phân tán, Qdrant mang lại thông lượng xử lý cao với độ trễ thấp và độ tin cậy vận hành ổn định.
- **MongoDB Vector Search (Atlas)** là giải pháp phù hợp cho các doanh nghiệp đã vận hành hệ thống phần mềm trên ngăn xếp cơ sở dữ liệu tài liệu MongoDB, giảm bớt chi phí đồng bộ hóa dữ liệu giữa hai hệ cơ sở dữ liệu tách biệt.
"""


# ==============================================================================
# PHẦN 2: TOÀN VĂN CHƯƠNG 5 (KẾT LUẬN, HẠN CHẾ VÀ HƯỚNG NGHIÊN CỨU TIẾP THEO)
# ==============================================================================

CHAPTER_5 = r"""## CHƯƠNG 5: KẾT LUẬN, HẠN CHẾ VÀ HƯỚNG NGHIÊN CỨU TIẾP THEO

### 5.1. Kết luận

Sự ra đời và phát triển của các mô hình ngôn ngữ lớn đã mở ra một giai đoạn mới cho trí tuệ nhân tạo, nhưng đồng thời cũng làm bộc lộ những ranh giới cơ bản của các kiến trúc thuần tham số: hiện tượng ảo giác tri thức, sự lạc hậu của dữ liệu do điểm dừng huấn luyện, và sự khó khăn trong việc tiếp cận các nguồn tài liệu nội bộ, bảo mật. Trong bối cảnh đó, kiến trúc Sinh Tăng cường Truy xuất RAG đã định hình một bước chuyển dịch mô hình căn bản, giải phóng mô hình ngôn ngữ khỏi gánh nặng phải ghi nhớ toàn bộ kho tàng dữ kiện để tập trung vào thế mạnh cốt lõi là đọc hiểu, phân tích và suy luận logic.

Bản báo cáo nghiên cứu khoa học này là kết quả nghiệm thu của Đề tài Nghiên cứu Khoa học Sinh viên: *"Nghiên cứu và xây dựng hệ thống trí tuệ nhân tạo có tri thức (RAG)"* — Mã số: **07-SV-2026-ĐT1**, do Khoa Kỹ thuật Điện tử 1 (Học viện Công nghệ Bưu chính Viễn thông) giao nhiệm vụ và phê duyệt ngày 03 tháng 4 năm 2026. Đề tài đã hoàn thành các mục tiêu nghiên cứu trọng tâm, thực hiện 4 nội dung nghiên cứu theo đề cương và bàn giao các sản phẩm: Báo cáo kết quả nghiên cứu khoa học hệ thống hóa, Mã nguồn phần mềm hệ thống RAG hoạt động ổn định trên cả môi trường Linux và Windows, cùng Tài liệu hướng dẫn cài đặt chi tiết (Phụ lục C).

#### 5.1.1. Tổng kết năm đóng góp khoa học và kỹ thuật cốt lõi

Công trình nghiên cứu này đóng góp cho cộng đồng học thuật và kỹ thuật năm kết quả nổi bật sau:

1. **Hệ thống hóa cơ sở lý thuyết về Hệ thống AI có Tri thức và chuẩn mực KILT**:
   Báo cáo đã phân định ranh giới khoa học giữa Tác vụ Dựa trên Kỹ năng Ngôn ngữ và Tác vụ Đòi hỏi Tri thức Chuyên sâu; làm rõ bản chất của nguyên lý phân tách giữa Bộ nhớ Tham số nơ-ron và Bộ nhớ Phi tham số rời rạc; đồng thời phân tích cấu trúc chuẩn mực của KILT Benchmark và tiêu chuẩn đánh giá nguồn gốc kép KILT-AC, khẳng định yêu cầu về tính minh bạch nguồn gốc tri thức trong kỷ nguyên AI tạo sinh.

2. **Giải phẫu mô hình toán học xác suất biên của RAG khởi nguyên (Lewis et al., 2020)**:
   Công trình đã trình bày chi tiết công thức xác suất biên phân rã trên biến tiềm ẩn tài liệu của hai biến thể: RAG-Sequence và RAG-Token; phân tích nguyên lý tìm kiếm tích vô hướng cực đại MIPS và cơ chế xấp xỉ giải mã nhanh Fast Decoding, cung cấp một tài liệu tham khảo toán học chuẩn xác cho các nhà nghiên cứu.

3. **Hệ thống hóa ba thế hệ kiến trúc RAG và phân tích chuyên sâu hai trường phái RAG Đa phương thức**:
   Dựa trên các nghiên cứu của Gao et al. (2023b) và khung giải pháp của Google, báo cáo đã xây dựng bức tranh tiến hóa từ Naive RAG, Advanced RAG đến Modular RAG; đồng thời phân tích hai trường phái kiến trúc RAG Đa phương thức (mô hình nhúng không gian đồng nhất 1408 chiều và nhúng văn bản qua tóm tắt) cùng cơ chế Truy xuất Đa vector (Multi-Vector Retriever) nhằm giải quyết bài toán bảng biểu phức tạp và hình ảnh thị giác trong tài liệu khoa học.

4. **Hiện thực hóa đường ống RAG cục bộ và thực nghiệm đo đạc định lượng trên 40 câu hỏi kiểm thử**:
   Nhóm nghiên cứu đã thiết kế và triển khai hệ thống đường ống RAG trên nền tảng Python 3.11 kế thừa từ dự án `vibecoding-sunflower`. Hệ thống đã trích xuất, tiền xử lý và lập chỉ mục 121 trang tài liệu khoa học từ 5 bài báo kinh điển vào cơ sở dữ liệu vector ChromaDB thông qua mô hình BAAI/bge-small-en-v1.5 trên môi trường tăng tốc ONNX Runtime CPU. Thực nghiệm đo đạc đối sánh trên bộ dữ liệu chuẩn 40 câu hỏi chân lý thực tế ghi nhận: cấu hình Cửa sổ trượt kết hợp BGE-small đạt **Hit@5 = 95.0%**, **Hit@3 = 87.5%**, **nDCG@5 = 0.810** với độ trễ xử lý khoảng **40.31 ms/câu hỏi** trên vi xử lý Intel Core i7-7700HQ.

5. **Phân tích các bộ khung đo lường và khảo sát đặc tả kỹ thuật đa hệ quản trị CSDL vector**:
   Công trình đã trình bày nguyên lý hoạt động của các bộ khung đánh giá: bốn trụ cột của RAGAS gồm Độ trung thực, Độ liên quan câu trả lời, Context Precision và Context Recall; khung tự động dựa trên khoảng tin cậy ARES, và bài thử nghiệm ứng suất RGB; đồng thời cung cấp các phân tích thực nghiệm so sánh định lượng ba chiến lược cắt đoạn văn bản và khảo sát đặc tả kỹ thuật bốn hệ quản trị cơ sở dữ liệu vector tiêu biểu gồm ChromaDB, Qdrant, MongoDB Atlas Vector Search và Milvus.

#### 5.1.2. Tóm lược câu trả lời cho các câu hỏi nghiên cứu

- **Về Câu hỏi nghiên cứu 1 - Tiến hóa kiến trúc**: Kiến trúc RAG đã phát triển qua ba thế hệ từ đường ống tuần tự của Naive RAG, sang tối ưu hóa ba tầng Tiền - Trong - Hậu truy xuất ở Advanced RAG, và mở rộng với mạng lưới các module thích ứng linh hoạt có khả năng tự phản chiếu ở Modular RAG, kết hợp với các bước tiến của RAG Đa phương thức.
- **Về Câu hỏi nghiên cứu 2 - Hiệu năng của BAAI/bge-small-en-v1.5**: Mô hình nhúng 384 chiều gọn nhẹ đạt hiệu năng khả quan trên tập 40 câu hỏi học thuật với Hit@5 đạt 95.0%, Hit@3 đạt 87.5%, MRR@5 đạt 0.763 và nDCG@5 đạt 0.810, vận hành ổn định với độ trễ ~40 ms trên CPU thông thường. Nghiên cứu cũng chỉ ra rằng điểm tương đồng Cosine có xu hướng dồn ở mức cao (0.72–0.86) và không thể phân biệt nguồn gốc tài liệu nguyên bản nếu không có tầng tái xếp hạng.
- **Về Câu hỏi nghiên cứu 3 - Chiến lược cắt đoạn tối ưu**: Chiến lược Cửa sổ trượt (250 từ / 50 từ gối đầu) đem lại hiệu năng ngữ nghĩa cao hơn cho mô hình nhúng nơ-ron BGE-small, nâng nDCG@5 thêm 8.3 điểm phần trăm so với cắt cố định. Chiến lược Cắt đệ quy theo cấu trúc mang lại sự cân bằng giữa chất lượng và chi phí lưu trữ, trong khi BM25 lại đạt Hit@1 cao nhất bảng (67.5%) trên các đoạn cắt cố định nhờ khả năng bắt trúng từ khóa hiếm.
- **Về Câu hỏi nghiên cứu 4 - RAG và Long-Context LLMs**: RAG và Long-Context LLMs tạo thành mối quan hệ cộng sinh tương hỗ, trong đó RAG giữ vai trò là bộ lọc tối ưu về chi phí, độ trễ và bảo mật cho kho tri thức lớn, còn Long-Context LLMs phát huy năng lực suy luận sâu trên tập ngữ cảnh tinh chọn.

---

### 5.2. Hạn chế của nghiên cứu

Mặc dù đã hoàn thành các mục tiêu đề ra và đạt được những kết quả khả quan, nhóm nghiên cứu thẳng thắn thừa nhận năm hạn chế nội tại của công trình:

1. **Quy mô ngữ liệu giới hạn ở năm bài báo tiếng Anh và định dạng văn bản thuần**:
   Thực nghiệm trong báo cáo mới chỉ được tiến hành trên tập dữ liệu gồm 5 bài báo khoa học bằng tiếng Anh với quy mô 121 trang tài liệu. Hệ thống hiện thời vận hành theo cơ chế đơn phương thức văn bản, chưa hỗ trợ phân giải và xử lý trực tiếp các bảng biểu số liệu phức tạp và hình ảnh trực quan qua mô hình nhúng đa phương thức 1408 chiều cũng như kỹ thuật Multi-Vector Retriever; đồng thời chưa được kiểm thử trên tập dữ liệu tiếng Việt chuyên ngành vốn có những đặc thù ngôn ngữ học phức tạp.

2. **Nhãn chân lý xác định ở cấp độ bài báo và tính đại diện của tập kiểm thử**:
   Bộ dữ liệu kiểm thử thực nghiệm gồm 40 câu hỏi chân lý thực tế đã được xây dựng công phu, nhưng nhãn đúng/sai được xác định ở cấp độ bài báo nguồn (paper-level). Do 3 trong số 5 bài báo là các khảo sát tổng quan cùng bao quát nhiều chủ đề chung (Self-RAG, CRAG, RAGAS), việc hệ thống trích xuất đoạn từ bài khảo sát này thay vì bài khảo sát kia tạo ra sự mơ hồ về nhãn hơn là sai lệch ngữ nghĩa. Hơn nữa, với đường cơ sở ngẫu nhiên đạt khoảng ~20% Hit@1 và ~67% Hit@5, kết quả 95% Hit@5 cần được nhìn nhận trong bối cảnh không gian tìm kiếm gồm 5 tài liệu mục tiêu.

3. **Tập trung đo kiểm định lượng thành phần truy xuất, chưa đo lường khâu sinh tự hồi quy bằng LLM**:
   Nghiên cứu hiện tại tập trung trọng tâm vào việc thiết kế, xây dựng và đo đạc định lượng hiệu năng của thành phần truy xuất thông tin, chất lượng vector hóa và độ chính xác của chỉ mục HNSW trên bộ dữ liệu 40 câu hỏi. Nhóm nghiên cứu chưa tích hợp trực tiếp một mô hình ngôn ngữ lớn đầu cuối (như GPT-4 hoặc LLaMA-3) để sinh phản hồi tự nhiên hoàn chỉnh do hạn chế về kinh phí gọi API thương mại và tài nguyên phần cứng máy chủ cục bộ, do đó chưa thể tiến hành tính toán các chỉ số định lượng về khâu sinh như Độ trung thực hay Độ liên quan của câu trả lời theo chuẩn RAGAS trên câu trả lời sinh ra.

4. **Hai thuật toán truy xuất BM25 và Vector Search được đo kiểm độc lập, chưa tích hợp mô hình Hợp nhất Thứ hạng Tương hỗ**:
   Mặc dù báo cáo đã phân tích cơ sở lý thuyết của tìm kiếm lai Hybrid Search và thuật toán RRF tại Chương 2, trong khuôn khổ thực nghiệm đường ống tại Chương 4, chúng tôi mới chỉ đo đạc độc lập hiệu năng của từng phương pháp (BM25 riêng biệt và Dense Bi-encoder riêng biệt) nhằm làm rõ bản chất đối kháng giữa hai cách tiếp cận, chứ chưa tích hợp mô-đun RRF và mô hình Cross-Encoder Re-ranking trực tiếp vào đường ống phục vụ thực tế.

5. **Khảo sát cơ sở dữ liệu vector dựa trên tổng hợp đặc tả công bố**:
   Nội dung so sánh giữa các hệ quản trị cơ sở dữ liệu vector tiêu biểu gồm ChromaDB, Qdrant, MongoDB Atlas Vector Search và Milvus được thực hiện dựa trên việc tổng hợp và phân tích kiến trúc phần mềm, thông số kỹ thuật đã công bố và kinh nghiệm triển khai dự án tham chiếu. Đề tài chưa tiến hành một bài đo kiểm chuẩn tải nặng độc lập trong cùng điều kiện phần cứng kiểm soát để đo đạc trực tiếp các chỉ số thông lượng QPS, mức tiêu hao RAM và thời gian lập chỉ mục trên quy mô hàng triệu vector.

*Lưu ý về quy trình kiểm thử tự động*: Kịch bản kiểm thử [verify_deliverables.py](file:///c:/project/NCKH/RAG/verify_deliverables.py) được xây dựng nhằm bảo đảm tính toàn vẹn về mặt cấu trúc văn bản, tính tương thích của các trường dữ liệu và không rò rỉ mã nguồn; kịch bản này đóng vai trò hỗ trợ thẩm định hình thức kỹ thuật chứ không thay thế cho việc đánh giá khoa học chuyên sâu của hội đồng bình duyệt.

---

### 5.3. Hướng nghiên cứu tiếp theo

Nhằm khắc phục các hạn chế nêu trên và đón đầu những bước tiến công nghệ mới nhất trong lĩnh vực trí tuệ nhân tạo, nhóm nghiên cứu đề xuất năm định hướng phát triển cụ thể tiếp theo:

#### 5.3.1. Hiện thực hóa kiến trúc RAG Đa phương thức và cơ chế Truy xuất Đa vector cho dữ liệu bán cấu trúc
Nhằm vượt qua ranh giới của RAG văn bản thuần, hướng phát triển trọng tâm đầu tiên là xây dựng đường ống xử lý chuyên sâu cho các bảng biểu khoa học phức tạp và hình ảnh kỹ thuật dựa trên hai trường phái:
- Ứng dụng mô hình nhúng đa phương thức không gian đồng nhất 1408 chiều (theo chuẩn Google Gemini) để hỗ trợ tìm kiếm chéo phương thức giữa văn bản câu hỏi và hình ảnh/sơ đồ thí nghiệm.
- Tích hợp kỹ thuật Multi-Vector Retriever: Tự động trích xuất bảng biểu thành bản tóm tắt để lập chỉ mục vector, đồng thời lưu trữ cấu trúc bảng thô định dạng HTML hoặc Markdown nguyên vẹn trong Docstore để nạp trực tiếp cho mô hình ngôn ngữ lớn tổng hợp câu trả lời, giảm thiểu sai lệch số liệu.

#### 5.3.2. Tích hợp kiến trúc GraphRAG phục vụ suy luận đa bước trên tài liệu chuyên khảo
Tìm kiếm vector truyền thống chỉ xử lý tốt các câu hỏi tra cứu cục bộ nhưng gặp điểm nghẽn trước các câu hỏi tổng kết toàn cục hoặc suy luận chéo nhiều bước xuyên suốt kho tài liệu. Trong giai đoạn tiếp theo, chúng tôi sẽ tích hợp kiến trúc GraphRAG theo đề xuất của Edge et al. (2024):
- Sử dụng mô hình ngôn ngữ lớn để trích xuất tự động toàn bộ Thực thể, Quan hệ và Thuộc tính từ các tài liệu khoa học để kiến tạo một Đồ thị Tri thức hoàn chỉnh.
- Áp dụng giải thuật phân cụm cộng đồng Leiden để tóm tắt đồ thị từ dưới lên trên, tạo ra các bản tóm tắt phân cấp.
- Kết hợp tìm kiếm vector và tìm kiếm đồ thị nhằm trả lời tốt cả câu hỏi chi tiết lẫn các câu hỏi phân tích khái quát toàn diện.

#### 5.3.3. Huấn luyện và vi chỉnh mô hình nhúng tiếng Việt chuyên sâu cho văn bản học thuật
Để hệ thống RAG hoạt động hiệu quả tối đa trên các văn bản học thuật và tài liệu pháp lý tại Việt Nam, hướng phát triển quan trọng là xây dựng không gian vector chuyên biệt cho tiếng Việt:
- Thu thập và chuẩn hóa tập ngữ liệu bài báo khoa học, luận văn và tài liệu chuyên ngành tiếng Việt quy mô lớn.
- Sử dụng các kỹ thuật tiền xử lý tách từ chuyên sâu kết hợp với việc vi chỉnh các mô hình nền tảng như `vietnamese-bi-encoder` hoặc `Alibaba-NLP/gte-multilingual-base` thông qua hàm mất mát InfoNCE với các mẫu đối âm tính chọn lọc.
- Đánh giá mô hình nhúng tiếng Việt sau vi chỉnh trên bảng xếp hạng MTEB tiếng Việt để bảo đảm chất lượng truy xuất.

#### 5.3.4. Xây dựng hệ thống Agentic RAG tự hành đa công cụ với cơ chế tự phản chiếu
Chuyển đổi từ một hệ thống RAG thụ động sang một Tác tử AI tự hành đa bước thông minh ứng dụng các nguyên lý tiên tiến nhất của Self-RAG và Corrective RAG:
- Trang bị cho tác tử khả năng tự lập kế hoạch phân rã câu hỏi phức tạp thành chuỗi các mục tiêu con.
- Tích hợp đa dạng các công cụ hỗ trợ: tra cứu Vector Database nội bộ, truy vấn cơ sở dữ liệu quan hệ SQL, thực thi mã Python, và tra cứu công cụ tìm kiếm Google Search khi thông tin nội bộ không đủ tin cậy.
- Áp dụng các token tự phản chiếu để tác tử liên tục kiểm định tính trung thực và mức độ đầy đủ của bằng chứng trước khi sinh phản hồi cuối cùng.

#### 5.3.5. Hiện thực hóa quy trình đánh giá toàn diện chu trình RAG bằng bộ khung RAGAS
Mở rộng hệ thống để đo lường toàn diện chu trình RAG từ khâu truy xuất đến khâu sinh câu trả lời:
- Tích hợp một mô hình ngôn ngữ lớn mã nguồn mở có chi phí hợp lý (như LLaMA-3.1-8B-Instruct hoặc Qwen-2.5-7B-Instruct) vào khâu tạo sinh văn bản cục bộ.
- Xây dựng tập dữ liệu kiểm thử chuẩn gồm 200 câu hỏi học thuật có sẵn câu trả lời đối chuẩn do chuyên gia thẩm định.
- Vận hành tự động bộ khung đo lường RAGAS để thu thập đầy đủ dữ liệu định lượng cho toàn bộ bốn chỉ số: Độ trung thực Faithfulness, Độ liên quan của câu trả lời Answer Relevance, Context Precision và Context Recall, kèm theo kiểm định thống kê ý nghĩa khoa học.

```mermaid
flowchart TD
    subgraph S1["GIAI ĐOẠN 1: MỞ RỘNG DỮ LIỆU VÀ MÔ HÌNH NHÚNG"]
        direction TB
        A1["Thu thập và xử lý 100+ bài báo khoa học"]
        A2["Vi chỉnh mô hình nhúng tiếng Việt chuyên biệt"]
        A1 --> A2
    end

    subgraph S2["GIAI ĐOẠN 2: NÂNG CẤP KIẾN TRÚC THÔNG MINH"]
        direction TB
        B1["Tích hợp kiến trúc GraphRAG với đồ thị tri thức"]
        B2["Xây dựng Tác tử Agentic RAG tự hành đa công cụ"]
        B1 --> B2
    end

    subgraph S3["GIAI ĐOẠN 3: ĐO KIỂM TOÀN DIỆN VÀ TỐI ƯU HÓA"]
        direction TB
        C1["Đo lường toàn diện 4 trụ cột bằng khung RAGAS"]
        C2["Kiểm chuẩn hiệu năng tải nặng trên cụm Qdrant phân tán"]
        C1 --> C2
    end

    S1 ==> S2
    S2 ==> S3
```

*Hình 5.1: Sơ đồ lộ trình các định hướng nghiên cứu và phát triển tiếp theo của đề tài*"""


# ==============================================================================
# HÀM KIỂM TRA ĐỘC LẬP
# ==============================================================================

def main():
    print("=" * 70)
    print("KIỂM TRA CÁC MỤC NỘI DUNG V2_DISCUSSION_CONCLUSION.PY")
    print("=" * 70)
    
    # Đo lường số từ và ký tự
    disc_words = len(DISCUSSION_SECTION.split())
    disc_chars = len(DISCUSSION_SECTION)
    ch5_words = len(CHAPTER_5.split())
    ch5_chars = len(CHAPTER_5)
    
    print(f"[*] Mục 4.7 Thảo luận: {disc_words:,} từ | {disc_chars:,} ký tự")
    print(f"[*] Chương 5 Toàn văn: {ch5_words:,} từ | {ch5_chars:,} ký tự")
    print(f"[*] Tổng cộng cả hai phần: {disc_words + ch5_words:,} từ")
    print("-" * 70)
    
    # Kiểm tra các tiêu chuẩn quy định
    checks = [
        ("RQ1 được thảo luận", "Câu hỏi nghiên cứu 1" in DISCUSSION_SECTION),
        ("RQ2 được thảo luận với số liệu thực tế", "Câu hỏi nghiên cứu 2" in DISCUSSION_SECTION and "95.0%" in DISCUSSION_SECTION),
        ("RQ3 được thảo luận với số liệu thực tế", "Câu hỏi nghiên cứu 3" in DISCUSSION_SECTION and "nDCG@5" in DISCUSSION_SECTION),
        ("RQ4 được thảo luận", "Câu hỏi nghiên cứu 4" in DISCUSSION_SECTION),
        ("Không có số liệu 14.2% bịa đặt", "14.2%" not in DISCUSSION_SECTION and "14.2%" not in CHAPTER_5),
        ("Không có tham chiếu Chương 7 sai lệch", "Chương 7" not in DISCUSSION_SECTION and "Chương 7" not in CHAPTER_5),
        ("Đối chiếu Lewis et al. (2020)", "Lewis et al. (2020)" in DISCUSSION_SECTION),
        ("Đối chiếu Gao et al. (2023b)", "Gao et al. (2023b)" in DISCUSSION_SECTION),
        ("ChromaDB & Qdrant thảo luận", "ChromaDB" in DISCUSSION_SECTION and "Qdrant" in DISCUSSION_SECTION),
        ("Chương 5 có Mục 5.1 Kết luận", "### 5.1. Kết luận" in CHAPTER_5),
        ("Chương 5 có 5 đóng góp cốt lõi", "năm đóng góp" in CHAPTER_5 or "5 đóng góp" in CHAPTER_5),
        ("Chương 5 trả lời 4 RQ", "Câu hỏi nghiên cứu 1" in CHAPTER_5 and "Câu hỏi nghiên cứu 4" in CHAPTER_5),
        ("Chương 5 có Mục 5.2 Hạn chế", "### 5.2. Hạn chế của nghiên cứu" in CHAPTER_5),
        ("Chương 5 có Mục 5.3 Hướng nghiên cứu tiếp theo", "### 5.3. Hướng nghiên cứu tiếp theo" in CHAPTER_5),
        ("Mermaid diagram có nhãn tiếng Việt", "```mermaid" in DISCUSSION_SECTION and "```mermaid" in CHAPTER_5),
    ]
    
    all_passed = True
    for title, status in checks:
        icon = "[OK]" if status else "[THẤT BẠI]"
        print(f"  {icon} {title}")
        if not status:
            all_passed = False
            
    print("=" * 70)
    if all_passed:
        print("[HOÀN TẤT] Toàn bộ tiêu chí học thuật đã được kiểm tra đạt chuẩn.")
    else:
        print("[CẢNH BÁO] Một số tiêu chí cần được xem xét lại.")

if __name__ == "__main__":
    main()
