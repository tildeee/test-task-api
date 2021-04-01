from flask import url_for
from app.routes import task_page


def test_index(client):
    response = client.get("/")
    response_body = response.get_json()
    assert "name" in response_body
    assert "message" in response_body


def test_get_tasks_no_saved_tasks(client):
    response = client.get("/tasks/1")

    assert response.status_code == 404

    response_body = response.get_json()

    assert response_body == []


# def test_list_tasks(client):
#     response = client.get("/tasks")
#     print("GGGGGGGGGGGGGGGG", response.data)
