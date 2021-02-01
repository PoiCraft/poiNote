from flask import Flask, request, url_for, redirect, render_template
from flask_sockets import Sockets

import json
from random import randint
import os

from geventwebsocket.websocket import WebSocket

from config import name_length
from ws_utils import WebSocketCollector

if not os.path.isdir('notes'):
    os.mkdir('notes')

app = Flask(__name__, static_folder='static')
socket = Sockets(app)

ws_c = WebSocketCollector()

name_list = '1244567890abcdefghijklmnopqrstuvwxyz'


def get_content(name):
    if not os.path.isfile('notes/%s' % name):
        with open('notes/%s' % name, 'w') as f:
            f.write(json.dumps({
                'title': 'Untitled Note',
                'body': '',
            }))
            f.close()
    with open('notes/%s' % name, 'r') as f:
        body = f.read()
        f.close()
        note = json.loads(body)
    return note


# Index
@app.route('/', methods=['GET'])
def index():
    # get Name
    name = ''
    for _ in range(name_length):
        name += name_list[randint(0, len(name_list) - 1)]
    print(f"[HOME] new note <{name}>")
    return redirect(url_for('edit', name=name))


# Basic I/O
@app.route('/<string:name>.edit', methods=['GET', 'POST'])
def edit(name):
    note = get_content(name)
    print(f"[EDIT] edit note <{name}>")
    if request.method == 'GET':
        return render_template('edit.html',
                               note=note,
                               name=name)
    if request.method == 'POST':
        print(f"[POST] edit note <{name}>")
        with open('notes/%s' % name, 'w') as f:
            f.write(json.dumps({
                'title': request.form['title'],
                'body': request.form['body']
            }))
            f.close()
            return {'msg': 'OK'}


# WebSocket Web I/O
@app.route('/<string:name>.ws', methods=['GET'])
def edit_ws(name):
    note = get_content(name)
    return render_template('ws.html',
                           note=note,
                           name=name)


# Websocket I/O
@socket.route('/ws')
def ws_io(ws: WebSocket):
    while not ws.closed:
        content = ws.receive()
        if content is not None:
            note = json.loads(content)
            print(f"[WS] reach note <{note['name']}>")
            ws_c.add(ws, note['name'])
            with open('notes/%s' % note['name'], 'w') as f:
                f.write(json.dumps({
                    'title': note['title'],
                    'body': note['body']
                }))
                f.close()
            ws_c.sent_to_all(note['name'], note['title'], note['body'])


# Read as Text
@app.route('/<string:name>.note', methods=['GET'])
def read_text(name):
    print(f"[TEXT] read note <{name}>")
    note = get_content(name)
    return render_template('note.html',
                           note=note,
                           name=name)


# Read as HTML
@app.route('/<string:name>.html', methods=['GET'])
def read_html(name):
    print(f"[HTML] read note <{name}>")
    note = get_content(name)
    return render_template('html.html',
                           note=note,
                           name=name)


# Debug
if __name__ == '__main__':
    app.run(debug=True)
