
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets


class FileWatcher(QtWidgets.QMainWindow):
    def __init__(self, pathToWatch=None, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi()
        self.pathToWatch = pathToWatch
        self.fileList = [os.path.join(dp, f) for dp, dn, fn in os.walk( 
self.pathToWatch) for f in fn]
        self.dirList = [dp for dp, dn, fn in os.walk(self.pathToWatch)]
        self.fileSysWatcher = QtCore.QFileSystemWatcher()
        self.fileSysWatcher.addPaths(self.dirList)
        self.fileSysWatcher.directoryChanged.connect(self.slotDirChanged)
        self.fileList = [os.path.join(dp, f) for dp, dn, fn in os.walk( self.pathToWatch) for f in fn]
        self.dirList = [dp for dp, dn, fn in os.walk(self.pathToWatch)]

	def xor(lst1, lst2):
		"""
		returns a tuple of items of item not in either of lists
		"""
		items = []
		for itm in lst1:
			 if itm not in lst2:
				 items.append(itm)
		for itm in lst2:
			 if itm not in lst1:
				 items.append(itm)
		return items


    def setupUi(self):
        self.label = QtWidgets.QLabel("Watching folder")
        self.setCentralWidget(self.label)
        self.setWindowTitle("Detect Dir Change")
    def slotDirChanged(self, path):
        #print("Watching folder {}".format(self.fileSysWatcher.directories()) )
        #print("Watching files {}".format(self.fileSysWatcher.files()) )
        tempDir = [dp for dp, dn, fn in os.walk(self.pathToWatch)]
        tempFile = [os.path.join(dp, f) for dp, dn, fn in os.walk(self.pathToWatch) for f in fn]
        chFiles = self.xor(tempFile, self.fileList)
        chFolders = self.xor(self.dirList, tempDir)
        msg = ""
        print("Folder change list: {} ".format(chFolders) )
        print("File change list: {} ".format(chFiles))
        if chFiles is not None : 
            for newContent1 in chFiles:
                print("File changed")
                if newContent1 not in self.fileList:
                    msg = msg + "added file : %s \n" % newContent1
                else:
                    msg = msg + "remove file : %s\n" % newContent1
        if chFolders is not None : 
            for newContent2 in chFolders:
                print("Folder changed")
                if newContent2 not in self.dirList:
                    msg = msg + "added folder : %s \n" % newContent2
                    self.fileSysWatcher.addPath (newContent2 )
                else:
                    msg = msg + "removed folder : %s \n" % newContent2
                    self.fileSysWatcher.removePath (newContent2 )
                    
                    
        self.fileList = [os.path.join(dp, f) for dp, dn, fn in    os.walk(self.pathToWatch) for f in fn]
        self.dirList = [dp for dp, dn, fn in os.walk(self.pathToWatch)]
        #self.fileSysWatcher.addPaths(self.dirList)
        self.label.setText("Detected  Change!! \n %s" % msg)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow("/home/saurabh/Dropbox/github/work/test")
    window.show()
    window.raise_()

    return sys.exit(app.exec_())


if __name__ == '__main__':
    main()mport os
from PyQt5 import QtCore, QtGui, QtWidgets


class FileWatcher(QtWidgets.QMainWindow):
    def __init__(self, pathToWatch=None, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi()
        self.pathToWatch = pathToWatch
        self.fileList = [os.path.join(dp, f) for dp, dn, fn in os.walk( 
self.pathToWatch) for f in fn]
        self.dirList = [dp for dp, dn, fn in os.walk(self.pathToWatch)]
        self.fileSysWatcher = QtCore.QFileSystemWatcher()
        self.fileSysWatcher.addPaths(self.dirList)
        self.fileSysWatcher.directoryChanged.connect(self.slotDirChanged)
        self.fileList = [os.path.join(dp, f) for dp, dn, fn in os.walk( self.pathToWatch) for f in fn]
        self.dirList = [dp for dp, dn, fn in os.walk(self.pathToWatch)]

	def xor(lst1, lst2):
		"""
		returns a tuple of items of item not in either of lists
		"""
		items = []
		for itm in lst1:
			 if itm not in lst2:
				 items.append(itm)
		for itm in lst2:
			 if itm not in lst1:
				 items.append(itm)
		return items


    def setupUi(self):
        self.label = QtWidgets.QLabel("Watching folder")
        self.setCentralWidget(self.label)
        self.setWindowTitle("Detect Dir Change")
    def slotDirChanged(self, path):
        #print("Watching folder {}".format(self.fileSysWatcher.directories()) )
        #print("Watching files {}".format(self.fileSysWatcher.files()) )
        tempDir = [dp for dp, dn, fn in os.walk(self.pathToWatch)]
        tempFile = [os.path.join(dp, f) for dp, dn, fn in os.walk(self.pathToWatch) for f in fn]
        chFiles = self.xor(tempFile, self.fileList)
        chFolders = self.xor(self.dirList, tempDir)
        msg = ""
        print("Folder change list: {} ".format(chFolders) )
        print("File change list: {} ".format(chFiles))
        if chFiles is not None : 
            for newContent1 in chFiles:
                print("File changed")
                if newContent1 not in self.fileList:
                    msg = msg + "added file : %s \n" % newContent1
                else:
                    msg = msg + "remove file : %s\n" % newContent1
        if chFolders is not None : 
            for newContent2 in chFolders:
                print("Folder changed")
                if newContent2 not in self.dirList:
                    msg = msg + "added folder : %s \n" % newContent2
                    self.fileSysWatcher.addPath (newContent2 )
                else:
                    msg = msg + "removed folder : %s \n" % newContent2
                    self.fileSysWatcher.removePath (newContent2 )
                    
                    
        self.fileList = [os.path.join(dp, f) for dp, dn, fn in    os.walk(self.pathToWatch) for f in fn]
        self.dirList = [dp for dp, dn, fn in os.walk(self.pathToWatch)]
        #self.fileSysWatcher.addPaths(self.dirList)
        self.label.setText("Detected  Change!! \n %s" % msg)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow("/home/saurabh/Dropbox/github/work/test")
    window.show()
    window.raise_()

    return sys.exit(app.exec_())


if __name__ == '__main__':
    main()
