import sys

from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget, QHBoxLayout, \
    QVBoxLayout, QLineEdit,QMainWindow, QInputDialog
from PyQt5.QtGui import QIcon, QFont

import SpiderTabs as st

from parse import get_url_param
from thread.SpiderThread import SpiderThread


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.qbtn = QPushButton('退出', self)
        self.qbtn.clicked.connect(self.quitbtnclick)
        self.qbtn.resize(self.qbtn.sizeHint())

        self.btn = QPushButton('连接', self)
        self.btn.setToolTip('点击连接')
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(self.spiderbtnclick)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btn)
        hbox.addWidget(self.qbtn)

        self.tab = st.SpiderTab()

        vbox = QVBoxLayout()
        vbox.addWidget(self.tab)
        vbox.addLayout(hbox)

        panel = QWidget()
        panel.setLayout(vbox)
        self.setCentralWidget(panel)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('微信信息验证')
        self.setWindowIcon(QIcon('res/icon.png'))
        self.center()
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '消息',
                                     "你确定要退出吗？", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
            self.btn.setEnabled(False)
        else:
            pass

    def spidercallback(self, msg):
        if msg == 'activate':
            self.btn.setEnabled(True)
            self.tab.bizEdit.setText(None)
            self.tab.uinEdit.setText(None)
            self.tab.keyEdit.setText(None)
            self.tab.urlEdit.setText(None)
            QMessageBox.information(self, "成功", "爬取数据并保存成功！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.critical(self, '错误', msg, QMessageBox.Abort)

    def quitbtnclick(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_()) 