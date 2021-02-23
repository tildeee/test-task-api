import pytest


def test_index(client):
    response = client.get("/")
    assert b"name" in response.data
    assert b"message" in response.data

def test_list_tasks(client):
    response = client.get("/tasks")
    print("GGGGGGGGGGGGGGGG", response.data)
