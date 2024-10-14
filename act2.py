from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

class Task(BaseModel):
    task_id: Optional[int] = None
    task_title: str
    task_desc: str
    is_finished: bool = False

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    return {"status": "ok", "task": task}

@app.post("/tasks")
def create_task(task: Task):
    if not task.task_title or not task.task_desc:
        raise HTTPException(status_code=400, detail={"error": "Invalid input: Title and Description are required"})
    
    task_id = max(task["task_id"] for task in task_db) + 1 if task_db else 1
    new_task = task.dict()
    new_task["task_id"] = task_id
    task_db.append(new_task)
    return {"status": "ok", "task": new_task}

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    task_to_update = next((task for task in task_db if task["task_id"] == task_id), None)
    
    if task_to_update is None:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    
    if task.task_title:
        task_to_update["task_title"] = task.task_title
    if task.task_desc:
        task_to_update["task_desc"] = task.task_desc
    task_to_update["is_finished"] = task.is_finished
    
    return {"status": "ok", "task": task_to_update}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task_to_delete = next((task for task in task_db if task["task_id"] == task_id), None)
    
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    
    task_db.remove(task_to_delete)
    return {"status": "ok"}
