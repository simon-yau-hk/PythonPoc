"""
Demonstration of SQLAlchemy Eager Loading vs Lazy Loading
Shows the performance difference between the two approaches
"""

from dotenv import load_dotenv
load_dotenv()

from app import app, db
from models.member_model import Member
from models.task_model import Task
from models.task_item_model import TaskItem
from sqlalchemy.orm import joinedload
import time

def demo_lazy_loading():
    """Demonstrate lazy loading (N+1 query problem)"""
    print("\n" + "="*60)
    print("🐌 LAZY LOADING DEMO (N+1 Query Problem)")
    print("="*60)
    
    start_time = time.time()
    
    with app.app_context():
        # This will trigger multiple queries
        members = Member.query.all()
        
        print(f"📊 Found {len(members)} members")
        
        total_tasks = 0
        total_items = 0
        
        for member in members:
            # Each access to member.tasks triggers a new query!
            tasks = member.tasks  # Query #2, #3, #4, etc.
            total_tasks += len(tasks)
            
            for task in tasks:
                # Each access to task.task_items triggers another query!
                items = task.task_items  # Query #5, #6, #7, etc.
                total_items += len(items)
        
        end_time = time.time()
        
        print(f"📋 Total tasks: {total_tasks}")
        print(f"📝 Total task items: {total_items}")
        print(f"⏱️  Time taken: {end_time - start_time:.4f} seconds")
        print(f"🔍 Queries executed: 1 + {len(members)} + {total_tasks} = {1 + len(members) + total_tasks} queries")

def demo_eager_loading():
    """Demonstrate eager loading (single query)"""
    print("\n" + "="*60)
    print("🚀 EAGER LOADING DEMO (Single Query)")
    print("="*60)
    
    start_time = time.time()
    
    with app.app_context():
        # This loads everything in a single query with JOINs
        members = Member.query.options(
            joinedload(Member.tasks).joinedload(Task.task_items)
        ).all()
        
        print(f"📊 Found {len(members)} members")
        
        total_tasks = 0
        total_items = 0
        
        for member in members:
            # No additional queries - data already loaded!
            tasks = member.tasks  # No query - already in memory
            total_tasks += len(tasks)
            
            for task in tasks:
                # No additional queries - data already loaded!
                items = task.task_items  # No query - already in memory
                total_items += len(items)
        
        end_time = time.time()
        
        print(f"📋 Total tasks: {total_tasks}")
        print(f"📝 Total task items: {total_items}")
        print(f"⏱️  Time taken: {end_time - start_time:.4f} seconds")
        print(f"🔍 Queries executed: 1 query (with JOINs)")

def demo_sql_query_comparison():
    """Show the actual SQL queries generated"""
    print("\n" + "="*60)
    print("🔍 SQL QUERY COMPARISON")
    print("="*60)
    
    with app.app_context():
        print("\n🐌 LAZY LOADING SQL QUERIES:")
        print("1. SELECT * FROM members")
        print("2. SELECT * FROM tasks WHERE member_id = 1")
        print("3. SELECT * FROM tasks WHERE member_id = 2")
        print("4. SELECT * FROM tasks WHERE member_id = 3")
        print("5. SELECT * FROM task_items WHERE task_id = 1")
        print("6. SELECT * FROM task_items WHERE task_id = 2")
        print("7. SELECT * FROM task_items WHERE task_id = 3")
        print("... and so on (N+1 problem)")
        
        print("\n🚀 EAGER LOADING SQL QUERY:")
        print("1. SELECT members.*, tasks.*, task_items.*")
        print("   FROM members")
        print("   LEFT JOIN tasks ON members.id = tasks.member_id")
        print("   LEFT JOIN task_items ON tasks.id = task_items.task_id")
        print("   ORDER BY members.id, tasks.id, task_items.id")
        
        print("\n💡 BENEFITS OF EAGER LOADING:")
        print("✅ Single database round-trip")
        print("✅ Better performance")
        print("✅ Reduced database load")
        print("✅ No N+1 query problem")
        print("✅ All data loaded at once")

def demo_relationship_access():
    """Demonstrate how relationships work with eager loading"""
    print("\n" + "="*60)
    print("🔗 RELATIONSHIP ACCESS DEMO")
    print("="*60)
    
    with app.app_context():
        # Get one member with all relationships loaded
        member = Member.query.options(
            joinedload(Member.tasks).joinedload(Task.task_items)
        ).first()
        
        if member:
            print(f"👤 Member: {member.username}")
            print(f"📧 Email: {member.email}")
            print(f"📋 Tasks: {len(member.tasks)}")
            
            for i, task in enumerate(member.tasks, 1):
                print(f"   📝 Task {i}: {task.title}")
                print(f"      Status: {task.status}")
                print(f"      Priority: {task.priority}")
                print(f"      📋 Items: {len(task.task_items)}")
                
                for j, item in enumerate(task.task_items, 1):
                    status = "✅" if item.is_completed else "⏳"
                    print(f"         {status} Item {j}: {item.title}")
        else:
            print("❌ No members found in database")

if __name__ == '__main__':
    print("🎯 SQLAlchemy Eager Loading vs Lazy Loading Demo")
    print("This demonstrates the power of proper relationship loading!")
    
    try:
        demo_lazy_loading()
        demo_eager_loading()
        demo_sql_query_comparison()
        demo_relationship_access()
        
        print("\n" + "="*60)
        print("🎉 DEMO COMPLETE!")
        print("="*60)
        print("💡 Key Takeaway: Use eager loading with joinedload()")
        print("   to avoid N+1 query problems and improve performance!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure your Flask app is configured and database is accessible.")
