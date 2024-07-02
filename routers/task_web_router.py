from fastapi import (APIRouter, Depends,
                     HTTPException, Request)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from schemas.task import TaskDB
from database import SessionLocal
from models.task import Task
from typing import Annotated, List




task_web_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

templates = Jinja2Templates(directory="templates")


# Зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@task_web_router.get("/", response_class=HTMLResponse)
async def tasks(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": tasks})

@task_web_router.get("/create", response_class=HTMLResponse)
async def create_task(request: Request):
    return templates.TemplateResponse("task_create.html", {"request": request})

@task_web_router.post("/create", response_class=HTMLResponse)
async def store_task(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    title = form.get("title")
    description = form.get("description")
    assigned_to = form.get("assigned_to")
    due_date_str = form.get("due_date")
    due_date = datetime.fromisoformat(due_date_str)
    status = form.get("status")

    new_task = TaskDB(
        title=title,
        description=description,
        assigned_to=assigned_to,
        due_date=due_date,
        status=status
    )
    db.add(new_task)
    db.commit()

    return templates.TemplateResponse("task_detail.html", {"request": request, "task": new_task})
@task_web_router.get("/{task_id}", response_class=HTMLResponse)
async def read_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("task_detail.html", {"request": request, "task": db_task})



@task_web_router.get("/{task_id}/edit", response_class=HTMLResponse)
async def edit_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("task_edit.html", {"request": request, "task": db_task})

@task_web_router.post("/{task_id}/edit", response_class=HTMLResponse)
async def update_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    form = await request.form()
    db_task.title = form.get("title")
    db_task.description = form.get("description")
    db_task.assigned_to = form.get("assigned_to")
    due_date_str = form.get("due_date")
    db_task.due_date = datetime.fromisoformat(due_date_str)
    db_task.status = form.get("status")
    db_task.updated_at = datetime.now()

    db.commit()
    return templates.TemplateResponse("task_detail.html", {"request": request, "task": db_task})


@task_web_router.get("/{task_id}/delete", response_class=HTMLResponse)
async def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # Удалите задачу
    db.delete(db_task)
    db.commit()
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": db.query(TaskDB).all()})








# @task_router.post("/tasks/", response_model=Task)
# def create_task(task: Annotated[Task, Depends()], db: Session = Depends(get_db)):
#     db_task = TaskDB(**task.model_dump())
#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)
#     return db_task

# @task_router.get("/tasks/", response_model=Task)
# def read_tasks(db: Session = Depends(get_db)):
#     db_tasks = db.query(TaskDB).all()
#     return db_tasks

# @task_router.get("/{task_id}", response_model=Task)
# def read_task(task_id: int, db: Session = Depends(get_db)):
#     db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task

# @task_router.put("/{task_id}", response_model=Task)
# def update_task(task_id: int, task: Annotated[Task, Depends()], db: Session = Depends(get_db)):
#     db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     for key, value in task.model_dump().items():
#         setattr(db_task, key, value)
#     db_task.updated_at = datetime.now()
#     db.commit()
#     db.refresh(db_task)
#     return db_task

# @task_router.delete("/tasks/{task_id}")
# def delete_task(task_id: int, db: Session = Depends(get_db)):
#     db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     db.delete(db_task)
#     db.commit()
#     return {"ok": True}
