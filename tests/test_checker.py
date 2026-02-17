import responses
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
    