"""
Task Service - Business Logic Layer
Contains all business rules and orchestrates operations between controllers and repositories
"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timedelta
import logging

from ..models.task import Task, TaskStatus, TaskPriority
from ..repositories.task_repository import TaskRepository
from ..dto.task_dto import (
    CreateTaskRequest, UpdateTaskRequest, TaskQueryParams,
    TaskResponse, TaskListResponse, TaskStatsResponse
)

logger = logging.getLogger(__name__)


class TaskNotFoundError(Exception):
    """Raised when a task is not found"""
    pass


class TaskValidationError(Exception):
    """Raised when task validation fails"""
    pass


class UnauthorizedOperationError(Exception):
    """Raised when user is not authorized to perform operation"""
    pass


class TaskService:
    """
    Task Service implementing business logic
    
    This layer contains all business rules, validation, and orchestration logic.
    It acts as the intermediary between controllers and repositories.
    """
    
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def create_task(self, request: CreateTaskRequest) -> TaskResponse:
        """
        Create a new task with business validation
        
        Business Rules:
        - Title must be unique for the user
        - Due date cannot be in the past
        - High/Urgent priority tasks must have due date
        """
        try:
            # Business validation
            self._validate_create_request(request)
            
            # Create domain entity
            task = Task(
                title=request.title,
                description=request.description,
                priority=TaskPriority(request.priority.value),
                created_by=request.created_by,
                assigned_to=request.assigned_to,
                due_date=request.due_date,
                status=TaskStatus.PENDING
            )
            
            # Auto-assign if assigned to someone
            if request.assigned_to:
                task.assign_to_user(request.assigned_to)
            
            # Save to repository
            created_task = self.task_repository.create(task)
            
            logger.info(f"Task created successfully: {created_task.id}")
            return TaskResponse.from_domain_model(created_task)
            
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise
    
    def get_task_by_id(self, task_id: int, requesting_user: str) -> TaskResponse:
        """Get task by ID with authorization check"""
        try:
            task = self.task_repository.get_by_id(task_id)
            
            if not task:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            
            # Authorization check
            if not self._can_user_access_task(task, requesting_user):
                raise UnauthorizedOperationError("User not authorized to access this task")
            
            return TaskResponse.from_domain_model(task)
            
        except (TaskNotFoundError, UnauthorizedOperationError):
            raise
        except Exception as e:
            logger.error(f"Error getting task {task_id}: {e}")
            raise
    
    def update_task(self, task_id: int, request: UpdateTaskRequest, requesting_user: str) -> TaskResponse:
        """
        Update task with business validation
        
        Business Rules:
        - Only task creator or assignee can update
        - Completed/Cancelled tasks cannot be edited
        - Status transitions must be valid
        """
        try:
            task = self.task_repository.get_by_id(task_id)
            
            if not task:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            
            # Authorization check
            if not self._can_user_modify_task(task, requesting_user):
                raise UnauthorizedOperationError("User not authorized to modify this task")
            
            # Business validation
            if not task.can_be_edited():
                raise TaskValidationError("Cannot edit completed or cancelled tasks")
            
            # Apply updates with validation
            self._apply_task_updates(task, request)
            
            # Save changes
            updated_task = self.task_repository.update(task)
            
            logger.info(f"Task updated successfully: {task_id}")
            return TaskResponse.from_domain_model(updated_task)
            
        except (TaskNotFoundError, UnauthorizedOperationError, TaskValidationError):
            raise
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {e}")
            raise
    
    def delete_task(self, task_id: int, requesting_user: str) -> bool:
        """
        Soft delete task
        
        Business Rules:
        - Only task creator can delete
        - Cannot delete completed tasks (for audit purposes)
        """
        try:
            task = self.task_repository.get_by_id(task_id)
            
            if not task:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            
            # Authorization check - only creator can delete
            if task.created_by != requesting_user:
                raise UnauthorizedOperationError("Only task creator can delete tasks")
            
            # Business rule - cannot delete completed tasks
            if task.status == TaskStatus.COMPLETED:
                raise TaskValidationError("Cannot delete completed tasks")
            
            success = self.task_repository.delete(task_id)
            
            if success:
                logger.info(f"Task deleted successfully: {task_id}")
            
            return success
            
        except (TaskNotFoundError, UnauthorizedOperationError, TaskValidationError):
            raise
        except Exception as e:
            logger.error(f"Error deleting task {task_id}: {e}")
            raise
    
    def get_tasks_paginated(self, query_params: TaskQueryParams, requesting_user: str) -> TaskListResponse:
        """Get paginated list of tasks with filtering"""
        try:
            # Build filters
            filters = self._build_filters_from_query(query_params, requesting_user)
            
            # Get paginated results
            tasks, total_count = self.task_repository.get_paginated(
                page=query_params.page,
                size=query_params.size,
                filters=filters,
                sort_by=query_params.sort_by,
                sort_order=query_params.sort_order
            )
            
            # Convert to DTOs
            task_responses = [TaskResponse.from_domain_model(task) for task in tasks]
            
            # Calculate pagination metadata
            total_pages = (total_count + query_params.size - 1) // query_params.size
            
            return TaskListResponse(
                tasks=task_responses,
                total=total_count,
                page=query_params.page,
                size=query_params.size,
                total_pages=total_pages,
                has_next=query_params.page < total_pages,
                has_previous=query_params.page > 1
            )
            
        except Exception as e:
            logger.error(f"Error getting paginated tasks: {e}")
            raise
    
    def get_user_tasks(self, user_id: str, include_created: bool = True, include_assigned: bool = True) -> List[TaskResponse]:
        """Get all tasks for a specific user"""
        try:
            tasks = self.task_repository.find_by_user(user_id, include_created, include_assigned)
            return [TaskResponse.from_domain_model(task) for task in tasks]
        except Exception as e:
            logger.error(f"Error getting tasks for user {user_id}: {e}")
            raise
    
    def get_task_statistics(self, user_id: Optional[str] = None) -> TaskStatsResponse:
        """Get task statistics (global or for specific user)"""
        try:
            if user_id:
                # Get user-specific stats
                user_tasks = self.task_repository.find_by_user(user_id)
                stats = self._calculate_user_stats(user_tasks)
            else:
                # Get global stats
                stats = self.task_repository.get_task_statistics()
            
            return TaskStatsResponse(**stats)
            
        except Exception as e:
            logger.error(f"Error getting task statistics: {e}")
            raise
    
    def complete_task(self, task_id: int, requesting_user: str) -> TaskResponse:
        """Mark task as completed"""
        try:
            task = self.task_repository.get_by_id(task_id)
            
            if not task:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            
            # Authorization check
            if not self._can_user_modify_task(task, requesting_user):
                raise UnauthorizedOperationError("User not authorized to complete this task")
            
            # Business logic
            task.mark_as_completed()
            
            updated_task = self.task_repository.update(task)
            logger.info(f"Task completed: {task_id}")
            
            return TaskResponse.from_domain_model(updated_task)
            
        except (TaskNotFoundError, UnauthorizedOperationError):
            raise
        except Exception as e:
            logger.error(f"Error completing task {task_id}: {e}")
            raise
    
    def assign_task(self, task_id: int, assignee_id: str, requesting_user: str) -> TaskResponse:
        """Assign task to a user"""
        try:
            task = self.task_repository.get_by_id(task_id)
            
            if not task:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            
            # Authorization check - only creator can assign
            if task.created_by != requesting_user:
                raise UnauthorizedOperationError("Only task creator can assign tasks")
            
            # Business logic
            task.assign_to_user(assignee_id)
            
            updated_task = self.task_repository.update(task)
            logger.info(f"Task {task_id} assigned to {assignee_id}")
            
            return TaskResponse.from_domain_model(updated_task)
            
        except (TaskNotFoundError, UnauthorizedOperationError):
            raise
        except Exception as e:
            logger.error(f"Error assigning task {task_id}: {e}")
            raise
    
    def get_overdue_tasks(self, user_id: Optional[str] = None) -> List[TaskResponse]:
        """Get overdue tasks (global or for specific user)"""
        try:
            if user_id:
                user_tasks = self.task_repository.find_by_user(user_id)
                overdue_tasks = [task for task in user_tasks if task.is_overdue()]
            else:
                overdue_tasks = self.task_repository.find_overdue_tasks()
            
            return [TaskResponse.from_domain_model(task) for task in overdue_tasks]
            
        except Exception as e:
            logger.error(f"Error getting overdue tasks: {e}")
            raise
    
    # Private helper methods
    def _validate_create_request(self, request: CreateTaskRequest) -> None:
        """Validate task creation request"""
        # Check due date is not in the past
        if request.due_date and request.due_date < datetime.utcnow():
            raise TaskValidationError("Due date cannot be in the past")
        
        # High/Urgent priority tasks must have due date
        if request.priority in [TaskPriority.HIGH, TaskPriority.URGENT] and not request.due_date:
            raise TaskValidationError("High and urgent priority tasks must have a due date")
        
        # Check for duplicate titles for the same user (business rule)
        existing_tasks = self.task_repository.find_by_criteria({
            'created_by': request.created_by
        })
        
        if any(task.title.lower() == request.title.lower() for task in existing_tasks):
            raise TaskValidationError(f"Task with title '{request.title}' already exists for this user")
    
    def _can_user_access_task(self, task: Task, user_id: str) -> bool:
        """Check if user can access task"""
        return task.created_by == user_id or task.assigned_to == user_id
    
    def _can_user_modify_task(self, task: Task, user_id: str) -> bool:
        """Check if user can modify task"""
        return task.created_by == user_id or task.assigned_to == user_id
    
    def _apply_task_updates(self, task: Task, request: UpdateTaskRequest) -> None:
        """Apply updates to task with validation"""
        if request.title is not None:
            task.title = request.title
        
        if request.description is not None:
            task.description = request.description
        
        if request.priority is not None:
            task.priority = TaskPriority(request.priority.value)
        
        if request.assigned_to is not None:
            task.assign_to_user(request.assigned_to)
        
        if request.due_date is not None:
            if request.due_date < datetime.utcnow():
                raise TaskValidationError("Due date cannot be in the past")
            task.due_date = request.due_date
        
        if request.status is not None:
            # Validate status transition
            self._validate_status_transition(task.status, TaskStatus(request.status.value))
            task.status = TaskStatus(request.status.value)
            
            if request.status.value == TaskStatus.COMPLETED.value:
                task.mark_as_completed()
    
    def _validate_status_transition(self, current_status: TaskStatus, new_status: TaskStatus) -> None:
        """Validate status transitions according to business rules"""
        valid_transitions = {
            TaskStatus.PENDING: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED],
            TaskStatus.IN_PROGRESS: [TaskStatus.COMPLETED, TaskStatus.PENDING, TaskStatus.CANCELLED],
            TaskStatus.COMPLETED: [],  # Cannot transition from completed
            TaskStatus.CANCELLED: [TaskStatus.PENDING]  # Can reopen cancelled tasks
        }
        
        if new_status not in valid_transitions[current_status]:
            raise TaskValidationError(
                f"Invalid status transition from {current_status.value} to {new_status.value}"
            )
    
    def _build_filters_from_query(self, query_params: TaskQueryParams, requesting_user: str) -> Dict[str, Any]:
        """Build filters dictionary from query parameters"""
        filters = {}
        
        if query_params.status:
            filters['status'] = TaskStatus(query_params.status.value)
        
        if query_params.priority:
            filters['priority'] = TaskPriority(query_params.priority.value)
        
        if query_params.assigned_to:
            filters['assigned_to'] = query_params.assigned_to
        
        if query_params.created_by:
            filters['created_by'] = query_params.created_by
        else:
            # Default: only show tasks user has access to
            filters['user_access'] = requesting_user
        
        return filters
    
    def _calculate_user_stats(self, tasks: List[Task]) -> Dict[str, int]:
        """Calculate statistics for a list of tasks"""
        stats = {
            'total_tasks': len(tasks),
            'pending_tasks': sum(1 for t in tasks if t.status == TaskStatus.PENDING),
            'in_progress_tasks': sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS),
            'completed_tasks': sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
            'cancelled_tasks': sum(1 for t in tasks if t.status == TaskStatus.CANCELLED),
            'overdue_tasks': sum(1 for t in tasks if t.is_overdue()),
            'high_priority_tasks': sum(1 for t in tasks if t.priority in [TaskPriority.HIGH, TaskPriority.URGENT])
        }
        
        return stats
