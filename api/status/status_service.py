from api.http_session import HTTPSession
from api.status import status_models
from api.status.status_request import (
    RequestData,
    RequestHeaders
)

from misc.format import format_phone
from misc.utils import extract_orders_data

from typing import List


'''class StatusAPI(HTTPSession):
    status_request = StatusRequest
    end_points = StatusEndPoints

    def url(self, end_point: str) -> str:
        url = f"{self.status_request.STATUS_URL}{self.status_request.PREFIX}{end_point}"
        return url

    async def user_orders(self, phone: str) -> List[dict]:
        url = self.url(end_point=self.end_points.USER_ORDERS)
        data = {
            'telefon': phone
        }
        response = await self.post_request(
            url=url,
            data=data
        )
        orders = json_to_dict(_json=response)
        return orders

    async def user_flyers(self, phone: str) -> str:
        url = self.url(end_point=self.end_points.USER_FLYERS)
        data = {
            'telefon': phone
        }
        response = await self.post_request(
            url=url,
            data=data
        )
        flyers = json_to_dict(_json=response)
        return flyers


status_api = StatusAPI()'''


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
    async def user_flyers(cls, phone: str):
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
    async def user_history(cls, phone: str):
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
