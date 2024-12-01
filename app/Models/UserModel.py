from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
from .CurrencyModel import CurrencyModel

class UserModel(BaseModel):
    __tablename__ = "User"

    user_name = Column(String(50), nullable=False)
    currency_id = Column(UUID(as_uuid=True), ForeignKey('Currency.id'), nullable=True)
    currency = relationship('CurrencyModel', back_populates='users')
    password = Column(String, nullable=False)


CurrencyModel.users = relationship('UserModel', back_populates='currency')
