# Task List

## One-time Setup

Create a virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ # You're in activated virtual environment!
```

Install dependencies (we've already gathered them all into a `requirements.txt` file):

```bash
(venv) $ pip install -r requirements.txt
```

Set up your database using psql.

Create two databases:

1. A development database named `task_list_development`
1. A test database 


Setup your `.env` file:

(Feel free to copy mine, but here's an explanation:)

```
FLASK_ENV=development

SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/task_list_flask

SQLALCHEMY_TEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/test_task_list_flask

SLACK_BOT_TOKEN = xoxb-15
```

1. `FLASK_ENV` as `development` enables hot-reloading
1. `SQLALCHEMY_DATABASE_URI` we'll use this when we need to tell SQLAlchemy where the database is
    - The `postgresql+` bit is just random stuff I copied/pasted from the internet, I have no idea how much is needed, but I know it's compatible with Heroku deployment ;)
    - In the curriculum, we'll direct students to make a postgres user named `postgres` soooo probably keep that
    - **Replace this if you want**: `task_list_flask` is the name of the database I put. It's more likely that the best name for this is `task_list_development` (tho this overrides the rails db)
1. `SQLALCHEMY_TEST_DATABASE_URI` we'll use this as test db
    - As of right now, I don't know why my project breaks with this
1. `SLACK_BOT_TOKEN` what's uuuuppp. Message me for me, but instructions are in the relevant wave, too

## Simon's Debugging Tips

When in doubt:

- Restart the server
  - Seriously
  - I probably do this every third change. The hot-reloading kinda sucks (better than nothing)
- You can safely run `flask db migrate` and `flask db upgrade` as many times as you'd like
  - `migrate` says "make migrations if you detect a need for new ones"
  - `upgrade` says "do the migrations"
- Don't forget to debug with the logs from the Flask server!!! They will be your friend!!!!!!
- VS Code Flask debugging ain't bad.
  1. close other server
  1. click on buggy play button on the left
  1. make a new config: top left corner with play button + dropdown, click "Add Configuration" and select "Python: Flask"
  1. Then click the green play button up there whenever u want
  1. The controls are in the top right corner, so press the stop button (red square) whenever. Press green play to re-run.
  1. Breakpoints work!! so you'll have to switch between Postman and vscode a bunch

## Wave 1: CRUD on Task model

In `app/routes.py`, make these routes, assuming this Blueprint (this blueprint should probably be renamed? Looking for better names):

```python
# Put this line at the top of routes.py, after the imports. This is what defines the "Blueprint", which is an object that will organize all of the routes. (The name in the decorator comes from here)
task_page = Blueprint('task_page', __name__)
```

### Test Home Route

Make this route for a sanity check, and replace the values of `"name"` and `"message"` with your own name and message.

```python
@task_page.route('/')
def index():
    return {
        "name": "Simon Del Rosario",
        "message": "Hi instructors! :)"
    }
```

Run `(venv) $ flask run` to get this going!!

Keep reading in [the Wave 01 doc](wave_01.md)

## Wave 2: Sort by title on Task List

[Wave 02 doc](wave_02.md)

## Wave : Complete a Task

[Wave 03 doc](complete_task.md)

## Wave : Completing a Task Notification

[Wave 04 doc](slack_notification.md)

## Wave : CRUD on Goal model

[Wave 05 doc](goal_crud.md)

## Wave : Goals and Tasks

[Wave 06 doc](goals_and_tasks.md)

## Wave : Deploy

Deploying an API on heroku using postgres is reliably straightforward.

## TODO

- Tests
- Confirm the Blueprint strategy (just `task_page`? Add path prefix? etc)
- Make a guide for how to read the setup/config files
- Spec out the Marshmallow refactor
- Figure out if there's room for many-to-many with Tags
- Probably add "filter by completion" somewhere
