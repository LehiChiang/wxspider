from PyQt5.QtWidgets import QLabel,QFormLayout, QLineEdit, QTabWidget, QWidget, QGridLayout


class SpiderTab(QTabWidget):
    def __init__(self,parent=None):
        super(SpiderTab, self).__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.biz = QLabel('biz')
        self.uin = QLabel('uin')
        self.key = QLabel('key')

        self.bizEdit = QLineEdit()
        self.uinEdit = QLineEdit()
        self.keyEdit = QLineEdit()

        self.urlLabel = QLabel('输入URL（mp/profile_ext?action）：')
        self.urlEdit = QLineEdit()

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

        self.setCurrentIndex(1)

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
        layout.addRow('URL：', self.urlEdit)

        self.setTabText(1,'自动提取')
        self.tab2.setLayout(layout)
