from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "This is index page"

app.run(host="192.168.35.206",port=5000)


