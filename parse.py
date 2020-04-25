
def get_url_param(url):
    param_dict = {}
    str = url
    list = str.split('&')
    list.pop(0)
    for i in list:
        param = i.split('=', 1)
        param_dict[param[0]] = param[1]
    return param_dict

