"""
Task Controller - API Layer for Task Management
Handles HTTP requests/responses and delegates business logic to TaskService
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional, List
import logging

from ..dto.task_dto import (
    CreateTaskRequest, UpdateTaskRequest, TaskQueryParams,
    TaskResponse, TaskListResponse, TaskStatsResponse
)
from ..services.task_service import (
    TaskService, TaskNotFoundError, TaskValidationError, UnauthorizedOperationError
)

logger = logging.getLogger(__name__)

# Create router for task endpoints
router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

# Register Task Management Endpoints
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

# Dependency to get task service
def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Get task service with dependencies"""
    repository = TaskRepository(db)
    return TaskService(repository)

# Task Management Endpoints
@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with the provided details"
)
async def create_task(
    request: CreateTaskRequest,
    task_service: TaskService = Depends(get_task_service),
    current_user: str = Depends(lambda: "demo_user")  # Mock current user
):
    """Create a new task"""
    try:
        request.created_by = current_user
        task = task_service.create_task(request)
        return task
    except TaskValidationError as e:
        logger.warning(f"Task validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Get tasks with pagination",
    description="Get a paginated list of tasks with optional filtering"
)
async def get_tasks(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    assigned_to: Optional[str] = Query(None, description="Filter by assignee"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    task_service: TaskService = Depends(get_task_service),
    current_user: str = Depends(lambda: "demo_user")
):
    """Get paginated list of tasks"""
    try:
        query_params = TaskQueryParams(
            page=page,
            size=size,
            status=status_filter,
            priority=priority,
            assigned_to=assigned_to,
            created_by=created_by,
            sort_by=sort_by,
            sort_order=sort_order
        )
        tasks = task_service.get_tasks_paginated(query_params, current_user)
        return tasks
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    description="Retrieve a specific task by its ID"
)
async def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user: str = Depends(lambda: "demo_user")
):
    """Get a specific task by ID"""
    try:
        task = task_service.get_task_by_id(task_id, current_user)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except UnauthorizedOperationError:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    except Exception as e:
        logger.error(f"Error getting task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
    description="Update an existing task"
)
async def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    task_service: TaskService = Depends(get_task_service),
    current_user: str = Depends(lambda: "demo_user")
):
    """Update an existing task"""
    try:
        task = task_service.update_task(task_id, request, current_user)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except UnauthorizedOperationError:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")
    except TaskValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task (soft delete)"
)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user: str = Depends(lambda: "demo_user")
):
    """Delete a task"""
    try:
        success = task_service.delete_task(task_id, current_user)
        if not success:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        return None  # 204 No Content
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except UnauthorizedOperationError:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    except TaskValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/{task_id}/complete",
    response_model=TaskResponse,
    summary="Complete task",
    description="Mark a task as completed"
)
async def complete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user: str = Depends(lambda: "demo_user")
):
    """Mark a task as completed"""
    try:
        task = task_service.complete_task(task_id, current_user)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except UnauthorizedOperationError:
        raise HTTPException(status_code=403, detail="Not authorized to complete this task")
    except Exception as e:
        logger.error(f"Error completing task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/{task_id}/assign",
    response_model=TaskResponse,
    summary="Assign task",
    description="Assign a task to a user"
)
async def assign_task(
    task_id: int,
    assignee_id: str = Query(..., description="User ID to assign the task to"),
    task_service: TaskService = Depends(get_task_service),
    current_user: str = Depends(lambda: "demo_user")
):
    """Assign a task to a user"""
    try:
        task = task_service.assign_task(task_id, assignee_id, current_user)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except UnauthorizedOperationError:
        raise HTTPException(status_code=403, detail="Not authorized to assign this task")
    except Exception as e:
        logger.error(f"Error assigning task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/stats/overview",
    response_model=TaskStatsResponse,
    summary="Get task statistics",
    description="Get task statistics overview"
)
async def get_task_statistics(
    user_id: Optional[str] = Query(None, description="Get stats for specific user"),
    task_service: TaskService = Depends(get_task_service),
    current_user: str = Depends(lambda: "demo_user")
):
    """Get task statistics"""
    try:
        stats = task_service.get_task_statistics(user_id or current_user)
        return stats
    except Exception as e:
        logger.error(f"Error getting task statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/overdue",
    response_model=List[TaskResponse],
    summary="Get overdue tasks",
    description="Get all overdue tasks"
)
async def get_overdue_tasks(
    user_id: Optional[str] = Query(None, description="Get overdue tasks for specific user"),
    task_service: TaskService = Depends(get_task_service),
    current_user: str = Depends(lambda: "demo_user")
):
    """Get overdue tasks"""
    try:
        tasks = task_service.get_overdue_tasks(user_id or current_user)
        return tasks
    except Exception as e:
        logger.error(f"Error getting overdue tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")