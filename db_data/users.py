import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    date_registration = sqlalchemy.Column(sqlalchemy.DateTime)
    date_last_using = sqlalchemy.Column(sqlalchemy.DateTime)
    count_photo = sqlalchemy.Column(sqlalchemy.Integer)
