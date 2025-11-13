@echo off
echo ========================================
echo Academic Chatbot - Backend Setup
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To run the backend:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run server: python -m uvicorn app.main:app --reload --port 8000
echo.
pause
