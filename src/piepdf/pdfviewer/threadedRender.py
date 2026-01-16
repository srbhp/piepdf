from piepdf.pdfviewer.fixedARLabel import ImageWidget
from PyQt6 import QtCore, QtGui, QtWidgets


class WorkerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)


class GetAllPage(QtCore.QRunnable):
    def __init__(self, docpages, fake_dpi, keepAR=False):
        super(GetAllPage, self).__init__()
        self.signals = WorkerSignals()
        self.docpages = docpages
        self.fake_dpi = fake_dpi
        self.keepAR = keepAR
        self.layout = QtWidgets.QVBoxLayout()
        self.numpages = self.docpages.numPages()
        self.label = []
        self.keepAR = keepAR
        if self.keepAR:
            for i in range(self.numpages):
                self.label.append(ImageWidget())
        else:
            for i in range(self.numpages):
                self.label.append(QtWidgets.QLabel())

    def _get_page(self):
        for i in range(self.numpages):
            try:
                page = self.docpages.page(i)
                if page is None:
                    print(f"Warning: Page {i} is None")
                    continue
                image = page.renderToImage(self.fake_dpi, self.fake_dpi)
                if image.isNull():
                    print(f"Warning: Could not render page {i}")
                    continue
                pixmap = QtGui.QPixmap.fromImage(image)
                self.label[i].setPixmap(pixmap)
                if not self.keepAR:
                    self.label[i].setSizePolicy(
                        QtWidgets.QSizePolicy.Policy.Fixed,
                        QtWidgets.QSizePolicy.Policy.Expanding,
                    )
                    self.label[i].setScaledContents(True)

                self.layout.addWidget(self.label[i], 1)
            except Exception as e:
                print(f"Error rendering page {i}: {e}")
                continue

    def run(self):
        self._get_page()
        self.signals.finished.emit(self.layout)
