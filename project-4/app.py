"""
FastAPI Todo Application

A RESTful API for managing todo items with full CRUD operations.
This application uses SQLAlchemy for database operations and Pydantic for data validation.

Author: Your Name
Version: 1.0.0
"""

from fastapi import FastAPI, Depends, HTTPException, Path, status
from database import engine, SessionLocal
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

import models

# Initialize FastAPI application
app = FastAPI(
    title="Todo API",
    description="A professional API for managing todo items",
    version="1.0.0"
)

# Create all database tables if they don't exist
# This runs when the application starts
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Database dependency for FastAPI endpoints.
    
    Creates a new SQLAlchemy session for each request and ensures
    it's properly closed after the request is complete.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Model).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Type alias for database dependency injection
# This makes the type annotation cleaner and more reusable
db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequestModel(BaseModel):
    """
    Pydantic model for todo item requests (POST/PUT operations).
    
    This model defines the structure and validation rules for incoming
    todo data. All fields are validated automatically by FastAPI.
    
    Attributes:
        title (str): Todo title, must be at least 3 characters
        description (str | None): Optional description, max 100 characters
        priority (int): Priority level between 1 and 5
        complete (bool): Completion status, defaults to False
        
    Example:
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "priority": 3,
            "complete": false
        }
    """
    title: str = Field(min_length=3, description="Todo title (minimum 3 characters)")
    description: str | None = Field(
        default=None, 
        max_length=100,
        description="Optional todo description (maximum 100 characters)"
    )
    priority: int = Field(
        gt=0, 
        lt=6,
        description="Priority level (1=lowest, 5=highest)"
    )
    complete: bool = Field(default=False, description="Completion status")


class TodoResponseModel(BaseModel):
    """
    Pydantic model for todo item responses (GET operations).
    
    This model defines the structure of data returned by the API.
    It includes all fields from the database model.
    
    Attributes:
        id (int): Unique identifier for the todo
        title (str): Todo title
        description (str | None): Optional description
        priority (int): Priority level (1-5)
        complete (bool): Completion status
        
    Example:
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "priority": 3,
            "complete": false
        }
    """
    id: int = Field(description="Unique identifier")
    title: str = Field(description="Todo title")
    description: str | None = Field(default=None, description="Todo description")
    priority: int = Field(default=1, description="Priority level (1-5)")
    complete: bool = Field(default=False, description="Completion status")


@app.get(
    "/", 
    status_code=status.HTTP_200_OK,
    response_model=List[TodoResponseModel],
    summary="Get all todos",
    description="Retrieve a list of all todo items from the database"
)
async def read_all(db: db_dependency):
    """
    Retrieve all todo items.
    
    This endpoint returns all todos in the database without any filtering
    or pagination. For production use, consider adding pagination.
    
    Args:
        db: Database session (injected automatically)
        
    Returns:
        List[TodoResponseModel]: List of all todo items
        
    Example Response:
        [
            {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": 3,
                "complete": false
            },
            {
                "id": 2,
                "title": "Call dentist",
                "description": null,
                "priority": 5,
                "complete": true
            }
        ]
    """
    return db.query(models.Todos).all()


@app.get(
    "/todos/{todo_id}", 
    status_code=status.HTTP_200_OK,
    response_model=TodoResponseModel,
    summary="Get a specific todo",
    description="Retrieve a single todo item by its ID"
)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0, description="The ID of the todo to retrieve")):
    """
    Retrieve a single todo by ID.
    
    Args:
        db: Database session (injected automatically)
        todo_id: ID of the todo to retrieve (must be greater than 0)
        
    Returns:
        TodoResponseModel: The requested todo item
        
    Raises:
        HTTPException: 404 error if todo is not found
        
    Example Response:
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "priority": 3,
            "complete": false
        }
    """
    # Query the database for the todo with the specified ID
    todo_element: models.Todos | None = db.query(models.Todos).filter(
        models.Todos.id == todo_id
    ).first()
    
    # If found, return it; otherwise, raise 404 error
    if todo_element:
        return todo_element
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Todo with id {todo_id} not found"
    )


