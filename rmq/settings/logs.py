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
    START_PROCESS_MESSAGE = "START PROCESS MESSAGE..."
    CONSUMED_MESSAGE = "CONSUMED MESSAGE: {message}"
    SUCCESSFUL_SEND_MESSAGE = "SUCCESSFUL SEND MESSAGE: {message}"
