import base64
import datetime
import io
import json
import os
import threading
import time
import uuid
from random import choices

import qrcode
import requests
import schedule
from PIL import Image
from PIL.Image import Transpose
from flask import Flask, render_template, request, url_for

from clear_db import delete_photos, delete_statistics
from db_data import db_session
from db_data.__all_models import Photo, Statistics
from settings import DB_NAME, BASE_DIR

app = Flask(__name__, static_folder="static")
app.debug = False

admin_password = 'admin1357!!!'


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
        path = os.path.join(BASE_DIR, 'static', 'images', f'{file_name}.png')

        fon = Image.open(os.path.join(BASE_DIR, 'static', 'img', 'frames', f'2.png'))
        bf = io.BytesIO(base64.b64decode(request.form['image']))
        image = Image.open(bf).transpose(method=Transpose.FLIP_LEFT_RIGHT)
        image.paste(fon, (0, 0), mask=fon)
        image.save(path)
        image.close()
        fon.close()
        # end
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
        session.close()
    except Exception as ex:
        print(ex)
        return json.dumps({'error': 'Loading has been error'})
    return json.dumps({'success': 'ok', 'img': f'{file_name}.png', 'code': code})


@app.route("/qr", methods=["GET"])
def qr_code():
    try:
        tgbot_name = 'PhotoKiosk1357Bot'
        tgbot_link = f'https://t.me/{tgbot_name}'
        tgbot_qr = qrcode.make(tgbot_link)
        path_tgbot_qr = 'src/static/images/qr-code-tg-bot.png'
        tgbot_qr.save(path_tgbot_qr)
    except Exception:
        return json.dumps({'error': 'Loadng has been error'})
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
    URL_LOGO = url_for('static', filename='data/1357_logo.jpg')
    for i in range(3):
        flag = False
        if 'attachments' in data[i] and len(data[i]['attachments']) > 0:
            if 'photo' in data[i]['attachments'][0]:
                photo = data[i]['attachments'][0]['photo']['sizes'][2]
                if photo['width'] > photo['height'] >= 400 and photo['width'] >= 600:
                    flag = True
        post = {
            'text': f"{data[i]['text'][:200]}...",
            'attachments': data[i]['attachments'][0]['photo']['sizes'][2]['url'] if flag else URL_LOGO,
            'colour': 'white' if flag else 'black'
        }
        posts.append(post)
    return json.dumps({'success': 'ok', 'data': posts})


def run_db():
    db_session.global_init(DB_NAME)


def generate_code():
    code = ''.join(choices('1234567890', k=6))
    session = db_session.create_session()
    codes = [el[0] for el in session.query(Photo.code).all()]
    while code in codes:
        code = ''.join(choices('1234567890', k=6))
    session.close()
    return code


# def change_password():
#     global admin_password
#     admin_password = ''.join(choices('0123456789qwertyuiopasdfghjklzxcvbnm', k=8))
#     print(admin_password)


def start():
    run_db()
    app.run()


def sch():
    schedule.every().minutes.do(delete_photos)
    schedule.every().day.at('00:00').do(delete_statistics)
    # schedule.every().day.at('23:40').do(change_password)
    schedule.every(1).hours.do(get_posts)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    t1 = threading.Thread(target=start)
    t2 = threading.Thread(target=sch)

    t1.start()
    t2.start()
    # run_db()
    # app.run()
