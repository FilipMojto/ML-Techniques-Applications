# database.py
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_PATH = "./data/example.db"
DATABASE_URL = "sqlite:///" + DATABASE_PATH

db_path = Path(DATABASE_PATH)
was_just_created = not db_path.exists()


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

