import sys

from PyQt5.QtCore import QSize, Qt
from qtawesome import icon
from PyQt5.QtGui import QIntValidator, QCursor
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QToolButton, QLineEdit, QLabel


class Pagination(QWidget):
    def __init__(self, total_page, current_page):
        super(Pagination, self).__init__()
        self.setStyleSheet('''
            QToolButton#page{
                background: #202940 !important;
                border-radius: 16px;
                padding:4px;
                margin-right:8px;
            }
            QLabel#pagelabel{
                font:楷体;
                font-size:17px;
            }
            QLineEdit {
                color: #495057;
                background-color: #fff;
                border: 2px solid #ced4da;
                border-radius: 5px;
                font-size: 17px;
                border-color: #202940;
                padding: 5px;
            }
            QLineEdit:focus{
                border-color: #3e93ff;
            }
        ''')
        size = QSize(22, 22)
        cursor = QCursor(Qt.PointingHandCursor)
        self.main_layout = QHBoxLayout()

        self.firstbtn = QToolButton()
        self.firstbtn.setObjectName('page')
        self.firstbtn.setIcon(icon('fa5s.step-backward', scale_factor=1, color='#fff'))
        self.firstbtn.setIconSize(size)
        self.firstbtn.setCursor(cursor)
        self.firstbtn.setToolTip('第1页')

        self.prebtn = QToolButton()
        self.prebtn.setObjectName('page')
        self.prebtn.setIcon(icon('fa5s.chevron-circle-left', scale_factor=1, color='#fff'))
        self.prebtn.setIconSize(size)
        self.prebtn.setCursor(cursor)
        self.prebtn.setToolTip('上一页')

        self.nextbtn = QToolButton()
        self.nextbtn.setObjectName('page')
        self.nextbtn.setIcon(icon('fa5s.chevron-circle-right', scale_factor=1, color='#fff'))
        self.nextbtn.setIconSize(size)
        self.nextbtn.setCursor(cursor)
        self.nextbtn.setToolTip('下一页')

        self.lastbtn = QToolButton()
        self.lastbtn.setObjectName('page')
        self.lastbtn.setIcon(icon('fa5s.step-forward', scale_factor=1, color='#fff'))
        self.lastbtn.setIconSize(size)
        self.lastbtn.setCursor(cursor)
        self.lastbtn.setToolTip('第%d页' % total_page)

        self.currentlabel = QLabel()
        self.currentlabel.setObjectName('pagelabel')
        self.currentlabel.setText('当前第%d页，' % current_page)

        self.inputEdit = QLineEdit()
        pageValidator = QIntValidator(1, 999)
        self.inputEdit.setValidator(pageValidator)
        self.inputEdit.setFixedWidth(60)

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.firstbtn)
        self.main_layout.addWidget(self.prebtn)
        self.main_layout.addWidget(self.nextbtn)
        self.main_layout.addWidget(self.lastbtn)
        self.main_layout.addWidget(self.currentlabel)
        l1 = QLabel('跳转到第')
        l1.setObjectName('pagelabel')
        self.main_layout.addWidget(l1)
        self.main_layout.addWidget(self.inputEdit)
        l2 = QLabel('页')
        l2.setObjectName('pagelabel')
        self.main_layout.addWidget(l2)
        self.main_layout.addStretch(1)
        self.setLayout(self.main_layout)
        self.setContentsMargins(0,0,0,0)
        self.setFixedHeight(54)
