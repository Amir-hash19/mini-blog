from dataclasses import asdict

from .events import ActivityEvent
from .tasks import process_activity_event


def publish_event(event: ActivityEvent) -> None:
    process_activity_event.delay(asdict(event))
