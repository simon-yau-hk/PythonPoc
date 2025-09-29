"""
Task Model - Domain Entity
Represents the core business entity in our domain
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from datetime import datetime
from typing import Optional

Base = declarative_base()


class TaskStatus(PyEnum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(PyEnum):
    """Task priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    """
    Task Entity - Core domain model
    
    This represents a task in our task management system.
    Following Domain-Driven Design principles.
    """
    __tablename__ = "tasks"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic task information
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Task metadata
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    
    # Ownership and assignment
    created_by = Column(String(100), nullable=False)
    assigned_to = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Flags
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status.value}')>"
    
    def __str__(self) -> str:
        return f"Task: {self.title} ({self.status.value})"
    
    # Domain methods (business logic at entity level)
    def mark_as_completed(self) -> None:
        """Mark task as completed with timestamp"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
    
    def assign_to_user(self, user_id: str) -> None:
        """Assign task to a user"""
        self.assigned_to = user_id
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.IN_PROGRESS
    
    def cancel_task(self) -> None:
        """Cancel the task"""
        self.status = TaskStatus.CANCELLED
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date:
            return False
        return (
            self.due_date < datetime.utcnow() and 
            self.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
        )
    
    def can_be_edited(self) -> bool:
        """Check if task can be edited"""
        return self.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
