from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from database import Base, engine
# from routers.task_web_router import task_web_router

from routers.task_api_router import task_api_router
from routers.status_web_router import status_web_router
from routers.responsible_web_router import responsible_web_router

import schemas
from schemas.comment import CommentDB
from schemas.responsible import ResponsibleDB
from schemas.status import StatusDB
from schemas.task import TaskDB
from utils import get_router

# Создание роутеров для каждой модели
task_router = get_router(TaskDB, "task", "task")
status_router = get_router(StatusDB, "status", "status")
responsible_router = get_router(ResponsibleDB, "responsible", "responsible")
comment_router = get_router(CommentDB, "comment", "comment")

# Создаем все таблицы
Base.metadata.create_all(bind=engine)



app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("404.html",
                                      {"request": request},
                                       status_code=404)



# Регистрируем роутер для задач
# app.include_router(task_api_router)
# app.include_router(task_web_router)
# app.include_router(status_web_router)
# app.include_router(responsible_web_router)

app.include_router(task_router)
app.include_router(status_router)
app.include_router(responsible_router)
app.include_router(comment_router)



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
