import pytest


def test_index(client):
    response = client.get("/")
    response_body = response.get_json()
    assert "name" in response_body
    assert "message" in response_body


def test_get_tasks_no_saved_tasks_test(client):
    response = client.get("/tasks")

    response_body = response.get_json()

    assert response_body == []


# def test_list_tasks(client):
#     response = client.get("/tasks")
#     print("GGGGGGGGGGGGGGGG", response.data)
