from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect


class ObjectDetectionTabs(QTabWidget):
    def __init__(self,parent=None):
        super(ObjectDetectionTabs, self).__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")
        self.addTab(self.tab4, "Tab 4")
        self.addTab(self.tab5, "Tab 5")
        self.addTab(self.tab6, "Tab 6")

        self.setCurrentIndex(0)

        optitle = QGraphicsOpacityEffect()
        optitle.setOpacity(0.7)
        self.setGraphicsEffect(optitle)
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tab5UI()
        self.tab6UI()

    def tab1UI(self):
        vbox = QVBoxLayout()
        placehoder = QLabel('YOLOv3 Tab Demo')
        font = QFont('Century Gothic', 20)
        placehoder.setFont(font)
        vbox.addWidget(placehoder)
        self.setTabText(0, 'YOLOv3')
        self.tab1.setLayout(vbox)

    def tab2UI(self):
        vbox = QVBoxLayout()
        placehoder = QLabel('YOLO9000 Tab Demo')
        font = QFont('Century Gothic', 20)
        placehoder.setFont(font)
        vbox.addWidget(placehoder)
        self.setTabText(1, 'YOLO9000')
        self.tab2.setLayout(vbox)

    def tab3UI(self):
        vbox = QVBoxLayout()
        placehoder = QLabel('YOLO Tab Demo')
        font = QFont('Century Gothic', 20)
        placehoder.setFont(font)
        vbox.addWidget(placehoder)
        self.setTabText(2, 'YOLO')
        self.tab3.setLayout(vbox)

    def tab4UI(self):
        vbox = QVBoxLayout()
        placehoder = QLabel('SSD Tab Demo')
        font = QFont('Century Gothic', 20)
        placehoder.setFont(font)
        vbox.addWidget(placehoder)
        self.setTabText(3, 'SSD')
        self.tab4.setLayout(vbox)

    def tab5UI(self):
        vbox = QVBoxLayout()
        placehoder = QLabel('Faster R-CNN Tab Demo')
        font = QFont('Century Gothic', 20)
        placehoder.setFont(font)
        vbox.addWidget(placehoder)
        self.setTabText(4, 'Faster R-CNN')
        self.tab5.setLayout(vbox)

    def tab6UI(self):
        vbox = QVBoxLayout()
        placehoder = QLabel('CenterNet Tab Demo')
        font = QFont('Century Gothic', 20)
        placehoder.setFont(font)
        vbox.addWidget(placehoder)
        self.setTabText(5, 'CenterNet')
        self.tab6.setLayout(vbox)


class ObjectDetectionTab(QWidget):
    def __init__(self,parent=None):
        super(ObjectDetectionTab, self).__init__(parent)

        #最上方
        label = QLabel('目标检测算法合集')
        label.setObjectName('tablabel')
        label.setFont(QFont('黑体', 20))
        subTitle = QLabel('这里展示集中目标检测算法的算法案例，仅供参考。')
        subTitle.setObjectName('tabsublabel')
        subTitle.setFont(QFont('黑体', 12))

        #中间部分
        self.tab = ObjectDetectionTabs()

        #status状态栏
        self.statusBar = QHBoxLayout()
        self.statusBar.setObjectName('statusbar')
        self.statusInfo = QLabel()
        self.statusBar.addWidget(self.statusInfo)
        self.statusInfo.setStyleSheet('font-family:微软雅黑;color: grey;')

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(subTitle)
        vbox.addWidget(self.tab)
        vbox.addLayout(self.statusBar)
        self.setLayout(vbox)
