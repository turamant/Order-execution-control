from fastapi import FastAPI
from database import Base, engine
from routers.task_router import task_router


# Создаем все таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Регистрируем роутер для задач
app.include_router(task_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
