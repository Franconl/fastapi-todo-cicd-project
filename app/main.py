import uuid
from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
from app.models import Task 

app = FastAPI(title="FastAPI TODO APP", version="1.0.1", description="Ahora con CI/CD")

# Almacenamiento en memoria, usando app.task_db (singular)
app.task_db: List[Task] = []

@app.get("/")
async def read_root():
    return {"message": "Welcome to TODO APP"}

@app.get("/tasks", response_model=List[Task], summary="obtener todas las tareas")
async def get_tasks(): 
    return app.task_db

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, summary="Crear una nueva tarea")
async def create_task(task: Task):
    if task.id is None:
        task.id = str(uuid.uuid4())
    app.task_db.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task, summary="obtener tarea por id")
async def get_task(task_id: str):
    for task in app.task_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    

@app.put("/tasks/{task_id}", response_model=Task, summary="Actualizar una tarea existente") 
async def update_task(task_id: str, updated_task: Task):
    for index, task in enumerate(app.task_db): 
        if task.id == task_id:
            app.task_db[index] = updated_task 
            return updated_task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="eliminar tarea") 
async def delete_task(task_id: str):
    initial_len= len(app.task_db)
    app.task_db = [task for task in app.task_db if task.id != task_id]
    if len(app.task_db) == initial_len:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return
