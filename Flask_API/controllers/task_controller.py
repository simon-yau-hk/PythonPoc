"""
Task Controller for Flask API
HTTP request handling for task operations
"""

from flask import Blueprint, request, jsonify
from services.task_service import TaskService
from services.member_service import MemberService
from datetime import datetime

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filters"""
    try:
        # Optional filters
        status = request.args.get('status')
        priority = request.args.get('priority')
        member_id = request.args.get('member_id', type=int)
        include_items = request.args.get('include_items', 'false').lower() == 'true'
        
        if member_id:
            tasks = TaskService.get_tasks_by_member(member_id)
        elif status:
            tasks = TaskService.get_tasks_by_status(status)
        elif priority:
            tasks = TaskService.get_tasks_by_priority(priority)
        else:
            tasks = TaskService.get_all_tasks()
        
        return jsonify({
            'success': True,
            'data': [task.to_dict(include_items=include_items) for task in tasks],
            'count': len(tasks)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get task by ID"""
    try:
        include_items = request.args.get('include_items', 'false').lower() == 'true'
        task = TaskService.get_task_by_id(task_id)
        
        if task:
            return jsonify({
                'success': True,
                'data': task.to_dict(include_items=include_items)
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('title') or not data.get('member_id'):
            return jsonify({
                'success': False,
                'message': 'Title and member_id are required'
            }), 400
        
        # Check if member exists
        member = MemberService.get_member_by_id(data['member_id'])
        if not member:
            return jsonify({
                'success': False,
                'message': 'Member not found'
            }), 400
        
        # Parse due_date if provided
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
        
        task = TaskService.create_task(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'pending'),
            due_date=due_date,
            member_id=data['member_id']
        )
        
        return jsonify({
            'success': True,
            'data': task.to_dict(),
            'message': 'Task created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task by ID"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Parse due_date if provided
        if data.get('due_date'):
            try:
                data['due_date'] = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
        
        task = TaskService.update_task(task_id, **data)
        if task:
            return jsonify({
                'success': True,
                'data': task.to_dict(),
                'message': 'Task updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete task by ID (cascades to task_items)"""
    try:
        success = TaskService.delete_task(task_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Task deleted successfully (including related task items)'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    """Mark task as completed"""
    try:
        task = TaskService.complete_task(task_id)
        if task:
            return jsonify({
                'success': True,
                'data': task.to_dict(),
                'message': 'Task marked as completed'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/<int:task_id>/items', methods=['GET'])
def get_task_items(task_id):
    """Get all items for a specific task"""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404
        
        items = [item.to_dict() for item in task.task_items]
        return jsonify({
            'success': True,
            'data': items,
            'count': len(items)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
