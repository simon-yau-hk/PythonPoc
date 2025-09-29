#!/usr/bin/env python3
"""
Main Application Entry Point
Demonstrates Controller-Service-Repository pattern with dependency injection
"""

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends
from typing import Protocol, Optional, List, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
import asyncio
import logging
from enum import Enum

# ============================================================================
# 1. TYPE SAFETY (Python 3.5+)
# ============================================================================

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

@dataclass
class User:
    """Type-safe user model with validation"""
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool = True
    
    def __post_init__(self):
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")

# ============================================================================
# 2. DEPENDENCY INJECTION & INTERFACES
# ============================================================================

class DatabaseProtocol(Protocol):
    """Interface for database operations"""
    async def get_user(self, user_id: int) -> Optional[User]: ...
    async def save_user(self, user: User) -> bool: ...

class CacheProtocol(Protocol):
    """Interface for caching operations"""
    async def get(self, key: str) -> Optional[Any]: ...
    async def set(self, key: str, value: Any, ttl: int = 300) -> None: ...

# ============================================================================
# 3. CLEAN ARCHITECTURE LAYERS
# ============================================================================

class UserRepository:
    """Data access layer"""
    
    def __init__(self, db: DatabaseProtocol, cache: CacheProtocol):
        self.db = db
        self.cache = cache
    
    async def get_user_with_cache(self, user_id: int) -> Optional[User]:
        # Try cache first
        cache_key = f"user:{user_id}"
        cached_user = await self.cache.get(cache_key)
        
        if cached_user:
            return cached_user
        
        # Fallback to database
        user = await self.db.get_user(user_id)
        if user:
            await self.cache.set(cache_key, user)
        
        return user

class UserService:
    """Business logic layer"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.logger = logging.getLogger(__name__)
    
    async def authenticate_user(self, user_id: int, required_role: UserRole) -> bool:
        """Complex business logic with proper error handling"""
        try:
            user = await self.repository.get_user_with_cache(user_id)
            
            if not user:
                self.logger.warning(f"User {user_id} not found")
                return False
            
            if not user.is_active:
                self.logger.warning(f"User {user_id} is inactive")
                return False
            
            # Role-based authorization
            role_hierarchy = {
                UserRole.GUEST: 0,
                UserRole.USER: 1,
                UserRole.ADMIN: 2
            }
            
            return role_hierarchy[user.role] >= role_hierarchy[required_role]
            
        except Exception as e:
            self.logger.error(f"Authentication error for user {user_id}: {e}")
            return False

# ============================================================================
# 4. ASYNC/CONCURRENT PROCESSING
# ============================================================================

class BatchProcessor:
    """Handle high-throughput operations"""
    
    def __init__(self, user_service: UserService, max_concurrent: int = 10):
        self.user_service = user_service
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_user_batch(self, user_ids: List[int]) -> Dict[int, bool]:
        """Process multiple users concurrently"""
        
        async def process_single_user(user_id: int) -> tuple[int, bool]:
            async with self.semaphore:  # Limit concurrency
                result = await self.user_service.authenticate_user(
                    user_id, UserRole.USER
                )
                return user_id, result
        
        # Process all users concurrently
        tasks = [process_single_user(uid) for uid in user_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle results and exceptions
        processed_results = {}
        for result in results:
            if isinstance(result, Exception):
                logging.error(f"Batch processing error: {result}")
                continue
            
            user_id, auth_result = result
            processed_results[user_id] = auth_result
        
        return processed_results

# ============================================================================
# 5. CONFIGURATION & ENVIRONMENT MANAGEMENT
# ============================================================================

@dataclass
class AppConfig:
    """Type-safe configuration"""
    database_url: str
    redis_url: str
    log_level: str = "INFO"
    max_connections: int = 100
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        import os
        return cls(
            database_url=os.getenv('DATABASE_URL', 'sqlite:///app.db'),
            redis_url=os.getenv('REDIS_URL', 'redis://localhost:6379'),
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            max_connections=int(os.getenv('MAX_CONNECTIONS', '100'))
        )

# ============================================================================
# 6. APPLICATION FACTORY PATTERN
# ============================================================================

class Application:
    """Main application with dependency injection"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self._setup_logging()
        
        # Dependency injection container
        self.db = self._create_database()
        self.cache = self._create_cache()
        self.repository = UserRepository(self.db, self.cache)
        self.user_service = UserService(self.repository)
        self.batch_processor = BatchProcessor(self.user_service)
    
    def _setup_logging(self):
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _create_database(self) -> DatabaseProtocol:
        # Factory pattern for database creation
        if self.config.database_url.startswith('postgresql'):
            from .adapters.postgres import PostgresDatabase
            return PostgresDatabase(self.config.database_url)
        else:
            from .adapters.sqlite import SQLiteDatabase
            return SQLiteDatabase(self.config.database_url)
    
    def _create_cache(self) -> CacheProtocol:
        if self.config.redis_url:
            from .adapters.redis import RedisCache
            return RedisCache(self.config.redis_url)
        else:
            from .adapters.memory import MemoryCache
            return MemoryCache()

# ============================================================================
# 7. TESTING SUPPORT
# ============================================================================

class MockDatabase:
    """Test double for database"""
    
    def __init__(self):
        self.users: Dict[int, User] = {}
    
    async def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)
    
    async def save_user(self, user: User) -> bool:
        self.users[user.id] = user
        return True

# ============================================================================
# 8. MAIN APPLICATION ENTRY POINT
# ============================================================================

async def main():
    """Application entry point with proper resource management"""
    
    config = AppConfig.from_env()
    app = Application(config)
    
    # Example usage
    test_user = User(
        id=1,
        username="john_doe",
        email="john@example.com",
        role=UserRole.USER
    )
    
    # Simulate complex operations
    user_ids = list(range(1, 101))  # 100 users
    results = await app.batch_processor.process_user_batch(user_ids)
    
    print(f"Processed {len(results)} users successfully")
    print(f"Authentication success rate: {sum(results.values()) / len(results) * 100:.1f}%")

if __name__ == "__main__":
    # Proper async application startup
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application stopped by user")
    except Exception as e:
        logging.error(f"Application error: {e}")
        raise
