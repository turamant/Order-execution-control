from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from models import Task, Responsible, Status, Comment

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# Маршруты для Task
@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    # Логика создания задачи
    return task

@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    # Логика получения списка задач
    return [Task(id=1, title="Task 1", description="Description 1", assigned_to="User 1", due_date=datetime(2024, 8, 1), status="Open")]

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    # Логика получения задачи по ID
    if task_id == 1:
        return Task(id=1, title="Task 1", description="Description 1", assigned_to="User 1", due_date=datetime(2024, 8, 1), status="Open")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    # Логика обновления задачи
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    # Логика удаления задачи
    return

# Маршруты для Responsible
@app.post("/responsibles/", response_model=Responsible, status_code=status.HTTP_201_CREATED)
def create_responsible(responsible: Responsible):
    # Логика создания ответственного
    return responsible

@app.get("/responsibles/", response_model=List[Responsible])
def read_responsibles():
    # Логика получения списка ответственных
    return [Responsible(id=1, name="User 1", email="user1@example.com", phone="123456789")]

# Маршруты для Status
@app.post("/statuses/", response_model=Status, status_code=status.HTTP_201_CREATED)
def create_status(status: Status):
    # Логика создания статуса
    return status

@app.get("/statuses/", response_model=List[Status])
def read_statuses():
    # Логика получения списка статусов
    return [Status(id=1, name="Open", description="Task is open")]

# Маршруты для Comment
@app.post("/comments/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(comment: Comment):
    # Логика создания комментария
    return comment

@app.get("/comments/", response_model=List[Comment])
def read_comments():
    # Логика получения списка комментариев
    return [Comment(id=1, task_id=1, author="User 1", text="This is a comment")]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
