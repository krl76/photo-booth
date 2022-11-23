import sqlite3
import datetime


def delete_photo():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    delete = cursor.execute(
        f'''DELETE FROM photos WHERE time<"{datetime.datetime.now() - datetime.timedelta(minutes=10)}"''').fetchall()
    connection.commit()
    connection.close()


if __name__ == '__main__':
    delete_photo()
