#!/usr/bin/env python3
"""Tags for the paper"""
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMenuBar,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)

from PyQt5.QtGui import QIcon
import sys

import flowlayout


class ClickableQLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(object)

    def __init__(self, text="", parent=None):
        QtWidgets.QLabel.__init__(self, text, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit(ev)


class tagBottom(QWidget):
    def __init__(self, text):
        super(QWidget, self).__init__()
        self.layout = QHBoxLayout(self)
        b1 = QPushButton(text)
        b2 = ClickableQLabel()
        b2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        pix = QtGui.QIcon.fromTheme("window-close")
        b2.setPixmap(pix.pixmap(QtCore.QSize(24, 24)))
        b2.clicked.connect(self.printHello)
        self.layout.setSpacing(0)
        self.setStyleSheet(
            "QPushButton {background-color : white; border: 5px solid white; border-top-left-radius: 10px; border-bottom-left-radius: 10px;}  QLabel {background-color : white;border: 5px solid white; border-top-right-radius: 10px; border-bottom-right-radius: 10px;}"
        )

    def printHello(self, e):
        print("Hello")


class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()
        mainLayout = flowlayout.FlowLayout()  # QHBoxLayout()
        lineedit = QLineEdit()
        mainLayout.addWidget(tagBottom("One lskjlj"))
        mainLayout.addWidget(tagBottom("Two lskjlj"))
        mainLayout.addWidget(tagBottom("Two lskgfdskjjjjlj"))
        mainLayout.addWidget(tagBottom("Twokkkkkkkkkkkkkkkkk lskjlj"))
        mainLayout.addWidget(lineedit)
        self.setLayout(mainLayout)
        self.setWindowTitle("Form Layout - pythonspot.com")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
