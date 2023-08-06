# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import hmac
import hashlib
import codecs
import base64
import six
import six.moves.urllib as urllib
import traceback

home_path = os.path.expanduser('~')
cache_path = os.path.join(home_path, '.dding')
file_name = cache_path + '/config.json'


def http_post(url, content):
    """
    http posts
    :param url:
    :param content:
    :return:
    """
    try:
        headers = {'Content-Type': 'application/json'}
        data = {"msgtype": "text", "text": {"content": content}}
        req = urllib.request.Request(url=url, headers=headers, data=json.dumps(data).encode())
        response = urllib.request.urlopen(req)
        res = response.read()
        print(res.decode("utf8"))
    except Exception as e:
        print(e)


def init():
    """
    初始化
    :return:
    """
    lst = []
    print("help url: https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq")
    token = six.moves.input("input token:")
    secret = six.moves.input("input secret:")
    if token == "" or secret == "":
        print("token or secret empty!! please check")
        sys.exit(1)
    else:
        if len(token) > 65:
            token = token[-64:]
        lst.append({
            'group': 'default',
            'token': token,
            'secret': secret
        })

    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
    save_config(lst)
    return read_config()


def read_config():
    return json.load(codecs.open(file_name, 'r', 'utf-8'))


def save_config(content):
    return json.dump(content, codecs.open(file_name, 'w', 'utf-8'), sort_keys=True, indent=4, separators=(',', ':'))


def check_config():
    dic = {}
    if not os.path.exists(file_name):
        lst = init()
    else:
        lst = read_config()
    for item in lst:
        dic[item['group']] = item
    return dic


def notify_dding(group='default', content=''):
    try:
        dic = check_config()
        token = dic[group]['token']
        secret = dic[group]['secret']
        print("-" * 60)
        print('group:\t%s' % (group))
        print('token:\t%s' % (token))
        print('secret:\t%s' % (secret))
        print("-" * 60)
        accesstoken_url = 'https://oapi.dingtalk.com/robot/send?access_token='
        timestamp = int(round(time.time() * 1000))
        secret_enc = secret.encode()
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode()
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        url = '%s%s&timestamp=%s&sign=%s' % (accesstoken_url, token, timestamp, sign)
        http_post(url, content)
    except Exception as e:
        traceback.print_exc()
        print(e)


def main():
    group = 'default'
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

    if len(sys.argv) > 2:
        _, group, content = sys.argv
    else:
        content = sys.argv[1]
    notify_dding(group, content)


def usage():
    print("usage: dding group=[custom name] contenet=hello")
    print("example: dding helloworld")


if __name__ == '__main__':
    main()
