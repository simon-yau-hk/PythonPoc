"""
Simple tests for Flask API
"""

import unittest
import json
from app import app, db
from models.user_model import User
from models.task_model import Task

class FlaskAPITestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.drop_all()
    
    def test_hello_world(self):
        """Test hello world endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_create_user(self):
        """Test user creation"""
        user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'nickname': 'testuser'
        }
        response = self.app.post('/api/users/', 
                               data=json.dumps(user_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['name'], 'Test User')
    
    def test_get_users(self):
        """Test getting all users"""
        response = self.app.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)

if __name__ == '__main__':
    unittest.main()
