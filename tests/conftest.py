import pytest
from fastapi.testclient import TestClient
from magalu_notification.main import app
from magalu_notification.models.notification import Notification


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
