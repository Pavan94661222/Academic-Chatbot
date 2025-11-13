from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
from .config import settings
from .database import engine, Base
from .routers import auth, feedback, chat, learning, academic_chatbot
# from .routers import evaluation  # Temporarily disabled - requires Google Cloud credentials

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Feedback Analysis API",
    description="Full-stack feedback analysis portal with NLP capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(feedback.router)
app.include_router(chat.router)
app.include_router(learning.router)
app.include_router(academic_chatbot.router)
# app.include_router(evaluation.router)  # Temporarily disabled - requires Google Cloud credentials

@app.get("/")
async def root():
    return {
        "message": "Student Feedback Analysis API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    from .health_check import get_system_performance_info
    
    try:
        performance_info = get_system_performance_info()
        
        if performance_info["database_healthy"] and performance_info["user_table_performance"]:
            return {
                "status": "healthy",
                "database": "responsive",
                "performance": "good",
                **performance_info
            }
        else:
            return {
                "status": "degraded",
                "database": "slow" if not performance_info["database_healthy"] else "ok",
                "performance": "poor" if not performance_info["user_table_performance"] else "ok",
                **performance_info
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }
