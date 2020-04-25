from PyQt5.QtGui import QBitmap, QPainter, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication


class MyForm(QWidget):
    def __init__(self, parent=None):
        super(MyForm,self).__init__(parent)
        self.pix=QBitmap("res/mask.png")
        self.resize(self.pix.size())
        self.setMask(self.pix)


    def paintEvent(self, event):
        painter=QPainter(self)
        painter.drawPixmap(0,0,self.pix.width(),self.pix.height(), QPixmap("res/bg1.jpg"))


app=QApplication([])
form=MyForm()
form.show()
app.exec_()
