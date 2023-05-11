import sqlite3
import datetime
import os

from db_data import db_session
from db_data.photos import Photo
from settings import DB_NAME


def delete_photos():
    db_session.global_init(DB_NAME)
    delta = datetime.datetime.now() - datetime.timedelta(minutes=15)
    db_sess = db_session.create_session()
    photos = db_sess.query(Photo.photo).filter(Photo.time < delta).all()
    for photo in photos:
        os.remove(photo[0])

    db_sess.query(Photo).filter(Photo.time < delta).delete()
    db_sess.commit()


def delete_statistics():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    delete = cursor.execute(
        f'''DELETE FROM statistics WHERE time<"{datetime.datetime.now() - datetime.timedelta(weeks=1)}"''').fetchall()
    connection.commit()
    connection.close()

if __name__ == '__main__':
    delete_photos()
    # delete_statistics()
