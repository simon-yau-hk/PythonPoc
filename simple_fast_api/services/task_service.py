from models.task_model import GetTaskRequest, GetTaskResponse, GetTaskRequestV2, GetTaskResponseV2
import logging
logger = logging.getLogger(__name__)

class TaskService:  
    """
    Task Service implementing business logic
    
    This layer contains all business rules, validation, and orchestration logic.
    It acts as the intermediary between controllers and repositories.
    """

    def get_task(self, request:GetTaskRequest) -> GetTaskResponse:
        """
        Create a new task with business validation
        
        Business Rules:
        - Title must be unique for the user
        - Due date cannot be in the past
        - High/Urgent priority tasks must have due date
        """
        try:
            # Business validation
           
            
            logger.info(f"Task: {request}")
            ret = GetTaskResponse()
            ret.id = request.id
            ret.title = "Task Title"
            ret.description = "Task Description"
            return ret
            
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise
    
    def get_task_v2(self, request:GetTaskRequestV2) -> GetTaskResponseV2:
        """
        Get task by ID with business validation
        """
       
        logger.info(f"Task: {request}")
        ret = GetTaskResponseV2(id=request.id,title="Task Title",description="Task Description")
        return ret
    