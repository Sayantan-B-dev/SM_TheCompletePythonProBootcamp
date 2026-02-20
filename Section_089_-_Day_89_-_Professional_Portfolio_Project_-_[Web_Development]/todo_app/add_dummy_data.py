# add_dummy_data.py
import random
import datetime
from app import app
from models import db, Project, Task

# Sample data pools
PROJECT_NAMES = [
    "Work", "Personal", "Shopping", "Fitness", "Study", "Home Improvement",
    "Travel Plans", "Book Ideas", "Recipes", "Garden", "Finance", "Gifts"
]

TASK_TEMPLATES = [
    "Write report", "Buy groceries", "Call mom", "Pay bills", "Schedule meeting",
    "Clean desk", "Review pull request", "Plan weekend", "Water plants", "Read chapter",
    "Update resume", "Book flight", "Buy gift", "Prepare presentation", "Fix bug",
    "Organize files", "Go for a run", "Meditate", "Call friend", "Research topic"
]

STATUSES = ['todo', 'doing', 'done']
PRIORITIES = ['low', 'medium', 'high']

def random_date(start, end):
    """Return a random datetime between two datetime objects."""
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    return start + datetime.timedelta(days=random_days, seconds=random_seconds)

def create_dummy_data():
    print("🌱 Creating dummy projects and tasks with varied creation dates...")

    # Optional: clear existing data (uncomment if you want to start fresh)
    # print("🧹 Clearing existing data...")
    # Task.query.delete()
    # Project.query.delete()
    # db.session.commit()

    # Create projects
    projects = []
    for name in random.sample(PROJECT_NAMES, k=random.randint(3, 6)):
        project = Project(
            name=name,
            description=f"This is the {name} project. Manage all related tasks here."
        )
        db.session.add(project)
        projects.append(project)
    db.session.commit()
    print(f"✅ Created {len(projects)} projects.")

    # Date range: last 6 months until today
    today = datetime.datetime.utcnow()
    six_months_ago = today - datetime.timedelta(days=180)

    total_tasks = 0
    for project in projects:
        num_tasks = random.randint(5, 12)
        for _ in range(num_tasks):
            # Random title
            title = random.choice(TASK_TEMPLATES)
            if random.random() < 0.3:
                title += f" #{random.randint(1, 99)}"

            # Random creation date within last 6 months
            created_at = random_date(six_months_ago, today)

            # Random due date within ±30 days of creation
            due_date = random_date(
                created_at - datetime.timedelta(days=15),
                created_at + datetime.timedelta(days=30)
            )

            task = Task(
                title=title,
                description=f"Details about {title.lower()}. This is a sample description.",
                status=random.choice(STATUSES),
                priority=random.choice(PRIORITIES),
                due_date=due_date,
                project_id=project.id,
                created_at=created_at  # Explicitly set for varied history
            )
            db.session.add(task)
            total_tasks += 1
        db.session.commit()
        print(f"  ➕ Added {num_tasks} tasks to '{project.name}'")
    print(f"✅ Total tasks created: {total_tasks}")

if __name__ == "__main__":
    with app.app_context():
        create_dummy_data()
    print("🎉 Dummy data injection complete!")