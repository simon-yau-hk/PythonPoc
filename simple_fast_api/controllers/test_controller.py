from fastapi import APIRouter
from config import settings
from models.test_model import ClassA, ClassB, ClassC
router = APIRouter(prefix="/api/test",tags=["test"])

@router.get("/testConfig")
def test_config():
   return {
        "instance_info": {
            "type": str(type(settings)),
            "class_name": settings.__class__.__name__,
            "has_Config": hasattr(settings, 'Config'),
            "Config_type": str(type(getattr(settings, 'Config', None))),
            "is_same_as_class_Config": getattr(settings, 'Config', None) is settings.__class__.Config,
        },
        "class_info": {
            "MyConfig_has_Config": hasattr(settings.__class__, 'Config'),
            "MyConfig_Config_env_file": settings.__class__.Config.env_file,
        },
        "comparison": {
            "settings.Config.env_file": getattr(settings, 'Config', {}).env_file if hasattr(settings, 'Config') else 'NOT_FOUND',
            "MyConfig.Config.env_file": settings.__class__.Config.env_file,
            "are_they_same": getattr(settings, 'Config', None) is settings.__class__.Config,
        }
    }


@router.get("/testClassInheritance")
def test_class_inheritance():
    classA = ClassA(id=1, class_type=ClassB(id=1, class_type=ClassC(id=1)))
    return {
        "message": "Class inheritance test successful",
        "classA": classA
    }

