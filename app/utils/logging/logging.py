import logging
import logging.config
from app.config import settings
from app.utils.logging.log_handlers import LogDispatcher

class ExternalLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.formatter = logging.Formatter(fmt="%(asctime)s", datefmt="%Y-%m-%d %H:%M:%S")

    def emit(self, record):
        log_data = {
            "asctime": self.format(record).strip(),
            "levelname": record.levelname,
            "message": record.getMessage(),
            "extra": getattr(record, "extra", {})
        }

        LogDispatcher.send_to_elasticsearch(log_data)
        LogDispatcher.send_to_sentry(log_data)
        LogDispatcher.send_to_telegram(log_data)

def setup_logging():
    
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG" if settings.DEBUG else "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        }
    }
    
    if settings.EXTERNAL_LOGGING_ENABLED:
        handlers["external"] = {
            "()": ExternalLogHandler,
            "level": "ERROR" 
        }
    
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(error_type)s] [%(endpoint)s] [%(method)s]"
            },
            "simple": {
                "format": "%(levelname)s - %(name)s - %(message)s"
            },
        },
        "handlers": handlers,
        "loggers": {
            "app": {
                "handlers": list(handlers.keys()),
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
        }
    }
    
    logging.config.dictConfig(log_config)
    logging.info("Logging setup complete", extra={"service": "logging"})