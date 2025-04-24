from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend2.db import TasksSessionLocal
# from backend2.models import User, Task
from backend2.controller import get_task  # Assuming you have a function to get tasks

app = FastAPI()

# Dependency for user DB
# def get_user_db():
#     db = UserSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Dependency for tasks DB
def get_tasks_db():
    db = TasksSessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/task_excel")
async def get_tasks(db: Session = Depends(get_tasks_db)):
    return get_task(db)