# Import pytest and requests
import pytest
import requests


# Define a test with timeout of 1.5 senconds
@pytest.mark.timeout(1.5)
def test_should_update_redis(redis_client, app_url):
    # Given
    redis_client.set("page_views", 4)

    # When
    response = requests.get(app_url)

    # Then
    assert response.status_code == 200
    assert response.json() == "This page has been seen 5 times."
    assert redis_client.get("page_views") == b"5"
