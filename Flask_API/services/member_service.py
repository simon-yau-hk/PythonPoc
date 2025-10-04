"""
Member Service for Flask API
Business logic for member operations
"""

from models.member_model import Member
from models.task_model import Task
from models.task_item_model import TaskItem
from database import db 
from typing import List, Optional
from sqlalchemy.orm import joinedload

class MemberService:
    
    @staticmethod
    def get_all_members() -> List[Member]:
        """Get all members"""
        return Member.query.all()
    
    @staticmethod
    def get_all_members_with_tasks_and_items() -> List[Member]:
        """Get all members with their tasks and task items using eager loading"""
        return Member.query.options(
            joinedload(Member.tasks).joinedload(Task.task_items)
        ).all()
    
    @staticmethod
    def get_member_by_id(member_id: int) -> Optional[Member]:
        """Get member by ID"""
        return Member.query.get(member_id)
    
    @staticmethod
    def get_member_by_email(email: str) -> Optional[Member]:
        """Get member by email"""
        return Member.query.filter_by(email=email).first()
    
    @staticmethod
    def get_member_by_username(username: str) -> Optional[Member]:
        """Get member by username"""
        return Member.query.filter_by(username=username).first()
    
    @staticmethod
    def get_active_members() -> List[Member]:
        """Get all active members"""
        return Member.query.filter_by(is_active=True).all()
    
    @staticmethod
    def create_member(username: str, email: str, first_name: str = None, 
                     last_name: str = None, password_hash: str = None) -> Member:
        """Create a new member"""
        member = Member(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=password_hash
        )
        db.session.add(member)
        db.session.commit()
        return member
    
    @staticmethod
    def update_member(member_id: int, **kwargs) -> Optional[Member]:
        """Update member by ID"""
        member = Member.query.get(member_id)
        if member:
            for key, value in kwargs.items():
                if hasattr(member, key) and key != 'id':
                    setattr(member, key, value)
            db.session.commit()
        return member
    
    @staticmethod
    def delete_member(member_id: int) -> bool:
        """Delete member by ID (cascades to tasks and task_items)"""
        member = Member.query.get(member_id)
        if member:
            db.session.delete(member)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def deactivate_member(member_id: int) -> Optional[Member]:
        """Deactivate member instead of deleting"""
        member = Member.query.get(member_id)
        if member:
            member.is_active = False
            db.session.commit()
        return member

