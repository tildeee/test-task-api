# Wave 1: Getting All Tasks, Creating a Task

## Structure

1. Goal requests/responses
1. Task model requirements (and walkthrough)
1. Writing our routes walkthrough
1. Postman walkthrough
1. Random Simon notes
1. Rest of CRUD hints

## Goal

Essentially filling this route stub, which will require setting up the DB and table, defining the `Task` model, and learning how to manually test with Postman

```python
@task_page.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        return {}
    elif request.method == 'POST':
        return {}
```

### `GET /tasks`

Gets a list of tasks and some end-user-relevant data.

No expected request body

Expected Response:

```json
[
  {
    "description": "Test Description",
    "id": 3,
    "is_complete": false,
    "title": "Test Title"
  },
  {
    "description": "Test Description",
    "id": 4,
    "is_complete": true,
    "title": "Another Test Title"
  }
]
```

Aka a JSON array of objects, where each object has the keys `id`, `description`, `is_complete`, `title`

- Empty array with no tasks

### `POST /tasks`

Creates a task.

Expected request body (see below Postman walkthrough):

```json
{
  "title": "c",
  "description": "Test Description",
  "completed_at": null
}
```

- Title is required
- Description is not required
- Completed at is `null`. I'm justifying this by saying that a form might explicitly send this.

Expected Response:

```json
{
  "task": {
    "description": "Test Description",
    "id": 7,
    "is_complete": false,
    "title": "c"
  }
}
```

Notes about `is_complete` in the CRUD section

## Task Model Requirements and Walkthrough

### Setup DB for the first time

For some reason, I needed to manually create my DB AND tables in `psql`. Idk why. I'm gonna write the directions for setting up the DB, and experiment with y'all by setting up the Model, then seeing if migrating works as expected.

Open up PSQL and make the database you're looking for. Using the DB name I specified in `.env`:

```sql
(venv) $ psql -U postgres

\l

CREATE DATABASE task_list_flask;

\l

\quit
```

### Write the Model definition

Now go to `app/models.py` and fill out this:

```python
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'
```

Do **not** add `__tablename__` (which most tutorials tell you to do. I wanna experiment and see if SQLAlchemy does good stuff with this.)

Add these columns (follow the pattern of `task_id`, `created_on`, `updated_on`):

- `title`, which is a String
- `description`, which is a String
- `completed_at`, which is a DateTime, and `nullable=True` (kwarg)

Or copy/paste mine:

```python
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'
```

Syntax explanation:

What's up with the `db.`?

- `db` is a SQLAlchemy-big-ole-db-object-thing that gets defined in `app/__init__.py`
- `__init__.py` is a special file in Python that says "Hey this folder is a package and you should look for files here like this is a package." It's why we can say `from app import db` (bc `__init__` is inside the `app` folder)
- `db` is defined on line 6: `db = SQLAlchemy()`, and configured in the `create_app` function (which gets called automatically from `app.py`)
- SQLAlchemy has defined all the cool Column stuff and column types, so that's why we access it off `db`

A bunch of tutorials recommend having a constructor in the model. I personally don't think it's necessary.

The `__repr__` is essentially the class's toString() method that we're overriding

### Migrate!

Run the following commands in this order:

1. `flask db init` (Only need to do this once successfully)
1. `flask db migrate`
1. `flask db upgrade`

Let's verify using Postman.

## Routes Walkthrough

Starting with this:

```python
@task_page.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        return {}
    elif request.method == 'POST':
        return {}
```

Hints for GET:

- You can get a list of all Task objects with SQLAlchemy: `Task.query.all()`
- You want to return a JSON array. You can jsonify any Python list with `jsonify(results)`
  - Build the result list in Python
  - Note that the structure of each Task object has non-obvious keys

Hints for POST:

- You get request body data using `request.get_json()`
  - `request` is a Flask object that represents each request
  - Using `.get_json()` is the best way to get the data in a Python form
- After creating an instance of a Task, add the following lines. You'll want something like these lines (specifically the `commit()`) to ever save anything
  - `db.session.add(new_task)`
  - `db.session.commit()`
- You don't need to jsonify a Python dictionary when you return it, I guess.
- I made helper methods
- When making a new `Task`, I only use keyword argument syntax

### Postman Walkthrough

Reminder: When debugging Postman, rely on the Postman console and the logs from the Flask server

1. Ensure server is running
1. Open Postman

POST Request configuration:

1. Configure `POST` to `localhost:5000/tasks`
1. Do not configure any "Params"
1. Go to "Body" tab
1. Select "raw" radio button
1. Select "JSON" in the dropdown to the right of it. My API really doesn't work if this isn't set
1. Paste this, or anything like this, into the textbox

```json
{
  "title": "Test Title",
  "description": "Test Description"
}
```

GET Request configuration:

1. Configure `GET` to `localhost:5000/tasks`
1. Technically you should remove all params/body. Do this by either method:
   - Create a new request tab in Postman (cmd+t or the + button in the request-tab-zone)
   - Unchecking each param in params, and selecting "none" in the body (the raw still gets preserved)

---

## Unformatted Simon notes:

REALLY IMPORTANT to not have trailing slash
SHOULD BE `/tasks`
not `/tasks/`
it gets to a weird spot in the browser if you leave it, and it gets sticky. debug with incognito or clearing cache

I suddenly started getting db errors after i started running `flask db upgrade`, which is weird, but whatever. Here's how I fixed it `$ pip install psycopg2`

route questions? use this python code

```python
print(app.url_map)
```

If it says you have no table `tasks`, add into your model `__tablename__ = 'tasks'` (as a class variable), and run `flask db migrate` and `flask db upgrade`

I personally had to make a `tasks` table using PSQL. Here was my SQL:

```sql
\c task_list_flask

CREATE TABLE tasks (task_id INT PRIMARY KEY, title VARCHAR(200), description VARCHAR(200), completed_at DATETIME);
```

Don't forget to `flask migrate` and `upgrade` any time you change the columns

---

## Rest of CRUD Hints

```python
@task_page.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
```

Assuming Task is found, here are the expected responses:

`GET /tasks/3`

No request body, no params

```json
{
  "task": {
    "description": "Test Description",
    "id": 3,
    "is_complete": true,
    "title": "Test Title"
  }
}
```

Note that `is_complete` is a boolean. If the task has a `completed_at` date, it's true.

`PUT /tasks/3`

Request body (no params):

```json
{
  "title": "Edited Title",
  "description": "Edited Description",
  "completed_at": null
}
```

Response:

```json
{
  "task": {
    "description": "Edited Description",
    "id": 3,
    "is_complete": false,
    "title": "Edited Title"
  }
}
```

`DELETE /tasks/3`

No request body, no params

Response:

```json
{
  "details": "Task 3 \"Edited Title\" successfully deleted"
}
```
