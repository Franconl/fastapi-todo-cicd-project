from fastapi import FastAPI, HTTPException, status
from typing import List
from app.models import Task

app = FastAPI(title = "FastAPI TODO APP", version = "1.0.1", description = "Ahora con CI/CD")

#almacenamiento en memoria
task_db: List[Task] = []

@app.get("/")
async def read_root():
    return {"message": "Welcome to TODO APP"}

@app.get("/tasks", response_model=List[Task], summary= "obtener todas las tareas")
async def get_task():
    return task_db

@app.post("/tasks", response_model= Task, status_code= status.HTTP_201_CREATED, summary="Crear una nueva tarea")
async def create_task(task: Task):
    if task.id is None:
        task.id = str(uuid.uuid4())
    task_db.append(task)
    return task

@app.get("/task/{task_id}", response_model=Task, summary="obtener tarea por id")
async def get_task(task_id: str):
    for task in task_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    

@app.put("/task/{task_id}", response_model=Task, summary="Actualizar una tarea existente")
async def update_task(task_id: str, updated_task: Task):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="eliminar tarea")
async def delete_task(task_id: str):
    global task_db
    initial_len= len(task_db)
    task_db= [task for task in task_db if task.id != task_id]
    if len(tasks_db) == initial_len:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return

