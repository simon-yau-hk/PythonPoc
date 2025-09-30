from typing import List, Optional, Dict, Any
from django.contrib.auth.models import User
from ..repositories.user_repository import UserRepository
from django.core.exceptions import ValidationError
import re

class UserService:
    """
    Service layer for User business logic
    Contains validation, business rules, and orchestration
    """
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    def get_all_users(self) -> List[User]:
        """Get all users with business logic applied"""
        return list(self.user_repository.get_all())
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID with validation"""
        if user_id <= 0:
            raise ValidationError("User ID must be positive")
        
        return self.user_repository.get_by_id(user_id)
    
    def create_user(self, username: str, email: str, password: str, **kwargs) -> User:
        """Create user with business validation"""
        # Business validation rules
        self._validate_username(username)
        self._validate_email(email)
        self._validate_password(password)
        
        # Check uniqueness
        if self.user_repository.get_by_username(username):
            raise ValidationError("Username already exists")
        
        if self.user_repository.get_by_email(email):
            raise ValidationError("Email already exists")
        
        # Create user
        return self.user_repository.create(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
    
    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user with business validation"""
        if user_id <= 0:
            raise ValidationError("User ID must be positive")
        
        # Validate fields if provided
        if 'username' in kwargs:
            self._validate_username(kwargs['username'])
            # Check if username is taken by another user
            existing_user = self.user_repository.get_by_username(kwargs['username'])
            if existing_user and existing_user.id != user_id:
                raise ValidationError("Username already exists")
        
        if 'email' in kwargs:
            self._validate_email(kwargs['email'])
            # Check if email is taken by another user
            existing_user = self.user_repository.get_by_email(kwargs['email'])
            if existing_user and existing_user.id != user_id:
                raise ValidationError("Email already exists")
        
        if 'password' in kwargs:
            self._validate_password(kwargs['password'])
        
        return self.user_repository.update(user_id, **kwargs)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user with business rules"""
        if user_id <= 0:
            raise ValidationError("User ID must be positive")
        
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False
        
        # Business rule: Don't delete superusers
        if user.is_superuser:
            raise ValidationError("Cannot delete superuser")
        
        # Business rule: Don't delete staff users (optional)
        if user.is_staff:
            raise ValidationError("Cannot delete staff user")
        
        return self.user_repository.delete(user_id)
    
    def get_active_users(self) -> List[User]:
        """Get only active users"""
        return list(self.user_repository.get_active_users())
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics (business logic)"""
        total_users = self.user_repository.count()
        active_users = len(self.get_active_users())
        inactive_users = total_users - active_users
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'active_percentage': (active_users / total_users * 100) if total_users > 0 else 0
        }
    
    def _validate_username(self, username: str) -> None:
        """Validate username business rules"""
        if not username or len(username.strip()) < 3:
            raise ValidationError("Username must be at least 3 characters long")
        
        if len(username) > 150:
            raise ValidationError("Username cannot exceed 150 characters")
        
        # Only alphanumeric and underscore allowed
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores")
    
    def _validate_email(self, email: str) -> None:
        """Validate email business rules"""
        if not email:
            raise ValidationError("Email is required")
        
        # Simple email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError("Invalid email format")
    
    def _validate_password(self, password: str) -> None:
        """Validate password business rules"""
        if not password:
            raise ValidationError("Password is required")
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        # Check for at least one number
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one number")
        
        # Check for at least one letter
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError("Password must contain at least one letter")
