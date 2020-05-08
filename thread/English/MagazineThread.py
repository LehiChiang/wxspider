from traceback import format_exc

from PyQt5.QtCore import pyqtSignal, QThread

class FetchFirstMagazineListThread(QThread):

    magazinelist = pyqtSignal(int, str, list, int, int)

    def __init__(self, magazine, tabindex, tabname):
        super(FetchFirstMagazineListThread, self).__init__()
        self.magazine = magazine
        self.tabindex = tabindex
        self.tabname = tabname

    def run(self):
        try:
            jsonStr = self.magazine.get_first_page()
            current_page = self.magazine.current_page
            total_page = self.magazine.total_page
            self.magazinelist.emit(self.tabindex,
                                   self.tabname,
                                   jsonStr,
                                   current_page,
                                   total_page)
        except Exception:
            e = str(format_exc())
            print(e)

class FetchNextMagazineListThread(QThread):

    magazinelist = pyqtSignal(int, str, list, int, int)

    def __init__(self, magazine, tabindex, tabname):
        super(FetchNextMagazineListThread, self).__init__()
        self.magazine = magazine
        self.tabindex = tabindex
        self.tabname = tabname

    def run(self):
        try:
            jsonStr = self.magazine.get_next_page()
            current_page = self.magazine.current_page
            total_page = self.magazine.total_page
            self.magazinelist.emit(self.tabindex,
                                   self.tabname,
                                   jsonStr,
                                   current_page,
                                   total_page)
        except Exception:
            e = str(format_exc())
            print(e)

class FetchPreMagazineListThread(QThread):

    magazinelist = pyqtSignal(int, str, list, int, int)

    def __init__(self, magazine, tabindex, tabname):
        super(FetchPreMagazineListThread, self).__init__()
        self.magazine = magazine
        self.tabindex = tabindex
        self.tabname = tabname

    def run(self):
        try:
            jsonStr = self.magazine.get_pre_page()
            current_page = self.magazine.current_page
            total_page = self.magazine.total_page
            self.magazinelist.emit(self.tabindex,
                                   self.tabname,
                                   jsonStr,
                                   current_page,
                                   total_page)
        except Exception:
            e = str(format_exc())
            print(e)

class FetchLastMagazineListThread(QThread):

    magazinelist = pyqtSignal(int, str, list, int, int)

    def __init__(self, magazine, tabindex, tabname):
        super(FetchLastMagazineListThread, self).__init__()
        self.magazine = magazine
        self.tabindex = tabindex
        self.tabname = tabname

    def run(self):
        try:
            jsonStr = self.magazine.get_last_page()
            current_page = self.magazine.current_page
            total_page = self.magazine.total_page
            self.magazinelist.emit(self.tabindex,
                                   self.tabname,
                                   jsonStr,
                                   current_page,
                                   total_page)
        except Exception:
            e = str(format_exc())
            print(e)

class FetchCustomizedMagazineListThread(QThread):

    magazinelist = pyqtSignal(int, str, list, int, int)

    def __init__(self, magazine, tabindex, tabname, index):
        super(FetchCustomizedMagazineListThread, self).__init__()
        self.magazine = magazine
        self.tabindex = tabindex
        self.tabname = tabname
        self.index = index

    def run(self):
        try:
            jsonStr = self.magazine.step_to_page(index=self.index)
            current_page = self.magazine.current_page
            total_page = self.magazine.total_page
            self.magazinelist.emit(self.tabindex,
                                   self.tabname,
                                   jsonStr,
                                   current_page,
                                   total_page)
        except Exception:
            e = str(format_exc())
            print(e)
