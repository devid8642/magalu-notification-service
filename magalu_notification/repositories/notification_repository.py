from magalu_notification.models.notification import Notification
from sqlalchemy.ext.asyncio import async_sessionmaker


class NotificationRepository:
    """Interface for NotificationRepository"""
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    async def create_notification(self, notification: Notification):
        raise NotImplementedError
    
    async def get_notification(self, notification_id: int) -> Notification | None:
        raise NotImplementedError


class PostgresNotificationRepository(NotificationRepository):
    """Postgres implementation of NotificationRepository"""
    async def create_notification(self, notification_data: dict) -> Notification:
        notification = Notification(**notification_data)

        async with self.session_factory() as session:
            async with session.begin():
                session.add(notification)
                await session.commit()
            await session.refresh(notification)

        return notification
    
    async def get_notification(self, notification_id: int) -> Notification | None:
        async with self.session_factory() as session:
            notification = await session.get(Notification, notification_id)

        return notification
