#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets

import piepdf.layout as wlayout
import piepdf.adjustUI as adjustUI

import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Mainwindow = wlayout.Ui_MainWindow()
    Mainwindow.setupUi()

    adfn = adjustUI.Adjust_UI(Mainwindow)
    #QtWidgets.QShortcut("Ctrl+Q", w, activated=w.close)
    Mainwindow.show()
    #spdfMainwindow.restoreSession()
    #print((w.height(),w.width() ))
    #app.aboutToQuit.connect(lambda: spdfMainwindow.saveSession(w))
    sys.exit(app.exec_())
