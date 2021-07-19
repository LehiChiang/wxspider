from PyQt5.QtCore import QThread, pyqtSignal
import time, requests
from os.path import join, basename


class DownloadThread(QThread):
    trigger = pyqtSignal(int)
    trigger2 = pyqtSignal(str)
    trigger3 = pyqtSignal(str)
    trigger4 = pyqtSignal(str)

    url = ""
    basedir = "./"

    def __init__(self):
        super(DownloadThread, self).__init__()

    def run(self):
        url = self.url
        self.trigger4.emit(url.split('/')[-1])
        path = join(self.basedir, basename(url))
        start = time.time()
        size = 0
        response = requests.get(url, stream=True)  # stream 必须带上
        chunk_size = 1024  # 每次下载大小
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            self.trigger3.emit("[文件大小]:%.2f MB" % (content_size / chunk_size / 1024))
            with open(path, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)  # 已下载大小
                    num = int(size / content_size * 100)
                    self.trigger.emit(num)
            end = time.time()  # 结束时间
            self.trigger2.emit("下载完成！用时%.2f秒|%s" % (end - start, self.basedir))
