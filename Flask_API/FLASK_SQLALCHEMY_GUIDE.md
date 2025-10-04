# Flask SQLAlchemy Complete Guide

## 🎯 Yes, Flask Uses SQLAlchemy ORM!

Flask uses **Flask-SQLAlchemy**, which is a Flask extension that adds support for SQLAlchemy to your Flask application. It's the same SQLAlchemy ORM you use in FastAPI, but with Flask-specific convenience features.

## 🔄 Flask-SQLAlchemy vs Pure SQLAlchemy

### Architecture Comparison

```
FastAPI + SQLAlchemy:
┌─────────────┐
│   FastAPI   │
└──────┬──────┘
       │
       ├── Pure SQLAlchemy
       ├── Manual SessionLocal
       └── Dependency Injection (get_db)

Flask + Flask-SQLAlchemy:
┌─────────────┐
│    Flask    │
└──────┬──────┘
       │
       ├── Flask-SQLAlchemy (wrapper)
       │   └── SQLAlchemy (underneath)
       ├── Automatic db.session
       └── App context integration
```

## 📚 Side-by-Side Comparison

### 1. Setup & Configuration

**FastAPI (Pure SQLAlchemy):**
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:pass@localhost/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Flask (Flask-SQLAlchemy):**
```python
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:pass@localhost/db'
db = SQLAlchemy(app)

# That's it! No need for SessionLocal or get_db()
```

### 2. Model Definition

**FastAPI:**
```python
from sqlalchemy import Column, Integer, String
from database import Base

class Member(Base):
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(150))
    email = Column(String(254))
```

**Flask:**
```python
from app import db

class Member(db.Model):
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(254))
```

**Difference:** 
- FastAPI: `Column` from sqlalchemy, inherit from `Base`
- Flask: `db.Column`, inherit from `db.Model`

### 3. Relationships

**FastAPI:**
```python
from sqlalchemy.orm import relationship

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    tasks = relationship("Task", back_populates="member")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id'))
    member = relationship("Member", back_populates="tasks")
```

**Flask:**
```python
class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    tasks = db.relationship('Task', backref='member', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    # No need to define member relationship, backref does it
```

**Difference:**
- FastAPI: Explicit two-way relationships with `back_populates`
- Flask: `backref` automatically creates reverse relationship

### 4. Querying Data

**FastAPI:**
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

@app.get("/members/")
def get_members(db: Session = Depends(get_db)):
    # Must use session parameter
    members = db.query(Member).all()
    return members

@app.get("/members/{id}")
def get_member(id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == id).first()
    return member
```

**Flask:**
```python
@app.route("/members/")
def get_members():
    # No session parameter needed
    members = Member.query.all()
    return jsonify([m.to_dict() for m in members])

@app.route("/members/<int:id>")
def get_member(id):
    member = Member.query.get(id)  # Simpler!
    return jsonify(member.to_dict())
```

**Difference:**
- FastAPI: Pass `db: Session` as dependency
- Flask: Use `Model.query` directly (automatic session)

### 5. Adding Data

**FastAPI:**
```python
@app.post("/members/")
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member
```

**Flask:**
```python
@app.route("/members/", methods=['POST'])
def create_member():
    data = request.get_json()
    member = Member(**data)
    db.session.add(member)
    db.session.commit()
    return jsonify(member.to_dict())
```

**Difference:**
- FastAPI: Use injected `db` session
- Flask: Use `db.session` (always available in app context)

### 6. Updating Data

**FastAPI:**
```python
@app.put("/members/{id}")
def update_member(id: int, updates: MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == id).first()
    if member:
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(member, key, value)
        db.commit()
        db.refresh(member)
    return member
```

**Flask:**
```python
@app.route("/members/<int:id>", methods=['PUT'])
def update_member(id):
    member = Member.query.get(id)
    if member:
        data = request.get_json()
        for key, value in data.items():
            setattr(member, key, value)
        db.session.commit()
    return jsonify(member.to_dict())
```

### 7. Deleting Data

**FastAPI:**
```python
@app.delete("/members/{id}")
def delete_member(id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == id).first()
    if member:
        db.delete(member)
        db.commit()
    return {"deleted": True}
