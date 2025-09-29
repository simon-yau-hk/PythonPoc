# Task Management API

A comprehensive **Task Management System** demonstrating the **Controller-Service-Repository** pattern in Python with FastAPI.

## 🏗️ Architecture Overview

This project showcases enterprise-level Python architecture following clean code principles:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Controllers   │───▶│    Services     │───▶│  Repositories   │
│   (API Layer)   │    │ (Business Logic)│    │ (Data Access)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      DTOs       │    │   Domain Models │    │    Database     │
│ (Data Transfer) │    │   (Entities)    │    │   (SQLAlchemy)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🎯 **Pattern Benefits Demonstrated:**

- **Separation of Concerns**: Each layer has a single responsibility
- **Dependency Injection**: Loose coupling between components
- **Testability**: Easy to mock and unit test each layer
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to extend and modify functionality

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or poetry

### Installation

```bash
# Clone or navigate to the project directory
cd task_management_api

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Access the API
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
task_management_api/
├── app/
│   ├── controllers/          # 🎮 API Layer
│   │   └── task_controller.py
│   ├── services/            # 🧠 Business Logic Layer
│   │   └── task_service.py
│   ├── repositories/        # 💾 Data Access Layer
│   │   ├── base_repository.py
│   │   └── task_repository.py
│   ├── models/             # 🏗️ Domain Models
│   │   └── task.py
│   ├── dto/                # 📦 Data Transfer Objects
│   │   └── task_dto.py
│   └── database.py         # 🗄️ Database Configuration
├── tests/                  # 🧪 Test Suite
│   └── test_task_service.py
├── main.py                 # 🚀 Application Entry Point
├── requirements.txt        # 📋 Dependencies
└── README.md              # 📖 Documentation
```

## 🔍 Layer Details

### 1. **Controllers (API Layer)**
- Handle HTTP requests/responses
- Input validation and serialization
- Error handling and status codes
- Authentication and authorization
- **Responsibility**: HTTP concerns only

```python
@router.post("/", response_model=TaskResponse)
async def create_task(request: CreateTaskRequest):
    return task_service.create_task(request)
```

### 2. **Services (Business Logic Layer)**
- Business rules and validation
- Transaction orchestration
- Complex operations coordination
- **Responsibility**: Business logic only

```python
def create_task(self, request: CreateTaskRequest) -> TaskResponse:
    self._validate_create_request(request)  # Business validation
    task = Task(...)  # Create domain entity
    return self.task_repository.create(task)  # Delegate to repository
```

### 3. **Repositories (Data Access Layer)**
- Database operations (CRUD)
- Query optimization
- Data mapping
- **Responsibility**: Data access only

```python
def get_paginated(self, page: int, size: int) -> Tuple[List[Task], int]:
    query = self.db.query(Task)
    # Complex query logic
    return query.offset(offset).limit(size).all(), total_count
```

## 🎯 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/tasks/` | Create new task |
| `GET` | `/api/v1/tasks/{id}` | Get task by ID |
| `PUT` | `/api/v1/tasks/{id}` | Update task |
| `DELETE` | `/api/v1/tasks/{id}` | Delete task |
| `GET` | `/api/v1/tasks/` | Get paginated tasks |
| `POST` | `/api/v1/tasks/{id}/complete` | Mark task complete |
| `POST` | `/api/v1/tasks/{id}/assign` | Assign task |
| `GET` | `/api/v1/tasks/user/{id}` | Get user's tasks |
| `GET` | `/api/v1/tasks/stats/overview` | Get statistics |
| `GET` | `/api/v1/tasks/overdue` | Get overdue tasks |

## 💡 Business Rules Implemented

1. **Task Creation**:
   - High/Urgent priority tasks must have due dates
   - Due dates cannot be in the past
   - Task titles must be unique per user

2. **Task Updates**:
   - Only creators or assignees can modify tasks
   - Completed/cancelled tasks cannot be edited
   - Status transitions follow business rules

3. **Authorization**:
   - Users can only access their own tasks
   - Only creators can delete tasks
   - Admin users have broader access

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Test Strategy:
- **Unit Tests**: Test each layer in isolation
- **Integration Tests**: Test layer interactions
- **Mocking**: Mock dependencies for isolated testing

## 🔧 Configuration

### Environment Variables:
- `DATABASE_URL`: Database connection string
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Development:
```bash
export DATABASE_URL="sqlite:///./tasks.db"
export LOG_LEVEL="DEBUG"
python main.py
```

### Production:
```bash
export DATABASE_URL="postgresql://user:pass@localhost/tasks"
export LOG_LEVEL="INFO"
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🚀 Scaling Considerations

### Horizontal Scaling:
- Stateless design enables multiple instances
- Database connection pooling
- Load balancer compatible

### Performance Optimizations:
- Repository layer handles query optimization
- Pagination for large datasets
- Async/await for I/O operations
- Database indexing on frequently queried fields

### Monitoring:
- Structured logging throughout all layers
- Health check endpoints
- Error tracking and metrics

## 🔄 Extending the System

### Adding New Features:
1. **Create DTO** for request/response
2. **Add Repository methods** for data access
3. **Implement Service logic** with business rules
4. **Create Controller endpoints** for API
5. **Write tests** for each layer

### Example - Adding Comments:
```python
# 1. DTO
class CommentRequest(BaseModel):
    task_id: int
    content: str

# 2. Repository
def add_comment(self, comment: Comment) -> Comment:
    return self.create(comment)

# 3. Service
def add_comment(self, request: CommentRequest) -> CommentResponse:
    # Business validation
    comment = Comment(...)
    return self.comment_repository.add_comment(comment)

# 4. Controller
@router.post("/tasks/{task_id}/comments")
async def add_comment(request: CommentRequest):
    return comment_service.add_comment(request)
```

## 🎓 Learning Outcomes

This example demonstrates:

✅ **Clean Architecture** principles in Python
✅ **Dependency Injection** without heavy frameworks
✅ **Domain-Driven Design** concepts
✅ **RESTful API** design with FastAPI
✅ **Business Logic** separation
✅ **Error Handling** strategies
✅ **Testing** patterns for each layer
✅ **Documentation** and API specs
✅ **Scalable** project structure

## 🆚 Comparison with C#/Java

| Aspect | Python (This Example) | C# | Java |
|--------|----------------------|-----|------|
| **Boilerplate** | Minimal | Medium | High |
| **Type Safety** | Optional (Pydantic) | Strong | Strong |
| **Development Speed** | Fast | Medium | Slower |
| **Performance** | Good for I/O | Excellent | Excellent |
| **Enterprise Features** | Demonstrated | Native | Native |
| **Learning Curve** | Gentle | Medium | Steep |

---

**This example proves Python is absolutely capable of enterprise-level applications with proper architecture!** 🐍✨
