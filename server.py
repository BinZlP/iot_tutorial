from flask import Flask
import threading
import server_runtime

app = Flask(__name__)


@app.route('/')
def index():
    return "Server runtime: "+str(server_runtime.runtime)+"s"

# Normal routing
@app.route('/board')
def board():
    return "normal board"

# Get a parameter from URL
@app.route('/board/<article_idx>')
def board_view(article_idx):
    return article_idx

# Function 'board_view' does the role of the end-point
@app.route('/boards',defaults={'page':'index'})
@app.route('/boards/<page>')
def boards(page):
    return "Page: "+page


app.run(host="192.168.35.206",port=5000)
