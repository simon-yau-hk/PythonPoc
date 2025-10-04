"""
Task Model for Flask API
Maps to existing 'tasks' table in database
"""

from database import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(10), nullable=True)  # e.g., 'low', 'medium', 'high'
    status = db.Column(db.String(15), nullable=True)    # e.g., 'pending', 'in_progress', 'completed'
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id', ondelete='CASCADE'), nullable=True)
    
    # Relationship to task_items
    task_items = db.relationship('TaskItem', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_items=False):
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'member_id': self.member_id
        }
        
        if include_items:
            result['task_items'] = [item.to_dict() for item in self.task_items]
        
        return result
    
    def __repr__(self):
        return f'<Task {self.title}>'
