import json
from loguru import logger
from typing import List, Any

from misc.tamplates import MessageTemplate


def json_to_dict(_json) -> Any:
    _json = json.dumps(_json, ensure_ascii=False)
    _dict = json.loads(_json)
    data = _dict['data']
    return data


def order_to_message(order: dict) -> dict:
    template = MessageTemplate(order=order)
    message = template.message()
    return message


def extract_orders_data(response: str) -> List[dict] | list:
    if response is not None:
        _json = json.dumps(response, ensure_ascii=False)
        _dict = json.loads(_json)
        orders = _dict['data']['orders']
        logger.info(orders)
        return orders
    else:
        logger.warning("JSON RESPONSE IS NONE...")
        _empty = []
        return _empty
