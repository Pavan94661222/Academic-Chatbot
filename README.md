# 🤖 Academic Chatbot - NLP Mini Project

**Problem Statement 18**: NLP-powered chatbot for academic queries

**Institution**: Global Academy of Technology  
**Department**: Artificial Intelligence & Machine Learning  
**Course**: Natural Language Processing (22AML71)

---

## 📋 Overview

An intelligent chatbot system that assists students with academic queries including course details, schedules, assignments, and learning support using Natural Language Processing and Google Gemini AI.

### ✨ Key Features

- ✅ **AI-Powered Responses** - Google Gemini 2.0 Flash integration
- ✅ **Intent Classification** - Automatically categorizes user queries
- ✅ **Entity Extraction** - Identifies courses, dates, faculty names
- ✅ **Context-Aware** - Maintains conversation history
- ✅ **Secure Authentication** - JWT-based user login/registration
- ✅ **Modern UI** - Beautiful, responsive interface with TailwindCSS
- ✅ **Real-time Chat** - Instant responses with loading states
- ✅ **Quick Actions** - Pre-defined queries for common questions

---

## 🚀 Quick Start

### 1️⃣ Setup Backend
```bash
# Run setup script
setup_backend.bat

# Create demo user
python create_demo_user.py

# Start backend server
run_backend.bat
```

Backend runs at: `http://localhost:8000`

### 2️⃣ Setup Frontend
```bash
# Run setup script
setup_frontend.bat

# Start frontend server
run_frontend.bat
```

Frontend runs at: `http://localhost:3000`

### 3️⃣ Login
- **Username**: `student`
- **Password**: `password123`

---

## 📁 Project Structure

```
Academic chatbot/
├── app/                      # Backend (FastAPI)
│   ├── main.py              # API routes
│   ├── database.py          # Database config
│   ├── models.py            # Data models
│   ├── auth.py              # Authentication
│   └── chatbot_service.py   # AI service
├── frontend/                 # Frontend (React)
│   └── src/
│       ├── components/
│       │   ├── Login.jsx
│       │   └── ChatInterface.jsx
│       ├── App.jsx
│       └── main.jsx
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── *.bat                     # Setup/run scripts
```

---

## 🔧 Configuration

Edit `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./academic_chatbot.db
SECRET_KEY=your-secret-key
```

Get Gemini API key: https://makersuite.google.com/app/apikey

---

## 💬 Chatbot Capabilities

### Sample Queries
- "Show me Monday's timetable"
- "When is the IA1 exam?"
- "Who teaches NLP?"
- "What courses are there this semester?"
- "What is the attendance requirement?"
- "Tell me about assignments"

### Academic Information
- 7th Semester courses and faculty
- Class timetables (Monday-Friday)
- Exam schedules (IA1, IA2, Lab exams)
- Assignment deadlines
- Attendance policies
- Course details and syllabus

---

## 🛠️ Technologies

**Backend**: FastAPI, SQLAlchemy, Google Gemini AI, JWT Auth  
**Frontend**: React 18, Vite, TailwindCSS, Axios  
**Database**: SQLite  

---

## 📚 Documentation

For detailed documentation, see:
- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Complete project guide
- **[CHATBOT_UPDATE_SUMMARY.md](CHATBOT_UPDATE_SUMMARY.md)** - Technical details

---

## 🐛 Troubleshooting

### Backend Issues
- Ensure Python 3.8+ is installed
- Activate virtual environment: `venv\Scripts\activate`
- Check `.env` has valid `GEMINI_API_KEY`

### Frontend Issues
- Ensure Node.js 16+ is installed
- Clear npm cache: `npm cache clean --force`
- Verify backend is running on port 8000

---

## 📞 API Endpoints

- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/chatbot/chat` - Send message
- `GET /api/chatbot/history` - Get chat history
- `GET /api/chatbot/quick-actions` - Get quick actions

API Docs: `http://localhost:8000/docs`

---

## 🎓 Academic Context

**Semester**: VII (2025-2026)  
**Courses**: NLP, Quantum Computing, Business Intelligence, Data Mining, Major Project  
**Faculty**: Dr. Roopa B S (HOD), Prof. Prasanna N, Prof. Vasugi I, Prof. Vani

---

## 📄 License

Created for academic purposes - NLP Mini Project  
Department of AI & ML, Global Academy of Technology

---

**Version**: 1.0.0  
**Last Updated**: November 2025
