from pydantic import BaseModel
class ClassA(BaseModel):
    id: int
    class_type: "ClassB"  


class ClassB(BaseModel):
    id: int
    class_type: "ClassC"

class ClassC(BaseModel):
    id: int