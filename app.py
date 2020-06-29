from flask import Flask,request

import json
from random import randint

from config import name_length,pass_length

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
    return name + '#' + passwd


# Basic I/O
@app.route('/<string:name>', methods = ['GET','POST'])
def io(name):
    return name


# Debug
if __name__ == '__main__':
    app.run(debug=True)
