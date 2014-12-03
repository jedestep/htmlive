from flask import Flask, Response, render_template
from time import sleep

import os
import sys
import signal

MONITOR_PATH = 'templates/out.html'

app = Flask(__name__)

going = True

def stopGoing(signum,frame):
    going = False
    exit(0)

def evstream():
    last_change = ''
    while going:
        try:
            stats = os.stat(MONITOR_PATH)
            if stats.st_ctime != last_change:
                last_change = stats.st_ctime
                yield 'data: refresh\n\n'
                print 'heard about a change'
            sleep(1)
        except KeyboardInterrupt:
            break

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/show')
def show():
    return render_template("out.html")

@app.route('/stream')
def stream():
    return Response(evstream(),
                    mimetype='text/event-stream')

if __name__ == '__main__':
    signal.signal(signal.SIGINT,stopGoing)
    signal.signal(signal.SIGABRT,stopGoing)
    signal.signal(signal.SIGQUIT,stopGoing)
    signal.signal(signal.SIGHUP,stopGoing)
    signal.signal(signal.SIGTERM,stopGoing)
    app.debug = True
    app.run(threaded=True)
