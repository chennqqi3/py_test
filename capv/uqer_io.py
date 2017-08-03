#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import requests
import json

host = 'https://gw.wmcloud.com'
path_anonymous = '/usermaster/captcha.json'
path_sso = '/usermaster/authenticate/v1.json'
path_upload = '/mercury/api/databooks'


def get_remote_token(username='3042149420@qq.com', password='asdf1234'):
    cookies_anonymous = requests.get(host + path_anonymous).cookies
    print('cloud-anonymous-token', cookies_anonymous['cloud-anonymous-token'])
    cookies_sso = requests.post(host + path_sso,
                                data={'username': username, 'password': password, 'rememberMe': True},
                                cookies=cookies_anonymous).cookies
    print ('cloud-sso-token', cookies_sso['cloud-sso-token'])
    return {
        'cloud-anonymous-token': cookies_anonymous['cloud-anonymous-token'],
        'cloud-sso-token': cookies_sso['cloud-sso-token']
    }


def get_local_token():
    with open('token.json') as token_file:
        return json.load(token_file)


def save_local_token(token):
    token_file = open('token.json', 'w')
    token_file.write(json.dumps(token))
    token_file.close()


def upload(file_path):
    cookies = get_local_token()
    result = enroll(file_path, cookies)

    if 'code' in result and result['code'] == -403:
        print result['message']
        cookies = get_remote_token()
        save_local_token(cookies)
        result = enroll(file_path, cookies)
    return result


def enroll(file_path, cookies):
    response = requests.post(host + path_upload,
                             files={'datafile': open(file_path, 'rb')},
                             cookies=cookies)

    #response.encoding='gbk'
    print (response.text)
    return json.loads(response.text)

#cookies = get_remote_token()
#save_local_token(cookies) 


#upload(u'abc.txt')

