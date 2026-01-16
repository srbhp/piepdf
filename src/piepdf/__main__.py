#!/usr/bin/env python3

import os
import sys

from PyQt6 import QtCore, QtWidgets

from piepdf import adjustUI
from piepdf import layout as wlayout


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # Set Qt attributes BEFORE creating QApplication
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1.5"
    # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(argv)
    Mainwindow = wlayout.Ui_MainWindow()
    Mainwindow.setupUi()
    _ = adjustUI.Adjust_UI(Mainwindow)
    Mainwindow.show()
    app.aboutToQuit.connect(Mainwindow.saveSession)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
