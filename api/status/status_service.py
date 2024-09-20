from api.http_session import HTTPSession
from api.status.status_request import (
    StatusRequest,
    StatusEndPoints
)

from misc.utils import json_to_dict

from typing import List


class StatusAPI(HTTPSession):
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


status_api = StatusAPI()
