# Danh mục Tài liệu & Nghiên cứu: Hệ thống AI có Tri thức & RAG (Retrieval-Augmented Generation)

Thư mục này chứa các bài báo khoa học kinh điển và tổng quan (survey) toàn diện nhất về RAG và các tác vụ NLP cần nhiều tri thức (Knowledge-Intensive NLP Tasks).

---

## 1. Bài báo khởi nguyên (Foundational Paper)
- **File**: [`1_Lewis_2020_Retrieval_Augmented_Generation.pdf`](./1_Lewis_2020_Retrieval_Augmented_Generation.pdf)
- **Tiêu đề**: *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- **Tác giả**: Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Sebastian Riedel, Douwe Kiela, et al. (Facebook AI Research, UCL, NYU)
- **Hội nghị / Năm**: NeurIPS 2020
- **Liên kết arXiv**: [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- **Khái niệm then chốt**:
  - Định nghĩa chính thức thuật ngữ **Retrieval-Augmented Generation (RAG)**.
  - Phân tách kiến trúc AI thành 2 thành phần: **Parametric Memory** (mô hình seq2seq/BART) và **Non-parametric Memory** (chỉ mục vector ngoài dạng Dense Passage Retrieval / DPR tìm kiếm trên Wikipedia qua FAISS).
  - Khái niệm **Knowledge-Intensive NLP Tasks**: Là những tác vụ mà ngay cả con người am hiểu cũng không thể trả lời chính xác nếu không tra cứu tài liệu tham khảo bên ngoài (như Fact Checking, Open-domain QA).
  - Hai biến thể nền tảng: **RAG-Sequence** (áp dụng cùng một tài liệu cho cả chuỗi sinh) và **RAG-Token** (từng token sinh ra có thể tham chiếu từ các đoạn trích khác nhau).

---

## 2. Khảo sát toàn diện về RAG trong kỷ nguyên LLM (Comprehensive Survey)
- **File**: [`2_Gao_2023_RAG_for_LLMs_Survey.pdf`](./2_Gao_2023_RAG_for_LLMs_Survey.pdf)
- **Tiêu đề**: *Retrieval-Augmented Generation for Large Language Models: A Survey*
- **Tác giả**: Yunfan Gao, Yun Xiong, Xinyu Gao, Haofen Wang, et al. (Fudan University, Tongji University)
- **Năm**: 2023 / 2024
- **Liên kết arXiv**: [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
- **Khái niệm then chốt**:
  - Bài tổng quan được trích dẫn nhiều nhất về RAG hiện đại cho LLM.
  - Đưa ra sơ đồ tiến hóa chuẩn mực gồm 3 giai đoạn:
    1. **Naive RAG**: Pipeline kinh điển (Indexing $\rightarrow$ Retrieval $\rightarrow$ Prompt Concatenation $\rightarrow$ Generation).
    2. **Advanced RAG**: Bổ sung tối ưu hóa trước truy xuất (Pre-retrieval như HyDE, Query Expansion), trong truy xuất (Hybrid search), và sau truy xuất (Post-retrieval như Re-ranking, Context Compression).
    3. **Modular RAG**: Kiến trúc module hóa linh hoạt cho phép định tuyến (Routing), lặp (Iterative RAG), đệ quy (Recursive RAG), và tự phản chiếu (Self-Reflective / CRAG / Self-RAG).

---

## 3. Khảo sát RAG Đa phương thức & AIGC (Multimodal & AIGC Survey)
- **File**: [`3_Zhao_2024_RAG_for_AIGC_Survey.pdf`](./3_Zhao_2024_RAG_for_AIGC_Survey.pdf)
- **Tiêu đề**: *Retrieval-Augmented Generation for AI-Generated Content: A Survey*
- **Tác giả**: Penghao Zhao, Hailin Zhang, Lingpeng Kong, et al.
- **Năm**: 2024
- **Liên kết arXiv**: [arXiv:2402.19473](https://arxiv.org/abs/2402.19473)
- **Khái niệm then chốt**:
  - Mở rộng khái niệm RAG từ văn bản thuần túy sang **AIGC** (hình ảnh, mã nguồn code, âm thanh, video, mô hình 3D).
  - Phân loại các giai đoạn tích hợp tri thức: *Input Augmentation* (ghép prompt), *Intermediate Layer Augmentation* (Cross-attention tầng ẩn), và *Decoding Augmentation* (kNN-LM / Logits ensemble).

---

## 4. Khảo sát Chu trình & Đánh giá RAG (Paradigms & Evaluation Survey)
- **File**: [`4_Huang_2024_Retrieval_Augmented_Text_Generation_Survey.pdf`](./4_Huang_2024_Retrieval_Augmented_Text_Generation_Survey.pdf)
- **Tiêu đề**: *A Survey on Retrieval-Augmented Text Generation for Large Language Models*
- **Tác giả**: Yizheng Huang, Jimmy Huang, et al.
- **Năm**: 2024
- **Liên kết arXiv**: [arXiv:2404.10981](https://arxiv.org/abs/2404.10981)
- **Khái niệm then chốt**:
  - Khảo sát các cơ chế tương tác giữa mô hình ngôn ngữ và nguồn tri thức: Single-step RAG, Iterative RAG, và Active / Self-directed RAG (mô hình tự quyết định khi nào cần tra cứu tri thức bên ngoài).
  - Tổng kết các khung đánh giá chất lượng RAG: Ragas (Faithfulness, Answer Relevance, Context Precision, Context Recall), RGB benchmark, CRUD.

---

## 5. Benchmark Định nghĩa Hệ thống AI Đòi hỏi Tri thức (Knowledge-Intensive Benchmark)
- **File**: [`5_Petroni_2020_KILT_Benchmark_Knowledge_Intensive_NLP.pdf`](./5_Petroni_2020_KILT_Benchmark_Knowledge_Intensive_NLP.pdf)
- **Tiêu đề**: *KILT: a Benchmark for Knowledge Intensive Language Tasks*
- **Tác giả**: Fabio Petroni, Aleksandra Piktus, Angela Fan, Patrick Lewis, Sebastian Riedel, Luke Zettlemoyer, et al. (FAIR, UCL)
- **Hội nghị / Năm**: NAACL-HLT 2021
- **Liên kết arXiv**: [arXiv:2009.02252](https://arxiv.org/abs/2009.02252)
- **Khái niệm then chốt**:
  - Đặt nền móng đo lường cho các mô hình AI có tri thức: chuẩn hóa 11 bài toán trên cùng một kho tri thức Wikipedia snapshot 5.9 triệu bài viết.
  - Chuẩn đánh giá **Provenance**: Không chỉ đo độ chính xác của câu trả lời, mà còn đánh giá liệu mô hình có trích dẫn đúng nguồn gốc tài liệu tri thức (ground truth evidence) hay không.
