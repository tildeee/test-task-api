```
$ pip install python-dotenv
flask_sqlalchemy
flask_migrate
```

.env

```
FLASK_ENV=development

SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/task_list_flask
```

Run with

```
$ export FLASK_ENV=development
$ flask run
```

Make first route

REALLY IMPORTANT to not have trailing slash
SHOULD BE `/tasks`
not `/tasks/`
it gets to a weird spot in the browser if you leave it, and it gets sticky. debug with incognito or clearing cache

Make model
(import and install SQLAlchemy, migrate)
Migrate enables `flask db upgrade`

Open up PSQL and make the database you're looking for
With what I have in the .env:

```
psql -U postgres

\l

CREATE DATABASE task_list_flask;

\l

\quit
```

Run `flask db init`
Run `flask db migrate`
Run `flask db upgrade` after

This happened in the middle after i started running `flask db upgrade`, which is weird, but whatever. Still do it

```
$ pip install psycopg2
```

Do this after models.

```
db.create_all()
db.session.commit()
```

This style (and not in `create_app()`) is that we don't need a context.

MAKING A POST REQUEST FROM POSTMAN:

POST localhost:5000/tasks

no params
go to body
raw
select "JSON" in dropdown next to it

```json
{
  "hello": "wofrld"
}
```

DEBUGGING:

restart server
run flask migrate
run flask upgrade

route questions?

```python
print(app.url_map)
```

The create_all() method only creates table if it doesn't already exist in the database. So you can run it safely multiple times. In addition to that, the create_all() method doesn't take account of the modifications made to the models while creating tables.

i had to flask migrate after adding some columns?

---

# tests

for some reason, hardcoding/string literal the test database url was the only way it worked. couldn't find it as an env var

for some reason, i needed to manually create the tasks table and all of the columns. after that it was great


---

wave:

CRUD on tasks

wave:

complete tasks

wave:

when completing tasks, posts a notice to Slack API

Theoretically, we could really all use the same Slack bot


---



MAKING SLACK BOT INSTRUCTIONS. Point is to get a slack bot created, has the right permissions, authorized in the workspace, and get the bot token

https://api.slack.com/

Go to "Your Apps"/sign in. You can always go back to the "Your apps" page on the top right.

Pick a workspace

Make a new app. Fill out:
1. App name
1. Development slack workspace

brings you to a new page. 

Add features and functionality:

1. click permissions
1. Scroll down to bot token scopes. Add chat:write and chat:write.public
1. Scroll back up: "install to workspace" is enabled. click that button.
1. Brings you to the authorization page that says "hey hUMAN, ARE YOU GOOD WITH THIS?" Say yes. check out the permissions
1. After you say yes, it should list in "OAuth Tokens for your team" and "Bot User OAuth Access Token". That value is your bot token. Should always start with `xoxb`
1. Copy the token. Whenever you want to get back here, go to "Your apps" (top right), click your app, open "features and functionality", go to "OAuth & Permissions"

Verify

1. Go to test https://api.slack.com/methods/chat.postMessage/test (if you click on the tab "Documentation", it will show you all the documentation)
1. Fill out the following params:
  - token: paste in your bot token
  - channel: use "test"
  - text: type a nice message for everyone to read
1. Hit Test Method button
1. Scroll down to see the response
  - admire the URL + header it's giving you


Verify AGAIN

1. open postman
1. make a new request
  - open new tab
  - change method to POST
  - use this as request URL `https://slack.com/api/chat.postMessage`
  - in "Params", fill the following values:
    - channel: "test"
    - text: "asdfsdf"
  - go to "Headers" and add this new key value pair
    - Authorization: "Bearer xoxb-150"
    - NB: Instead of this, you COULD put in a param of token: token. It works. Better to do this method tho


NOW ADD TO FLASK

import requests

Requests module
https://requests.readthedocs.io/en/master/user/quickstart/


```python
@task_page.route('/')
def index():
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        'Authorization': 'Bearer xoxb-15'
    }
    payload = {
        "channel": "secret-simon",
        "text": "hello world from flask"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.json()
```


when debugging postman, debug with logs from flask server

-----

wave

add goal model

DECLARING MODELS
optional in Flask-SQLAlchemy. For instance the table name is automatically set for you unless overridden. It’s derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case”. To override the table name, set the `__tablename__` class attribute.

don't need `__tablename__`

one goal has many addresses

Make goal model

`backref` is a simple way to also declare a new property on the Address class. You can then also use my_address.person to get to the person at that address.

update Task to have goal_id

```
goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),
      nullable=False)
```


WHEN RUNNING FLASK DB MIGRATE, FLASK DB UPGRADE
Alembic will always post "INFO" messages, which doesn't really matter, it's just info, not a warning
you can change this with changing alembic config


Goals:

CRUD

don't forget to import Goal ;)

everything you need to know about models with sql_alchemy
how to make models and their relationships:
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

what we can do with models:
https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/

To see every kind of query we can make, go here
https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery
(We want the header for BaseQuery)


sqlalchemy composition stuff. use append and kwargs with model objs

```python
a = Address(email='foo@bar.com')
p = Person(name='foo')
p.addresses.append(a)
```

look we can do .addresses.count(), .addresses[], .addresses.filter_by()
```python
db.session.add(p)
db.session.add(a)
db.session.commit()
print p.addresses.count() # 1
print p.addresses[0] # <Address object at 0x10c098ed0>
print p.addresses.filter_by(email='foo@bar.com').count() # 1
```


NEW ROUTE:


POST
`/goals/<goal_id>/tasks`

request body:

```json
{
  "task_ids": []
}
```

