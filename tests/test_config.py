import pytest
import tempfile
import os
from api_health_monitor.config import load_config, EndpointConfig


def test_load_config():
    yaml_content = """
endpoints:
    - name: Test API
      url: https://example.com
      timeout: 10
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
        f.write(yaml_content)
        tmp_path = f.name

    try:
        endpoints = load_config(tmp_path)
        assert len(endpoints) == 1
        assert endpoints[0].url == "https://example.com"
        assert endpoints[0].name == "Test API"
        assert endpoints[0].timeout == 10
    finally:
        os.unlink(tmp_path)    