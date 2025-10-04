"""
Member Mapper for Flask API
Converts SQLAlchemy models to JSON-serializable dictionaries
"""

from typing import List, Dict, Any
from models.member_model import Member
from models.task_model import Task
from models.task_item_model import TaskItem

class MemberMapper:
    
    @staticmethod
    def to_dict(member: Member) -> Dict[str, Any]:
        """Convert Member model to dictionary"""
        return {
            'id': member.id,
            'username': member.username,
            'email': member.email,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'is_active': member.is_active,
            'created_at': member.created_at.isoformat() if member.created_at else None,
            'updated_at': member.updated_at.isoformat() if member.updated_at else None
        }
    
    @staticmethod
    def to_dict_with_tasks(member: Member) -> Dict[str, Any]:
        """Convert Member model to dictionary with tasks"""
        member_data = MemberMapper.to_dict(member)
        
        # Add tasks
        tasks_data = []
        for task in member.tasks:
            task_data = TaskMapper.to_dict(task)
            tasks_data.append(task_data)
        
        member_data['tasks'] = tasks_data
        member_data['task_count'] = len(tasks_data)
        
        # Calculate task statistics
        completed_tasks = len([t for t in member.tasks if t.status == 'completed'])
        pending_tasks = len([t for t in member.tasks if t.status != 'completed'])
        
        member_data['task_stats'] = {
            'total': len(tasks_data),
            'completed': completed_tasks,
            'pending': pending_tasks
        }
        
        return member_data
    
    @staticmethod
    def to_dict_with_tasks_and_items(member: Member) -> Dict[str, Any]:
        """Convert Member model to dictionary with tasks and task items"""
        member_data = MemberMapper.to_dict(member)
        
        # Add tasks with their items
        tasks_data = []
        for task in member.tasks:
            task_data = TaskMapper.to_dict_with_items(task)
            tasks_data.append(task_data)
        
        member_data['tasks'] = tasks_data
        member_data['task_count'] = len(tasks_data)
        
        # Calculate task statistics
        completed_tasks = len([t for t in member.tasks if t.status == 'completed'])
        pending_tasks = len([t for t in member.tasks if t.status != 'completed'])
        
        member_data['task_stats'] = {
            'total': len(tasks_data),
            'completed': completed_tasks,
            'pending': pending_tasks
        }
        
        return member_data
    
    @staticmethod
    def to_list_dict(members: List[Member]) -> List[Dict[str, Any]]:
        """Convert list of Member models to list of dictionaries"""
        return [MemberMapper.to_dict(member) for member in members]
    
    @staticmethod
    def to_list_dict_with_tasks(members: List[Member]) -> List[Dict[str, Any]]:
        """Convert list of Member models to list of dictionaries with tasks"""
        return [MemberMapper.to_dict_with_tasks(member) for member in members]
    
    @staticmethod
    def to_list_dict_with_tasks_and_items(members: List[Member]) -> List[Dict[str, Any]]:
        """Convert list of Member models to list of dictionaries with tasks and items"""
        return [MemberMapper.to_dict_with_tasks_and_items(member) for member in members]

class TaskMapper:
    
    @staticmethod
    def to_dict(task: Task) -> Dict[str, Any]:
        """Convert Task model to dictionary"""
        return {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'updated_at': task.updated_at.isoformat() if task.updated_at else None,
            'member_id': task.member_id
        }
    
    @staticmethod
    def to_dict_with_items(task: Task) -> Dict[str, Any]:
        """Convert Task model to dictionary with task items"""
        task_data = TaskMapper.to_dict(task)
        
        # Add task items
        items_data = []
        for item in task.task_items:
            item_data = TaskItemMapper.to_dict(item)
            items_data.append(item_data)
        
        task_data['task_items'] = items_data
        task_data['item_count'] = len(items_data)
        
        # Calculate item statistics
        completed_items = len([i for i in task.task_items if i.is_completed])
        pending_items = len([i for i in task.task_items if not i.is_completed])
        
        task_data['item_stats'] = {
            'total': len(items_data),
            'completed': completed_items,
            'pending': pending_items
        }
        
        return task_data
    
    @staticmethod
    def to_list_dict(tasks: List[Task]) -> List[Dict[str, Any]]:
        """Convert list of Task models to list of dictionaries"""
        return [TaskMapper.to_dict(task) for task in tasks]
    
    @staticmethod
    def to_list_dict_with_items(tasks: List[Task]) -> List[Dict[str, Any]]:
        """Convert list of Task models to list of dictionaries with items"""
        return [TaskMapper.to_dict_with_items(task) for task in tasks]

class TaskItemMapper:
    
    @staticmethod
    def to_dict(item: TaskItem) -> Dict[str, Any]:
        """Convert TaskItem model to dictionary"""
        return {
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'is_completed': item.is_completed,
            'order': item.order,
            'created_at': item.created_at.isoformat() if item.created_at else None,
            'updated_at': item.updated_at.isoformat() if item.updated_at else None,
            'completed_at': item.completed_at.isoformat() if item.completed_at else None,
            'task_id': item.task_id
        }
    
    @staticmethod
    def to_list_dict(items: List[TaskItem]) -> List[Dict[str, Any]]:
        """Convert list of TaskItem models to list of dictionaries"""
        return [TaskItemMapper.to_dict(item) for item in items]
