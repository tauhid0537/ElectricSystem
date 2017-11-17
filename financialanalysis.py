from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/FinancialAnalysis")
from frmFinance import *
from fininputtable import *

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
#import resources

class frmFinance_dialog(QDialog, Ui_frmFinance):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.cmdInputTable.clicked.connect(self.openInputTable)
        self.cmdClose.clicked.connect(self.onClose)

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def onClose(self):
        self.close()

    def openInputTable(self):
        proname = self.txtPro.text()

        self.close()
        gpsForm = frmInputTable_dialog(self.iface)
        gpsForm.txtPro.setText(proname)
        gpsForm.txtPBS.setText(basicOps.dbasename)
        gpsForm.txtSub.setText(basicOps.substation)
        gpsForm.txtFed.setText(basicOps.feeder)
        gpsForm.exec_()

