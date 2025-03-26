import logging
from typing import Dict, Any
import httpx
from app.config import settings

class LogDispatcher:
    @staticmethod
    def send_to_elasticsearch(log_data: Dict[str, Any]):
        if not settings.ELASTICSEARCH_URL:
            return
            
        try:
            doc = {
                "@timestamp": log_data.get("asctime"),
                "level": log_data.get("levelname"),
                "message": log_data.get("message"),
                "service": "tron_api",
                **log_data.get("extra", {})
            }
            
            httpx.post(
                f"{settings.ELASTICSEARCH_URL}/logs/_doc",
                json=doc,
                timeout=2
            )
        except Exception as e:
            logging.warning(f"Failed to send log to Elastic: {str(e)}")

    @staticmethod
    def send_to_sentry(log_data: Dict[str, Any]):
        if not settings.SENTRY_DSN or log_data.get("levelname") not in ("ERROR", "CRITICAL"):
            return
            
        try:
            # Здесь будет интеграция с Sentry SDK
            pass
        except Exception as e:
            logging.warning(f"Failed to send log to Sentry: {str(e)}")

    @staticmethod
    def send_to_telegram(log_data: Dict[str, Any]):
        if not settings.TELEGRAM_BOT_TOKEN or log_data.get("levelname") != "CRITICAL":
            return
            
        try:
            message = f"🚨 CRITICAL ERROR\n{log_data.get('message')}"
            httpx.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": settings.TELEGRAM_CHAT_ID,
                    "text": message
                },
                timeout=5
            )
        except Exception as e:
            logging.warning(f"Failed to send log to Telegram: {str(e)}")