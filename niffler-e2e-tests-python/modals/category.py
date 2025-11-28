from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from tools.fakers import fake


class Category(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    username: str
    archived: bool


class CategoryAdd(BaseModel):
    name: str = Field(default_factory=fake.text)
    username: str | None = None
    archived: bool | None = None