from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QListWidgetItem, QMessageBox, QFileDialog, QTabBar
from qtawesome import icon

from thread.DownloadPage.DownloadThread import DownloadThread
from win.DownloadPage.DownloadItemList import DownloadingListWidget, DownloadedListWidget


class TabBar(QTabBar):
    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        w = int(self.width() / self.count())
        return QSize(w, size.height())


class DownloadTabs(QTabWidget):
    def __init__(self, parent=None):
        super(DownloadTabs, self).__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "正在下载")
        self.addTab(self.tab2, "已完成")
        self.setMovable(True)
        self.setElideMode(Qt.ElideMiddle)

        self.setCurrentIndex(0)

        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):
        vbox = QVBoxLayout()
        self.downloadingtab = DownloadingListWidget()
        vbox.addWidget(self.downloadingtab)
        self.tab1.setLayout(vbox)

    def tab2UI(self):
        vbox = QVBoxLayout()
        self.downloadedtab = DownloadedListWidget()
        vbox.addWidget(self.downloadedtab)
        self.tab2.setLayout(vbox)


class DownloadTab(QWidget):
    def __init__(self, parent=None):
        super(DownloadTab, self).__init__(parent)
        self.workthread = DownloadThread()
        self.workthread.trigger.connect(self.progressbar)
        self.workthread.trigger2.connect(self.downresult)
        self.workthread.trigger3.connect(self.filesize)
        self.workthread.trigger4.connect(self.filetitle)

        # 最上方
        label = QLabel('下载器')
        label.setObjectName('tablabel')
        label.setFont(QFont('黑体', 20))
        subTitle = QLabel('仅提供外链下载，提供下载历史')
        subTitle.setObjectName('tabsublabel')
        subTitle.setFont(QFont('黑体', 12))

        # 中间部分
        self.firstRow = QHBoxLayout()
        self.secondRow = QHBoxLayout()

        self.urllabel = QLabel("下载链接:")
        self.urllabel.setObjectName('content')
        self.urledit = QLineEdit()
        # self.urledit.setText('https://dldir1.qq.com/weixin/Windows/WeChatSetup.exe')
        # self.urledit.setText('https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B9B1246D2-897D-C009-E882-BCA0E62162DB%7D%26lang%3Dzh-CN%26browser%3D4%26usagestats%3D1%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26installdataindex%3Dempty/update2/installers/ChromeSetup.exe')
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

        # Tab部分
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
                QMessageBox.information(self, "错误", "URL不能为空")
                return
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setIcon(icon('fa.download', color='red'))
            self.tab.downloadingtab.addItem(item)
            self.tab.downloadingtab.setItemWidget(item, self.tab.downloadingtab.get_Item_Widget())
            self.downloadbtn.setEnabled(False)
            self.workthread.url = self.urledit.text()
            self.workthread.basedir = self.locedit.text()
            self.workthread.start()
        except Exception as e:
            print(e)

    def progressbar(self, num):
        self.tab.downloadingtab.pbar.setValue(num)
        if num == 100:
            self.downloadbtn.setEnabled(True)
            self.tab.downloadingtab.clear()

    def downresult(self, info):
        infor, path = info.split('|')
        item = QListWidgetItem()
        item.setIcon(icon('fa.download', color='green'))
        self.tab.downloadedtab.addItem(item)
        self.tab.downloadedtab.setItemWidget(item,
                                             self.tab.downloadedtab.get_Item_Widget(title=self.tmptitle, info=infor,
                                                                                    url=path))

    def filesize(self, size):
        self.tab.downloadingtab.sizelabel.setText(size)

    def filetitle(self, title):
        self.tmptitle = title
        self.tab.downloadingtab.title.setText(title)

    def showDir(self):
        download_path = QFileDialog.getExistingDirectory(self, "浏览", r"C:/Users/Administrator/Desktop")
        self.locedit.setText(download_path)
