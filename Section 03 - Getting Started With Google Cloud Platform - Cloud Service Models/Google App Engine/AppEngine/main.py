from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    html = "<div style='text-align:center;margin:20px;'><h1>Greetings from KF && Cloud & AI Analytics! </h1><img src='https://storage.googleapis.com/kfbucket2233/desktopwallpapercopy.jpeg' width='40%' alt='Pinehead @ Cloud & AI Analytics'></div>"
    return html


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
