from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

API_KEY = "rayan"

class Todo(BaseModel):
    id: int
    task: str

class TodoCreate(BaseModel):
    task: str

todos: List[Todo] = [Todo(id=1, task="Do project"), Todo(id=2, task="Go to the gym")]

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

@app.post("/todos", response_model=Todo, status_code=201)
def add_todo(new_todo: TodoCreate):
    todo = Todo(id=len(todos) + 1, task=new_todo.task)
    todos.append(todo)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return
        
    raise HTTPException(status_code=404, detail="Todo not found")