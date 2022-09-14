from flask import Flask, render_template, redirect, url_for, request
import base64

app = Flask(__name__, static_folder="static")


@app.route("/")
def first():
    return render_template('main.html')


@app.route("/camera")
def second():
    return render_template('second.html')


@app.route("/send")
def third():
    with open('static/images/image.txt', 'rb') as file:
        with open('static/images/image.png', 'wb') as file2:
            img_b64 = file.read()
            file2.write(base64.b64decode(img_b64))
    return render_template('third.html')


if __name__ == '__main__':
    app.run(debug=True)
