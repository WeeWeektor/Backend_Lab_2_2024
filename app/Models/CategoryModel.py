from sqlalchemy import Column, String
from .BaseModel import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "Category"

    category_name = Column(String(50), nullable=False)
    category_description = Column(String(100), nullable=False)
