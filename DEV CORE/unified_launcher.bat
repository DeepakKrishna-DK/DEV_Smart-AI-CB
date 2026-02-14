@echo off
echo [System] Initializing Unified DEV System...

echo [System] Booting MERN Legacy Core (Port 5000)...
start /b node index.js

timeout /t 5 /nobreak > nul

echo [System] Booting Neural RAG Engine (Port 8501)...
cd Advanced_RAG_Chatbot
.\venv\Scripts\python.exe -m streamlit run app.py

pause
