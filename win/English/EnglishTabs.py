import sys
from traceback import format_exc

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect, QApplication, \
    QComboBox, QTabBar

import CommomHelper
from thread.English.MagazineThread import FetchMagazineListThread
from win.English.EnglishItemList import EnglishListWidget


class EnglishTabs(QTabWidget):
    def __init__(self,parent=None):
        super(EnglishTabs, self).__init__(parent)

        self.setMovable(True)
        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideMiddle)
        self.setUsesScrollButtons(True)
        self.tabCloseRequested.connect(self.closetab)

        #self.currentChanged.connect(self.tabchange)

    def closetab(self, index):
        tab = self.widget(index)
        tab.deleteLater()
        self.removeTab(index)


    # def tabchange(self, index):
    #     print(index)

class EnglishTab(QWidget):
    def __init__(self,parent=None):
        super(EnglishTab, self).__init__(parent)

        #最上方
        label = QLabel('英语资料分享')
        label.setObjectName('tablabel')
        label.setFont(QFont('黑体', 20))
        self.comboMenu = QComboBox(minimumWidth=200)
        top_layout = QHBoxLayout()
        top_layout.addWidget(label)
        top_layout.addStretch(1)
        top_layout.addWidget(self.comboMenu)
        subTitle = QLabel('田间小站 - 英语学习及资源分享，官网请访问'
                          '<a href="https://www.tianfateng.cn/">https://www.tianfateng.cn/</a>')
        subTitle.setOpenExternalLinks(True)
        subTitle.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        subTitle.setObjectName('tabsublabel')
        subTitle.setFont(QFont('黑体', 12))
        self.init_comboboxMenu()
        self.comboMenu.activated.connect(self.on_comboboxMenu_Activate)

        #中间部分
        self.tab = EnglishTabs()

        #status状态栏
        self.statusBar = QHBoxLayout()
        self.statusBar.setObjectName('statusbar')
        self.statusInfo = QLabel('jsadsadhsahh')
        self.statusBar.addWidget(self.statusInfo)
        self.statusInfo.setStyleSheet('font-family:微软雅黑;color: grey;')

        vbox = QVBoxLayout()
        vbox.addLayout(top_layout)
        vbox.addWidget(subTitle)
        vbox.addWidget(self.tab)
        vbox.addLayout(self.statusBar)
        self.setLayout(vbox)

    def init_comboboxMenu(self):
        menu_data = CommomHelper.CommonHelper.load_english_source('../config/english_source.cm')
        for menu in menu_data['source']:
            self.comboMenu.addItem(menu)
        self.comboMenu.setCurrentIndex(-1)

    def on_comboboxMenu_Activate(self, index):
        try:
            if index==0:
                url = 'https://www.tianfateng.cn/tag/economist-official-translation-digest/page'
            elif index==1:
                url = 'https://www.tianfateng.cn/tag/nytimes/page'
            tabName = self.comboMenu.currentText()
            tabindex = self.tab.addTab(self.get_TabWidget(), tabName)
            self.tab.setTabToolTip(tabindex, '<h3>{}</h3>'.format(tabName))
            self.tab.setCurrentIndex(tabindex)
            self.thread = FetchMagazineListThread(url=url,
                                                  page='1',
                                                  tabindex = str(tabindex),
                                                  tabname = tabName)
            self.thread.magazinelist.connect(self.magalist_callback)
            self.thread.start()
        except Exception as e:
            print(e)

    def magalist_callback(self, id, tabname, json):
        try:
            # print(id, json)
            wget = QWidget()
            vbox = QVBoxLayout()
            vbox.addWidget(EnglishListWidget(menulist=json))
            wget.setLayout(vbox)
            self.tab.removeTab(int(id))
            self.tab.insertTab(int(id), wget, tabname)
            self.tab.setCurrentIndex(int(id))
        except Exception:
            e = str(format_exc())
            print(e)

    def get_TabWidget(self):
        wget = QWidget()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addStretch(1)
        waitlabel = QLabel('正在加载中,请稍等')
        waitlabel.setFont(QFont('黑体', 15))
        hbox.addWidget(waitlabel)
        hbox.addStretch(1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        wget.setLayout(vbox)
        return wget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = EnglishTab()
    win.show()
    sys.exit(app.exec_())