from time import strftime, localtime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect, QLineEdit, \
    QPushButton, QListWidgetItem, QMessageBox
from qtawesome import icon

from thread.DownloadPage.DownloadThread import DownloadThread
from win.DownloadPage.DownloadingItemList import DownloadingListWidget


class DownloadTabs(QTabWidget):
    def __init__(self,parent=None):
        super(DownloadTabs, self).__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

        self.setCurrentIndex(0)

        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):
        vbox = QVBoxLayout()
        self.downloadingtab = DownloadingListWidget()
        vbox.addWidget(self.downloadingtab)
        self.setTabText(0, '正在下载(6)')
        self.tab1.setLayout(vbox)

    def tab2UI(self):
        vbox = QVBoxLayout()
        placehoder = QLabel('YOLO9000 Tab Demo')
        font = QFont('Century Gothic', 20)
        placehoder.setFont(font)
        vbox.addWidget(placehoder)
        self.setTabText(1, '已完成')
        self.tab2.setLayout(vbox)


class DownloadTab(QWidget):
    def __init__(self,parent=None):
        super(DownloadTab, self).__init__(parent)

        #最上方
        label = QLabel('下载器')
        label.setObjectName('tablabel')
        label.setFont(QFont('黑体', 20))
        subTitle = QLabel('仅提供外链下载，提供下载历史')
        subTitle.setObjectName('tabsublabel')
        subTitle.setFont(QFont('黑体', 12))

        #中间部分
        self.firstRow = QHBoxLayout()
        self.secondRow = QHBoxLayout()

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
        #self.dirbtn.clicked.connect(self.showDir)
        self.secondRow.addWidget(self.locurl)
        self.secondRow.addWidget(self.locedit)
        self.secondRow.addWidget(self.dirbtn)

        #Tab部分
        self.tab = DownloadTabs()

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(subTitle)
        vbox.addLayout(self.firstRow)
        vbox.addLayout(self.secondRow)
        vbox.addWidget(self.tab)
        self.setLayout(vbox)

    def down(self):
        try:
            if self.urledit.text() == '':
                QMessageBox.information(self,"错误","URL不能为空")
                return
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setIcon(icon('fa.download',color='red'))
            self.tab.downloadingtab.addItem(item)
            self.tab.downloadingtab.setItemWidget(item, self.tab.downloadingtab.get_Item_Widget())
            # 创建线程
            # workthread = DownloadThread()
            # workthread.trigger.connect(self.progressbar)
            # workthread.trigger2.connect(self.downresult)
            # workthread.trigger3.connect(self.filesize)
            # workthread.url = self.urledit.text()
            # workthread.basedir = self.locedit.text()
            # workthread.start()
        except Exception as e:
            print(e)

    def progressbar(self, num):
        self.pbar.setValue(num)
        if num == 100:
            pass
            #info = strftime("%y/%M/%d %H:%M:%S", localtime()) + ":"
            #self.history.append(info)
            #self.downloadbtn.setEnabled(True)

    def downresult(self,info):
        #self.history.append(info)
        pass

    def filesize(self, size):
        pass
