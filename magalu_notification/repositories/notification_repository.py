from magalu_notification.models.notification import Notification
from sqlalchemy.ext.asyncio import AsyncSession


class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_notification(self, notification: Notification):
        raise NotImplementedError


class PostgresNotificationRepository(NotificationRepository):
    async def create_notification(self, notification: Notification) -> Notification:
        async with self.session() as session:
            async with session.begin():
                session.add(notification)
                await session.commit()
            await session.refresh(notification)

        return notification
