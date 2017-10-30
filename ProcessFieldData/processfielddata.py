from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


import csv
import sys
import os

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
        QMessageBox.information(self.iface.mainWindow(),"Test",str(file_path))
        """proname = self.txtPro.text()
        self.close()
        gpsForm = frmGPSData_dialog(self.iface)
        gpsForm.txtPro.setText(proname)
        gpsForm.exec_()"""

