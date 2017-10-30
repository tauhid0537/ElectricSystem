from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import csv
import sys
import os
import sqlite3
import utility
from utility import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ProcessFieldData")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")

from frmGPSData import *
import resources

class frmGPSData_dialog(QDialog, Ui_frmGPSData):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        poleDB = self.getTableRowName(basicOps.sqlitedb, "vw_Pole_Data")
        self.poleModel = QtGui.QStandardItemModel(self)
        self.poleModel.setHorizontalHeaderLabels(poleDB.split(","))
        cur = self.sqliteCursor(basicOps.sqlitedb)
        columnsqry = "PRAGMA table_info(vw_Pole_Data)"
        cur.execute(columnsqry)
        numberOfColumns = len(cur.fetchall())
        polesql = "select * from vw_Pole_Data"
        cur.execute(polesql)
        rows = cur.fetchall()
        k = -1
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                item = QStandardItem(col)
                self.poleModel.setItem(i,j,item)
        self.poleView = self.dgvPole
        self.poleView.setModel(self.poleModel)

        """cur = self.sqliteCursor(basicOps.sqlitedb)
        polesql = "select * from vw_Pole_Data"
        cur.execute(polesql)
        poleRows = cur.fetchall()
        for poleRow in poleRows:"""

        self.cmdGPSEdit.clicked.connect(self.populatePoleTable)
        self.cmdClose.clicked.connect(self.onClose)

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def populatePoleTable(self):
        self.poleModel.clear()
        poleDB = self.getTableRowName(basicOps.sqlitedb, "vw_Pole_Data")
        self.poleModel.setHorizontalHeaderLabels(poleDB.split(","))
        cur = self.sqliteCursor(basicOps.sqlitedb)
        columnsqry = "PRAGMA table_info(vw_Pole_Data)"
        cur.execute(columnsqry)
        numberOfColumns = len(cur.fetchall())
        polesql = "select * from vw_Pole_Data"
        cur.execute(polesql)
        rows = cur.fetchall()
        k = -1
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                item = QStandardItem(col)
                self.poleModel.setItem(i,j,item)

        """for val in rows:
            row = []
            if k < numberOfColumns:
                k = k+1
                item = QStandardItem(val[k])
                row.append(item)
            self.poleModel.appendRow(row)
        self.poleView.setModel(self.poleModel)
        cur.close()"""

    def sqliteCursor(self,db):
        con = sqlite3.connect(db)
        c= con.cursor()
        return c

    def getTableRowName(self, db, table):
        c= self.sqliteCursor(db)
        c.execute("PRAGMA table_info(" + table + ")")
        rows = c.fetchall()
        text = []
        for row in rows:
            text.append(row[1])
        finaltext = ",".join(text)
        return finaltext


    def onClose(self):
        self.close()



