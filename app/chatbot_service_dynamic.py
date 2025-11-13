"""
Enhanced Academic Chatbot Service with Dynamic Database Integration
Fetches real data from database and uses Gemini AI for intelligent responses
"""
from typing import Dict, Tuple, List, Optional
from datetime import datetime
import os
import json
from sqlalchemy.orm import Session

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: Google Gemini SDK not available")

from .database import SessionLocal
from . import models
import sqlite3
from difflib import SequenceMatcher

class DynamicChatbotService:
    def __init__(self):
        self.gemini_available = GEMINI_AVAILABLE
        self.client = None
        self.conversation_history = {}
        
        if GEMINI_AVAILABLE:
            try:
                api_key = os.getenv("GEMINI_API_KEY")
                if api_key:
                    self.client = genai.Client(api_key=api_key)
                    print("✓ Gemini AI initialized successfully")
                else:
                    print("Warning: GEMINI_API_KEY not found")
                    self.gemini_available = False
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
                self.gemini_available = False
    
    def get_db(self):
        """Get database session"""
        return SessionLocal()
    
    def search_database_enhanced(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Enhanced database search using multiple strategies
        """
        try:
            conn = sqlite3.connect('feedback.db')
            cursor = conn.cursor()
            
            # Get all FAQs
            cursor.execute("SELECT faq_id, question, answer, keywords FROM faqs")
            all_faqs = cursor.fetchall()
            conn.close()
            
            query_lower = query.lower()
            scored_results = []
            
            for faq_id, question, answer, keywords in all_faqs:
                score = 0
                
                # 1. Direct keyword matching in question
                question_lower = question.lower()
                if any(word in question_lower for word in query_lower.split()):
                    score += 30
                
                # 2. Keyword field matching
                if keywords:
                    keywords_lower = keywords.lower()
                    matching_keywords = sum(1 for word in query_lower.split() if word in keywords_lower)
                    score += matching_keywords * 20
                
                # 3. FAQ ID matching (for specific queries)
                faq_id_lower = faq_id.lower()
                if any(word in faq_id_lower for word in query_lower.split()):
                    score += 25
                
                # 4. Sequence similarity
                similarity = SequenceMatcher(None, query_lower, question_lower).ratio()
                score += similarity * 15
                
                # 5. Subject-specific matching
                subjects = ['nlp', 'quantum', 'business', 'data mining', 'robotics', 'project']
                for subject in subjects:
                    if subject in query_lower and subject in faq_id_lower:
                        score += 40
                
                # 6. Detail level matching
                detail_keywords = ['module', 'clo', 'syllabus', 'textbook', 'reference', 'detailed', 'complete']
                if any(keyword in query_lower for keyword in detail_keywords):
                    if any(keyword in faq_id_lower for keyword in detail_keywords):
                        score += 35
                
                if score > 0:
                    scored_results.append({
                        'faq_id': faq_id,
                        'question': question,
                        'answer': answer,
                        'score': score
                    })
            
            # Sort by score and return top results
            scored_results.sort(key=lambda x: x['score'], reverse=True)
            return scored_results[:limit]
            
        except Exception as e:
            print(f"Enhanced search error: {e}")
            return []
    
    def fetch_academic_context(self, db: Session, intent: str, entities: Dict, message: str = "") -> str:
        """Dynamically fetch relevant academic data from database using enhanced search"""
        context_parts = []
        
        try:
            # Use enhanced search for better results
            search_results = self.search_database_enhanced(message, limit=3)
            
            # Use enhanced search results if available
            if search_results and search_results[0]['score'] > 15:  # Lower threshold for more results
                context_parts.append("**Relevant Information:**")
                for result in search_results:
                    context_parts.append(f"Q: {result['question']}")
                    context_parts.append(f"A: {result['answer']}\n")
            
            # ALWAYS also try basic category search for comprehensive coverage
            if intent in ['timetable', 'exam', 'faculty', 'course', 'assignment']:
                faqs = db.query(models.FAQ).filter(
                    models.FAQ.category.like(f'%{intent}%')
                ).limit(3).all()
                
                if faqs:
                    if not context_parts:  # Only add header if no enhanced results
                        context_parts.append("**Relevant FAQs:**")
                    for faq in faqs:
                        # Avoid duplicates
                        faq_text = f"Q: {faq.question}\nA: {faq.answer}\n"
                        if faq_text not in "\n".join(context_parts):
                            context_parts.append(f"Q: {faq.question}")
                            context_parts.append(f"A: {faq.answer}\n")
            
            # Fetch course information
            if intent == 'course' or entities.get('course'):
                courses = db.query(models.Course).all()
                if courses:
                    context_parts.append("\n**Available Courses:**")
                    for course in courses:
                        context_parts.append(
                            f"- {course.course_code}: {course.course_name} "
                            f"({course.credits} credits, Faculty: {course.faculty_theory})"
                        )
            
            # Fetch assignment information
            if intent == 'assignment':
                assignments = db.query(models.Assignment).order_by(
                    models.Assignment.deadline
                ).limit(10).all()
                
                if assignments:
                    context_parts.append("\n**Upcoming Assignments:**")
                    for assignment in assignments:
                        deadline_str = assignment.deadline.strftime('%B %d, %Y')
                        context_parts.append(
                            f"- {assignment.title} ({assignment.course_code}) - "
                            f"Due: {deadline_str}, Marks: {assignment.marks}"
                        )
            
            # Fetch all courses for general queries
            if not context_parts:
                courses = db.query(models.Course).limit(5).all()
                if courses:
                    context_parts.append("**7th Semester Courses:**")
                    for course in courses:
                        context_parts.append(
                            f"- {course.course_code}: {course.course_name}"
                        )
            
        except Exception as e:
            print(f"Error fetching context: {e}")
        
        return "\n".join(context_parts) if context_parts else "No specific data found."
    
    def classify_intent(self, message: str) -> Tuple[str, float]:
        """Classify user intent"""
        msg_lower = message.lower()
        
        # Intent patterns
        if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "greeting", 0.95
        elif any(word in msg_lower for word in ['bye', 'goodbye', 'thanks', 'thank you']):
            return "farewell", 0.95
        elif any(word in msg_lower for word in ['timetable', 'schedule', 'class']):
            return "timetable", 0.90
        elif any(word in msg_lower for word in ['faculty', 'teacher', 'professor', 'hod']):
            return "faculty", 0.90
        elif any(word in msg_lower for word in ['exam', 'test', 'ia', 'assessment']):
            return "exam", 0.90
        elif any(word in msg_lower for word in ['assignment', 'deadline', 'seminar', 'term paper']):
            return "assignment", 0.90
        elif any(word in msg_lower for word in ['course', 'subject', 'syllabus']):
            return "course", 0.90
        elif any(word in msg_lower for word in ['attendance', 'policy']):
            return "attendance", 0.90
        else:
            return "general", 0.70
    
    def extract_entities(self, message: str, intent: str) -> Dict:
        """Extract entities from message"""
        entities = {}
        msg_lower = message.lower()
        
        # Days
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        for day in days:
            if day in msg_lower:
                entities['day'] = day
                break
        
        # Courses
        course_keywords = {
            'nlp': '22AML71',
            'natural language': '22AML71',
            'quantum': '22AML72',
            'business intelligence': '22AML73',
            'bi': '22AML73',
            'data mining': '22AML74A',
            'dmdw': '22AML74A'
        }
        
        for keyword, code in course_keywords.items():
            if keyword in msg_lower:
                entities['course'] = code
                break
        
        return entities
    
    def generate_response(self, message: str, intent: str, entities: Dict, session_id: str, db: Session = None) -> str:
        """Generate response using ONLY Gemini AI with database context"""
        
        # Get database session if not provided
        if db is None:
            db = self.get_db()
        
        try:
            # Fetch relevant data from database
            db_context = self.fetch_academic_context(db, intent, entities, message)
            
            # Check if Gemini is available
            if not self.gemini_available or not self.client:
                return "⚠️ AI service is currently unavailable. Please ensure GEMINI_API_KEY is configured correctly."
            
            # If no relevant database context found, let Gemini use its knowledge as last resort
            use_gemini_knowledge = len(db_context.strip()) < 50 or "No specific data found" in db_context
            
            # Use Gemini AI for ALL responses (including greetings)
            try:
                history = self.conversation_history.get(session_id, [])
                context_messages = "\n".join([
                    f"User: {h['user']}\nBot: {h['bot']}" 
                    for h in history[-3:]
                ])
                
                if use_gemini_knowledge:
                    prompt = f"""You are an AI assistant for Global Academy of Technology, Department of AI & ML, 7th Semester.

**Context:** The specific information requested is not available in the current database, but you can provide general academic guidance.

**Previous Conversation:**
{context_messages if context_messages else "No previous conversation"}

**Student Question:** "{message}"

**Instructions:**
- The database doesn't have specific details for this query
- Provide helpful general information based on your knowledge of academic institutions
- Be honest that specific details aren't available in the database
- Suggest contacting the department office for specific information
- Keep responses helpful and professional
- For faculty questions, mention common academic roles and suggest contacting the department

**Response:**"""
                else:
                    prompt = f"""You are an AI assistant for Global Academy of Technology, Department of AI & ML, 7th Semester.

**Database Information:**
{db_context}

**Previous Conversation:**
{context_messages if context_messages else "No previous conversation"}

**Student Question:** "{message}"

**Instructions:**
- You MUST use the database information provided above to answer questions
- Provide specific details from the database (course codes, faculty names, dates, deadlines, etc.)
- Be helpful, friendly, and professional
- Format responses with bullet points or lists when showing multiple items
- Keep responses concise but informative (2-5 sentences for simple queries, more for complex ones)

**Response:**"""
                
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                if response and response.text:
                    bot_response = response.text.strip()
                    self._update_history(session_id, message, bot_response)
                    return bot_response
                else:
                    return "⚠️ Unable to generate response. Please try again."
                    
            except Exception as e:
                error_msg = f"⚠️ Error communicating with AI service: {str(e)}"
                print(f"Gemini error: {e}")
                return error_msg
            
        finally:
            if db:
                db.close()
    
    
    def _update_history(self, session_id: str, user_msg: str, bot_msg: str):
        """Update conversation history"""
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        self.conversation_history[session_id].append({
            'user': user_msg,
            'bot': bot_msg,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 exchanges
        if len(self.conversation_history[session_id]) > 10:
            self.conversation_history[session_id] = self.conversation_history[session_id][-10:]
    
    def clear_session(self, session_id: str):
        """Clear conversation history"""
        if session_id in self.conversation_history:
            del self.conversation_history[session_id]

# Singleton instance
dynamic_chatbot_service = DynamicChatbotService()
