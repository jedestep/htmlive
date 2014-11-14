from flask import Flask, render_template
from flask.ext.socketio import SocketIO,send,emit

import sys

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('my event')
def do_my_event(json):
    print 'received event:', json

@socketio.on('_read')
def do_read(json):
    print 'input command now'
    text = sys.stdin.readline()
    emit('_write',{'html': text})

if __name__ == '__main__':
    socketio.run(app)
