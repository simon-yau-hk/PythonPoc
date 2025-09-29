from fastapi import APIRouter


router = APIRouter(prefix="/api/users",tags=["users"])

@router.get("/")
def get_user():
    return {"message": "Hello User"}