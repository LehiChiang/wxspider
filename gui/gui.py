import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QHBoxLayout, \
    QVBoxLayout, QLineEdit, QMainWindow, QInputDialog
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QCursor

import SpiderTabs as st

from parse import get_url_param
from thread.SpiderThread import SpiderThread


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
        self.tab.tab1.setStatusTip('手动添加请求参数爬取数据')
        self.tab.tab2.setStatusTip('提供URL分析并爬取数据')

        vbox = QVBoxLayout()
        vbox.addWidget(self.tab)
        vbox.addLayout(hbox)

        panel = QWidget()
        panel.setLayout(vbox)
        panel.setContentsMargins(8,35,8,0)
        self.statusBar()
        self.setCentralWidget(panel)
        self.setStyleSheet('*{padding:5px}'
                           'QStatusBar{font-family:幼圆;font-size: 14px;}'
                           'QLineEdit{font:bold;font-size: 17px;}'
                           'QLabel{font-size: 17px;}'
                           '''
                           QTabWidget::pane{
                                border:none;
                            }
                            QTabWidget::tab-bar{
                                alignment:left;
                            }
                           QTabBar::tab{
                                margin-right:1ex;
                                background:transparent;
                                color:white;
                                font:bold;
                                font-size:15px;
                                font-family:幼圆;
                                min-width:25ex;
                                min-height:8ex;
                                border-radius:10px
                            }
                            QTabBar::tab:hover{
                                background:rgb(255, 255, 255, 100);
                            }
                            QTabBar::tab:selected{
                                border-color: white;
                                background:white;
                                color:red;
                            }
                           '''
                           '''QPushButton{
                                margin-top: 6px;
                                margin-bottom: 6px;
                                height: 30px;
                                line-height: 28px;
                                min-width: 72px;
                                margin-left: 8px;
                                margin-right: 8px;
                                font-family: 黑体;
                                padding: 0 8px;
                                display: inline-block;
                                font-size: 14px;
                                border-radius: 4px;
                                text-align: center;
                                color: #fff !important;
                                border: 1px solid #ca0c16 !important;
                                background-color: #ca0c16 !important;
                                cursor: pointer;
                            }''')
        self.setGeometry(0, 0, 700, 500)
        self.setWindowTitle('微信信息验证')
        self.setWindowIcon(QIcon('res/icon.png'))
        self.pix = QPixmap("res/bg2.png")  # 蒙版
        self.resize(self.pix.size())
        self.setMask(self.pix.mask())

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.width(), self.height())
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

    def paintEvent(self, event):  # 绘制窗口
        painter=QPainter(self)
        painter.drawPixmap(0,0,self.pix.width(),self.pix.height(), self.pix)

    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))  #更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

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
            self.setStatusTip('正在爬取，请等待........')
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
            self.setStatusTip('成功！')
        else:
            QMessageBox.critical(self, '错误', msg, QMessageBox.Abort)

    def quitbtnclick(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
