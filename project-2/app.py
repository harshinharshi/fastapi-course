"""
Books Management API - Project 2
=================================
A RESTful API for managing a book collection with full CRUD operations.

Author: [Your Name]
Date: October 2025
Version: 1.0.0

Features:
- List all books
- Add new books with validation
- Search books by title or rating
- Update book information (partial updates supported)
- Delete books by title and author

Tech Stack: FastAPI, Pydantic, Python 3.10+
"""

from fastapi import FastAPI, HTTPException, Body, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import uuid4
from starlette import status

# ============================================================================
# APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="Books Management API",
    description="A comprehensive API for managing book collections",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# ============================================================================

class Book(BaseModel):
    """
    Complete book model with all fields.
    
    Attributes:
        id: Unique identifier (UUID)
        title: Book title
        author: Book author
        description: Optional book description
        published_year: Year of publication
        rating: Book rating (0-5 scale)
    """
    id: str
    title: str
    author: str
    description: Optional[str] = None
    published_year: Optional[int] = None
    rating: Optional[float] = None


class BookCreate(BaseModel):
    """
    Model for creating a new book (excludes ID as it's auto-generated).
    
    Includes validation constraints:
    - Title and author must be at least 3 characters
    - Rating must be between 0 and 6
    """
    title: str = Field(
        min_length=3, 
        example="The Catcher in the Rye",
        description="Book title (minimum 3 characters)"
    )
    author: str = Field(
        min_length=3, 
        example="J.D. Salinger",
        description="Author name (minimum 3 characters)"
    )
    description: Optional[str] = Field(
        None, 
        example="A novel about teenage rebellion",
        description="Brief book description"
    )
    published_year: Optional[int] = Field(
        None, 
        example=1951,
        description="Year of publication"
    )
    rating: Optional[float] = Field(
        None, 
        gt=0, 
        lt=6, 
        example=4.5,
        description="Book rating (0-5 scale)"
    )


class BookUpdate(BaseModel):
    """
    Model for partial book updates.
    All fields are optional to support partial updates.
    """
    title: Optional[str] = Field(None, min_length=3)
    author: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = None
    published_year: Optional[int] = None
    rating: Optional[float] = Field(None, gt=0, lt=6)


# ============================================================================
# IN-MEMORY DATABASE
# ============================================================================

BOOKS: List[Book] = [
    Book(
        id=str(uuid4()), 
        title="1984", 
        author="George Orwell", 
        description="Dystopian novel about totalitarianism", 
        published_year=1949, 
        rating=4.8
    ),
    Book(
        id=str(uuid4()), 
        title="To Kill a Mockingbird", 
        author="Harper Lee", 
        description="Classic novel about racial injustice", 
        published_year=1960, 
        rating=4.9
    ),
    Book(
        id=str(uuid4()), 
        title="The Great Gatsby", 
        author="F. Scott Fitzgerald", 
        description="Novel set in the Jazz Age", 
        published_year=1925, 
        rating=4.7
    ),
    Book(
        id=str(uuid4()), 
        title="Pride and Prejudice", 
        author="Jane Austen", 
        description="Romantic novel about manners and marriage", 
        published_year=1813, 
        rating=4.8
    ),
]

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get(
    "/books", 
    response_model=List[Book], 
    status_code=status.HTTP_200_OK,
    summary="Get all books",
    description="Retrieve a list of all books in the collection"
)
async def get_books() -> List[Book]:
    """
    Retrieve all books from the collection.
    
    Returns:
        List[Book]: A list containing all books in the database
    """
    return BOOKS


@app.post(
    "/books", 
    response_model=Book, 
    status_code=status.HTTP_201_CREATED,
    summary="Add a new book",
    description="Create a new book entry with auto-generated ID"
)
async def add_book(book_request: BookCreate) -> Book:
    """
    Add a new book to the collection.
    
    Args:
        book_request: Book data (without ID)
    
    Returns:
        Book: The newly created book with generated ID
    
    Note:
        The ID is automatically generated using UUID4.
        Use .model_dump() instead of .dict() for Pydantic v2+
    """
    new_book = Book(
        id=str(uuid4()),
        **book_request.model_dump()  # Use model_dump() for Pydantic v2+
    )
    BOOKS.append(new_book)
    return new_book


