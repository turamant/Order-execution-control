from fastapi import (APIRouter, Depends,
                     HTTPException, Request)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from schemas.responsible import ResponsibleDB
from schemas.status import StatusDB
from schemas.task import TaskDB
from database import SessionLocal



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
    db_tasks = db.query(TaskDB).all()
    return templates.TemplateResponse("task_list.html",
                                      {"request": request,
                                       "tasks": db_tasks
                                       })


@task_web_router.get("/create", response_class=HTMLResponse)
async def create_task(request: Request, db: Session = Depends(get_db)):
    responsibles = db.query(ResponsibleDB).all()
    statuses = db.query(StatusDB).all()
    return templates.TemplateResponse("task_create.html",
                                       {"request": request,
                                        "responsibles": responsibles,
                                        "statuses": statuses})

@task_web_router.post("/create", response_class=HTMLResponse)
async def store_task(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    title = form.get("title")
    description = form.get("description")
    responsible_id = int(form.get("responsible_id"))
    status_id = int(form.get("status_id"))
    due_date_str = form.get("due_date")
    due_date = datetime.fromisoformat(due_date_str)

    new_task = TaskDB(
        title=title,
        description=description,
        responsible_id=responsible_id,
        status_id=status_id,
        due_date=due_date
    )
    db.add(new_task)
    db.commit()

    return templates.TemplateResponse("task_detail.html",
                                      {"request": request,
                                       "task": new_task})

@task_web_router.get("/{task_id}", response_class=HTMLResponse)
async def read_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("task_detail.html",
                                      {"request": request,
                                       "task": db_task})



@task_web_router.get("/{task_id}/edit", response_class=HTMLResponse)
async def edit_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    responsibles = db.query(ResponsibleDB).all()
    statuses = db.query(StatusDB).all()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("task_edit.html", {"request": request,
                                                         "task": db_task,
                                                         "responsibles": responsibles,
                                                         "statuses": statuses})

@task_web_router.post("/{task_id}/edit", response_class=HTMLResponse)
async def update_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    form = await request.form()
    db_task.title = form.get("title")
    db_task.description = form.get("description")
    db_task.responsible_id = form.get("responsible_id")
    db_task.status_id = form.get("status_id")
    due_date_str = form.get("due_date")
    db_task.due_date = datetime.fromisoformat(due_date_str)
    
    db_task.updated_at = datetime.now()

    db.commit()
    return templates.TemplateResponse("task_detail.html",
                                      {"request": request,
                                       "task": db_task,
                                       })


@task_web_router.get("/{task_id}/delete", response_class=HTMLResponse)
async def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # Удалите задачу
    db.delete(db_task)
    db.commit()
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": db.query(TaskDB).all()})


@task_web_router.get("/statuses/create", response_class=HTMLResponse)
async def create_status_get(request: Request):
    return templates.TemplateResponse("status_create.html", {"request": request})

@task_web_router.post("/statuses/create", response_class=HTMLResponse)
async def create_status_post(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    new_status = StatusDB(name=name)
    db.add(new_status)
    db.commit()
    return RedirectResponse(url="/tasks", status_code=302)

@task_web_router.get("/responsibles/create", response_class=HTMLResponse)
async def create_responsible_get(request: Request):
    return templates.TemplateResponse("responsible_create.html", {"request": request})

@task_web_router.post("/responsibles/create", response_class=HTMLResponse)
async def create_responsible_post(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    new_responsible = ResponsibleDB(name=name)
    db.add(new_responsible)
    db.commit()
    return RedirectResponse(url="/tasks", status_code=302)





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
