"""
Simple run script for Flask API
Alternative to running 'python app.py'
"""

from app import app, db

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the Flask application
    print("\n" + "="*50)
    print("Flask API is starting...")
    print("="*50)
    print(f"Server running at: http://localhost:5000")
    print(f"API Endpoints:")
    print(f"  - GET  http://localhost:5000/")
    print(f"  - GET  http://localhost:5000/health")
    print(f"  - GET  http://localhost:5000/api/users/")
    print(f"  - POST http://localhost:5000/api/users/")
    print(f"  - GET  http://localhost:5000/api/tasks/")
    print(f"  - POST http://localhost:5000/api/tasks/")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

