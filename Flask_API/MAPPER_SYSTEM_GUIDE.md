# Flask API Mapper System Guide

## 🎯 **What is a Mapper?**

A **mapper** is a design pattern that converts objects from one format to another. In our Flask API, mappers convert SQLAlchemy model objects to JSON-serializable dictionaries.

## 🔧 **Why Do We Need Mappers?**

### **The Problem:**
```python
# ❌ This doesn't work - SQLAlchemy objects aren't JSON serializable
members = Member.query.all()
return jsonify(members)  # TypeError: Object of type Member is not JSON serializable
```

### **The Solution:**
```python
# ✅ This works - Mappers convert to dictionaries
members = Member.query.all()
members_data = MemberMapper.to_list_dict(members)
return jsonify(members_data)  # Clean JSON response
```

## 🏗️ **Mapper System Architecture**

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Controller    │───▶│    Mapper    │───▶│   JSON Response │
│                 │    │              │    │                 │
│ SQLAlchemy Obj  │    │ Convert to   │    │ Dictionary      │
│                 │    │ Dictionary   │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘
```

## 📁 **File Structure**

```
Flask_API/
├── mappers/
│   ├── __init__.py
│   └── member_mapper.py          # All mapper classes
├── controllers/
│   └── member_controller.py     # Uses mappers
└── models/
    ├── member_model.py          # SQLAlchemy models
    ├── task_model.py
    └── task_item_model.py
```

## 🔧 **Mapper Classes**

### **MemberMapper**
```python
class MemberMapper:
    @staticmethod
    def to_dict(member: Member) -> Dict[str, Any]:
        """Convert single Member to dictionary"""
        
    @staticmethod
    def to_dict_with_tasks(member: Member) -> Dict[str, Any]:
        """Convert Member with tasks to dictionary"""
        
    @staticmethod
    def to_dict_with_tasks_and_items(member: Member) -> Dict[str, Any]:
        """Convert Member with tasks and task items to dictionary"""
        
    @staticmethod
    def to_list_dict(members: List[Member]) -> List[Dict[str, Any]]:
        """Convert list of Members to list of dictionaries"""
```

### **TaskMapper**
```python
class TaskMapper:
    @staticmethod
    def to_dict(task: Task) -> Dict[str, Any]:
        """Convert single Task to dictionary"""
        
    @staticmethod
    def to_dict_with_items(task: Task) -> Dict[str, Any]:
        """Convert Task with items to dictionary"""
```

### **TaskItemMapper**
```python
class TaskItemMapper:
    @staticmethod
    def to_dict(item: TaskItem) -> Dict[str, Any]:
        """Convert single TaskItem to dictionary"""
