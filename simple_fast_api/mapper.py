from typing import List
from entity import User, Task, TaskDetail
from models.db_user_model import (
    UserDto, UserWithTasksDto, TaskDto, TaskDetailDto, UserListDto,
    UserRoleDto, UserStatusDto, TaskStatusDto, TaskPriorityDto, TaskDetailTypeDto
)

class UserMapper:
    
    @staticmethod
    def to_user_dto(user: User) -> UserDto:
        """Convert User entity to UserDto"""
        return UserDto(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            role=UserRoleDto(user.role.value),
            status=UserStatusDto(user.status.value),
            created_at=user.created_at,
            email_verified=user.email_verified
        )
    
    @staticmethod
    def to_task_detail_dto(detail: TaskDetail) -> TaskDetailDto:
        """Convert TaskDetail entity to TaskDetailDto"""
        return TaskDetailDto(
            id=detail.id,
            detail_type=TaskDetailTypeDto(detail.detail_type.value),
            title=detail.title,
            content=detail.content,
            file_path=detail.file_path,
            file_name=detail.file_name,
            created_by=detail.created_by,
            created_at=detail.created_at,
            is_completed=detail.is_completed,
            order_index=detail.order_index
        )
    
    @staticmethod
    def to_task_dto(task: Task) -> TaskDto:
        """Convert Task entity to TaskDto"""
        return TaskDto(
            id=task.id,
            title=task.title,
            description=task.description,
            status=TaskStatusDto(task.status.value),
            priority=TaskPriorityDto(task.priority.value),
            created_by=task.created_by,
            assigned_to=task.assigned_to,
            created_at=task.created_at,
            due_date=task.due_date,
            completed_at=task.completed_at,
            task_details=[
                UserMapper.to_task_detail_dto(detail) 
                for detail in task.task_details
            ]
        )
    
    @staticmethod
    def to_user_with_tasks_dto(user: User) -> UserWithTasksDto:
        """Convert User entity with tasks to UserWithTasksDto"""
        return UserWithTasksDto(
            user=UserMapper.to_user_dto(user),
            tasks=[
                UserMapper.to_task_dto(task) 
                for task in user.tasks
            ],
            total_tasks=len(user.tasks)
        )
    
    @staticmethod
    def to_user_list_dto(users: List[User]) -> UserListDto:
        """Convert list of User entities to UserListDto"""
        return UserListDto(
            users=[
                UserMapper.to_user_dto(user) 
                for user in users
            ],
            total=len(users)
        )