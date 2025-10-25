# FastAPI Todo Application

A professional, production-ready RESTful API for managing todo items built with FastAPI and SQLAlchemy.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- 🗄️ SQLite database with SQLAlchemy ORM
- 📝 Comprehensive input validation with Pydantic
- 🔄 Automatic API documentation (Swagger UI & ReDoc)
- ⚡ Async/await support for better performance
- 🎯 Type hints throughout the codebase
- 📊 Structured response models

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **SQLite**: Lightweight database for data persistence

## Project Structure

```
project-3/
├── app.py           # Main application file with API endpoints
├── models.py        # SQLAlchemy database models
├── database.py      # Database configuration and session management
├── project3.db      # SQLite database file (auto-generated)
└── README.md        # This file
```

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. **Clone the repository** (or navigate to the project directory)

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

   This will install all required dependencies including FastAPI, SQLAlchemy, and Uvicorn.

3. **Database initialization**:
   The database will be automatically created when you first run the application.

## Running the Application

### Development Mode

Move to the project folder
```bash
cd project-3
```

Start the development server with hot-reload enabled:

```bash
uv run fastapi dev app.py
```

The API will be available at: `http://localhost:8000`

### Production Mode

For production deployment:

```bash
uv run fastapi run app.py
```

Or directly with uvicorn:

```bash
uv run uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all available endpoints
- Test API calls directly from the browser
- See request/response schemas
- Download the OpenAPI specification

## API Endpoints

### Get All Todos

```http
GET /
```

**Response**: List of all todo items

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": 3,
    "complete": false
  }
]
```

### Get Single Todo

```http
GET /todos/{todo_id}
```

**Parameters**:
- `todo_id` (path): Todo ID (must be > 0)

**Response**: Single todo item or 404 if not found

### Create Todo

```http
POST /todos/
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": 3,
  "complete": false
}
```

**Validation Rules**:
- `title`: Required, minimum 3 characters
- `description`: Optional, maximum 100 characters
- `priority`: Required, must be between 1 and 5
- `complete`: Optional, defaults to false

**Response**: Created todo with HTTP 201 status

### Update Todo

```http
PUT /todos/{todo_id}
```

**Parameters**:
- `todo_id` (path): Todo ID (must be > 0)

**Request Body**: Same as create, but only provided fields are updated

**Response**: Updated todo item or 404 if not found

### Delete Todo

```http
DELETE /todos/{todo_id}
```

**Parameters**:
- `todo_id` (path): Todo ID (must be > 0)

**Response**: Success message with deleted item data

```json
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
```

## Database Schema

### Todos Table

| Column      | Type    | Constraints           | Description                    |
|-------------|---------|----------------------|--------------------------------|
| id          | Integer | Primary Key, Indexed | Unique identifier              |
| title       | String  | Required             | Todo title                     |
| description | String  | Nullable             | Optional description           |
| priority    | Integer | Required             | Priority level (1-5)           |
| complete    | Boolean | Default: False       | Completion status              |

## Development

### Code Style

The project follows:
- Type hints for all functions
- Comprehensive docstrings
- PEP 8 naming conventions
- Async/await best practices

### Adding New Features

1. **New Models**: Add to `models.py`
2. **Database Changes**: Modify `database.py` for configuration
3. **API Endpoints**: Add to `app.py` with proper validation
4. **Dependencies**: Update `pyproject.toml` and run `uv sync`

## Testing

You can test the API using:

### cURL

```bash
# Get all todos
curl http://localhost:8000/

# Create a todo
curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test todo", "priority": 3}'

# Update a todo
curl -X PUT http://localhost:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated todo", "priority": 4, "complete": true}'

# Delete a todo
curl -X DELETE http://localhost:8000/todos/1
```

### HTTPie

```bash
# Get all todos
http localhost:8000/

# Create a todo
http POST localhost:8000/todos/ title="Test todo" priority=3

# Update a todo
http PUT localhost:8000/todos/1 title="Updated todo" complete=true

# Delete a todo
http DELETE localhost:8000/todos/1
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET, PUT, DELETE
- `201 Created`: Successful POST
- `404 Not Found`: Resource doesn't exist
- `422 Unprocessable Entity`: Validation errors

Example error response:

```json
{
  "detail": [
    {
      "loc": ["body", "priority"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

## Production Considerations

Before deploying to production:

1. **Change to PostgreSQL/MySQL** for better scalability
2. **Add authentication** (JWT, OAuth2)
3. **Implement rate limiting** to prevent abuse
4. **Add logging** for monitoring and debugging
5. **Use environment variables** for configuration
6. **Set up CORS** if accessed from browsers
7. **Add comprehensive tests** (pytest)
8. **Enable HTTPS** for secure communication

## Troubleshooting

### Database Locked Error

If you encounter database locked errors:
```bash
# Stop all running instances
# Delete the database file
rm project3.db
# Restart the application
```

### Port Already in Use

```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Module Not Found

```bash
# Reinstall dependencies
uv sync --refresh
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate comments
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue in the repository.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Database management by [SQLAlchemy](https://www.sqlalchemy.org/)
- Package management by [uv](https://github.com/astral-sh/uv)