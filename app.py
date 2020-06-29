from flask import Flask,request,url_for,redirect

import json
from random import randint
import os

from config import name_length,pass_length

if not os.path.isdir('notes'):
    os.mkdir('notes')

app = Flask(__name__)

name_list = '1244567890abcdefghijklmnopqrstuvwxyz'
pass_list = '1234567890abcdefghijklmnopqrstivwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-@)(!;:'

# Index
@app.route('/', methods = ['GET'])
def index():
    # get Name
    name = ''
    for _ in range(name_length):
        name += name_list[randint(0,len(name_list) - 1)]
    # get password
    passwd = ''
    for _ in range(pass_length):
        passwd += pass_list[randint(0,len(pass_list) - 1)]
    return redirect(url_for('io',name = name) + '#' + passwd)


# Basic I/O
@app.route('/<string:name>.note', methods = ['GET','POST'])
def io(name):
    note_new = False
    if not os.path.isfile('notes/%s'%name):
        with open('notes/%s'%name,'w') as f:
            f.write(json.dumps({'md5':'','body':''}))
            f.close()
        note_new = True
    if request.method == 'GET':
        with open('notes/%s'%name,'r') as f:
            body = f.read()
            f.close()
            return body
    if request.method == 'POST':
        with open('notes/%s'%name,'w') as f:
            f.write(json.dumps({
                'md5':request.form['md5'],
                'body':request.form['body']
                }))
            f.close()
            return {'msg':'OK'}

# Debug
if __name__ == '__main__':
    app.run(debug=True)
