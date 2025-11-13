from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Simple, fast database configuration
if "sqlite" in settings.DATABASE_URL:
    # SQLite optimizations for local development
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        connect_args={
            "check_same_thread": False,
            "timeout": 5
        }
    )
else:
    # PostgreSQL optimizations for production
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=5,               # Reduced pool size
        max_overflow=10,           # Reduced overflow
        pool_pre_ping=True,
        pool_recycle=1800,         # 30 minutes
        echo=False,
        connect_args={
            "connect_timeout": 3,   # Reduced timeout
            "options": "-c statement_timeout=5000"  # 5 second query timeout
        }
    )

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=False  # Prevent lazy loading issues
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
