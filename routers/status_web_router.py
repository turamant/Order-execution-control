from fastapi import (APIRouter, Depends,
                     HTTPException, Request)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from models.responsible import Responsible
from models.status import Status
from schemas.status import StatusDB
from database import SessionLocal
from models.task import Task
from typing import Annotated, List




status_web_router = APIRouter(
    prefix="/statuses",
    tags=["statuses"],
)

templates = Jinja2Templates(directory="templates")


# Зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@status_web_router.get("/", response_class=HTMLResponse)
async def statuses(request: Request, db: Session = Depends(get_db)):
    statuses = db.query(StatusDB).all()
    return templates.TemplateResponse("status_list.html", {"request": request, "statuses": statuses})



@status_web_router.get("/create", response_class=HTMLResponse)
async def create_status(request: Request, db: Session = Depends(get_db)):
    
    return templates.TemplateResponse("status_create.html",
                                       {"request": request
                                        })

@status_web_router.post("/create", response_class=HTMLResponse)
async def store_status(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    description = form.get("description")
    
    new_status = StatusDB(
        name=name,
        description=description,

    )
    db.add(new_status)
    db.commit()

    return templates.TemplateResponse("status_detail.html",
                                      {"request": request,
                                       "status": new_status
                                       })

@status_web_router.get("/{status_id}", response_class=HTMLResponse)
async def read_status(request: Request, status_id: int, db: Session = Depends(get_db)):
    db_status = db.query(StatusDB).filter(StatusDB.id == status_id).first()
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return templates.TemplateResponse("status_detail.html",
                                      {"request": request,
                                       "status": db_status})


@status_web_router.get("/{status_id}/edit", response_class=HTMLResponse)
async def edit_status(request: Request, status_id: int, db: Session = Depends(get_db)):
    db_status = db.query(StatusDB).filter(StatusDB.id == status_id).first()

    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return templates.TemplateResponse("status_edit.html", {"request": request,
                                                         "status": db_status,
                                                         })

@status_web_router.post("/{status_id}/edit", response_class=HTMLResponse)
async def update_status(request: Request, status_id: int, db: Session = Depends(get_db)):
    db_status = db.query(StatusDB).filter(StatusDB.id == status_id).first()
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    
    form = await request.form()
    db_status.name = form.get("name")
    db_status.description = form.get("description")
    db.commit()
    return templates.TemplateResponse("status_detail.html",
                                      {"request": request,
                                       "status": db_status,
                                       })



@status_web_router.get("/{status_id}/delete", response_class=HTMLResponse)
async def delete_task(request: Request, status_id: int, db: Session = Depends(get_db)):
    db_status = db.query(StatusDB).filter(StatusDB.id == status_id).first()
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    # Удалите задачу
    db.delete(db_status)
    db.commit()
    return templates.TemplateResponse("status_list.html",
                                      {"request": request,
                                       "statuses": db.query(StatusDB).all()})
