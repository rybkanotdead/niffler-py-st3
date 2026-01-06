from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class CategorySQL(SQLModel, table=True):
    __tablename__ = "category"
    id: str = Field(default=None, primary_key=True)
    name: str
    username: str
    archived: bool = Field(default=False)


class CategoryAdd(BaseModel):
    name: str
    username: str | None = None
    archived: bool | None = None