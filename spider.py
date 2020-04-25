import requests
import time
import os
import json
import pandas as pd
import config.RequestParams as reparams
import get_proxies
from time import clock

class PassageSpider:

    def __init__(self,
                 key,
                 biz,
                 uin,
                 offset='0',
                 count='10'
                 ):
        self.offset = offset
        self.count = count
        self.biz = biz
        self.uin = uin
        self.key = key
        self.sleeptime = 10 #休眠10秒
        self.pass_url = reparams.get_request_url()
        self.datatmsp = pd.DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
        self.headers = reparams.get_request_header()
        # ip = get_proxies.get_proxies()
        # print('Proxy IP: ', ip)
        # self.proxies = {ip.split(':')[0]:ip}

    def request_url(self, getall, filename='passagedata.csv'):
        '''
        getall参数表达的含义是是否获取微信公众号的所有文章，为True时表示获取全部
        :param getall:
        :return:
        '''
        requests.packages.urllib3.disable_warnings()
        result = requests.get(url=self.pass_url,
                              # proxies=self.proxies,
                              headers=self.headers,
                              params=reparams.get_request_params(self.biz, self.uin, self.offset, self.count, self.key),
                              verify=False,)
        print('URL: ', result.url)
        print('status_code: ', result.status_code)
        html = json.loads(result.text)
        self.parse_json(html, getall, filename)

    def parse_json(self, html, getall, filename):
        '''
        解析html页面
        :param html:
        :return:
        '''
        can_msg_continue = html['can_msg_continue']
        next_offset = html['next_offset']
        json_list = json.loads(html['general_msg_list'])['list']

        for item in json_list:
            id = item['comm_msg_info']['id']
            datatime = item['comm_msg_info']['datetime']
            time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(datatime)))
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
                print(id, title_, content_url_, time_)
                df_insert = pd.DataFrame({'id':[id],
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
                    print(id, title_, content_url_, time_)
                    df_insert = pd.DataFrame({'id': [id],
                                              'title': [title_],
                                              'url': [content_url_],
                                              'datetime': [time_],
                                              'copyright': [copyright_]
                                              })
                    self.datatmsp = self.datatmsp.append(df_insert, ignore_index=True)

        self.save_xls(filename=filename)
        self.datatmsp.drop(self.datatmsp.index, inplace=True)

        if can_msg_continue == 1 and getall:
            time.sleep(self.sleeptime)
            self.offset = next_offset
            self.request_url(getall=True, filename=filename)

    def save_xls(self, filename):
        '''
        将数据保存到csv格式的文件中，并使用追加添加的模式
        :return:
        '''
        self.datatmsp.drop_duplicates()
        self.datatmsp.to_csv(os.path.join('../data', filename),
                             encoding='utf_8_sig',
                             mode='a',
                             index=False,
                             header=False)

# if __name__ == '__main__':
#
#     biz = 'MjM5NDU1MDU2Nw=='
#     uin = 'MTY4MDI2MzkxNA=='
#     key = 'ad1327b1c72241bf4d1d6d68fe11254cbcc8ae146d1638e3f27f641e19eec96a0cf3247aac29169515df8026c31538d6ec3279dd7f54b3756e7298d79241f25a9707e4849e5c04d80a4aadf186bd2c97'
#
#     option = input('爬取全部输入‘all’，自定义页数输入页数，（例如：‘2’）：')
#     filename = 'datastmp.csv'
#
#     titledata = pd.DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
#     titledata.to_csv(os.path.join('../data', filename), encoding='utf_8_sig', index=False)
#
#     start = time.clock()
#     if option == 'all':
#         spider = PassageSpider(offset=0,
#                                count=10,
#                                biz=biz,
#                                uin=uin,
#                                key=key)
#         spider.request_url(getall=True, filename=filename)
#         spider.save_xls(filename=filename)
#     else:
#         pages = int(option)
#         spider = PassageSpider(offset=0,
#                                count=10,
#                                biz=biz,
#                                uin=uin,
#                                key=key)
#         for i in range(pages):
#             spider.request_url(getall=False, filename=filename)
#             spider.offset += spider.count
#             spider.save_xls(filename=filename)
#             time.sleep(spider.sleeptime)
#
#     end = time.clock()
#     print('Running time: %s Seconds'%(end-start))