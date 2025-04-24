from pydantic import BaseModel
from typing import Optional, List, Dict, Union

class TaskCreate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    task : Optional[str] = None
    etc : Optional[int] = 1
    due_date : Optional[str] = "yyyy-mm-dd"

class TaskUpdate(BaseModel):
    title : Optional[str] = None
    task: Optional[str] = "Select one among [Pending, Complete, Incomplete]" 

class TaskDelete(BaseModel):
    title : Optional[str] = None