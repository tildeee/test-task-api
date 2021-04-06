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


def test_get_tasks_sorted_asc(client, three_tasks):
    response = client.get("/tasks?sort=asc")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"},
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
    ]


def test_get_tasks_sorted_desc(client, three_tasks):
    response = client.get("/tasks?sort=desc")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"},
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
    ]
