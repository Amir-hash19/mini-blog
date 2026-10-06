from dataclasses import dataclass, field
from datetime import datetime
from typing import Any



@dataclass
class ActivityEvent:
    user_id: int
    action: str
    target_type: str
    target_id: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: datetime | None = None