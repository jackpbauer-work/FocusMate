from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Task, User
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate email
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        return jsonify({'message': 'Invalid email.'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered.'}), 400
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        # Ideally, you should return a JWT token or similar here, but for simplicity:
        return jsonify({'message': 'Login successful', 'user': user.name}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 400
    
# API Endpoints
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime('%Y-%m-%d'),
            'priority': task.priority,
            'category': task.category,
            'user_id': task.user_id
        })
    return jsonify(task_list)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data['description'],
        due_date=data['due_date'],
        priority=data['priority'],
        category=data['category'],
        user_id=data['user_id']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=3005)
