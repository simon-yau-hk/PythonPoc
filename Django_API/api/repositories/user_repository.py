from django.contrib.auth.models import User
from typing import List, Optional, Dict, Any
from django.db.models import QuerySet
import re

class UserRepository:
    """
    Repository pattern for User data access
    Handles all database operations for User model
    """
    
    def get_all(self) -> QuerySet[User]:
        """Get all users"""
        return User.objects.all()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    def create(self, **kwargs) -> User:
        """Create new user"""
        password = kwargs.pop('password', None)
        user = User(**kwargs)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user by ID"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        password = kwargs.pop('password', None)
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        if password:
            user.set_password(password)
        
        user.save()
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user by ID"""
        user = self.get_by_id(user_id)
        if user:
            user.delete()
            return True
        return False
    
    def get_active_users(self) -> QuerySet[User]:
        """Get only active users"""
        return User.objects.filter(is_active=True)
    
    def count(self) -> int:
        """Get total user count"""
        return User.objects.count()


