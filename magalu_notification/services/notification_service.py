from magalu_notification.db.postgres import PostgresConnection
from magalu_notification.models.notification import (
    Notification,
    NotificationStatus,
)
from magalu_notification.repositories.notification_repository import (
    NotificationRepository,
    PostgresNotificationRepository,
)
from magalu_notification.schemas.notification import NotificationSchema

from .exceptions import NotificationAlreadySended, NotificationNotFound


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    async def create_notification(
        self, notification_data: NotificationSchema
    ) -> Notification:
        notification = await self.notification_repository.create_notification(
            notification_data
        )

        return notification

    async def get_notification(
        self, notification_id: int
    ) -> Notification | None:
        notification = await self.notification_repository.get_notification(
            notification_id
        )

        return notification

    async def cancel_notification(self, notification_id: int) -> None:
        notification = await self.get_notification(notification_id)

        if not notification:
            raise NotificationNotFound('Notificação não encontrada')

        if (
            notification.status == NotificationStatus.SUCCESS
            or notification.status == NotificationStatus.FAILED
        ):
            raise NotificationAlreadySended('Notificação já enviada')

        notification.status = NotificationStatus.CANCELED

        await self.notification_repository.update_notification(notification)


def get_notification_service():
    session_factory = PostgresConnection.get_session_factory()
    notification_repository = PostgresNotificationRepository(session_factory)
    return NotificationService(notification_repository)
