import sys

from loguru import logger


logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    filter="sub.module",
    level="INFO"
)


class RequestLoggingMessage:
    successful_response = "HTTP REQUEST SENT SUCCESSFULLY"
    none_json_response = "RESPONSE IS NONE VALUE"
