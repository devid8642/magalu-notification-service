from fastapi import FastAPI
from magalu_notification.schemas.notification import SendNotificationSchema, NotificationSchema
from magalu_notification.services.notification_service import get_notification_service


app = FastAPI(version='0.1.0', title='Magalu Notification API')


@app.post('/send/notification')
async def send_notification(notification_data: SendNotificationSchema) -> NotificationSchema:
    notification_service = get_notification_service()

    notification = await notification_service.create_notification(
        notification_data.model_dump()
    )

    return notification