@app.get(
    "/books/title/{book_title}", 
    response_model=Book, 
    status_code=status.HTTP_200_OK,
    summary="Get book by title",
    description="Retrieve a specific book by its exact title"
)
async def get_book_by_title(
    book_title: str = Path(
        min_length=3,
        description="Book title to search for (minimum 3 characters)"
    )
) -> Book:
    """
    Retrieve a book by its exact title.
    
    Args:
        book_title: The exact title of the book to find
    
    Returns:
        Book: The book matching the given title
    
    Raises:
        HTTPException: 404 if no book with the given title is found
    """
    book: Optional[Book] = next(
        (book for book in BOOKS if book.title == book_title), 
        None
    )
    
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with title '{book_title}' not found"
        )
    
    return book


@app.get(
    "/books/rating/{rating}", 
    response_model=List[Book],
    status_code=status.HTTP_200_OK,
    summary="Get books by rating",
    description="Retrieve all books with a specific rating"
)
async def get_books_by_rating(
    rating: float = Path(
        gt=0,
        lt=6,
        description="Rating to filter by (0-5 scale)"
    )
) -> List[Book]:
    """
    Retrieve all books with a specific rating.
    
    Args:
        rating: The exact rating to filter by
    
    Returns:
        List[Book]: All books with the specified rating
    
    Raises:
        HTTPException: 404 if no books with the given rating are found
    """
    books: List[Book] = [book for book in BOOKS if book.rating == rating]
    
    # Log the search for debugging purposes
    print(f'Books with rating {rating}: {len(books)} found')
    
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No books found with rating {rating}"
        )
    
    return books


@app.put(
    "/books/update", 
    response_model=Book, 
    status_code=status.HTTP_200_OK,
    summary="Update a book",
    description="Update book information by title and author (partial updates supported)"
)
async def update_book_by_title_author(
    title: str = Query(
        ..., 
        min_length=3,
        description="Book title to identify the book to update"
    ), 
    author: str = Query(
        ..., 
        min_length=3,
        description="Book author to identify the book to update"
    ), 
    update_data: BookUpdate = Body(
        ...,
        description="Fields to update (only provided fields will be updated)"
    )
) -> Book:
    """
    Update a book identified by title and author.
    
    This endpoint supports partial updates - only fields included in the
    request body will be updated. The book's ID remains unchanged.
    
    Args:
        title: Title of the book to update
        author: Author of the book to update
        update_data: Fields to update (all optional)
    
    Returns:
        Book: The updated book object
    
    Raises:
        HTTPException: 404 if no book matches the title and author
    """
    for i, book in enumerate(BOOKS):
        if book.title == title and book.author == author:
            # Extract only the fields that were explicitly provided
            update_dict = update_data.model_dump(exclude_unset=True)
            
            # Create updated book while preserving the ID
            updated_book = book.copy(update=update_dict)
            
            # Replace the book in the list
            BOOKS[i] = updated_book
            
            return updated_book
    
    # Book not found with given title and author
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Book '{title}' by {author} not found"
    )


@app.delete(
    "/books/delete", 
    status_code=status.HTTP_200_OK,
    summary="Delete a book",
    description="Remove a book from the collection by title and author"
)
async def delete_book_by_title_author(
    title: str = Query(
        ..., 
        min_length=3,
        description="Title of the book to delete"
    ), 
    author: str = Query(
        ..., 
        min_length=3,
        description="Author of the book to delete"
    )
) -> dict:
    """
    Delete a book identified by title and author.
    
    Args:
        title: Title of the book to delete
        author: Author of the book to delete
    
    Returns:
        dict: Confirmation message
    
    Raises:
        HTTPException: 404 if no book matches the title and author
    """
    for i, book in enumerate(BOOKS):
        if book.title == title and book.author == author:
            # Remove the book from the list
            del BOOKS[i]
            
            return {
                "detail": f"Book '{title}' by {author} successfully deleted",
                "status": "success"
            }
    
    # Book not found with given title and author
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Book '{title}' by {author} not found"
    )


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # To run: python main.py
    # Or use: uvicorn main:app --reload
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )