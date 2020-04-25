from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel,QFormLayout, QLineEdit, QTabWidget, QWidget, QGridLayout


class SpiderTab(QTabWidget):
    def __init__(self,parent=None):
        super(SpiderTab, self).__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        font = QFont()   #实例化字体对象
        font.setFamily('Century Gothic')  #字体
        font.setBold(True)  #加粗

        self.biz = QLabel('biz')
        self.biz.setFont(font)
        self.uin = QLabel('uin')
        self.uin.setFont(font)
        self.key = QLabel('key')
        self.key.setFont(font)


        self.bizEdit = QLineEdit()
        self.bizEdit.setClearButtonEnabled(True)
        self.bizEdit.setFont(font)
        self.uinEdit = QLineEdit()
        self.uinEdit.setClearButtonEnabled(True)
        self.uinEdit.setFont(font)
        self.keyEdit = QLineEdit()
        self.keyEdit.setClearButtonEnabled(True)
        self.keyEdit.setFont(font)

        self.urlLabel = QLabel('输入URL（mp/profile_ext?action）：')
        self.urlLabel.setFont(font)
        self.urll = QLabel('URL')
        self.urll.setFont(font)
        self.urlEdit = QLineEdit()
        self.urlEdit.setClearButtonEnabled(True)
        self.urlEdit.setFont(font)

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

        self.setCurrentIndex(1)


        # optab = QtWidgets.QGraphicsOpacityEffect()
        # optab.setOpacity(0.3)
        # self.tab1.setGraphicsEffect(optab)
        # self.tab2.setGraphicsEffect(optab)
        optitle = QtWidgets.QGraphicsOpacityEffect()
        optitle.setOpacity(0.7)
        self.setGraphicsEffect(optitle)
        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.biz, 1, 0)
        grid.addWidget(self.bizEdit, 1, 1)
        grid.addWidget(self.uin, 2, 0)
        grid.addWidget(self.uinEdit, 2, 1)
        grid.addWidget(self.key, 3, 0)
        grid.addWidget(self.keyEdit, 3, 1)
        self.setTabText(0, '手动输入')
        self.tab1.setLayout(grid)

    def tab2UI(self):
        layout=QFormLayout()

        layout.addRow(self.urlLabel)
        layout.addRow(self.urll, self.urlEdit)

        self.setTabText(1,'自动提取')
        self.tab2.setLayout(layout)
