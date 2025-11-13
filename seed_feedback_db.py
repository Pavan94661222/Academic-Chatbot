"""
Seed feedback.db with academic data
"""
import os
os.environ['DATABASE_URL'] = 'sqlite:///./feedback.db'

from app.database import SessionLocal, engine, Base
from app import models
import json
from datetime import datetime, timedelta

# Create all tables
Base.metadata.create_all(bind=engine)

def seed_faqs(db):
    print("Seeding FAQs...")
    existing = db.query(models.FAQ).first()
    if existing:
        print("  FAQs already exist, skipping...")
        return
    
    faqs_data = [
        {"faq_id": "FAQ101", "question": "What is my class schedule?", 
         "answer": "Your 7th semester timetable runs Monday to Friday, 8:30 AM to 4:00 PM with breaks at 10:30-11:00 AM and 1:00-2:00 PM.",
         "category": "timetable", "keywords": json.dumps(["schedule", "timetable", "classes"])},
        
        {"faq_id": "FAQ102", "question": "When is my NLP class?",
         "answer": "NLP (22AML71) classes: Monday 8:30-9:30 (AIB-401), Wednesday 8:30-9:30 and 2:00-3:00 (AIB-402), Thursday 12:00-1:00.",
         "category": "timetable", "keywords": json.dumps(["nlp", "22aml71"])},
        
        {"faq_id": "FAQ103", "question": "What classes do I have on Monday?",
         "answer": "Monday: 8:30-9:30 NLP (AIB-401), 9:30-10:30 Data Mining (AIB-401), 11:00-12:00 Open Elective, 12:00-1:00 Quantum Computing (AIB-402), 2:00-4:00 Major Project.",
         "category": "timetable", "keywords": json.dumps(["monday", "schedule"])},
        
        {"faq_id": "FAQ201", "question": "Who is the HOD?",
         "answer": "Dr. Roopa B S is the Head of Department for AI & ML. She teaches Quantum Computing (22AML72).",
         "category": "faculty", "keywords": json.dumps(["hod", "roopa"])},
        
        {"faq_id": "FAQ202", "question": "Who is my class teacher?",
         "answer": "Prof. Prasanna N is your class teacher. He teaches Business Intelligence (22AML73).",
         "category": "faculty", "keywords": json.dumps(["class teacher", "prasanna"])},
        
        {"faq_id": "FAQ203", "question": "Who teaches NLP?",
         "answer": "Prof. Vasugi I teaches Natural Language Processing (22AML71) for both theory and lab.",
         "category": "faculty", "keywords": json.dumps(["nlp", "vasugi"])},
        
        {"faq_id": "FAQ301", "question": "When is IA1?",
         "answer": "IA1 is scheduled for October 6-8, 2025. Question papers must be submitted by September 26, 2025.",
         "category": "exam", "keywords": json.dumps(["ia1", "exam"])},
        
        {"faq_id": "FAQ302", "question": "How are CIE marks calculated?",
         "answer": "CIE (50 marks): Best 2 of 3 tests (30+30 marks average) for theory. For labs: Tests (30) + Lab work (20).",
         "category": "exam", "keywords": json.dumps(["cie", "marks"])},
        
        {"faq_id": "FAQ303", "question": "What is the SEE exam pattern?",
         "answer": "SEE: 3 hours, 10 questions (2 per module, 20 marks each). Answer any 5 questions (one from each module).",
         "category": "exam", "keywords": json.dumps(["see", "exam pattern"])},
        
        {"faq_id": "FAQ401", "question": "What is the attendance requirement?",
         "answer": "Minimum 85% attendance is mandatory for all courses.",
         "category": "attendance", "keywords": json.dumps(["attendance", "policy"])},
    ]
    
    for faq_data in faqs_data:
        faq = models.FAQ(**faq_data)
        db.add(faq)
    
    db.commit()
    print(f"  Added {len(faqs_data)} FAQs")

