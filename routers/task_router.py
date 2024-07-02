from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from schemas.task import TaskDB
from database import SessionLocal
from models.task import Task
from typing import Annotated

task_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

# Зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@task_router.post("/", response_model=Task)
def create_task(task: Annotated[Task, Depends()], db: Session = Depends(get_db)):
    db_task = TaskDB(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@task_router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@task_router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task: Annotated[Task, Depends()], db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db_task.updated_at = datetime.now()
    db.commit()
    db.refresh(db_task)
    return db_task

@task_router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"ok": True}
