from random import choice

from bs4 import BeautifulSoup
from requests import get


def get_ip_list(url, headers):
    web_data = get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        httptype = str.lower(tds[5].text)
        ip_list.append(httptype + '://' + tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip(ip_list):
    proxy_ip = choice(ip_list)
    return proxy_ip


def get_proxies():
    url = 'http://www.xicidaili.com/wt/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    ip_list = get_ip_list(url, headers=headers)
    proxies = get_random_ip(ip_list)
    return proxies


if __name__ == "__main__":
    ss = {get_proxies().split(':')[0]: get_proxies()}
    print(ss)
