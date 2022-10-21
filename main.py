import json
import qrcode
from flask import Flask, render_template, redirect, url_for, request
import base64
from time import sleep
import uuid

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
    except Exception:
        return json.dumps({'error': 'При загрузке произошла ошибка'})
    return json.dumps({'success': 'ok', 'img': path})


@app.route("/qr", methods=["GET"])
def qr_code():
    try:
        tgbot_name = 'photobooth1357_bot'
        tgbot_link = f'https://t.me/{tgbot_name}'
        tgbot_qr = qrcode.make(tgbot_link)
        path_tgbot_qr = '/static/images/telegram-qrcode.png'
        tgbot_qr.save('/static/images/telegram-qrcode.png')
    except Exception:
        return json.dumps({'error': 'При загрузке произошла ошибка'})
    return json.dumps({'success': 'ok', 'tglink': path_tgbot_qr})


if __name__ == '__main__':
    app.run(debug=True)
