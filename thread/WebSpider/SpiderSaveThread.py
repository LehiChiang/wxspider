import json
import traceback

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

class SpiderSaveThread(QtCore.QThread):

    signal = pyqtSignal(str)

    msg = {}

    def __init__(self, setting):
        super(SpiderSaveThread, self).__init__()
        self.setting = setting

    def __del__(self):
        self.wait()

    def run(self):
        try:
            with open('../config/wxspider_setting.cm', 'w', encoding='utf-8') as fp:
                fp.write(json.dumps(self.setting, indent=4, ensure_ascii=False))
        except Exception as e:
            e = str(traceback.format_exc())
            self.signal.emit(e)
