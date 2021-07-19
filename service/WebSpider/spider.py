from json import loads
from time import strftime, localtime, sleep
from pandas import DataFrame
from requests import packages, get

from config.RequestParams import get_request_url, get_request_header, get_request_params


class PassageSpider:

    def __init__(self,
                 appmsg_token,
                 biz,
                 cookie,
                 offset='0',
                 count='10',
                 sleeptime=10
                 ):
        self.offset = offset
        self.count = count
        self.biz = biz
        self.appmsg_token = appmsg_token
        self.sleeptime = sleeptime
        self.pass_url = "https://mp.weixin.qq.com/mp/profile_ext"
        self.datatmsp = DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
        self.headers = {"Host": "mp.weixin.qq.com", "Connection": "keep-alive",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
                        "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", 'Cookie': cookie}
        # ip = get_proxies.get_proxies()
        # print('Proxy IP: ', ip)
        # self.proxies = {ip.split(':')[0]:ip}

    def request_url(self, getall, filename='passagedata.csv'):
        '''
        getall参数表达的含义是是否获取微信公众号的所有文章，为True时表示获取全部
        :param getall:
        :return:
        '''
        packages.urllib3.disable_warnings()
        result = get(url=self.pass_url,
                     # proxies=self.proxies,
                     headers=self.headers,
                     params=get_request_params(self.biz, self.offset, self.count, self.appmsg_token),
                     verify=False)
        print('URL: ', result.url)
        html = loads(result.text)
        self.parse_json(html, getall, filename)

    def parse_json(self, html, getall, filename):
        '''
        解析html页面
        :param html:
        :return:
        '''
        can_msg_continue = html['can_msg_continue']
        next_offset = html['next_offset']
        json_list = loads(html['general_msg_list'])['list']

        for item in json_list:
            id = item['comm_msg_info']['id']
            datatime = item['comm_msg_info']['datetime']
            time_ = strftime("%Y-%m-%d %H:%M:%S", localtime(int(datatime)))
            try:
                title_ = item['app_msg_ext_info']['title']
            except:
                continue
            content_url_ = item['app_msg_ext_info']['content_url']
            try:
                copyright_ = item['app_msg_ext_info']['copyright_stat']
            except:
                copyright_ = ''
            eleinums = item['app_msg_ext_info']['multi_app_msg_item_list']

            if title_ != "":
                # print(id, title_, content_url_, time_)
                df_insert = DataFrame({'id': [id],
                                       'title': [title_],
                                       'url': [content_url_],
                                       'datetime': [time_],
                                       'copyright': [copyright_]
                                       })
                self.datatmsp = self.datatmsp.append(df_insert, ignore_index=True)

            if eleinums != []:
                for ele in eleinums:
                    title_ = ele['title']
                    content_url_ = ele['content_url']
                    try:
                        copyright_ = ele['copyright_stat']
                    except:
                        copyright_ = ''
                    # print(id, title_, content_url_, time_)
                    df_insert = DataFrame({'id': [id],
                                           'title': [title_],
                                           'url': [content_url_],
                                           'datetime': [time_],
                                           'copyright': [copyright_]
                                           })
                    self.datatmsp = self.datatmsp.append(df_insert, ignore_index=True)

        self.save_xls(filename=filename)
        self.datatmsp.drop(self.datatmsp.index, inplace=True)

        if can_msg_continue == 1 and getall:
            sleep(self.sleeptime)
            self.offset = next_offset
            self.request_url(getall=True, filename=filename)

    def save_xls(self, filename):
        """
        将数据保存到csv格式的文件中，并使用追加添加的模式
        :return:
        """
        self.datatmsp.drop_duplicates()
        self.datatmsp.to_csv(filename,
                             encoding='utf_8_sig',
                             mode='a',
                             index=False,
                             header=False)


if __name__ == "__main__":
    spider = PassageSpider(appmsg_token='1085_IMGZhOp7E1a6QRiq5foSkt27KJ__Z_3jAQkzgA~~', biz='MzA3MzI4MjgzMw==',
                           cookie='')
    spider.request_url(False)
