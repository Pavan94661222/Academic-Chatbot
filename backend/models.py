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
    role = Column(String, nullable=False)  # student, faculty, parent
    usn = Column(String, unique=True, index=True, nullable=True)  # For students
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    feedbacks = relationship("Feedback", back_populates="student", foreign_keys="Feedback.student_id")

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course = Column(String, nullable=False)
    comment = Column(Text, nullable=False)
    
    # Ratings
    content_rating = Column(Integer)
    delivery_rating = Column(Integer)
    engagement_rating = Column(Integer)
    difficulty_rating = Column(Integer)
    resources_rating = Column(Integer)
    overall_rating = Column(Integer)
    
    # NLP Analysis Results
    vader_sentiment = Column(String)
    vader_score = Column(Float)
    textblob_sentiment = Column(String)
    textblob_score = Column(Float)
    subjectivity = Column(String)
    subjectivity_score = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("User", back_populates="feedbacks", foreign_keys=[student_id])

class AIChat(Base):
    __tablename__ = "ai_chats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AnswerEvaluation(Base):
    __tablename__ = "answer_evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    teacher_answer = Column(Text, nullable=False)
    student_answer = Column(Text, nullable=False)
    semantic_similarity = Column(Float)
    ai_score = Column(Float)
    final_score = Column(Float)
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    faculty = relationship("User", foreign_keys=[faculty_id])

class AcademicChatHistory(Base):
    __tablename__ = "academic_chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, nullable=False, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    intent = Column(String)
    confidence = Column(Float)
    entities = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", foreign_keys=[user_id])

class FAQ(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    faq_id = Column(String, unique=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String, index=True)
    keywords = Column(Text)  # JSON string
    confidence_level = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True, nullable=False)
    course_name = Column(String, nullable=False)
    course_type = Column(String)  # IPC, PC, PEC, OEC
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

class CourseLearningObjective(Base):
    __tablename__ = "course_learning_objectives"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, ForeignKey("courses.course_code"), nullable=False)
    clo_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CourseModule(Base):
    __tablename__ = "course_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, ForeignKey("courses.course_code"), nullable=False)
    module_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    hours = Column(Integer)
    rbt_level = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CourseOutcome(Base):
    __tablename__ = "course_outcomes"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, ForeignKey("courses.course_code"), nullable=False)
    co_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CourseResource(Base):
    __tablename__ = "course_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, ForeignKey("courses.course_code"), nullable=False)
    resource_type = Column(String, nullable=False)  # textbook, reference, ebook, mooc, web
    title = Column(String, nullable=False)
    author = Column(String)
    publisher = Column(String)
    edition = Column(String)
    year = Column(String)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, ForeignKey("courses.course_code"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    assignment_type = Column(String)  # seminar, term_paper, mini_project, etc.
    deadline = Column(DateTime(timezone=True), nullable=False)
    marks = Column(Integer)
    status = Column(String, default="pending")  # pending, submitted, graded
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
