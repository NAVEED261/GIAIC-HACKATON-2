"""
Notification Service - Phase-5
Handles notification delivery via Dapr pub/sub

@author: Phase-5 System
"""

import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI(
    title="Notification Service",
    version="1.0.0"
)

DAPR_PORT = os.getenv("DAPR_HTTP_PORT", "3500")


class NotificationEvent(BaseModel):
    """Notification event from Kafka"""
    event_type: str
    reminder_id: int
    task_id: int
    user_id: str
    type: str  # email, push, sms, in_app
    message: Optional[str] = None


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "notification"}


@app.post("/dapr/subscribe")
async def subscribe():
    """Dapr subscription configuration"""
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "notifications",
            "route": "/notifications"
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminders",
            "route": "/reminders"
        }
    ]


@app.post("/notifications")
async def handle_notification(event: dict):
    """Handle notification events"""
    print(f"📬 Notification event: {event}")

    data = event.get("data", event)
    notification_type = data.get("type", "in_app")
    user_id = data.get("user_id")
    message = data.get("message", "You have a notification")

    # Process based on type
    if notification_type == "email":
        await send_email(user_id, message)
    elif notification_type == "push":
        await send_push(user_id, message)
    elif notification_type == "sms":
        await send_sms(user_id, message)
    else:
        await send_in_app(user_id, message)

    return {"status": "processed"}


@app.post("/reminders")
async def handle_reminder(event: dict):
    """Handle reminder events"""
    print(f"⏰ Reminder event: {event}")

    data = event.get("data", event)
    event_type = data.get("event_type")

    if event_type == "reminder_scheduled":
        print(f"  Reminder scheduled: {data.get('reminder_id')}")
    elif event_type == "reminder_cancelled":
        print(f"  Reminder cancelled: {data.get('reminder_id')}")

    return {"status": "processed"}


async def send_email(user_id: str, message: str):
    """Send email notification (mock)"""
    print(f"📧 Email to user {user_id}: {message}")
    # In production: integrate with email service (SendGrid, SES, etc.)


async def send_push(user_id: str, message: str):
    """Send push notification (mock)"""
    print(f"🔔 Push to user {user_id}: {message}")
    # In production: integrate with push service (FCM, APNs, etc.)


async def send_sms(user_id: str, message: str):
    """Send SMS notification (mock)"""
    print(f"📱 SMS to user {user_id}: {message}")
    # In production: integrate with SMS service (Twilio, etc.)


async def send_in_app(user_id: str, message: str):
    """Send in-app notification"""
    print(f"💬 In-app to user {user_id}: {message}")

    # Save to Dapr state store for user to fetch
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                f"http://localhost:{DAPR_PORT}/v1.0/state/statestore",
                json=[{
                    "key": f"notification-{user_id}",
                    "value": {"message": message, "read": False}
                }]
            )
        except Exception as e:
            print(f"  Error saving notification: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
