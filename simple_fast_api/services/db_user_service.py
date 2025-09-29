from repositories.db_user_repository import DbUserRepository
from mapper import UserMapper
from models.db_user_model import UserDto, UserWithTasksDto, UserListDto
from typing import Optional

class DbUserService:    
    def __init__(self):
        self.repository = DbUserRepository()

    def get_user_by_id(self, user_id: int):
        user = self.repository.get_user_by_id(user_id)
        return UserMapper.to_user_with_tasks_dto(user)

    def get_all_users(self):
        return self.repository.get_all_users()
    