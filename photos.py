import sqlalchemy
from .db_session import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    image = sqlalchemy.Column(sqlalchemy.String, unique=True)
    code = sqlalchemy.Column(sqlalchemy.String, unique=True)
    time = sqlalchemy.Column(sqlalchemy.DateTime)