from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *
import qgis

#import resources_rc
import os
import sys
import csv
from os import listdir
from os.path import isfile, join

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import psycopg2

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ToolForms")

import utility
from utility import *

from frmAddTransformer import *
from addTransformer import *

class testTool(QgsMapTool):
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.canvas = iface.mapCanvas()
        self.iface = iface
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                          "      c None",
                                          ".     c #FF0000",


                                          "+     c #FFFFFF",
                                          "                ",
                                          "       +.+      ",
                                          "      ++.++     ",
                                          "     +.....+    ",
                                          "    +.     .+   ",
                                          "   +.   .   .+  ",
                                          "  +.    .    .+ ",
                                          " ++.    .    .++",
                                          " ... ...+... ...",
                                          " ++.    .    .++",
                                          "  +.    .    .+ ",
                                          "   +.   .   .+  ",
                                          "   ++.     .+   ",
                                          "    ++.....+    ",
                                          "      ++.++     ",
                                          "       +.+      "]))

    def activate(self):
        self.canvas.setCursor(self.cursor)
        usr = basicOps.usrname
        dbase = basicOps.dbasename
        sub = basicOps.substation
        fed = basicOps.feeder
        transForm = frmAddTransformer_dialog(self.iface)
        transForm.txtPro.setText(basicOps.usrname)
        transForm.txtDatabase.setText(basicOps.dbasename)
        transForm.txtSub.setText(basicOps.substation)
        transForm.txtFed.setText(basicOps.feeder)
        transForm.exec_()

    def canvasPressEvent(self, event):
        QMessageBox.information(self.iface.mainWindow(),"Test Tool","Project Number: "+ extensionProject.ProjectNumber + ", Substation: "+ basicOps.substation + "!!!")
