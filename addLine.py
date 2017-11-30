from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import ogr
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import psycopg2

import csv
import sys
import os
import utility
from utility import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/SystemInformation")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/MainForm")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ToolForms")

import resources
from frmAddLine import *

class frmAddLine_dialog(QDialog, Ui_frmAdLine):
    def __init__(self, iface):
        QtGui.QMainWindow.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.cmdClose.clicked.connect(self.onClose)
        self.cmdOK.clicked.connect(self.onOK)

    def onClose(self):
        self.close()

    def onOK(self):
        extensionProject.ProjectNumber = self.txtProNum.text()
        extensionProject.PhaseConfiguration = self.cmbConPhase.currentText()
        extensionProject.PrimaryConductor = self.cmbConSize.currentText()
        self.close()