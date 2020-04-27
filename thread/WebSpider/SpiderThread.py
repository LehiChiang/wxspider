import traceback

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import os
import time
import pandas as pd

from service.WebSpider.spider import PassageSpider

class SpiderThread(QtCore.QThread):

    signal = pyqtSignal(object)

    msg = {}

    def __init__(self, biz, uin, key, option):
        super(SpiderThread, self).__init__()
        self.biz = biz
        self.uin = uin
        self.key = key
        self.option = option

    def __del__(self):
        self.wait()

    def run(self):
        try:
            option = self.option
            filename = 'datastmp.csv'

            titledata = pd.DataFrame(columns=['id', 'title', 'url', 'datetime', 'copyright'])
            titledata.to_csv(os.path.join('../data', filename), encoding='utf_8_sig', index=False)

            start = time.clock()
            if option == 'all':
                spider = PassageSpider(offset=0,
                                       count=10,
                                       biz=self.biz,
                                       uin=self.uin,
                                       key=self.key)
                spider.request_url(getall=True, filename=filename)
                spider.save_xls(filename=filename)
            else:
                pages = int(option)
                spider = PassageSpider(offset=0,
                                       count=10,
                                       biz=self.biz,
                                       uin=self.uin,
                                       key=self.key)
                for i in range(pages):
                    spider.request_url(getall=False, filename=filename)
                    spider.offset += spider.count
                    spider.save_xls(filename=filename)
                    time.sleep(spider.sleeptime)

            end = time.clock()

        except Exception:
            e = str(traceback.format_exc())
            self.msg['error'] = e
            self.msg['state'] = 'fail'

        self.msg['time'] = end-start
        self.msg['state'] = 'success'
        self.signal.emit(self.msg)
