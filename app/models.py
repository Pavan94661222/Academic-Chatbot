from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="student")
    usn = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, nullable=False, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    intent = Column(String)
    confidence = Column(Float)
    entities = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FAQ(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    faq_id = Column(String, unique=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String, index=True)
    keywords = Column(Text)
    confidence_level = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True, nullable=False)
    course_name = Column(String, nullable=False)
    course_type = Column(String)
    credits = Column(Integer)
    faculty_theory = Column(String)
    faculty_lab = Column(String)
    semester = Column(Integer)
    prerequisites = Column(Text)
    cie_marks = Column(Integer)
    see_marks = Column(Integer)
    hours_per_week = Column(String)
    see_duration = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, ForeignKey("courses.course_code"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    assignment_type = Column(String)
    deadline = Column(DateTime(timezone=True), nullable=False)
    marks = Column(Integer)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
