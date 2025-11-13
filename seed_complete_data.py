"""
Seed complete academic data including SEE dates, timetable, and calendar
"""
import os
os.environ['DATABASE_URL'] = 'sqlite:///./feedback.db'

from app.database import SessionLocal, engine, Base
from app import models
import json
from datetime import datetime, timedelta

# Create all tables
Base.metadata.create_all(bind=engine)

def seed_complete_faqs(db):
    print("Seeding Complete FAQs...")
    
    # Delete existing FAQs
    db.query(models.FAQ).delete()
    db.commit()
    
    faqs_data = [
        # SEE Exam Schedule
        {"faq_id": "SEE001", "question": "When is the SEE exam for NLP?", 
         "answer": "SEE exam for 22AML71 - Natural Language Processing is on 16.12.2025 (Tuesday) from 2:00 PM to 5:00 PM.",
         "category": "exam", "keywords": json.dumps(["see", "nlp", "22aml71", "exam date"])},
        
        {"faq_id": "SEE002", "question": "When is the SEE exam for Quantum Computing?",
         "answer": "SEE exam for 22AML72 - Quantum Computing is on 18.12.2025 (Thursday) from 2:00 PM to 5:00 PM.",
         "category": "exam", "keywords": json.dumps(["see", "quantum", "22aml72", "exam date"])},
        
        {"faq_id": "SEE003", "question": "When is the SEE exam for Business Intelligence?",
         "answer": "SEE exam for 22AML73 - Business Intelligence is on 22.12.2025 (Monday) from 2:00 PM to 5:00 PM.",
         "category": "exam", "keywords": json.dumps(["see", "business intelligence", "22aml73", "exam date"])},
        
        {"faq_id": "SEE004", "question": "When is the SEE exam for Data Mining?",
         "answer": "SEE exam for 22AML74 - Data Mining and Data Warehousing is on 24.12.2025 (Wednesday) from 2:00 PM to 5:00 PM.",
         "category": "exam", "keywords": json.dumps(["see", "data mining", "22aml74", "exam date"])},
        
        {"faq_id": "SEE005", "question": "When is the SEE exam for Addictive Manufacturing?",
         "answer": "SEE exam for 22AML75 - Addictive Manufacturing is on 29.12.2025 (Monday) from 2:00 PM to 5:00 PM.",
         "category": "exam", "keywords": json.dumps(["see", "addictive manufacturing", "22aml75", "exam date"])},
        
        {"faq_id": "SEE006", "question": "When are SEE practical exams?",
         "answer": "SEE practical examinations will be held between 2nd January 2026 and 10th January 2026.",
         "category": "exam", "keywords": json.dumps(["see", "practical", "lab exam"])},
        
        {"faq_id": "SEE007", "question": "What is the SEE exam timing?",
         "answer": "All SEE theory exams for VII Semester are from 2:00 PM to 5:00 PM (3 hours duration).",
         "category": "exam", "keywords": json.dumps(["see", "timing", "duration"])},
        
        # Monday Timetable
        {"faq_id": "TT001", "question": "What is Monday's timetable?",
         "answer": "Monday: 8:30-9:30 AM 22AML71 (NLP), 9:30-10:30 AM 22AML74A (Open Elective), Break 10:30-11:00 AM, 11:00-12:00 PM 22AML72 (Quantum), 12:00-1:00 PM 22AML76 (Major Project), Lunch 1:00-2:00 PM, 2:00-3:00 PM 22AML73 (BI), 3:00-4:00 PM 22AML76 (Major Project).",
         "category": "timetable", "keywords": json.dumps(["monday", "schedule", "timetable"])},
        
        # Tuesday Timetable
        {"faq_id": "TT002", "question": "What is Tuesday's timetable?",
         "answer": "Tuesday: 8:30-9:30 AM 22AML76 (Major Project), 9:30-10:30 AM 22AML72 (Quantum), Break 10:30-11:00 AM, 11:00-12:00 PM 22AML71 (NLP), 12:00-1:00 PM Skill Lab, Lunch 1:00-2:00 PM, 2:00-3:00 PM 22AML73(T) (BI Theory).",
         "category": "timetable", "keywords": json.dumps(["tuesday", "schedule", "timetable"])},
        
        # Wednesday Timetable
        {"faq_id": "TT003", "question": "What is Wednesday's timetable?",
         "answer": "Wednesday: 8:30-9:30 AM 22AML73 (BI), 9:30-10:30 AM Open Elective, Break 10:30-11:00 AM, 11:00-12:00 PM 22AML71 (NLP), 12:00-1:00 PM 22AML76 (Major Project), Lunch 1:00-2:00 PM, 2:00-4:00 PM 22AML76 (Major Project - 2 hours).",
         "category": "timetable", "keywords": json.dumps(["wednesday", "schedule", "timetable"])},
        
        # Thursday Timetable
        {"faq_id": "TT004", "question": "What is Thursday's timetable?",
         "answer": "Thursday: 8:30-9:30 AM 22AML74A (Data Mining) in AIB-401, 9:30-10:30 AM 22AML71 (NLP) in AIB-402, Break 10:30-11:00 AM, 11:00-12:00 PM 22AML72 (Quantum Lab) in AIB-Lab1.",
         "category": "timetable", "keywords": json.dumps(["thursday", "schedule", "timetable"])},
        
        # Friday Timetable
        {"faq_id": "TT005", "question": "What is Friday's timetable?",
         "answer": "Friday: 8:30-9:30 AM 22AML74A (Data Mining) in AIB-402, 9:30-10:30 AM 22AML72 (Quantum) in AIB-402, Break 10:30-11:00 AM, 11:00-12:00 PM 22AML73 (BI) in AIB-402.",
         "category": "timetable", "keywords": json.dumps(["friday", "schedule", "timetable"])},
        
        # Faculty Information
        {"faq_id": "FAC001", "question": "Who is the class teacher?",
         "answer": "Prof. Prasanna N is the Class Teacher for VII Semester AI & ML.",
         "category": "faculty", "keywords": json.dumps(["class teacher", "prasanna"])},
        
        {"faq_id": "FAC002", "question": "Who teaches Natural Language Processing?",
         "answer": "Prof. Vasugi I (VI) teaches 22AML71 Natural Language Processing.",
         "category": "faculty", "keywords": json.dumps(["nlp", "vasugi", "22aml71"])},
        
        {"faq_id": "FAC003", "question": "Who teaches Quantum Computing?",
         "answer": "Dr. Roopa BS (RBS) teaches 22AML72 Quantum Computing.",
         "category": "faculty", "keywords": json.dumps(["quantum", "roopa", "22aml72"])},
        
        {"faq_id": "FAC004", "question": "Who teaches Business Intelligence?",
         "answer": "Prof. Prasanna N teaches 22AML73 Business Intelligence.",
         "category": "faculty", "keywords": json.dumps(["business intelligence", "prasanna", "22aml73"])},
        
        {"faq_id": "FAC005", "question": "Who teaches Data Mining?",
         "answer": "Prof. Vani teaches 22AML74A Data Mining and Data Warehousing.",
         "category": "faculty", "keywords": json.dumps(["data mining", "vani", "22aml74a"])},
        
        {"faq_id": "FAC006", "question": "Who coordinates Major Project?",
         "answer": "22AML76 Major Project Phase-II is coordinated by Prof. C Christlin Shanuja (CS) and Prof. Vasugi I (VI).",
         "category": "faculty", "keywords": json.dumps(["major project", "christlin", "vasugi", "22aml76"])},
        
        {"faq_id": "FAC007", "question": "Who coordinates Skill Lab?",
         "answer": "Skill Lab is coordinated by Prof. C Christlin Shanuja (CS) and Prof. Vani.",
         "category": "faculty", "keywords": json.dumps(["skill lab", "christlin", "vani"])},
        
        # Calendar Events
        {"faq_id": "CAL001", "question": "When does the semester start?",
         "answer": "Odd Semester 7 commenced on 18th August 2025 (Monday).",
         "category": "calendar", "keywords": json.dumps(["semester start", "commencement"])},
        
        {"faq_id": "CAL002", "question": "When is the last working day?",
         "answer": "The last working day of Odd Semester 7 is 22nd November 2025 (Friday).",
         "category": "calendar", "keywords": json.dumps(["last day", "semester end"])},
        
        {"faq_id": "CAL003", "question": "When is IA1?",
         "answer": "IA1 question papers must be submitted to COE on 26th September 2025. The exam will be conducted in the following week (6-11 October 2025).",
         "category": "exam", "keywords": json.dumps(["ia1", "internal assessment"])},
        
        {"faq_id": "CAL004", "question": "When is IA2?",
         "answer": "IA2 question papers must be submitted to COE on 3rd November 2025. The exam will be conducted in the following week.",
         "category": "exam", "keywords": json.dumps(["ia2", "internal assessment"])},
        
        {"faq_id": "CAL005", "question": "When are Open Elective exams?",
         "answer": "Open Elective exams are scheduled on 8th October 2025 (Afternoon) and 12th November 2025 (Afternoon).",
         "category": "exam", "keywords": json.dumps(["open elective", "exam"])},
        
        {"faq_id": "CAL006", "question": "When is Parent Teacher Meeting?",
         "answer": "Parent Teacher Meeting Week is scheduled during 6-11 October 2025.",
         "category": "event", "keywords": json.dumps(["ptm", "parent teacher meeting"])},
        
        {"faq_id": "CAL007", "question": "When is Class Committee Meeting?",
         "answer": "Class Committee Meeting Week is scheduled during 1-6 September 2025.",
         "category": "event", "keywords": json.dumps(["class committee", "meeting"])},
        
        {"faq_id": "CAL008", "question": "When is Remedial Class Week?",
         "answer": "Remedial Class Week is scheduled during 13-18 October 2025.",
         "category": "event", "keywords": json.dumps(["remedial", "class"])},
        
        # Holidays
        {"faq_id": "HOL001", "question": "What are the holidays in this semester?",
         "answer": "Holidays: 27 Aug (Varasiddhi Vinayaka Vratha), 1 Oct (Maha Navami/Vijayadashami), 2 Oct (Gandhi Jayanthi), 20 Oct (Diwali), 22 Oct (Balipadyami). Also, every 1st and 3rd Saturday of the month are holidays.",
         "category": "holiday", "keywords": json.dumps(["holiday", "festival", "saturday"])},
        
        {"faq_id": "HOL002", "question": "Are Saturdays holidays?",
         "answer": "Every 1st and 3rd Saturday of the month are holidays. Working Saturdays are utilized for Personality Development, Placement Training, Aptitude Training and Non-Academic Activities.",
         "category": "holiday", "keywords": json.dumps(["saturday", "holiday", "working day"])},
        
        # Academic Policies
        {"faq_id": "POL001", "question": "What is the attendance requirement?",
         "answer": "85% attendance is mandatory for all courses in the semester.",
         "category": "policy", "keywords": json.dumps(["attendance", "policy", "mandatory"])},
        
        {"faq_id": "POL002", "question": "When should VAC/Certification documents be submitted?",
         "answer": "Report/Document relevant to VAC/Certification courses conducted by the department should be submitted to IQAC on or before 22nd November 2025.",
         "category": "policy", "keywords": json.dumps(["vac", "certification", "submission"])},
        
        {"faq_id": "POL003", "question": "When should Co-Po Mapping be completed?",
         "answer": "Co-Po Mapping have to be completed on or before 22nd December 2025.",
         "category": "policy", "keywords": json.dumps(["co-po", "mapping", "deadline"])},
        
        # Working Days
        {"faq_id": "WD001", "question": "How many working days are there?",
         "answer": "Total working days: Monday-13, Tuesday-14, Wednesday-11, Thursday-13, Friday-14, Saturday-8. Classroom interactive days: Monday-11, Tuesday-12, Wednesday-9, Thursday-13, Friday-14, Saturday-8.",
         "category": "calendar", "keywords": json.dumps(["working days", "interactive days"])},
        
        # Contact Information
        {"faq_id": "CONT001", "question": "What is the college contact information?",
         "answer": "Global Academy of Technology, Ideal Homes Township, Rajarajeshwari Nagar, Bangalore-560 098. Phone: +91-080-28603158, 28603157. Email: info@gat.ac.in. Website: www.gat.ac.in",
         "category": "contact", "keywords": json.dumps(["contact", "phone", "email", "address"])},
        
        # Classroom Information
        {"faq_id": "CLASS001", "question": "Which classrooms are used?",
         "answer": "Classes are held in classrooms AIB-401 and AIB-402. Lab sessions are conducted in AIB-Lab1.",
         "category": "facility", "keywords": json.dumps(["classroom", "lab", "location"])},
        
        {"faq_id": "CLASS002", "question": "When is the timetable effective from?",
         "answer": "The timetable for Academic Year 2025-2026 (Odd Semester) for Semester VII is effective from 18th August 2025.",
         "category": "timetable", "keywords": json.dumps(["timetable", "effective date"])},
    ]
    
    for faq_data in faqs_data:
        faq = models.FAQ(**faq_data)
        db.add(faq)
    
    db.commit()
    print(f"  Added {len(faqs_data)} FAQs")

