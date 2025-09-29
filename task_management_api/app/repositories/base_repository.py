"""
Base Repository - Abstract base for all repositories
Implements common database operations using Repository pattern
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

T = TypeVar('T')

logger = logging.getLogger(__name__)


class BaseRepository(Generic[T], ABC):
    """
    Abstract base repository implementing common CRUD operations
    
    This follows the Repository pattern to abstract data access logic
    and provide a consistent interface for all entities.
    """
    
    def __init__(self, db_session: Session, model_class: type):
        self.db = db_session
        self.model_class = model_class
    
    def create(self, entity: T) -> T:
        """Create a new entity"""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            logger.info(f"Created {self.model_class.__name__} with id: {entity.id}")
            return entity
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error creating {self.model_class.__name__}: {e}")
            raise
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID"""
        try:
            entity = self.db.query(self.model_class).filter(
                self.model_class.id == entity_id,
                getattr(self.model_class, 'is_deleted', True) != True  # Soft delete check
            ).first()
            return entity
        except SQLAlchemyError as e:
            logger.error(f"Error fetching {self.model_class.__name__} by id {entity_id}: {e}")
            raise
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination"""
        try:
            query = self.db.query(self.model_class)
            
            # Apply soft delete filter if model supports it
            if hasattr(self.model_class, 'is_deleted'):
                query = query.filter(self.model_class.is_deleted != True)
            
            entities = query.offset(skip).limit(limit).all()
            return entities
        except SQLAlchemyError as e:
            logger.error(f"Error fetching {self.model_class.__name__} list: {e}")
            raise
    
    def update(self, entity: T) -> T:
        """Update an existing entity"""
        try:
            self.db.commit()
            self.db.refresh(entity)
            logger.info(f"Updated {self.model_class.__name__} with id: {entity.id}")
            return entity
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error updating {self.model_class.__name__}: {e}")
            raise
    
    def delete(self, entity_id: int) -> bool:
        """Delete entity (soft delete if supported, otherwise hard delete)"""
        try:
            entity = self.get_by_id(entity_id)
            if not entity:
                return False
            
            # Soft delete if supported
            if hasattr(entity, 'is_deleted'):
                entity.is_deleted = True
                self.db.commit()
                logger.info(f"Soft deleted {self.model_class.__name__} with id: {entity_id}")
            else:
                # Hard delete
                self.db.delete(entity)
                self.db.commit()
                logger.info(f"Hard deleted {self.model_class.__name__} with id: {entity_id}")
            
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error deleting {self.model_class.__name__} with id {entity_id}: {e}")
            raise
    
    def count(self, filters: Dict[str, Any] = None) -> int:
        """Count entities with optional filters"""
        try:
            query = self.db.query(self.model_class)
            
            # Apply soft delete filter
            if hasattr(self.model_class, 'is_deleted'):
                query = query.filter(self.model_class.is_deleted != True)
            
            # Apply additional filters
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model_class, field):
                        query = query.filter(getattr(self.model_class, field) == value)
            
            return query.count()
        except SQLAlchemyError as e:
            logger.error(f"Error counting {self.model_class.__name__}: {e}")
            raise
    
    def exists(self, entity_id: int) -> bool:
        """Check if entity exists"""
        try:
            return self.db.query(self.model_class).filter(
                self.model_class.id == entity_id
            ).first() is not None
        except SQLAlchemyError as e:
            logger.error(f"Error checking existence of {self.model_class.__name__} with id {entity_id}: {e}")
            raise
    
    @abstractmethod
    def find_by_criteria(self, criteria: Dict[str, Any]) -> List[T]:
        """Find entities by specific criteria - to be implemented by subclasses"""
        pass
