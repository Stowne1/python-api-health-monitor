import responses
import requests
from unittest.mock import patch
from io import StringIO
from api_health_monitor.cli import main


@responses.activate
def test_healthy_output():
    responses.add(
        responses.GET,
        "https://example.com/api",
        status=200
    )

    with patch("sys.argv", ["cli", "https://example.com/api"]):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()

    assert "[HEALTHY]" in output        


@responses.activate
def test_unhealthy_response():
    responses.add(
        responses.GET,
        "https://example.com/api",
        status=500

    )
    with patch("sys.argv", ["cli", "https://example.com/api"]):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()

    assert "[UNHEALTHY]" in output        


