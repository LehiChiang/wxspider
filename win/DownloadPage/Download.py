import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QProgressBar, QDesktopWidget, \
    QTextEdit, QMessageBox, QFileDialog, QHBoxLayout, QGridLayout
from time import strftime
from PyQt5.QtCore import Qt
from time import localtime
from thread.DownloadPage.DownloadThread import DownloadThread


class DownLoad(QWidget):
    def __init__(self):
        super().__init__()
        # 创建线程
        self.workthread = DownloadThread()
        self.workthread.trigger.connect(self.progressbar)
        self.workthread.trigger2.connect(self.downresult)
        self.workthread.trigger3.connect(self.filesize)
        self.initUI()

    def initUI(self):
        self.firstRow = QHBoxLayout()
        self.secondRow = QHBoxLayout()
        self.thirdRow = QHBoxLayout()
        self.forthRow = QHBoxLayout()

        self.urllabel = QLabel("下载链接:")
        self.urllabel.setObjectName('content')
        self.urledit = QLineEdit()
        self.downloadbtn = QPushButton("下载")
        self.downloadbtn.clicked.connect(self.down)
        self.firstRow.addWidget(self.urllabel)
        self.firstRow.addWidget(self.urledit)
        self.firstRow.addWidget(self.downloadbtn)

        self.locurl = QLabel("下载位置:")
        self.locurl.setObjectName('content')
        self.locedit = QLineEdit()
        self.locedit.setFocusPolicy(Qt.NoFocus)
        self.dirbtn = QPushButton("选择目录")
        self.dirbtn.clicked.connect(self.showDir)
        self.secondRow.addWidget(self.locurl)
        self.secondRow.addWidget(self.locedit)
        self.secondRow.addWidget(self.dirbtn)

        self.pbar = QProgressBar()
        self.progresslabel = QLabel()
        self.thirdRow.addWidget(self.pbar)
        self.thirdRow.addWidget(self.progresslabel)

        self.history = QTextEdit()

        self.resrtbtn = QPushButton('重置')
        self.resrtbtn.clicked.connect(self.clear)
        self.forthRow.addStretch(1)
        self.forthRow.addWidget(self.resrtbtn)

        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.firstRow, 0,0,1,10)
        self.main_layout.addLayout(self.secondRow, 1,0,1,10)
        self.main_layout.addLayout(self.thirdRow, 2,1,1,8)
        self.main_layout.addWidget(self.history, 3,0,4,10)
        self.main_layout.addLayout(self.forthRow, 7,0,1,10)
        self.main_layout.setSpacing(10)

        self.setLayout(self.main_layout)

    def showDir(self):
        download_path = QFileDialog.getExistingDirectory(self,"浏览",r"C:/Users/Administrator/Desktop")
        self.locedit.setText(download_path)

    def down(self):
        if self.urledit.text() == '':
            QMessageBox.information(self,"错误","URL不能为空")
            return
        self.downloadbtn.setEnabled(False)
        self.workthread.url = self.urledit.text()
        self.workthread.basedir = self.locedit.text()
        self.workthread.start()

    def downresult(self,info):
        self.history.append(info)

    def progressbar(self, num):
        self.pbar.setValue(num)
        if num == 100:
            info = strftime("%y/%M/%d %H:%M:%S", localtime()) + ":"
            self.history.append(info)
            self.downloadbtn.setEnabled(True)

    def filesize(self, size):
        self.progresslabel.setText(size)

    def clear(self):
        try:
            self.urledit.setText('')
            self.locedit.setText('')
            self.pbar.setValue(0)
            self.progresslabel.setText('')
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    down = DownLoad()
    down.show()
    sys.exit(app.exec_())
