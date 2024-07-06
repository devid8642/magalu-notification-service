import pytz
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
import enum
from datetime import datetime


class Base(DeclarativeBase):
    pass


class CommunicationType(enum.Enum):
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push'
    WHATSAPP = 'whatsapp'


class NotificationStatus(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    CANCELED = "canceled"
    FAILED = "failed"


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    send_time = Column(DateTime, default=lambda: datetime.now(pytz.timezone('America/Sao_Paulo')))
    recipient = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    communication_type = Column(Enum(CommunicationType), nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING, nullable=False)
