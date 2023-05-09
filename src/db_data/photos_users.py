import sqlalchemy
from .db_session import SqlAlchemyBase


class PhotoUser(SqlAlchemyBase):
    __tablename__ = 'photosusers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    photo = sqlalchemy.Column(sqlalchemy.String)
