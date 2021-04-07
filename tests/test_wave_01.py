def test_index(client):
    response = client.get("/")
    response_body = response.get_json()
    assert "name" in response_body
    assert "message" in response_body


def test_get_tasks_no_saved_tasks(client):
    response = client.get("/tasks")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_tasks_one_saved_tasks(client, one_task):
    response = client.get("/tasks")
    response_body = response.get_json()
    first_task = response_body[0]

    assert response.status_code == 200

    assert "id" in first_task
    assert "title" in first_task
    assert "description" in first_task
    assert "is_complete" in first_task


def test_get_task(client, one_task):
    response = client.get("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "id" in response_body["task"]
    assert "title" in response_body["task"]
    assert "description" in response_body["task"]
    assert "is_complete" in response_body["task"]


def test_get_task_not_found(client):
    response = client.get("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None


def test_post_task(client):
    response = client.post("/tasks", json={
        "title": "c",
        "description": "Test Description",
        "completed_at": None
    })
    response_body = response.get_json()

    assert response.status_code == 200

    assert "task" in response_body
    assert response_body["task"] == {
        "description": "Test Description",
        "id": 1,
        "is_complete": False,
        "title": "c"
    }


def test_update_task(client, one_task):
    response = client.put("/tasks/1", json={
        "title": "c",
        "description": "Test Description",
        "completed_at": None
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert "task" in response_body
    assert response_body["task"] == {
        "description": "Test Description",
        "id": 1,
        "is_complete": False,
        "title": "c"
    }


def test_update_task_not_found(client):
    response = client.put("/tasks/1", json={
        "title": "c",
        "description": "Test Description",
        "completed_at": None
    })

    response_body = response.get_json()

    assert response.status_code == 404

    assert response_body == None


def test_delete_task(client, one_task):
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body

    # Check that the task was deleted
    response = client.get("/tasks/1")
    assert response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/1")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None
