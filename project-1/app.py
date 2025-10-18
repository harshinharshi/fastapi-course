"""
Book Management API - FastAPI Application
==========================================
A RESTful API for managing a collection of books with CRUD operations.

This is a beginner-friendly FastAPI project that demonstrates:
- GET requests (retrieve data)
- POST requests (create data)
- PUT requests (update data)
- DELETE requests (remove data)
- Path parameters and query parameters
- Pydantic models for data validation

Author: Harshin
Date: 2025
Version: 1.0
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List

# Initialize FastAPI application
app = FastAPI(
    title="Book Management API",
    description="A simple API to manage a collection of books",
    version="1.0.0"
)

# In-memory database - list of books stored as dictionaries
# In a production app, this would be replaced with a real database
BOOKS: List[dict] = [
    {"id": 1, "title": "1984", "author": "George Orwell", "category": "Fiction"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Fiction"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Fiction"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "category": "Romance"},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Fiction"},
]


# Pydantic Models for Request/Response Validation
# ===============================================

class BookCreate(BaseModel):
    """
    Model for creating a new book.
    
    Attributes:
        id: Optional book identifier (auto-generated if not provided)
        title: The title of the book (required)
        author: The author's name (required)
        category: The book's category/genre (required)
    """
    id: Optional[int] = Field(None, description="Book ID (auto-generated if not provided)")
    title: str = Field(..., min_length=1, max_length=200, description="Book title")
    author: str = Field(..., min_length=1, max_length=100, description="Author name")
    category: str = Field(..., min_length=1, max_length=50, description="Book category")

    class Config:
        # Example shown in API documentation
        json_schema_extra = {
            "example": {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "category": "Fantasy"
            }
        }


class BookUpdate(BaseModel):
    """
    Model for updating an existing book.
    
    All fields are optional - only provided fields will be updated.
    
    Attributes:
        title: The new title (optional)
        author: The new author name (optional)
        category: The new category (optional)
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Updated book title")
    author: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated author name")
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="Updated book category")

    class Config:
        # Example shown in API documentation
        json_schema_extra = {
            "example": {
                "title": "1984 (Updated Edition)",
                "category": "Dystopian Fiction"
            }
        }


# API Endpoints
# =============

@app.get("/", tags=["Root"])
async def root() -> dict:
    """
    Root endpoint - Welcome message and API information.
    
    Returns:
        dict: Welcome message with API documentation link
    """
    return {
        "message": "Welcome to the Book Management API",
        "documentation": "/docs",
        "version": "1.0.0"
    }


@app.get("/books/", tags=["Books"], response_model=List[dict])
async def get_all_books() -> List[dict]:
    """
    Retrieve all books in the collection.
    
    Returns:
        List[dict]: A list of all books with their details
    
    Example Response:
        [
            {"id": 1, "title": "1984", "author": "George Orwell", "category": "Fiction"},
            ...
        ]
    """
    return BOOKS


@app.get("/books/{book_id}", tags=["Books"])
async def get_book_by_id(book_id: int) -> dict:
    """
    Retrieve a specific book by its ID.
    
    Args:
        book_id (int): The unique identifier of the book (path parameter)
    
    Returns:
        dict: The book details if found
    
    Raises:
        HTTPException: 404 error if book is not found
    
    Example:
        GET /books/1
        Returns: {"id": 1, "title": "1984", "author": "George Orwell", "category": "Fiction"}
    """
    # Search through all books for matching ID
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    
    # If no book found, raise 404 error
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"
    )


@app.get("/books/category/{category}", tags=["Books"])
async def get_books_by_category(category: str) -> List[dict]:
    """
    Retrieve all books in a specific category.
    
    Args:
        category (str): The category to filter by (path parameter, case-insensitive)
    
    Returns:
        List[dict]: A list of books in the specified category
    
    Example:
        GET /books/category/Fiction
        Returns all books with category "Fiction"
    """
    # Filter books by category (case-insensitive comparison)
    filtered_books = [
        book for book in BOOKS 
        if book["category"].lower() == category.lower()
    ]
    
    # Return empty list if no books found in this category
    return filtered_books


