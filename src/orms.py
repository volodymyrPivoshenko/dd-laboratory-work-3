"""
ORMs for SQLAlchemy and API.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Numeric
from pydantic import BaseModel
from typing import List


class DrugsTable(declarative_base()):
    """
    ORM for SQLAlchemy.
    """

    __tablename__ = "drugs"

    code = Column("code", Numeric, nullable=True, primary_key=True)
    barcode = Column("barcode", Numeric, nullable=True)
    name = Column("name", String(64), nullable=True)
    producer = Column("producer", String(64), nullable=True)
    tax = Column("tax", Numeric, nullable=True)
    price = Column("price", Numeric, nullable=True)
    quantity = Column("quantity", Numeric, nullable=True)
    price_reserve = Column("price_reserve", Numeric, nullable=True)
    price_reserve_order = Column("price_reserve_order", Numeric, nullable=True)


class DrugModel(BaseModel):
    """
    Model for `drug` endpoint.
    """

    code: float
    barcode: float
    name: str
    producer: str
    tax: float
    price: float
    quantity: float
    price_reserve: float
    price_reserve_order: float


class DrugsModel(BaseModel):
    """
    Model for `all` endpoint.
    """

    drugs: List[DrugModel]


class InputModel(BaseModel):
    """
    Model for `drug` input.
    """

    code: float
