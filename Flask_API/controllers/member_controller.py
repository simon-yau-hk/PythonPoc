"""
Member Controller for Flask API
HTTP request handling for member operations
"""

from flask import Blueprint, request, jsonify
from services.member_service import MemberService
from mappers.member_mapper import MemberMapper, TaskMapper

member_bp = Blueprint('members', __name__)

@member_bp.route('/', methods=['GET'])
def get_members():
    """Get all members"""
    try:
        # Optional filter for active members only
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        
        if active_only:
            members = MemberService.get_active_members()
        else:
            members = MemberService.get_all_members()
        
        return jsonify({
            'success': True,
            'data': MemberMapper.to_list_dict(members),
            'count': len(members)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@member_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Get member by ID"""
    try:
        member = MemberService.get_member_by_id(member_id)
        if member:
            return jsonify({
                'success': True,
                'data': MemberMapper.to_dict(member)
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Member not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@member_bp.route('/', methods=['POST'])
def create_member():
    """Create a new member"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('username') or not data.get('email'):
            return jsonify({
                'success': False,
                'message': 'Username and email are required'
            }), 400
        
        # Check if username already exists
        existing_member = MemberService.get_member_by_username(data['username'])
        if existing_member:
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 400
        
        # Check if email already exists
        existing_member = MemberService.get_member_by_email(data['email'])
        if existing_member:
            return jsonify({
                'success': False,
                'message': 'Email already exists'
            }), 400
        
        member = MemberService.create_member(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            password_hash=data.get('password_hash')
        )
        
        return jsonify({
            'success': True,
            'data': MemberMapper.to_dict(member),
            'message': 'Member created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@member_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Update member by ID"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        member = MemberService.update_member(member_id, **data)
        if member:
            return jsonify({
                'success': True,
                'data': MemberMapper.to_dict(member),
                'message': 'Member updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Member not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@member_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete member by ID (cascades to tasks and task_items)"""
    try:
        success = MemberService.delete_member(member_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Member deleted successfully (including related tasks and task items)'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Member not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@member_bp.route('/<int:member_id>/deactivate', methods=['PATCH'])
def deactivate_member(member_id):
    """Deactivate member (soft delete)"""
    try:
        member = MemberService.deactivate_member(member_id)
        if member:
            return jsonify({
                'success': True,
                'data': MemberMapper.to_dict(member),
                'message': 'Member deactivated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Member not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@member_bp.route('/<int:member_id>/tasks', methods=['GET'])
def get_member_tasks(member_id):
    """Get all tasks for a specific member"""
    try:
        member = MemberService.get_member_by_id(member_id)
        if not member:
            return jsonify({
                'success': False,
                'message': 'Member not found'
            }), 404
        
        tasks = [TaskMapper.to_dict(task) for task in member.tasks]
        return jsonify({
            'success': True,
            'data': tasks,
            'count': len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@member_bp.route('/with-tasks', methods=['GET'])
def get_members_with_tasks():
    """Get all members with their tasks and task details (task items) using eager loading"""
    try:
        # Use eager loading to get all data in a single query
        members = MemberService.get_all_members_with_tasks_and_items()
        
        # Optional filter for active members only
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        if active_only:
            members = [m for m in members if m.is_active]
        
        # Use mapper to convert to JSON-serializable dictionaries
        members_data = MemberMapper.to_list_dict_with_tasks_and_items(members)
        
        return jsonify({
            'success': True,
            'data': members_data,
            'count': len(members_data),
            'message': 'Members with tasks and task details (eager loaded)'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

