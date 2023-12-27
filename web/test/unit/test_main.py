import unittest.mock as mock
from httpx import Response
from fastapi.testclient import TestClient

from redis import ConnectionError


@mock.patch("page_tracker.app.redis")
def test_should_call_redis_incr(mock_redis, http_client: TestClient):
    # Given
    mock_redis.return_value.incr.return_value = 5

    # When
    response: Response = http_client.get("/")

    # Then
    assert response.status_code == 200
    assert response.json() == "This page has been seen 5 times."
    mock_redis.return_value.incr.assert_called_once_with("page_views")


@mock.patch("page_tracker.app.redis")
def test_should_handle_redis_connection_error(mock_redis, http_client: TestClient):
    # Given
    mock_redis.return_value.incr.side_effect = ConnectionError

    # When
    response: Response = http_client.get("/")

    # Then
    assert response.status_code == 500
    assert response.json() == "Sorry, something went wrong \N{pensive face}"
