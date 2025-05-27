import requests
import json
from datetime import datetime

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

def test_create_task():
    """Test creating a new task"""
    print("\n1. Testing Create Task (POST /tasks)")
    
    # Test data
    task_data = {
        "title": "Learn Flask API Testing",
        "description": "Practice testing REST APIs with Python requests",
        "completed": False
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    print_response(response)
    return response.json()['id'] if response.status_code == 201 else None

def test_get_all_tasks():
    """Test getting all tasks"""
    print("\n2. Testing Get All Tasks (GET /tasks)")
    response = requests.get(f"{BASE_URL}/tasks")
    print_response(response)

def test_get_single_task(task_id):
    """Test getting a single task"""
    print(f"\n3. Testing Get Single Task (GET /tasks/{task_id})")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print_response(response)

def test_update_task(task_id):
    """Test updating a task"""
    print(f"\n4. Testing Update Task (PUT /tasks/{task_id})")
    
    update_data = {
        "title": "Updated: Learn Flask API Testing",
        "description": "Updated: Practice testing REST APIs with Python requests",
        "completed": True
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    print_response(response)

def test_mark_task_incomplete(task_id):
    """Test marking a task as incomplete"""
    print(f"\n5. Testing Mark Task Incomplete (PUT /tasks/{task_id}/incomplete)")
    response = requests.put(f"{BASE_URL}/tasks/{task_id}/incomplete")
    print_response(response)

def test_mark_task_complete(task_id):
    """Test marking a task as complete"""
    print(f"\n6. Testing Mark Task Complete (PUT /tasks/{task_id}/complete)")
    response = requests.put(f"{BASE_URL}/tasks/{task_id}/complete")
    print_response(response)

def test_delete_task(task_id):
    """Test deleting a task"""
    print(f"\n7. Testing Delete Task (DELETE /tasks/{task_id})")
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print_response(response)

def test_invalid_task():
    """Test getting a non-existent task"""
    print("\n8. Testing Invalid Task (GET /tasks/99999)")
    response = requests.get(f"{BASE_URL}/tasks/99999")
    print_response(response)

def test_create_invalid_task():
    """Test creating a task with invalid data"""
    print("\n9. Testing Create Invalid Task (POST /tasks)")
    invalid_data = {
        "description": "This should fail because title is missing"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=invalid_data)
    print_response(response)

def main():
    print("Starting API Tests...")
    print("=" * 50)
    
    # Run all tests
    task_id = test_create_task()
    if task_id:
        test_get_all_tasks()
        test_get_single_task(task_id)
        test_update_task(task_id)
        test_mark_task_incomplete(task_id)
        test_mark_task_complete(task_id)
        test_delete_task(task_id)
    
    # Test error cases
    test_invalid_task()
    test_create_invalid_task()
    
    print("\nAPI Testing Complete!")

if __name__ == "__main__":
    main() 