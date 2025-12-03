# FastAPI Quiz App

A comprehensive quiz application built with FastAPI, following Clean Architecture principles, featuring OAuth2 authentication, and full CRUD operations for users, journeys, quizzes, and questions.

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

- **Domain Layer**: Core business entities and repository interfaces
- **Application Layer**: Use cases and business logic
- **Infrastructure Layer**: Database implementations, authentication, and external services
- **API Layer**: FastAPI routes, schemas, and dependencies

## 🚀 Features

- ✅ **User Management**: Complete CRUD operations with OAuth2 authentication
- ✅ **Journey System**: Organize multiple quizzes into learning journeys
- ✅ **Quiz Management**: Create and manage quizzes within journeys
- ✅ **Question System**: Multiple-choice questions with answer validation
- ✅ **JWT Authentication**: Secure token-based authentication
- ✅ **PostgreSQL Database**: Robust relational database with SQLAlchemy ORM
- ✅ **Docker Support**: Full containerization with docker-compose
- ✅ **Comprehensive Tests**: Unit and integration tests with pytest
- ✅ **API Documentation**: Auto-generated with FastAPI (Swagger/ReDoc)

## 📋 Requirements

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

## 🛠️ Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd fast-quizz-app
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the application:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Manual Installation

1. Clone and navigate to the repository:
```bash
git clone <repository-url>
cd fast-quizz-app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the application:
```bash
uvicorn src.main:app --reload
```

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Users
- `GET /api/users/me` - Get current user info
- `GET /api/users/` - List all users
- `GET /api/users/{user_id}` - Get user by ID
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user

### Journeys
- `POST /api/journeys/` - Create a journey
- `GET /api/journeys/` - List user's journeys
- `GET /api/journeys/{journey_id}` - Get journey by ID
- `PUT /api/journeys/{journey_id}` - Update journey
- `DELETE /api/journeys/{journey_id}` - Delete journey

### Quizzes
- `POST /api/quizzes/` - Create a quiz
- `GET /api/quizzes/journey/{journey_id}` - List quizzes in a journey
- `GET /api/quizzes/{quiz_id}` - Get quiz by ID
- `PUT /api/quizzes/{quiz_id}` - Update quiz
- `DELETE /api/quizzes/{quiz_id}` - Delete quiz

### Questions
- `POST /api/questions/` - Create a question
- `GET /api/questions/quiz/{quiz_id}` - List questions in a quiz
- `GET /api/questions/{question_id}` - Get question by ID
- `POST /api/questions/{question_id}/check` - Check answer
- `PUT /api/questions/{question_id}` - Update question
- `DELETE /api/questions/{question_id}` - Delete question

## 🧪 Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test types:
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/
```

## 🗄️ Database

The application uses PostgreSQL with SQLAlchemy ORM. Database schema includes:

- **Users**: User accounts with authentication
- **Journeys**: Collections of quizzes
- **Quizzes**: Quiz content within journeys
- **Questions**: Multiple-choice questions with options

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## 🔒 Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- OAuth2 with Bearer tokens
- CORS middleware configured
- Input validation with Pydantic

## 📁 Project Structure

```
fast-quizz-app/
├── src/
│   ├── domain/              # Domain entities and interfaces
│   │   ├── entities/        # Business entities
│   │   └── repositories/    # Repository interfaces
│   ├── application/         # Business logic
│   │   └── use_cases/       # Use case implementations
│   ├── infrastructure/      # External implementations
│   │   ├── database/        # Database models and connection
│   │   ├── repositories/    # Repository implementations
│   │   └── auth/            # Authentication logic
│   ├── api/                 # FastAPI routes and schemas
│   │   ├── routes/          # API endpoints
│   │   ├── schemas.py       # Pydantic models
│   │   └── dependencies.py  # FastAPI dependencies
│   └── main.py              # Application entry point
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── alembic/                 # Database migrations
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Application container
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛡️ Environment Variables

```env
# Database
DATABASE_URL=postgresql://quizz_user:quizz_password@db:5432/quizz_db

# JWT Authentication
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME="FastAPI Quiz App"
APP_VERSION="0.1.0"
DEBUG=True
```

## 📝 Usage Example

1. Register a new user:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"secure123"}'
```

2. Login to get token:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secure123"}'
```

3. Create a journey (use token from login):
```bash
curl -X POST "http://localhost:8000/api/journeys/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Python Basics","description":"Learn Python fundamentals"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for the ORM
- PostgreSQL for the database
- Clean Architecture principles by Robert C. Martin
