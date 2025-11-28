from datetime import datetime
from pydantic import BaseModel

from models.category import CategoryAdd, Category
from sqlmodel import Field, SQLModel
from tools.fakers import fake


class Spend(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: Category
    spendDate: datetime
    currency: str
    username: str


class SpendAdd(BaseModel):
    amount: float = Field(default_factory=fake.integer)
    description: str = Field(default_factory=fake.text)
    category: CategoryAdd
    spendDate: str = Field(default_factory=fake.data)
    currency: str | None = Field(default="RUB")


class SpendSQL(SQLModel, table=True):
    __tablename__ = 'spend'
    id: str | None = Field(default=None, primary_key=True)
    username: str
    amount: float
    description: str
    category_id: str = Field(foreign_key="category.id")
    spend_date: datetime
    currency: str