from flask import Flask, request, url_for, redirect, render_template

import json
from random import randint
import os

from config import name_length, pass_length

if not os.path.isdir('notes'):
    os.mkdir('notes')

app = Flask(__name__)

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
    return redirect(url_for('edit', name=name))


# Basic I/O
@app.route('/<string:name>.edit', methods=['GET', 'POST'])
def edit(name):
    note = get_content(name)
    if request.method == 'GET':
        return render_template('edit.html',
                               note=note,
                               name=name)
    if request.method == 'POST':
        with open('notes/%s' % name, 'w') as f:
            f.write(json.dumps({
                'title': request.form['title'],
                'body': request.form['body']
            }))
            f.close()
            return {'msg': 'OK'}


# Read as Text
@app.route('/<string:name>.note', methods=['GET'])
def read_text(name):
    note = get_content(name)
    return render_template('note.html',
                           note=note,
                           name=name)


# Read as HTML
@app.route('/<string:name>.html', methods=['GET'])
def read_html(name):
    note = get_content(name)
    return render_template('html.html',
                           note=note,
                           name=name)


# Debug
if __name__ == '__main__':
    app.run(debug=True)
