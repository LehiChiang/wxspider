# from PyQt5.QtWidgets import QApplication, QProgressBar, QPushButton
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import Qt, QBasicTimer
#
# class ProgressBar(QtWidgets.QWidget):
#     def __init__(self, parent= None):
#         QtWidgets.QWidget.__init__(self)
#
#         self.setGeometry(300, 300, 250, 150)
#         self.setWindowTitle('ProgressBar')
#         self.pbar = QProgressBar(self)
#         self.pbar.setGeometry(30, 40, 200, 25)
#
#         self.button = QPushButton('Start', self)
#         self.button.setFocusPolicy(Qt.NoFocus)
#         self.button.move(40, 80)
#
#         self.button.clicked.connect(self.onStart)
#         self.timer = QBasicTimer()
#         self.step = 0
#
#     def timerEvent(self, event):
#         if self.step >=100:
#             self.timer.stop()
#             return
#         self.step = self.step + 1
#         self.pbar.setValue(self.step)
#
#     def onStart(self):
#         if self.timer.isActive():
#             self.timer.stop()
#             self.button.setText('Start')
#         else:
#             self.timer.start(100, self)
#             self.button.setText('Stop')
#
#
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     qb = ProgressBar()
#     qb.show()
#     sys.exit(app.exec_())
#
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication


class Emiterer(QtCore.QThread):
    f = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(Emiterer, self).__init__()

        self.message = {'time':'90s', 'state':'ok', 'error':'no error!'}

    def run(self):
        #self.f.emit({"2": 'hello'})
        self.f.emit(self.message)


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.e = Emiterer()
        self.e.f.connect(self.finised)
        self.e.start()

    def finised(self, r_dict):
        print(r_dict['time'])


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())
