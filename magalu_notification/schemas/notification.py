from pydantic import BaseModel
from datetime import datetime
from magalu_notification.models.notification import Channels, NotificationStatus


class SendNotificationSchema(BaseModel):
    recipient: str
    message: str
    send_time: datetime
    channel: Channels


class NotificationSchema(BaseModel):
    id: int
    recipient: str
    message: str
    send_time: datetime
    channel: Channels
    status: NotificationStatus
