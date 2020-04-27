import sys

import qtawesome
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget, QHBoxLayout, \
    QVBoxLayout, QMainWindow, QGridLayout, QToolButton, QFrame, QLabel, \
    QStackedWidget
from PyQt5.QtGui import QIcon, QCursor

from CommomHelper import CommonHelper
from win.CV.CVTabs import ObjectDetectionTab
from win.LeftItemList import LeftListWidget
from win.WebSpider.SpiderTabs import SpiderTab


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

        #右侧上方三个按钮
        self.top_right_group = QHBoxLayout()
        self.top_right_group.addStretch(1)
        self.top_right_group.addWidget(self.leftmini)
        self.top_right_group.addWidget(self.leftvisit)
        self.top_right_group.addWidget(self.leftclose)

        #定义最主界面
        self.main_widget = QFrame()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        #右侧下方的StackWidget
        self.stack=QStackedWidget(self)
        self.spidertab = SpiderTab()
        self.cvtab = ObjectDetectionTab()
        self.demotab = QWidget()
        self.stack.addWidget(self.spidertab)
        self.stack.addWidget(self.cvtab)

        #右侧全部
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.top_right_group)
        self.vbox.addWidget(self.stack)

        #定义左侧
        self.left_widget = QWidget()
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)

        #定义右侧
        self.right_widget = QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = self.vbox
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.setContentsMargins(8,8,8,0)

        #将左侧和右侧加到最主窗体中
        self.main_layout.addWidget(self.left_widget,0,0,12,2)
        self.main_layout.addWidget(self.right_widget,0,2,12,10)

        #左侧的按钮们
        self.left_label_1 = QLabel("功能")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QLabel("设置")
        self.left_label_2.setObjectName('left_label')
        self.leftlist=LeftListWidget()
        self.leftlist.setObjectName('fun')
        self.leftlist.currentRowChanged.connect(self.display)
        self.left_layout.addWidget(self.left_label_1)
        self.left_layout.addWidget(self.leftlist, alignment=QtCore.Qt.AlignHCenter)
        self.left_layout.addWidget(self.left_label_2)
        self.left_layout.addStretch(1)

        #最主窗体的设置
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.main_widget)
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)
        self.resize(self.screenWidth, self.screenHeight)
        self.setWindowTitle('微信信息验证')
        self.setWindowIcon(QIcon('res/icon.png'))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()

    def display(self,i):
        self.stack.setCurrentIndex(i)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindowUI()
    styleFile = 'res/style.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    win.setStyleSheet(qssStyle)
    win.show()
    sys.exit(app.exec_())
