import sys

import qtawesome as qta
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem, QVBoxLayout, QWidget, QLabel, QApplication, QListWidget

import CommomHelper


class LeftListWidget(QListWidget):

    def __init__(self):
        super(LeftListWidget, self).__init__()

        menu_data = CommomHelper.CommonHelper.load_json('../config/menu.json')

        self.setIconSize(QSize(24, 24))
        self.setFont(QFont('黑体', 11))
        self.setFixedWidth(200)
        self.setViewMode(QListWidget.ListMode)

        for menu in menu_data['menu']:
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setIcon(qta.icon(menu['icon'],color='#fff'))
            self.addItem(item)
            self.setItemWidget(item, self.get_Item_Widget(menu['title']))

    def get_Item_Widget(self, titletxt):
        wight = QWidget()
        self.layout_main = QVBoxLayout()
        self.title = QLabel()
        self.title.setText(titletxt)
        self.title.setObjectName('menutitle')
        self.layout_main.addWidget(self.title)
        wight.setLayout(self.layout_main)
        return wight


if __name__ == '__main__':
    app = QApplication(sys.argv)
    listWidget = LeftListWidget()
    listWidget.show()
    sys.exit(app.exec_())
