"""
User DTOs - Data Transfer Objects for User API
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Re-export enums for DTOs
class UserRoleDTO(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"

class UserStatusDTO(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

# Request DTOs (Input)
class CreateUserRequest(BaseModel):
    """DTO for creating a new user"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "password": "securepassword123",
                "role": "user"
            }
        }
    )
    
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: str = Field(..., description="User email address")
    full_name: str = Field(..., min_length=1, max_length=200, description="User's full name")
    password: str = Field(..., min_length=6, description="User password")
    role: UserRoleDTO = Field(UserRoleDTO.USER, description="User role")

class UpdateUserRequest(BaseModel):
    """DTO for updating an existing user"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = None
    role: Optional[UserRoleDTO] = None
    status: Optional[UserStatusDTO] = None

class UserQueryParams(BaseModel):
    """DTO for user query parameters"""
    role: Optional[UserRoleDTO] = None
    status: Optional[UserStatusDTO] = None
    search: Optional[str] = None
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Page size")
    sort_by: str = Field("created_at", description="Sort field")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")

# Response DTOs (Output)
class UserResponse(BaseModel):
    """DTO for user response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str
    full_name: str
    role: UserRoleDTO
    status: UserStatusDTO
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    email_verified: bool
    
    @classmethod
    def from_domain_model(cls, user) -> 'UserResponse':
        """Convert domain model to DTO"""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=UserRoleDTO(user.role.value),
            status=UserStatusDTO(user.status.value),
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            email_verified=user.email_verified
        )

class UserListResponse(BaseModel):
    """DTO for paginated user list response"""
    users: List[UserResponse]
    total: int
    page: int
    size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class UserStatsResponse(BaseModel):
    """DTO for user statistics"""
    total_users: int
    active_users: int
    inactive_users: int
    admin_users: int
    manager_users: int
    regular_users: int
