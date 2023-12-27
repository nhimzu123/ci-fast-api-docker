import os

import pytest
import redis
from fastapi.testclient import TestClient
from page_tracker.app import app


# To extend pytest with custom command-line arguments
def pytest_addoption(parser):
    parser.addoption("--app-url")


@pytest.fixture(
    scope="session"
)  # to inject into your test functions and other fixtures
def app_url(request):
    return request.config.getoption("--app-url")


@pytest.fixture
def http_client():
    return TestClient(app)


@pytest.fixture(
    scope="module"
)  # scope module to reuse the same Redis client instance for all functions within a test module.
def redis_client():
    return redis.Redis(os.getenv("REDIS_HOST", "localhost"), port=6379)
