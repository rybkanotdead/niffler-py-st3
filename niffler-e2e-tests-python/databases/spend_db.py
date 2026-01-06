import uuid
from typing import Sequence
from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select
from modals.spend import SpendSQL
from modals.category import CategorySQL
from modals.config import Envs
from utils.allure_helpers import attach_sql


class SpendDb:
    """Клиент для взаимодействия с БД"""

    engine: Engine

    def __init__(self, envs: Envs) -> object:
        self.engine = create_engine(envs.spend_db_url)
        event.listen(self.engine, "do_execute", fn=attach_sql)

    def get_user_categories(self, username: str) -> Sequence[CategorySQL]:
        with Session(self.engine) as session:
            statement = select(CategorySQL).where(CategorySQL.username == username)
            return session.exec(statement).all()

    def add_user_category(self, username: str, category_name: str) -> CategorySQL:
        with Session(self.engine) as session:
            new_category = CategorySQL(
                id=str(uuid.uuid4()),
                name=category_name,
                username=username
            )

            session.add(new_category)
            session.commit()
            session.refresh(new_category)

            return new_category

    def get_category_by_name(self, username: str, category_name: str) -> CategorySQL:
        with Session(self.engine) as session:
            category = select(CategorySQL).where(
                CategorySQL.username == username,
                CategorySQL.name == category_name
            )
            return session.exec(category).first()

    def get_category_by_id(self, category_id: str) -> CategorySQL:
        with Session(self.engine) as session:
            category = select(CategorySQL).where(CategorySQL.id == category_id)
            return session.exec(category).first()

    def delete_category(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(CategorySQL, category_id)
            session.delete(category)
            session.commit()

    def get_spend_in_db(self, username: str):
        with Session(self.engine) as session:
            spend = select(SpendSQL).where(SpendSQL.username == username)
            result = session.exec(spend).all()
            return result