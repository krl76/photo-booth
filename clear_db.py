import sqlite3
import datetime


def delete_photos():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    delete = cursor.execute(
        f'''DELETE FROM photos WHERE time<"{datetime.datetime.now() - datetime.timedelta(minutes=10)}"''').fetchall()
    connection.commit()
    connection.close()


def delete_statistics():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    delete = cursor.execute(
        f'''DELETE FROM statistics WHERE time<"{datetime.datetime.now() - datetime.timedelta(weeks=1)}"''').fetchall()
    connection.commit()
    connection.close()

