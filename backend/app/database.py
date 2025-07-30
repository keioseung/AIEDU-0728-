from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Docker Compose 환경에서의 기본값
    DATABASE_URL = "postgresql://postgres:password@postgres:5432/ai_mastery_hub"
    print(f"⚠️ DATABASE_URL 환경변수가 설정되지 않아 기본값을 사용합니다: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
