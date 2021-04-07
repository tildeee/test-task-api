def test_get_tasks_for_specific_goal(client):
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_tasks_for_specific_goal_no_tasks(client, one_goal):
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Build a habit of going outside daily",
        "tasks": []
    }


def test_get_tasks_for_specific_goal(client, one_task_belongs_to_one_goal):
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    assert response.status_code == 200

    assert response_body == {
        "id": 1,
        "title": "Build a habit of going outside daily",
        "tasks": [
            {
                "id": 1,
                "goal_id": 1,
                "title": "Go on my daily walk 🏞",
                "description": "Notice something new every day",
                "is_complete": False
            }
        ]
    }


def test_get_task_includes_goal_id(client, one_task_belongs_to_one_goal):
    response = client.get("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "task": {
            "id": 1,
            "goal_id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }
