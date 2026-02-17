from api_health_monitor.models import HealthResult


def test_healthy_result():
    result = HealthResult(
        url="https://example.com",
        is_healthy=True,
        status_code=200,
        response_time_ms=150.0,
    )
    assert result.url == "https://example.com"
    assert result.is_healthy is True
    assert result.status_code == 200
    assert result.response_time_ms == 150.0
    assert result.error is None
    


  