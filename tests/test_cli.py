import pytest
import httpx
import respx
from unittest.mock import patch
from io import StringIO
from api_health_monitor.cli import main


@respx.mock
def test_healthy_output():
    respx.get(
        "https://example.com/api").mock(return_value=httpx.Response(200)
    )

    with patch("sys.argv", ["cli", "https://example.com/api"]):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()

    assert "[HEALTHY]" in output


@respx.mock
def test_unhealthy_response():
    respx.get(
        "https://example.com/api").mock(return_value=httpx.Response(500)
    )

    with patch("sys.argv", ["cli", "https://example.com/api"]):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            with pytest.raises(SystemExit) as exc_info:
                main()
            output = mock_stdout.getvalue()

    assert "[UNHEALTHY]" in output
    assert exc_info.value.code == 1        


