import pytest
from unittest.mock import AsyncMock, MagicMock
from magalu_notification.services.notification_service import NotificationService
from magalu_notification.models.notification import Notification
from magalu_notification.repositories.notification_repository import NotificationRepository


@pytest.mark.asyncio
async def test_create_notification(notification_data: dict, notification: Notification):
    mock_repo = MagicMock(NotificationRepository)
    mock_repo.create_notification = AsyncMock(return_value=notification)

    service = NotificationService(mock_repo)

    created_notification = await service.create_notification(notification_data)

    mock_repo.create_notification.assert_called_once_with(notification_data)
    assert created_notification == notification


@pytest.mark.asyncio
async def test_get_notification(notification: Notification):
    mock_repo = MagicMock(NotificationRepository)
    mock_repo.get_notification = AsyncMock(return_value=notification)

    service = NotificationService(mock_repo)

    fetched_notification = await service.get_notification(notification.id)

    mock_repo.get_notification.assert_called_once_with(notification.id)
    assert fetched_notification == notification


@pytest.mark.asyncio
async def test_get_notification_not_found():
    mock_repo = MagicMock(NotificationRepository)
    mock_repo.get_notification = AsyncMock(return_value=None)

    service = NotificationService(mock_repo)

    fetched_notification = await service.get_notification(999)

    mock_repo.get_notification.assert_called_once_with(999)
    assert fetched_notification is None
