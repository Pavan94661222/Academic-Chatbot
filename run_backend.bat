@echo off
echo ========================================
echo Starting Academic Chatbot Backend
echo ========================================
echo.

call venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
