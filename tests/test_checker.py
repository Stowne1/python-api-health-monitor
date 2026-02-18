import responses
import requests
from api_health_monitor.checker import check_health


@responses.activate
def test_healthy_response():
    responses.add(
        responses.GET,
        "https://example.com/api",
        status=200
    )

    result = check_health("https://example.com/api")

    assert result.url == "https://example.com/api"
    assert result.is_healthy is True
    assert result.status_code == 200
    assert result.response_time_ms is not None
    assert result.error is None


@responses.activate
def test_unhealthy_response():
    responses.add(
        responses.GET,
        "https://example.com/api",
        status=500
    )

    result = check_health("https://example.com/api")

    assert result.is_healthy is False
    assert result.status_code == 500
    assert result.error is None


@responses.activate
def test_timeout():
    responses.add(
        responses.GET,
        "https://example.com/api",
        body=requests.exceptions.Timeout()
    )

    result = check_health("https://example.com/api")

    assert result.is_healthy is False
    assert result.status_code is None
    assert "Timeout" in result.error


@responses.activate
def test_connection_error():
    responses.add(
        responses.GET,
        "https://example.com/api",
        body=requests.exceptions.ConnectionError()
    )

    result = check_health("https://example.com/api")

    assert result.is_healthy is False
    assert result.status_code is None 
    assert "Connection failed" in result.error
