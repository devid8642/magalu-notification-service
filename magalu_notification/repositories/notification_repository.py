from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import async_sessionmaker

from magalu_notification.models.notification import (
    Notification,
    NotificationStatus,
)
from magalu_notification.schemas.notification import NotificationSchema


class NotificationRepository(ABC):
    """Interface for NotificationRepository"""

    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    @abstractmethod
    async def create_notification(
        self, notification_data: NotificationSchema
    ) -> Notification:
        raise NotImplementedError

    @abstractmethod
    async def get_notification(
        self, notification_id: int
    ) -> Notification | None:
        raise NotImplementedError

    @abstractmethod
    async def update_notification(
        self, notification: Notification
    ) -> Notification:
        raise NotImplementedError


class PostgresNotificationRepository(NotificationRepository):
    """Postgres implementation of NotificationRepository"""

    async def create_notification(
        self, notification_data: NotificationSchema
    ) -> Notification:
        notification = Notification(**notification_data.model_dump())

        async with self.session_factory() as session:
            async with session.begin():
                session.add(notification)
                await session.commit()
            await session.refresh(notification)

        return notification

    async def get_notification(
        self, notification_id: int
    ) -> Notification | None:
        async with self.session_factory() as session:
            notification = await session.get(Notification, notification_id)

        return notification

    async def update_notification(
        self, notification: Notification
    ) -> Notification:
        async with self.session_factory() as session:
            async with session.begin():
                session.add(notification)
                await session.commit()
            await session.refresh(notification)

        return notification
