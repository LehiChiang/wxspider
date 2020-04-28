from json import load


def get_request_params(biz, uin, offset, count, key, appmsg_token='', pass_ticket=''):
    # key,__biz和appmsg_token的属性是不一样的
    return {
            'action': 'getmsg',
            '__biz': biz,
            'offset': offset,  # offset是改变的，它的值是上次的offset的值加上上次的count值
            'count': count,
            'is_ok': '1',
            'scene': '124',
            'uin': uin,
            'key': key,
            'pass_ticket': pass_ticket,
            'appmsg_token': appmsg_token,
            'f': 'json'
        }


def get_request_url():
        return load(open('../config/url.json', 'r', encoding='utf-8'))['url']


def get_request_header():
        return load(open('../config/header.json', 'r', encoding='utf-8'))

def get_proxies():
        return load(open('../config/proxies.json', 'r', encoding='utf-8'))
