from fastapi import FastAPI, Depends, HTTPException
from models import Tasks
from schema import TaskCreate,TaskDelete, TaskUpdate
import pandas as pd
from io import BytesIO
from starlette.responses import StreamingResponse
import traceback


def get_excel_report(db):
    try:
        tasks = db.query(Tasks).all()
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found.")

        df = pd.DataFrame([task.__dict__ for task in tasks])
        df.drop(columns=["_sa_instance_state"], errors="ignore", inplace=True)

        output = BytesIO()
        df.to_excel(output, index=False, sheet_name="Tasks")
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=tasks.xlsx"}
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))




def add_task(req,task, db):
    title = task.title
    description = task.description
    status = task.status
    etc = task.etc
    due_date = task.due_date
    print("req.state", req.state)
    # decoded = jwt.decode(token=token, key=SECRET_KEY, algorithms=["HS256"])
    user_id = req.state.user.id
    print("req.state", user_id)
    print("title, description, task_name, etc, due_date, user_id",title, description, status, etc, due_date, user_id )
    # Check if the task already exists
    db_task = db.query(Tasks).filter(Tasks.user_id == user_id, Tasks.title == title).first()
    
    if db_task:
        raise HTTPException(status_code=200, detail="Task already exists")
    
    # Insert new task into database
    db_task = Tasks(user_id=user_id, title=title, status=status, description=description, 
                   etc=etc, due_date=due_date)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return {"message": "Task added successfully"}

def update_task(req, update_body ,db):
    title = update_body.title
    status = update_body.status
    user_id = req.state.user.id
    print("title, user_id update_task", title, user_id)
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    # Check if task exists for the user
    db_task = db.query(Tasks).filter(Tasks.user_id == user_id, Tasks.title == title).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found for this user")
    
    # Toggle status from 'complete' to 'incomplete' or vice versa    
    # Update the task's status
    db_task.status = status
    db.commit()
    db.refresh(db_task)

    return {"message": f"Task status updated to {status}", "updated_status": status}

def get_task(req, db):
    user_id = req.state.user.id
    
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required as query parameter")
    
    # Fetch the task based on user_id and title
    db_task = db.query(Tasks).filter(Tasks.user_id == user_id).all()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task fetched successfully", "task": db_task}

def delete_task(req, db, id):
    user_id = req.state.user.id
    
    # Check if the task exists
    db_task = db.query(Tasks).filter(Tasks.user_id == user_id, Tasks.id == id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Delete the task
    db.delete(db_task)
    db.commit()
    
    return {"message": "Task deleted successfully"}
