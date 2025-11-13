# 🤖 Academic Chatbot - NLP Mini Project

**Problem Statement 18**: NLP-powered chatbot for academic queries

**Institution**: Global Academy of Technology  
**Department**: Artificial Intelligence & Machine Learning  
**Course**: Natural Language Processing (22AML71)

---

## 📋 Overview

An intelligent chatbot system that assists students with academic queries including course details, schedules, assignments, and learning support using Natural Language Processing and Google Gemini AI.

### 🤖 AIML_VOICE_ASSISTANT - NLP-Driven Academic Chatbot

[![Netlify Status](https://api.netlify.com/api/v1/badges/1c22e78c-62d2-45df-8b92-6efe04eda828/deploy-status)](https://app.netlify.com/sites/aiml-voice-assistant/deploys)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-aiml--voice--assistant.netlify.app-blue)](https://aiml-voice-assistant.netlify.app)
[![GitHub](https://img.shields.io/github/license/Pavan94661222/Academic-Chatbot)](LICENSE)

## 🎯 Overview
**AIML_VOICE_ASSISTANT** is a sophisticated **Natural Language Processing (NLP) driven chatbot** with voice capabilities, designed specifically for the AI & ML Department at Global Academy of Technology. This intelligent academic companion provides instant access to course information, schedules, assignments, and academic guidance through both text and voice interactions.

## ✨ Key Features

### 🎙️ Advanced Voice Interface
- **Real-time Speech Recognition**: Web Speech API integration
- **Natural Voice Responses**: Text-to-speech with conversational personality  
- **Cosmic-themed UI**: Visually stunning space-themed voice interface
- **Hands-free Operation**: Complete voice-controlled academic assistance

### 💬 Intelligent Chat System
- **NLP-Powered Responses**: Advanced natural language understanding
- **161+ Academic FAQs**: Pre-loaded comprehensive academic database
- **Smart Fallback**: Open-source LLM (Gemini AI) integration for complex queries
- **Chat History**: Persistent conversation tracking and retrieval
- **Quick Actions**: Pre-defined common academic queries

### 🧠 Advanced NLP Architecture
- **Intent Classification**: Automatic categorization of user queries
- **Entity Extraction**: Recognition of courses, dates, faculty names
- **Semantic Search**: Multi-strategy content matching and similarity analysis
- **Context Management**: Maintains conversation flow and history

## 🛠️ Technology Stack

### Frontend (React-based)
- **Framework**: React 18 with Vite
- **Styling**: TailwindCSS with glassmorphism effects
- **Voice**: Web Speech API for speech-to-text and text-to-speech
- **UI Components**: Lucide React icons, custom animations
- **HTTP Client**: Axios for API communication

### Backend (Python-based)
- **Framework**: FastAPI (high-performance async web framework)
- **Database**: SQLAlchemy with SQLite
- **Authentication**: JWT token-based security
- **NLP Integration**: Google Gemini AI (open-source LLM)
- **Security**: Bcrypt password hashing, CORS middleware

### Database (SQL)
- **Type**: SQLite (lightweight, serverless)
- **Tables**: Users, FAQs, Chat History, Academic Data
- **Content**: 161+ academic FAQs, course information, schedules

## 🚀 Live Demo

**🌐 Frontend**: [https://aiml-voice-assistant.netlify.app](https://aiml-voice-assistant.netlify.app)

*Note: Backend deployment required for full functionality*

## 📋 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/Pavan94661222/Academic-Chatbot.git
cd Academic-Chatbot
```

### 2. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
python seed_database.py

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🌐 Deployment

### Frontend - Netlify ✅
- **Live URL**: https://aiml-voice-assistant.netlify.app
- **Auto-deploy**: Configured with `netlify.toml`
- **Build**: Optimized React production build

### Backend - Recommended Platforms
- **Railway**: https://railway.app (Recommended)
- **Render**: https://render.com
- **Heroku**: https://heroku.com

## 📚 Academic Content

### Supported Queries
- **Course Information**: Syllabus, modules, credits, prerequisites
- **Schedules**: Class timetables, examination schedules
- **Assignments**: Deadlines, submission guidelines, project details
- **Faculty**: Contact information, office hours
- **Academic Calendar**: Important dates, events, holidays

### Sample Questions
```
"What are the modules for NLP?"
"Tell me about Machine Learning syllabus"
"When is the next assignment deadline?"
"What are the course outcomes for Deep Learning?"
"Show me the examination schedule"
```

## 🔧 Configuration

### Environment Variables
```env
# Backend (.env)
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_jwt_secret_key
DATABASE_URL=sqlite:///./feedback.db
CORS_ORIGINS=https://aiml-voice-assistant.netlify.app

# Frontend
VITE_API_URL=http://localhost:8000
```

## 📖 Documentation

- **📋 Complete Project Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **❓ Sample Questions**: [sample_questions.md](sample_questions.md)
- **📝 Detailed Questions**: [detailed_sample_questions.md](detailed_sample_questions.md)
- **🚀 Deployment Guide**: [NETLIFY_DEPLOYMENT.md](NETLIFY_DEPLOYMENT.md)

## 🏗️ Project Structure

```
AIML_VOICE_ASSISTANT/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── VoiceAssistant.jsx
│   │   │   └── Login.jsx
│   │   └── App.jsx
│   ├── public/
│   └── netlify.toml         # Netlify deployment config
├── app/                     # FastAPI backend
│   ├── main.py             # FastAPI application
│   ├── models.py           # Database models
│   ├── chatbot_service_dynamic.py  # NLP service
│   └── auth.py             # Authentication
├── backend/                 # Alternative backend setup
├── *.db                    # SQLite databases
├── seed_*.py              # Database seeding scripts
└── *.md                   # Documentation files
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** Pull Request

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**Global Academy of Technology**
- **Department**: Artificial Intelligence & Machine Learning
- **Project**: NLP-Driven Academic Assistant
- **Technology**: React + FastAPI + Open Source LLM

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent response generation
- **React & FastAPI** communities for excellent frameworks
- **Web Speech API** for voice capabilities
- **Global Academy of Technology** for academic support

## 📊 Features Showcase

### 🎨 Modern UI/UX
- Glassmorphism design with smooth animations
- Responsive layout for all devices
- Cosmic-themed voice interface
- Real-time typing indicators

### 🔊 Voice Capabilities
- Speech-to-text conversion
- Natural voice responses
- Voice command recognition
- Hands-free operation

### 🧠 AI-Powered Intelligence
- Context-aware responses
- Multi-strategy search algorithms
- Intelligent fallback to LLM
- Conversation memory

---

**🎓 Built with ❤️ for AI & ML students using cutting-edge NLP technology**

**⭐ Star this repository if you find it helpful!**

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
