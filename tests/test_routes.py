from flask import url_for
from app.routes import task_page


def test_index(client):
    response = client.get("/")
    response_body = response.get_json()
    assert "name" in response_body
    assert "message" in response_body


def test_get_tasks_no_saved_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200

    response_body = response.get_json()

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

# def test_list_tasks(client):
#     response = client.get("/tasks")
#     print("GGGGGGGGGGGGGGGG", response.data)
