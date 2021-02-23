# Wave 03: Complete a Task

Make a route to toggle completion for a task:

- If the task does not have a completed_at date, set one
- Otherwise, set it to `None`

Route stub:

```python
@task_page.route('/tasks/<task_id>/complete', methods=['PATCH'])
def toggle_complete(task_id):
    task = Task.query.get_or_404(task_id)
    return {}
```

## `PATCH /tasks/<task_id>/complete`

Expected response if the task is incomplete

```json
{
  "task": {
    "description": "Test Description",
    "id": 4,
    "is_complete": true,
    "title": "Test Title"
  }
}
```

Expected response if the task is already complete

```json
{
  "task": {
    "description": "Test Description",
    "id": 4,
    "is_complete": false,
    "title": "Test Title"
  }
}
```

Hints:

- Use `task.completed_at`
- Get current datetime with `datetime.utcnow()`
  - `datetime` needs to be imported
- Don't forget to `db.session.commit()`
