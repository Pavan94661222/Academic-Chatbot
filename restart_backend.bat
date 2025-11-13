@echo off
echo ========================================
echo Restarting Academic Chatbot Backend
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Starting backend with dynamic database integration...
python -m uvicorn app.main:app --reload --port 8000
