import os
import sqlite3
import time

from piepdf.database import metadata
from PyQt5 import QtCore

DATABASE_PATH = (
    QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    + "/piepdf/piepdf_database"
)


class WorkerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)
    status = QtCore.pyqtSignal(object)


def xor(lst1, lst2):
    """ "
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


class DatabaseInit(QtCore.QRunnable):
    def __init__(self, pdfsPath, email=""):
        super(DatabaseInit, self).__init__()
        self.email = email
        self.signals = WorkerSignals()
        self.pdfsPath = pdfsPath
        os.makedirs(DATABASE_PATH, exist_ok=True)
        self.crMetadata = metadata.GetPdfInfo(email=self.email)
        self.database_path = os.path.join(DATABASE_PATH, "piepdf.db")
        self.column_list = (
            "Path, Title, Author, Year, Abstract, Doi, Url, Journal, Tags, Notes"
        )

        self.dirList = [dp for dp, dn, fn in os.walk(self.pdfsPath)]
        print(self.dirList)

        # Only create QFileSystemWatcher in main thread - disable it for now
        # to avoid threading issues with popplerqt5
        # self.fileSysWatcher = QtCore.QFileSystemWatcher()
        # self.fileSysWatcher.addPaths(self.dirList)
        # self.fileSysWatcher.directoryChanged.connect(self.slotDirChanged)
        # self.fileSysWatcher.fileChanged.connect(self.slotDirChanged)

        # self.deleteDatabase()
        # self.createDatabase()
        # self.addToDatabase(pdfsPath)

    def run(self):
        try:
            self.signals.status.emit("Updating  Database ..\n ")
            if os.path.exists(self.database_path):
                print("Database already exists! \n {}".format(self.database_path))
                self.checkDatabase()
            else:
                self.createDatabase()
                self.addToDatabase(self.pdfsPath)
            self.signals.finished.emit("Finished Database work!")
        except Exception as e:
            print(f"Error in database thread: {e}")
            import traceback

            traceback.print_exc()
            self.signals.finished.emit(f"Database error: {e}")

    def slotDirChanged(self):
        print("Directory changed !")
        self.dirList = [dp for dp, dn, fn in os.walk(self.pdfsPath)]
        if hasattr(self, "fileSysWatcher"):
            self.fileSysWatcher.addPaths(self.dirList)
        self.checkDatabase()

    def checkDatabase(self):
        """
        CHECK IF THERE IS ANY NEW FILE ADDED
        """
        try:
            print("Checking Database")
            dbFileList = []
            with sqlite3.connect(self.database_path) as db:
                cursor = db.cursor()
                cursor.execute("SELECT Path FROM pdffulltext ")
                for f in cursor.fetchall():
                    dbFileList.append(f[0])
            print(self.pdfsPath)
            self.fileList = [
                os.path.join(dp, f) for dp, dn, fn in os.walk(self.pdfsPath) for f in fn
            ]
            chFiles = xor(dbFileList, self.fileList)
            db = sqlite3.connect(self.database_path)
            if chFiles is not None:
                for filepath1 in chFiles:
                    try:
                        self.signals.status.emit(f"Updating  Database for {filepath1}")
                        print(f"Working on the file {filepath1}")
                        if filepath1 in self.fileList:
                            extension = os.path.splitext(filepath1)[1]
                            if ".pdf" == extension:
                                print("added file : {} ".format(filepath1))
                                try:
                                    info = self.crMetadata.getMetadata(filepath1)
                                except Exception as pdf_error:
                                    print(
                                        f"Error extracting metadata from {filepath1}: {pdf_error}"
                                    )
                                    info = {
                                        "title": os.path.basename(filepath1),
                                        "author": "",
                                        "year": "",
                                        "abstract": "",
                                        "doi": "",
                                        "url": "",
                                        "journal": "",
                                    }

                                try:
                                    db.execute(
                                        """INSERT INTO
                                    pdffulltext( Path, Title, Author, Year, Abstract, Doi, Url,
                                    Journal, Tags, Notes )
                                        VALUES(?,?,?,?,?,?,?,?,?,?);""",
                                        (
                                            filepath1,
                                            info["title"],
                                            info["author"],
                                            info["year"],
                                            info["abstract"],
                                            info["doi"],
                                            info["url"],
                                            info["journal"],
                                            "",
                                            "",
                                        ),
                                    )
                                    time.sleep(1)
                                except Exception as db_error:
                                    print(f"Error inserting into database: {db_error}")
                        else:
                            print("Removed File : {} ".format(filepath1))
                    except Exception as inst:
                        print(f"Unable read {filepath1} with error {inst}")

            db.commit()
            db.close()
        except Exception as e:
            print(f"Error in checkDatabase: {e}")
            import traceback

            traceback.print_exc()

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

    def createDatabase(self):
        self.database = sqlite3.connect(self.database_path)
        self.database.execute(
            "CREATE VIRTUAL TABLE pdffulltext USING FTS5({})".format(self.column_list)
        )

        self.database.commit()
        self.database.close()

    def addToDatabase(self, rootpath):
        db = sqlite3.connect(self.database_path)
        print("started database")
        for path, subdirs, files in os.walk(rootpath):
            for name in files:
                try:
                    self.signals.status.emit(f"Updating  Database for {name}")
                    filepath1 = os.path.join(path, name)
                    extension = os.path.splitext(filepath1)[1]
                    if ".pdf" == extension:
                        info = self.crMetadata.getMetadata(filepath1)
                        db.execute(
                            """INSERT INTO
                        pdffulltext( Path, Title, Author, Year, Abstract, Doi, Url,
                        Journal, Tags, Notes )
                              VALUES(?,?,?,?,?,?,?,?,?,?);""",
                            (
                                filepath1,
                                info["title"],
                                info["author"],
                                info["year"],
                                info["abstract"],
                                info["doi"],
                                info["url"],
                                info["journal"],
                                "",
                                "",
                            ),
                        )
                        time.sleep(5)
                except Exception as inst:
                    print(f"Unable read {filepath1} with error {inst}")

        db.commit()
        db.close()

    def searchDb(self, string="kondo", columns=["Author", "Title"]):
        slist = []
        sql_command = "SELECT * FROM pdffulltext WHERE "
        for i in columns:
            sql_command += " {} LIKE '%{:s}%' OR".format(i, string)
        sql_command = sql_command[:-3]
        # "Author  LIKE '%{:s}%' OR Title LIKE '%{:s}%'".format(string,string)
        print(sql_command)
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            cursor.execute(sql_command)
            # cursor.execute("SELECT * FROM pdffulltext WHERE Author LIKE  '%{:s}%' ".format(string))
            for f in cursor.fetchall():
                print(f)
                slist.append(f)
        return slist

    def getFileList(self, string=""):
        slist = []
        with sqlite3.connect(self.database_path) as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM pdffulltext WHERE Path LIKE '%{:s}%'".format(string)
            )
            for f in cursor.fetchall():
                slist.append(f)
        return slist

    def deleteDatabase(self):
        if os.path.exists(self.database_path):
            os.remove(self.database_path)
