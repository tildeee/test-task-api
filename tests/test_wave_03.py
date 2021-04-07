import unittest
from unittest.mock import Mock, patch


def test_toggle_complete_on_incomplete_task(client, one_task):
    # Arrange
    # We need to mock the POST request that this may cause while testing
    with patch("app.routes.requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        # Act
        response = client.patch("/tasks/1/complete")

    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["task"]["is_complete"] == True


def test_toggle_complete_on_complete_task(client, completed_task):
    # Act
    response = client.patch("/tasks/1/complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["task"]["is_complete"] == False
