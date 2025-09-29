"""
Task Repository - Data Access Layer for Tasks
Implements specific data access operations for Task entities
"""

from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from datetime import datetime

from ..models.task import Task, TaskStatus, TaskPriority
from .base_repository import BaseRepository
import logging

logger = logging.getLogger(__name__)


class TaskRepository(BaseRepository[Task]):
    """
    Task Repository implementing specific data access operations
    
    This class extends BaseRepository to provide Task-specific
    database operations following the Repository pattern.
    """
    
    def __init__(self, db_session: Session):
        super().__init__(db_session, Task)
    
    def find_by_criteria(self, criteria: Dict[str, Any]) -> List[Task]:
        """Find tasks by multiple criteria"""
        try:
            query = self.db.query(Task).filter(Task.is_deleted != True)
            
            # Apply filters based on criteria
            if 'status' in criteria and criteria['status']:
                query = query.filter(Task.status == criteria['status'])
            
            if 'priority' in criteria and criteria['priority']:
                query = query.filter(Task.priority == criteria['priority'])
            
            if 'assigned_to' in criteria and criteria['assigned_to']:
                query = query.filter(Task.assigned_to == criteria['assigned_to'])
            
            if 'created_by' in criteria and criteria['created_by']:
                query = query.filter(Task.created_by == criteria['created_by'])
            
            return query.all()
        except Exception as e:
            logger.error(f"Error finding tasks by criteria {criteria}: {e}")
            raise
    
    def find_by_status(self, status: TaskStatus) -> List[Task]:
        """Find all tasks with specific status"""
        try:
            return self.db.query(Task).filter(
                and_(Task.status == status, Task.is_deleted != True)
            ).all()
        except Exception as e:
            logger.error(f"Error finding tasks by status {status}: {e}")
            raise
    
    def find_by_user(self, user_id: str, include_created: bool = True, include_assigned: bool = True) -> List[Task]:
        """Find tasks associated with a user (created by or assigned to)"""
        try:
            conditions = []
            
            if include_created:
                conditions.append(Task.created_by == user_id)
            
            if include_assigned:
                conditions.append(Task.assigned_to == user_id)
            
            if not conditions:
                return []
            
            query = self.db.query(Task).filter(
                and_(or_(*conditions), Task.is_deleted != True)
            )
            
            return query.all()
        except Exception as e:
            logger.error(f"Error finding tasks for user {user_id}: {e}")
            raise
    
    def find_overdue_tasks(self) -> List[Task]:
        """Find all overdue tasks"""
        try:
            current_time = datetime.utcnow()
            return self.db.query(Task).filter(
                and_(
                    Task.due_date < current_time,
                    Task.status.in_([TaskStatus.PENDING, TaskStatus.IN_PROGRESS]),
                    Task.is_deleted != True
                )
            ).all()
        except Exception as e:
            logger.error(f"Error finding overdue tasks: {e}")
            raise
    
    def find_high_priority_tasks(self) -> List[Task]:
        """Find all high priority and urgent tasks"""
        try:
            return self.db.query(Task).filter(
                and_(
                    Task.priority.in_([TaskPriority.HIGH, TaskPriority.URGENT]),
                    Task.status != TaskStatus.COMPLETED,
                    Task.is_deleted != True
                )
            ).all()
        except Exception as e:
            logger.error(f"Error finding high priority tasks: {e}")
            raise
    
    def get_paginated(
        self, 
        page: int = 1, 
        size: int = 10, 
        filters: Dict[str, Any] = None,
        sort_by: str = 'created_at',
        sort_order: str = 'desc'
    ) -> Tuple[List[Task], int]:
        """
        Get paginated tasks with filtering and sorting
        Returns (tasks, total_count)
        """
        try:
            # Base query
            query = self.db.query(Task).filter(Task.is_deleted != True)
            
            # Apply filters
            if filters:
                if filters.get('status'):
                    query = query.filter(Task.status == filters['status'])
                
                if filters.get('priority'):
                    query = query.filter(Task.priority == filters['priority'])
                
                if filters.get('assigned_to'):
                    query = query.filter(Task.assigned_to == filters['assigned_to'])
                
                if filters.get('created_by'):
                    query = query.filter(Task.created_by == filters['created_by'])
                
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Task.title.ilike(search_term),
                            Task.description.ilike(search_term)
                        )
                    )
            
            # Get total count before pagination
            total_count = query.count()
            
            # Apply sorting
            if hasattr(Task, sort_by):
                sort_column = getattr(Task, sort_by)
                if sort_order.lower() == 'desc':
                    query = query.order_by(desc(sort_column))
                else:
                    query = query.order_by(asc(sort_column))
            
            # Apply pagination
            offset = (page - 1) * size
            tasks = query.offset(offset).limit(size).all()
            
            return tasks, total_count
            
        except Exception as e:
            logger.error(f"Error getting paginated tasks: {e}")
            raise
    
    def get_task_statistics(self) -> Dict[str, int]:
        """Get task statistics for dashboard"""
        try:
            base_query = self.db.query(Task).filter(Task.is_deleted != True)
            
            stats = {
                'total_tasks': base_query.count(),
                'pending_tasks': base_query.filter(Task.status == TaskStatus.PENDING).count(),
                'in_progress_tasks': base_query.filter(Task.status == TaskStatus.IN_PROGRESS).count(),
                'completed_tasks': base_query.filter(Task.status == TaskStatus.COMPLETED).count(),
                'cancelled_tasks': base_query.filter(Task.status == TaskStatus.CANCELLED).count(),
                'high_priority_tasks': base_query.filter(
                    Task.priority.in_([TaskPriority.HIGH, TaskPriority.URGENT])
                ).count()
            }
            
            # Calculate overdue tasks
            current_time = datetime.utcnow()
            stats['overdue_tasks'] = base_query.filter(
                and_(
                    Task.due_date < current_time,
                    Task.status.in_([TaskStatus.PENDING, TaskStatus.IN_PROGRESS])
                )
            ).count()
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting task statistics: {e}")
            raise
    
    def search_tasks(self, search_term: str, limit: int = 50) -> List[Task]:
        """Search tasks by title and description"""
        try:
            search_pattern = f"%{search_term}%"
            return self.db.query(Task).filter(
                and_(
                    or_(
                        Task.title.ilike(search_pattern),
                        Task.description.ilike(search_pattern)
                    ),
                    Task.is_deleted != True
                )
            ).limit(limit).all()
        except Exception as e:
            logger.error(f"Error searching tasks with term '{search_term}': {e}")
            raise
    
    def bulk_update_status(self, task_ids: List[int], new_status: TaskStatus) -> int:
        """Bulk update status for multiple tasks"""
        try:
            updated_count = self.db.query(Task).filter(
                and_(
                    Task.id.in_(task_ids),
                    Task.is_deleted != True
                )
            ).update(
                {Task.status: new_status},
                synchronize_session=False
            )
            
            self.db.commit()
            logger.info(f"Bulk updated {updated_count} tasks to status {new_status}")
            return updated_count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error bulk updating tasks: {e}")
            raise
