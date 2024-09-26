from pydantic import BaseModel


class OrderModel(BaseModel):
    command: str
    telefon: str


class OrdersModel(BaseModel):
    command: str
    active: str = 'true'


class FlyerModel(BaseModel):
    command: str
    telefon: str
    project: str = 'Сушеф.рф'


class HistoryModel(BaseModel):
    command: str
    telefon: str
    project: str = 'Сушеф.рф'
