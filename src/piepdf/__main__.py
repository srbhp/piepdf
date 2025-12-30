#!/usr/bin/env python3

import os
import sys

import adjustUI as adjustUI
import layout as wlayout
from PyQt5 import QtCore, QtWidgets

if __name__ == "__main__":
    # Set Qt attributes BEFORE creating QApplication
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1.5"
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    Mainwindow = wlayout.Ui_MainWindow()
    Mainwindow.setupUi()
    adfn = adjustUI.Adjust_UI(Mainwindow)
    # QtWidgets.QShortcut("Ctrl+Q", w, activated=w.close)
    Mainwindow.show()
    # spdfMainwindow.restoreSession()
    app.aboutToQuit.connect(Mainwindow.saveSession)
    sys.exit(app.exec_())
