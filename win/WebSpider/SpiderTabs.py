import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, QTabWidget, QWidget, QVBoxLayout, \
    QPushButton, QHBoxLayout, QInputDialog, QMessageBox, QTextEdit, QGridLayout, QFileDialog
from qtawesome import icon

from service.CommomHelper import CommonHelper
from service.WebSpider.parse import get_url_param
from thread.WebSpider.SpiderSaveThread import SpiderSaveThread
from thread.WebSpider.SpiderThread import SpiderThread


class SpiderSettingTab(QWidget):
    def __init__(self):
        super(SpiderSettingTab, self).__init__()
        self.setupUI()

    def setupUI(self):
        self.firstBlock_layout = QFormLayout()
        self.chooseURLButton = QPushButton('点击选择保存路径')
        self.chooseURLButton.setIcon(icon('fa5.file', color='cadetblue'))
        self.chooseURLButton.setIconSize(QSize(27, 27))
        self.chooseURLButton.clicked.connect(self.on_urlbtn_clicked)
        self.chooseURLButton.setObjectName('urlbtn')
        self.get_directory_path = 'C:/'
        self.URLLabel = QLabel(self.get_directory_path)
        self.URLLabel.setWordWrap(True)
        self.URLLabel.setObjectName('content')
        self.firstBlock_layout.addRow(self.chooseURLButton, self.URLLabel)
        self.firstBlock_filename_label = QLabel('文件名')
        self.firstBlock_filename_label.setObjectName('content')
        self.firstBlock_filename_input = QLineEdit()
        self.firstBlock_filename_input.setDragEnabled(True)
        self.firstBlock_filename_input.setClearButtonEnabled(True)
        self.firstBlock_layout.addRow(self.firstBlock_filename_label, self.firstBlock_filename_input)
        self.firstBlock_waittime_label = QLabel('缓冲时间')
        self.firstBlock_waittime_label.setObjectName('content')
        self.firstBlock_waittime_input = QLineEdit()
        self.firstBlock_waittime_input.setDragEnabled(True)
        self.firstBlock_waittime_input.setClearButtonEnabled(True)
        self.firstBlock_layout.addRow(self.firstBlock_waittime_label, self.firstBlock_waittime_input)

        self.save_btn = QPushButton('保存更改')
        self.save_btn.setFixedWidth(200)
        self.save_btn.clicked.connect(self.savebtnclick)

        hbox1 = QVBoxLayout()
        hbox1.setContentsMargins(10, 10, 10, 10)
        hbox1.addStretch(1)
        hbox1.addLayout(self.firstBlock_layout)
        hbox1.addWidget(self.save_btn, alignment=Qt.AlignCenter)
        hbox1.addStretch(1)

        self.setLayout(hbox1)
        self.readSetting()

    def on_urlbtn_clicked(self):
        self.get_directory_path = QFileDialog.getExistingDirectory(self, "选取指定文件夹", "C:/")
        self.URLLabel.setText(str(self.get_directory_path))

    def savebtnclick(self):
        filename = self.firstBlock_filename_input.text()
        sleeptime = self.firstBlock_waittime_input.text()
        setting = {"filename": filename,
                   "sleeptime": sleeptime}
        self.thread = SpiderSaveThread(setting=setting)
        self.thread.signal.connect(self.savebtnclickcallback)
        self.thread.start()

    def savebtnclickcallback(self, msg):
        if msg == 'activate':
            QMessageBox.information(self, "成功", "设置保存成功！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.critical(self, '错误', msg, QMessageBox.Abort)

    def readSetting(self):
        setting = CommonHelper.load_setting('config/wxspider_setting.cm')
        self.firstBlock_waittime_input.setText(setting['sleeptime'])
        self.firstBlock_filename_input.setText(setting['filename'])


class SpiderTabs(QTabWidget):
    def __init__(self, parent=None):
        super(SpiderTabs, self).__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = SpiderSettingTab()

        self.biz = QLabel('__biz')
        self.biz.setObjectName('content')
        self.appmsg_token = QLabel('appmsg_token')
        self.appmsg_token.setObjectName('content')
        self.cookie = QLabel('Cookie')
        self.cookie.setObjectName('content')

        self.bizEdit = QLineEdit()
        self.bizEdit.setPlaceholderText('请输入__biz的值')
        self.bizEdit.setClearButtonEnabled(True)
        self.bizEdit.setDragEnabled(True)
        self.cookieEdit = QTextEdit()
        self.cookieEdit.setPlaceholderText('请输入Cookie值')
        self.cookieEdit.setAcceptRichText(False)
        self.appmsg_tokenEdit = QLineEdit()
        self.appmsg_tokenEdit.setPlaceholderText('请输入appmsg_token的值')
        self.appmsg_tokenEdit.setClearButtonEnabled(True)
        self.appmsg_tokenEdit.setDragEnabled(True)

        self.urlLabel = QLabel('输入URL（mp/profile_ext?action）：')
        self.urlLabel.setObjectName('content')
        self.urll = QLabel('URL')
        self.urll.setObjectName('content')
        self.urlEdit = QLineEdit()
        self.urlEdit.setDragEnabled(True)
        self.urlEdit.setClearButtonEnabled(True)
        #暂时停用
        self.urlEdit.setPlaceholderText('暂时停用，请使用手动输入方式')
        self.urlEdit.setDisabled(True)

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, 'Tab 3')

        self.setMovable(True)
        self.setElideMode(Qt.ElideMiddle)

        self.setCurrentIndex(0)

        self.tab1UI()
        self.tab2UI()
        self.setTabToolTip(2, '爬取公众号的参数设置')
        self.setTabText(2, '设置')

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow(self.biz, self.bizEdit)
        layout.addRow(self.appmsg_token, self.appmsg_tokenEdit)
        layout.addRow(self.cookie, self.cookieEdit)
        layout.setContentsMargins(20, 50, 20, 50)
        self.setTabText(0, '手动输入')
        hbox = QGridLayout()
        hbox.addLayout(layout, 0, 0, 5, 5)
        self.tab1.setLayout(hbox)

    def tab2UI(self):
        layout = QFormLayout()
        layout.addRow(self.urlLabel)
        layout.addRow(self.urll, self.urlEdit)
        layout.setContentsMargins(20, 20, 20, 50)
        self.setTabText(1, '自动提取')
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(layout)
        vbox.addStretch(1)
        self.tab2.setLayout(vbox)


