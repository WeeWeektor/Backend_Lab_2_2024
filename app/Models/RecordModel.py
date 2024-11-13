from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .BaseModel import BaseModel
from .UserModel import UserModel
from .CategoryModel import CategoryModel
from .CurrencyModel import CurrencyModel


class RecordModel(BaseModel):
    __tablename__ = "Record"

    user_id = Column(UUID(as_uuid=True), ForeignKey('User.id'), nullable=False)
    user = relationship('UserModel', back_populates='Records')

    category_id = Column(UUID(as_uuid=True), ForeignKey('Category.id'), nullable=False)
    category = relationship('CategoryModel', back_populates='Records')

    date = Column(DateTime, nullable=False)
    total_price = Column(Numeric, nullable=False)

    currency_id = Column(UUID(as_uuid=True), ForeignKey('Currency.id'), nullable=True)
    currency = relationship('CurrencyModel')


UserModel.records = relationship('RecordModel', back_populates='User')
CategoryModel.records = relationship('RecordModel', back_populates='Category')
