import os
from dotenv import load_dotenv
load_dotenv()

from app.database import DATABASE_URL, SessionLocal
from app.models import User

print(f"Database URL: {DATABASE_URL}")
print(f"Database file: {DATABASE_URL.replace('sqlite:///', '')}")

db = SessionLocal()
user_count = db.query(User).count()
print(f"Users in database: {user_count}")

users = db.query(User).all()
for u in users:
    print(f"  - {u.username} ({u.email})")

db.close()
