import pytest
from fastapi.testclient import TestClient
from magalu_notification.main import app


@pytest.fixture
def client():
    return TestClient(app)
