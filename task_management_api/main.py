"""
Main Application Entry Point
Demonstrates Controller-Service-Repository pattern with dependency injection
"""
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
import uvicorn

# Import application components
from app.database import get_db, create_tables
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.controllers.task_controller import router as task_router
from app.controllers.user_controller import router as user_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class TaskManagementAPI:
    """
    Main application class implementing dependency injection
    and Controller-Service-Repository pattern
    """
    
    def __init__(self):
        self.app = FastAPI(
            title="Task Management API",
            description="A comprehensive task management system demonstrating Controller-Service-Repository pattern",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        self._setup_middleware()
        self._setup_database()
        self._setup_dependencies()
        self._setup_routes()
    
    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_database(self):
        """Initialize database"""
        create_tables()
        logger.info("Database tables created successfully")
    
    def _setup_dependencies(self):
        """Setup dependency injection"""
        
        def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
            """Factory function for TaskRepository"""
            return TaskRepository(db)
        
        def get_task_service(
            task_repository: TaskRepository = Depends(get_task_repository)
        ) -> TaskService:
            """Factory function for TaskService"""
            return TaskService(task_repository)
        
        # Store dependency factories for use in routes
        self.get_task_service = get_task_service
    
    def _setup_routes(self):
        """Setup application routes"""
        
        # Health check endpoint
        @self.app.get("/health", tags=["health"])
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "message": "Task Management API is running"}
        
        # Root endpoint
        @self.app.get("/", tags=["root"])
        async def root():
            """Root endpoint with API information"""
            return {
                "message": "Welcome to Task Management API",
                "version": "1.0.0",
                "docs": "/docs",
                "redoc": "/redoc",
                "health": "/health"
            }
        
       
       
        
        # Include task routes
        self.app.include_router(task_router)
        
        # Include user routes
        self.app.include_router(user_router)
        
        logger.info("Routes configured successfully")
    
    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance"""
        return self.app


# Create application instance
task_management_api = TaskManagementAPI()
app = task_management_api.get_app()


if __name__ == "__main__":
    """
    Run the application directly
    
    For development: python main.py
    For production: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
    """
    
    logger.info("Starting Task Management API...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
