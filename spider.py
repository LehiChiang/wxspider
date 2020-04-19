import requests
import time
import json
import pandas as pd

class PassageSpider:

    def __init__(self,key, biz,
                 offset='0',
                 count='10',
                 appmsg_token=''
                 ):
        self.pass_url = "https://mp.weixin.qq.com/mp/profile_ext"
        self.datatmsp = pd.DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/'
                      'signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '80.0.3987.163 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        # key,__biz和appmsg_token的属性是不一样的
        self.params = {
            'action': 'getmsg',
            '__biz': biz,
            'f': 'json',
            'offset': offset,  # offset是改变的，它的值是上次的offset的值加上上次的count值
            'count': count,
            'is_ok': '1',
            'scene': '124',
            'uin': 'MTY4MDI2MzkxNA==',
            'key': key,
            'pass_ticket': 'wyeBEKFvPyKdz2dFi+yXTiGxxA0aIrFdRhi9vefIjZRfpRFArkBheJEh7X2oXe7M',
            'appmsg_token': appmsg_token,
            'x5': '0',
            'f': 'json'
        }

    def request_url(self):
        requests.packages.urllib3.disable_warnings()
        result = requests.get(url=self.pass_url,
                              headers=self.headers,
                              params=self.params,
                              verify=False)
        html = json.loads(result.text)
        return html

    def parse_json(self,html):
        json_list = json.loads(html['general_msg_list'])['list']
        for item in json_list:
            id = item['comm_msg_info']['id']
            datatime = item['comm_msg_info']['datetime']
            time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(datatime)))
            title_ = item['app_msg_ext_info']['title']
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
                                              'copyright':[copyright_]
                                              })
                    self.datatmsp = self.datatmsp.append(df_insert, ignore_index=True)

    def save_xls(self):
        self.datatmsp.to_csv('data/datastmsp.csv',
                             mode='a',
                             encoding='utf_8_sig',
                             index=False,
                             header=False)

    def url2pdf(self):
        pass

if __name__ == "__main__":
    offset = 0
    #每页10个
    count = 10
    #爬取20页
    pages = 2
    #时间间隔，建议长一点
    interval = 5
    #每个公众号都会变的地方
    biz = 'MjM5NDU1MDU2Nw=='
    key = '4bc1bbadb5ce2652bdff9f69406a6806f545bc01e287d131ce9a1e5d0bbcf390234040870ee4c11467faece7e3c53765b29ef7c8b44845d20cb84cb7df8a478d532179d5d6082b9bac780f6a2bc9e4e9'

    titledata = pd.DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
    titledata.to_csv('data/datastmsp.csv',
                     encoding='utf_8_sig',
                     index=False)

    for i in range(pages):
        spider = PassageSpider(offset=offset,
                               count=count,
                               biz=biz,
                               key=key)
        html = spider.request_url()
        spider.parse_json(html)
        offset += count
        time.sleep(interval)
        spider.save_xls()
