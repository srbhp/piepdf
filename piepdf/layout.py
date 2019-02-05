# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from piepdf import infoWidget
import os 

class Ui_MainWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def  __init__(self):
        super(Ui_MainWindow, self).__init__()
    def setupUi(self):
        self.setObjectName("MainWindow")
        #sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        #self.resize(int(sizeObject.height()*0.8),int(sizeObject.width()*0.5))
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralWidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.splitter.setStyleSheet("QSplitter::handle { image: none; }")

        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)

        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")
        self.bookmarkTab = QtWidgets.QWidget()
        self.bookmarkTab.setObjectName("Main Projects")
        self.verticalLayout_3 = QtWidgets.QGridLayout( self.bookmarkTab)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.treeView = QtWidgets.QTreeView()
        self.treeView_2 = QtWidgets.QTreeView()
        #self.treeView.setEnabled(False)
        self.listView = QtWidgets.QTableView()
        self.listView.setSortingEnabled(True)
        #self.listView = QtWidgets.QListView()
        self.graphicsView = infoWidget.InfoWindow()
        #self.listView.setEnabled(False)
        self.splitter1 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitter1.addWidget(self.treeView)
        self.splitter1.addWidget(self.treeView_2)
        self.splitter2 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.listView)
        self.splitter2.addWidget(self.graphicsView)

        self.splitter2.setStyleSheet("QSplitter::handle { image: none; }")
        self.splitter1.setStyleSheet("QSplitter::handle { image: none; }")
        self.verticalLayout_3.addWidget(self.splitter2)

        """
        self.verticalLayout_3.addWidget(self.treeView,0,0)
        self.verticalLayout_3.addWidget(self.treeView_2,1,0)

        self.verticalLayout_3.addWidget(self.listView,0,1,2,1)
        self.verticalLayout_3.addWidget(self.graphicsView,0,2,2,1)
        """
        self.tabWidget.addTab(self.bookmarkTab, "Main Window ")
        self.tabWidget.tabBar().setTabButton(0,QtWidgets.QTabBar.RightSide,None)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        self.verticalLayout_2.addWidget(self.splitter)
        self.verticalLayout.addWidget(self.widget)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        #self.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(self)
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setFloatable(False)
        self.mainToolBar.setObjectName("mainToolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.actionHome = QtWidgets.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("piepdf/icons/home.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon)
        self.actionHome.setObjectName("actionHome")
        self.actionQuit = QtWidgets.QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(self)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.search_list = QtCore.QStringListModel()
        self.search_list.setStringList(['some', 'words', 'in', 'my', 'dictionary'])
        completer = QtWidgets.QCompleter()
        completer.setModel(self.search_list)
        self.setWindowIcon(QtGui.QIcon('piepdf/icons/mainicon.svg'))

        self.menuFile.addAction(self.actionHome)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuView.addSeparator()
        #self.menuBar.addAction(self.menuFile.menuAction())
        #self.menuBar.addAction(self.menuView.menuAction())
        #self.menuBar.addAction(self.menuHelp.menuAction())
        self.mainToolBar.addAction(self.actionHome)
        self.mainToolBar.addSeparator()

        self.retranslateUi(self)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "PDF Viewer"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionHome.setText(_translate("MainWindow", "Home"))
        self.actionHome.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))


    def saveSession(self,MainWindow):
        settings =QtCore.QSettings("piepdf", "piepdf")
        settings.beginGroup('mainWindow')
        settings.setValue("splitter1Settings",self.splitter1.saveState())
        settings.setValue("splitter2Settings",self.splitter2.saveState())
        settings.setValue("geometry",self.saveGeometry())
        settings.setValue("windowState",self.saveState())
        settings.endGroup()
        #self.settings.sync()

    def restoreSession(self):
        settings =QtCore.QSettings("piepdf", "piepdf")
        settings.beginGroup('mainWindow')
        try :
            self.splitter1.restoreState(settings.value("splitter1Settings"))
        except :
            print("Unable to set Qsplitter Setting !")
        try :
            self.splitter2.restoreState(settings.value("splitter2Settings"))
        except :
            print("Unable to set Qsplitter Setting !")
        try:
            self.restoreGeometry(settings.value("geometry"))
        except :
            print("Unable to set MainWindow Setting !")
        try:
            self.restoreState(settings.value("windowState"))
        except :
            print("Unable to set MainWindow Setting !")
        settings.endGroup()
           
        #settings = QtCore.QSettings("piepdf", "piepdf")
        settings.beginGroup('Settings')
        try : 
            self.PiePdf_Path = settings.value("PiePdf_Path")
        except :
            self.PiePdf_Path = os.path.expanduser("~/PiePdf")
        if self.PiePdf_Path is None  or " ":
            self.PiePdf_Path = os.path.expanduser("~/PiePdf")
        try :
            self.usePdfViewer = int(settings.value("PdfViewerState")) is 2
        except : 
            self.usePdfViewer = True 
        try :
            self.WatchFolder = int(settings.value("WatchFolderState")) is 2 
        except :
            self.WatchFolder = True
        try :
            self.emailaddress  = settings.value("EmailAddress") 
        except : 
            self.emailaddress =  ""
        settings.beginGroup('Settings')
    def restoreSetting(self) :
        settings = QtCore.QSettings("piepdf", "piepdf")
        settings.beginGroup('Settings')
        try : 
            self.PiePdf_Path = settings.value("PiePdf_Path")      
        except :
            self.PiePdf_Path = os.path.expanduser("~/PiePdf")
        if self.PiePdf_Path is None or " " :
            self.PiePdf_Path = os.path.expanduser("~/PiePdf")
        try :
            self.usePdfViewer = int(settings.value("PdfViewerState")) is 2
        except : 
            self.usePdfViewer = True 
        try :
            self.WatchFolder = int(settings.value("WatchFolderState")) is 2 
        except :
            self.WatchFolder = True
        try :
            self.emailaddress  = settings.value("EmailAddress") 
        except : 
            self.emailaddress =  ""
        settings.beginGroup('Settings')


