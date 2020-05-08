import sys
import requests
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QImage, QPixmap, QDesktopServices
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QListWidget, QHBoxLayout, \
    QListWidgetItem, QApplication


class EnglishListWidget(QListWidget):

    def __init__(self, menulist):
        super(EnglishListWidget, self).__init__()

        self.setViewMode(QListWidget.ListMode)
        self.setObjectName('english')
        self.itemClicked.connect(self.clicked)

        for menu in menulist:
            item = QListWidgetItem()
            self.addItem(item)
            self.setItemWidget(item, self.get_Item_Widget(menu['img'], menu['url'], menu['title'], menu['time'], menu['author'], menu['description']))

    def clicked(self, item):
        url = self.itemWidget(item).toolTip()
        QDesktopServices.openUrl(QUrl(url))

    def get_Item_Widget(self, img, url, title, time, user, description):
        wight = QWidget()
        wight.setToolTip(url)
        self.layout_main = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.middleLine = QHBoxLayout()


        self.titlelabel = QLabel()
        self.titlelabel.setText(title)
        self.titlelabel.setObjectName('engtitle')
        self.titlelabel.setWordWrap(True)

        self.descriptionlabel = QLabel()
        self.descriptionlabel.setText(description)
        self.descriptionlabel.setObjectName('engdes')
        self.descriptionlabel.setWordWrap(True)

        self.timelabel = QLabel()
        self.timelabel.setText(time)
        self.timelabel.setObjectName('engmid')

        self.userlabel = QLabel()
        self.userlabel.setText(user)
        self.userlabel.setObjectName('engmid')

        res = requests.get(img)
        img = QImage.fromData(res.content)
        size = QSize(img.width()*0.5, img.height()*0.5)
        self.imgurl = QLabel()
        self.imgurl.resize(size)
        self.imgurl.setPixmap(QPixmap.fromImage(img.scaled(size)))

        self.right_layout.addWidget(self.titlelabel)
        self.right_layout.addLayout(self.middleLine)
        self.middleLine.addWidget(self.timelabel)
        self.middleLine.addWidget(self.userlabel)
        self.middleLine.addStretch(1)
        self.right_layout.addWidget(self.descriptionlabel)

        self.layout_main.addWidget(self.imgurl)
        self.layout_main.addLayout(self.right_layout)
        wight.setLayout(self.layout_main)
        return wight

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = EnglishListWidget()
    win.show()
    sys.exit(app.exec_())