from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, QTabWidget, QWidget, QVBoxLayout, \
    QPushButton, QHBoxLayout, QInputDialog, QMessageBox, QAction

from CommomHelper import CommonHelper
from service.WebSpider.parse import get_url_param
from thread.WebSpider.SpiderSaveThread import SpiderSaveThread
from thread.WebSpider.SpiderThread import SpiderThread


class SpiderSettingTab(QWidget):
    def __init__(self):
        super(SpiderSettingTab, self).__init__()
        self.setupUI()

    def setupUI(self):
        grid = QVBoxLayout()
        self.label1 = QLabel('基本设置')
        self.label1.setObjectName('content')
        self.label2 = QLabel('高级设置')
        self.label2.setObjectName('content')

        self.firstBlock_layout = QFormLayout()
        self.firstBlock_filename_label = QLabel('文件名')
        self.firstBlock_filename_label.setObjectName('content')
        self.firstBlock_filename_input = QLineEdit()
        self.firstBlock_filename_input.setDragEnabled(True)
        self.firstBlock_filename_input.setClearButtonEnabled(True)
        self.firstBlock_layout.addRow(self.firstBlock_filename_label, self.firstBlock_filename_input)
        self.firstBlock_waittime_label = QLabel('等待时间')
        self.firstBlock_waittime_label.setObjectName('content')
        self.firstBlock_waittime_input = QLineEdit()
        self.firstBlock_waittime_input.setDragEnabled(True)
        self.firstBlock_waittime_input.setClearButtonEnabled(True)
        self.firstBlock_layout.addRow(self.firstBlock_waittime_label, self.firstBlock_waittime_input)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.label1, 1, alignment=Qt.AlignTop)
        hbox1.addLayout(self.firstBlock_layout, 3)
        hbox1.addStretch(1)

        self.save_btn = QPushButton('保存更改')
        self.save_btn.setFixedWidth(150)
        self.save_btn.resize(self.save_btn.sizeHint())
        self.save_btn.clicked.connect(self.savebtnclick)

        grid.addLayout(hbox1)
        grid.addWidget(self.save_btn, alignment=Qt.AlignCenter)
        grid.addStretch(1)
        self.setLayout(grid)
        self.readSetting()


    def savebtnclick(self):
        filename = self.firstBlock_filename_input.text()
        sleeptime = self.firstBlock_waittime_input.text()
        setting = {"filename":filename,
                   "sleeptime":sleeptime}
        self.thread = SpiderSaveThread(setting=setting)
        self.thread.signal.connect(self.savebtnclickcallback)
        self.thread.start()

    def savebtnclickcallback(self, msg):
        if msg == 'activate':
            QMessageBox.information(self, "成功", "设置保存成功！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.critical(self, '错误', msg, QMessageBox.Abort)

    def readSetting(self):
        setting = CommonHelper.load_setting('../config/wxspider_setting.cm')
        self.firstBlock_waittime_input.setText(setting['sleeptime'])
        self.firstBlock_filename_input.setText(setting['filename'])


class SpiderTabs(QTabWidget):
    def __init__(self,parent=None):
        super(SpiderTabs, self).__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = SpiderSettingTab()

        self.biz = QLabel('biz')
        self.biz.setObjectName('content')
        self.uin = QLabel('uin')
        self.uin.setObjectName('content')
        self.key = QLabel('key')
        self.key.setObjectName('content')


        self.bizEdit = QLineEdit()
        self.bizEdit.setClearButtonEnabled(True)
        self.bizEdit.setDragEnabled(True)
        self.uinEdit = QLineEdit()
        self.uinEdit.setClearButtonEnabled(True)
        self.uinEdit.setDragEnabled(True)
        self.keyEdit = QLineEdit()
        self.keyEdit.setClearButtonEnabled(True)
        self.keyEdit.setDragEnabled(True)

        self.urlLabel = QLabel('输入URL（mp/profile_ext?action）：')
        self.urlLabel.setObjectName('content')
        self.urll = QLabel('URL')
        self.urll.setObjectName('content')
        self.urlEdit = QLineEdit()
        self.urlEdit.setDragEnabled(True)
        self.urlEdit.setClearButtonEnabled(True)

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, 'Tab 3')

        self.setCurrentIndex(1)

        # optitle = QtWidgets.QGraphicsOpacityEffect()
        # optitle.setOpacity(0.7)
        # self.setGraphicsEffect(optitle)
        self.tab1UI()
        self.tab2UI()
        self.setTabToolTip(2, '爬取公众号的参数设置')
        self.setTabText(2, '设置')


    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow(self.biz, self.bizEdit)
        layout.addRow(self.uin, self.uinEdit)
        layout.addRow(self.key, self.keyEdit)
        self.setTabText(0, '手动输入')
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(layout)
        hbox.addStretch(1)
        self.tab1.setLayout(hbox)

    def tab2UI(self):
        layout = QFormLayout()
        layout.addRow(self.urlLabel)
        layout.addRow(self.urll, self.urlEdit)
        self.setTabText(1, '自动提取')
        self.tab2.setLayout(layout)


