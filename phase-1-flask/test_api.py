import requests
import json
from datetime import datetime, timedelta

# Base URL for our API
BASE_URL = 'http://localhost:5000'

def print_response(response):
    """Helper function to print response details"""
    print(f"\nStatus Code: {response.status_code}")
    try:
        print("Response Body:", json.dumps(response.json(), indent=2))
    except:
        print("Response Body:", response.text)
    print("-" * 50)

def test_create_task(title, description, completed, tags=None):
    """Test creating a new task"""
    print("\n1. Testing Create Task (POST /tasks)")
    
    # Test data
    task_data = {
        "title": title,
        "description": description,
        "completed": completed
    }
    
    if tags:
        task_data["tags"] = tags
    
    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    print_response(response)
    return response.json()['id'] if response.status_code == 201 else None

def test_get_all_tasks():
    """Test getting all tasks"""
    print("\n2. Testing Get All Tasks (GET /tasks)")
    response = requests.get(f"{BASE_URL}/tasks")
    print_response(response)

def test_get_completed_tasks():
    """Test getting only completed tasks"""
    print("\n3. Testing Get Completed Tasks (GET /tasks?completed=true)")
    response = requests.get(f"{BASE_URL}/tasks?completed=true")
    print_response(response)

def test_get_incomplete_tasks():
    """Test getting only incomplete tasks"""
    print("\n4. Testing Get Incomplete Tasks (GET /tasks?completed=false)")
    response = requests.get(f"{BASE_URL}/tasks?completed=false")
    print_response(response)

def test_get_tasks_by_date():
    """Test getting tasks by date range"""
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print("\n5. Testing Get Tasks by Date Range")
    print(f"Date range: {today} to {tomorrow}")
    response = requests.get(f"{BASE_URL}/tasks?start_date={today}&end_date={tomorrow}")
    print_response(response)

def test_get_tasks_by_tags():
    """Test getting tasks by tags"""
    print("\n6. Testing Get Tasks by Tags")
    response = requests.get(f"{BASE_URL}/tasks?tags=urgent&tags=work")
    print_response(response)

def test_get_single_task(task_id):
    """Test getting a single task"""
    print(f"\n7. Testing Get Single Task (GET /tasks/{task_id})")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print_response(response)

def test_update_task(task_id):
    """Test updating a task"""
    print(f"\n8. Testing Update Task (PUT /tasks/{task_id})")
    
    update_data = {
        "title": "Updated: Learn Flask API Testing",
        "description": "Updated: Practice testing REST APIs with Python requests",
        "completed": True,
        "tags": ["updated", "important"]
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    print_response(response)

def test_mark_task_incomplete(task_id):
    """Test marking a task as incomplete"""
    print(f"\n9. Testing Mark Task Incomplete (PUT /tasks/{task_id}/incomplete)")
    response = requests.put(f"{BASE_URL}/tasks/{task_id}/incomplete")
    print_response(response)

def test_mark_task_complete(task_id):
    """Test marking a task as complete"""
    print(f"\n10. Testing Mark Task Complete (PUT /tasks/{task_id}/complete)")
    response = requests.put(f"{BASE_URL}/tasks/{task_id}/complete")
    print_response(response)

def test_delete_task(task_id):
    """Test deleting a task"""
    print(f"\n11. Testing Delete Task (DELETE /tasks/{task_id})")
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print_response(response)

def test_create_tag():
    """Test creating a new tag"""
    print("\n12. Testing Create Tag (POST /tags)")
    tag_data = {"name": "test-tag"}
    response = requests.post(f"{BASE_URL}/tags", json=tag_data)
    print_response(response)

def test_get_tags():
    """Test getting all tags"""
    print("\n13. Testing Get Tags (GET /tags)")
    response = requests.get(f"{BASE_URL}/tags")
    print_response(response)

def test_invalid_task():
    """Test getting a non-existent task"""
    print("\n14. Testing Invalid Task (GET /tasks/99999)")
    response = requests.get(f"{BASE_URL}/tasks/99999")
    print_response(response)

def test_create_invalid_task():
    """Test creating a task with invalid data"""
    print("\n15. Testing Create Invalid Task (POST /tasks)")
    invalid_data = {
        "description": "This should fail because title is missing"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=invalid_data)
    print_response(response)

def main():
    print("Starting API Tests...")
    print("=" * 50)
    
    # Create some tags first
    test_create_tag()
    
    # Run all tests
    task_id = test_create_task(
        title="Learn Flask API Testing",
        description="Practice testing REST APIs with Python requests",
        completed=False,
        tags=["urgent", "work"]
    )
    
    if task_id:
        test_get_all_tasks()
        test_get_completed_tasks()
        test_get_incomplete_tasks()
        test_get_tasks_by_date()
        test_get_tasks_by_tags()
        test_get_single_task(task_id)
        test_update_task(task_id)
        test_mark_task_incomplete(task_id)
        test_mark_task_complete(task_id)
        test_delete_task(task_id)
    
    # Test tag endpoints
    test_get_tags()
    
    # Test error cases
    test_invalid_task()
    test_create_invalid_task()
    
    print("\nAPI Testing Complete!")

if __name__ == "__main__":
    main() 