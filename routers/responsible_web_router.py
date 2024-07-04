from fastapi import (APIRouter, Depends,
                     HTTPException, Request)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from models.responsible import Responsible
from models.status import Status
from schemas.responsible import ResponsibleDB
from schemas.status import StatusDB
from database import SessionLocal
from models.task import Task
from typing import Annotated, List




responsible_web_router = APIRouter(
    prefix="/responsibles",
    tags=["responsibles"],
)

templates = Jinja2Templates(directory="templates")


# Зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@responsible_web_router.get("/", response_class=HTMLResponse)
async def responsibles(request: Request, db: Session = Depends(get_db)):
    responsibles = db.query(ResponsibleDB).all()
    return templates.TemplateResponse("responsible_list.html", {"request": request, "responsibles": responsibles})
