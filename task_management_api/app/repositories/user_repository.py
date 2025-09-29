"""
User Repository - Data Access Layer for Users
"""

from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func

from ..models.user import User, UserRole, UserStatus
from .base_repository import BaseRepository
import logging

logger = logging.getLogger(__name__)

class UserRepository(BaseRepository[User]):
    """User Repository implementing specific data access operations"""
    
    def __init__(self, db_session: Session):
        super().__init__(db_session, User)
    
    def find_by_criteria(self, criteria: Dict[str, Any]) -> List[User]:
        """Find users by multiple criteria"""
        try:
            query = self.db.query(User).filter(User.is_deleted != True)
            
            if 'role' in criteria and criteria['role']:
                query = query.filter(User.role == criteria['role'])
            
            if 'status' in criteria and criteria['status']:
                query = query.filter(User.status == criteria['status'])
            
            if 'search' in criteria and criteria['search']:
                search_term = f"%{criteria['search']}%"
                query = query.filter(
                    or_(
                        User.username.ilike(search_term),
                        User.full_name.ilike(search_term),
                        User.email.ilike(search_term)
                    )
                )
            
            return query.all()
        except Exception as e:
            logger.error(f"Error finding users by criteria {criteria}: {e}")
            raise
    
    def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        try:
            return self.db.query(User).filter(
                and_(User.username == username, User.is_deleted != True)
            ).first()
        except Exception as e:
            logger.error(f"Error finding user by username {username}: {e}")
            raise
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        try:
            return self.db.query(User).filter(
                and_(User.email == email, User.is_deleted != True)
            ).first()
        except Exception as e:
            logger.error(f"Error finding user by email {email}: {e}")
            raise
    
    def get_paginated(
        self, 
        page: int = 1, 
        size: int = 10, 
        filters: Dict[str, Any] = None,
        sort_by: str = 'created_at',
        sort_order: str = 'desc'
    ) -> Tuple[List[User], int]:
        """Get paginated users with filtering and sorting"""
        try:
            query = self.db.query(User).filter(User.is_deleted != True)
            
            # Apply filters
            if filters:
                if filters.get('role'):
                    query = query.filter(User.role == filters['role'])
                
                if filters.get('status'):
                    query = query.filter(User.status == filters['status'])
                
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            User.username.ilike(search_term),
                            User.full_name.ilike(search_term),
                            User.email.ilike(search_term)
                        )
                    )
            
            total_count = query.count()
            
            # Apply sorting
            if hasattr(User, sort_by):
                sort_column = getattr(User, sort_by)
                if sort_order.lower() == 'desc':
                    query = query.order_by(desc(sort_column))
                else:
                    query = query.order_by(asc(sort_column))
            
            # Apply pagination
            offset = (page - 1) * size
            users = query.offset(offset).limit(size).all()
            
            return users, total_count
            
        except Exception as e:
            logger.error(f"Error getting paginated users: {e}")
            raise
    
    def get_user_statistics(self) -> Dict[str, int]:
        """Get user statistics"""
        try:
            base_query = self.db.query(User).filter(User.is_deleted != True)
            
            stats = {
                'total_users': base_query.count(),
                'active_users': base_query.filter(User.status == UserStatus.ACTIVE).count(),
                'inactive_users': base_query.filter(User.status == UserStatus.INACTIVE).count(),
                'admin_users': base_query.filter(User.role == UserRole.ADMIN).count(),
                'manager_users': base_query.filter(User.role == UserRole.MANAGER).count(),
                'regular_users': base_query.filter(User.role == UserRole.USER).count(),
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user statistics: {e}")
            raise
