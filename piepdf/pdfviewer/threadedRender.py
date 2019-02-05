from PyQt5 import QtCore, QtGui, QtWidgets
from piepdf.pdfviewer.fixedARLabel import  ImageWidget

class WorkerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)

class GetAllPage(QtCore.QRunnable):
    def __init__(self, docpages,fake_dpi,keepAR=False):
        super(GetAllPage, self).__init__()
        self.signals = WorkerSignals()
        self.docpages = docpages
        self.fake_dpi = fake_dpi
        self.keepAR=keepAR
        self.layout = QtWidgets.QVBoxLayout()
        self.numpages= self.docpages.numPages()
        self.label= []
        self.keepAR=keepAR
        if (self.keepAR):
            for i in range(self.numpages ):
                self.label.append( ImageWidget() )
        else :
            for i in range(self.numpages ):
                self.label.append( QtWidgets.QLabel() )
    def _get_page(self ):
        for i in range(self.numpages ):
            page = self.docpages.page(i)
            image = page.renderToImage(self.fake_dpi,self.fake_dpi)
            pixmap=QtGui.QPixmap.fromImage(image)
            self.label[i].setPixmap(pixmap)
            if not self.keepAR:
                self.label[i].setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding )
                self.label[i].setScaledContents(True)

            self.layout.addWidget(self.label[i],1)
    def run(self):
        self._get_page()
        self.signals.finished.emit(self.layout)
