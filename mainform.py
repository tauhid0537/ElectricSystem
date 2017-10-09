from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/MainForm")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/DatabaseInitialization")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ProcessFieldData")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ValidateDatabase")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/FinancialAnalysis")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")

from frmMain import *
from databaseinitialization import *
from processfielddata import *
from validatedatabase import *
from financialanalysis import *
import resources

class frmMain_dialog(QDialog, Ui_frmMain):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        #self.setStyle(QtGui.QStyleFactory.create("GTK+"))

        self.cmdCreate.clicked.connect(self.openInitialize)
        self.cmdProcess.clicked.connect(self.openProcess)
        self.cmdValidate.clicked.connect(self.openValidate)
        self.cmdFinance.clicked.connect(self.openFinance)
        self.cmdAddlayer.clicked.connect(self.getText)
        self.cmdClose.clicked.connect(self.onClose)

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def onClose(self):
        self.close()

    def openInitialize(self):
        proname = self.txtPro.text()
        self.close()
        intialize = frmInitialize_dialog(self.iface)
        intialize.txtPro.setText(proname)
        intialize.exec_()

    def openProcess(self):
        proname = self.txtPro.text()
        self.close()
        intialize = frmProcessFieldData_dialog(self.iface)
        intialize.txtPro.setText(proname)
        intialize.exec_()

    def openValidate(self):
        proname = self.txtPro.text()
        self.close()
        validate = frmValidate_dialog(self.iface)
        validate.txtPro.setText(proname)
        validate.exec_()

    def openFinance(self):
        proname = self.txtPro.text()
        self.close()
        validate = frmFinance_dialog(self.iface)
        validate.txtPro.setText(proname)
        validate.exec_()