def seed_courses_complete(db):
    print("Seeding Complete Courses...")
    
    # Delete existing courses
    db.query(models.Course).delete()
    db.commit()
    
    courses_data = [
        {"course_code": "22AML71", "course_name": "Natural Language Processing", "course_type": "IPC", "credits": 4,
         "faculty_theory": "Prof. Vasugi I", "faculty_lab": "Prof. Vasugi I", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "4L + 2P", "see_duration": "3 hours"},
        
        {"course_code": "22AML72", "course_name": "Quantum Computing", "course_type": "IPC", "credits": 4,
         "faculty_theory": "Dr. Roopa BS", "faculty_lab": "Dr. Roopa BS", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "4L + 2P", "see_duration": "3 hours"},
        
        {"course_code": "22AML73", "course_name": "Business Intelligence", "course_type": "PC", "credits": 4,
         "faculty_theory": "Prof. Prasanna N", "faculty_lab": "Prof. Prasanna N", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "4L + 2P", "see_duration": "3 hours"},
        
        {"course_code": "22AML74A", "course_name": "Data Mining & Data Warehousing", "course_type": "PEC", "credits": 3,
         "faculty_theory": "Prof. Vani", "faculty_lab": "Prof. Vani", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "3L + 2P", "see_duration": "3 hours"},
        
        {"course_code": "22AML75", "course_name": "Addictive Manufacturing", "course_type": "Elective", "credits": 3,
         "faculty_theory": "TBD", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "3L", "see_duration": "3 hours"},
        
        {"course_code": "22AML75A", "course_name": "Business Intelligence (Open Elective)", "course_type": "Open Elective", "credits": 3,
         "faculty_theory": "Prof. Sushmitha M", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "3L", "see_duration": "3 hours"},
        
        {"course_code": "22AML76", "course_name": "Major Project Phase-II", "course_type": "Project", "credits": 6,
         "faculty_theory": "Prof. C Christlin Shanuja, Prof. Vasugi I", "semester": 7,
         "cie_marks": 50, "see_marks": 50, "hours_per_week": "12 hours", "see_duration": "N/A"},
    ]
    
    for course_data in courses_data:
        course = models.Course(**course_data)
        db.add(course)
    
    db.commit()
    print(f"  Added {len(courses_data)} courses")

