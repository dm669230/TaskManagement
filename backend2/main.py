import time
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from db import SessionLocal
from functools import wraps
from models import User, Tasks
import jwt
from jwt import PyJWTError
from fastapi.security import OAuth2PasswordBearer
from schema import TaskUpdate, TaskCreate, TaskDelete
from fastapi.middleware.cors import CORSMiddleware
import os
# from backend2.models import User, Task
from controller import get_task, update_task, delete_task, add_task, get_excel_report  # Assuming you have a function to get tasks
SECRET_KEY = "v8Q!z&7P@kR#2sM$gT*F9nL0bX!uCwYd"
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] if you want to be specific
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Dependency for user DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for tasks DB
# def get_tasks_db():
#     db = TasksSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Dependency to simulate user extraction from JWT token
def get_current_user():
    # Assuming JWT token is decoded here, returning dummy user data
    return {"id": 1, "username": "example_user"}

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        req = kwargs.get("req")
        db = kwargs.get("db")
        headers =  req.headers
        print("headers999", req.headers)
        print("in the wrapper")
        if not headers or not headers.get("Authorization"):
            return JSONResponse({"message":"Authentication Credentials were Not Provided"})
        token = headers.get('Authorization').split(' ')[1]
        
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            
            print("decoded username id", decoded)
        except PyJWTError:
            return JSONResponse({"message": "Invalid token"}, status_code=401)
        exp = decoded.get("exp")
        if exp < int(time.time()):
            return JSONResponse({"message": "Token Expired"}, status_code=401)
        username = decoded.get("username")

        user_id = decoded.get("id")
        exist_user = db.query(User).filter(User.id == user_id).first()
        if exist_user and exist_user.username == username:
            # req.user = exist_user
            req.state.user = exist_user  # ✅ Set user in req.stateassign req.user
            return func(*args, **kwargs)
        return JSONResponse({"message": "user does not exist"})
    return wrapper


@app.get("/task_excel")
@login_required
def get_excel(req : Request,db: Session = Depends(get_db)):
    return get_excel_report(db)

@app.post('/task_add')
@login_required
def add_tasks(req : Request, task: TaskCreate, db: Session = Depends(get_db)):
    print(task)
    return add_task(req, task, db)

@app.patch('/task_update')
@login_required
def update_tasks(req : Request, update_body : TaskUpdate,db: Session = Depends(get_db)):
    return update_task(req, update_body, db)

@app.get('/task_get')
@login_required
def get_tasks(req : Request, db: Session = Depends(get_db)):
    return get_task(req, db)

@app.delete('/task_delete/{id}')
@login_required
def delete_tasks(req : Request, id: int, db: Session = Depends(get_db)):
    return delete_task(req, db, id)
