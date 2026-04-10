from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class HealthResult:
    """Represents the result of a single health check against an endpoint.

    is_healthy is True if the response status code is below 400.
    error is set when a network-level failure occurs (timeout, connection error).
    """
    url: str
    is_healthy: bool
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)



