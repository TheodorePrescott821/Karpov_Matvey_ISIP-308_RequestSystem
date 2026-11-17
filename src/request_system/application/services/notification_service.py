"""Notification service for managing request notifications."""

from datetime import datetime, timezone
from typing import Optional

from request_system.domain.entities import Notification


class NotificationService:
    """Handles creation and retrieval of notifications."""

    @staticmethod
    def create_notification(
        user_id: int,
        event_type: str,
        request_id: Optional[int] = None
    ) -> Notification:
        """Create a new notification."""
        return Notification(
            notification_id=None,
            user_id=user_id,
            event_type=event_type,
            request_id=request_id,
            created_at=datetime.now(timezone.utc),
            read_at=None
        )

    @staticmethod
    def get_event_description(event_type: str) -> str:
        """Get human-readable description for event type."""
        descriptions = {
            "request_created": "Новая заявка зарегистрирована",
            "assigned": "Вам назначена заявка",
            "status_changed": "Статус заявки изменился",
            "result_submitted": "Результат передан на проверку",
            "decision_made": "Решение принято",
            "comment_added": "Добавлен новый комментарий",
            "returned_for_rework": "Заявка возвращена на доработку"
        }
        return descriptions.get(event_type, event_type)
