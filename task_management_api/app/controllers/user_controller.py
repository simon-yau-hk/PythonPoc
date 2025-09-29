"""
User Controller - API Layer for User Management
Handles HTTP requests/responses and delegates business logic to UserService
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional, List
import logging

from ..dto.user_dto import (
    CreateUserRequest, UpdateUserRequest, UserQueryParams,
    UserResponse, UserListResponse, UserStatsResponse
)
from ..services.user_service import (
    UserService, UserNotFoundError, UserValidationError, UnauthorizedUserOperationError
)

logger = logging.getLogger(__name__)

# Create router for user endpoints with specific name
router = APIRouter(prefix="/api/v1/users", tags=["users"])

class UserController:
    """
    User Controller implementing RESTful API endpoints
    
    Follows Controller-Service-Repository pattern for user management
    """
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def _get_current_user(self) -> str:
        """
        Get current authenticated user
        In a real application, this would validate JWT tokens, etc.
        """
        # TODO: Implement actual authentication
        return "admin_user"  # Mock admin user for demo

# Register User Management Endpoints
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

# Dependency to get user service
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Get user service with dependencies"""
    repository = UserRepository(db)
    return UserService(repository)

# User Management Endpoints
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account"
)
async def create_user(
    request: CreateUserRequest,
    user_service: UserService = Depends(get_user_service),
    current_user: str = Depends(lambda: "admin_user")  # Mock current user
):
    """Create a new user"""
    try:
        user = user_service.create_user(request, current_user)
        return user
    except UserValidationError as e:
        logger.warning(f"User validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except UnauthorizedUserOperationError as e:
        logger.warning(f"Unauthorized user operation: {e}")
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get users with pagination",
    description="Get a paginated list of users with optional filtering"
)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    role: Optional[str] = Query(None, description="Filter by role"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in username, name, email"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    user_service: UserService = Depends(get_user_service),
    current_user: str = Depends(lambda: "admin_user")
):
    """Get paginated list of users"""
    try:
        query_params = UserQueryParams(
            page=page,
            size=size,
            role=role,
            status=status,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
        users = user_service.get_users_paginated(query_params, current_user)
        return users
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID"
)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: str = Depends(lambda: "admin_user")
):
    """Get a specific user by ID"""
    try:
        user = user_service.get_user_by_id(user_id, current_user)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    except UnauthorizedUserOperationError:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update an existing user"
)
async def update_user(
    user_id: int,
    request: UpdateUserRequest,
    user_service: UserService = Depends(get_user_service),
    current_user: str = Depends(lambda: "admin_user")
):
    """Update an existing user"""
    try:
        user = user_service.update_user(user_id, request, current_user)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    except UnauthorizedUserOperationError:
        raise HTTPException(status_code=403, detail="Not authorized to modify this user")
    except UserValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user (soft delete)"
)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: str = Depends(lambda: "admin_user")
):
    """Delete a user"""
    try:
        success = user_service.delete_user(user_id, current_user)
        if not success:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return None  # 204 No Content
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    except UnauthorizedUserOperationError:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    except UserValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/stats/overview",
    response_model=UserStatsResponse,
    summary="Get user statistics",
    description="Get user statistics overview (admin only)"
)
async def get_user_statistics(
    user_service: UserService = Depends(get_user_service),
    current_user: str = Depends(lambda: "admin_user")
):
    """Get user statistics"""
    try:
        stats = user_service.get_user_statistics(current_user)
        return stats
    except UnauthorizedUserOperationError:
        raise HTTPException(status_code=403, detail="Only admins can view user statistics")
    except Exception as e:
        logger.error(f"Error getting user statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/authenticate",
    response_model=UserResponse,
    summary="Authenticate user",
    description="Authenticate user with username and password"
)
async def authenticate_user(
    username: str = Query(..., description="Username"),
    password: str = Query(..., description="Password"),
    user_service: UserService = Depends(get_user_service)
):
    """Authenticate user credentials"""
    try:
        user = user_service.authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error authenticating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
