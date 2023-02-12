import sqlite3
import datetime
import os


def delete_photos():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    delete = cursor.execute(
        f'''SELECT photo FROM photos WHERE time<"{datetime.datetime.now() - datetime.timedelta(minutes=15)}"''').fetchall()
    for photo in delete:
        os.remove(photo[0])
    delete = cursor.execute(
        f'''DELETE FROM photos WHERE time<"{datetime.datetime.now() - datetime.timedelta(minutes=15)}"''').fetchall()
    connection.commit()
    connection.close()


def delete_statistics():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    delete = cursor.execute(
        f'''DELETE FROM statistics WHERE time<"{datetime.datetime.now() - datetime.timedelta(weeks=1)}"''').fetchall()
    connection.commit()
    connection.close()


# if __name__ == '__main__':
#     delete_photos()
#     delete_statistics()

