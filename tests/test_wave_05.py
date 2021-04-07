def test_get_goals_no_saved_goals(client):
    response = client.get("/goals")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_goals_one_saved_goal(client, one_goal):
    response = client.get("/goals")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "title": "Build a habit of going outside daily"
    }]


def test_get_goal(client, one_goal):
    response = client.get("/goals/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    }


def test_get_task_not_found(client):
    response = client.get("/goals/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None


def test_create_goal(client):
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "My New Goal"
        }
    }


def test_update_goal(client, one_goal):
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Updated Goal Title"
        }
    }


def test_update_goal_not_found(client):
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"
    })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None


def test_delete_goal(client, one_goal):
    response = client.delete("/goals/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }

    # Check that the task was deleted
    response = client.get("/goals/1")
    assert response.status_code == 404


def test_delete_goal_not_found(client):
    response = client.delete("/goals/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None
