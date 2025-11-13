from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .database import engine, Base, get_db
from . import models, auth
from .chatbot_service_dynamic import dynamic_chatbot_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Academic Chatbot API",
    description="NLP-powered chatbot for academic queries",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    entities: dict
    session_id: str
    timestamp: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Academic Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Health check
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    # Check database connectivity
    try:
        faq_count = db.query(models.FAQ).count()
        course_count = db.query(models.Course).count()
        assignment_count = db.query(models.Assignment).count()
        db_healthy = True
    except:
        faq_count = course_count = assignment_count = 0
        db_healthy = False
    
    return {
        "status": "healthy" if db_healthy else "degraded",
        "gemini_available": dynamic_chatbot_service.gemini_available,
        "database": {
            "healthy": db_healthy,
            "faqs": faq_count,
            "courses": course_count,
            "assignments": assignment_count
        },
        "timestamp": datetime.now().isoformat()
    }

# Authentication endpoints
@app.post("/api/auth/register", response_model=auth.Token)
async def register(user: auth.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        usn=user.usn,
        role="student"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=auth.Token)
async def login(user_login: auth.UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    print(f"Login attempt - Username: {user_login.username}")
    user = db.query(models.User).filter(
        models.User.username == user_login.username
    ).first()
    
    print(f"User found: {user is not None}")
    if user:
        password_valid = auth.verify_password(user_login.password, user.hashed_password)
        print(f"Password valid: {password_valid}")
    
    if not user or not auth.verify_password(user_login.password, user.hashed_password):
        print(f"Login failed for user: {user_login.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get current user information"""
    return current_user

# Chatbot endpoints
@app.post("/api/chatbot/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Main chatbot endpoint"""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Classify intent
        intent, confidence = dynamic_chatbot_service.classify_intent(request.message)
        
        # Extract entities
        entities = dynamic_chatbot_service.extract_entities(request.message, intent)
        
        # Generate response with database context
        response_text = dynamic_chatbot_service.generate_response(
            request.message, intent, entities, session_id, db
        )
        
        # Save to database
        chat_record = models.ChatHistory(
            user_id=current_user.id,
            session_id=session_id,
            user_message=request.message,
            bot_response=response_text,
            intent=intent,
            confidence=confidence,
            entities=json.dumps(entities)
        )
        db.add(chat_record)
        db.commit()
        
        return ChatResponse(
            response=response_text,
            intent=intent,
            confidence=confidence,
            entities=entities,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )

@app.get("/api/chatbot/history")
async def get_chat_history(
    limit: int = 50,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's chat history"""
    try:
        history = db.query(models.ChatHistory)\
            .filter(models.ChatHistory.user_id == current_user.id)\
            .order_by(models.ChatHistory.created_at.desc())\
            .limit(limit)\
            .all()
        
        return {
            "history": [
                {
                    "id": chat.id,
                    "user_message": chat.user_message,
                    "bot_response": chat.bot_response,
                    "intent": chat.intent,
                    "confidence": chat.confidence,
                    "created_at": chat.created_at.isoformat()
                }
                for chat in history
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching history: {str(e)}"
        )

@app.delete("/api/chatbot/session/{session_id}")
async def clear_session(
    session_id: str,
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Clear conversation context"""
    try:
        dynamic_chatbot_service.clear_session(session_id)
        return {"message": "Session cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing session: {str(e)}"
        )

@app.get("/api/chatbot/quick-actions")
async def get_quick_actions(db: Session = Depends(get_db)):
    """Get dynamic quick action buttons based on database"""
    actions = [
        {"label": "📚 All Courses", "query": "What courses are there this semester?"},
        {"label": "🎯 Assignments", "query": "What assignments are due soon?"},
        {"label": "📝 Exam Schedule", "query": "When are the upcoming exams?"},
        {"label": "👨‍🏫 Faculty Info", "query": "Who are the faculty members?"},
        {"label": "📅 Today's Classes", "query": "What classes do I have today?"},
        {"label": "📊 Policies", "query": "What are the academic policies?"}
    ]
    
    # Add dynamic actions based on database content
    try:
        # Check if there are upcoming assignments
        assignment_count = db.query(models.Assignment).count()
        if assignment_count > 0:
            actions.insert(1, {"label": f"⏰ {assignment_count} Assignments", "query": "Show me all assignment deadlines"})
    except:
        pass
    
    return {"actions": actions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
