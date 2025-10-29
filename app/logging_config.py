import logging
from logging.config import dictConfig


def setup_logging() -> None:
    """
    Configure application-wide logging with sensible production defaults.
    Uses JSON-like formatter fields for easier ingestion by log aggregators.
    """
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": (
                        "%(asctime)s %(levelname)s %(name)s "
                        "%(funcName)s:%(lineno)d - %(message)s"
                    )
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "standard",
                }
            },
            "loggers": {
                "uvicorn": {"level": "INFO"},
                "uvicorn.error": {"level": "INFO"},
                "uvicorn.access": {"level": "INFO"},
            },
            "root": {
                "level": "INFO",
                "handlers": ["console"],
            },
        }
    )

    logging.getLogger(__name__).info("Logging configured")


