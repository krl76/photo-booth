from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__, static_folder="static")


@app.route("/")
def first():
    return render_template('main.html')


@app.route("/camera")
def second():
    return render_template('second.html')


@app.route("/send")
def third():
    # with open('image.txt') as file:
    return render_template('third.html')


if __name__ == '__main__':
    app.run(debug=True)
