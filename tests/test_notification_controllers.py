import pytest
from unittest.mock import patch, AsyncMock
from magalu_notification.schemas.notification import SendNotificationSchema, NotificationSchema
from fastapi.testclient import TestClient


def test_send_notification(client: TestClient, notification_data, notification_response):
    with patch('magalu_notification.main.get_notification_service') as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.create_notification = AsyncMock(
            return_value=NotificationSchema(**notification_response)
        )

        response = client.post('/send/notification', json=notification_data)

        assert response.status_code == 201
        assert response.json() == notification_response


def test_get_notification(client: TestClient, notification_response):
    with patch('magalu_notification.main.get_notification_service') as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.get_notification = AsyncMock(
            return_value=NotificationSchema(**notification_response)
        )

        response = client.get('/notification/1')

        assert response.status_code == 200
        assert response.json() == notification_response


def test_get_notification_not_found(client: TestClient):
    with patch('magalu_notification.main.get_notification_service') as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.get_notification = AsyncMock(
            return_value=None
        )

        response = client.get('/notification/999')

        assert response.status_code == 404
        assert response.json() == {'message': 'Notificação não encontrada'}
