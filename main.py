import json

from flask import Flask, render_template, redirect, url_for, request
import base64
from time import sleep
import uuid

app = Flask(__name__, static_folder="static")


@app.route("/")
def first():
    return render_template('main.html')


@app.route("/camera")
def second():
    return render_template('second.html')


# @app.route("/image", methods=["GET", "POST"])
# def upload_image():
#     if request.method == 'POST':
#         with open('static/images/image.txt', 'w') as file:
#             img = request.form['image']
#             file.write(img)
#         with open('static/images/image.txt', 'rb') as file:
#             with open('static/images/image.png', 'wb') as file2:
#                 img_b64 = file.read()
#                 file2.write(base64.b64decode(img_b64))
#         sleep(0.5)
#         return redirect(url_for('send'))


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


if __name__ == '__main__':
    app.run(debug=True)
