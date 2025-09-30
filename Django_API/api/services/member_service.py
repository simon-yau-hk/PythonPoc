from typing import List, Optional, Dict, Any
from django.core.exceptions import ValidationError
from ..entities.entity import Member
from ..repositories.member_repository import MemberRepository
import hashlib
import re

class MemberService:
    """
    Service layer for Member business logic
    Contains validation, business rules, and orchestration
    """
    
    def __init__(self):
        self.member_repository = MemberRepository()
    
    def get_all_members(self) -> List[Member]:
        """Get all members with business logic applied"""
        return list(self.member_repository.get_all())
    
    def get_member_by_id(self, member_id: int) -> Optional[Member]:
        """Get member by ID with validation"""
        if member_id <= 0:
            raise ValidationError("Member ID must be positive")
        
        return self.member_repository.get_by_id(member_id)
    
    def create_member(self, username: str, email: str, password: str, **kwargs) -> Member:
        """Create member with business validation"""
        # Business validation rules
        self._validate_username(username)
        self._validate_email(email)
        self._validate_password(password)
        
        # Check uniqueness
        if self.member_repository.get_by_username(username):
            raise ValidationError("Username already exists")
        
        if self.member_repository.get_by_email(email):
            raise ValidationError("Email already exists")
        
        # Hash password (simple hash for demo - use proper hashing in production)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Create member
        return self.member_repository.create(
            username=username,
            email=email,
            password_hash=password_hash,
            **kwargs
        )
    
    def update_member(self, member_id: int, **kwargs) -> Optional[Member]:
        """Update member with business validation"""
        if member_id <= 0:
            raise ValidationError("Member ID must be positive")
        
        # Validate fields if provided
        if 'username' in kwargs:
            self._validate_username(kwargs['username'])
            # Check if username is taken by another member
            existing_member = self.member_repository.get_by_username(kwargs['username'])
            if existing_member and existing_member.id != member_id:
                raise ValidationError("Username already exists")
        
        if 'email' in kwargs:
            self._validate_email(kwargs['email'])
            # Check if email is taken by another member
            existing_member = self.member_repository.get_by_email(kwargs['email'])
            if existing_member and existing_member.id != member_id:
                raise ValidationError("Email already exists")
        
        if 'password' in kwargs:
            self._validate_password(kwargs['password'])
            # Hash the new password
            kwargs['password_hash'] = hashlib.sha256(kwargs['password'].encode()).hexdigest()
            del kwargs['password']  # Remove plain password
        
        return self.member_repository.update(member_id, **kwargs)
    
    def delete_member(self, member_id: int) -> bool:
        """Delete member with business rules"""
        if member_id <= 0:
            raise ValidationError("Member ID must be positive")
        
        member = self.member_repository.get_by_id(member_id)
        if not member:
            return False
        
        # Business rule: Check if member has active tasks
        if hasattr(member, 'tasks') and member.tasks.filter(status__in=['pending', 'in_progress']).exists():
            raise ValidationError("Cannot delete member with active tasks")
        
        return self.member_repository.delete(member_id)
    
    def get_active_members(self) -> List[Member]:
        """Get only active members"""
        return list(self.member_repository.get_active_members())
    
    def deactivate_member(self, member_id: int) -> Optional[Member]:
        """Deactivate member instead of deleting"""
        return self.update_member(member_id, is_active=False)
    
    def activate_member(self, member_id: int) -> Optional[Member]:
        """Activate member"""
        return self.update_member(member_id, is_active=True)
    
    def get_member_stats(self) -> Dict[str, Any]:
        """Get member statistics (business logic)"""
        all_members = self.get_all_members()
        active_members = self.get_active_members()
        
        total_count = len(all_members)
        active_count = len(active_members)
        inactive_count = total_count - active_count
        
        return {
            'total_members': total_count,
            'active_members': active_count,
            'inactive_members': inactive_count,
            'active_percentage': (active_count / total_count * 100) if total_count > 0 else 0
        }
    
    def get_all_members_with_tasks(self) -> List[Member]:
        """Get all members with their tasks and task items"""
        return list(self.member_repository.get_all_with_tasks())

    def get_member_with_tasks_by_id(self, member_id: int) -> Optional[Member]:
        """Get member by ID with tasks and task items"""
        if member_id <= 0:
            raise ValidationError("Member ID must be positive")
        
        return self.member_repository.get_by_id_with_tasks(member_id)

    def get_active_members_with_tasks(self) -> List[Member]:
        """Get active members with their tasks and task items"""
        return list(self.member_repository.get_active_members_with_tasks())
    
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
