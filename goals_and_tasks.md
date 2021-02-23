# Wave 6: Goals and Tasks

We want two routes:

1. A route that will get and list all tasks that belong to a specific goal
2. A route that will update a specific goal's tasks to be all the task ids provided
    - Think like rails forms where it always sent an array of ids because there would be multiple checkboxes

Route stub:

```python
@task_page.route('/goals/<goal_id>/tasks', methods=['GET', 'POST'])
def goal_tasks(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == 'GET':
        return {}
    elif request.method == 'POST':
        return {}
```

## `GET /goals/<goal_id>/tasks`

Example response:

```json
{
    "id": 2,
    "tasks": [
        {
            "description": "Test Description",
            "id": 5,
            "is_complete": false,
            "title": "a"
        },
        {
            "description": "Test Description",
            "id": 6,
            "is_complete": false,
            "title": "b"
        },
        {
            "description": "Test Description",
            "id": 7,
            "is_complete": false,
            "title": "c"
        }
    ],
    "title": "Another Goal"
}
```

Hints:

- You can get a list of a Goal's Tasks objects with `goal.tasks`

## `POST /goals/<goal_id>/tasks`

Example request:

```json
{
    "task_ids": [5, 6, 7]
}
```

Example response:

```json
{
    "id": 2,
    "task_ids": [
        5,
        6,
        7
    ]
}
```

Hints:

- Recall using `request.get_json()`
- Add a task to a goal with `goal.tasks.append(task)`
    - I haven't gotten `task.goal = goal` to work
- Don't forget to `db.session.commit()`

## Revisit `GET /tasks/<task_id>`

A task with a goal set should respond like this:

```json
{
    "task": {
        "description": "Test Description",
        "goal_id": 3,
        "id": 7,
        "is_complete": false,
        "title": "c"
    }
}
```

A task without a goal should still respond like this:

```json
{
    "task": {
        "description": "Test Description",
        "id": 5,
        "is_complete": false,
        "title": "a"
    }
}
```
