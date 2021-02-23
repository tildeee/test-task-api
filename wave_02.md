# Wave 2: Sort by Title on Task List

We should teach query params in a way that is useful. Query params are important!

We want to use query params to designate that we're sorting our tasks. Modify `GET /tasks`.

## Walkthrough

You're probably starting with a route similar to this:

```python
@task_page.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        results = []
        for task in tasks:
            results.append(build_dict_from_task(task))
        return jsonify(results)
    elif request.method == 'POST':
        new_task = build_task_from_json(request.get_json())

        db.session.add(new_task)
        db.session.commit()

        return {"task": build_dict_from_task(new_task)}
```

And we want to be able to make these two requests:

```
localhost:5000/tasks?sort=asc
localhost:5000/tasks?sort=desc
```

It should sort by title.

Hints:

- You get the value of query params using `request.args.get(sort)`
    - If it doesn't exist, it returns `None`
- You can sort things using `order_by`
    - `Task.query.order_by( ... )`
- You can say desc/asc with some methods that the model provides:
    - `Task.title.desc()`
    - `Task.title.asc()`


Here's both hints combined: `Task.query.order_by(Task.title.asc())`
