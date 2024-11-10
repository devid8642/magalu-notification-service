import psycopg
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from magalu_notification import settings
from magalu_notification.db.base import Base
from magalu_notification.main import app
from magalu_notification.models.notification import Notification
from magalu_notification.repositories.notification_repository import (
    PostgresNotificationRepository,
)
from magalu_notification.schemas.notification import SendNotificationSchema


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def notification_data():
    return {
        'recipient': 'example@example.com',
        'message': 'Test message',
        'send_time': '2024-07-07T14:48:35.961116',
        'channel': 'email',
    }


@pytest.fixture
def send_notification_data(notification_data):
    return SendNotificationSchema(**notification_data)


@pytest.fixture
def notification_response():
    return {
        'id': 1,
        'recipient': 'example@example.com',
        'message': 'Test message',
        'send_time': '2024-07-07T14:48:35.961116',
        'channel': 'email',
        'status': 'pending',
    }


@pytest.fixture
def notification(notification_data):
    return Notification(id=1, **notification_data)


@pytest_asyncio.fixture(scope='session')
async def test_engine():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', future=True)
    async with engine.begin() as conn:
        # Cria as tabelas de teste
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def notification_repository(session_factory):
    return PostgresNotificationRepository(session_factory)
