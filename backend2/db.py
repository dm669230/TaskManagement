from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL for SQLite (you can replace this with any other DB)
DATABASE_URL = "sqlite:///../database/main.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models (tables)
Base = declarative_base()

# To create all tables based on the Base class
Base.metadata.create_all(bind=engine)
