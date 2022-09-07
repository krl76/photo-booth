from flask import Flask, render_template

app = Flask(__name__, static_folder="static")


@app.route("/")
def first():
    # return 'hello'
    return render_template('main.html')


@app.route("/camera")
def second():
    return "show camera"


@app.route("/send")
def third():
    return "photo qr string"


if __name__ == '__main__':
    app.run(debug=True)
