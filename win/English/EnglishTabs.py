import sys
from traceback import format_exc

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QApplication, \
    QComboBox

from win import CommomHelper
from service.English.Magazines import Magazine
from thread.English.MagazineThread import FetchPreMagazineListThread, FetchNextMagazineListThread, \
    FetchFirstMagazineListThread, FetchLastMagazineListThread, FetchCustomizedMagazineListThread
from win.English.PaginationWidget import Pagination
from win.English.EnglishItemList import EnglishListWidget

class SourceComboBox(QComboBox):
    def __init__(self):
        super(SourceComboBox, self).__init__()

        self.menu_data = CommomHelper.CommonHelper.load_english_source('../../config/english_source.cm')
        for menu in self.menu_data['source']:
            self.insertItem(int(menu['id']), menu['title'], menu['url'])
        self.setCurrentIndex(-1)

        self.setMinimumWidth(200)

class EnglishTabs(QTabWidget):
    def __init__(self,parent=None):
        super(EnglishTabs, self).__init__(parent)

        self.setMovable(True)
        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideMiddle)
        self.setUsesScrollButtons(True)
        self.tabCloseRequested.connect(self.closetab)
        self.setContentsMargins(0,0,0,0)

    def closetab(self, index):
        tab = self.widget(index)
        tab.deleteLater()
        self.removeTab(index)

class EnglishTab(QWidget):
    def __init__(self,parent=None):
        super(EnglishTab, self).__init__(parent)

        #最上方
        label = QLabel('英语资料分享')
        label.setObjectName('tablabel')
        label.setFont(QFont('黑体', 20))
        self.comboMenu = SourceComboBox()
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
        self.comboMenu.activated.connect(self.Menu_Activate)

        #中间部分
        self.tab = EnglishTabs()

        vbox = QVBoxLayout()
        vbox.addLayout(top_layout)
        vbox.addWidget(subTitle)
        vbox.addWidget(self.tab)
        self.setLayout(vbox)

    def Menu_Activate(self, index):
        try:
            for menu in self.comboMenu.menu_data['source']:
                if int(menu['id']) == index:
                    url = menu['url']
                else:
                    continue
            self.generatetab(url)
            self.first_btn_thread()
        except Exception:
            e = str(format_exc())
            print(e)

    def magalist_callback(self, id, tabname, json, current_page, total_page):
        try:
            wget = QWidget()
            vbox = QVBoxLayout()
            vbox.addWidget(EnglishListWidget(menulist=json))
            self.pageWidget = Pagination(total_page=total_page, current_page=current_page)
            self.pageWidget.nextbtn.clicked.connect(self.next_btn_clicked)
            self.pageWidget.prebtn.clicked.connect(self.pre_btn_clicked)
            self.pageWidget.firstbtn.clicked.connect(self.first_btn_clicked)
            self.pageWidget.lastbtn.clicked.connect(self.last_btn_clicked)
            self.pageWidget.inputEdit.returnPressed.connect(self.turn_to_page)
            vbox.addWidget(self.pageWidget)
            wget.setLayout(vbox)
            self.tab.removeTab(id)
            self.tab.insertTab(id, wget, tabname)
            self.tab.setCurrentIndex(id)
        except Exception:
            e = str(format_exc())
            print(e)

    def first_btn_clicked(self):
        self.modifytab()
        self.first_btn_thread()

    def first_btn_thread(self):
        try:
            self.thread = FetchFirstMagazineListThread(magazine=self.magazine,
                                                       tabindex = self.tab.currentIndex(),
                                                       tabname = self.comboMenu.currentText())
            self.thread.magazinelist.connect(self.magalist_callback)
            self.thread.start()
        except Exception:
            e = str(format_exc())
            print(e)

    def next_btn_clicked(self):
        if self.magazine.current_page != self.magazine.total_page:
            self.modifytab()
            try:
                self.next_page_thread = FetchNextMagazineListThread(magazine=self.magazine,
                                                                    tabindex = self.tab.currentIndex(),
                                                                    tabname = self.comboMenu.currentText())
                self.next_page_thread.magazinelist.connect(self.magalist_callback)
                self.next_page_thread.start()
            except Exception:
                e = str(format_exc())
                print(e)

    def pre_btn_clicked(self):
        if self.magazine.current_page != 1:
            self.modifytab()
            try:
                self.pre_page_thread = FetchPreMagazineListThread(magazine=self.magazine,
                                                                  tabindex = self.tab.currentIndex(),
                                                                  tabname = self.comboMenu.currentText())
                self.pre_page_thread.magazinelist.connect(self.magalist_callback)
                self.pre_page_thread.start()
            except Exception:
                e = str(format_exc())
                print(e)

    def last_btn_clicked(self):
        self.modifytab()
        try:
            self.last_page_thread = FetchLastMagazineListThread(magazine=self.magazine,
                                                              tabindex = self.tab.currentIndex(),
                                                              tabname = self.comboMenu.currentText())
            self.last_page_thread.magazinelist.connect(self.magalist_callback)
            self.last_page_thread.start()
        except Exception:
            e = str(format_exc())
            print(e)

    def turn_to_page(self):
        pageNum = int(self.pageWidget.inputEdit.text())
        if pageNum != '':
            self.modifytab()
            try:
                self.customized_page_thread = FetchCustomizedMagazineListThread(magazine=self.magazine,
                                                                    tabindex = self.tab.currentIndex(),
                                                                    tabname = self.comboMenu.currentText(),
                                                                                index=pageNum)
                self.customized_page_thread.magazinelist.connect(self.magalist_callback)
                self.customized_page_thread.start()
            except Exception:
                e = str(format_exc())
                print(e)

    def placeholder(self):
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

    def modifytab(self):
        tabName = self.comboMenu.currentText()
        tabindex = self.tab.currentIndex()
        self.tab.removeTab(tabindex)
        self.tab.insertTab(tabindex, self.placeholder(), tabName)
        self.tab.setTabToolTip(tabindex, '<h3>{}</h3>'.format(tabName))
        self.tab.setCurrentIndex(tabindex)

    def generatetab(self, url):
        tabName = self.comboMenu.currentText()
        tabindex = self.tab.addTab(self.placeholder(), tabName)
        self.tab.setTabToolTip(tabindex, '<h3>{}</h3>'.format(tabName))
        self.tab.setCurrentIndex(tabindex)
        self.magazine = Magazine(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = EnglishTab()
    win.show()
    sys.exit(app.exec_())