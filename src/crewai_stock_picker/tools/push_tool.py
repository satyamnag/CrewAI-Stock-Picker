import os
from typing import Type
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")

class PushNotificationTool(BaseTool):
    name: str = "Send a Push Notification"
    description: str = "This tool is used to send a push notification to the user."
    args_schema: Type[BaseModel] = PushNotification
    def _run(self, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        if not pushover_user or not pushover_token:
            return '{"error": "Missing PUSHOVER_USER or PUSHOVER_TOKEN environment variables"}'
        pushover_url = "https://api.pushover.net/1/messages.json"
        payload = {
            "user": pushover_user,
            "token": pushover_token,
            "message": message,
        }
        try:
            response = requests.post(
                pushover_url,
                data=payload,
                timeout=10,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            return f'{{"notification": "failed", "error": "{str(exc)}"}}'
        return '{"notification": "ok"}'