class SpiderTab(QWidget):
    def __init__(self, parent=None):
        super(SpiderTab, self).__init__(parent)

        # 最上方
        label = QLabel('爬取微信公众号的文章')
        label.setObjectName('tablabel')
        label.setFont(QFont('黑体', 20))
        subTitle = QLabel('通过输入微信公众号的页面地址，提取参数，最后进行文章的爬取。')
        subTitle.setObjectName('tabsublabel')
        subTitle.setFont(QFont('黑体', 12))

        # 最下方
        self.btn = QPushButton('连接', self)
        self.btn.setToolTip('点击连接')
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(self.spiderbtnclick)
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.btn)

        # 中间部分
        self.tab = SpiderTabs()

        # status状态栏
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
        filename_option = os.path.join(self.tab.tab3.URLLabel.text(), self.tab.tab3.firstBlock_filename_input.text())
        waittime_option = self.tab.tab3.firstBlock_waittime_input.text()
        if filename_option == '':
            filename_option = os.path.join(self.tab.tab3.URLLabel.text(), 'datastmp.csv')
        if waittime_option == '':
            waittime_option = 10
        if self.tab.urlEdit.text() != '':
            param = get_url_param(self.tab.urlEdit.text())
            self.tab.bizEdit.setText(param['__biz'])
            self.tab.appmsg_tokenEdit.setText(param['appmsg_token'])
        if okPressed and text != '':
            self.thread = SpiderThread(biz=self.tab.bizEdit.text(),
                                       cookie=self.tab.cookieEdit.toPlainText(),
                                       appmsg_token=self.tab.appmsg_tokenEdit.text(),
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
                QMessageBox.information(self, "成功", "爬取数据并保存成功！", QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.critical(self, '错误', '爬取失败，请检查合理的url路径！', QMessageBox.Abort, QMessageBox.Abort)
            self.btn.setEnabled(True)
            self.statusInfo.setText('')
            self.tab.bizEdit.setText('')
            self.tab.appmsg_tokenEdit.setText('')
            self.tab.cookieEdit.setPlainText('')
            # self.tab.urlEdit.setText('')
        except Exception as e:
            print(e)
