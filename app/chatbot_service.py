"""
Academic Chatbot Service using Google Gemini AI
"""
from typing import Dict, Tuple, Optional
from datetime import datetime
import os
import json

# Import Gemini
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: Google Gemini SDK not available")

ACADEMIC_CONTEXT = """
You are an AI assistant for Global Academy of Technology, Department of Artificial Intelligence and Machine Learning.
Academic Year: 2025-2026, Semester VII

COURSES (7th Semester):
1. 22AML71 - Natural Language Processing (Prof. Vasugi I)
2. 22AML72 - Quantum Computing (Dr. Roopa B S - HOD)
3. 22AML73 - Business Intelligence (Prof. Prasanna N)
4. 22AML74A - Data Mining & Data Warehousing (Prof. Vani)
5. 22AML76 - Major Project Phase-II

FACULTY:
- HOD: Dr. Roopa B S
- Class Teacher: Prof. Prasanna N
- Coordinator: Prof. Vani
- NLP Faculty: Prof. Vasugi I

IMPORTANT DATES:
- IA1: Oct 6-8, 2025
- IA2: Nov 20-22, 2025
- Lab Exams: Nov 24-29, 2025
- Last Working Day: Dec 4, 2025

POLICIES:
- Minimum 85% attendance mandatory
- CIE: Best 2 of 3 tests
- SEE: 3 hours, answer 5 of 10 questions

Provide accurate, helpful, and concise responses.
"""

