"""
Simple FastAPI - Hello World
The most basic FastAPI application possible
"""

from fastapi import FastAPI
from database import get_db
from controllers.task_controller import router as task_router
from controllers.user_controller import router as user_router
from controllers.test_controller import router as test_router
from controllers.db_user_controller import router as db_user_router

app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)
app.include_router(test_router)
app.include_router(db_user_router)

get_db()
# Single endpoint - Hello World
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)