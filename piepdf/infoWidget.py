#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from PyQt5 import QtCore, QtGui, QtWidgets

# from PyQt5 import QtWebKitWidgets
# from PyQt5 import QtWebEngineWidgets
import os
import sqlite3

piepdf_PATH = (
    QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    + "/piepdf"
)
CONFIG_PATH = (
    QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    + "/piepdf/piepdf.conf"
)
DATABASE_PATH = (
    QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    + "/piepdf/piepdf_database"
)


class GrowingTextEdit(QtWidgets.QTextEdit):
    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.heightMin = 0
        self.heightMax = 65000
        self.setMinimumHeight(250)

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)

class ClickableQLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(object)
    def __init__(self, text = "", parent=None):
        QtWidgets.QLabel.__init__(self,text, parent)
    def mousePressEvent(self, ev):
        self.clicked.emit(ev)

class tagBottom(QtWidgets.QWidget):
    def __init__(self, text):
        super(QtWidgets.QWidget, self).__init__()
        self.layout  = QtWidgets.QHBoxLayout(self)
        self.b1 = QtWidgets.QPushButton(text)
        self.b2 = ClickableQLabel()
        self.layout.addWidget(self.b1)
        self.layout.addWidget(self.b2)
        pix = QtGui.QIcon.fromTheme("window-close")
        self.b2.setPixmap(pix.pixmap(QtCore.QSize(16, 16)))
        self.layout.setSpacing(0)
        self.setStyleSheet(
            "QPushButton {background-color : white; border: 5px solid white; border-top-left-radius: 10px; border-bottom-left-radius: 10px;}  QLabel {background-color : white;border: 5px solid white; border-top-right-radius: 10px; border-bottom-right-radius: 10px;}"
        )
        self.layout.addStretch(1)
 



class InfoWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.layout = QtWidgets.QGridLayout()
        self.database_path = os.path.join(DATABASE_PATH, "piepdf.db")

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def setData(self, metadata):
        # self.tableTitles = ['Path','Title','Author','Year','Text','Doi',        #'Url','Journal', 'Tags','Addition']
        self.clearLayout(self.layout)
        self.table = QtWidgets.QTableView()
        self.metadata = metadata

        newfont2 = QtGui.QFont()
        newfont2.setPointSize(14)
        self.title = GrowingTextEdit(self.metadata["Title"])
        # QtWidgets.QTextEdit(self.metadata['Title'])
        self.title.setFrameStyle(QtWidgets.QFrame.NoFrame)
        newfont = QtGui.QFont()
        newfont.setPointSize(18)

        newfont.setWeight(55)
        self.title.setFont(newfont)

        self.info_model = QtGui.QStandardItemModel()
        # self.info_model.setHorizontalHeaderLabels(['Titles'])
        self.info_model.setColumnCount(2)
        item_name = QtGui.QStandardItem("Authors")
        item_name.setTextAlignment(QtCore.Qt.AlignRight)
        item_name.setFont(newfont2)
        item_name.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        item_path = QtGui.QStandardItem(self.metadata["Author"])
        item_path.setTextAlignment(QtCore.Qt.AlignLeft)
        item_path.setFont(newfont2)
        self.info_model.appendRow([item_name, item_path])

        item_name = QtGui.QStandardItem("Abstract")
        item_name.setTextAlignment(QtCore.Qt.AlignRight)
        item_name.setFont(newfont2)
        item_name.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        item_path = QtGui.QStandardItem(self.metadata["Abstract"])
        item_path.setTextAlignment(QtCore.Qt.AlignLeft)
        self.info_model.dataChanged.connect(self.dataChangeSignal)
        self.info_model.appendRow([item_name, item_path])

        item_name = QtGui.QStandardItem("Doi")
        item_name.setTextAlignment(QtCore.Qt.AlignRight)
        item_name.setFont(newfont2)
        item_path = QtGui.QStandardItem(self.metadata["Doi"])
        item_path.setTextAlignment(QtCore.Qt.AlignLeft)
        item_path.setFont(newfont2)
        self.info_model.appendRow([item_name, item_path])

        item_name = QtGui.QStandardItem("")
        item_name.setTextAlignment(QtCore.Qt.AlignRight)
        item_name.setFont(newfont2)
        item_name.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        item_path = QtGui.QStandardItem("Open Url  ")
        item_path.setTextAlignment(QtCore.Qt.AlignLeft)
        item_path.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        item_path.setToolTip("Double click to open the link")
        self.info_model.appendRow([item_name, item_path])
        url = QtWidgets.QLabel("OPenUrl")

        item_name = QtGui.QStandardItem("Journal")
        item_name.setTextAlignment(QtCore.Qt.AlignRight)
        item_name.setFont(newfont2)
        item_path = QtGui.QStandardItem(self.metadata["Journal"])
        item_path.setTextAlignment(QtCore.Qt.AlignLeft)
        item_path.setFont(newfont2)
        self.info_model.appendRow([item_name, item_path])

        item_name = QtGui.QStandardItem("Year")
        item_name.setTextAlignment(QtCore.Qt.AlignRight)
        item_name.setFont(newfont2)
        item_path = QtGui.QStandardItem(self.metadata["Year"])
        item_path.setTextAlignment(QtCore.Qt.AlignLeft)
        item_path.setFont(newfont2)
        self.info_model.appendRow([item_name, item_path])
        # Tags 
        item_name = QtGui.QStandardItem("Tags")
        item_name.setTextAlignment(QtCore.Qt.AlignRight)
        item_name.setFont(newfont2)
        item_path = QtGui.QStandardItem(self.metadata["Tags"])
        item_path.setTextAlignment(QtCore.Qt.AlignLeft)
        item_path.setFont(newfont2)
        item_path.setToolTip("Tags are separated by ;")
        self.info_model.appendRow([item_name, item_path])

        item_name = QtGui.QStandardItem("Notes")
        item_name.setTextAlignment(QtCore.Qt.AlignRight)
        item_name.setFont(newfont2)
        item_path = QtGui.QStandardItem(self.metadata["Notes"])
        item_path.setTextAlignment(QtCore.Qt.AlignLeft)
        item_path.setFont(newfont2)
        item_path.setToolTip("Add note to the pdf ..")
        self.info_model.appendRow([item_name, item_path])
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.setModel(self.info_model)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch
        )
        self.table.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.table.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.layout.addWidget(self.title, 0, 0)
        self.layout.addWidget(self.table, 1, 0)
        # Tags
        ic = 0 
        for tags in  self.metadata["Tags"].split(";")[:-1]:
            ic =ic + 1
            self.layout.addWidget(tagBottom(str(tags)),2+ic, 0   )
        print("Total ic ", ic)
        #self.layout.addWidget(QtWidgets.QLineEdit("line edit"), 2, 0 )
        self.layout.setRowStretch(1, 1)
        # self.layout.setRowStretch(1, 10)
        self.layout.setVerticalSpacing(0)
        self.table.doubleClicked.connect(self.openUrl)
        self.setLayout(self.layout)

    def dataChangeSignal(self):
        print("Data Change !")
        index = self.table.selectedIndexes()[0]
        key = self.info_model.item(index.row(), 0).text()
        value = self.info_model.item(index.row(), 1).text()
        # if key == "Abstract":
        print((key, value))
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE pdffulltext SET {} = ? WHERE path = ? ".format(key),
                (value, self.metadata["Path"]),
            )

    def openUrl(self):
        index = self.table.selectedIndexes()[0]
        value = self.info_model.item(index.row(), 1).text()
        print(value[:3])
        if value[:4] == "Open":
            print(self.metadata["Url"])
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.metadata["Url"]))
        """
        if key == "Doi":
            value = self.info_model.item(index.row(),1).text()
            webdoi = self.metadata['Url']
            webView = QtWebEngineWidgets.QWebEngineView()
            print(webdoi )
            self.layout.addWidget(webView ,2,0)
            webView.load(QtCore.QUrl(webdoi))
        """
