
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = settings.database_uri

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    print(SQLALCHEMY_DATABASE_URL)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Iam dependable and I love helping (team) develop ideas and implement code on various products while gaining valuable experience with latest technologies and tools. I also would like to apply knowledge and skills acquired to work on software user interfaces. This will help me hone my problem-solving skills to keep projects moving forward.I am dedicated to giving customers the best possible software with high-quality programming and debugging of software systems.
