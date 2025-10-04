"""
Flask Web API Application
Configured to use existing MySQL database with members, tasks, and task_items tables
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api, Resource, fields, Namespace
import os
from datetime import datetime
from dotenv import load_dotenv
from database import db 

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration - MySQL Database
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost:3306/task_management')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # Set to True to see SQL queries

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)  # Enable CORS for all routes

# Initialize Flask-RESTX API for Swagger documentation
api = Api(
    app,
    version='1.0.0',
    title='Flask Task Management API',
    description='A comprehensive Flask API for task management with MySQL database integration',
    doc='/docs/',  # Swagger UI will be available at /swagger/
    prefix='/api'
)

# Create namespaces for better organization
members_ns = Namespace('members', description='Member operations')
tasks_ns = Namespace('tasks', description='Task operations')
task_items_ns = Namespace('task-items', description='Task item operations')

# Add namespaces to API
api.add_namespace(members_ns)
api.add_namespace(tasks_ns)
api.add_namespace(task_items_ns)

# Import models after db is initialized
from models.member_model import Member
from models.task_model import Task
from models.task_item_model import TaskItem

# Import services and mappers
from services.member_service import MemberService
from services.task_service import TaskService
from services.task_item_service import TaskItemService
from mappers.member_mapper import MemberMapper, TaskMapper, TaskItemMapper

# Define Swagger models for request/response documentation
member_model = api.model('Member', {
    'id': fields.Integer(readonly=True, description='Member ID'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email address'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'is_active': fields.Boolean(description='Active status'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

member_create_model = api.model('MemberCreate', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email address'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'password_hash': fields.String(description='Password hash')
})

task_item_model = api.model('TaskItem', {
    'id': fields.Integer(readonly=True, description='Task item ID'),
    'title': fields.String(required=True, description='Task item title'),
    'description': fields.String(description='Task item description'),
    'is_completed': fields.Boolean(description='Completion status'),
    'order': fields.Integer(description='Display order'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp'),
    'completed_at': fields.DateTime(description='Completion timestamp'),
    'task_id': fields.Integer(description='Parent task ID')
})

task_model = api.model('Task', {
    'id': fields.Integer(readonly=True, description='Task ID'),
    'title': fields.String(required=True, description='Task title'),
    'description': fields.String(description='Task description'),
    'priority': fields.String(description='Task priority (low, medium, high)'),
    'status': fields.String(description='Task status (pending, in_progress, completed)'),
    'due_date': fields.DateTime(description='Due date'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp'),
    'member_id': fields.Integer(description='Assigned member ID'),
    'task_items': fields.List(fields.Nested(task_item_model), description='Task items')
})

task_create_model = api.model('TaskCreate', {
    'title': fields.String(required=True, description='Task title'),
    'description': fields.String(description='Task description'),
    'priority': fields.String(description='Task priority'),
    'status': fields.String(description='Task status'),
    'due_date': fields.DateTime(description='Due date'),
    'member_id': fields.Integer(required=True, description='Assigned member ID')
})

task_item_create_model = api.model('TaskItemCreate', {
    'title': fields.String(required=True, description='Task item title'),
    'description': fields.String(description='Task item description'),
    'order': fields.Integer(description='Display order'),
    'task_id': fields.Integer(required=True, description='Parent task ID')
})

# Response models
success_response = api.model('SuccessResponse', {
    'success': fields.Boolean(description='Operation success status'),
    'data': fields.Raw(description='Response data'),
    'count': fields.Integer(description='Number of items returned'),
    'message': fields.String(description='Response message')
})

error_response = api.model('ErrorResponse', {
    'success': fields.Boolean(description='Operation success status'),
    'message': fields.String(description='Error message')
})

# Import controllers
from controllers.member_controller import member_bp
from controllers.task_controller import task_bp
from controllers.task_item_controller import task_item_bp

# Register blueprints
app.register_blueprint(member_bp, url_prefix='/api/members')
app.register_blueprint(task_bp, url_prefix='/api/tasks')
app.register_blueprint(task_item_bp, url_prefix='/api/task-items')

# Root endpoint
@app.route('/')
def hello_world():
    return jsonify({
        "message": "Flask API connected to MySQL Database",
        "version": "1.0.0",
        "database": "task_management",
        "timestamp": datetime.now().isoformat()
    })

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    })


# Member endpoints
@members_ns.route('/')
class MemberList(Resource):
    @api.doc('get_members')
    @api.marshal_with(success_response)
    def get(self):
        """Get all members"""
        try:
            members = MemberService.get_all_members()
            return {
                'success': True,
                'data': MemberMapper.to_list_dict(members),
                'count': len(members),
                'message': 'Members retrieved successfully'
            }
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('create_member')
    @api.expect(member_create_model)
    @api.marshal_with(success_response, code=201)
    def post(self):
        """Create a new member"""
        try:
            data = api.payload
            if not data or not data.get('username') or not data.get('email'):
                api.abort(400, 'Username and email are required')
            
            member = MemberService.create_member(
                username=data['username'],
                email=data['email'],
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                password_hash=data.get('password_hash')
            )
            
            return {
                'success': True,
                'data': MemberMapper.to_dict(member),
                'count': 1,
                'message': 'Member created successfully'
            }, 201
        except Exception as e:
            api.abort(500, str(e))

@members_ns.route('/<int:member_id>')
class MemberDetail(Resource):
    @api.doc('get_member')
    @api.marshal_with(success_response)
    def get(self, member_id):
        """Get member by ID"""
        try:
            member = MemberService.get_member_by_id(member_id)
            if member:
                return {
                    'success': True,
                    'data': MemberMapper.to_dict(member),
                    'count': 1,
                    'message': 'Member retrieved successfully'
                }
            else:
                api.abort(404, 'Member not found')
        except Exception as e:
            api.abort(500, str(e))

@members_ns.route('/with-tasks')
class MembersWithTasks(Resource):
    @api.doc('get_members_with_tasks')
    @api.marshal_with(success_response)
    def get(self):
        """Get all members with their tasks and task details"""
        try:
            members = MemberService.get_all_members_with_tasks_and_items()
            members_data = MemberMapper.to_list_dict_with_tasks_and_items(members)
            
            return {
                'success': True,
                'data': members_data,
                'count': len(members_data),
                'message': 'Members with tasks and task details retrieved successfully'
            }
        except Exception as e:
            api.abort(500, str(e))

if __name__ == '__main__':
    # Note: We don't call db.create_all() because tables already exist
    print("\n" + "="*60)
    print("Flask API Server Starting...")
    print("="*60)
    print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Server: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
