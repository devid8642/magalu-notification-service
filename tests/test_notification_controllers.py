from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from magalu_notification.schemas.general import SuccessSchema
from magalu_notification.schemas.notification import (
    NotificationSchema,
    SendNotificationSchema,
)
from magalu_notification.services.exceptions import (
    NotificationAlreadySended,
    NotificationNotFound,
)


def test_send_notification(
    client: TestClient, notification_data, notification_response
):
    with patch(
        'magalu_notification.main.get_notification_service'
    ) as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.create_notification = AsyncMock(
            return_value=NotificationSchema(**notification_response)
        )

        response = client.post('/send/notification', json=notification_data)

        assert response.status_code == 201
        assert response.json() == notification_response


def test_get_notification(client: TestClient, notification_response):
    with patch(
        'magalu_notification.main.get_notification_service'
    ) as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.get_notification = AsyncMock(
            return_value=NotificationSchema(**notification_response)
        )

        response = client.get('/notification/1')

        assert response.status_code == 200
        assert response.json() == notification_response


def test_get_notification_not_found(client: TestClient):
    with patch(
        'magalu_notification.main.get_notification_service'
    ) as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.get_notification = AsyncMock(return_value=None)

        response = client.get('/notification/999')

        assert response.status_code == 404
        assert response.json() == {'message': 'Notificação não encontrada'}


def test_cancel_notification_success(client: TestClient):
    with patch(
        'magalu_notification.main.get_notification_service'
    ) as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.cancel_notification = AsyncMock(
            return_value=None
        )

        response = client.post('/notification/cancel/1')

        assert response.status_code == 200
        assert response.json() == {
            'message': 'Notificação cancelada com sucesso'
        }


def test_cancel_notification_not_found(client: TestClient):
    with patch(
        'magalu_notification.main.get_notification_service'
    ) as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.cancel_notification = AsyncMock(
            side_effect=NotificationNotFound()
        )

        response = client.post('/notification/cancel/999')

        assert response.status_code == 404
        assert response.json() == {'message': 'Notificação não encontrada'}


def test_cancel_notification_already_sent(client: TestClient):
    with patch(
        'magalu_notification.main.get_notification_service'
    ) as mock_service:
        mock_service_instance = mock_service.return_value
        mock_service_instance.cancel_notification = AsyncMock(
            side_effect=NotificationAlreadySended()
        )

        response = client.post('/notification/cancel/1')

        assert response.status_code == 400
        assert response.json() == {'message': 'Notificação já enviada'}
