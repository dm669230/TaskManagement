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
    task = Column(String)
    description = Column(String)
    effort_to_complete = Column(Integer) # in days
    due_date = Column(String)

{
    "title":"debug",
    "status": 'complete',
    "description": "Router path for /task_add bug fixed in backend2",
    "etc": 2,
    "due_date":"01-04-2025"
 }
