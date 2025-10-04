"""
TaskItem Controller for Flask API
HTTP request handling for task item operations
"""

from flask import Blueprint, request, jsonify
from services.task_item_service import TaskItemService
from services.task_service import TaskService

task_item_bp = Blueprint('task_items', __name__)

@task_item_bp.route('/', methods=['GET'])
def get_task_items():
    """Get all task items with optional filters"""
    try:
        task_id = request.args.get('task_id', type=int)
        completed = request.args.get('completed')
        
        if task_id and completed is not None:
            if completed.lower() == 'true':
                items = TaskItemService.get_completed_items(task_id)
            else:
                items = TaskItemService.get_pending_items(task_id)
        elif task_id:
            items = TaskItemService.get_items_by_task(task_id)
        elif completed is not None:
            if completed.lower() == 'true':
                items = TaskItemService.get_completed_items()
            else:
                items = TaskItemService.get_pending_items()
        else:
            items = TaskItemService.get_all_task_items()
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in items],
            'count': len(items)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_item_bp.route('/<int:item_id>', methods=['GET'])
def get_task_item(item_id):
    """Get task item by ID"""
    try:
        item = TaskItemService.get_task_item_by_id(item_id)
        if item:
            return jsonify({
                'success': True,
                'data': item.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Task item not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_item_bp.route('/', methods=['POST'])
def create_task_item():
    """Create a new task item"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('title') or not data.get('task_id'):
            return jsonify({
                'success': False,
                'message': 'Title and task_id are required'
            }), 400
        
        # Check if task exists
        task = TaskService.get_task_by_id(data['task_id'])
        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 400
        
        item = TaskItemService.create_task_item(
            title=data['title'],
            description=data.get('description', ''),
            task_id=data['task_id'],
            order=data.get('order', 0)
        )
        
        return jsonify({
            'success': True,
            'data': item.to_dict(),
            'message': 'Task item created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_item_bp.route('/<int:item_id>', methods=['PUT'])
def update_task_item(item_id):
    """Update task item by ID"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        item = TaskItemService.update_task_item(item_id, **data)
        if item:
            return jsonify({
                'success': True,
                'data': item.to_dict(),
                'message': 'Task item updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Task item not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_item_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_task_item(item_id):
    """Delete task item by ID"""
    try:
        success = TaskItemService.delete_task_item(item_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Task item deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Task item not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_item_bp.route('/<int:item_id>/complete', methods=['PATCH'])
def complete_task_item(item_id):
    """Mark task item as completed"""
    try:
        item = TaskItemService.complete_task_item(item_id)
        if item:
            return jsonify({
                'success': True,
                'data': item.to_dict(),
                'message': 'Task item marked as completed'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Task item not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_item_bp.route('/<int:item_id>/uncomplete', methods=['PATCH'])
def uncomplete_task_item(item_id):
    """Mark task item as not completed"""
    try:
        item = TaskItemService.uncomplete_task_item(item_id)
        if item:
            return jsonify({
                'success': True,
                'data': item.to_dict(),
                'message': 'Task item marked as not completed'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Task item not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_item_bp.route('/reorder', methods=['POST'])
def reorder_task_items():
    """Reorder task items within a task"""
    try:
        data = request.get_json()
        
        if not data or not data.get('task_id') or not data.get('item_orders'):
            return jsonify({
                'success': False,
                'message': 'task_id and item_orders are required'
            }), 400
        
        # item_orders should be a dict like: {"1": 0, "2": 1, "3": 2}
        item_orders = {int(k): int(v) for k, v in data['item_orders'].items()}
        
        success = TaskItemService.reorder_items(data['task_id'], item_orders)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Task items reordered successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to reorder items'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

