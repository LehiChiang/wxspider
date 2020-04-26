import math
import sys

import qtawesome
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QHBoxLayout, \
    QVBoxLayout, QLineEdit, QMainWindow, QInputDialog, QGridLayout, QToolButton, QFrame, QLabel
from PyQt5.QtGui import QIcon, QCursor

import SpiderTabs as st

from CommomHelper import CommonHelper
from parse import get_url_param
from thread.SpiderThread import SpiderThread


class MainWindowUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.iconsizenum = 25
        self.widthRatio = 0.65
        self.heightRatio = 0.7
        desktop = QApplication.desktop()
        self.winWidth = desktop.width()
        self.winHeight = desktop.height()
        self.screenWidth = self.winWidth * self.widthRatio
        self.screenHeight = self.winHeight * self.heightRatio
        self.initUI()

    def initUI(self):

        self.btn = QPushButton('连接', self)
        self.btn.setToolTip('点击连接')
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(self.spiderbtnclick)

        self.leftclose = QToolButton()
        self.leftclose.setIcon(qtawesome.icon('fa.times', color='white'))
        self.leftclose.setIconSize(QSize(self.iconsizenum, self.iconsizenum))
        self.leftclose.setObjectName('left_close')
        self.leftclose.setToolTip('关闭程序')
        self.leftclose.setFixedSize(self.iconsizenum, self.iconsizenum)
        self.leftclose.clicked.connect(self.quitbtnclick)

        self.leftvisit = QToolButton()
        self.leftvisit.setIcon(qtawesome.icon('fa5s.window-maximize', color='white'))
        self.leftvisit.setIconSize(QSize(self.iconsizenum, self.iconsizenum))
        self.leftvisit.setObjectName('left_visit')
        self.leftvisit.setToolTip('最大化界面')
        self.leftvisit.setFixedSize(self.iconsizenum, self.iconsizenum)
        self.leftvisit.clicked.connect(self.windowMaximize)

        self.leftmini = QToolButton()
        self.leftmini.setIcon(qtawesome.icon('fa5s.window-minimize', color='white'))
        self.leftmini.setIconSize(QSize(self.iconsizenum, self.iconsizenum))
        self.leftmini.setObjectName('left_mini')
        self.leftmini.setToolTip('最小化界面')
        self.leftmini.setFixedSize(self.iconsizenum, self.iconsizenum)
        self.leftmini.clicked.connect(self.windowMinimize)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.btn)

        self.top_right_group = QHBoxLayout()
        self.top_right_group.addStretch(1)
        self.top_right_group.addWidget(self.leftmini)
        self.top_right_group.addWidget(self.leftvisit)
        self.top_right_group.addWidget(self.leftclose)

        self.tab = st.SpiderTab()

        self.main_widget = QFrame()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        self.left_widget = QWidget()
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)

        self.right_widget = QWidget()
        self.right_widget.setObjectName('right_widget')
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.top_right_group)
        self.vbox.addWidget(self.tab)
        self.vbox.addLayout(self.hbox)
        self.right_layout = self.vbox
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.setContentsMargins(8,8,8,0)

        self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列


        self.left_label_1 = QLabel("每日推荐")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QLabel("我的音乐")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QLabel("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        self.left_button_2 = QPushButton(qtawesome.icon('fa.sellsy',color='white'),"在线FM")
        self.left_button_2.setObjectName('left_button')
        self.left_button_4 = QPushButton(qtawesome.icon('fa.home',color='white'),"本地音乐")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QPushButton(qtawesome.icon('fa.download',color='white'),"下载管理")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QPushButton(qtawesome.icon('fa.heart',color='white'),"我的收藏")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QPushButton(qtawesome.icon('fa.comment',color='white'),"反馈建议")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QPushButton(qtawesome.icon('fa.star',color='white'),"关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QPushButton(qtawesome.icon('fa.question',color='white'),"遇到问题")
        self.left_button_9.setObjectName('left_button')

        self.left_layout.addWidget(self.left_label_1)
        self.left_layout.addWidget(self.left_button_2)
        self.left_layout.addWidget(self.left_label_2)
        self.left_layout.addWidget(self.left_button_4)
        self.left_layout.addWidget(self.left_button_5)
        self.left_layout.addWidget(self.left_button_6)
        self.left_layout.addWidget(self.left_label_3)
        self.left_layout.addWidget(self.left_button_7)
        self.left_layout.addWidget(self.left_button_8)
        self.left_layout.addWidget(self.left_button_9)
        self.left_layout.addStretch(1)

        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.main_widget)
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)
        self.resize(self.screenWidth, self.screenHeight)
        self.setWindowTitle('微信信息验证')
        self.setWindowIcon(QIcon('res/icon.png'))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '消息',
                                     "你确定要退出吗？", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def windowMaximize(self):
        if self.windowState() == QtCore.Qt.WindowNoState:
            self.setWindowState(QtCore.Qt.WindowMaximized)
        elif self.windowState() == QtCore.Qt.WindowMaximized:
            self.setWindowState(QtCore.Qt.WindowNoState)

    def windowMinimize(self):
        self.setWindowState(QtCore.Qt.WindowMinimized)

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

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        self.windowMaximize()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def quitbtnclick(self):
        self.close()


class MainWindowService(MainWindowUI):

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindowService()
    styleFile = 'res/style.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    win.setStyleSheet(qssStyle)
    win.show()
    sys.exit(app.exec_())
