# -*- coding:UTF-8 -*-
from flask import Flask
import os
from flask import request  # 获取参数
from parseImage import ParseImage;
from pyModules import parseImage

app = Flask(__name__)


@app.route('/check', methods=['GET'])
def check():
    return 'ok'


@app.route('/api/', methods=['GET'])
def get_image():
    try:
        print('请求接口====>' + request.args.get('url'))
        ap = os.path.split(os.path.realpath(__file__))[0] + '/image/'
        downUrl = request.args.get('url')
        pid = downUrl[downUrl.rindex('/') + 1:len(downUrl)]
        cookie = request.args.get('cookie')
        parseSelf = ParseImage(pid, downUrl, cookie)
        if not os.path.exists(ap):
            os.makedirs(ap)
        flag = parseImage.parseGif(self=parseSelf)
        if not flag:
            flag = parseImage.parseMany(self=parseSelf)
        if not flag:
            parseImage.parseOne(self=parseSelf)
    except IOError:
        return 'failed'

    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
