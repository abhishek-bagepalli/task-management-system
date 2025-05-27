# Flask Task Manager API

A simple Flask-based REST API for managing tasks with SQLite database.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### Tasks

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
  - Required fields: `title`
  - Optional fields: `description`, `completed`
- `GET /tasks/<task_id>` - Get a specific task
- `PUT /tasks/<task_id>` - Update a task
- `DELETE /tasks/<task_id>` - Delete a task
- `PUT /tasks/<task_id>/complete` - Mark a task as complete
- `PUT /tasks/<task_id>/incomplete` - Mark a task as incomplete

## Example Usage

Create a new task:
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

Get all tasks:
```bash
curl http://localhost:5000/tasks
```

Mark a task as complete:
```bash
curl -X PUT http://localhost:5000/tasks/1/complete
``` 