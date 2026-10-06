from celery import shared_task
from celery.utils.log import get_task_logger

from .services import create_activity

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=3,
    soft_time_limit=10,
    time_limit=15,
)
def process_activity_event(self, event_data):
    activity = create_activity(event_data)

    logger.info(
        "Activity created successfully | "
        "id=%s | action=%s | user_id=%s | target=%s:%s",
        activity.id,
        activity.action,
        activity.user_id,
        activity.target_type,
        activity.target_id,
    )

    return {
        "activity_id": str(activity.id),
        "action": activity.action,
        "user_id": activity.user_id,
    }
