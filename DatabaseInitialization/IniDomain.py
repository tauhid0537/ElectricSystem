from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/DatabaseInitialization")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")

from frmDomain import *
import resources


class frmDomain_dialog(QDialog, Ui_frmDomain):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.cmdDomEdit.clicked.connect(self.getText)
        self.cmdClose.clicked.connect(self.onClose)

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def onClose(self):
        self.close()



