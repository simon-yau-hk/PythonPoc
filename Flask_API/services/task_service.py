"""
Task Service for Flask API
Business logic for task operations
"""

from models.task_model import Task
from models.member_model import Member
from database import db 
from typing import List, Optional
from datetime import datetime

class TaskService:
    
    @staticmethod
    def get_all_tasks(include_items: bool = False) -> List[Task]:
        """Get all tasks"""
        tasks = Task.query.all()
        return tasks
    
    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return Task.query.get(task_id)
    
    @staticmethod
    def get_tasks_by_member(member_id: int) -> List[Task]:
        """Get tasks by member ID"""
        return Task.query.filter_by(member_id=member_id).all()
    
    @staticmethod
    def get_tasks_by_status(status: str) -> List[Task]:
        """Get tasks by status"""
        return Task.query.filter_by(status=status).all()
    
    @staticmethod
    def get_tasks_by_priority(priority: str) -> List[Task]:
        """Get tasks by priority"""
        return Task.query.filter_by(priority=priority).all()
    
    @staticmethod
    def create_task(title: str, member_id: int, description: str = None, 
                   priority: str = 'medium', status: str = 'pending', 
                   due_date: datetime = None) -> Task:
        """Create a new task"""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date,
            member_id=member_id
        )
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def update_task(task_id: int, **kwargs) -> Optional[Task]:
        """Update task by ID"""
        task = Task.query.get(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key) and key != 'id':
                    setattr(task, key, value)
            db.session.commit()
        return task
    
    @staticmethod
    def delete_task(task_id: int) -> bool:
        """Delete task by ID (cascades to task_items)"""
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def complete_task(task_id: int) -> Optional[Task]:
        """Mark task as completed"""
        task = Task.query.get(task_id)
        if task:
            task.status = 'completed'
            db.session.commit()
        return task
