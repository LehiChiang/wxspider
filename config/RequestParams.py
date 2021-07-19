from json import load


def get_request_params(biz, offset, count, appmsg_token):
    # key,__biz和appmsg_token的属性是不一样的
    # https://mp.weixin.qq.com/mp/profile_ext?
    # action=getmsg
    # &__biz=MzA3MzI4MjgzMw==
    # &f=json
    # &offset=0
    # &count=10
    # &appmsg_token=1085_IMGZhOp7E1a6QRiq5foSkt27KJ__Z_3jAQkzgA~~
    return {
            'action': 'getmsg',
            '__biz': biz,
            'offset': offset,  # offset是改变的，它的值是上次的offset的值加上上次的count值
            'count': count,
            # 'uin': '777',
            # 'key': '777',
            'is_ok': '1',
            'scene': '124',
            'appmsg_token': appmsg_token,
            'f': 'json'
    }


def get_request_url():
        return load(open('config/url.json', 'r', encoding='utf-8'))['url']


def get_request_header():
        return load(open('config/header.json', 'r', encoding='utf-8'))

def get_proxies():
        return load(open('config/proxies.json', 'r', encoding='utf-8'))
