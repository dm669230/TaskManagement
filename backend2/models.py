from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from pydantic import EmailStr
from db import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key = True)
    username = Column(String)
    password = Column(String)

class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String)
    status = Column(String)
    description = Column(String)
    etc = Column(Integer)  #it stands for effort to complete
    due_date = Column(String)

