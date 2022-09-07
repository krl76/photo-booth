from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__, static_folder="static")


@app.route("/", methods = ["GET"])
def first():
    return render_template('main.html')


@app.route("/camera")
def second():
    return render_template('second.html')


@app.route("/send")
def third():
    return "photo qr string"


if __name__ == '__main__':
    app.run(debug=True)
