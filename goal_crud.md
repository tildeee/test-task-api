# Wave 5: Goal CRUD

Tasks can be in service of one goal

A goal can have many tasks

## Structure

1. Define Goal model
1. Set relationship in Task table
1. Route Walkthrough
1. Answers at the bottom

## Define Goal Model

Goals should have a `goal_id`, a `title`, and `tasks`

In `models.py`, above the `Task` def:

```python
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
```

Hints:

- `title` is type String
- `tasks` should be set to the magical SQLAlchemy relationship stuff
- `tasks = db.relationship(...)` sets the relationship:
  - The first positional argument is a string of the name of the other model, `'Task'`
  - The keyword argument `backref` is the thing that says `goal.tasks` will work! We should set it to `"tasks"`, so `backref='tasks'`

That's it!

## Set Relationship in Task Table

A task can only belong to one Goal. Goals are optional for tasks.

Add a new column `goal_id` for the Task model, which should be a foreign key to a Goal's id

Hints:

- Follow the column patterns from the other columns
- The first positional argument is `db.Integer`
- The second positional arg designates how the FK relationship works. We'll use `db.ForeignKey('goal.goal_id')`, where `goal.goal_id` is the name of the column we need (sql easily supports `goal.` to namespace tables i think)
- We want this column to be nullable, so `nullable=True`

## Migrate

Here's your reminder to migrate and upgrade

## Route Walkthrough

I won't actually get into the details of the CRUD of Goal. It's not different from Tasks or special.

## Simon's `models.py` File at this Point

```python
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='tasks', lazy=True)


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'
```