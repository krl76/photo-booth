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

app = Flask(__name__, static_folder="static")


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
            'text': data[i]['text'],
            'attachments': data[i]['attachments'][0]['photo']['sizes'][2]['url'] if 'attachments' in data[i] else URL_LOGO
        }
        posts.append(post)

        if 'attachments' in data[i]:

            posts[f'text_{i + 1}'] = data[i]['text']
            posts[f'attachments_{i + 1}'] = data[i]['attachments'][0]['photo']['sizes'][2]['url']
            posts[f'colour_{i + 1}'] = 'white'
        else:
            posts[f'text_{i + 1}'] = data[i]['text']
            posts[f'attachments_{i + 1}'] = 'static/data/1357_logo.jpg'
            posts[f'colour_{i + 1}'] = 'black'
    return json.dumps({'success': 'ok',
                       'data': [
                           {
                               'text': posts['text_1'],
                               'attachments': posts['attachments_1'],
                            }
                       ]})
                       # 'text_1': posts['text_1'], 'attachments_1': posts['attachments_1'], 'colour_1': posts['colour_1'],
                       # 'text_2': posts['text_2'], 'attachments_2': posts['attachments_2'], 'colour_2': posts['colour_2'],
                       # 'text_3': posts['text_3'], 'attachments_3': posts['attachments_3'], 'colour_3': posts['colour_3']})


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


if __name__ == '__main__':
    schedule.every(1).minutes.do(delete_photos)
    schedule.every().day.at('00:00').do(delete_statistics)
    schedule.every(60).minutes.do(get_posts)
    run_db()
    app.run(debug=True)
    while True:
        schedule.run_pending()
        time.sleep(1)
