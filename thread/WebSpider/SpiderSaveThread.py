from json import dumps
from traceback import format_exc

from PyQt5.QtCore import pyqtSignal, QThread


class SpiderSaveThread(QThread):

    signal = pyqtSignal(str)

    def __init__(self, setting):
        super(SpiderSaveThread, self).__init__()
        self.setting = setting

    def __del__(self):
        self.wait()

    def run(self):
        try:
            with open('../config/wxspider_setting.cm', 'w', encoding='utf-8') as fp:
                fp.write(dumps(self.setting, indent=4, ensure_ascii=False))
        except Exception as e:
            e = str(format_exc())
            self.signal.emit(e)
        self.signal.emit('activate')
