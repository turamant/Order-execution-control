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
