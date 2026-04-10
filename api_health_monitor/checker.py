import time
import asyncio
import httpx
from api_health_monitor.models import HealthResult


async def check_health(url: str, timeout: float = 5.0, retries: int = 3) -> HealthResult:
    for attempt in range(retries):
        start = time.time()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=timeout)
            elapsed_ms = (time.time() - start) * 1000
            is_healthy = response.status_code < 400
            return HealthResult(
                url=url,
                is_healthy=is_healthy,
                status_code=response.status_code,
                response_time_ms=round(elapsed_ms, 2),
            )

        except httpx.TimeoutException:
            if attempt == retries - 1:
                elapsed_ms = (time.time() - start) * 1000
                return HealthResult(url=url, is_healthy=False, response_time_ms=round(elapsed_ms, 2), error=f"Timeout after {timeout}s")
            await asyncio.sleep(2 ** attempt)

        except httpx.ConnectError:
            if attempt == retries - 1:
                elapsed_ms = (time.time() - start) * 1000
                return HealthResult(url=url, is_healthy=False, response_time_ms=round(elapsed_ms, 2), error="Connection failed")
            await asyncio.sleep(2 ** attempt)

        except httpx.RequestError as e:
            if attempt == retries - 1:
                elapsed_ms = (time.time() - start) * 1000
                return HealthResult(url=url, is_healthy=False, response_time_ms=round(elapsed_ms, 2), error=str(e))
            await asyncio.sleep(2 ** attempt)


async def check_all(urls: list[str], timeout: float = 5.0, retries: int = 3) -> list[HealthResult]:
    tasks = [check_health(url, timeout, retries) for url in urls]
    return await asyncio.gather(*tasks)
