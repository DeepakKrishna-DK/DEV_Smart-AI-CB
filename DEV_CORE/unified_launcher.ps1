Write-Host "[System] Initializing Unified DEV System..." -ForegroundColor Cyan

# 1. Start Node.js MERN Chatbot (Port 5000)
$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($port5000) {
    Write-Host "[System] MERN Legacy Core on Port 5000 is ALREADY ACTIVE. Skipping launch." -ForegroundColor Yellow
} else {
    Write-Host "[System] Booting MERN Legacy Core (Port 5000)..." -ForegroundColor Yellow
    Start-Process -NoNewWindow -FilePath "node" -ArgumentList "index.js" -WorkingDirectory "."
    # 2. Wait for Node.js to stabilize
    Start-Sleep -Seconds 5
}

# 3. Start Python RAG Chatbot (Port 8501)
Write-Host "[System] Booting Neural RAG Engine (Port 8501)..." -ForegroundColor Magenta
$venvPython = "Advanced_RAG_Chatbot\venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    # Use python module execution for stability
    Start-Process -FilePath $venvPython -ArgumentList "-m streamlit run app.py" -WorkingDirectory "Advanced_RAG_Chatbot"
}
else {
    # Fallback to system python if venv missing (less reliable)
    Write-Host "[Warning] Venv python not found, trying system python..." -ForegroundColor Red
    Set-Location "Advanced_RAG_Chatbot"
    Start-Process -FilePath "python" -ArgumentList "-m streamlit run app.py" -WorkingDirectory "."
    Set-Location ..
}

Write-Host "[System] Unified DEV System is Active!" -ForegroundColor Green
Write-Host "Neural UI: http://localhost:8501" -ForegroundColor Cyan
Write-Host "Legacy API: http://localhost:5000" -ForegroundColor Yellow