class ChatbotService:
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
        elif any(word in msg_lower for word in ['faculty', 'teacher', 'professor']):
            return "faculty", 0.90
        elif any(word in msg_lower for word in ['exam', 'test', 'ia', 'assessment']):
            return "exam", 0.90
        elif any(word in msg_lower for word in ['assignment', 'deadline', 'project']):
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
        if 'nlp' in msg_lower or 'natural language' in msg_lower:
            entities['course'] = 'NLP'
        elif 'quantum' in msg_lower:
            entities['course'] = 'Quantum Computing'
        elif 'business' in msg_lower or 'bi' in msg_lower:
            entities['course'] = 'Business Intelligence'
        elif 'data mining' in msg_lower or 'dmdw' in msg_lower:
            entities['course'] = 'Data Mining'
        
        return entities
    
    def generate_response(self, message: str, intent: str, entities: Dict, session_id: str) -> str:
        """Generate response using Gemini or fallback"""
        
        # Try fallback first for specific queries
        fallback = self._get_fallback_response(message, intent, entities)
        if fallback and not fallback.startswith("I can help"):
            self._update_history(session_id, message, fallback)
            return fallback
        
        # Try Gemini for general queries
        if self.gemini_available and self.client:
            try:
                history = self.conversation_history.get(session_id, [])
                context_messages = "\n".join([
                    f"User: {h['user']}\nBot: {h['bot']}" 
                    for h in history[-3:]
                ])
                
                prompt = f"""{ACADEMIC_CONTEXT}

Previous Conversation:
{context_messages if context_messages else "No previous conversation"}

Student Question: "{message}"

Provide a helpful, accurate, and concise response (2-4 sentences)."""
                
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                if response and response.text:
                    bot_response = response.text.strip()
                    self._update_history(session_id, message, bot_response)
                    return bot_response
                    
            except Exception as e:
                print(f"Gemini error: {e}")
        
        return fallback
    
    def _get_fallback_response(self, message: str, intent: str, entities: Dict) -> str:
        """Fallback responses"""
        msg_lower = message.lower()
        
        if intent == "greeting":
            return "Hello! I'm your AIML Academic Assistant 🎓\n\nI can help you with:\n• Class timetables 📅\n• Course information 📚\n• Exam schedules 📝\n• Faculty details 👨‍🏫\n• Assignment deadlines ⏰\n\nWhat would you like to know?"
        
        elif intent == "farewell":
            return "You're welcome! Feel free to ask anytime. Good luck with your studies! 📚"
        
        elif intent == "timetable":
            day = entities.get('day', '').lower()
            if day == 'monday':
                return "**Monday Schedule:**\n• 8:30-9:30: NLP (AIB-401)\n• 9:30-10:30: Data Mining (AIB-401)\n• 11:00-12:00: Open Elective\n• 12:00-1:00: Quantum Computing (AIB-402)\n• 2:00-4:00: Major Project"
            elif day == 'tuesday':
                return "**Tuesday Schedule:**\n• 8:30-9:30: Business Intelligence (AIB-402)\n• 9:30-1:00: Major Project\n• 2:00-3:00: Data Mining (AIB-402)\n• 3:00-4:00: Quantum Computing Lab"
            elif day == 'wednesday':
                return "**Wednesday Schedule:**\n• 8:30-9:30: NLP (AIB-402)\n• 9:30-10:30: Data Mining (AIB-402)\n• 11:00-12:00: Quantum Computing (AIB-402)\n• 12:00-1:00: Business Intelligence (AIB-402)\n• 2:00-3:00: NLP (AIB-402)"
            elif day == 'thursday':
                return "**Thursday Schedule:**\n• 8:30-9:30: Business Intelligence Tutorial\n• 9:30-10:30: Business Intelligence\n• 11:00-12:00: Open Elective\n• 12:00-1:00: NLP\n• 2:00-4:00: Major Project"
            elif day == 'friday':
                return "**Friday Schedule:**\n• 8:30-1:00: Skill Lab / Upskill\n• 2:00-4:00: Major Project"
            else:
                return "Please specify which day's timetable you'd like to see (Monday to Friday)."
        
        elif intent == "faculty":
            return "**Faculty Information:**\n\n• **HOD**: Dr. Roopa B S - Quantum Computing\n• **Class Teacher**: Prof. Prasanna N - Business Intelligence\n• **Coordinator**: Prof. Vani - Data Mining\n• **NLP Faculty**: Prof. Vasugi I\n• **Project Coordinators**: Prof. C Christlin Shanuja, Prof. Vasugi I"
        
        elif intent == "exam":
            return "**Important Exam Dates:**\n\n📅 **IA1**: October 6-8, 2025\n📅 **IA2**: November 20-22, 2025\n📅 **Lab Exams**: November 24-29, 2025\n📅 **CIE Freeze**: December 1, 2025\n\n**Evaluation:**\n• CIE: 50 marks (Best 2 of 3 tests)\n• SEE: 50 marks (3 hours)"
        
        elif intent == "course":
            return "**7th Semester Courses:**\n\n1. **22AML71** - Natural Language Processing (4 credits)\n2. **22AML72** - Quantum Computing (4 credits)\n3. **22AML73** - Business Intelligence (4 credits)\n4. **22AML74A** - Data Mining & Data Warehousing (3 credits)\n5. **22AML76** - Major Project Phase-II (6 credits)"
        
        elif intent == "attendance":
            return "**Academic Policies:**\n\n📊 **Attendance**: Minimum 85% mandatory\n📊 **CIE**: Best 2 of 3 tests (30+30 marks)\n📊 **SEE**: 3 hours, answer 5 of 10 questions\n📊 **Total Credits**: 21 credits this semester"
        
        elif intent == "assignment":
            return "**Assignment Information:**\n\n📝 **Seminar 1**: Mid-October (10 marks)\n📝 **Term Papers**: Mid-November (10 marks)\n📝 **Mini Projects**: End of semester (20 marks)\n\nCheck with your course instructors for specific deadlines!"
        
        return "I can help you with:\n• Class timetables 📅\n• Course information 📚\n• Exam schedules 📝\n• Faculty details 👨‍🏫\n• Assignment deadlines ⏰\n\nWhat would you like to know?"
    
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
chatbot_service = ChatbotService()
