import enum
from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, Enum, Integer, String, Text

from magalu_notification.db.base import Base


class Channels(enum.Enum):
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push'
    WHATSAPP = 'whatsapp'


class NotificationStatus(enum.Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    CANCELED = 'canceled'
    FAILED = 'failed'


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    send_time = Column(
        DateTime,
        default=lambda: datetime.now(pytz.timezone('America/Sao_Paulo')),
    )
    recipient = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    channel = Column(Enum(Channels), nullable=False)
    status = Column(
        Enum(NotificationStatus),
        default=NotificationStatus.PENDING,
        nullable=False,
    )
