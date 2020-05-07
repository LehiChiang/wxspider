import json

import requests
from lxml import etree

def get_magazine(url, page):
    '''
    获取经济学人和纽约时报
    :param url:
    :param page:
    :return:
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    result = requests.get('%s/%s'%(url, page), headers=headers)
    text = etree.HTML(result.text)
    # xpath 获取想要的信息
    img_list = [img.strip() for img in text.xpath('//article/figure/a/img/@src')]
    url_list = [url.strip() for url in text.xpath('//article/figure/a/@href')]
    title_list = [title.strip() for title in text.xpath('//article/div/header/h3/a/text()')]
    time_list = [time.strip() for time in text.xpath('//article/div/header/div/span[1]/text()')]
    author_list = [author.strip() for author in text.xpath('//article/div/header/div/span[2]/a/text()')]
    description_list = [description.strip() for description in text.xpath('//article/div/div/div/p/text()')]

    passage_map_list = []

    for i in range(len(img_list)):
        passage_map = {}
        passage_map['img']=img_list[i]
        passage_map['url']=url_list[i]
        passage_map['title']=title_list[i]
        passage_map['time']=time_list[i]
        passage_map['author']=author_list[i]
        passage_map['description']=description_list[i]
        passage_map_list.insert(i, passage_map)

    passage_json = json.dumps(passage_map_list, indent=2, ensure_ascii=False)  # json转为string
    return passage_json

if __name__ == '__main__':
    r = get_magazine('https://www.tianfateng.cn/tag/nytimes/page', '3')
    print(r)