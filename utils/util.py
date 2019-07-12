import random
import re
import arrow
import base64
from urllib import parse
from flask import current_app
import requests
from api.config import load_config
config = load_config()
user_info_user = config.USER_URL
activity_join_url = config.ACTIVITY_JOIN_URL
badge_gain_url = config.BADGE_GAIN_URL
verify_sid_url = config.CHECK_SESSION
upload_cdn_url = config.UPLOAD_CDN_URL


def get_uid_info(uid):
    pass
    # if uid is None:
    #     return ['', '']
    # cursor = joyuser_db.cursor()
    # 拿到成员id，查询名字
    # sql = ''' select nick, headerurl from usr_user where uid = {} '''.format(uid)
    # cursor.execute(sql)
    # info = cursor.fetchone()
    # if info:
    #     nick = info[0]
    #     url = info[1]
    # else:
    #     nick = url = ''
    # cursor.close()
    # return [nick, url]


def req_get_uid_info(uid):
    # return ['测试', 'http://linked-runner-upyun.thejoyrun.com/linked-runner/u_111_avatar_20160830_090229_6807.jpg']
    url = user_info_user.format(user=uid)
    req = requests.get(url)
    # print(req.text, 'req_get_uid_info')
    if req.status_code != 200:
        print('req_get_uid_info != 200')
        return ['', '']
    try:
        j = req.json()
        if j.get('ret', None) != '0':
            return ['', '']
        data = j.get('data', None)
        if data is None:
            return ['', '']
        return [data['nick'], data['faceUrl']]
    except Exception as e:
        return ['', '']


def req_user_join_activity(uid, activity_id=2443):
    req = requests.post(activity_join_url, data=dict(uid=uid, activity_id=activity_id, secret='bpjCw8BCh5'))
    print(req.text, 'req_user_join_activity')
    if req.status_code != 200:
        print('req_user_join_activity != 200')
        return None
    return True


def req_user_gain_achievement(uid, achievement_id=31961):
    req = requests.post(badge_gain_url, json=dict(uid=uid, badgeId=achievement_id))
    print(req.text, 'req_user_gain_achievement')
    if req.status_code != 200:
        print('req_user_gain_achievement != 200')
        return None
    if req.json().get('ret') == "0":
        return True
    return False


def req_verify_sid(uid, sid):
    url = verify_sid_url.format(uid=uid, sid=sid)
    req = requests.get(url)
    print(req.text, 'req_verify_sid')
    if req.status_code != 200:
        print('req_verify_sid != 200')
    try:
        j = req.json()
        if j.get('data') is True:
            return True
        return False
    except Exception as e:
        print(e)
        return False


def parse_cookie(cookie):
    try:
        result = parse.parse_qs(cookie)
        if not isinstance(result, dict):
            print('rresult is not dict')
            return [None, None]

        ypcookie = result.get('ypcookie') if result.get('ypcookie') else result.get(' ypcookie')  # 为啥会有个空格？？？？
        if not ypcookie:
            print('not ypcookie')
            return [None, None]

        ss = ypcookie[0]

        result = parse.parse_qs(ss)

        uid = result.get('uid')
        if not uid:
            print('not uid')
            print(result)
            return [None, None]

        sid = result.get('sid')
        if not sid:
            sid = ['1']

        if uid[0].isdigit():
            uid = int(uid[0])

        return [uid, sid[0]]
    except Exception as e:
        print(e)
        return [None, None]


def verify_name(str):
    pass


def write_data_url_file(s):
    req = requests.post(upload_cdn_url, data=dict(sk='38271d7c768d0ff754c39c2be4df4bad', image=s))
    print(req.text, 'write_data_url_file')
    try:
        data = req.json()
        if data['code'] != 1:
            return None
        return data['data']['imgUrl']
    except Exception as e:
        print(e)
        return None


def return_random_name():
    random_i = return_random_time()
    root_path = '{}/pic/{}.png'.format(current_app.root_path, random_i)
    return root_path


def return_random_time():
    return '{}{}'.format(int(arrow.now().float_timestamp), ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 20)))
