"""
Dapr Publisher - Phase-5
Publishes events via Dapr Sidecar

@author: Phase-5 System
"""

import os
import httpx
import logging

logger = logging.getLogger(__name__)

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_URL = f"http://localhost:{DAPR_HTTP_PORT}"


class DaprPublisher:
    """
    Publish events to Kafka via Dapr PubSub
    """

    def __init__(self, pubsub_name: str = "pubsub"):
        self.pubsub_name = pubsub_name
        self.dapr_url = DAPR_URL

    async def publish(self, topic: str, data: dict) -> bool:
        """
        Publish event to a topic

        Args:
            topic: Kafka topic name
            data: Event data (dict)

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.dapr_url}/v1.0/publish/{self.pubsub_name}/{topic}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=5.0
                )

                if response.status_code in (200, 204):
                    logger.info(f"Published to {topic}: {data}")
                    return True
                else:
                    logger.warning(f"Dapr publish failed: {response.status_code}")
                    return False

        except Exception as e:
            # Dapr sidecar might not be running (local dev)
            logger.debug(f"Dapr publish error (sidecar may not be running): {e}")
            return False

    async def publish_task_created(self, task_id: int, user_id: int, priority: str):
        """Publish task created event"""
        await self.publish("task-events", {
            "event_type": "task_created",
            "task_id": task_id,
            "user_id": user_id,
            "priority": priority
        })

    async def publish_task_completed(self, task_id: int, user_id: int, title: str):
        """Publish task completed event"""
        await self.publish("task-events", {
            "event_type": "task_completed",
            "task_id": task_id,
            "user_id": user_id,
            "title": title
        })

    async def publish_task_deleted(self, task_id: int, user_id: int, title: str):
        """Publish task deleted event"""
        await self.publish("task-events", {
            "event_type": "task_deleted",
            "task_id": task_id,
            "user_id": user_id,
            "title": title
        })

    async def publish_reminder(self, task_id: int, user_id: int, reminder_type: str):
        """Publish reminder event"""
        await self.publish("reminders", {
            "event_type": "reminder_triggered",
            "task_id": task_id,
            "user_id": user_id,
            "reminder_type": reminder_type
        })


# Singleton instance
dapr_publisher = DaprPublisher()
