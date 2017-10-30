from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


import csv
import sys
import os
import utility
from utility import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ProcessFieldData")
from frmProcessFieldData import *
from ProGPSData import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
import resources

class frmProcessFieldData_dialog(QDialog, Ui_frmProcessData):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.cmdGetData.clicked.connect(self.openGPSDataForm)
        self.cmdClose.clicked.connect(self.onClose)
        self.cmbGroup.clear()
        self.cmbGroup.addItem('A')
        self.cmbGroup.addItem('B')
        self.cmbGroup.addItem('C')
        self.cmbGroup.addItem('D')
        self.cmbGroup.addItem('E')
        self.cmbGroup.addItem('F')
        self.cmbGroup.addItem('G')
        self.cmbGroup.addItem('H')
        self.cmbGroup.addItem('I')
        self.cmbGroup.addItem('J')
        self.cmbGroup.addItem('K')


    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def onClose(self):
        self.close()

    def selectSQLliteFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
         'c:\\',"SQLite Database files (*.sqlite)")
        return fname

    def openGPSDataForm(self):
        file_path = self.selectSQLliteFile()
        basicOps.sqlitedb = file_path
        proname = self.txtPro.text()
        self.close()
        gpsForm = frmGPSData_dialog(self.iface)
        gpsForm.txtPro.setText(proname)
        gpsForm.txtPBS.setText(basicOps.dbasename)
        group = self.cmbGroup.currentText()
        date = self.dtpSurvey.date()
        gpsForm.txtGroup.setText(group)
        gpsForm.txtSub.setText(basicOps.substation)
        gpsForm.txtFed.setText(basicOps.feeder)
        gpsForm.txtDate.setText(str(date.day()) + "/" + str(date.month()) + "/" + str(date.year()))
        gpsForm.exec_()

