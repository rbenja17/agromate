@echo off
echo Starting Agromate Development Environment...

:: Start Backend
start "Agromate Backend" cmd /k "call .venv\Scripts\activate.bat && cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Start Frontend
start "Agromate Frontend" cmd /k "cd frontend && npm run dev"

echo Backend running on http://localhost:8000
echo Frontend running on http://localhost:3000
echo Press any key to exit this launcher (servers will keep running)...
pause >nul
