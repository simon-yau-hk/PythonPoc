"""
User Service - Business Logic Layer for Users
Contains all user-related business rules and operations
"""

from typing import List, Optional, Dict, Any
import hashlib
import logging

from ..models.user import User, UserRole, UserStatus
from ..repositories.user_repository import UserRepository
from ..dto.user_dto import (
    CreateUserRequest, UpdateUserRequest, UserQueryParams,
    UserResponse, UserListResponse, UserStatsResponse
)

logger = logging.getLogger(__name__)

class UserNotFoundError(Exception):
    """Raised when a user is not found"""
    pass

class UserValidationError(Exception):
    """Raised when user validation fails"""
    pass

class UnauthorizedUserOperationError(Exception):
    """Raised when user operation is not authorized"""
    pass

class UserService:
    """
    User Service implementing business logic for user management
    
    This layer contains all business rules, validation, and orchestration logic.
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def create_user(self, request: CreateUserRequest, requesting_user: str = None) -> UserResponse:
        """
        Create a new user with business validation
        
        Business Rules:
        - Username must be unique
        - Email must be unique
        - Password must be hashed
        - Only admins can create admin users
        """
        try:
            # Business validation
            self._validate_create_request(request, requesting_user)
            
            # Hash password (simplified - use proper hashing in production!)
            password_hash = self._hash_password(request.password)
            
            # Create domain entity
            user = User(
                username=request.username,
                email=request.email,
                full_name=request.full_name,
                password_hash=password_hash,
                role=UserRole(request.role.value),
                status=UserStatus.ACTIVE
            )
            
            # Save to repository
            created_user = self.user_repository.create(user)
            
            logger.info(f"User created successfully: {created_user.username}")
            return UserResponse.from_domain_model(created_user)
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def get_user_by_id(self, user_id: int, requesting_user: str) -> UserResponse:
        """Get user by ID with authorization check"""
        try:
            user = self.user_repository.get_by_id(user_id)
            
            if not user:
                raise UserNotFoundError(f"User with ID {user_id} not found")
            
            # Authorization check (users can see their own profile, admins can see all)
            if not self._can_user_access_profile(user, requesting_user):
                raise UnauthorizedUserOperationError("Not authorized to access this user profile")
            
            return UserResponse.from_domain_model(user)
            
        except (UserNotFoundError, UnauthorizedUserOperationError):
            raise
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise
    
    def update_user(self, user_id: int, request: UpdateUserRequest, requesting_user: str) -> UserResponse:
        """
        Update user with business validation
        
        Business Rules:
        - Users can only update their own profile
        - Admins can update any user
        - Role changes require admin privileges
        """
        try:
            user = self.user_repository.get_by_id(user_id)
            
            if not user:
                raise UserNotFoundError(f"User with ID {user_id} not found")
            
            # Authorization check
            if not self._can_user_modify_profile(user, requesting_user, request):
                raise UnauthorizedUserOperationError("Not authorized to modify this user")
            
            # Apply updates with validation
            self._apply_user_updates(user, request, requesting_user)
            
            # Save changes
            updated_user = self.user_repository.update(user)
            
            logger.info(f"User updated successfully: {user_id}")
            return UserResponse.from_domain_model(updated_user)
            
        except (UserNotFoundError, UnauthorizedUserOperationError, UserValidationError):
            raise
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            raise
    
    def delete_user(self, user_id: int, requesting_user: str) -> bool:
        """
        Soft delete user
        
        Business Rules:
        - Only admins can delete users
        - Cannot delete yourself
        - Cannot delete other admins unless super admin
        """
        try:
            user = self.user_repository.get_by_id(user_id)
            
            if not user:
                raise UserNotFoundError(f"User with ID {user_id} not found")
            
            # Authorization check - only admins can delete
            requesting_user_obj = self.user_repository.find_by_username(requesting_user)
            if not requesting_user_obj or not requesting_user_obj.is_admin():
                raise UnauthorizedUserOperationError("Only admins can delete users")
            
            # Business rule - cannot delete yourself
            if user.username == requesting_user:
                raise UserValidationError("Cannot delete your own account")
            
            # Business rule - cannot delete other admins
            if user.is_admin():
                raise UserValidationError("Cannot delete admin users")
            
            success = self.user_repository.delete(user_id)
            
            if success:
                logger.info(f"User deleted successfully: {user_id}")
            
            return success
            
        except (UserNotFoundError, UnauthorizedUserOperationError, UserValidationError):
            raise
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            raise
    
    def get_users_paginated(self, query_params: UserQueryParams, requesting_user: str) -> UserListResponse:
        """Get paginated list of users with filtering"""
        try:
            # Build filters
            filters = self._build_filters_from_query(query_params)
            
            # Get paginated results
            users, total_count = self.user_repository.get_paginated(
                page=query_params.page,
                size=query_params.size,
                filters=filters,
                sort_by=query_params.sort_by,
                sort_order=query_params.sort_order
            )
            
            # Convert to DTOs
            user_responses = [UserResponse.from_domain_model(user) for user in users]
            
            # Calculate pagination metadata
            total_pages = (total_count + query_params.size - 1) // query_params.size
            
            return UserListResponse(
                users=user_responses,
                total=total_count,
                page=query_params.page,
                size=query_params.size,
                total_pages=total_pages,
                has_next=query_params.page < total_pages,
                has_previous=query_params.page > 1
            )
            
        except Exception as e:
            logger.error(f"Error getting paginated users: {e}")
            raise
    
    def get_user_statistics(self, requesting_user: str) -> UserStatsResponse:
        """Get user statistics (admin only)"""
        try:
            # Authorization check - only admins can view stats
            requesting_user_obj = self.user_repository.find_by_username(requesting_user)
            if not requesting_user_obj or not requesting_user_obj.is_admin():
                raise UnauthorizedUserOperationError("Only admins can view user statistics")
            
            stats = self.user_repository.get_user_statistics()
            return UserStatsResponse(**stats)
            
        except UnauthorizedUserOperationError:
            raise
        except Exception as e:
            logger.error(f"Error getting user statistics: {e}")
            raise
    
    def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        """Authenticate user credentials"""
        try:
            user = self.user_repository.find_by_username(username)
            
            if not user or not user.is_active_user():
                return None
            
            # Verify password (simplified)
            if self._verify_password(password, user.password_hash):
                user.update_last_login()
                self.user_repository.update(user)
                return UserResponse.from_domain_model(user)
            
            return None
            
        except Exception as e:
            logger.error(f"Error authenticating user {username}: {e}")
            raise
    
    # Private helper methods
    def _validate_create_request(self, request: CreateUserRequest, requesting_user: str = None) -> None:
        """Validate user creation request"""
        # Check username uniqueness
        if self.user_repository.find_by_username(request.username):
            raise UserValidationError(f"Username '{request.username}' already exists")
        
        # Check email uniqueness
        if self.user_repository.find_by_email(request.email):
            raise UserValidationError(f"Email '{request.email}' already exists")
        
        # Only admins can create admin users
        if request.role == UserRole.ADMIN and requesting_user:
            requesting_user_obj = self.user_repository.find_by_username(requesting_user)
            if not requesting_user_obj or not requesting_user_obj.is_admin():
                raise UnauthorizedUserOperationError("Only admins can create admin users")
    
    def _can_user_access_profile(self, user: User, requesting_user: str) -> bool:
        """Check if user can access profile"""
        # Users can see their own profile
        if user.username == requesting_user:
            return True
        
        # Admins can see all profiles
        requesting_user_obj = self.user_repository.find_by_username(requesting_user)
        return requesting_user_obj and requesting_user_obj.is_admin()
    
    def _can_user_modify_profile(self, user: User, requesting_user: str, request: UpdateUserRequest) -> bool:
        """Check if user can modify profile"""
        requesting_user_obj = self.user_repository.find_by_username(requesting_user)
        
        # Users can modify their own profile (except role)
        if user.username == requesting_user:
            if request.role is not None:  # Role change requires admin
                return requesting_user_obj and requesting_user_obj.is_admin()
            return True
        
        # Admins can modify any profile
        return requesting_user_obj and requesting_user_obj.is_admin()
    
    def _apply_user_updates(self, user: User, request: UpdateUserRequest, requesting_user: str) -> None:
        """Apply updates to user with validation"""
        if request.full_name is not None:
            user.full_name = request.full_name
        
        if request.email is not None:
            # Check email uniqueness
            existing_user = self.user_repository.find_by_email(request.email)
            if existing_user and existing_user.id != user.id:
                raise UserValidationError(f"Email '{request.email}' already exists")
            user.email = request.email
        
        if request.role is not None:
            user.role = UserRole(request.role.value)
        
        if request.status is not None:
            user.status = UserStatus(request.status.value)
    
    def _build_filters_from_query(self, query_params: UserQueryParams) -> Dict[str, Any]:
        """Build filters dictionary from query parameters"""
        filters = {}
        
        if query_params.role:
            filters['role'] = UserRole(query_params.role.value)
        
        if query_params.status:
            filters['status'] = UserStatus(query_params.status.value)
        
        if query_params.search:
            filters['search'] = query_params.search
        
        return filters
    
    def _hash_password(self, password: str) -> str:
        """Hash password (simplified - use bcrypt in production!)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == password_hash
