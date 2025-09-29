# models/user_response_dto.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class UserRoleDto(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    USER = "USER"
    GUEST = "GUEST"

class UserStatusDto(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class TaskStatusDto(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class TaskPriorityDto(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class TaskDetailTypeDto(str, Enum):
    COMMENT = "COMMENT"
    ATTACHMENT = "ATTACHMENT"
    LOG = "LOG"
    NOTE = "NOTE"
    CHECKLIST_ITEM = "CHECKLIST_ITEM"

class TaskDetailDto(BaseModel):
    id: int
    detail_type: TaskDetailTypeDto
    title: Optional[str] = None
    content: Optional[str] = None
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    is_completed: Optional[bool] = None
    order_index: Optional[int] = None

class TaskDto(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatusDto
    priority: TaskPriorityDto
    created_by: str
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    task_details: List[TaskDetailDto] = []

class UserDto(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    role: UserRoleDto
    status: UserStatusDto
    email_verified: bool

class UserWithTasksDto(BaseModel):
    user: UserDto
    tasks: List[TaskDto] = []
    total_tasks: int

class UserListDto(BaseModel):
    users: List[UserDto]
    total: int