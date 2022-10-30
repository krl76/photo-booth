import sqlite3


def delete_photo():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    cursor.execute(f'DELETE * FROM photos')
