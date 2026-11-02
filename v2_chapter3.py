# -*- coding: utf-8 -*-
"""
Báo cáo Nghiên cứu Khoa học: Hệ thống Trí tuệ Nhân tạo có Tri thức và RAG
Chương 3: Phương pháp Nghiên cứu
"""
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

CHAPTER_3 = r"""## CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU

Phương pháp nghiên cứu đóng vai trò là kim chỉ nam khoa học, bảo đảm tính minh bạch, khách quan và khả năng tái lập của các luận điểm lý thuyết cũng như kết quả thực nghiệm trong công trình này. Nhằm giải quyết các bài toán cốt lõi của hệ thống trí tuệ nhân tạo có tri thức và các kiến trúc sinh tăng cường truy xuất, chương này trình bày tường minh loại hình nghiên cứu, quy trình tổng quan tài liệu có chọn lọc theo chủ đề, thiết kế đường ống thực nghiệm, thông số tập ngữ liệu chuẩn, môi trường kỹ thuật, bộ tiêu chí đo lường định lượng và thiết kế các kịch bản thực nghiệm đối sánh chuyên sâu.

### 3.1. Loại hình nghiên cứu

Đề tài áp dụng loại hình nghiên cứu hỗn hợp kết hợp giữa hai phương pháp:
1. **Phương pháp nghiên cứu định tính qua tổng quan tài liệu có chọn lọc theo chủ đề**: Tiến hành thu thập, phân tích, phân loại và so sánh các kiến trúc RAG từ công trình khởi nguyên đến các biến thể hiện đại.
2. **Phương pháp nghiên cứu thực nghiệm định lượng**: Trực tiếp xây dựng, tích hợp và đo đạc một đường ống RAG trên tập ngữ liệu khoa học thực tế, kiểm chứng các chỉ số định lượng về độ tương đồng ngữ nghĩa, độ chính xác truy xuất và hiệu năng tính toán.

Sự lựa chọn phương pháp nghiên cứu hỗn hợp xuất phát từ tính chất đặc thù và tốc độ phát triển của lĩnh vực trí tuệ nhân tạo tạo sinh:
- *Thứ nhất*, kiến trúc RAG phát triển rất nhanh kể từ năm 2020 đến nay với hàng nghìn bài báo khoa học được công bố. Một cách tiếp cận thuần túy thực nghiệm kỹ thuật cục bộ sẽ có nguy cơ bỏ sót các bước chuyển dịch mô hình then chốt, thiếu đi góc nhìn tổng quan bao quát về sự tiến hóa từ Naive RAG, Advanced RAG đến Modular RAG và Multimodal RAG. Do đó, phương pháp tổng quan tài liệu có chọn lọc là cần thiết nhằm khái quát hóa các mô hình toán học nền tảng, thiết lập hệ thống phân loại và nhận diện các điểm nghẽn lý thuyết cốt tử.
- *Thứ hai*, nếu chỉ dừng lại ở khảo cứu lý thuyết định tính đơn thuần, nghiên cứu sẽ không kiểm chứng được tính khả thi kỹ thuật, không nắm bắt được sự tương tác giữa chiến lược phân đoạn văn bản, mô hình nhúng và thuật toán tìm kiếm láng giềng gần nhất trong không gian đa chiều. Việc triển khai thực nghiệm định lượng trên một đường ống RAG thực tế cho phép đo lường cụ thể các tham số kỹ thuật, đánh giá sự đánh đổi giữa thời gian suy luận và độ chính xác, từ đó mang lại những đóng góp có giá trị thực tiễn cho cộng đồng kỹ thuật phần mềm và khoa học dữ liệu.

Khung phương pháp luận tổng thể của công trình được triển khai qua bốn pha nghiên cứu liên hoàn:
- **Pha 1 - Khảo cứu và tổng quan có chọn lọc**: Thu thập, sàng lọc theo tiêu chí học thuật và tổng hợp các công trình khoa học tiêu biểu nhất về RAG từ các hội nghị hàng đầu.
- **Pha 2 - Hiện thực hóa đường ống thực nghiệm**: Xây dựng hệ thống RAG chuẩn mực từ trích xuất tài liệu, phân đoạn văn bản, nhúng vector đến lập chỉ mục đồ thị thế giới nhỏ điều hướng phân tầng.
- **Pha 3 - Kiểm thử và đo đạc đối sánh**: Thực hiện các kịch bản thực nghiệm độc lập nhằm đối chiếu các chiến lược cắt đoạn, khảo sát đặc tả kỹ thuật các hệ quản trị cơ sở dữ liệu vector và kiểm tra toàn trình hiệu năng truy xuất trên bộ dữ liệu câu hỏi chân lý thực tế.
- **Pha 4 - Tổng hợp và đề xuất khuyến nghị**: Phân tích tương quan giữa các phát hiện định tính và số liệu định lượng để đúc kết nguyên lý thiết kế phù hợp cho hệ thống AI có tri thức.

---

### 3.2. Quy trình tổng quan tài liệu có chọn lọc theo chủ đề

Nhằm thu thập và chắt lọc các công trình khoa học có giá trị học thuật cao, quy trình tổng quan tài liệu được thiết kế theo các nguyên tắc định hướng có hệ thống (Systematic-guided Narrative Review), bao gồm các tiêu chuẩn tìm kiếm, sàng lọc và lựa chọn cụ thể.

```mermaid
flowchart TD
    subgraph G1["GIAI ĐOẠN 1: XÁC ĐỊNH NGUỒN TÀI LIỆU"]
        A1["Truy vấn cơ sở dữ liệu học thuật<br/>arXiv, ACL Anthology, NeurIPS, Google Scholar"]
        A2["Thu thập ban đầu: 280 tài liệu khoa học"]
        A1 --> A2
    end

    subgraph G2["GIAI ĐOẠN 2: SÀNG LỌC BAN ĐẦU"]
        B1["Kiểm tra tiêu đề và tóm tắt công trình"]
        B2["Áp dụng tiêu chí loại trừ sơ bộ<br/>Loại bỏ 195 bài báo không phù hợp"]
        B3["Còn lại: 85 bài báo vào vòng đánh giá"]
        B1 --> B2 --> B3
    end

    subgraph G3["GIAI ĐOẠN 3: ĐÁNH GIÁ MỨC ĐỘ PHÙ HỢP TOÀN VĂN"]
        C1["Đọc toàn văn và thẩm định học thuật chuyên sâu"]
        C2["Kiểm tra uy tín hội nghị và số lượt trích dẫn"]
        C3["Chọn lọc 15 công trình phân tích định tính chuyên sâu"]
        C1 --> C2 --> C3
    end

    subgraph G4["GIAI ĐOẠN 4: THIẾT LẬP TẬP NGỮ LIỆU THỰC NGHIỆM"]
        D1["Chọn 5 công trình hạt nhân tiêu biểu nhất"]
        D2["Trích xuất toàn văn 121 trang xây dựng tập ngữ liệu thực nghiệm"]
        D1 --> D2
    end

    A2 --> B1
    B3 --> C1
    C3 --> D1
```

*Hình 3.1: Sơ đồ luồng quy trình tổng quan tài liệu có chọn lọc và lựa chọn ngữ liệu thực nghiệm*

#### 3.2.1. Cơ sở dữ liệu, chuỗi truy vấn và phạm vi thời gian
Nghiên cứu tiến hành thu thập dữ liệu học thuật từ bốn nguồn cơ sở dữ liệu khoa học uy tín trong lĩnh vực Khoa học Máy tính và Trí tuệ Nhân tạo:
1. **arXiv**: Chuyên trang lưu trữ các bản thảo nghiên cứu tiền xuất bản, đặc biệt tập trung vào các nhánh chuyên môn cs.CL, cs.AI và cs.IR về tính toán ngôn ngữ, trí tuệ nhân tạo và truy xuất thông tin.
2. **ACL Anthology**: Kho lưu trữ toàn văn các công trình của Hiệp hội Ngôn ngữ học Tính toán, bao gồm kỷ yếu của các hội nghị như ACL, EMNLP, NAACL, EACL.
3. **Kỷ yếu hội nghị quốc tế NeurIPS, ICML, ICLR**: Các diễn đàn học thuật danh giá về học máy và biểu diễn tri thức học sâu.
4. **Google Scholar**: Sử dụng như công cụ kiểm tra chéo độ phủ trích dẫn và phát hiện các bài báo có tầm ảnh hưởng lớn được trích dẫn rộng rãi.

- **Chuỗi truy vấn tìm kiếm tiêu chuẩn**:
  `("Retrieval-Augmented Generation" OR "RAG") AND ("survey" OR "benchmark" OR "framework" OR "evaluation" OR "knowledge-intensive")`
- **Thời gian tra cứu và sàng lọc**: Tiến hành từ tháng 05/2024 đến tháng 10/2024.
- **Phạm vi xuất bản khảo sát**: Từ tháng 05/2020 (thời điểm xuất bản bài báo khởi nguyên của Lewis et al. tại NeurIPS 2020) đến hết năm 2024.

#### 3.2.2. Tiêu chí lựa chọn và tiêu chí loại trừ
Để đảm bảo chất lượng khoa học và loại bỏ các nguồn dữ liệu gây nhiễu, các tiêu chí lựa chọn và loại trừ được quy định cụ thể:

- **Tiêu chí lựa chọn**:
  - Bài báo định nghĩa trực tiếp, đề xuất khung kiến trúc mới, tối ưu hóa các thành phần thuật toán hoặc thiết lập bộ chuẩn đo lường cho hệ thống RAG và các tác vụ NLP đòi hỏi tri thức.
  - Công trình được xuất bản chính thức tại các hội nghị khoa học hoặc tạp chí chuyên ngành xếp hạng uy tín, hoặc các bản thảo học thuật trên arXiv có số lượng trích dẫn học thuật tối thiểu từ 50 lượt trở lên tính đến thời điểm khảo sát.
  - Cung cấp mô tả kỹ thuật rõ ràng về thuật toán, công thức toán học hoặc kết quả thực nghiệm có đối chứng định lượng minh bạch.

- **Tiêu chí loại trừ**:
  - Các bài viết nhật ký kỹ thuật, bài đăng trên diễn đàn công nghệ cá nhân hoặc các bài hướng dẫn mã nguồn không qua bình duyệt học thuật.
  - Các nghiên cứu chỉ tập trung thuần túy vào tinh chỉnh tham số mô hình ngôn ngữ lớn mà không tích hợp thành phần truy xuất dữ liệu ngoài phi tham số.
  - Các bài khảo sát tổng quan về AI tạo sinh có phạm vi quá rộng, chỉ đề cập đến RAG một cách khái quát mà không phân tích sâu các tầng kỹ thuật bên trong.

#### 3.2.3. Quy trình thực hiện sàng lọc
Quy trình sàng lọc được thực hiện qua hai vòng đánh giá độc lập bởi nhóm nghiên cứu:
- Vòng 1 (Sàng lọc sơ bộ): Rà soát tiêu đề và phần tóm tắt của 280 tài liệu thu thập ban đầu, loại bỏ 195 tài liệu không đáp ứng tiêu chuẩn lựa chọn.
- Vòng 2 (Đánh giá toàn văn): Đọc toàn văn 85 bài báo còn lại để thẩm định độ sâu toán học và tác động học thuật, qua đó xác định được **15 bài báo khoa học tiêu biểu nhất** để phân tích định tính chuyên sâu xuyên suốt báo cáo.
- Từ 15 công trình này, nhóm nghiên cứu đã chắt lọc ra **5 bài báo khoa học hạt nhân mang tính đại diện cao nhất** để trực tiếp đưa vào tập ngữ liệu xây dựng cơ sở dữ liệu tri thức thực nghiệm cho đường ống RAG.

---

### 3.3. Thiết kế thực nghiệm

Thiết kế thực nghiệm của đề tài mô phỏng một hệ thống RAG hiện đại, tuân thủ quy trình chuẩn từ dữ liệu phi cấu trúc ban đầu đến bước truy xuất thông tin có ngữ nghĩa cao.

```mermaid
flowchart TD
    subgraph B1["BƯỚC 1: TRÍCH XUẤT TÀI LIỆU"]
        T1["Tài liệu khoa học PDF 121 trang"] --> T2["Phân giải văn bản liên tục bằng PyMuPDF"]
        T2 --> T3["Làm sạch ký tự và ghi nhận phạm vi trang"]
    end

    subgraph B2["BƯỚC 2: PHÂN ĐOẠN VĂN BẢN"]
        C1["Cửa sổ trượt liên tục 250 từ"]
        C2["Vùng gối đầu 50 từ bảo toàn ngữ cảnh"]
        C3["Đánh mã định danh và siêu dữ liệu cấu trúc"]
        C1 --> C2 --> C3
    end

    subgraph B3["BƯỚC 3: MÃ HÓA VECTOR NGỮ NGHĨA"]
        E1["Mô hình nhúng BAAI bge-small-en-v1.5"]
        E2["Tăng tốc suy luận CPU bằng ONNX Runtime"]
        E3["Chỉ dẫn truy vấn và sinh vector 384 chiều"]
        E1 --> E2 --> E3
    end

    subgraph B4["BƯỚC 4: LƯU TRỮ VÀ LẬP CHỈ MỤC"]
        V1["Cơ sở dữ liệu vector bền vững ChromaDB"]
        V2["Chỉ mục đồ thị thế giới nhỏ phân tầng HNSW"]
        V3["Không gian độ đo khoảng cách Cosine"]
        V1 --> V2 --> V3
    end

    subgraph B5["BƯỚC 5: TRUY VẤN VÀ ĐÁNH GIÁ"]
        Q1["Mã hóa câu hỏi kèm tiền tố chỉ dẫn chuyên biệt"]
        Q2["Truy xuất top-k ứng viên tương đồng nhất"]
        Q3["Đo đạc chỉ số Hit@k, MRR@5, nDCG@5 và độ trễ"]
        Q1 --> Q2 --> Q3
    end

    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5
```

*Hình 3.2: Quy trình năm bước của đường ống thực nghiệm RAG*

#### 3.3.1. Giai đoạn 1: Trích xuất tài liệu
Tài liệu đầu vào là các tệp PDF khoa học chứa cấu trúc trang hai cột, công thức toán học và bảng số liệu. Để trích xuất nội dung mà không làm sai lệch luồng ngữ nghĩa, thư viện PyMuPDF với mô-đun `fitz` được sử dụng nhằm đọc dữ liệu văn bản theo từng trang. Thư viện này có tốc độ phân giải tài liệu cao nhờ lõi xử lý C++, đồng thời cho phép trích xuất siêu dữ liệu đi kèm bao gồm tên tệp và số thứ tự trang tài liệu. Văn bản trích xuất được ghép nối thành luồng văn bản liên tục xuyên trang, lọc bỏ các dòng ngắt trang giả tạo nhưng vẫn duy trì cấu trúc câu hoàn chỉnh.

#### 3.3.2. Giai đoạn 2: Phân đoạn văn bản bằng cửa sổ trượt liên tục
Phân đoạn văn bản đóng vai trò quan trọng đến sự cân bằng giữa tính cục bộ của vector và tính trọn vẹn của ngữ cảnh. Nếu đoạn quá ngắn, vector nhúng sẽ thiếu thông tin liên kết; ngược lại, nếu đoạn quá dài, vector nhúng sẽ bị loãng và làm giảm độ sắc bén khi tìm kiếm tương đồng. Đặc biệt, mô hình nhúng `BAAI/bge-small-en-v1.5` có giới hạn độ dài đầu vào tối đa là 512 tokens. Do đó, kích thước đoạn văn bản cần được kiểm soát chặt chẽ dưới ngưỡng này.

Hệ thống triển khai thuật toán cửa sổ trượt liên tục xuyên suốt toàn bộ tài liệu (cross-page continuous sliding window) dựa trên số lượng từ với hai tham số điều khiển cốt lõi:
- **Kích thước đoạn văn bản**: $L = 250$ từ (tương đương khoảng 330–360 tokens theo bộ tách từ BERT/WordPiece), bảo đảm nằm an toàn dưới ngưỡng 512 tokens của mô hình nhúng.
- **Độ dài gối đầu**: $O = 50$ từ, đóng vai trò là vùng chuyển tiếp giúp bảo toàn tính liên tục của các mệnh đề khoa học và công thức toán học nằm ngay tại ranh giới phân tách giữa các đoạn.

Bước nhảy dịch chuyển của cửa sổ trượt được xác định theo công thức:
$$S = L - O = 250 - 50 = 200 \text{ (từ)}$$

Giả sử văn bản của toàn bộ tài liệu bao gồm chuỗi $N$ từ được đánh chỉ mục $\{w_0, w_1, \dots, w_{N-1}\}$. Đoạn thứ $j$ được trích xuất dưới dạng lát cắt liên tục:
$$\mathcal{C}_j = \{w_{j \cdot S}, w_{j \cdot S + 1}, \dots, w_{\min(j \cdot S + L - 1, N - 1)}\}$$

Mỗi đoạn văn bản $\mathcal{C}_j$ sau khi khởi tạo đều được gắn kèm mã định danh duy nhất có cấu trúc:
$$\text{ID}_j = \text{MãTàiLiệu} + \text{"\_c"} + \text{ChỉSốĐoạn} + \text{"\_p"} + \text{DảiTrang}$$
cùng với siêu dữ liệu gồm tên tệp, dải trang tương ứng (`pages`, `start_page`, `end_page`) nhằm phục vụ công tác truy xuất nguồn gốc chính xác.

#### 3.3.3. Giai đoạn 3: Mã hóa vector ngữ nghĩa với FastEmbed và tiền tố chỉ dẫn
Sau khi phân đoạn, chuỗi văn bản thuần túy được chuyển đổi sang không gian vector nhiều chiều bằng mô hình nhúng `BAAI/bge-small-en-v1.5` thông qua thư viện FastEmbed.

Mô hình ánh xạ mỗi đoạn văn bản $\mathcal{C}_j$ thành một vector đặc trưng liên tục:
$$\vec{d}_j = \mathcal{E}(\mathcal{C}_j) \in \mathbb{R}^{d}, \quad \text{với } d = 384$$

Đối với câu hỏi truy vấn $q$, mô hình BGE yêu cầu bổ sung tiền tố chỉ dẫn chuyên biệt (query instruction prefix) nhằm hướng dẫn mô hình trích xuất biểu diễn ngữ nghĩa phục vụ tác vụ tìm kiếm tài liệu liên quan:
$$\text{Prompt}(q) = \text{"Represent this sentence for searching relevant passages: "} + q$$
$$\vec{q} = \mathcal{E}(\text{Prompt}(q)) \in \mathbb{R}^{384}$$

Quá trình tính toán vector được tăng tốc thông qua môi trường thực thi ONNX Runtime tối ưu hóa cho CPU với tập chỉ lệnh mở rộng AVX2. Kích thước lô xử lý `batch_size = 16` được áp dụng nhằm tối ưu hóa việc phân bổ bộ nhớ đệm và bảo đảm tính ổn định trong suốt quá trình nhúng dữ liệu.

#### 3.3.4. Giai đoạn 4: Lưu trữ và chỉ mục hóa trên ChromaDB
Hệ thống sử dụng hệ quản trị cơ sở dữ liệu vector ChromaDB ở chế độ lưu trữ bền vững với lớp `PersistentClient`. Mỗi đoạn văn bản được nạp vào tập hợp dữ liệu bằng phương thức `upsert` kèm theo vector biểu diễn 384 chiều, chuỗi văn bản gốc và siêu dữ liệu cấu trúc. Việc sử dụng `upsert` thay cho `add` bảo đảm tính bất biến và khả năng chạy lại đường ống mà không bị lỗi trùng lặp mã định danh.

Chỉ mục tìm kiếm vector được xây dựng dựa trên cấu trúc đồ thị thế giới nhỏ điều hướng phân tầng HNSW. Đây là giải pháp tìm kiếm láng giềng gần nhất xấp xỉ phổ biến hiện nay, cho phép thực hiện truy vấn với độ phức tạp thời gian theo thang đo logarit $\mathcal{O}(\log N)$. Không gian đo lường khoảng cách được thiết lập theo độ đo Cosine:
$$\text{metadata} = \{\text{"hnsw:space"}: \text{"cosine"}\}$$

#### 3.3.5. Giai đoạn 5: Cơ chế truy xuất ngữ nghĩa top-$k$
Khi người dùng đưa ra câu hỏi truy vấn $q$, hệ thống kích hoạt quy trình truy xuất theo các bước:
1. Thêm tiền tố chỉ dẫn và mã hóa câu hỏi thành vector truy vấn $\vec{q} \in \mathbb{R}^{384}$.
2. Quét chỉ mục HNSW trên ChromaDB để xác định tập hợp $k$ vector đoạn văn bản $\{\vec{d}_1, \vec{d}_2, \dots, \vec{d}_k\}$ có khoảng cách Cosine nhỏ nhất đối với $\vec{q}$.

Khoảng cách Cosine giữa vector truy vấn $\vec{q}$ và vector tài liệu $\vec{d}_i$ được tính theo công thức:
$$D_{\text{cosine}}(\vec{q}, \vec{d}_i) = 1 - \frac{\vec{q} \cdot \vec{d}_i}{\|\vec{q}\|_2 \|\vec{d}_i\|_2} = 1 - \frac{\sum_{m=1}^{384} q_m d_{i,m}}{\sqrt{\sum_{m=1}^{384} q_m^2} \sqrt{\sum_{m=1}^{384} d_{i,m}^2}}$$

Điểm số tương đồng chuẩn hóa được xác định bằng:
$$\text{Similarity Score}(\vec{q}, \vec{d}_i) = 1.0 - D_{\text{cosine}}(\vec{q}, \vec{d}_i) = \frac{\vec{q} \cdot \vec{d}_i}{\|\vec{q}\|_2 \|\vec{d}_i\|_2}$$

Cần nhấn mạnh rằng điểm tương đồng Cosine là một đại lượng đo độ gần gũi về hướng hình học trong không gian đặc trưng nhiều chiều, được thuật toán sử dụng để xếp hạng các ứng viên tiềm năng. Điểm tương đồng cao không đồng nghĩa với tính chính xác của dữ kiện, bởi một bài báo tổng quan trích dẫn lại một công trình gốc vẫn có thể đạt điểm số Cosine rất cao do chia sẻ cùng không gian từ vựng và ngữ cảnh học thuật.

---

### 3.4. Dữ liệu thực nghiệm

Nhằm xây dựng một tập ngữ liệu kiểm thử vừa mang tính học thuật cao cấp, vừa có độ phức tạp phản ánh đúng thực tế, đề tài tuyển chọn 5 bài báo khoa học hạt nhân tiêu biểu nhất về RAG từ các hội nghị và kho lưu trữ uy tín.

*Bảng 3.1: Bảng thống kê chi tiết các công trình khoa học trong tập ngữ liệu thực nghiệm*

| STT | Tên tài liệu | Tác giả chính | Năm | Hội nghị / Nơi xuất bản | Số trang | Số chunk (Cố định 250w) | Số chunk (Trượt 250w/50ov) | Số chunk (Đệ quy) |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Lewis, P. et al. | 2020 | NeurIPS 2020 | 19 | 49 | 50 | 58 |
| 2 | Retrieval-Augmented Generation for Large Language Models: A Survey | Gao, Y. et al. | 2023 | arXiv:2312.10997 | 21 | 63 | 79 | 75 |
| 3 | Retrieval-Augmented Generation for AI-Generated Content: A Survey | Zhao, P. et al. | 2024 | arXiv:2402.19473 | 22 | 56 | 102 | 67 |
| 4 | A Survey on Retrieval-Augmented Text Generation for Large Language Models | Huang, Y. et al. | 2024 | arXiv:2404.10981 | 37 | 93 | 103 | 111 |
| 5 | KILT: a Benchmark for Knowledge Intensive Language Tasks | Petroni, F. et al. | 2021 | NAACL 2021 | 22 | 57 | 64 | 68 |
| **Tổng** | **5 công trình nghiên cứu tiêu biểu** | — | **2020–2024** | **NeurIPS, NAACL, arXiv** | **121** | **318** | **398** | **379** |

Tập ngữ liệu này sở hữu các đặc tính nghiên cứu khoa học nhờ sự kết hợp giữa các khía cạnh lý thuyết và thực tiễn:
1. **Bài báo số 1 (Lewis et al., 2020)**: Công trình khởi nguyên đặt nền móng toán học xác suất biên cho RAG-Sequence và RAG-Token. Tài liệu này cung cấp các đoạn văn bản chứa nhiều công thức giải tích xác suất phức tạp, phù hợp để kiểm tra khả năng truy xuất các truy vấn kỹ thuật chuyên sâu.
2. **Bài báo số 2 (Gao et al., 2023b)**: Bản khảo sát chuẩn mực có lượt trích dẫn hàng đầu, phân định ranh giới tiến hóa giữa Naive RAG, Advanced RAG và Modular RAG. Tài liệu này đóng vai trò là căn cứ lý thuyết chính để kiểm tra các câu hỏi mang tính khái niệm và phân loại kiến trúc.
3. **Bài báo số 3 (Zhao et al., 2024)**: Mở rộng phạm vi của RAG sang toàn bộ hệ sinh thái nội dung do AI tạo ra AIGC, bao gồm văn bản, hình ảnh, mã nguồn và âm thanh. Văn bản cung cấp các phân loại về bốn tầng tăng cường tri thức: tăng cường dựa trên truy vấn, tăng cường dựa trên biểu diễn tiềm ẩn, tăng cường dựa trên phân bố xác suất logit, và tăng cường phỏng đoán.
4. **Bài báo số 4 (Huang và Huang, 2024)**: Đi sâu phân tích các cơ chế tương tác đa bước giữa mô hình ngôn ngữ và nguồn tri thức, bao gồm các mô hình sinh lặp, tự phản chiếu và các khung đánh giá độ tin cậy. Đây là nguồn dữ liệu chuẩn để kiểm nghiệm các câu hỏi so sánh giải pháp.
5. **Bài báo số 5 (Petroni et al., 2021)**: Công trình thiết lập bộ chuẩn KILT, định hình tiêu chuẩn đo lường nguồn gốc trích dẫn và các tác vụ NLP đòi hỏi tri thức. Văn bản này đóng vai trò là cơ sở để đánh giá khả năng định vị tài liệu nguồn đích.

Với quy mô chính xác **121 trang tài liệu khoa học nguyên bản**, quá trình phân đoạn tạo ra từ 318 đến 398 đoạn văn bản tùy theo chiến lược tiền xử lý.

---

### 3.5. Công cụ và môi trường thực nghiệm

Toàn bộ các thực nghiệm trong đề tài được đo đạc trực tiếp trên một hệ thống phần cứng xác định, bảo đảm tính minh bạch và khả năng tái lập độc lập.

#### 3.5.1. Môi trường phần cứng thực nghiệm
- **Bộ vi xử lý (CPU)**: Intel Core i7-7700HQ @ 2.80GHz (4 nhân vật lý, 8 luồng xử lý, tần số xung nhịp tối đa Turbo Boost đạt 3.80GHz), hỗ trợ tập chỉ lệnh vector mở rộng AVX2 và FMA3, cho phép tăng tốc xử lý song song các phép nhân ma trận dấu phẩy động trong quá trình sinh vector nhúng.
- **Bộ nhớ truy cập ngẫu nhiên (RAM)**: 16 GB DDR4 Dual-Channel (tần số 2400MHz), bảo đảm đủ không gian chứa toàn bộ chỉ mục đồ thị HNSW và mô hình nhúng trong bộ nhớ đệm.
- **Ổ cứng lưu trữ**: Ổ thể rắn SSD NVMe với tốc độ đọc tuần tự xấp xỉ 2000 MB/s, phục vụ việc đọc ghi liên tục các tệp dữ liệu bền vững của ChromaDB.

#### 3.5.2. Môi trường phần mềm và hệ điều hành đa nền tảng
Tuân thủ yêu cầu kỹ thuật của sản phẩm Dạng III trong Đề cương Nghiên cứu Khoa học Sinh viên số 07-SV-2026-ĐT1 ("Mã nguồn phần mềm của hệ thống: Hoạt động với môi trường Linux"), toàn bộ hệ thống được xây dựng với kiến trúc hướng chuẩn POSIX và kiểm thử trên cả hai môi trường:
- **Môi trường máy chủ Linux**: Phân phối Ubuntu 22.04 LTS (nhân Linux 5.15+), tối ưu hóa việc quản lý tiến trình nền, vận hành trơn tru với các container Docker và các thư viện số học mã nguồn mở.
- **Môi trường phát triển thử nghiệm**: Windows 10/11 Professional 64-bit (sử dụng PowerShell 7 và WSL2).
- **Môi trường thực thi**: Ngôn ngữ lập trình Python phiên bản 3.11, tận dụng các cải tiến tối ưu hóa tốc độ thực thi của trình thông dịch CPython thế hệ mới.
- **Các thư viện mã nguồn mở chuyên dụng**:
  - `chromadb` (phiên bản 0.4.x trở lên): Hệ quản trị cơ sở dữ liệu vector gọn nhẹ, hỗ trợ chỉ mục HNSW và lưu trữ bền vững trên đĩa cục bộ.
  - `fastembed` (phiên bản 0.2.x trở lên): Thư viện mã hóa vector hiệu năng cao tích hợp ONNX Runtime, giúp chạy các mô hình nhúng nơ-ron Transformer trực tiếp trên CPU.
  - `PyMuPDF` (`fitz` phiên bản 1.23.x trở lên): Thư viện phân giải và trích xuất cấu trúc văn bản từ tệp PDF hiệu năng cao.
  - `numpy`, `python-docx`, `latex2mathml`: Bộ công cụ xử lý số học, định dạng văn bản học thuật và chuyển đổi công thức toán học sang chuẩn biểu diễn số học OMML.

#### 3.5.3. Đặc tả mô hình nhúng và suy luận trên CPU
Nghiên cứu sử dụng mô hình nhúng `BAAI/bge-small-en-v1.5`. Đây là mô hình Bi-encoder tối ưu với kích thước không gian vector $d = 384$ chiều. So với các mô hình 768 chiều hay 1536 chiều, kích thước 384 chiều giúp giảm 50% đến 75% dung lượng bộ nhớ RAM cần thiết để lưu trữ đồ thị HNSW, đồng thời tăng tốc độ tính toán tích vô hướng trong không gian vector.

Nhờ việc đóng gói mô hình dưới dạng định dạng chuẩn ONNX và thực thi qua bộ tăng tốc ONNX Runtime Execution Provider (AVX2), các phép toán đại số tuyến tính được phân rã thành các luồng chỉ lệnh SIMD xử lý song song trên CPU:
- Thời gian sinh vector nhúng trung bình của BGE-small-en-v1.5 đạt **~200–228 mili-giây cho mỗi đoạn văn bản** (với độ dài đoạn 250 từ).
- Mô hình so sánh `all-MiniLM-L6-v2` đạt thời gian trung bình **~48–52 mili-giây cho mỗi đoạn văn bản**.
- Thuật toán `BM25` thực hiện tách từ và xây dựng chỉ mục từ vựng toàn bộ 121 trang trong **~70–100 mili-giây**.

#### 3.5.4. Hệ thống tham chiếu thực nghiệm
Hệ thống thử nghiệm trong công trình được phát triển dựa trên cơ sở tham chiếu kiến trúc từ nền tảng `vibecoding-sunflower`. Đây là một hệ thống RAG thực tế quy mô lớn được thiết kế với kiến trúc trừu tượng hóa đa động cơ cơ sở dữ liệu vector, hỗ trợ chuyển đổi linh hoạt giữa ChromaDB, Qdrant và MongoDB Vector Search.

---

### 3.6. Tiêu chí đo lường định lượng

Để lượng hóa chất lượng của hệ thống một cách khoa học, nghiên cứu áp dụng bộ tiêu chí chuẩn mực quốc tế trong lĩnh vực Truy xuất Thông tin (Information Retrieval - IR).

#### 3.6.1. Tỷ lệ trúng tài liệu đích Hit@k (k = 1, 3, 5)
Chỉ số $\text{Hit}@k$ đo lường tỷ lệ các câu hỏi truy vấn mà trong đó có ít nhất một đoạn văn bản thuộc tài liệu đích chuẩn (Ground-Truth Target Document) xuất hiện trong danh sách top-$k$ kết quả được hệ thống trả về:
$$\text{Hit}@k = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \mathbb{I}\left( \exists d \in \text{Top-}k(q_i) \text{ sao cho } \text{Doc}(d) = \text{Target}(q_i) \right)$$
trong đó $|Q| = 40$ là tổng số câu hỏi kiểm thử, $\text{Top-}k(q_i)$ là tập hợp $k$ đoạn văn bản có điểm xếp hạng cao nhất cho truy vấn $q_i$, $\text{Doc}(d)$ là tài liệu xuất xứ của đoạn trích $d$, và $\mathbb{I}(\cdot)$ là hàm chỉ thị nhận giá trị 1 nếu điều kiện thỏa mãn và 0 nếu ngược lại. Nghiên cứu khảo sát ba mức: $\text{Hit}@1$, $\text{Hit}@3$, và $\text{Hit}@5$.

*Lưu ý về đường cơ sở ngẫu nhiên và chỉ số Recall@5*:
- Trong thiết kế bài toán với 1 tài liệu đích chính cho mỗi câu hỏi, chỉ số $\text{Recall}@5$ đồng nhất về mặt toán học với $\text{Hit}@5$ (đều nhận giá trị 1 nếu tài liệu đích xuất hiện trong top-5 và 0 nếu ngược lại). Do đó, chỉ số $\text{Hit}@5$ được sử dụng làm đại diện chính để tránh trùng lặp dữ liệu.
- Đường cơ sở ngẫu nhiên (Random Baseline): Với 398 đoạn văn bản trích xuất từ 5 tài liệu, xác suất để một đoạn văn bản chọn ngẫu nhiên thuộc đúng tài liệu đích là khoảng $\approx 20.0\%$ (tương ứng $\text{Hit}@1$). Đối với phép chọn $k=5$ đoạn trích ngẫu nhiên không hoàn lại, xác suất có ít nhất một đoạn trích đúng tài liệu đích ước tính là $1 - (1 - 0.20)^5 \approx 67.2\%$.

#### 3.6.2. Nghịch đảo thứ hạng trung bình MRR@k (Mean Reciprocal Rank)
Chỉ số $\text{MRR}$ đánh giá vị trí xuất hiện đầu tiên của tài liệu đích trong danh sách kết quả trả về, phản ánh mức độ ưu tiên xếp hạng của hệ thống:
$$\text{MRR}@k = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$
trong đó $\text{rank}_i$ là thứ hạng của đoạn trích đúng đầu tiên trong top-$k$ đối với câu hỏi $q_i$. Nếu không có đoạn trích đúng nào xuất hiện trong top-$k$, giá trị $\frac{1}{\text{rank}_i}$ được quy ước bằng 0.

#### 3.6.3. Độ lợi tích lũy giảm dần chuẩn hóa nDCG@k (Normalized Discounted Cumulative Gain)
Chỉ số $\text{nDCG}@k$ là thước đo xếp hạng chuẩn mực trong hệ thống tìm kiếm, kết hợp cả tính đúng đắn của tài liệu và vị trí của nó trong danh sách kết quả thông qua hàm suy giảm logarit:
$$\text{DCG}@k = \sum_{r=1}^k \frac{2^{\text{rel}_r} - 1}{\log_2(r + 1)}$$
$$\text{nDCG}@k = \frac{\text{DCG}@k}{\text{IDCG}@k}$$
trong đó $\text{rel}_r \in \{0, 1\}$ là mức độ liên quan nhị phân của đoạn trích tại vị trí thứ hạng $r$, và $\text{IDCG}@k$ là giá trị DCG lý tưởng khi toàn bộ các tài liệu liên quan được xếp ở các vị trí đầu tiên.

#### 3.6.4. Độ trễ truy vấn (Query Latency)
Đo lường thời gian xử lý toàn trình từ khi nhận chuỗi câu hỏi văn bản của người dùng, thực hiện mã hóa vector (hoặc tách từ cho BM25), quét chỉ mục và trả về danh sách $k$ đoạn trích dẫn, tính bằng mili-giây (ms).

---

### 3.7. Thiết kế các thực nghiệm đối sánh

Nhằm cung cấp các kết luận khoa học vững chắc và có tính định hướng thực tiễn, đề tài thiết kế ba kịch bản thực nghiệm độc lập và có đối chứng.

#### 3.7.1. Thực nghiệm 1: Đo đạc đối sánh ba chiến lược phân đoạn văn bản và ba thuật toán truy xuất
Thực nghiệm này tiến hành đánh giá ma trận kết hợp giữa ba chiến lược phân đoạn văn bản và ba thuật toán truy xuất thông tin khác nhau trên cùng tập ngữ liệu 121 trang:

1. **Ba cấu hình phân đoạn văn bản** (tất cả đều bảo đảm giới hạn an toàn dưới 512 tokens):
   - *Cấu hình 1 - Cắt kích thước cố định (Fixed-size 250w, 0ov)*: Cắt văn bản theo từng khối đúng 250 từ không gối đầu, tạo ra **318 đoạn văn bản**.
   - *Cấu hình 2 - Cửa sổ trượt liên tục (Sliding Window 250w, 50ov)*: Cắt văn bản theo cửa sổ 250 từ với 50 từ gối đầu, tạo ra **398 đoạn văn bản**.
   - *Cấu hình 3 - Cắt đệ quy theo cấu trúc (Recursive Structure-aware)*: Phân tách văn bản theo phân cấp đoạn, dòng, dấu chấm kết thúc câu với giới hạn kích thước đoạn 250 từ, tạo ra **379 đoạn văn bản**.

2. **Ba thuật toán truy xuất đối sánh**:
   - *Thuật toán 1 - BM25 (Sparse Lexical Retrieval)*: Thuật toán tìm kiếm từ khóa thưa kinh điển, dựa trên tần suất từ (TF) và tần suất nghịch đảo văn bản (IDF).
   - *Thuật toán 2 - all-MiniLM-L6-v2 (Dense Bi-encoder)*: Mô hình Transformer nhỏ gọn với 6 tầng mã hóa, sinh vector 384 chiều, tìm kiếm bằng tích vô hướng Cosine.
   - *Thuật toán 3 - BAAI/bge-small-en-v1.5 (Dense Bi-encoder với Instruction)*: Mô hình nhúng ngôn ngữ chuyên sâu 384 chiều của BAAI, tích hợp tiền tố chỉ dẫn truy vấn chuyên biệt.

*Bảng 3.2: Ma trận thiết kế thực nghiệm đo đạc đối sánh $3 \times 3$ giữa chiến lược cắt đoạn và thuật toán truy xuất*

| Thuật toán truy xuất | Cố định 250 từ (318 đoạn) | Cửa sổ trượt 250w / 50ov (398 đoạn) | Cắt đệ quy cấu trúc (379 đoạn) |
| :--- | :---: | :---: | :---: |
| **BM25 (Từ vựng thưa)** | Cấu hình A1 | Cấu hình A2 | Cấu hình A3 |
| **MiniLM-L6-v2 (Vector dày)** | Cấu hình B1 | Cấu hình B2 | Cấu hình B3 |
| **BGE-small-v1.5 (Vector dày + Chỉ dẫn)** | Cấu hình C1 | Cấu hình C2 | Cấu hình C3 |

#### 3.7.2. Thực nghiệm 2: Khảo sát và đối sánh đặc tả kỹ thuật bốn hệ quản trị cơ sở dữ liệu vector
Nội dung này tiến hành khảo sát, tổng hợp và so sánh toàn diện bốn hệ quản trị cơ sở dữ liệu vector phổ biến hiện nay trên các tiêu chí kiến trúc phần mềm, năng lực lưu trữ và hiệu năng vận hành dựa trên tài liệu công bố và kinh nghiệm triển khai dự án tham chiếu `vibecoding-sunflower`:
1. **ChromaDB**: Cơ sở dữ liệu vector nhúng mã nguồn mở, hoạt động trực tiếp trong quy trình Python thông qua bộ lưu trữ cục bộ SQLite và thư viện lõi HNSW bằng Rust/C++, tối ưu cho nghiên cứu học thuật và các ứng dụng đơn máy.
2. **Qdrant**: Hệ quản trị cơ sở dữ liệu vector chuyên dụng viết bằng ngôn ngữ Rust, nổi bật với khả năng tối ưu hóa tài nguyên phần cứng qua tập chỉ lệnh SIMD, hỗ trợ lọc siêu dữ liệu đồng thời trong quá trình duyệt đồ thị HNSW ở quy mô sản xuất công nghiệp.
3. **MongoDB Vector Search**: Giải pháp tìm kiếm vector tích hợp trên nền tảng đám mây phân tán NoSQL (MongoDB Atlas), cho phép lưu trữ và truy vấn đồng thời dữ liệu tài liệu BSON nghiệp vụ và vector nhúng thông qua giai đoạn `$vectorSearch` trong chuỗi truy vấn Aggregation Pipeline.
4. **Milvus**: Nền tảng cơ sở dữ liệu vector phân tán quy mô lớn được thiết kế theo kiến trúc hướng đám mây (cloud-native) bằng Go và C++, phân tách độc lập giữa tầng điều phối, tầng tính toán và tầng lưu trữ đối tượng (S3/MinIO), hỗ trợ đa dạng loại chỉ mục từ HNSW, IVF_FLAT đến DiskANN cho các kho dữ liệu quy mô hàng tỷ vector.

*Bảng 3.3: Bảng đối sánh đặc tả kỹ thuật toàn diện giữa bốn hệ quản trị cơ sở dữ liệu vector*

| Đặc tính kỹ thuật | ChromaDB | Qdrant | MongoDB Vector Search (Atlas) | Milvus |
| :--- | :--- | :--- | :--- | :--- |
| **Ngôn ngữ phát triển cốt lõi** | Python / Rust (lõi hnswlib C++) | Rust | C++ | Go / C++ |
| **Kiến trúc triển khai** | Nhúng nội quy trình / Máy chủ độc lập | Máy chủ độc lập / Cụm phân tán | Cụm dịch vụ đám mây phân tán | Cụm phân tán hướng đám mây microservices |
| **Cấu trúc chỉ mục chính** | HNSW (đồ thị phân tầng) | HNSW tùy biến tối ưu | HNSW / IVF phân vùng | HNSW, IVF_FLAT, SCaNN, DiskANN |
| **Cơ chế lưu trữ bền vững** | SQLite cục bộ / Tệp Parquet | Ổ đĩa thể rắn / Ánh xạ bộ nhớ mmap | Bộ máy lưu trữ WiredTiger | S3 / MinIO / Phân tán Ceph |
| **Khả năng lọc siêu dữ liệu** | Lọc cơ bản qua từ điển siêu dữ liệu | Lọc siêu dữ liệu đồng thời cấp Payload | Khai thác cú pháp MQL Aggregation | Biểu thức điều kiện Boolean Scalar Filtering |
| **Mức độ phức tạp triển khai** | Rất thấp (cài qua pip) | Thấp đến trung bình (Docker container) | Thấp (dịch vụ đám mây quản lý sẵn) | Cao (đòi hỏi cụm điều phối Kubernetes) |
| **Trường hợp sử dụng tối ưu** | Nghiên cứu, thử nghiệm nhanh PoC | Doanh nghiệp tải cao, yêu cầu độ trễ | Tích hợp hệ thống ứng dụng Web có sẵn | Kho tri thức quy mô hàng tỷ vector |

#### 3.7.3. Thực nghiệm 3: Kiểm thử toàn trình với bộ câu hỏi chân lý thực tế Ground-Truth QA
Để kiểm tra độ nhạy và tính ổn định của đường ống RAG trên bộ dữ liệu 121 trang, nghiên cứu thiết kế một tập câu hỏi kiểm thử chuẩn gồm **40 câu hỏi chân lý thực tế (Ground-Truth QA Dataset)**. Bộ câu hỏi được phân bổ đồng đều với **8 câu hỏi chuyên sâu cho mỗi bài báo khoa học hạt nhân**, bao quát bốn nhóm hình thái truy vấn học thuật khác nhau:

- **Nhóm 1 - Truy vấn sự kiện đơn lẻ**: Kiểm tra khả năng định vị chính xác các con số, tên mô hình nền tảng, thuật ngữ định danh hoặc cấu hình thử nghiệm (ví dụ: mô hình ngôn ngữ gốc trong Lewis et al., số lượng tác vụ trong KILT).
- **Nhóm 2 - Truy vấn khái niệm tổng quan**: Yêu cầu hệ thống tổng hợp các định nghĩa học thuật bao quát, phân loại các thế hệ kiến trúc (ví dụ: ba thế hệ Naive, Advanced, Modular RAG trong Gao et al., phân loại các tầng tăng cường tri thức trong Zhao et al.).
- **Nhóm 3 - Truy vấn kỹ thuật chuyên sâu và công thức toán học**: Đo lường khả năng tìm kiếm các đoạn văn bản mô tả thuật toán giải tích, công thức tính xác suất biên, cơ chế xấp xỉ giải mã nhanh (ví dụ: công thức xác suất biên của RAG-Sequence và RAG-Token trong Lewis et al., các loại token tự phản chiếu trong Self-RAG).
- **Nhóm 4 - Truy vấn so sánh đối chiếu và chuẩn đánh giá**: Đòi hỏi hệ thống truy xuất các dữ kiện thực nghiệm về các khung đo lường độ tin cậy và hiệu năng (ví dụ: bốn trụ cột của khung RAGAS, nguyên lý đánh giá nguồn gốc kép KILT-AC).

*Bảng 3.4: Bảng đặc tả mẫu bộ câu hỏi kiểm thử thực nghiệm toàn trình (trích 8 câu hỏi đại diện)*

| Mã câu hỏi | Tài liệu đích chuẩn | Nhóm hình thái truy vấn | Nội dung câu hỏi kiểm thử chuyên sâu |
| :---: | :--- | :--- | :--- |
| **Q01** | Lewis et al. (2020) | Kỹ thuật và công thức toán | What is the mathematical formulation of the marginal probability for RAG-Sequence model? |
| **Q02** | Lewis et al. (2020) | Kỹ thuật và công thức toán | How does RAG-Token marginalize over retrieved documents at each target token generation step? |
| **Q04** | Lewis et al. (2020) | Sự kiện và kiến trúc | Which pretrained bi-encoder architecture and generator model are used in the original RAG paper? |
| **Q09** | Gao et al. (2023b) | Khái niệm tổng quan | What are the structural differences between Naive RAG, Advanced RAG, and Modular RAG paradigms? |
| **Q17** | Zhao et al. (2024) | Khái niệm tổng quan | What are the four RAG enhancement stages classified by Zhao et al. for AI-Generated Content? |
| **Q25** | Huang và Huang (2024) | Kỹ thuật và đánh giá | What are the core evaluation metrics defined in the RAGAS framework according to survey papers? |
| **Q33** | Petroni et al. (2021) | Sự kiện đơn lẻ | What is the structure of the KILT benchmark and how many tasks across how many domains does it include? |
| **Q35** | Petroni et al. (2021) | Kỹ thuật và đánh giá | What is the provenance evaluation metric KILT-AC and how does it penalize hallucinations? |

Mỗi truy vấn được đưa vào đường ống với tham số truy xuất $k = 5$. Kết quả được ghi nhận tự động bao gồm: danh sách mã định danh của 5 đoạn văn bản trả về, điểm tương đồng ngữ nghĩa của từng đoạn, tên tài liệu nguồn gốc và dải trang trích xuất. Dữ liệu này là đầu vào trực tiếp cho việc tính toán các chỉ số $\text{Hit}@1$, $\text{Hit}@3$, $\text{Hit}@5$, $\text{MRR}@5$, $\text{nDCG}@5$ và độ trễ truy vấn trung bình (ms), phục vụ cho các phân tích kết quả chuyên sâu tại Chương 4.
"""
