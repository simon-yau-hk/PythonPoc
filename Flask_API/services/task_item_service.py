"""
TaskItem Service for Flask API
Business logic for task item operations
"""

from models.task_item_model import TaskItem
from models.task_model import Task
from database import db 
from typing import List, Optional
from datetime import datetime

class TaskItemService:
    
    @staticmethod
    def get_all_task_items() -> List[TaskItem]:
        """Get all task items"""
        return TaskItem.query.all()
    
    @staticmethod
    def get_task_item_by_id(item_id: int) -> Optional[TaskItem]:
        """Get task item by ID"""
        return TaskItem.query.get(item_id)
    
    @staticmethod
    def get_items_by_task(task_id: int) -> List[TaskItem]:
        """Get all items for a specific task, ordered by 'order' field"""
        return TaskItem.query.filter_by(task_id=task_id).order_by(TaskItem.order).all()
    
    @staticmethod
    def get_completed_items(task_id: int = None) -> List[TaskItem]:
        """Get completed items, optionally filtered by task"""
        query = TaskItem.query.filter_by(is_completed=True)
        if task_id:
            query = query.filter_by(task_id=task_id)
        return query.all()
    
    @staticmethod
    def get_pending_items(task_id: int = None) -> List[TaskItem]:
        """Get pending (not completed) items, optionally filtered by task"""
        query = TaskItem.query.filter_by(is_completed=False)
        if task_id:
            query = query.filter_by(task_id=task_id)
        return query.all()
    
    @staticmethod
    def create_task_item(title: str, task_id: int, description: str = None, 
                        order: int = 0) -> TaskItem:
        """Create a new task item"""
        item = TaskItem(
            title=title,
            description=description,
            task_id=task_id,
            order=order
        )
        db.session.add(item)
        db.session.commit()
        return item
    
    @staticmethod
    def update_task_item(item_id: int, **kwargs) -> Optional[TaskItem]:
        """Update task item by ID"""
        item = TaskItem.query.get(item_id)
        if item:
            for key, value in kwargs.items():
                if hasattr(item, key) and key != 'id':
                    setattr(item, key, value)
            db.session.commit()
        return item
    
    @staticmethod
    def delete_task_item(item_id: int) -> bool:
        """Delete task item by ID"""
        item = TaskItem.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def complete_task_item(item_id: int) -> Optional[TaskItem]:
        """Mark task item as completed"""
        item = TaskItem.query.get(item_id)
        if item:
            item.is_completed = True
            item.completed_at = datetime.utcnow()
            db.session.commit()
        return item
    
    @staticmethod
    def uncomplete_task_item(item_id: int) -> Optional[TaskItem]:
        """Mark task item as not completed"""
        item = TaskItem.query.get(item_id)
        if item:
            item.is_completed = False
            item.completed_at = None
            db.session.commit()
        return item
    
    @staticmethod
    def reorder_items(task_id: int, item_orders: dict) -> bool:
        """
        Reorder task items
        item_orders: dict mapping item_id to new order value
        Example: {1: 0, 2: 1, 3: 2}
        """
        try:
            for item_id, new_order in item_orders.items():
                item = TaskItem.query.get(item_id)
                if item and item.task_id == task_id:
                    item.order = new_order
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

