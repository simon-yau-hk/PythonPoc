# Database Setup Guide for Flask API

This Flask application connects to your **existing MySQL database** with tables: `members`, `tasks`, and `task_items`.

## 🗄️ Database Connection

### Step 1: Configure Database URL

Edit the `.env` file (or create it from `.env.example`):

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/task_management
```

Replace:
- `root` - your MySQL username
- `your_password` - your MySQL password
- `localhost:3306` - your MySQL host and port
- `task_management` - your database name

### Step 2: Verify Database Schema

Make sure your MySQL database has these tables already created:

**Members Table:**
```sql
CREATE TABLE members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE,
    email VARCHAR(254) UNIQUE,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    password_hash VARCHAR(128),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME,
    updated_at DATETIME
);
```

**Tasks Table:**
```sql
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200),
    description TEXT,
    priority VARCHAR(10),
    status VARCHAR(15),
    due_date DATETIME,
    created_at DATETIME,
    updated_at DATETIME,
    member_id INT,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
);
```

**Task Items Table:**
```sql
CREATE TABLE task_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200),
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    `order` INT DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME,
    completed_at DATETIME,
    task_id INT,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
```

## 🔧 SQLAlchemy ORM in Flask

### How Flask Uses SQLAlchemy

Flask uses **Flask-SQLAlchemy**, which is a wrapper around SQLAlchemy ORM:

```python
from flask_sqlalchemy import SQLAlchemy

# Initialize
db = SQLAlchemy(app)

# Define models
class Member(db.Model):
    __tablename__ = 'members'  # Maps to existing table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    # ...
```

### Key Differences: Flask vs FastAPI SQLAlchemy

| Feature | Flask-SQLAlchemy | FastAPI (Pure SQLAlchemy) |
|---------|------------------|---------------------------|
| Import | `from app import db` | `from database import Base, SessionLocal` |
| Model Base | `db.Model` | `Base` from declarative_base() |
| Session | `db.session` | Dependency injection with `get_db()` |
| Query | `Model.query.all()` | `session.query(Model).all()` |
| Add | `db.session.add(obj)` | `session.add(obj)` |
| Commit | `db.session.commit()` | `session.commit()` |

### Example: Flask vs FastAPI

**Flask:**
```python
# Get all members
members = Member.query.all()

# Get by ID
member = Member.query.get(1)

# Filter
active = Member.query.filter_by(is_active=True).all()

# Add new
member = Member(username='john')
db.session.add(member)
db.session.commit()
```

**FastAPI:**
```python
# Get all members
members = session.query(Member).all()

# Get by ID
member = session.query(Member).filter(Member.id == 1).first()

# Filter
active = session.query(Member).filter(Member.is_active == True).all()

# Add new
member = Member(username='john')
session.add(member)
session.commit()
```

## 🚀 Running the Application

### 1. Install Dependencies

```bash
cd Flask_API
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Run the Application

```bash
python app.py
```

The application will:
- Connect to your existing MySQL database
- **NOT create any new tables** (uses existing ones)
- Start server on `http://localhost:5000`

## 📊 Testing Database Connection

### Test Endpoints

1. **Check Connection:**
```bash
curl http://localhost:5000/health
```

2. **Get Members:**
```bash
curl http://localhost:5000/api/members/
```

3. **Get Tasks:**
```bash
curl http://localhost:5000/api/tasks/
```

## 🔍 Important Notes

### Using Existing Tables

The Flask app is configured to **use your existing database tables**:

1. **No `db.create_all()`**: We removed this from `app.py` because tables already exist
2. **Table names match**: `__tablename__` in models matches your SQL schema
3. **Column types match**: SQLAlchemy columns match your MySQL column types
4. **Relationships preserved**: Foreign keys and cascades work as defined

### Model-to-Table Mapping

```python
class Member(db.Model):
    __tablename__ = 'members'  # ← Must match existing table name
    
    # Columns must match existing schema
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
```

## 🐛 Troubleshooting

### Connection Error
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server")
```

**Solutions:**
- Check MySQL is running: `mysql -u root -p`
- Verify credentials in `.env`
- Check host and port are correct

### Table Not Found
```
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'task_management.members' doesn't exist")
```

**Solutions:**
- Run the SQL schema from `Django_API/init_sql.txt`
- Verify database name in `DATABASE_URL`
- Check `__tablename__` matches actual table name

### Authentication Error
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1045, "Access denied for user")
```

**Solutions:**
- Verify MySQL username and password
- Grant privileges: `GRANT ALL PRIVILEGES ON task_management.* TO 'root'@'localhost';`

## 📚 Learn More

- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [Flask Blueprints](https://flask.palletsprojects.com/en/2.3.x/blueprints/)

