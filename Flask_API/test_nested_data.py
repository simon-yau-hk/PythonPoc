"""
Test script for the new nested data endpoint
Demonstrates how to get all members with their tasks and task details
"""

import requests
import json

def test_members_with_tasks():
    """Test the new endpoint that returns members with tasks and task details"""
    
    print("\n" + "="*70)
    print("Testing Members with Tasks and Task Details")
    print("="*70 + "\n")
    
    try:
        # Test the new endpoint
        url = "http://localhost:5000/api/members/with-tasks"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Success! Got members with tasks and task details")
            print(f"📊 Found {data['count']} members")
            print(f"📝 Message: {data['message']}")
            
            # Display the structure
            if data['data']:
                print(f"\n📋 Sample Data Structure:")
                print(f"   └── {len(data['data'])} members")
                
                for i, member in enumerate(data['data'][:2]):  # Show first 2 members
                    print(f"\n👤 Member {i+1}: {member.get('username', 'N/A')}")
                    print(f"   📧 Email: {member.get('email', 'N/A')}")
                    print(f"   📊 Task Stats: {member.get('task_stats', {})}")
                    print(f"   📝 Tasks: {member.get('task_count', 0)} tasks")
                    
                    # Show tasks for this member
                    tasks = member.get('tasks', [])
                    if tasks:
                        print(f"   📋 Task Details:")
                        for j, task in enumerate(tasks[:2]):  # Show first 2 tasks
                            print(f"      └── Task {j+1}: {task.get('title', 'N/A')}")
                            print(f"         Status: {task.get('status', 'N/A')}")
                            print(f"         Priority: {task.get('priority', 'N/A')}")
                            
                            # Show task items
                            task_items = task.get('task_items', [])
                            if task_items:
                                print(f"         📋 Task Items ({len(task_items)} items):")
                                for k, item in enumerate(task_items[:2]):  # Show first 2 items
                                    status = "✅" if item.get('is_completed') else "⏳"
                                    print(f"            └── {status} {item.get('title', 'N/A')}")
                            else:
                                print(f"         📋 No task items")
                    else:
                        print(f"   📋 No tasks for this member")
            
            print(f"\n🔗 Full API Response Structure:")
            print(f"   ├── success: {data['success']}")
            print(f"   ├── count: {data['count']}")
            print(f"   ├── message: {data['message']}")
            print(f"   └── data: Array of {len(data['data'])} members")
            print(f"       └── Each member contains:")
            print(f"           ├── Member info (id, username, email, etc.)")
            print(f"           ├── tasks: Array of tasks")
            print(f"           │   └── Each task contains:")
            print(f"           │       ├── Task info (title, status, priority, etc.)")
            print(f"           │       └── task_items: Array of task items")
            print(f"           ├── task_count: Number of tasks")
            print(f"           └── task_stats: Statistics (total, completed, pending)")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Flask app is running on http://localhost:5000")
        print("   Run: python app.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_alternative_endpoints():
    """Test other related endpoints"""
    
    print(f"\n" + "="*70)
    print("Testing Alternative Endpoints")
    print("="*70 + "\n")
    
    endpoints = [
        ("Basic members", "http://localhost:5000/api/members/"),
        ("Health check", "http://localhost:5000/health"),
        ("Members with tasks", "http://localhost:5000/api/members/with-tasks"),
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {name}: {url} ({response.status_code})")
        except:
            print(f"❌ {name}: {url} (Connection failed)")

if __name__ == '__main__':
    test_members_with_tasks()
    test_alternative_endpoints()
