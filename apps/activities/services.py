from .models import Activity


def create_activity(event_data: dict) -> Activity:
    return Activity.objects.create(
        user_id=event_data["user_id"],
        action=event_data["action"],
        target_type=event_data["target_type"],
        target_id=event_data.get("target_id"),
        metadata=event_data.get("metadata", {}),
        ip_address=event_data.get("ip_address"),
        user_agent=event_data.get("user_agent"),
    )
