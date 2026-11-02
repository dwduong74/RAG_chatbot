# -*- coding: utf-8 -*-
"""
Web Chat RAG Khoa Kỹ thuật Điện tử 1 (SEA - PTIT) tích hợp Google Gemini API
Framework: FastAPI + ChromaDB + FastEmbed + Google Gemini
"""

import os
import sys
import time
import json
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Tải cấu hình từ .env
load_dotenv()

# Đảm bảo UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from query_sea_rag import SeaPTITRAGRetriever, CHROMA_DIR, EMBED_MODEL_NAME

app = FastAPI(
    title="SEA PTIT RAG Chatbot",
    description="Hệ thống hỏi đáp tăng cường truy xuất tri thức Khoa Kỹ thuật Điện tử 1 - PTIT",
    version="1.0.0"
)

# Khởi tạo RAG Retriever singleton
print("[*] Đang khởi tạo SEA PTIT RAG Retriever...")
retriever = SeaPTITRAGRetriever(persist_dir=CHROMA_DIR, model_name=EMBED_MODEL_NAME)
print("[OK] RAG Retriever sẵn sàng phục vụ!")

DEFAULT_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

class ChatRequest(BaseModel):
    query: str
    api_key: Optional[str] = None
    top_k: int = 5
    model_name: Optional[str] = "gemini-3.1-flash-lite"

class CitationItem(BaseModel):
    title: str
    url: str
    score: float

class RawChunkItem(BaseModel):
    title: str
    text: str
    score: float
    url: str

class ChatResponse(BaseModel):
    answer: str
    source: str # "gemini" | "retriever"
    citations: List[CitationItem]
    raw_chunks: List[RawChunkItem]
    latency_ms: float

@app.get("/", response_class=HTMLResponse)
async def get_index():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Không tìm thấy file giao diện templates/index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "collection": retriever.collection.name,
        "total_chunks": retriever.collection.count(),
        "embed_model": EMBED_MODEL_NAME
    }

