from os import system
from time import strftime, localtime

from qtawesome import icon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QListWidget, QHBoxLayout, QProgressBar, QToolButton, QAction


class DownloadingListWidget(QListWidget):

    def __init__(self):
        super(DownloadingListWidget, self).__init__()

        self.setIconSize(QSize(24, 24))
        #self.setFont(QFont('黑体', 11))
        #self.setFixedWidth(240)
        self.setViewMode(QListWidget.ListMode)
        self.setObjectName('download')


    def get_Item_Widget(self):
        wight = QWidget()
        self.layout_main = QVBoxLayout()
        self.title = QLabel()
        #self.title.setObjectName('menutitle')

        self.bottomLine = QHBoxLayout()
        self.sizelabel = QLabel()
        self.pbar = QProgressBar()
        self.bottomLine.addWidget(self.sizelabel)
        self.bottomLine.addWidget(self.pbar)

        self.layout_main.addWidget(self.title)
        self.layout_main.addLayout(self.bottomLine)
        wight.setLayout(self.layout_main)
        return wight


class DownloadedListWidget(QListWidget):

    def __init__(self):
        super(DownloadedListWidget, self).__init__()
        self.setIconSize(QSize(24, 24))
        self.setViewMode(QListWidget.ListMode)
        self.currentRowChanged.connect(self.savelog)
        self.setObjectName('download')

    def get_Item_Widget(self, title, info, url):
        wight = QWidget()
        self.opendirAct = QAction(QIcon('res/opendir.png'), '打开下载路径')
        self.opendirAct.triggered.connect(self.on_click)
        self.fileurl = url
        self.outer = QHBoxLayout()
        self.layout_main = QVBoxLayout()
        self.title = QLabel()
        self.title.setText(title)
        self.bottomLine = QHBoxLayout()
        self.sizelabel = QLabel()
        self.sizelabel.setText(info)
        self.timelabel = QLabel()
        self.timelabel.setText('完成时间：{}'.format(strftime("%Y-%m-%d %H:%M:%S",localtime())))
        self.openbtn = QToolButton()
        self.openbtn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.openbtn.setToolTip('选择')
        self.openbtn.setPopupMode(QToolButton.MenuButtonPopup)
        self.openbtn.setIcon(QIcon('res/setting.png'))
        self.openbtn.setFixedSize(QSize(38, 38))
        self.openbtn.setIconSize(QSize(38, 38))
        self.openbtn.addAction(self.opendirAct)
        self.bottomLine.addWidget(self.sizelabel)
        self.bottomLine.addWidget(self.timelabel)
        self.layout_main.addWidget(self.title)
        self.layout_main.addLayout(self.bottomLine)
        self.outer.addLayout(self.layout_main)
        self.outer.addWidget(self.openbtn)
        wight.setLayout(self.outer)
        return wight

    def opendir(self):
        system(("start explorer %s" % self.fileurl).replace('/','\\'))

    def on_click(self):
        #QDesktopServices.openUrl(QUrl('https://www.alipay.com/'))
        if self.sender() == self.opendirAct:
            self.opendir()

    def savelog(self):
        print('添加了')