```

## 🚀 **Usage Examples**

### **1. Basic Member Conversion**
```python
# Controller
member = MemberService.get_member_by_id(1)
member_data = MemberMapper.to_dict(member)
return jsonify({'data': member_data})
```

### **2. List of Members**
```python
# Controller
members = MemberService.get_all_members()
members_data = MemberMapper.to_list_dict(members)
return jsonify({'data': members_data, 'count': len(members_data)})
```

### **3. Members with Tasks and Items**
```python
# Controller
members = MemberService.get_all_members_with_tasks_and_items()
members_data = MemberMapper.to_list_dict_with_tasks_and_items(members)
return jsonify({'data': members_data, 'count': len(members_data)})
```

## 📊 **Output Examples**

### **Basic Member Dictionary**
```json
{
  "id": 1,
  "username": "johnsmith1",
  "email": "johnsmith1@gmail.com",
  "first_name": "John",
  "last_name": "Smith",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### **Member with Tasks**
```json
{
  "id": 1,
  "username": "johnsmith1",
  "email": "johnsmith1@gmail.com",
  "tasks": [
    {
      "id": 1,
      "title": "Complete Project",
      "status": "pending",
      "priority": "high",
      "member_id": 1
    }
  ],
  "task_count": 1,
  "task_stats": {
    "total": 1,
    "completed": 0,
    "pending": 1
  }
}
```

### **Member with Tasks and Task Items**
```json
{
  "id": 1,
  "username": "johnsmith1",
  "tasks": [
    {
      "id": 1,
      "title": "Complete Project",
      "task_items": [
        {
          "id": 1,
          "title": "Research requirements",
          "is_completed": false,
          "order": 0
        },
        {
          "id": 2,
          "title": "Create wireframes",
          "is_completed": true,
          "order": 1
        }
      ],
      "item_count": 2,
      "item_stats": {
        "total": 2,
        "completed": 1,
        "pending": 1
      }
    }
  ]
}
```

## 🎯 **Controller Integration**

### **Before (Without Mapper)**
```python
@member_bp.route('/')
def get_members():
    members = MemberService.get_all_members()
    return jsonify({
        'data': [member.to_dict() for member in members]  # Manual conversion
    })
```

### **After (With Mapper)**
```python
@member_bp.route('/')
def get_members():
    members = MemberService.get_all_members()
    return jsonify({
        'data': MemberMapper.to_list_dict(members)  # Clean mapper conversion
    })
```

## 💡 **Benefits of Mapper System**

### **1. JSON Serialization**
- ✅ Converts SQLAlchemy objects to JSON-serializable dictionaries
- ✅ No more "Object is not JSON serializable" errors

### **2. Clean Separation**
- ✅ Business logic (services) separate from serialization (mappers)
- ✅ Controllers focus on HTTP handling, not data conversion

### **3. Reusability**
- ✅ Same mapper used across different endpoints
- ✅ Consistent output format everywhere

### **4. Maintainability**
- ✅ Easy to modify output format in one place
- ✅ Clear, organized code structure

### **5. Type Safety**
- ✅ Clear input/output types
- ✅ IDE autocomplete and error checking

### **6. Performance**
- ✅ Efficient conversion with eager loading
- ✅ No N+1 query problems

## 🔄 **Mapper vs Direct Serialization**

| Aspect | Direct Serialization | Mapper System |
|--------|---------------------|---------------|
| **JSON Errors** | ❌ Common | ✅ None |
| **Code Reuse** | ❌ Repeated logic | ✅ Reusable |
| **Maintainability** | ❌ Scattered changes | ✅ Centralized |
| **Type Safety** | ❌ Manual typing | ✅ Clear types |
| **Consistency** | ❌ Inconsistent | ✅ Standardized |
| **Performance** | ❌ Manual optimization | ✅ Optimized |

## 🧪 **Testing the Mapper System**

### **Run the test script:**
```bash
python test_mapper.py
```

### **Test endpoints:**
```bash
# Basic members
curl http://localhost:5000/api/members/

# Members with tasks and items
curl http://localhost:5000/api/members/with-tasks

# Health check
curl http://localhost:5000/health
```

## 🎓 **Best Practices**

### **1. Use Appropriate Mapper Method**
```python
# For simple data
MemberMapper.to_dict(member)

# For nested data
MemberMapper.to_dict_with_tasks_and_items(member)

# For lists
MemberMapper.to_list_dict(members)
```

### **2. Keep Mappers Focused**
```python
# ✅ Good - focused on conversion
def to_dict(member: Member) -> Dict[str, Any]:
    return {...}

# ❌ Bad - mixing business logic
def to_dict_with_calculations(member: Member) -> Dict[str, Any]:
    # Don't put business logic in mappers
```

### **3. Use Type Hints**
```python
# ✅ Good - clear types
def to_dict(member: Member) -> Dict[str, Any]:

# ❌ Bad - no type hints
def to_dict(member):
```

### **4. Handle None Values**
```python
# ✅ Good - handle None safely
'created_at': member.created_at.isoformat() if member.created_at else None

# ❌ Bad - can cause errors
'created_at': member.created_at.isoformat()
```

## 🚀 **Advanced Usage**

### **Custom Mapper Methods**
```python
@staticmethod
def to_dict_for_api(member: Member) -> Dict[str, Any]:
    """Custom format for API responses"""
    return {
        'id': member.id,
        'name': f"{member.first_name} {member.last_name}",
        'email': member.email,
        'active': member.is_active
    }
```

### **Conditional Mapping**
```python
@staticmethod
def to_dict_with_optional_tasks(member: Member, include_tasks: bool = False) -> Dict[str, Any]:
    """Include tasks only if requested"""
    data = MemberMapper.to_dict(member)
    if include_tasks:
        data['tasks'] = [TaskMapper.to_dict(task) for task in member.tasks]
    return data
```

## 🎉 **Summary**

The mapper system provides:

1. ✅ **Clean JSON serialization** - No more serialization errors
2. ✅ **Consistent output** - Standardized format across all endpoints
3. ✅ **Reusable logic** - Same mappers used everywhere
4. ✅ **Easy maintenance** - Change output format in one place
5. ✅ **Type safety** - Clear input/output types
6. ✅ **Performance** - Efficient conversion with eager loading

This is a professional, maintainable approach to handling object serialization in Flask APIs! 🚀
