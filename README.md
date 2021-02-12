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