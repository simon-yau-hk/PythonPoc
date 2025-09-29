from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, Enum, ForeignKey, BigInteger, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from database import Base

# Define Python enums to match your MySQL enums
class TaskStatus(PyEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class TaskPriority(PyEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class UserRole(PyEnum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    USER = "USER"
    GUEST = "GUEST"

class UserStatus(PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class User(Base):
    __tablename__ = "users"
    
    # Match your existing columns exactly
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, nullable=False)
    email_verified = Column(Boolean, nullable=False)
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    
    # Match your existing columns exactly
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, index=True)
    priority = Column(Enum(TaskPriority), nullable=False)
    created_by = Column(String(100), nullable=False)
    assigned_to = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, nullable=False)
    
        # ✅ Foreign key column (matches your database)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    task_details = relationship("TaskDetail", back_populates="task", cascade="all, delete-orphan")
    user = relationship("User", back_populates="tasks")

class TaskDetailType( PyEnum):
    COMMENT = "COMMENT"
    ATTACHMENT = "ATTACHMENT"
    LOG = "LOG"
    NOTE = "NOTE"
    CHECKLIST_ITEM = "CHECKLIST_ITEM"

class TaskDetail(Base):
    __tablename__ = "task_details"
    
    # SQLAlchemy Column definitions (not type hints!)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    detail_type = Column(Enum(TaskDetailType), nullable=False, index=True)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_size = Column(BigInteger, nullable=True)
    mime_type = Column(String(100), nullable=True)
    task_metadata = Column("metadata", JSON, nullable=True)
    created_by = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    is_deleted = Column(Boolean, nullable=False, default=False)
    order_index = Column(Integer, nullable=True)
    is_completed = Column(Boolean, nullable=True)
    
    # Relationship back to Task
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    task = relationship("Task", back_populates="task_details")