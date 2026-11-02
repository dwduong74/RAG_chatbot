@echo off
chcp 65001 > nul
title SEA PTIT RAG Chatbot Server
echo ======================================================================
echo    HE THONG HOI DAP TRI THUC RAG - KHOA KY THUAT DIEN TU 1 (PTIT)
echo                   Tich hop Google Gemini API
echo ======================================================================
echo.
echo [*] Dang khoi dong Web Server tai http://127.0.0.1:8000...
echo [*] Du lieu: 248 tai lieu, 722 doan trich ChromaDB
echo.
start http://127.0.0.1:8000
"C:\Users\MC HOME\AppData\Local\Programs\Python\Python311\python.exe" -m uvicorn web_rag_sea_ptit:app --host 127.0.0.1 --port 8000
pause
