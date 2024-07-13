from magalu_notification.repositories.notification_repository import NotificationRepository, PostgresNotificationRepository
from magalu_notification.models.notification import Notification
from magalu_notification.db.postgres import PostgresConnection


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository
    
    async def create_notification(self, notification_data: dict) -> Notification:
        notification = await self.notification_repository.create_notification(
            notification_data
        )

        return notification
    
    async def get_notification(self, notification_id: int) -> Notification | None:
        notification = await self.notification_repository.get_notification(notification_id)

        return notification


def get_notification_service():
    session = PostgresConnection.get_session()
    notification_repository = PostgresNotificationRepository(session)
    return NotificationService(notification_repository)
