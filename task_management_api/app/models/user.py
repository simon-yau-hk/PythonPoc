"""
User Model - Domain Entity
Represents a user in our system
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from datetime import datetime
from .task import Base  # Use the same Base as Task

class UserRole(PyEnum):
    """User role enumeration"""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"

class UserStatus(PyEnum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class User(Base):
    """
    User Entity - Core domain model for users
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic user information
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False)
    
    # Authentication (simplified - in real app, hash passwords!)
    password_hash = Column(String(255), nullable=False)
    
    # User metadata
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Flags
    is_deleted = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"
    
    def __str__(self) -> str:
        return f"User: {self.username} ({self.full_name})"
    
    # Domain methods
    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.role == UserRole.ADMIN
    
    def can_manage_tasks(self) -> bool:
        """Check if user can manage tasks"""
        return self.role in [UserRole.ADMIN, UserRole.MANAGER]
    
    def is_active_user(self) -> bool:
        """Check if user is active"""
        return self.status == UserStatus.ACTIVE and not self.is_deleted
    
    def update_last_login(self) -> None:
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
