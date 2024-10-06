from api.http_session import HTTPSession
from api.status import status_models
from api.status.status_request import (
    RequestData,
    RequestHeaders
)

from misc.format import format_phone
from misc.utils import extract_orders_data

from typing import List, Any


class StatusAPI(HTTPSession):
    request_headers = RequestHeaders()
    request_data = RequestData()

    @classmethod
    def url(cls) -> str:
        url = cls.request_headers.url
        return url

    @classmethod
    async def user_orders(cls, phone: str) -> List[dict] | list:
        phone = format_phone(phone=phone)
        data = {
            'command': f'{cls.request_data.order}',
            'telefon': f'{phone}'
        }
        data = status_models.OrderModel.model_validate(data)
        response = await cls.post_request(
            url=cls.url(),
            data=data.model_dump()
        )
        orders = extract_orders_data(response=response)
        return orders

    @classmethod
    async def user_flyers(cls, phone: str) -> Any:
        phone = format_phone(phone=phone)
        data = {
            'command': f'{cls.request_data.flyer}',
            'telefon': f'{phone}',
            'project': f'{cls.request_headers.project}'
        }
        data = status_models.FlyerModel.model_validate(data)
        response = await cls.post_request(
            url=cls.url(),
            data=data.model_dump()
        )
        return response

    @classmethod
    async def user_history(cls, phone: str) -> dict[str, str]:
        phone = format_phone(phone=phone)
        data = {
            'command': f'{cls.request_data.history}',
            'telefon': f'{phone}',
            'project': f'{cls.request_headers.project}'
        }
        data = status_models.HistoryModel.model_validate(data)
        response = await cls.post_request(
            url=cls.url(),
            data=data.model_dump()
        )
        return response


status_api = StatusAPI()
