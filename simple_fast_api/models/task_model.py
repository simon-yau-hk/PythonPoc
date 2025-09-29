from pydantic import BaseModel
class GetTaskRequest():
    id: int


class GetTaskResponse():
    id: int
    title: str
    description: str

class GetTaskRequestV2(BaseModel):
    id: int


class GetTaskResponseV2(BaseModel):
    id: int
    title: str
    description: str