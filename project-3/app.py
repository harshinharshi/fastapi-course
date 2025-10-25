from fastapi import FastAPI, Depends, HTTPException, Path, status
from database import engine, SessionLocal
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequestModel(BaseModel):
    title: str = Field(min_length=3)
    description: str | None = Field(default=None, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False 

class TodoResponseModel(BaseModel):
    id: int
    title: str
    description: str | None = None
    priority: int = 1
    complete: bool = False

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(models.Todos).all()


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_element: models.Todos | None = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_element :
        return todo_element
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos/", status_code=status.HTTP_201_CREATED, response_model=TodoResponseModel)
async def create_todo(db: db_dependency, todo_request: TodoRequestModel):
    todo_element = models.Todos(**todo_request.model_dump())
    db.add(todo_element)
    db.commit()
    db.refresh(todo_element)
    return todo_element


@app.put("/todos/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponseModel)
async def update_todo(db: db_dependency, todo_request: TodoRequestModel, todo_id: int = Path(gt=0)):
    # Get todo by ID
    todo_element = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo_element:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update only non-null fields
    update_data = todo_request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo_element, key, value)

    db.commit()
    db.refresh(todo_element)
    return todo_element


@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_element = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo_element:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Store the data before deletion
    deleted_data = {
        "id": todo_element.id,
        "title": todo_element.title,
        "description": todo_element.description,
        "priority": todo_element.priority,
        "complete": todo_element.complete
    }

    db.delete(todo_element)
    db.commit()

    return {"message": "Todo deleted successfully", "deleted_value": deleted_data}
