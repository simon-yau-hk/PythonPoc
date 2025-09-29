from fastapi import APIRouter, Form, File, UploadFile
from typing import List, Optional 
from services.task_service import TaskService
from models.task_model import GetTaskRequest, GetTaskResponse,GetTaskRequestV2, GetTaskResponseV2
router = APIRouter(prefix="/api/tasks",tags=["tasks"])

@router.get("/{id}")
def get_task(id: int):
    task_service = TaskService()
    request = GetTaskRequest()
    request.id = id
    response = task_service.get_task(request)
    return response

@router.get("/{id}/v2")
def get_task_v2(id: int):
    task_service = TaskService()
    request = GetTaskRequestV2(id=id)
    response = task_service.get_task_v2(request)
    return response

@router.post("/testPassFormData")
async def test_pass_form_data(
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form("medium"),
    completed: bool = Form(False)
):
    """
    Test endpoint for handling form data
    Content-Type: application/x-www-form-urlencoded
    """
    return {
        "message": "Form data received successfully",
        "data": {
            "title": title,
            "description": description,
            "priority": priority,
            "completed": completed
        }
    }

@router.post("/testPassFormDataWithFiles")
async def test_pass_form_data_with_files(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    optional_files: List[UploadFile] = File(None)
):
    """
    Test endpoint for handling form data with file uploads
    Content-Type: multipart/form-data
    """
    # Read file content (optional)
    file_content = await file.read()
    
    # Process optional files
    uploaded_files = []
    if optional_files:
        for uploaded_file in optional_files:
            if uploaded_file.filename:  # Check if file was actually uploaded
                uploaded_files.append({
                    "filename": uploaded_file.filename,
                    "content_type": uploaded_file.content_type,
                    "size": len(await uploaded_file.read())
                })
    
    return {
        "message": "Form data with files received successfully",
        "form_data": {
            "title": title,
            "description": description
        },
        "main_file": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content)
        },
        "additional_files": uploaded_files
    }


@router.post("/testPassJsonData")
async def test_pass_json_data(
    request_data: dict
):
   
    return {
        "message": "JSON data received successfully",
        "your_json_data": request_data,
        "data_type": type(request_data).__name__
    }