from unittest.mock import AsyncMock, MagicMock

import pytest

from magalu_notification.models.notification import (
    Notification,
    NotificationStatus,
)
from magalu_notification.repositories.notification_repository import (
    NotificationRepository,
)
from magalu_notification.schemas.notification import SendNotificationSchema
from magalu_notification.services.exceptions import (
    NotificationAlreadySended,
    NotificationNotFound,
)
from magalu_notification.services.notification_service import (
    NotificationService,
)


@pytest.mark.asyncio
async def test_create_notification(
    send_notification_data: SendNotificationSchema, notification: Notification
):
    mock_repo = MagicMock(NotificationRepository)
    mock_repo.create_notification = AsyncMock(return_value=notification)

    service = NotificationService(mock_repo)

    created_notification = await service.create_notification(
        send_notification_data
    )

    mock_repo.create_notification.assert_called_once_with(
        send_notification_data
    )
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


@pytest.mark.asyncio
async def test_cancel_notification_success(notification: Notification):
    mock_repo = MagicMock(NotificationRepository)
    mock_repo.get_notification = AsyncMock(return_value=notification)
    mock_repo.update_notification = AsyncMock()

    service = NotificationService(mock_repo)

    await service.cancel_notification(notification.id)

    mock_repo.get_notification.assert_called_once_with(notification.id)
    assert notification.status == NotificationStatus.CANCELED
    mock_repo.update_notification.assert_called_once_with(notification)


@pytest.mark.asyncio
async def test_cancel_notification_not_found():
    mock_repo = MagicMock(NotificationRepository)
    mock_repo.get_notification = AsyncMock(return_value=None)

    service = NotificationService(mock_repo)

    with pytest.raises(NotificationNotFound):
        await service.cancel_notification(999)

    mock_repo.get_notification.assert_called_once_with(999)


@pytest.mark.asyncio
async def test_cancel_notification_already_sent(notification: Notification):
    notification.status = NotificationStatus.SUCCESS

    mock_repo = MagicMock(NotificationRepository)
    mock_repo.get_notification = AsyncMock(return_value=notification)

    service = NotificationService(mock_repo)

    with pytest.raises(NotificationAlreadySended):
        await service.cancel_notification(notification.id)

    mock_repo.get_notification.assert_called_once_with(notification.id)
    mock_repo.update_notification.assert_not_called()
