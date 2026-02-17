from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class HealthResult:
    url: str
    is_healthy: bool
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)



