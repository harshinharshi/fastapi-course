# Books Management API - Project 2

A professional RESTful API built with FastAPI for managing a book collection. This project demonstrates full CRUD (Create, Read, Update, Delete) operations with proper validation, error handling, and documentation.

## 📚 Overview

This API allows you to manage a collection of books with features including:
- List all books in the collection
- Add new books with validation
- Search books by title or rating
- Update book information (supports partial updates)
- Delete books from the collection

## 🚀 Features

- **FastAPI Framework**: High-performance, modern Python web framework
- **Automatic API Documentation**: Interactive docs with Swagger UI
- **Data Validation**: Pydantic models with built-in validation
- **Type Safety**: Full type hints throughout the codebase
- **RESTful Design**: Follows REST principles and best practices
- **In-Memory Database**: Quick setup with pre-populated sample data
- **Comprehensive Error Handling**: Meaningful error messages and status codes

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI**: Web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **Starlette**: Lightweight ASGI framework (FastAPI dependency)

## 📋 Prerequisites

Before running this project, ensure you have:
- Python 3.10 or higher installed
- pip (Python package manager)

## 💻 Installation

1. **Clone the repository** (or download the files)
```bash
git clone <your-repository-url>
cd books-api
```

2. **Create a virtual environment** (recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn pydantic
```

Or using a requirements.txt file:
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
```

## 🏃 Running the Application

### Method 1: Direct Execution
```bash
python main.py
```

### Method 2: Using Uvicorn
```bash
uvicorn main:app --reload
```

The API will start running on `http://localhost:8000`

**Options:**
- `--reload`: Auto-reload on code changes (development mode)
- `--host 0.0.0.0`: Make accessible on network
- `--port 8080`: Use a different port

## 📖 API Documentation

Once the application is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test all endpoints directly from your browser.

## 🔌 API Endpoints

### 1. Get All Books
**GET** `/books`

Returns a list of all books in the collection.

**Response:**
```json
[
  {
    "id": "uuid-string",
    "title": "1984",
    "author": "George Orwell",
    "description": "Dystopian novel about totalitarianism",
    "published_year": 1949,
    "rating": 4.8
  }
]
```

### 2. Add a New Book
**POST** `/books`

Creates a new book with an auto-generated ID.

**Request Body:**
```json
{
  "title": "The Catcher in the Rye",
  "author": "J.D. Salinger",
  "description": "A novel about teenage rebellion",
  "published_year": 1951,
  "rating": 4.0
}
```

**Response:** `201 Created`
```json
{
  "id": "generated-uuid",
  "title": "The Catcher in the Rye",
  "author": "J.D. Salinger",
  "description": "A novel about teenage rebellion",
  "published_year": 1951,
  "rating": 4.0
}
```

### 3. Get Book by Title
**GET** `/books/title/{book_title}`

Retrieves a specific book by its exact title.

**Example:** `/books/title/1984`

**Response:** `200 OK`

### 4. Get Books by Rating
**GET** `/books/rating/{rating}`

Retrieves all books with a specific rating.

**Example:** `/books/rating/4.8`

**Response:** `200 OK`

### 5. Update a Book
**PUT** `/books/update`

Updates a book identified by title and author. Supports partial updates.

**Query Parameters:**
- `title`: Book title (required)
- `author`: Book author (required)

**Request Body:**
```json
{
  "rating": 4.9,
  "description": "Updated description"
}
```

**Response:** `200 OK`

### 6. Delete a Book
**DELETE** `/books/delete`

Deletes a book identified by title and author.

**Query Parameters:**
- `title`: Book title (required)
- `author`: Book author (required)

**Example:** `/books/delete?title=1984&author=George%20Orwell`

**Response:** `200 OK`
```json
{
  "detail": "Book '1984' by George Orwell successfully deleted",
  "status": "success"
}
```

## 📊 Data Models

### Book Model
```python
{
  "id": "string (UUID)",
  "title": "string (min 3 chars)",
  "author": "string (min 3 chars)",
  "description": "string (optional)",
  "published_year": "integer (optional)",
  "rating": "float (0-5, optional)"
}
```

## ⚠️ Error Responses

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error

**Example Error Response:**
```json
{
  "detail": "Book with title 'Unknown Book' not found"
}
```

## 🧪 Testing the API

### Using cURL

**Get all books:**
```bash
curl http://localhost:8000/books
```

**Add a new book:**
```bash
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "author": "Test Author",
    "rating": 4.5
  }'
```

**Delete a book:**
```bash
curl -X DELETE "http://localhost:8000/books/delete?title=Test%20Book&author=Test%20Author"
```

### Using Python Requests

```python
import requests

# Get all books
response = requests.get("http://localhost:8000/books")
print(response.json())

# Add a new book
new_book = {
    "title": "New Book",
    "author": "New Author",
    "rating": 4.5
}
response = requests.post("http://localhost:8000/books", json=new_book)
print(response.json())
```

## 📁 Project Structure

```
books-api/
│
├── main.py              # Main application file
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── .gitignore          # Git ignore file
```

## 🔧 Configuration

### Pydantic Version
This project uses Pydantic v2+ features:
- Use `.model_dump()` instead of `.dict()`
- Enhanced validation and type checking

If you're using Pydantic v1, change `model_dump()` to `dict()` in the code.

## 🚧 Future Enhancements

Potential improvements for this project:
- [ ] Add database integration (PostgreSQL/MongoDB)
- [ ] Implement authentication and authorization
- [ ] Add pagination for book listings
- [ ] Implement search functionality with filters
- [ ] Add unit and integration tests
- [ ] Deploy to cloud platform (AWS/Azure/GCP)
- [ ] Add rate limiting
- [ ] Implement caching
- [ ] Add logging and monitoring

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Your Name**
- Project: Books Management API (Project 2)
- Date: October 2025

## 📞 Support

If you have any questions or run into issues, please:
- Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- Review the interactive API docs at `/docs`
- Open an issue in the repository

## 🙏 Acknowledgments

- FastAPI framework by Sebastián Ramírez
- Python community for excellent libraries
- All contributors to this project

---

**Happy Coding! 📚✨**