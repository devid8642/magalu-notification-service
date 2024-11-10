import pytest
from magalu_notification.models.notification import Notification, NotificationStatus
from magalu_notification.repositories.notification_repository import NotificationRepository
from magalu_notification import settings
from magalu_notification.schemas.notification import SendNotificationSchema


@pytest.mark.asyncio
async def test_create_notification(send_notification_data: SendNotificationSchema, notification_repository: NotificationRepository, session_factory):
    notification = await notification_repository.create_notification(send_notification_data)

    async with session_factory() as session:
        db_notification: Notification = await session.get(
            Notification, notification.id
        )
    
    assert notification.id == db_notification.id
    assert notification.recipient == db_notification.recipient
    assert notification.message == db_notification.message
    assert notification.send_time == db_notification.send_time
    assert notification.channel == db_notification.channel
    assert notification.status == db_notification.status


@pytest.mark.asyncio
async def test_get_notification(send_notification_data: SendNotificationSchema, notification_repository: NotificationRepository, session_factory):
    notification = Notification(**send_notification_data.model_dump())

    async with session_factory() as session:
        async with session.begin():
            session.add(notification)
            await session.commit()
        await session.refresh(notification)

    db_notification = await notification_repository.get_notification(notification.id)

    assert notification.id == db_notification.id
    assert notification.recipient == db_notification.recipient
    assert notification.message == db_notification.message
    assert notification.send_time == db_notification.send_time
    assert notification.channel == db_notification.channel
    assert notification.status == db_notification.status


@pytest.mark.asyncio
async def test_update_notification(send_notification_data: SendNotificationSchema, notification_repository: NotificationRepository, session_factory):
    notification = Notification(**send_notification_data.model_dump())

    async with session_factory() as session:
        async with session.begin():
            session.add(notification)
            await session.commit()
        await session.refresh(notification)

    # Update notification status
    notification.status = NotificationStatus.CANCELED
    updated_notification = await notification_repository.update_notification(notification)

    async with session_factory() as session:
        db_notification: Notification = await session.get(
            Notification, updated_notification.id
        )

    assert updated_notification.id == db_notification.id
    assert updated_notification.recipient == db_notification.recipient
    assert updated_notification.message == db_notification.message
    assert updated_notification.send_time == db_notification.send_time
    assert updated_notification.channel == db_notification.channel
    assert updated_notification.status == NotificationStatus.CANCELED
