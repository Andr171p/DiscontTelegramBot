import json

from typing import Any


def json_to_dict(_json) -> Any:
    _json = json.dumps(_json, ensure_ascii=False)
    _dict = json.loads(_json)
    data = _dict['data']
    return data
