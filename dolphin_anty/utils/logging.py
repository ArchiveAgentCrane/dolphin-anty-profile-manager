"""structlog wiring — pretty in dev, JSON in prod."""

from __future__ import annotations

import logging
import os
import sys

import structlog


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(stream=sys.stdout, level=level.upper(), format="%(message)s")
    renderer = (
        structlog.processors.JSONRenderer()
        if os.environ.get("DAPM_LOG_JSON") == "1"
        else structlog.dev.ConsoleRenderer(colors=True)
    )
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level.upper(), 20)),
        cache_logger_on_first_use=True,
    )