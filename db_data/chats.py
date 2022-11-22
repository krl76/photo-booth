import sqlalchemy
from .db_session import SqlAlchemyBase


class Chat(SqlAlchemyBase):
    __tablename__ = 'Chats'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    chat_id =sqlalchemy.Column(sqlalchemy.String, unique=True)
    data = sqlalchemy.Column(sqlalchemy.DateTime)
    count_photo = sqlalchemy.Column(sqlalchemy.Float)
