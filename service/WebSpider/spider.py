from json import loads
from time import strftime, localtime, sleep
from os.path import join
from pandas import DataFrame
from requests import packages, get

from config.RequestParams import get_request_url, get_request_header, get_request_params


class PassageSpider:

    def __init__(self,
                 key,
                 biz,
                 uin,
                 offset='0',
                 count='10',
                 sleeptime=10
                 ):
        self.offset = offset
        self.count = count
        self.biz = biz
        self.uin = uin
        self.key = key
        self.sleeptime = sleeptime
        self.pass_url = get_request_url()
        self.datatmsp = DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
        self.headers = get_request_header()
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
                              params=get_request_params(self.biz, self.uin, self.offset, self.count, self.key),
                              verify=False,)
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
                #print(id, title_, content_url_, time_)
                df_insert = DataFrame({'id':[id],
                                          'title':[title_],
                                          'url':[content_url_],
                                          'datetime':[time_],
                                          'copyright':[copyright_]
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
                    #print(id, title_, content_url_, time_)
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
        '''
        将数据保存到csv格式的文件中，并使用追加添加的模式
        :return:
        '''
        self.datatmsp.drop_duplicates()
        self.datatmsp.to_csv(join('../data', filename),
                             encoding='utf_8_sig',
                             mode='a',
                             index=False,
                             header=False)
