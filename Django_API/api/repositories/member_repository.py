from typing import List, Optional
from django.db.models import QuerySet, Prefetch
from ..entities.entity import Member, Task, TaskItem

class MemberRepository:
    """
    Repository for Member data access
    """
    
    def get_all(self) -> QuerySet[Member]:
        """Get all members"""
        return Member.objects.all()
    
    def get_all_with_tasks(self) -> QuerySet[Member]:
        """Get all members with their tasks and task items"""
        return Member.objects.prefetch_related(
            Prefetch(
                'tasks',
                queryset=Task.objects.prefetch_related('task_items').order_by('-created_at')
            )
        ).order_by('username')
    
    def get_by_id(self, member_id: int) -> Optional[Member]:
        """Get member by ID"""
        try:
            return Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return None
    
    def get_by_id_with_tasks(self, member_id: int) -> Optional[Member]:
        """Get member by ID with tasks and task items"""
        try:
            return Member.objects.prefetch_related(
                Prefetch(
                    'tasks',
                    queryset=Task.objects.prefetch_related('task_items').order_by('-created_at')
                )
            ).get(id=member_id)
        except Member.DoesNotExist:
            return None
    
    def get_by_username(self, username: str) -> Optional[Member]:
        """Get member by username"""
        try:
            return Member.objects.get(username=username)
        except Member.DoesNotExist:
            return None
    
    def get_by_email(self, email: str) -> Optional[Member]:
        """Get member by email"""
        try:
            return Member.objects.get(email=email)
        except Member.DoesNotExist:
            return None
    
    def create(self, **kwargs) -> Member:
        """Create new member"""
        return Member.objects.create(**kwargs)
    
    def update(self, member_id: int, **kwargs) -> Optional[Member]:
        """Update member"""
        member = self.get_by_id(member_id)
        if not member:
            return None
        
        for key, value in kwargs.items():
            if hasattr(member, key):
                setattr(member, key, value)
        
        member.save()
        return member
    
    def delete(self, member_id: int) -> bool:
        """Delete member"""
        member = self.get_by_id(member_id)
        if member:
            member.delete()
            return True
        return False
    
    def get_active_members(self) -> QuerySet[Member]:
        """Get only active members"""
        return Member.objects.filter(is_active=True)
    
    def get_active_members_with_tasks(self) -> QuerySet[Member]:
        """Get active members with their tasks and task items"""
        return Member.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                'tasks',
                queryset=Task.objects.prefetch_related('task_items').order_by('-created_at')
            )
        ).order_by('username')