```

**Flask:**
```python
@app.route("/members/<int:id>", methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if member:
        db.session.delete(member)
        db.session.commit()
    return jsonify({"deleted": True})
```

## 🎯 Key Differences Summary

| Feature | FastAPI (SQLAlchemy) | Flask (Flask-SQLAlchemy) |
|---------|---------------------|--------------------------|
| **Setup** | Manual engine & session | Automatic with `db = SQLAlchemy(app)` |
| **Model Base** | `Base` (from declarative_base) | `db.Model` |
| **Columns** | `Column(Integer, ...)` | `db.Column(db.Integer, ...)` |
| **Session** | Injected via `Depends(get_db)` | Auto-managed `db.session` |
| **Queries** | `db.query(Model)` | `Model.query` |
| **Filter** | `filter(Model.id == 1)` | `filter_by(id=1)` or `filter()` |
| **Get by ID** | `filter(Model.id == id).first()` | `query.get(id)` |
| **Relationships** | `relationship()` with `back_populates` | `db.relationship()` with `backref` |
| **Transactions** | Manual `db.commit()` | Manual `db.session.commit()` |

## 💡 Flask-SQLAlchemy Advantages

### 1. Simpler Query API
```python
# Flask - More intuitive
members = Member.query.filter_by(is_active=True).all()
member = Member.query.get(1)

# FastAPI - More verbose
members = db.query(Member).filter(Member.is_active == True).all()
member = db.query(Member).filter(Member.id == 1).first()
```

### 2. No Session Management
```python
# Flask - Session automatic
member = Member(username='john')
db.session.add(member)
db.session.commit()

# FastAPI - Must inject session
def create(db: Session = Depends(get_db)):
    member = Member(username='john')
    db.add(member)
    db.commit()
```

### 3. Built-in Pagination
```python
# Flask
members = Member.query.paginate(page=1, per_page=20)
for member in members.items:
    print(member.username)

# FastAPI - Must implement manually
members = db.query(Member).offset(0).limit(20).all()
```

## 🔧 Query Examples

### Basic Queries

```python
# Get all
members = Member.query.all()

# Get by primary key
member = Member.query.get(1)

# Get first match
member = Member.query.filter_by(email='test@test.com').first()

# Get or 404
member = Member.query.get_or_404(1)

# Count
count = Member.query.count()
```

### Filtering

```python
# Simple filter
active = Member.query.filter_by(is_active=True).all()

# Complex filter
admins = Member.query.filter(
    Member.is_active == True,
    Member.role == 'admin'
).all()

# OR condition
from sqlalchemy import or_
results = Member.query.filter(
    or_(Member.username == 'john', Member.email == 'john@test.com')
).all()

# LIKE
results = Member.query.filter(Member.username.like('%john%')).all()

# IN
results = Member.query.filter(Member.id.in_([1, 2, 3])).all()
```

### Ordering

```python
# Ascending
members = Member.query.order_by(Member.username).all()

# Descending
members = Member.query.order_by(Member.created_at.desc()).all()

# Multiple
members = Member.query.order_by(
    Member.is_active.desc(),
    Member.username
).all()
```

### Joining & Relationships

```python
# Access relationship (automatic join)
member = Member.query.get(1)
tasks = member.tasks  # Returns list of Task objects

# Eager loading (avoid N+1 queries)
from sqlalchemy.orm import joinedload
members = Member.query.options(joinedload(Member.tasks)).all()

# Filter on relationship
members_with_tasks = Member.query.filter(Member.tasks.any()).all()
```

### Aggregation

```python
from sqlalchemy import func

# Count by group
results = db.session.query(
    Task.status,
    func.count(Task.id)
).group_by(Task.status).all()

# Sum
total = db.session.query(func.sum(Task.id)).scalar()

# Average
avg = db.session.query(func.avg(Task.id)).scalar()
```

## 🚀 Using Your Existing Database

### Important: Your App Uses Existing Tables!

```python
# ❌ DON'T DO THIS - Will try to create tables
if __name__ == '__main__':
    db.create_all()  # Don't use this!
    app.run()

# ✅ DO THIS - Just connect to existing tables
if __name__ == '__main__':
    app.run()  # Tables already exist in MySQL
```

### How It Works

1. **Define models** that match your existing table structure
2. **SQLAlchemy maps** Python classes to database tables
3. **No table creation** needed - just connect and query!

```python
class Member(db.Model):
    __tablename__ = 'members'  # ← Must match existing table
    
    # Columns must match existing schema
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
```

When you query `Member.query.all()`, SQLAlchemy:
1. Generates SQL: `SELECT * FROM members`
2. Executes against your MySQL database
3. Maps results to `Member` objects
4. Returns Python objects you can work with

## 📖 Learn More

- **Official Docs**: https://flask-sqlalchemy.palletsprojects.com/
- **SQLAlchemy Core**: https://docs.sqlalchemy.org/
- **Flask Mega-Tutorial**: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

## 🎓 Key Takeaways

1. ✅ Flask uses **SQLAlchemy ORM** (same as FastAPI)
2. ✅ **Flask-SQLAlchemy** adds Flask-specific conveniences
3. ✅ **Simpler API** - `Model.query` vs `session.query(Model)`
4. ✅ **Automatic session** - no dependency injection needed
5. ✅ **Works with existing databases** - no table creation required
6. ✅ **Same concepts** - just slightly different syntax

You already know SQLAlchemy from FastAPI, so Flask will feel familiar! 🎉

