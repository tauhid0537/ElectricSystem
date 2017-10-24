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
import math

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
        self.usr = basicOps.usrname
        self.dbase = basicOps.dbasename
        self.sub = basicOps.substation
        self.fed = basicOps.feeder
        self.hst = basicOps.hostname
        self.pas = basicOps.password
        self.lineLayerName = self.dbase + ": " + self.sub + "-" + self.fed + "-line"
        self.poleLayerName = self.dbase + ": " + self.sub + "-" + self.fed + "-pole"
        self.setLayerName = self.dbase + ": Settlement"
        self.strLayerName = self.dbase + ": Structure"
        self.villayerName = self.dbase + ": Village"
        self.lodlayerName = self.dbase + ": LoadCenter"

        self.setProName = self.dbase + ": " + self.sub + "-" + self.fed + "-Settlement-Project-" + extensionProject.ProjectNumber
        self.strProName = self.dbase + ": " + self.sub + "-" + self.fed + "-Structure-Project-" + extensionProject.ProjectNumber
        self.cenProName = self.dbase + ": " + self.sub + "-" + self.fed + "-LoadCenter-Project-" + extensionProject.ProjectNumber
        self.trnProName = self.dbase + ": " + self.sub + "-" + self.fed + "-Pole-Project-" + extensionProject.ProjectNumber
        self.linProName = self.dbase + ": " + self.sub + "-" + self.fed + "-Line-Project-" + extensionProject.ProjectNumber

        transForm = frmAddTransformer_dialog(self.iface)
        transForm.txtPro.setText(basicOps.usrname)
        transForm.txtDatabase.setText(basicOps.dbasename)
        transForm.txtSub.setText(basicOps.substation)
        transForm.txtFed.setText(basicOps.feeder)

        transForm.exec_()

    def powerDemand(self, consumer, consumption):
        pd = consumer *(1 - 0.4 * consumer + 0.4 * math.pow((math.pow(consumer, 2) + 40), 0.5) * (0.0059256 * math.pow(consumption, 0.885)))
        return pd
    def transformerMinMaxSize(self):
        minSize = 0
        maxSize = 0
        strselwhrClause = "Item = '" + "Equipment" + "' AND Type = '" + "Transformer" + "' AND Voltage = " + extensionProject.LineVoltage
        tableName = "exprojects.FinInConstructionCost"
        sql = "select min(size), max(size) from " + tableName + "where " + strselwhrClause + ";"
        cur = self.getCursor(self.usr, self.hst, self.pas, self.dbase)
        cur.execute(sql)
        row = cur.fetchOne()
        minSize = row[0]
        maxSize = row[1]
        return minSize, maxSize

    def getCursor(self, usr, hst, pas, db):
        cur = None
        try:
            condb = psycopg2.connect(user = usr, host = hst, password = pas, dbname = db)
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = condb.cursor()
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        return cur

    def checkAllLayers(self, householdSource):
        message = None
        check = False
        bsOps = utility.basicOps()
        if householdSource == "Settlement":
            if (bsOps.checkLayer(self.lineLayerName) == True and
            bsOps.checkLayer(self.poleLayerName) == True and
            bsOps.checkLayer(self.setLayerName) == True and
            bsOps.checkLayer(self.trnProName) == True and
            bsops.checkLayer(self.linProName) == True and
            bsOps.checkLayer(self.setProName) == True):
                check = True
            else:
                message = "The Following Layers Must Exist in the Map:\n\nFeeder Line\r\nFeeder Pole\r\nSettlement\r\nProject Line\r\nProject Pole\r\nProject Settlement"
        elif householdSource == "Structure":
            if (bsOps.checkLayer(self.lineLayerName) == True and
            bsOps.checkLayer(self.poleLayerName) == True and
            bsOps.checkLayer(self.strLayerName) == True and
            bsOps.checkLayer(self.trnProName) == True and
            bsops.checkLayer(self.linProName) == True and
            bsOps.checkLayer(self.strProName) == True):
                check = True
            else:
                message = "The Following Layers Must Exist in the Map:\n\nFeeder Line\r\nFeeder Pole\r\nStructure\r\nProject Line\r\nProject Pole\r\nProject Structure"
        elif householdSource == "Village":
            if (bsOps.checkLayer(self.lineLayerName) == True and
            bsOps.checkLayer(self.poleLayerName) == True and
            bsOps.checkLayer(self.villayerName) == True and
            bsOps.checkLayer(self.trnProName) == True and
            bsops.checkLayer(self.linProName) == True and
            bsOps.checkLayer(self.cenProName) == True):
                check = True
            else:
                message = "The Following Layers Must Exist in the Map: \n\nFeeder Line\r\nFeeder Pole\r\nVillage Area\r\nProject Line\r\nProject Load Center"
        else:
            message = "Unknown Household Data Source"
        return check, message

    def getProNum(self):
        projectNumber = None
        layers = qgis.utils.iface.mapCanvas().layers()
        for layer in layers:
            name = layer.name()
            if "Project" in name:
                fullName = name.split('-')
                projectNumber = fullName[4].strip()
        return projectNumber


    def canvasPressEvent(self, event):
        QMessageBox.information(self.iface.mainWindow(),"Test Tool","Project Number: "+ extensionProject.ProjectNumber + ", Substation: "+ basicOps.substation + "!!!")
