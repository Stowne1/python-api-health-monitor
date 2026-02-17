import time
import requests
from api_health_monitor.models import HealthResult


def check_health(url: str, timeout: float = 5.0) -> HealthResult:
    start = time.time()

    try: 
        response = requests.get(url, timeout=timeout)
        elapsed_ms = (time.time() - start) * 1000

        is_healthy = response.status_code < 400

        return HealthResult(
            url=url,
            is_healthy=is_healthy,
            status_code=response.status_code,
            response_time_ms=round(elapsed_ms, 2),
        )
    
    except requests.exceptions.Timeout:
        elapsed_ms = (time.time() - start) * 1000
        return HealthResult(
            url=url,
            is_healthy=False,
            response_time_ms=round(elapsed_ms, 2),
            error=f"Timeout after {timeout}s",
        )
    except requests.exceptions.ConnectionError:
        elapsed_ms = (time.time() - start) * 1000
        return HealthResult(
            url=url,
            is_healthy=False,
            response_time_ms=round(elapsed_ms, 2),
            error="Connection failed",
        )
    except requests.exceptions.RequestException as e:
        elapsed_ms = (time.time() - start) * 1000
        return HealthResult(
            url=url,
            is_healthy=False,
            response_time_ms=round(elapsed_ms, 2),
            error=str(e),
        )