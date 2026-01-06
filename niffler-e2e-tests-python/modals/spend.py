from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime
from modals.category import CategorySQL


class SpendSQL(SQLModel, table=True):
    __tablename__ = "spend"
    id: str = Field(default=None, primary_key=True)
    username: str
    amount: float
    description: str
    category_id: str = Field(foreign_key="category.id")
    spend_date: datetime
    currency: str


class Spend(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: CategorySQL
    spendDate: datetime
    currency: str
    username: str


class SpendAdd(BaseModel):
    amount: float
    description: str
    category: dict
    spendDate: str
    currency: str


class SpendEdit(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: dict
    spendDate: str
    currency: str