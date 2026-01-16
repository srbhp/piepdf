from PyQt6 import QtCore, QtWidgets
import os


class Ui_SettingWindow(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self):
        super(Ui_SettingWindow, self).__init__()

    def setupUi(self):
        self.setObjectName("SettingWindow")
        self.resize(568, 109)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidgets = QtWidgets.QTabWidget()
        self.tabWidgets.setTabBarAutoHide(True)

        self.generalTab = QtWidgets.QWidget()
        self.tabWidgets.addTab(self.generalTab, "General Tab")
        self.setGeneralTab()

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.addWidget(self.tabWidgets)

        self.buttonwidget = QtWidgets.QWidget()
        self.buttonlayout = QtWidgets.QHBoxLayout(self.buttonwidget)
        self.okbutton = QtWidgets.QPushButton("OK")
        self.cancelbutton = QtWidgets.QPushButton("Cancel")
        self.buttonlayout.addStretch(1)
        self.buttonlayout.addWidget(self.okbutton)
        self.buttonlayout.addWidget(self.cancelbutton)
        self.okbutton.clicked.connect(self.saveSetting)
        self.cancelbutton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.buttonwidget)
        self.setCentralWidget(self.centralwidget)

        self.readSetting()

    def setGeneralTab(self):
        self.gLayout = QtWidgets.QVBoxLayout(self.generalTab)
        self.generalTab.setLayout(self.gLayout)

        self.pathWidget = QtWidgets.QWidget()
        self.layout1 = QtWidgets.QHBoxLayout(self.pathWidget)
        self.mainpdfPath = QtWidgets.QLabel(os.path.expanduser("~/PiePdf"))
        self.layout1.addWidget(self.mainpdfPath)
        self.setPath = QtWidgets.QPushButton("Set Path")
        self.layout1.addStretch(1)
        self.layout1.addWidget(self.setPath)
        self.setPath.clicked.connect(self.setMainPath)

        self.gLayout.addWidget(self.pathWidget)

        self.pdfView = QtWidgets.QCheckBox("Use inbuilt PdfViewer")
        self.pdfView.setCheckable(True)
        self.gLayout.addWidget(self.pdfView)

        self.watchFolder = QtWidgets.QCheckBox(
            "Watch folder to add pdf files automatically"
        )
        self.gLayout.addWidget(self.watchFolder)

        self.emailwidget = QtWidgets.QLineEdit()
        self.emailwidget.setMaximumWidth(300)
        self.emailwidget.setPlaceholderText("Email Address for crossref api")
        self.gLayout.addWidget(self.emailwidget)

    def setMainPath(self):
        path = str(QtWidgets.QFileDialog.getExistingDirectory())
        # "Select Directory"))
        print(path)
        if path is not None:
            self.mainpdfPath.setText(path)

    def saveSetting(self):
        settings = QtCore.QSettings("piepdf", "piepdf")
        settings.beginGroup("Settings")
        settings.setValue("PiePdf_Path", self.mainpdfPath.text())
        settings.setValue("PdfViewerState", self.pdfView.checkState())
        settings.setValue("WatchFolderState", self.watchFolder.checkState())
        settings.setValue("EmailAddress", self.emailwidget.text())
        settings.endGroup()
        self.close()

    def readSetting(self):
        settings = QtCore.QSettings("piepdf", "piepdf")
        # self.pdfView.setCheckState(2)
        settings.beginGroup("Settings")
        try:
            self.mainpdfPath.setText(settings.value("PiePdf_Path"))
            self.pdfView.setCheckState(int(settings.value("PdfViewerState")))
            self.watchFolder.setCheckState(int(settings.value("WatchFolderState")))
            self.emailwidget.setText(settings.value("EmailAddress"))
        except Exception as e:
            print(f"Failed at reading setting {e}")
        print(settings.value("PiePdf_Path"))
        if settings.value("PiePdf_Path") is None:
            self.mainpdfPath.setText(os.path.expanduser("~/PiePdf"))
        settings.endGroup()

    def closeEvent(self, event):
        print("Closed")
        self.closed.emit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = Ui_SettingWindow()
    ui.setupUi()
    w.show()
    sys.exit(app.exec_())
