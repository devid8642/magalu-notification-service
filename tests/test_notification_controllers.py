import pytest
from unittest.mock import patch, AsyncMock
from magalu_notification.schemas.notification import SendNotificationSchema, NotificationSchema
from fastapi.testclient import TestClient


@pytest.fixture
def notification_data():
    return {
        "recipient": "example@example.com",
        "message": "Test message",
        "send_time": "2024-07-07T14:48:35.961116",
        "channel": "email"
    }


@pytest.fixture
def notification_response():
    return {
        "id": 1,
        "recipient": "example@example.com",
        "message": "Test message",
        "send_time": "2024-07-07T14:48:35.961116",
        "channel": "email",
        "status": "pending"
    }


def test_send_notification(client: TestClient, notification_data, notification_response):
    with patch('magalu_notification.main.get_notification_service') as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.create_notification = AsyncMock(
            return_value=NotificationSchema(**notification_response)
        )

        response = client.post("/send/notification", json=notification_data)

        assert response.status_code == 200
        assert response.json() == notification_response
