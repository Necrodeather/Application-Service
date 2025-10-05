# Application Service

A RESTful service for handling applications with PostgreSQL storage and Kafka messaging.

## ✨ Features

- REST API for creating and retrieving user applications
- Asynchronous data storage using PostgreSQL
- Real-time messaging with Apache Kafka
- Filtering and pagination for application lists
- Docker containerization

## 🛠️ Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM with async support
- **PostgreSQL** - Database
- **Kafka** - Message broker
- **Dishka** - Dependency injection
- **Docker** - Containerization

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your configuration

# Start services
docker-compose up -d

# Application will be available at http://localhost:8000
```

### API Endpoints

**Create Application**

```bash
curl -X POST http://localhost:8000/applications \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John Doe",
    "description": "Application for new service access"
  }'
```

**Get Applications with filtering and pagination**

```bash
curl "http://localhost:8000/applications?user_name=John%20Doe&page=0&size=20"
```

## 🐳 Services

| Service | Port | Description |
|--------|------|-------------|
| Backend | 8000 | FastAPI application |
| Kafka UI | 8080 | Kafka web interface |

## 📝 Configuration

Set environment variables in `.env` file with database credentials and Kafka settings.
