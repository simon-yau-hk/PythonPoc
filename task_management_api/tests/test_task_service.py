"""
Tests for TaskService - Business Logic Layer
Demonstrates testing the service layer in isolation
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock

from app.services.task_service import TaskService, TaskNotFoundError, TaskValidationError
from app.repositories.task_repository import TaskRepository
from app.models.task import Task, TaskStatus, TaskPriority
from app.dto.task_dto import CreateTaskRequest, UpdateTaskRequest, TaskPriorityDTO, TaskStatusDTO


class TestTaskService:
    """Test suite for TaskService"""
    
    @pytest.fixture
    def mock_repository(self):
        """Create mock repository"""
        return Mock(spec=TaskRepository)
    
    @pytest.fixture
    def task_service(self, mock_repository):
        """Create TaskService with mock repository"""
        return TaskService(mock_repository)
    
    @pytest.fixture
    def sample_task(self):
        """Create a sample task for testing"""
        return Task(
            id=1,
            title="Test Task",
            description="Test Description",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            created_by="user1",
            assigned_to=None,
            created_at=datetime.utcnow()
        )
    
    def test_create_task_success(self, task_service, mock_repository):
        """Test successful task creation"""
        # Arrange
        request = CreateTaskRequest(
            title="New Task",
            description="Task Description",
            priority=TaskPriorityDTO.HIGH,
            created_by="user1",
            due_date=datetime.utcnow() + timedelta(days=1)
        )
        
        mock_task = Task(
            id=1,
            title=request.title,
            description=request.description,
            priority=TaskPriority.HIGH,
            created_by=request.created_by,
            status=TaskStatus.PENDING
        )
        
        mock_repository.find_by_criteria.return_value = []  # No existing tasks
        mock_repository.create.return_value = mock_task
        
        # Act
        result = task_service.create_task(request)
        
        # Assert
        assert result.title == request.title
        assert result.priority == TaskPriorityDTO.HIGH
        mock_repository.create.assert_called_once()
    
    def test_create_task_validation_error_past_due_date(self, task_service, mock_repository):
        """Test task creation with past due date"""
        # Arrange
        request = CreateTaskRequest(
            title="Invalid Task",
            description="Task with past due date",
            priority=TaskPriorityDTO.MEDIUM,
            created_by="user1",
            due_date=datetime.utcnow() - timedelta(days=1)  # Past date
        )
        
        # Act & Assert
        with pytest.raises(TaskValidationError, match="Due date cannot be in the past"):
            task_service.create_task(request)
    
    def test_create_task_validation_error_high_priority_no_due_date(self, task_service, mock_repository):
        """Test high priority task without due date"""
        # Arrange
        request = CreateTaskRequest(
            title="High Priority Task",
            description="High priority without due date",
            priority=TaskPriorityDTO.HIGH,
            created_by="user1",
            due_date=None  # No due date
        )
        
        # Act & Assert
        with pytest.raises(TaskValidationError, match="High and urgent priority tasks must have a due date"):
            task_service.create_task(request)
    
    def test_get_task_by_id_success(self, task_service, mock_repository, sample_task):
        """Test successful task retrieval"""
        # Arrange
        mock_repository.get_by_id.return_value = sample_task
        
        # Act
        result = task_service.get_task_by_id(1, "user1")
        
        # Assert
        assert result.id == sample_task.id
        assert result.title == sample_task.title
        mock_repository.get_by_id.assert_called_once_with(1)
    
    def test_get_task_by_id_not_found(self, task_service, mock_repository):
        """Test task not found scenario"""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(TaskNotFoundError):
            task_service.get_task_by_id(999, "user1")
    
    def test_update_task_success(self, task_service, mock_repository, sample_task):
        """Test successful task update"""
        # Arrange
        request = UpdateTaskRequest(
            title="Updated Title",
            status=TaskStatusDTO.IN_PROGRESS
        )
        
        mock_repository.get_by_id.return_value = sample_task
        mock_repository.update.return_value = sample_task
        
        # Act
        result = task_service.update_task(1, request, "user1")
        
        # Assert
        assert result.title == "Updated Title"
        mock_repository.update.assert_called_once()
    
    def test_complete_task_success(self, task_service, mock_repository, sample_task):
        """Test successful task completion"""
        # Arrange
        mock_repository.get_by_id.return_value = sample_task
        mock_repository.update.return_value = sample_task
        
        # Act
        result = task_service.complete_task(1, "user1")
        
        # Assert
        assert sample_task.status == TaskStatus.COMPLETED
        assert sample_task.completed_at is not None
        mock_repository.update.assert_called_once()
    
    def test_delete_task_success(self, task_service, mock_repository, sample_task):
        """Test successful task deletion"""
        # Arrange
        mock_repository.get_by_id.return_value = sample_task
        mock_repository.delete.return_value = True
        
        # Act
        result = task_service.delete_task(1, "user1")
        
        # Assert
        assert result is True
        mock_repository.delete.assert_called_once_with(1)
    
    def test_get_task_statistics(self, task_service, mock_repository):
        """Test task statistics retrieval"""
        # Arrange
        expected_stats = {
            'total_tasks': 10,
            'pending_tasks': 3,
            'in_progress_tasks': 4,
            'completed_tasks': 2,
            'cancelled_tasks': 1,
            'overdue_tasks': 2,
            'high_priority_tasks': 3
        }
        mock_repository.get_task_statistics.return_value = expected_stats
        
        # Act
        result = task_service.get_task_statistics()
        
        # Assert
        assert result.total_tasks == 10
        assert result.pending_tasks == 3
        assert result.completed_tasks == 2
