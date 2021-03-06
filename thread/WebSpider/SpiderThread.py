from traceback import format_exc
from PyQt5.QtCore import pyqtSignal, QThread
from os.path import join
from time import clock, sleep
from pandas import DataFrame

from service.WebSpider.spider import PassageSpider

class SpiderThread(QThread):

    signal = pyqtSignal(str)


    def __init__(self, biz, uin, key, option, filename, sleeptime):
        super(SpiderThread, self).__init__()
        self.biz = biz
        self.uin = uin
        self.key = key
        self.option = option
        self.filename = filename
        self.sleeptime = sleeptime

    def __del__(self):
        self.wait()

    def run(self):
        try:
            option = self.option
            filename = self.filename

            titledata = DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
            titledata.to_csv(join('../data', filename), encoding='utf_8_sig', index=False)

            start = clock()
            if option == 'all':
                spider = PassageSpider(offset=0,
                                       count=10,
                                       biz=self.biz,
                                       uin=self.uin,
                                       key=self.key,
                                       sleeptime=self.sleeptime)
                spider.request_url(getall=True, filename=filename)
                spider.save_xls(filename=filename)
            else:
                pages = int(option)
                spider = PassageSpider(offset=0,
                                       count=10,
                                       biz=self.biz,
                                       uin=self.uin,
                                       key=self.key,
                                       sleeptime=self.sleeptime)
                for i in range(pages):
                    spider.request_url(getall=False, filename=filename)
                    spider.offset += spider.count
                    spider.save_xls(filename=filename)
                    sleep(spider.sleeptime)
            end = clock()
            print(end-start)
        except Exception:
            e = str(format_exc())
            self.signal.emit(e)
        self.signal.emit('activate')
