import requests
import time
import os
import json
import pandas as pd
import config.RequestParams as params

class PassageSpider:

    def __init__(self,
                 key,
                 biz,
                 offset='0',
                 count='10'
                 ):
        self.offset = offset
        self.count = count
        self.sleeptime = 3 #休眠3秒
        self.pass_url = params.get_request_url()
        self.datatmsp = pd.DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
        self.headers = params.get_request_header()
        self.params = params.get_request_params(biz, offset, count, key)

    def request_url(self, getall):
        '''
        getall参数表达的含义是是否获取微信公众号的所有文章，为True时表示获取全部
        :param getall:
        :return:
        '''
        requests.packages.urllib3.disable_warnings()
        result = requests.get(url=self.pass_url,
                              headers=self.headers,
                              params=self.params,
                              verify=False)
        html = json.loads(result.text)
        self.parse_json(html, getall)

    def parse_json(self, html, getall):
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
                # print(id, title_, content_url_, time_)
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
                    # print(id, title_, content_url_, time_)
                    df_insert = pd.DataFrame({'id': [id],
                                              'title': [title_],
                                              'url': [content_url_],
                                              'datetime': [time_],
                                              'copyright': [copyright_]
                                              })
                    self.datatmsp = self.datatmsp.append(df_insert, ignore_index=True)
        print(self.datatmsp)
        if can_msg_continue == 1 and getall:
            time.sleep(self.sleeptime)
            self.params = params.get_request_params(biz, next_offset, self.count, key)
            self.request_url(getall=True)

    def save_xls(self, getall, filename='passagedata.csv'):
        '''
        将数据保存到csv格式的文件中，并使用追加添加的模式
        :return:
        '''
        if getall:
            titledata = pd.DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
            titledata.to_csv(os.path.join('data', filename),
                                encoding='utf_8_sig',
                                index=False)
        self.datatmsp.to_csv(os.path.join('data', filename),
                             mode='a',
                             encoding='utf_8_sig',
                             index=False,
                             header=False)

    def url2pdf(self):
        '''
        将获取到的公众号url保存为pdf单独的文件
        :return:
        '''
        pass


if __name__ == "__main__":
    option = input('爬取全部输入‘all’，自定义页数输入页数，（例如：‘2’）：')
    filename = 'datastmp.csv'
    # 每个公众号都会变的地方
    biz = 'MzI3ODYyNjEwNQ=='
    key = '0bede9ac882f25ac7aa5df8e929e74045e9beb69489883fc944079865128faa0ebf4830eb6d8a2eb502146422d54ae8b99f352c4f6533c83dce443f681ab194a8bec9569a513bc1b6e3c76dbd2bd8cf5'

    if option == 'all':
        spider = PassageSpider(offset=0,
                               count=10,
                               biz=biz,
                               key=key)
        spider.request_url(getall=True)
        spider.save_xls(getall=True, filename=filename)
    else:
        pages = int(option)
        offset = 0
        count =10
        titledata = pd.DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
        titledata.to_csv(os.path.join('data', filename),
                         encoding='utf_8_sig',
                         index=False)
        for i in range(pages):
            spider = PassageSpider(offset=offset,
                                   count=count,
                                   biz=biz,
                                   key=key)
            spider.request_url(getall=False)
            offset += count
            time.sleep(spider.sleeptime)
            spider.save_xls(getall=False, filename=filename)
