from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from osgeo import ogr
import qgis

import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Utilities")
import utilities

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/DatabaseInitialization")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")

from frmConductor import *
import resources

class frmConductor_dialog(QDialog, Ui_frmConductor):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['Name', 'Construction Type', 'Strand', 'Type', 'Diameter in mm', 'Cross Section Area in mm', 'Resistance per km', 'Geometric Mean Radius-meter','Reactance per km for 50 Hz System','Reactance per km for 60 Hz System','Maximum Current Carrying Capacity in Amps' ])
        self.tableView = self.dgvTable
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

        self.cmdConSave.clicked.connect(self.getTableSaved)
        self.cmdConEdit.clicked.connect(self.getTableEditable)
        self.cmdClose.clicked.connect(self.onClose)

    def loadTable(self):
        # Load Conductor Table to DataGridView
        drv = utilities.drvpath
        pro = utilities.proname
        sub = self.txtSub.text()
        fed = self.txtFed.text()
        pbs = self.txtPBS.text()


        tabLoc = drv + ":\\" + pro + "\\Database\\" + pbs + "\\Tables\\SysConductor.dbf" 
        pTable = QgsVectorLayer(tabLoc, 'SysConductor', 'ogr')
        pCursor = pTable.getFeatures()

        r = 0

        for row in pCursor:
            self.model.insertRow(r)
            for field in  pTable.fields():
                fieldname = field.name()
                idx = pTable.fieldNameIndex(fieldname)
                if row[fieldname] != None:
                    self.model.setItem(r, idx, QtGui.QStandardItem(str(row[fieldname])))
            r = r + 1

    def getTableEditable(self):
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Interactive)
        QMessageBox.information(self,"Edit Conductor Table", "Table is now editable\nDouble-Click the cell to edit")

    def getTableSaved(self):
        reply = QMessageBox.question(self, "Edit Conductor Table", "Do you want to save the conductor table?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            QMessageBox.information(self,"Edit Conductor Table", "Table is saved")

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def onClose(self):
        self.close()
