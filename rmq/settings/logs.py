import sys

from loguru import logger


logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    filter="sub.module",
    level="INFO"
)


class RMQLoggingMessage:
    START_CONSUMING = "START CONSUMING..."
    SUCCESSFUL_CONNECT = "SUCCESSFUL CONNECT..."
