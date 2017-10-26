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
from frmAddTransformer import *

class frmAddTransformer_dialog(QDialog, Ui_frmAddTransformer):

    def __init__(self, iface):
        QtGui.QMainWindow.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.cmdClose.clicked.connect(self.onClose)
        self.cmdOK.clicked.connect(self.onOK)

    def onClose(self):
        self.close()

    def onOK(self):
        sub = self.txtSub.text()
        fed = self.txtFed.text()
        proNum = self.txtProNum.text()
        extensionProject.ProjectNumber = self.txtProNum.text()
        extensionProject.BufferDistance = float(self.txtBuffDist.text())
        extensionProject.MinimumTransformerkVA = float(self.txtMinTrn.text())
        extensionProject.MaximumTransformerkVA = float(self.txtMaxTrn.text())
        self.close()