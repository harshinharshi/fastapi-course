# Book Management API - Project 1

A beginner-friendly RESTful API built with FastAPI for managing a collection of books. This project demonstrates the fundamentals of API development, CRUD operations, and HTTP methods.

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Project Structure](#project-structure)
- [Learning Objectives](#learning-objectives)
- [Common Issues & Solutions](#common-issues--solutions)
- [Student Assignment](#student-assignment)

## 🎯 Overview

This project is a simple Book Management API that allows users to perform Create, Read, Update, and Delete (CRUD) operations on a collection of books. It serves as an excellent introduction to:

- RESTful API design
- FastAPI framework
- HTTP methods and status codes
- Data validation with Pydantic
- API documentation

## ✨ Features

- **Get All Books**: Retrieve the complete list of books
- **Get Book by ID**: Find a specific book using its unique identifier
- **Search by Category**: Filter books by their category
- **Search by Author**: Find books by author name (supports partial matching)
- **Create New Book**: Add a new book to the collection
- **Update Book**: Modify existing book details
- **Delete Book**: Remove a book from the collection
- **Automatic API Documentation**: Interactive docs powered by Swagger UI and ReDoc

## 🛠️ Technologies Used

- **Python 3.8+**: Programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application

## 📦 Installation

### Prerequisites

Make sure you have Python 3.8 or higher installed on your system. You can check your Python version by running:

```bash
python --version
```

### Step 1: Clone or Download the Project

Download the project files to your local machine.

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment helps keep your project dependencies isolated.

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the required packages using pip:

```bash
pip install fastapi uvicorn
```

Or if you have a requirements.txt file:

```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

### Method 1: Using Python

Navigate to the project directory and run:

```bash
python main.py
```

### Method 2: Using Uvicorn directly

```bash
uvicorn main:app --reload
```

The application will start on `http://127.0.0.1:8000`

### Accessing the API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://127.0.0.1:8000/docs (Interactive API documentation)
- **ReDoc**: http://127.0.0.1:8000/redoc (Alternative documentation)
- **API Root**: http://127.0.0.1:8000 (Welcome message)

## 📝 API Endpoints

### 1. Root Endpoint

```http
GET /
```

Returns a welcome message and API information.

### 2. Get All Books

```http
GET /books/
```

Returns a list of all books in the collection.

**Response Example:**
```json
[
  {
    "id": 1,
    "title": "1984",
    "author": "George Orwell",
    "category": "Fiction"
  }
]
```

### 3. Get Book by ID

```http
GET /books/{book_id}
```

**Parameters:**
- `book_id` (path parameter): Integer ID of the book

**Example:** `GET /books/1`

### 4. Get Books by Category

```http
GET /books/category/{category}
```

**Parameters:**
- `category` (path parameter): Category name (case-insensitive)

**Example:** `GET /books/category/Fiction`

### 5. Search Books by Author

```http
GET /books/author/{author_name}
```

**Parameters:**
- `author_name` (path parameter): Author name or partial name

**Example:** `GET /books/author/orwell`

### 6. Create a New Book

```http
POST /books/
```

**Request Body:**
```json
{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "category": "Fantasy"
}
```

### 7. Update a Book

```http
PUT /books/{book_id}
```

**Parameters:**
- `book_id` (path parameter): Integer ID of the book to update

**Request Body:**
```json
{
  "title": "1984 (Updated Edition)",
  "category": "Dystopian Fiction"
}
```

### 8. Delete a Book

```http
DELETE /books/{book_id}
```

**Parameters:**
- `book_id` (path parameter): Integer ID of the book to delete

## 🧪 Testing the API

### Using Swagger UI (Recommended for Beginners)

1. Navigate to http://127.0.0.1:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the required parameters
5. Click "Execute" to see the response

### Using curl (Command Line)

```bash
# Get all books
curl http://127.0.0.1:8000/books/

# Get book by ID
curl http://127.0.0.1:8000/books/1

# Create a new book
curl -X POST "http://127.0.0.1:8000/books/" \
     -H "Content-Type: application/json" \
     -d '{"title":"The Hobbit","author":"J.R.R. Tolkien","category":"Fantasy"}'

# Update a book
curl -X PUT "http://127.0.0.1:8000/books/1" \
     -H "Content-Type: application/json" \
     -d '{"title":"1984 (Updated)"}'

# Delete a book
curl -X DELETE "http://127.0.0.1:8000/books/1"
```

### Using Postman or Thunder Client

Import the API endpoints and test them visually using these popular tools.

## 📂 Project Structure

```
book-management-api/
│
├── main.py                 # Main application file with all code
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation (this file)
```

### Code Organization

The `main.py` file contains:

- **Imports**: Required libraries and modules
- **FastAPI App Instance**: Application initialization
- **In-Memory Database**: BOOKS list storing book data
- **Pydantic Models**: BookCreate and BookUpdate for validation
- **API Endpoints**: All route handlers (GET, POST, PUT, DELETE)
- **Main Entry Point**: Server startup configuration

## 🎓 Learning Objectives

By completing this project, students will learn:

1. **HTTP Methods**: Understanding GET, POST, PUT, and DELETE
2. **RESTful API Design**: Best practices for structuring APIs
3. **Path Parameters**: Extracting data from URL paths
4. **Request Body**: Handling JSON data in requests
5. **Data Validation**: Using Pydantic models for input validation
6. **Status Codes**: Proper use of HTTP status codes (200, 201, 404)
7. **Error Handling**: Implementing proper error responses
8. **API Documentation**: Auto-generated docs with Swagger/ReDoc
9. **Async/Await**: Understanding asynchronous programming basics
10. **CRUD Operations**: Create, Read, Update, Delete patterns

## ⚠️ Common Issues & Solutions

### Issue 1: Port Already in Use

**Error:** `Address already in use`

**Solution:** Either kill the process using port 8000 or change the port:

```python
uvicorn.run(app, host="127.0.0.1", port=8001)
```

### Issue 2: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Make sure you've installed the dependencies:

```bash
pip install fastapi uvicorn
```

### Issue 3: Cannot Access API from Other Devices

**Problem:** Want to access API from phone or another computer

**Solution:** Change host to `0.0.0.0`:

```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Issue 4: Changes Not Reflecting

**Problem:** Code changes don't appear when testing

**Solution:** Make sure `reload=True` is set, or restart the server manually.

## 📚 Additional Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [REST API Tutorial](https://restfulapi.net/)

---

## 🎯 Student Assignment: Enhance the Book Management API

Now that you've learned the basics of building a RESTful API, it's time to put your skills to the test! Complete the following assignments to deepen your understanding.

### Assignment Overview

You will enhance the existing Book Management API by adding new features, improving functionality, and implementing best practices. Choose assignments based on your comfort level.

---

### Level 1: Basic Enhancements (Beginner)

**Estimated Time:** 2-3 hours

#### Task 1: Add More Book Attributes

Expand the book model to include additional fields:
- `publication_year` (integer)
- `isbn` (string, optional)
- `pages` (integer)
- `rating` (float, 0-5 scale)

**Requirements:**
- Update both `BookCreate` and `BookUpdate` models
- Add sample data with new fields
- Test all endpoints to ensure they work correctly

#### Task 2: Implement Search by Year Range

Create a new endpoint that allows searching for books published within a specific year range.

**Example:** `GET /books/year-range?start_year=1900&end_year=1950`

**Requirements:**
- Use query parameters for `start_year` and `end_year`
- Return all books within the specified range
- Handle cases where no books are found

#### Task 3: Add Pagination

Implement pagination for the "Get All Books" endpoint to handle large collections.

**Example:** `GET /books/?skip=0&limit=10`

**Requirements:**
- Add `skip` and `limit` query parameters
- Return only the specified number of books
- Set default values (skip=0, limit=10)

---

### Level 2: Intermediate Features (Intermediate)

**Estimated Time:** 4-6 hours

#### Task 4: Implement Data Persistence

Replace the in-memory list with persistent storage.

**Option A:** Use JSON file storage
- Create functions to save/load books from a JSON file
- Ensure data persists between server restarts

**Option B:** Use SQLite database (more advanced)
- Set up SQLAlchemy with SQLite
- Create proper database models
- Implement database CRUD operations

#### Task 5: Add Input Validation and Error Handling

Improve the API's robustness:
- Validate that book IDs are positive integers
- Ensure ISBN follows proper format (if implemented)
- Validate rating is between 0-5
- Prevent duplicate book IDs
- Return appropriate error messages for all validation failures

#### Task 6: Implement Sorting

Add the ability to sort books by different criteria.

**Example:** `GET /books/?sort_by=title&order=asc`

**Requirements:**
- Support sorting by: title, author, publication_year, rating
- Support both ascending and descending order
- Default to sorting by ID if not specified

---

### Level 3: Advanced Challenges (Advanced)

**Estimated Time:** 8-10 hours

#### Task 7: Add User Authentication

Implement basic authentication for the API:
- Create a user registration endpoint
- Implement login with JWT tokens
- Protect certain endpoints (create, update, delete) - require authentication
- Allow anyone to read books (GET endpoints)

**Tools to Use:**
- `python-jose` for JWT
- `passlib` for password hashing
- `python-multipart` for form data

#### Task 8: Add Book Reviews System

Create a new feature for users to review books:
- Create a `Review` model with: user_id, book_id, rating, comment, date
- Add endpoints:
  - `POST /books/{book_id}/reviews` - Add a review
  - `GET /books/{book_id}/reviews` - Get all reviews for a book
  - `PUT /reviews/{review_id}` - Update a review
  - `DELETE /reviews/{review_id}` - Delete a review
- Calculate and display average rating for each book

#### Task 9: Implement Advanced Search

Create a comprehensive search endpoint with multiple filters:

**Example:** `GET /books/search?query=dystopian&category=Fiction&min_rating=4&max_year=2000`

**Requirements:**
- Support text search in title and author
- Filter by category, rating range, year range
- Combine multiple filters
- Return ranked results (best matches first)

#### Task 10: Add API Rate Limiting and Caching

Implement performance optimizations:
- Add rate limiting (e.g., 100 requests per minute per IP)
- Implement caching for frequently accessed endpoints
- Add request logging with timestamps
- Create a statistics endpoint showing API usage

---

### Bonus Challenge: Complete API Redesign 🌟

**For Advanced Students**

Create a **Movie Management API** from scratch using everything you've learned:

**Requirements:**
- Movies should have: title, director, cast (list), genre, release_year, duration, rating
- Implement all CRUD operations
- Add advanced search and filtering
- Include user authentication
- Add a "watchlist" feature where users can save movies
- Implement movie recommendations based on genre preferences
- Add proper error handling and validation
- Write comprehensive API documentation
- Include unit tests for all endpoints

---

### Submission Guidelines

1. **Code Quality:**
   - Follow PEP 8 style guidelines
   - Include comprehensive comments
   - Write clear docstrings for all functions

2. **Documentation:**
   - Update the README with new features
   - Document all new endpoints
   - Include examples of API calls

3. **Testing:**
   - Test all endpoints using Swagger UI
   - Provide screenshots or a video demo
   - Document any issues encountered and how you solved them

4. **Reflection:**
   - Write a brief reflection (200-300 words) on:
     - What you learned
     - Challenges you faced
     - How you overcame difficulties
     - What you would improve next time

### Evaluation Criteria

- **Functionality (40%)**: Does the code work as expected?
- **Code Quality (25%)**: Is the code clean, readable, and well-organized?
- **Documentation (20%)**: Are the changes well-documented?
- **Testing (10%)**: Has the code been thoroughly tested?
- **Creativity (5%)**: Any innovative features or solutions?

---

## 📧 Support

If you encounter any issues or have questions:
1. Check the Common Issues section above
2. Review the FastAPI documentation
3. Ask your instructor or peers for help
4. Search for solutions on Stack Overflow

**Good luck with your assignment! Happy coding! 🚀**