@app.get("/books/author/{author_name}", tags=["Books"])
async def search_books_by_author(author_name: str) -> List[dict]:
    """
    Search for books by author name (partial match supported).
    
    Args:
        author_name (str): The author name or partial name to search for (case-insensitive)
    
    Returns:
        List[dict]: A list of books by authors matching the search term
    
    Example:
        GET /books/author/orwell
        Returns: [{"id": 1, "title": "1984", "author": "George Orwell", "category": "Fiction"}]
    """
    # Search for books where author name contains the search term
    matching_books = [
        book for book in BOOKS 
        if author_name.lower() in book["author"].lower()
    ]
    
    return matching_books


@app.post("/books/", tags=["Books"], status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookCreate) -> dict:
    """
    Create a new book and add it to the collection.
    
    Args:
        new_book (BookCreate): The book data to create (from request body)
    
    Returns:
        dict: The newly created book with all its details
    
    Notes:
        - If no ID is provided or ID is 0, a new ID will be auto-generated
        - The new ID will be one more than the current maximum ID
    
    Example Request Body:
        {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "category": "Fantasy"
        }
    """
    # Auto-generate ID if not provided or if it's 0
    if new_book.id is None or new_book.id == 0:
        # Find the maximum ID currently in use and add 1
        max_id = max([book["id"] for book in BOOKS], default=0)
        new_book.id = max_id + 1
    
    # Convert Pydantic model to dictionary and add to books list
    book_dict = new_book.model_dump()
    BOOKS.append(book_dict)
    
    return book_dict


@app.put("/books/{book_id}", tags=["Books"])
async def update_book(book_id: int, updated_book: BookUpdate) -> dict:
    """
    Update an existing book's information.
    
    Args:
        book_id (int): The ID of the book to update (path parameter)
        updated_book (BookUpdate): The fields to update (from request body)
    
    Returns:
        dict: The updated book with all its details
    
    Raises:
        HTTPException: 404 error if book is not found
    
    Notes:
        - Only fields provided in the request will be updated
        - Empty or null fields will be ignored
        - The book ID cannot be changed
    
    Example Request Body:
        {
            "title": "1984 (Updated Edition)",
            "category": "Dystopian Fiction"
        }
    """
    # Search for the book to update
    for book in BOOKS:
        if book["id"] == book_id:
            # Update only the fields that were provided (not None)
            if updated_book.title is not None:
                book["title"] = updated_book.title
            
            if updated_book.author is not None:
                book["author"] = updated_book.author
            
            if updated_book.category is not None:
                book["category"] = updated_book.category
            
            return book
    
    # If book not found, raise 404 error
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"
    )


@app.delete("/books/{book_id}", tags=["Books"])
async def delete_book(book_id: int) -> dict:
    """
    Delete a book from the collection.
    
    Args:
        book_id (int): The ID of the book to delete (path parameter)
    
    Returns:
        dict: Success message with deleted book details
    
    Raises:
        HTTPException: 404 error if book is not found
    
    Example:
        DELETE /books/1
        Returns: {"message": "Book deleted successfully", "deleted_book": {...}}
    """
    # Search for the book to delete
    for book in BOOKS:
        if book["id"] == book_id:
            # Store book details before removing
            deleted_book = book.copy()
            BOOKS.remove(book)
            
            return {
                "message": "Book deleted successfully",
                "deleted_book": deleted_book
            }
    
    # If book not found, raise 404 error
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"
    )


# Application Entry Point
# ========================

if __name__ == "__main__":
    """
    Run the FastAPI application using Uvicorn server.
    
    The server will start at: http://127.0.0.1:8000
    Interactive API documentation available at: http://127.0.0.1:8000/docs
    Alternative documentation at: http://127.0.0.1:8000/redoc
    """
    import uvicorn
    
    # Start the server
    uvicorn.run(
        app,
        host="127.0.0.1",  # localhost - only accessible from this computer
        port=8000,          # Port number
        reload=True         # Auto-reload on code changes (for development only)
    )