import pytest
import httpx
import respx
from api_health_monitor.checker import check_health


@pytest.mark.asyncio
@respx.mock
async def test_healthy_response():
    respx.get("https://example.com/api").mock(return_value=httpx.Response(200))
    result = await check_health("https://example.com/api")

    assert result.url == "https://example.com/api"
    assert result.is_healthy is True
    assert result.status_code == 200
    assert result.response_time_ms is not None
    assert result.error is None


@pytest.mark.asyncio
@respx.mock
async def test_unhealthy_response():
    respx.get("https://example.com/api").mock(return_value=httpx.Response(500))
    result = await check_health("https://example.com/api")

    assert result.is_healthy is False
    assert result.status_code == 500
    assert result.error is None


@pytest.mark.asyncio
@respx.mock
async def test_timeout():
    respx.get("https://example.com/api").mock(side_effect=httpx.TimeoutException("timout"))
    result = await check_health("https://example.com/api")

    assert result.is_healthy is False
    assert result.status_code is None
    assert "Timeout" in result.error


@pytest.mark.asyncio
@respx.mock
async def test_connection_error():
    respx.get("https://example.com/api").mock(side_effect=httpx.ConnectError("failed"))
    result = await check_health("https://example.com/api")

    assert result.is_healthy is False
    assert result.status_code is None 
    assert "Connection failed" in result.error


@pytest.mark.asyncio
@respx.mock
async def test_404_is_unhealthy():
    respx.get("https://example.com/api").mock(return_value=httpx.Response(404))
    result = await check_health("https://example.com/api")

    assert result.is_healthy is False 
    assert result.status_code == 404
    assert result.error is None