@app.post("/api/chat", response_model=ChatResponse)
def api_chat(req: ChatRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Câu hỏi không được để trống!")

    t_start = time.time()

    # 1. TRUY XUẤT CSDL CHROMADB
    try:
        hits, search_latency = retriever.search(query=query, top_k=req.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi truy xuất ChromaDB: {str(e)}")

    # 2. XỬ LÝ TRÍCH DẪN & RAW CHUNKS
    citations_dict: Dict[str, Dict[str, Any]] = {}
    raw_chunks: List[RawChunkItem] = []

    for hit in hits:
        url = hit.get("url") or "https://sea.ptit.edu.vn"
        title = hit.get("title") or "Khoa Kỹ thuật Điện tử 1"
        score = float(hit.get("score", 0.0))

        if url not in citations_dict or score > citations_dict[url]["score"]:
            citations_dict[url] = {
                "title": title,
                "url": url,
                "score": round(score, 4)
            }

        raw_chunks.append(RawChunkItem(
            title=title,
            text=hit.get("text", ""),
            score=round(score, 4),
            url=url
        ))

    citations = [
        CitationItem(title=v["title"], url=v["url"], score=v["score"])
        for v in sorted(citations_dict.values(), key=lambda x: x["score"], reverse=True)
    ]

    # 3. KIỂM TRA GEMINI API KEY
    effective_api_key = req.api_key.strip() if req.api_key else None
    if not effective_api_key:
        effective_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or DEFAULT_GEMINI_KEY

    # 4. SINH CÂU TRẢ LỜI
    if effective_api_key:
        # CHẾ ĐỘ RAG GENERATIVE VỚI GEMINI
        try:
            genai.configure(api_key=effective_api_key, transport='rest')

            # Xây dựng ngữ cảnh chuẩn hóa
            context_blocks = []
            for i, hit in enumerate(hits, 1):
                context_blocks.append(
                    f"--- [NGUỒN {i}: {hit['title']}] ---\n"
                    f"Đường dẫn: {hit['url']}\n"
                    f"Ngày cập nhật: {hit.get('date', '')}\n"
                    f"Nội dung:\n{hit['text']}\n"
                )
            context_text = "\n".join(context_blocks)

            system_instruction = (
                "Bạn là Trợ lý Trí tuệ Nhân tạo chính thức của Khoa Kỹ thuật Điện tử 1 (SEA), "
                "Học viện Công nghệ Bưu chính Viễn thông (PTIT).\n"
                "Nhiệm vụ của bạn là giải đáp câu hỏi của giảng viên, sinh viên và phụ huynh dựa trên các đoạn ngữ cảnh trích xuất dưới đây.\n\n"
                "QUY TẮC TRẢ LỜI:\n"
                "1. CHỈ sử dụng thông tin có trong ngữ cảnh. Không suy đoán hoặc bịa đặt dữ liệu ngoài ngữ cảnh.\n"
                "2. Nếu ngữ cảnh không có hoặc không đủ thông tin để trả lời đầy đủ, hãy thông báo rõ ràng rằng trên website khoa chưa có thông tin này, và hướng dẫn liên hệ Văn phòng Khoa KTĐT1 (Tầng 2, Nhà A2, Cơ sở Hà Đông).\n"
                "3. Trình bày câu trả lời rõ ràng, mạch lạc bằng định dạng Markdown (tiêu đề, gạch đầu dòng, in đậm tên giảng viên, phòng thí nghiệm, môn học, email, số điện thoại).\n"
                "4. Ở cuối câu trả lời, hãy trích dẫn các liên kết nguồn từ website sea.ptit.edu.vn đã dùng để trả lời."
            )

            prompt = (
                f"{system_instruction}\n\n"
                f"=== DỮ LIỆU TRÍCH XUẤT TỪ CSDL KHOA KTĐT1 ({len(hits)} ĐOẠN LIÊN QUAN NHẤT) ===\n"
                f"{context_text}\n"
                f"========================================================================\n\n"
                f"CÂU HỎI: {query}\n\n"
                f"CÂU TRẢ LỜI (Trình bày học thuật, chuẩn xác, đầy đủ):"
            )

            # Danh sách model thử nghiệm ưu tiên các model đang hoạt động tốt nhất
            target_models = []
            if req.model_name:
                target_models.append(req.model_name)
            for m in [
                "gemini-3.1-flash-lite",
                "gemini-3.6-flash",
                "gemini-3.8-flash",
                "gemini-flash-latest",
                "gemini-2.5-flash-lite",
                "gemini-1.5-flash"
            ]:
                if m not in target_models:
                    target_models.append(m)

            gemini_answer = None
            last_err = None
            for model_name in target_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    res = model.generate_content(prompt)
                    if res and res.text:
                        gemini_answer = res.text
                        break
                except Exception as ex:
                    last_err = ex
                    continue

            if gemini_answer:
                total_latency = (time.time() - t_start) * 1000.0
                return ChatResponse(
                    answer=gemini_answer,
                    source="gemini",
                    citations=citations,
                    raw_chunks=raw_chunks,
                    latency_ms=round(total_latency, 1)
                )
            else:
                # Nếu API key lỗi hoặc rate limit, thông báo rõ và fallback
                warning_header = (
                    f"> ⚠️ **Cảnh báo kết nối Gemini API**: Không thể gọi mô hình Gemini ({last_err}). "
                    f"Hệ thống tự động chuyển sang chế độ Hiển thị Ngữ cảnh Trích xuất trực tiếp.\n\n"
                )
                fallback_answer = warning_header + build_retriever_summary(query, hits)
                total_latency = (time.time() - t_start) * 1000.0
                return ChatResponse(
                    answer=fallback_answer,
                    source="retriever",
                    citations=citations,
                    raw_chunks=raw_chunks,
                    latency_ms=round(total_latency, 1)
                )

        except Exception as e:
            fallback_answer = (
                f"> ⚠️ **Lỗi cấu hình Gemini**: {str(e)}\n\n"
                f"{build_retriever_summary(query, hits)}"
            )
            total_latency = (time.time() - t_start) * 1000.0
            return ChatResponse(
                answer=fallback_answer,
                source="retriever",
                citations=citations,
                raw_chunks=raw_chunks,
                latency_ms=round(total_latency, 1)
            )

    else:
        # CHẾ ĐỘ SEMANTIC RETRIEVAL THUẦN TÚY (KHI CHƯA NHẬP KEY)
        summary_answer = build_retriever_summary(query, hits)
        total_latency = (time.time() - t_start) * 1000.0
        return ChatResponse(
            answer=summary_answer,
            source="retriever",
            citations=citations,
            raw_chunks=raw_chunks,
            latency_ms=round(total_latency, 1)
        )

def build_retriever_summary(query: str, hits: List[Dict[str, Any]]) -> str:
    """Tổng hợp tóm tắt nội dung các đoạn văn bản trích xuất khi không dùng Gemini"""
    if not hits:
        return (
            "**Không tìm thấy tài liệu phù hợp trong CSDL Khoa KTĐT1.**\n\n"
            "Bạn hãy thử điều chỉnh từ khóa tìm kiếm hoặc liên hệ trực tiếp với Văn phòng Khoa để được hỗ trợ."
        )

    lines = []
    lines.append(
        "> 💡 **Chế độ Tìm kiếm Ngữ nghĩa (CSDL Khoa KTĐT1)**  \n"
        "> *Hệ thống đang hiển thị các đoạn trích xuất trực tiếp từ CSDL.*"
    )
    lines.append(f"\n### Kết quả trích xuất liên quan nhất đến câu hỏi: *\"{query}\"*\n")

    for i, hit in enumerate(hits, 1):
        score_pct = hit.get("score", 0.0) * 100.0
        title = hit.get("title", "")
        url = hit.get("url", "#")
        category = hit.get("category", "")
        text = hit.get("text", "")

        # Làm gọn đoạn text nếu có header
        clean_text = text.split("\n\n", 1)[-1] if "\n\n" in text else text
        if len(clean_text) > 400:
            preview = clean_text[:400].strip() + "..."
        else:
            preview = clean_text.strip()

        lines.append(f"#### {i}. [{title}]({url}) `(Độ phù hợp: {score_pct:.1f}%)`")
        if category:
            lines.append(f"*{category}*")
        lines.append(f"```text\n{preview}\n```\n")

    return "\n".join(lines)

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print("🚀 KHỞI ĐỘNG MÁY CHỦ WEB CHAT RAG KHOA KỸ THUẬT ĐIỆN TỬ 1 (PTIT)")
    print("👉 Mở trình duyệt truy cập: http://127.0.0.1:8000")
    print("="*70 + "\n")
    uvicorn.run("web_rag_sea_ptit:app", host="127.0.0.1", port=8000, reload=False)
