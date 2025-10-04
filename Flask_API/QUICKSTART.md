# Flask API Quick Start Guide

## 🚀 Getting Started in 3 Steps

### 1. Install Dependencies

```bash
cd Flask_API
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The API will start at `http://localhost:5000`

### 3. Test the API

Open your browser or use curl:

**Test Hello World:**
```bash
curl http://localhost:5000/
```

**Get all users:**
```bash
curl http://localhost:5000/api/users/
```

## 📝 Quick Examples

### Create a User

```bash
curl -X POST http://localhost:5000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "nickname": "johnny"}'
```

### Create a Task (use user_id from above)

```bash
curl -X POST http://localhost:5000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask", "description": "Complete the tutorial", "user_id": 1}'
```

### Get All Tasks

```bash
curl http://localhost:5000/api/tasks/
```

### Update a Task

```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask Advanced", "completed": true}'
```

### Mark Task as Complete

```bash
curl -X PATCH http://localhost:5000/api/tasks/1/complete
```

## 📚 Key Concepts

### Flask Blueprints
Blueprints organize routes into modules (like controllers in FastAPI):

```python
user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    # Handle request
```

### SQLAlchemy Models
Define database tables as Python classes:

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
```

### Service Layer
Business logic separated from controllers:

```python
class UserService:
    @staticmethod
    def create_user(name, email):
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return user
```

## 🔧 Project Structure

```
Flask_API/
├── app.py                    # Main application & configuration
├── requirements.txt          # Python dependencies
├── models/                   # Database models
│   ├── user_model.py
│   └── task_model.py
├── services/                 # Business logic
│   ├── user_service.py
│   └── task_service.py
└── controllers/              # HTTP request handlers (Blueprints)
    ├── user_controller.py
    └── task_controller.py
```

## 🆚 Flask vs FastAPI Comparison

| Feature | FastAPI | Flask |
|---------|---------|-------|
| Routing | `@app.get("/users")` | `@app.route("/users", methods=['GET'])` |
| JSON Response | Return dict directly | Use `jsonify()` |
| Request Body | Pydantic models | `request.get_json()` |
| Path Parameters | Function parameters | Function parameters with type hints |
| Blueprints/Routers | APIRouter | Blueprint |
| ORM Integration | Manual or plugins | Flask-SQLAlchemy |

## 🎓 Learning Tips

1. **Start with app.py** - Understand how Flask app initializes
2. **Explore models** - See how database tables are defined
3. **Check controllers** - Learn how routes are handled
4. **Study services** - Understand business logic separation
5. **Run tests** - Execute `python test_app.py`

## 📖 Next Steps

- Add authentication (Flask-Login or JWT)
- Add input validation (Marshmallow)
- Add database migrations (Flask-Migrate)
- Add API documentation (Flask-RESTX or Flasgger)
- Deploy to production (Gunicorn + Nginx)

## 🔍 Common Flask Patterns

### Error Handling
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404
```

### Before Request Hook
```python
@app.before_request
def before_request():
    # Run before each request
    pass
```

### Database Session Management
```python
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
```

Happy Learning! 🎉

