#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets

import layout as wlayout
import adjustUI as adjustUI
import os
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Mainwindow = wlayout.Ui_MainWindow()
    Mainwindow.setupUi()
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1.5"
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons
    adfn = adjustUI.Adjust_UI(Mainwindow)
    # QtWidgets.QShortcut("Ctrl+Q", w, activated=w.close)
    Mainwindow.show()
    # spdfMainwindow.restoreSession()
    app.aboutToQuit.connect(Mainwindow.saveSession)
    sys.exit(app.exec_())
