"""
Database configuration for Flask API
Separates database initialization from app.py to avoid circular imports
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()