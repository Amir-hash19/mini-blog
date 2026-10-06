from .events import ActivityEvent
from .tasks import process_activity_event

from dataclasses import asdict

def publish_event(event: ActivityEvent) -> None:
    process_activity_event.delay(asdict(event))