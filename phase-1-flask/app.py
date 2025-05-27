from flask import Flask, request, jsonify
from database import db, Task, Tag
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

def parse_date(date_str):
    """Parse date string in format YYYY-MM-DD"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False)
    )
    
    # Handle tags if provided
    if 'tags' in data:
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            task.tags.append(tag)
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Get filter parameters
    completed = request.args.get('completed')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    tags = request.args.getlist('tags')  # Get multiple tags
    
    # Start with base query
    query = Task.query
    
    # Apply completion filter
    if completed is not None:
        completed_bool = completed.lower() == 'true'
        query = query.filter(Task.completed == completed_bool)
    
    # Apply date filters
    if start_date:
        start = parse_date(start_date)
        if start:
            query = query.filter(Task.created_at >= start)
    
    if end_date:
        end = parse_date(end_date)
        if end:
            # Add one day to include the end date
            end = end + timedelta(days=1)
            query = query.filter(Task.created_at < end)
    
    # Apply tag filters
    if tags:
        for tag_name in tags:
            query = query.filter(Task.tags.any(Tag.name == tag_name))
    
    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    
    # Update tags if provided
    if 'tags' in data:
        task.tags = []
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            task.tags.append(tag)
    
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def mark_complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>/incomplete', methods=['PUT'])
def mark_incomplete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = False
    db.session.commit()
    return jsonify(task.to_dict())

# Tag management endpoints
@app.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([tag.to_dict() for tag in tags])

@app.route('/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Tag name is required'}), 400
    
    tag = Tag.query.filter_by(name=data['name']).first()
    if tag:
        return jsonify({'error': 'Tag already exists'}), 400
    
    tag = Tag(name=data['name'])
    db.session.add(tag)
    db.session.commit()
    
    return jsonify(tag.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