class SpiderTab(QWidget):
    def __init__(self,parent=None):
        super(SpiderTab, self).__init__(parent)

        #最上方
        label = QLabel('爬取微信公众号的文章')
        label.setObjectName('tablabel')
        label.setFont(QFont('黑体', 20))
        subTitle = QLabel('通过输入微信公众号的页面地址，提取参数，最后进行文章的爬取。')
        subTitle.setObjectName('tabsublabel')
        subTitle.setFont(QFont('黑体', 12))

        #最下方
        self.btn = QPushButton('连接', self)
        self.btn.setToolTip('点击连接')
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(self.spiderbtnclick)
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.btn)

        #中间部分
        self.tab = SpiderTabs()

        #status状态栏
        self.statusBar = QHBoxLayout()
        self.statusBar.setObjectName('statusbar')
        self.statusInfo = QLabel()
        self.statusBar.addWidget(self.statusInfo)
        self.statusInfo.setStyleSheet('font-family:微软雅黑;color: grey;')

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(subTitle)
        vbox.addWidget(self.tab)
        vbox.addLayout(self.hbox)
        vbox.addLayout(self.statusBar)
        self.setLayout(vbox)

    def spiderbtnclick(self):
        text, okPressed = QInputDialog.getText(self,
                                               "输入",
                                               "爬取全部输入‘all’，自定义页数输入页数，（例如：‘2’）：",
                                               QLineEdit.Normal, "")
        filename_option = self.tab.tab3.firstBlock_filename_input.text()
        waittime_option = self.tab.tab3.firstBlock_waittime_input.text()
        if filename_option == '':
            filename_option = 'datastmp.csv'
        if waittime_option == '':
            waittime_option = 10
        if self.tab.urlEdit.text() != '':
            param = get_url_param(self.tab.urlEdit.text())
            self.tab.bizEdit.setText(param['__biz'])
            self.tab.uinEdit.setText(param['uin'])
            self.tab.keyEdit.setText(param['key'])
        if okPressed and text != '':
            self.thread = SpiderThread(biz=self.tab.bizEdit.text(),
                                       uin=self.tab.uinEdit.text(),
                                       key=self.tab.keyEdit.text(),
                                       option=text,
                                       filename=filename_option,
                                       sleeptime=int(waittime_option))
            self.thread.signal.connect(self.spidercallback)
            self.thread.start()
            self.statusInfo.setText("正在爬取，请等待......")
            self.btn.setEnabled(False)
        else:
            pass

    def spidercallback(self, msg):
        try:
            if msg == 'activate':
                print('Scraping Successfully!')
                QMessageBox.information(self, "成功", "爬取数据并保存成功！", QMessageBox.Yes, QMessageBox.Yes)
            else:
                print('There is something wrong with the URL!')
                QMessageBox.critical(self, '错误', '爬取失败，请检查合理的url路径！', QMessageBox.Abort, QMessageBox.Abort)
            self.btn.setEnabled(True)
            self.statusInfo.setText(None)
            self.tab.bizEdit.setText(None)
            self.tab.uinEdit.setText(None)
            self.tab.keyEdit.setText(None)
            self.tab.urlEdit.setText(None)
        except Exception as e:
            print(e)
