from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

# Función para limpiar la "base de datos" en memoria antes de cada test
# Asegura que app.task_db sea el que se limpie
def setup_function():
    app.task_db.clear()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to TODO APP"} 

def test_create_task():
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "This is a test description"}
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == "Test Task"
    assert response.json()["completed"] is False
    # Verificar que se añadió a la "DB" en memoria, usando app.task_db
    assert len(app.task_db) == 1
    assert app.task_db[0].title == "Test Task"

def test_get_tasks():
    # Primero se crean algunas tareas
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Task 1"
    assert response.json()[1]["title"] == "Task 2"

def test_get_single_task():
    create_response = client.post("/tasks", json={"title": "Single Task"})
    task_id = create_response.json()["id"]
    response = client.get(f"/tasks/{task_id}") 
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Single Task"

def test_get_nonexistent_task():
    response = client.get("/tasks/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"} 

def test_update_task():
    create_response = client.post("/tasks", json={"title": "Task to Update"})
    task_id = create_response.json()["id"]
    update_data = {"id": task_id, "title": "Updated Task", "description": "New description", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["completed"] is True
    # Verificar que la tarea se actualizó en la "DB" en memoria, usando app.task_db
    assert app.task_db[0].title == "Updated Task"

def test_update_nonexistent_task():
    response = client.put("/tasks/nonexistent_id", json={"id": "nonexistent_id", "title": "Nope"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"} 

def test_delete_task():
    create_response = client.post("/tasks", json={"title": "Task to Delete"})
    task_id = create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204 # No Content
    assert len(app.task_db) == 0

def test_delete_nonexistent_task():
    response = client.delete("/tasks/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"} # La aplicación devuelve "Task not found"
