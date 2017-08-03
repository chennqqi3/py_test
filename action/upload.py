# coding=utf-8
import os
import uuid

from flask import request


upload_dir = 'd:/data/static/img/'

static_url = 'http://static.capvision.cn'


class Upload:

    def __init__(self):
        pass

    @staticmethod
    def img():
        f = request.files['file']
        f_path = os.path.join(upload_dir, uuid.uuid4().urn[9:] + '.jpg')
        f.save(f_path)
        return static_url + f_path[12:]
