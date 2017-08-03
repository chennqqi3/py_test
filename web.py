# coding=utf-8
from flask import Flask
from flask.ext.cors import CORS

from action import upload

app = Flask(__name__)
CORS(app)

upload_action = upload.Upload()


@app.route('/upload/<action>', methods=['GET', 'POST'])
def upload(action=None):
    op = getattr(upload_action, action, None)
    if callable(op):
        return op()
    else:
        return 'Action not found'


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
