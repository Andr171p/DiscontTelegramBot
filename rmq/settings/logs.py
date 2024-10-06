import sys

from loguru import logger


logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    filter="sub.module",
    level="INFO"
)


class RMQLoggingMessage:
    START_CONSUMING = "RMQ START CONSUMING..."
    START_RECEIVING = "RMQ START RECEIVING..."
    STOP_RECEIVING = "RMQ STOP RECEIVING..."
    SUCCESSFUL_CONNECT = "RMQ SUCCESSFUL CONNECT..."
    START_PROCESS_MESSAGE = "RMQ START PROCESS MESSAGE..."
    CONSUMED_MESSAGE = "RMQ CONSUMED MESSAGE: {message}"
    SUCCESSFUL_SEND_MESSAGE = "RMQ SUCCESSFUL SEND MESSAGE: {message}"
    QUEUE_CREATED = "RMQ QUEUE CREATED: {queue}"
    SUCCESSFULLY_CLOSED = "RMQ SUCCESSFULLY CLOSED..."
