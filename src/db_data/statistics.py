import sqlalchemy
from .db_session import SqlAlchemyBase


class Statistics(SqlAlchemyBase):
    __tablename__ = 'statistics'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo = sqlalchemy.Column(sqlalchemy.String, unique=True)
    time = sqlalchemy.Column(sqlalchemy.DateTime)
    count_send = sqlalchemy.Column(sqlalchemy.Integer)
