from collections.abc import Sequence

from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select

from models.category import Category
from models.spend import SpendSQL


class SpendDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_user_categories(self, username: str) -> Sequence[Category]:
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            return session.exec(statement).all()

    def delete_category(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            session.delete(category)
            session.commit()

    def get_user_category(self, category_id: str):
        with Session(self.engine) as session:
            statement = select(Category).where(Category.id == category_id)
            return session.exec(statement).first()

    def get_spend_by_id(self, spend_id: str) -> SpendSQL:
        with Session(self.engine) as session:
            statement = select(SpendSQL).where(SpendSQL.id == spend_id)
            return session.exec(statement).first()

    def get_user_spends(self, username: str):
        with Session(self.engine) as session:
            statement = select(SpendSQL, Category).join(Category, SpendSQL.category_id == Category.id).where(
                SpendSQL.username == username)
            result = session.exec(statement).all()
            return result