import sqlalchemy
from .db_session import SqlAlchemyBase


class CommentAdmin(SqlAlchemyBase):
    __tablename__ = 'commentsadmins'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    admin = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    commnets = sqlalchemy.Column(sqlalchemy.Integer)
