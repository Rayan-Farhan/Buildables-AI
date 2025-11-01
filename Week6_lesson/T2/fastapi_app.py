from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Todo(BaseModel):
    id: int
    task: str

class TodoCreate(BaseModel):
    task: str

# storage
todos: List[Todo] = [Todo(id=1, task="Do project")]

# GET Endpoint - Return todos
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

# POST Endpoint - Add todo
@app.post("/todos", response_model=Todo, status_code=201)
def add_todo(new_todo: TodoCreate):
    todo = Todo(id=len(todos) + 1, task=new_todo.task)
    todos.append(todo)
    return todo