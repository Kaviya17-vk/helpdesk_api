from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite local database connection URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./helpdesk.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency loop to yield database sessions per request securely
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
