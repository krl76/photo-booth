import json
import qrcode
from flask import Flask, render_template, redirect, url_for, request
import base64
import uuid
from db_data import db_session
from db_data.photos import Photo
from random import choices

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
        db = db_session.create_session()
        photo = Photo()
        photo.photo = path
        generate_code = ''.join(choices(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], k=6))
        photo.code = generate_code
        db.add(photo)
        db.commit()
    except Exception:
        return json.dumps({'error': 'Loading has been error'})
    return json.dumps({'success': 'ok', 'img': path, 'code': generate_code})


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


def run_db():
    db_session.global_init('db/photo-booth.sqlite')
    app.run()


if __name__ == '__main__':
    run_db()
    app.run(debug=True)