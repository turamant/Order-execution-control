from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Base, engine
from routers.task_web_router import task_web_router
from routers.task_api_router import task_api_router
from routers.status_web_router import status_web_router
from routers.responsible_web_router import responsible_web_router
# Создаем все таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Регистрируем роутер для задач
app.include_router(task_api_router)
app.include_router(task_web_router)
app.include_router(status_web_router)
app.include_router(responsible_web_router)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
