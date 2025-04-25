from pydantic import BaseModel
from typing import Optional, List, Dict, Union

class TaskCreate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    status : Optional[str] = "In Progress"
    etc : Optional[str] = None
    due_date : Optional[str] = None

class TaskUpdate(BaseModel):
    title : Optional[str] = None
    status: Optional[str] = "Completed" 

class TaskDelete(BaseModel):
    title : Optional[str] = None
