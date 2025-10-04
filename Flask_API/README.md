# Flask Web API - Task Management System

A complete Flask web API application that connects to your **existing MySQL database** using **SQLAlchemy ORM**.

## 🎯 Overview

This Flask application demonstrates:
- **Flask-SQLAlchemy ORM** integration with existing MySQL database
- **RESTful API** design with complete CRUD operations
- **Blueprint architecture** for organized routing
- **Service layer pattern** for business logic separation
- **Existing database integration** (no table creation, uses your schema)

## 📋 Database Schema

Works with existing tables:
- **members** - User/member information
- **tasks** - Tasks assigned to members
- **task_items** - Sub-items/checklist items for tasks

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd Flask_API
pip install -r requirements.txt
```

### 2. Configure Database

Create `.env` file:
```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/task_management
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. Run Application

```bash
python app.py
```

Server starts at: `http://localhost:5000`

## 📚 Project Structure

```
Flask_API/
├── app.py                          # Main Flask application
├── config.py                       # Configuration classes
├── requirements.txt                # Python dependencies
├── DATABASE_SETUP.md              # Database connection guide
├── models/                        # SQLAlchemy ORM models
│   ├── member_model.py           # Member (maps to 'members' table)
│   ├── task_model.py             # Task (maps to 'tasks' table)
│   └── task_item_model.py        # TaskItem (maps to 'task_items' table)
├── services/                      # Business logic layer
│   ├── member_service.py         # Member operations
│   ├── task_service.py           # Task operations
│   └── task_item_service.py      # Task item operations
└── controllers/                   # HTTP request handlers (Blueprints)
    ├── member_controller.py       # Member API endpoints
    ├── task_controller.py         # Task API endpoints
    └── task_item_controller.py    # Task item API endpoints
```

## 🔌 API Endpoints

### General Endpoints

- `GET /` - API information
- `GET /health` - Health check

### Member Endpoints

- `GET /api/members/` - Get all members
  - Query: `?active_only=true` - Filter active members only
- `GET /api/members/{id}` - Get member by ID
- `POST /api/members/` - Create new member
- `PUT /api/members/{id}` - Update member
- `DELETE /api/members/{id}` - Delete member (cascades to tasks)
- `PATCH /api/members/{id}/deactivate` - Deactivate member
- `GET /api/members/{id}/tasks` - Get all tasks for member

### Task Endpoints

- `GET /api/tasks/` - Get all tasks
  - Query: `?status=pending` - Filter by status
  - Query: `?priority=high` - Filter by priority
  - Query: `?member_id=1` - Filter by member
  - Query: `?include_items=true` - Include task items
- `GET /api/tasks/{id}` - Get task by ID
- `POST /api/tasks/` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task (cascades to items)
- `PATCH /api/tasks/{id}/complete` - Mark task as completed
- `GET /api/tasks/{id}/items` - Get all items for task

### Task Item Endpoints

- `GET /api/task-items/` - Get all task items
  - Query: `?task_id=1` - Filter by task
  - Query: `?completed=true` - Filter completed items
- `GET /api/task-items/{id}` - Get task item by ID
- `POST /api/task-items/` - Create new task item
- `PUT /api/task-items/{id}` - Update task item
- `DELETE /api/task-items/{id}` - Delete task item
- `PATCH /api/task-items/{id}/complete` - Mark as completed
- `PATCH /api/task-items/{id}/uncomplete` - Mark as not completed
- `POST /api/task-items/reorder` - Reorder items

## 💡 Example Usage

### Create a Member

```bash
curl -X POST http://localhost:5000/api/members/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Create a Task

```bash
curl -X POST http://localhost:5000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Flask Tutorial",
    "description": "Learn Flask ORM integration",
    "priority": "high",
    "status": "pending",
    "member_id": 1,
    "due_date": "2025-12-31T23:59:59"
  }'
```

### Create Task Items (Checklist)

```bash
curl -X POST http://localhost:5000/api/task-items/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Read documentation",
    "description": "Read Flask-SQLAlchemy docs",
    "task_id": 1,
    "order": 0
  }'
```

### Get Tasks with Items

```bash
curl "http://localhost:5000/api/tasks/1?include_items=true"
```

### Filter Tasks

```bash
# Get high priority tasks
curl "http://localhost:5000/api/tasks/?priority=high"

# Get completed tasks
curl "http://localhost:5000/api/tasks/?status=completed"

# Get tasks for specific member
curl "http://localhost:5000/api/tasks/?member_id=1"
```

## 🔄 Flask vs FastAPI - SQLAlchemy Comparison

### Database Connection

**Flask:**
```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://...'
db = SQLAlchemy(app)
```

**FastAPI:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://...')
SessionLocal = sessionmaker(bind=engine)
```

### Models

**Flask:**
```python
class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
```

**FastAPI:**
```python
class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
```

### Querying

**Flask:**
```python
# Simple query
members = Member.query.all()
member = Member.query.get(1)
member = Member.query.filter_by(email='test@example.com').first()
```

**FastAPI:**
```python
# Requires session
members = db.query(Member).all()
member = db.query(Member).filter(Member.id == 1).first()
member = db.query(Member).filter(Member.email == 'test@example.com').first()
```

### Session Management

**Flask:**
```python
# Automatic session management
db.session.add(member)
db.session.commit()
```

**FastAPI:**
```python
# Manual session via dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 🎓 Learning Resources

1. **DATABASE_SETUP.md** - Complete database setup guide
2. **QUICKSTART.md** - Quick start guide
3. **models/** - Study SQLAlchemy model definitions
4. **services/** - Business logic patterns
5. **controllers/** - Flask Blueprint routing

## 🔧 Key Features

### SQLAlchemy ORM Benefits

✅ **Object-Relational Mapping** - Work with Python objects, not SQL
✅ **Automatic Query Generation** - ORM generates SQL for you
✅ **Relationship Management** - Easy foreign key handling
✅ **Type Safety** - Python type hints and validation
✅ **Query API** - Chainable, expressive query interface

### Flask-SQLAlchemy Features

✅ **Flask Integration** - Seamless Flask app integration
✅ **Automatic Session** - `db.session` managed automatically
✅ **Query Property** - `Model.query` shortcut for queries
✅ **Pagination** - Built-in pagination support
✅ **Signals** - Model lifecycle events

## 🐛 Troubleshooting

See **DATABASE_SETUP.md** for detailed troubleshooting.

Common issues:
- **Connection errors**: Check DATABASE_URL in `.env`
- **Table not found**: Verify tables exist in database
- **Import errors**: Run `pip install -r requirements.txt`

## 📖 Next Steps

1. ✅ Test all endpoints with your existing database
2. ✅ Compare with your FastAPI implementation
3. ✅ Add authentication (Flask-Login or JWT)
4. ✅ Add input validation (Marshmallow)
5. ✅ Add API documentation (Flask-RESTX)
6. ✅ Add pagination to list endpoints
7. ✅ Deploy to production

## 🌟 Why Flask + SQLAlchemy?

- **Mature ecosystem**: 10+ years of production use
- **Flexible**: Minimal framework, add what you need
- **Well documented**: Extensive documentation and community
- **Industry standard**: Used by many large companies
- **ORM flexibility**: Can use raw SQL when needed

Happy Learning! 🎉
