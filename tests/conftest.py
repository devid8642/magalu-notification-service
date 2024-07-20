import pytest
from fastapi.testclient import TestClient
from magalu_notification.main import app
from magalu_notification.models.notification import Notification
import psycopg
from magalu_notification import settings
from magalu_notification.schemas.notification import SendNotificationSchema
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def notification_data():
    return {
        'recipient': 'example@example.com',
        'message': 'Test message',
        'send_time': '2024-07-07T14:48:35.961116',
        'channel': 'email'
    }


@pytest.fixture
def send_notification_data(notification_data):
    return SendNotificationSchema(**notification_data).model_dump()


@pytest.fixture
def notification_response():
    return {
        'id': 1,
        'recipient': 'example@example.com',
        'message': 'Test message',
        'send_time': '2024-07-07T14:48:35.961116',
        'channel': 'email',
        'status': 'pending'
    }


@pytest.fixture
def notification(notification_data):
    return Notification(id=1, **notification_data)


@pytest.fixture(scope='session')
def create_test_database():
    connection_string = (
        f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}'
        f'@{settings.DB_HOST}:{settings.DB_PORT}/postgres'
    )

    with psycopg.connect(connection_string, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute('CREATE DATABASE test_db')

    yield

    with psycopg.connect(connection_string, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute('DROP DATABASE test_db')
