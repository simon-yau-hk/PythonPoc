"""
Test database connection script
Run this to verify your Flask app can connect to the database
"""

from dotenv import load_dotenv
load_dotenv()  # Load .env file before importing app

from app import app, db
from models.member_model import Member
from models.task_model import Task
from models.task_item_model import TaskItem

def test_connection():
    """Test database connection and query existing data"""
    
    print("\n" + "="*60)
    print("Testing Flask Database Connection")
    print("="*60 + "\n")
    
    try:
        with app.app_context():
            # Test connection
            print("✓ Database connection successful!")
            print(f"  Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Test querying members
            print("\n--- Testing Members Table ---")
            members = Member.query.limit(5).all()
            print(f"✓ Found {Member.query.count()} members in database")
            if members:
                print(f"  Sample member: {members[0].username} ({members[0].email})")
            
            # Test querying tasks
            print("\n--- Testing Tasks Table ---")
            tasks = Task.query.limit(5).all()
            print(f"✓ Found {Task.query.count()} tasks in database")
            if tasks:
                print(f"  Sample task: {tasks[0].title} (Priority: {tasks[0].priority})")
            
            # Test querying task items
            print("\n--- Testing Task Items Table ---")
            items = TaskItem.query.limit(5).all()
            print(f"✓ Found {TaskItem.query.count()} task items in database")
            if items:
                print(f"  Sample item: {items[0].title} (Completed: {items[0].is_completed})")
            
            # Test relationships
            print("\n--- Testing Relationships ---")
            if members and tasks:
                member_with_tasks = Member.query.filter(Member.tasks.any()).first()
                if member_with_tasks:
                    print(f"✓ Member '{member_with_tasks.username}' has {len(member_with_tasks.tasks)} tasks")
            
            if tasks and items:
                task_with_items = Task.query.filter(Task.task_items.any()).first()
                if task_with_items:
                    print(f"✓ Task '{task_with_items.title}' has {len(task_with_items.task_items)} items")
            
            print("\n" + "="*60)
            print("✅ All tests passed! Database connection working.")
            print("="*60 + "\n")
            
    except Exception as e:
        print("\n" + "="*60)
        print("❌ Error connecting to database!")
        print("="*60)
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your .env file has correct DATABASE_URL")
        print("2. Verify MySQL server is running")
        print("3. Confirm database and tables exist")
        print("4. Check username/password are correct")
        print("\nSee DATABASE_SETUP.md for more help.\n")
        return False
    
    return True

if __name__ == '__main__':
    test_connection()

