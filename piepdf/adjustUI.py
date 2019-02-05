#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from piepdf.pdfviewer import pdfviewer
from piepdf import infoWidget, settings
from PyQt5 import QtCore, QtGui, QtWidgets
import piepdf.database.sql as sqldb
import time 
import os 

class ClickableQLabel(QtWidgets.QLabel):
    clicked=QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
    def mousePressEvent(self, ev):
        self.clicked.emit(ev)

class MyFileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self):
        super().__init__()
        self.headerfirstcolumn="Main Projects"
    def headerData(self,section, orientation,  role):
        if section == 0 and  role == QtCore.Qt.DisplayRole :
            return self.headerfirstcolumn
        else :
            return QtWidgets.QFileSystemModel.headerData(self,section,orientation,role)

class Adjust_UI(object):
    def __init__(self,parent_ui):
        self.parent_ui = parent_ui
        self.parent_ui.restoreSession()
        self.piepdf_path  = self.parent_ui.PiePdf_Path 
        os.makedirs(self.piepdf_path, exist_ok=True)
        print(self.piepdf_path )

        self.parent_ui.listView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.parent_ui.listView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.parent_ui.listView.horizontalHeader().setStretchLastSection(True)
        self.parent_ui.listView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.parent_ui.tabWidget.tabBar().setTabButton(0,QtWidgets.QTabBar.RightSide,None )
        self.parent_ui.tabWidget.tabBar().setTabButton(0,QtWidgets.QTabBar.LeftSide,None )
        self.model_3 = QtGui.QStandardItemModel()

        self.tableTitles = ['Path','Title','Author','Year','Abstract','Doi',
        'Url','Journal', 'Tags','Notes']
        self.ncols = len(self.tableTitles)
        self.parent_ui.actionHome.triggered.connect(self.updateWidgets)
        self.addSearchBox()
        self.addSettings()       
        self.decorateMain()
        """
        if self.piepdf_path is "" or None or "None" :
            self.openSettingWindow() 
            self.parent_ui.restoreSetting()
            self.piepdf_path  = self.parent_ui.PiePdf_Path 

            self.settings_ui.closed.connect(self.decorateMain)
         """ 
    def decorateMain(self):
            self.threadpool = QtCore.QThreadPool()
            print(self.parent_ui.PiePdf_Path)
            print(self.piepdf_path)
            self.piepdf_db = sqldb.DatabaseInit(self.piepdf_path,email = self.parent_ui.emailaddress)
            self.threadpool.start( self.piepdf_db )
            self.piepdf_db.signals.status.connect(self.dbStatus)
            self.piepdf_db.signals.finished.connect(self.dbFinish)
    def addSettings(self):
        self.actionSetting = QtWidgets.QAction()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("piepdf/icons/settings.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSetting.setIcon(icon)
        self.actionSetting.setObjectName("actionSettings")
        self.actionSetting.triggered.connect(self.openSettingWindow)
        self.parent_ui.mainToolBar.addAction(self.actionSetting)
    def openSettingWindow(self ):
        print("Opening Setting Window")   
        self.settings_ui = settings.Ui_SettingWindow()
        self.settings_ui.setupUi()
        #self.parent_ui.setEnabled(False)
        self.settings_ui.show() 

    def dbStatus(self,obj):
        print(obj)
        #QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)        
        #QtWidgets.QApplication.restoreOverrideCursor()
        self.parent_ui.statusBar.showMessage(obj)
    def dbFinish(self,obj):
        #QtWidgets.QApplication.processEvents()
        print(obj)
        self.parent_ui.statusBar.showMessage(obj)
        #Update main window after database work  finished
        self.updateWidgets( )
        self.addsignals( )

    def filesignal(self):
        index=self.parent_ui.listView.selectedIndexes()[0]
        fullpath = self.model_3.item(index.row(),0).text()
        name = self.model_3.item(index.row(),1).text()
        view=pdfviewer.Pdf_Widget(fullpath)
        self.parent_ui.tabWidget.addTab(view, name)

    def search_signal(self):
        stext = self.searchBox.text()
        scol=[]
        for i in self.searchColumns :
            if self.searchColumns['All'] and i != 'All' :
                scol.append(i)
            if not self.searchColumns['All'] and i != 'All' and self.searchColumns[i] :
                scol.append(i)
        info = self.piepdf_db.searchDb(stext, scol )
        self.model_3.clear()
        self.model_3.setColumnCount(self.ncols)
        #Path, Title, Author, Year, Text, Doi, Url, Journal, Tags, Addition
        self.model_3.setHorizontalHeaderLabels(self.tableTitles)
        for i in range(len(info)):
            items = []
            for j in range(self.ncols):
                item_title = QtGui.QStandardItem(info[i][j])
                items.append(item_title)
            self.model_3.appendRow(items)
        self.parent_ui.listView.verticalHeader().hide()
        self.parent_ui.listView.setModel(self.model_3)
        self.parent_ui.listView.hideColumn(0)
        self.parent_ui.listView.hideColumn(4)
        self.parent_ui.listView.hideColumn(5)
        self.parent_ui.listView.hideColumn(6)
        self.parent_ui.listView.hideColumn(7)
        self.parent_ui.listView.hideColumn(8)
        self.parent_ui.listView.hideColumn(9)
        self.parent_ui.listView.setColumnWidth(1,self.parent_ui.listView.width()*0.6)
        self.parent_ui.listView.setColumnWidth(3,self.parent_ui.listView.width()*0.1)

    def update_listview(self,subrootpath):
        info = self.piepdf_db.getFileList(subrootpath )
        self.model_3.clear()
        self.model_3.setColumnCount(self.ncols)
        #Path, Title, Author, Year, Text, Doi, Url, Journal, Tags, Addition
        self.model_3.setHorizontalHeaderLabels(self.tableTitles)
        for i in range(len(info)):
            items = []
            for j in range(self.ncols):
                item_title = QtGui.QStandardItem(info[i][j])
                items.append(item_title)
            self.model_3.appendRow(items)
        self.parent_ui.listView.verticalHeader().hide()
        self.parent_ui.listView.setModel(self.model_3)
        self.parent_ui.listView.hideColumn(0)
        self.parent_ui.listView.hideColumn(4)
        self.parent_ui.listView.hideColumn(5)
        self.parent_ui.listView.hideColumn(6)
        self.parent_ui.listView.hideColumn(7)
        self.parent_ui.listView.hideColumn(8)
        self.parent_ui.listView.hideColumn(9)
        self.parent_ui.listView.setColumnWidth(1,self.parent_ui.listView.width()*0.6)
        self.parent_ui.listView.setColumnWidth(3,self.parent_ui.listView.width()*0.1)
    def addSearchBox(self):
        self.searchWidget = QtWidgets.QWidget()
        self.searchlayout=QtWidgets.QHBoxLayout(self.searchWidget)
        self.searchBox = QtWidgets.QLineEdit()
        self.searchIcon = ClickableQLabel()
        self.searchBox.setFrame(QtWidgets.QFrame.NoFrame)
        self.searchBox.setPlaceholderText("Search ")
        self.searchBox.setMaximumWidth(800)
        self.searchBox.setMinimumWidth(300)
        pix = QtGui.QPixmap("piepdf/icons/search.svg")
        self.searchIcon.setPixmap(pix)
        self.searchWidget.setStyleSheet("QLabel {background-color : white; border: 5px solid white; border-top-left-radius: 10px; border-bottom-left-radius: 10px;} QLineEdit {background-color : white;border: 5px solid white; border-top-right-radius: 10px; border-bottom-right-radius: 10px;}")                                                    
        self.searchlayout.addStretch(1)
        self.searchlayout.addWidget(self.searchIcon )
        self.searchlayout.setSpacing(0)
        self.searchlayout.addWidget(self.searchBox )
        self.searchColumns = {'All':True}
        for i in self.tableTitles :
            self.searchColumns[i] = True

        self.searchMenu = QtWidgets.QMenu('All')
        self.searchMenuList = []
        #Add 'All' first

        self.searchMenuList.append( QtWidgets.QAction('All', checkable=True) )
        for i in self.searchColumns:
            if i != 'All':
               self.searchMenuList.append( QtWidgets.QAction(i, checkable=True) )
        for d in self.searchMenuList :
            d.setChecked(self.searchColumns[d.text()] )
            self.searchMenu.addAction(d)

        self.searchIcon.clicked.connect(self.showsearchIcon)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.parent_ui.mainToolBar.addWidget(spacer)
        self.parent_ui.mainToolBar.addWidget(self.searchWidget)
    def showsearchIcon(self,event):
        action = self.searchMenu.exec_(self.searchIcon.mapToGlobal(event.pos()))
        if action is not None:
        #while action is not None:
            actText = action.text()
            if actText == "All":
                self.searchColumns['All'] = not self.searchColumns['All']
                for i in self.searchColumns:
                    if i != "All":
                        self.searchColumns[i] =  self.searchColumns['All']
            else :
                self.searchColumns[actText] = not self.searchColumns[actText]
                self.searchColumns['All'] = False
            for d in self.searchMenuList:
                d.setChecked(self.searchColumns[d.text()] )
            #action = self.searchMenu.exec_(self.searchIcon.mapToGlobal(event.pos()))

    def metaSignal(self):
        try :
            index=self.parent_ui.listView.selectedIndexes()[0]
            info = {}
            for i in range(len(self.tableTitles)):
                info[self.tableTitles[i]] = self.model_3.item(index.row(),i).text()
            self.parent_ui.graphicsView.setData(info)
        except :
            print ("Meta Signal Failed " )
    def trsignal1(self):
        print("Signal 1 Triggered ")
        item = self.parent_ui.treeView.selectedIndexes()[0]
        subrootpath = self.model.filePath(item)
        print(self.model.filePath(item))
        self.model_2.setRootPath(subrootpath)
        self.parent_ui.treeView_2.setRootIndex(self.model_2.index(subrootpath))
        self.update_listview(subrootpath)
        # print(QFileSystemModel.fetchMore(item.parent()) )
        # print( item.model().itemFromIndex(index).text())


    def tr2_signal1(self):
        print("Signal 1 Triggered ")
        item = self.parent_ui.treeView_2.selectedIndexes()[0]
        subrootpath = self.model_2.filePath(item)
        self.update_listview(subrootpath)
        # print(QFileSystemModel.fetchMore(item.parent()) )
        # print( item.model().itemFromIndex(index).text())

    def updateWidgets(self):
        self.model = MyFileSystemModel( )
        self.model.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs )
        self.model.setRootPath(self.piepdf_path)
        self.model_2=MyFileSystemModel()
        self.model_2.setRootPath(self.piepdf_path)
        self.model_2.headerfirstcolumn="Sub Projects"
        self.model_2.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs )
        self.parent_ui.treeView.setModel(self.model)
        self.parent_ui.treeView.setRootIndex(self.model.index(self.piepdf_path ))
        self.parent_ui.treeView.setIndentation(20)
        self.parent_ui.treeView.hideColumn(2)
        self.parent_ui.treeView.hideColumn(1)
        self.parent_ui.treeView.hideColumn(3)
        self.parent_ui.treeView_2.setModel(self.model_2)
        self.parent_ui.treeView_2.setRootIndex(self.model_2.index(self.piepdf_path))
        self.parent_ui.treeView_2.setIndentation(20)
        self.parent_ui.treeView_2.hideColumn(2)
        self.parent_ui.treeView_2.hideColumn(1)
        self.parent_ui.treeView_2.hideColumn(3)
        self.parent_ui.listView.setWindowTitle('Example List')
        self.parent_ui.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.update_listview( self.piepdf_path)
    def resizefn():
        print("Windows Resized : ")
    def removeTab(self,index):
        #todo hide close tab for mainWindow
        if (index != 0 ):
            widget = self.parent_ui.tabWidget.widget(index)
            if widget is not None:
                widget.deleteLater()
            self.parent_ui.tabWidget.removeTab(index)

    def addsignals(self):
        self.parent_ui.tabWidget.setCurrentIndex(0)
        self.parent_ui.tabWidget.tabCloseRequested.connect( self.removeTab )
        self.parent_ui.treeView.activated.connect( self.trsignal1 )
        self.parent_ui.treeView_2.activated.connect( self.tr2_signal1)
        self.parent_ui.listView.doubleClicked.connect( self.filesignal )
        self.parent_ui.listView.clicked.connect(self.metaSignal )
        self.parent_ui.listView.selectionModel().selectionChanged.connect(self.metaSignal )
        self.searchBox.returnPressed.connect(self.search_signal )
