from PyQt5.QtCore import pyqtSignal, QThread

from service.English.Magazines import get_magazine


class FetchMagazineListThread(QThread):

    magazinelist = pyqtSignal(str, str, str)

    def __init__(self, url, page, tabindex, tabname):
        super(FetchMagazineListThread, self).__init__()
        self.url = url
        self.page = page
        self.tabindex = tabindex
        self.tabname = tabname


    def run(self):
        jsonStr = get_magazine(url=self.url, page=self.page)
        self.magazinelist.emit(self.tabindex, self.tabname, jsonStr)
