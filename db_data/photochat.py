import sqlalchemy
from .db_session import SqlAlchemyBase


class PhotoChat(SqlAlchemyBase):
    __tablename__ = 'photochat'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    chat_id = sqlalchemy.Column(sqlalchemy.String)
    photo = sqlalchemy.Column(sqlalchemy.String)
