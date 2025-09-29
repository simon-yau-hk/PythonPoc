"""
Task DTOs - Data Transfer Objects
Used for API request/response serialization and validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Re-export enums for DTOs
class TaskStatusDTO(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriorityDTO(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# Request DTOs (Input)
class CreateTaskRequest(BaseModel):
    """DTO for creating a new task"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the new API",
                "priority": "high",
                "assigned_to": "john.doe",
                "due_date": "2024-01-15T10:00:00Z"
            }
        }
    )
    
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    priority: TaskPriorityDTO = Field(TaskPriorityDTO.MEDIUM, description="Task priority")
    assigned_to: Optional[str] = Field(None, max_length=100, description="User assigned to the task")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    created_by: str = Field(..., max_length=100, description="User who created the task")


class UpdateTaskRequest(BaseModel):
    """DTO for updating an existing task"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated task title",
                "description": "Updated description",
                "status": "in_progress",
                "priority": "high",
                "assigned_to": "jane.smith"
            }
        }
    )
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatusDTO] = None
    priority: Optional[TaskPriorityDTO] = None
    assigned_to: Optional[str] = Field(None, max_length=100)
    due_date: Optional[datetime] = None


class TaskQueryParams(BaseModel):
    """DTO for task query parameters"""
    status: Optional[TaskStatusDTO] = None
    priority: Optional[TaskPriorityDTO] = None
    assigned_to: Optional[str] = None
    created_by: Optional[str] = None
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Page size")
    sort_by: str = Field("created_at", description="Sort field")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")


# Response DTOs (Output)
class TaskResponse(BaseModel):
    """DTO for task response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: Optional[str]
    status: TaskStatusDTO
    priority: TaskPriorityDTO
    created_by: str
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    is_overdue: bool = False
    
    @classmethod
    def from_domain_model(cls, task) -> 'TaskResponse':
        """Convert domain model to DTO"""
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            status=TaskStatusDTO(task.status.value),
            priority=TaskPriorityDTO(task.priority.value),
            created_by=task.created_by,
            assigned_to=task.assigned_to,
            created_at=task.created_at,
            updated_at=task.updated_at,
            due_date=task.due_date,
            completed_at=task.completed_at,
            is_overdue=task.is_overdue()
        )


class TaskListResponse(BaseModel):
    """DTO for paginated task list response"""
    tasks: List[TaskResponse]
    total: int
    page: int
    size: int
    total_pages: int
    has_next: bool
    has_previous: bool


class TaskStatsResponse(BaseModel):
    """DTO for task statistics"""
    total_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int
    cancelled_tasks: int
    overdue_tasks: int
    high_priority_tasks: int


# Error DTOs
class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    message: str
    details: Optional[dict] = None


class ValidationErrorResponse(BaseModel):
    """Validation error response"""
    error: str = "validation_error"
    message: str
    field_errors: List[dict]
