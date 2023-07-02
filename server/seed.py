from faker import Faker
from werkzeug.security import generate_password_hash
from app import app, db, Task, User  # Make sure to import app

fake = Faker()


# Generate fake tasks
def generate_fake_tasks(num_tasks):
    tasks = []
    for _ in range(num_tasks):
        task = Task(
            title=fake.catch_phrase(),
            description=fake.text(),
            due_date=fake.date_between(start_date='-30d', end_date='+30d'),
            priority=fake.random_element(elements=('Low', 'Medium', 'High')),
            category=fake.random_element(elements=('Work', 'Personal', 'Study')),
            user_id=1
        )
        tasks.append(task)
    return tasks

# Generate a fake user
def generate_fake_user():
    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email()
    )
    user.set_password(fake.password(length=10))
    return user

# Seed the database
def seed():
    # Drop existing tables (optional)
    db.drop_all()

    # Create tables
    db.create_all()

    # Create a fake user
    user = generate_fake_user()
    db.session.add(user)
    db.session.commit()

    # Generate fake tasks
    tasks = generate_fake_tasks(num_tasks=10)

    # Add tasks to the database
    for task in tasks:
        db.session.add(task)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():  # Create an application context
        seed()