@app.post(
    "/todos/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=TodoResponseModel,
    summary="Create a new todo",
    description="Create a new todo item with the provided data"
)
async def create_todo(db: db_dependency, todo_request: TodoRequestModel):
    """
    Create a new todo item.
    
    This endpoint validates the incoming data and creates a new todo
    in the database. The ID is automatically generated.
    
    Args:
        db: Database session (injected automatically)
        todo_request: Todo data from request body (validated automatically)
        
    Returns:
        TodoResponseModel: The newly created todo with its generated ID
        
    Example Request:
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "priority": 3,
            "complete": false
        }
        
    Example Response:
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "priority": 3,
            "complete": false
        }
    """
    # Convert Pydantic model to dictionary and create SQLAlchemy model
    todo_element = models.Todos(**todo_request.model_dump())
    
    # Add to database session and commit the transaction
    db.add(todo_element)
    db.commit()
    
    # Refresh to get the generated ID and any default values
    db.refresh(todo_element)
    
    return todo_element


@app.put(
    "/todos/{todo_id}", 
    status_code=status.HTTP_200_OK, 
    response_model=TodoResponseModel,
    summary="Update a todo",
    description="Update an existing todo item with new data"
)
async def update_todo(
    db: db_dependency, 
    todo_request: TodoRequestModel, 
    todo_id: int = Path(gt=0, description="The ID of the todo to update")
):
    """
    Update an existing todo item.
    
    This endpoint updates only the fields provided in the request body.
    If a field is not provided, it retains its current value.
    
    Args:
        db: Database session (injected automatically)
        todo_request: Updated todo data from request body
        todo_id: ID of the todo to update (must be greater than 0)
        
    Returns:
        TodoResponseModel: The updated todo item
        
    Raises:
        HTTPException: 404 error if todo is not found
        
    Example Request:
        {
            "title": "Buy groceries and cook dinner",
            "priority": 4,
            "complete": true
        }
        
    Example Response:
        {
            "id": 1,
            "title": "Buy groceries and cook dinner",
            "description": "Milk, eggs, bread",  # Unchanged
            "priority": 4,
            "complete": true
        }
    """
    # Find the todo by ID
    todo_element = db.query(models.Todos).filter(
        models.Todos.id == todo_id
    ).first()
    
    # Raise 404 if not found
    if not todo_element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with id {todo_id} not found"
        )

    # Update only the fields that were provided in the request
    # exclude_unset=True means only set fields are included
    update_data = todo_request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo_element, key, value)

    # Commit changes and refresh the object
    db.commit()
    db.refresh(todo_element)
    
    return todo_element


@app.delete(
    "/todos/{todo_id}", 
    status_code=status.HTTP_200_OK,
    summary="Delete a todo",
    description="Delete a todo item by its ID"
)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0, description="The ID of the todo to delete")):
    """
    Delete a todo item.
    
    This endpoint permanently removes a todo from the database.
    It returns the deleted item's data for confirmation.
    
    Args:
        db: Database session (injected automatically)
        todo_id: ID of the todo to delete (must be greater than 0)
        
    Returns:
        dict: Confirmation message and deleted todo data
        
    Raises:
        HTTPException: 404 error if todo is not found
        
    Example Response:
        {
            "message": "Todo deleted successfully",
            "deleted_value": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": 3,
                "complete": false
            }
        }
    """
    # Find the todo by ID
    todo_element = db.query(models.Todos).filter(
        models.Todos.id == todo_id
    ).first()
    
    # Raise 404 if not found
    if not todo_element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with id {todo_id} not found"
        )

    # Store the data before deletion for the response
    deleted_data = {
        "id": todo_element.id,
        "title": todo_element.title,
        "description": todo_element.description,
        "priority": todo_element.priority,
        "complete": todo_element.complete
    }

    # Delete from database and commit
    db.delete(todo_element)
    db.commit()

    # Return confirmation with deleted data
    return {
        "message": "Todo deleted successfully", 
        "deleted_value": deleted_data
    }