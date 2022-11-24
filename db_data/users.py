import sqlalchemy
from .db_session import SqlAlchemyBase

import datetime


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    ADMIN = 1
    USER = 2

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    status = sqlalchemy.Column(sqlalchemy.String, default=USER)
    date_registration = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    count_photo = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    date_last_using = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
