import json
import time

import qrcode
import requests
from flask import Flask, render_template, redirect, url_for, request
import base64
import uuid

from db_data import db_session
from db_data.__all_models import Photo, Statistics
import sqlite3
from clear_db import delete_photos, delete_statistics

from random import choices
import datetime
import schedule
import threading

app = Flask(__name__, static_folder="static")

admin_password = 'admin1357'


@app.route("/")
def greetings_screen():
    return render_template('main.html')


@app.route("/camera")
def camera_screen():
    return render_template('second.html')


@app.route("/send", methods=["POST"])
def upload_image():
    try:
        file_name = uuid.uuid1()
        path = f'static/images/{file_name}.png'
        with open('static/images/image.txt', 'w') as file:
            img = request.form['image']
            file.write(img)
        with open('static/images/image.txt', 'rb') as file:
            with open(path, 'wb') as file2:
                img_b64 = file.read()
                file2.write(base64.b64decode(img_b64))
        session = db_session.create_session()
        code = generate_code()
        photo = Photo(
            photo=path,
            code=code,
            time=datetime.datetime.now()
        )
        session.add(photo)
        statistics = Statistics(
            photo=path,
            time=datetime.datetime.now(),
            count_send=0
        )
        session.add(statistics)
        session.commit()
    except Exception:
        return json.dumps({'error': 'Loading has been error'})
    return json.dumps({'success': 'ok', 'img': path, 'code': code})


@app.route("/qr", methods=["GET"])
def qr_code():
    try:
        tgbot_name = 'photobooth1357_bot'
        tgbot_link = f'https://t.me/{tgbot_name}'
        tgbot_qr = qrcode.make(tgbot_link)
        path_tgbot_qr = 'static/images/telegram-qrcode.png'
        tgbot_qr.save(path_tgbot_qr)
    except Exception:
        return json.dumps({'error': 'Loading has been error'})
    return json.dumps({'success': 'ok', 'tglink': path_tgbot_qr})


@app.route("/parser", methods=["GET"])
def get_posts():
    try:
        token = '959d5e65959d5e65959d5e651c968c8f919959d959d5e65f60ec3723e409a0e81b86762'
        version = 5.131
        domain = 'gbou1357'
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': 5
                                }
                                )
        data = response.json()['response']['items']
    except Exception:
        return json.dumps({'error': 'Loading has been error'})
    posts = []
    URL_LOGO = 'static/data/1357_logo.jpg'
    for i in range(3):
        post = {
            'text': data[i]['text'][:200] + '...',
            'attachments': data[i]['attachments'][0]['photo']['sizes'][2]['url'] if 'attachments' in data[i]
                                                                                    and
                                                                                    data[i]['attachments'][0]['photo'][
                                                                                        'sizes'][2]['width'] >
                                                                                    data[i]['attachments'][0]['photo'][
                                                                                        'sizes'][2]['height'] >= 400
                                                                                    and data[i]['attachments'][0]['photo']['sizes'][2]['width'] >= 600
                                                                                    else URL_LOGO,
            'colour': 'white' if 'attachments' in data[i] and data[i]['attachments'][0]['photo']['sizes'][2]['width']
                                 > data[i]['attachments'][0]['photo']['sizes'][2]['height']
                                 >= 400 and data[i]['attachments'][0]['photo']['sizes'][2]['width'] >= 600 else 'black'
        }
        posts.append(post)
    return json.dumps({'success': 'ok',
                       'data': posts})


def run_db():
    db_session.global_init('db/photo-booth.sqlite')


def generate_code():
    code = ''.join(choices(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], k=6))
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    codes = cursor.execute(f'''SELECT code FROM photos''').fetchall()
    if (code,) in codes:
        connection.close()
        return generate_code()
    else:
        connection.close()
        return code


# def change_password():
#     global admin_password
#     admin_password = ''.join(choices('0 1 2 3 4 5 6 7 8 9 q w e r t y u i o p a s d f g h j k l z x c v b n m'.split(), k=8))
#     print(admin_password)


def start():
    run_db()
    app.run()


def sch():
    schedule.every().minutes.do(delete_photos)
    schedule.every().day.at('00:00').do(delete_statistics)
    # schedule.every().day.at('23:40').do(change_password)
    schedule.every(60).minutes.do(get_posts)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    t1 = threading.Thread(target=start)
    t2 = threading.Thread(target=sch)

    t1.start()
    t2.start()
