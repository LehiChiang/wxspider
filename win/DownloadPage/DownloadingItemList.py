from qtawesome import icon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem, QVBoxLayout, QWidget, QLabel, QListWidget, QHBoxLayout, QProgressBar


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
        self.title.setText('')
        #self.title.setObjectName('menutitle')

        self.bottomLine = QHBoxLayout()
        self.sizelabel = QLabel()
        self.sizelabel.setText('[文件大小]：0MB/0MB')
        self.pbar = QProgressBar()
        self.bottomLine.addWidget(self.sizelabel)
        self.bottomLine.addWidget(self.pbar)

        self.layout_main.addWidget(self.title)
        self.layout_main.addLayout(self.bottomLine)
        wight.setLayout(self.layout_main)
        return wight
