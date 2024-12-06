from PyQt5 import QtCore, QtGui, QtWidgets

class ThumbWidget(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.clicked.emit(event.pos())

class ImageWidget(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)
    def hasHeightForWidth(self):
        return self.pixmap() is not None
    def minimumSizeHint(self):
        s = self.size()
        s.scale(QtCore.QSize(10, 10), QtCore.Qt.KeepAspectRatio)
        return s
    def heightForWidth(self, w):
        if self.pixmap():
            return int(w * (self.pixmap().height() / self.pixmap().width()))
