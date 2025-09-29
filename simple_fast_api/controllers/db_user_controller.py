from fastapi import APIRouter
from services.db_user_service import DbUserService
router = APIRouter(prefix="/api/db_users",tags=["db_users"])

@router.get("/{id}")
def get_user(id: int):
    db_user_service = DbUserService()
    
    user = db_user_service.get_user_by_id(id)
    return user