def seed_assignments_complete(db):
    print("Seeding Complete Assignments...")
    
    # Delete existing assignments
    db.query(models.Assignment).delete()
    db.commit()
    
    assignments_data = [
        # NLP Assignments
        {"course_code": "22AML71", "title": "Seminar 1 - Regular Expressions and Text Processing", 
         "assignment_type": "seminar", "deadline": datetime(2025, 11, 20), "marks": 10,
         "description": "Present on regular expressions, tokenization, and text preprocessing techniques."},
        {"course_code": "22AML71", "title": "Term Paper - N-gram Language Models", 
         "assignment_type": "term_paper", "deadline": datetime(2025, 11, 27), "marks": 10,
         "description": "Write a comprehensive term paper on N-gram language models and their applications."},
        {"course_code": "22AML71", "title": "Mini Project - Sentiment Analysis System", 
         "assignment_type": "mini_project", "deadline": datetime(2025, 12, 10), "marks": 20,
         "description": "Develop a sentiment analysis system using NLP techniques."},
        
        # Quantum Computing Assignments
        {"course_code": "22AML72", "title": "Seminar 1 - Quantum Gates and Circuits", 
         "assignment_type": "seminar", "deadline": datetime(2025, 11, 22), "marks": 10,
         "description": "Present on quantum gates, quantum circuits, and quantum algorithms."},
        {"course_code": "22AML72", "title": "Lab Assignment - Quantum Circuit Implementation", 
         "assignment_type": "lab_assignment", "deadline": datetime(2025, 12, 5), "marks": 15,
         "description": "Implement quantum circuits using Qiskit or similar framework."},
        {"course_code": "22AML72", "title": "Mini Project - Quantum Algorithm Simulation", 
         "assignment_type": "mini_project", "deadline": datetime(2025, 12, 12), "marks": 20,
         "description": "Simulate a quantum algorithm (Grover's or Shor's algorithm)."},
        
        # Business Intelligence Assignments
        {"course_code": "22AML73", "title": "Case Study - BI Dashboard Design", 
         "assignment_type": "case_study", "deadline": datetime(2025, 11, 25), "marks": 10,
         "description": "Analyze and design a Business Intelligence dashboard for a real-world scenario."},
        {"course_code": "22AML73", "title": "Mini Project - Data Visualization and Analytics", 
         "assignment_type": "mini_project", "deadline": datetime(2025, 12, 8), "marks": 20,
         "description": "Create an interactive data visualization and analytics solution."},
        
        # Data Mining Assignments
        {"course_code": "22AML74A", "title": "Seminar 1 - Association Rules and Market Basket Analysis", 
         "assignment_type": "seminar", "deadline": datetime(2025, 11, 23), "marks": 10,
         "description": "Present on association rule mining and market basket analysis techniques."},
        {"course_code": "22AML74A", "title": "Mini Project - Clustering and Classification Analysis", 
         "assignment_type": "mini_project", "deadline": datetime(2025, 12, 6), "marks": 20,
         "description": "Implement clustering and classification algorithms on a real dataset."},
        
        # Major Project
        {"course_code": "22AML76", "title": "Major Project Phase-II - Mid Review", 
         "assignment_type": "project_review", "deadline": datetime(2025, 10, 15), "marks": 25,
         "description": "Mid-semester review of Major Project Phase-II progress."},
        {"course_code": "22AML76", "title": "Major Project Phase-II - Final Submission", 
         "assignment_type": "project_submission", "deadline": datetime(2025, 11, 20), "marks": 25,
         "description": "Final submission and presentation of Major Project Phase-II."},
    ]
    
    for assignment_data in assignments_data:
        assignment = models.Assignment(**assignment_data)
        db.add(assignment)
    
    db.commit()
    print(f"  Added {len(assignments_data)} assignments")

print("=" * 60)
print("Seeding Complete Academic Data to feedback.db")
print("=" * 60)

db = SessionLocal()

try:
    seed_complete_faqs(db)
    seed_courses_complete(db)
    seed_assignments_complete(db)
    
    print("\n" + "=" * 60)
    print("Complete Database Seeding Finished!")
    print("=" * 60)
    
    faq_count = db.query(models.FAQ).count()
    course_count = db.query(models.Course).count()
    assignment_count = db.query(models.Assignment).count()
    
    print(f"\nFinal Database Statistics:")
    print(f"  FAQs: {faq_count}")
    print(f"  Courses: {course_count}")
    print(f"  Assignments: {assignment_count}")
    print(f"\nData includes:")
    print(f"  - SEE exam dates (16-29 Dec 2025)")
    print(f"  - Complete daily timetable (Mon-Fri)")
    print(f"  - Calendar of events (Aug-Nov 2025)")
    print(f"  - Faculty information")
    print(f"  - Holiday list")
    print(f"  - Academic policies")
    print(f"  - Contact information")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
