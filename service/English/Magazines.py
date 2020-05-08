import requests
from lxml import etree

class Magazine:
    def __init__(self, url):
        self.url = url
        self.header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.total_page = self.get_pages()
        self.current_page = 1

    def get_magazine(self, page):
        '''
        获取经济学人和纽约时报
        :param page:
        :return:
        '''
        result = requests.get('%s/page/%d'%(self.url, page), headers=self.header)
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
            passage_map['img'] = img_list[i]
            passage_map['url'] = url_list[i]
            passage_map['title'] = title_list[i]
            passage_map['time'] = time_list[i]
            passage_map['author'] = author_list[i]
            passage_map['description'] = description_list[i]
            passage_map_list.insert(i, passage_map)

        #passage_json = json.dumps(passage_map_list, indent=2, ensure_ascii=False)
        return passage_map_list

    def get_pages(self):
        '''
        获取当前栏目所有文章的页数
        :return:
        '''
        result = requests.get(url=self.url, headers=self.header)
        text = etree.HTML(result.text)
        total_page = text.xpath("//nav[@class='navigation pagination']/div/a[contains(@class,'page-numbers')][2]/text()")
        return int(total_page[0])

    def get_first_page(self):
        '''
        获取列表的第一页
        :return:
        '''
        self.current_page = 1
        return self.get_magazine(self.current_page)

    def get_next_page(self):
        '''
        获取列表的下一页
        :return:
        '''
        if self.current_page != self.total_page:
            self.current_page = self.current_page + 1
            return self.get_magazine(self.current_page)

    def get_pre_page(self):
        '''
        获取列表的前一页
        :return:
        '''
        if self.current_page != 1:
            self.current_page = self.current_page - 1
            return self.get_magazine(self.current_page)

    def get_last_page(self):
        '''
        获取列表的最后一页
        :return:
        '''
        self.current_page = self.total_page
        return self.get_magazine(self.current_page)

    def step_to_page(self, index):
        if index >= 1 and index <= self.total_page:
            self.current_page = index
            return self.get_magazine(self.current_page)


if __name__ == '__main__':
    maga = Magazine('https://www.tianfateng.cn/tag/nytimes')
    r1 = maga.step_to_page(5)
    r2 = maga.get_next_page()
    print(r1)
    print(r2)
