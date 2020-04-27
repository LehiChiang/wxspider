import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, QTabWidget, QWidget, QApplication, QVBoxLayout, \
    QPushButton, QHBoxLayout, QInputDialog, QMessageBox

from service.WebSpider.parse import get_url_param
from thread.WebSpider.SpiderThread import SpiderThread


class SpiderTabs(QTabWidget):
    def __init__(self,parent=None):
        super(SpiderTabs, self).__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.biz = QLabel('biz')
        self.biz.setObjectName('content')
        self.uin = QLabel('uin')
        self.uin.setObjectName('content')
        self.key = QLabel('key')
        self.key.setObjectName('content')


        self.bizEdit = QLineEdit()
        self.bizEdit.setClearButtonEnabled(True)
        self.uinEdit = QLineEdit()
        self.uinEdit.setClearButtonEnabled(True)
        self.keyEdit = QLineEdit()
        self.keyEdit.setClearButtonEnabled(True)

        self.urlLabel = QLabel('输入URL（mp/profile_ext?action）：')
        self.urlLabel.setObjectName('content')
        self.urll = QLabel('URL')
        self.urll.setObjectName('content')
        self.urlEdit = QLineEdit()
        self.urlEdit.setClearButtonEnabled(True)

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

        self.setCurrentIndex(1)

        optitle = QtWidgets.QGraphicsOpacityEffect()
        optitle.setOpacity(0.7)
        self.setGraphicsEffect(optitle)
        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow(self.biz, self.bizEdit)
        layout.addRow(self.uin, self.uinEdit)
        layout.addRow(self.key, self.keyEdit)
        self.setTabText(0, '手动输入')
        self.tab1.setLayout(layout)

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
        if self.tab.urlEdit.text() != '':
            param = get_url_param(self.tab.urlEdit.text())
            self.tab.bizEdit.setText(param['__biz'])
            self.tab.uinEdit.setText(param['uin'])
            self.tab.keyEdit.setText(param['key'])
        if okPressed and text != '':
            self.thread = SpiderThread(biz=self.tab.bizEdit.text(),
                                       uin=self.tab.uinEdit.text(),
                                       key=self.tab.keyEdit.text(),
                                       option=text)
            self.thread.signal.connect(self.spidercallback)
            self.thread.start()
            self.statusInfo.setText("正在爬取，请等待......")
            self.btn.setEnabled(False)
        else:
            pass

    def spidercallback(self, msg):
        if msg == 'activate':
            self.btn.setEnabled(True)
            self.statusInfo.setText(None)
            self.tab.bizEdit.setText(None)
            self.tab.uinEdit.setText(None)
            self.tab.keyEdit.setText(None)
            self.tab.urlEdit.setText(None)
            QMessageBox.information(self, "成功", "爬取数据并保存成功！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.critical(self, '错误', msg, QMessageBox.Abort)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SpiderTab()
    win.show()
    sys.exit(app.exec_())
