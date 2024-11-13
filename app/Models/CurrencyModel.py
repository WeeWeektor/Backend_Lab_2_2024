from sqlalchemy import Column, String
from .BaseModel import BaseModel


class CurrencyModel(BaseModel):
    __tablename__ = "Currency"

    currency_name = Column(String(50), nullable=False)