def seed_courses(db):
    print("Seeding Courses...")
    existing = db.query(models.Course).first()
    if existing:
        print("  Courses already exist, skipping...")
        return
    
    courses_data = [
        {"course_code": "22AML71", "course_name": "Natural Language Processing", "course_type": "IPC", "credits": 4,
         "faculty_theory": "Prof. Vasugi I", "faculty_lab": "Prof. Vasugi I", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "4L + 2P", "see_duration": "3 hours"},
        
        {"course_code": "22AML72", "course_name": "Quantum Computing", "course_type": "IPC", "credits": 4,
         "faculty_theory": "Dr. Roopa B S", "faculty_lab": "Dr. Roopa B S", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "4L + 2P", "see_duration": "3 hours"},
        
        {"course_code": "22AML73", "course_name": "Business Intelligence", "course_type": "PC", "credits": 4,
         "faculty_theory": "Prof. Prasanna N", "faculty_lab": "Prof. Prasanna N", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "4L + 2P", "see_duration": "3 hours"},
        
        {"course_code": "22AML74A", "course_name": "Data Mining & Data Warehousing", "course_type": "PEC", "credits": 3,
         "faculty_theory": "Prof. Vani", "faculty_lab": "Prof. Vani", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "3L + 2P", "see_duration": "3 hours"},
        
        {"course_code": "22AML76", "course_name": "Major Project Phase-II", "course_type": "Project", "credits": 6,
         "faculty_theory": "Prof. C Christlin Shanuja, Prof. Vasugi I", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "12 hours", "see_duration": "N/A"},
    ]
    
    for course_data in courses_data:
        course = models.Course(**course_data)
        db.add(course)
    
    db.commit()
    print(f"  Added {len(courses_data)} courses")

def seed_assignments(db):
    print("Seeding Assignments...")
    existing = db.query(models.Assignment).first()
    if existing:
        print("  Assignments already exist, skipping...")
        return
    
    base_date = datetime(2025, 11, 15)
    
    assignments_data = [
        {"course_code": "22AML71", "title": "Seminar 1 - Regular Expressions", 
         "assignment_type": "seminar", "deadline": base_date + timedelta(days=7), "marks": 10},
        {"course_code": "22AML71", "title": "Term Paper - N-gram Language Models", 
         "assignment_type": "term_paper", "deadline": base_date + timedelta(days=14), "marks": 10},
        {"course_code": "22AML71", "title": "Mini Project - Sentiment Analysis", 
         "assignment_type": "mini_project", "deadline": base_date + timedelta(days=30), "marks": 20},
        {"course_code": "22AML72", "title": "Seminar 1 - Quantum Gates", 
         "assignment_type": "seminar", "deadline": base_date + timedelta(days=10), "marks": 10},
        {"course_code": "22AML72", "title": "Lab Assignment - Quantum Circuits", 
         "assignment_type": "lab_assignment", "deadline": base_date + timedelta(days=20), "marks": 15},
        {"course_code": "22AML73", "title": "Case Study - BI Dashboard", 
         "assignment_type": "case_study", "deadline": base_date + timedelta(days=12), "marks": 10},
        {"course_code": "22AML73", "title": "Mini Project - Data Visualization", 
         "assignment_type": "mini_project", "deadline": base_date + timedelta(days=25), "marks": 20},
        {"course_code": "22AML74A", "title": "Seminar 1 - Association Rules", 
         "assignment_type": "seminar", "deadline": base_date + timedelta(days=8), "marks": 10},
        {"course_code": "22AML74A", "title": "Mini Project - Clustering Analysis", 
         "assignment_type": "mini_project", "deadline": base_date + timedelta(days=28), "marks": 20},
    ]
    
    for assignment_data in assignments_data:
        assignment = models.Assignment(**assignment_data)
        db.add(assignment)
    
    db.commit()
    print(f"  Added {len(assignments_data)} assignments")

print("=" * 50)
print("Seeding feedback.db")
print("=" * 50)

db = SessionLocal()

try:
    seed_faqs(db)
    seed_courses(db)
    seed_assignments(db)
    
    print("\n" + "=" * 50)
    print("Database seeding completed!")
    print("=" * 50)
    
    faq_count = db.query(models.FAQ).count()
    course_count = db.query(models.Course).count()
    assignment_count = db.query(models.Assignment).count()
    
    print(f"\nDatabase Statistics:")
    print(f"  FAQs: {faq_count}")
    print(f"  Courses: {course_count}")
    print(f"  Assignments: {assignment_count}")
    
except Exception as e:
    print(f"\nError: {e}")
    db.rollback()
finally:
    db.close()
