from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import qgis

import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/MainForm")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/DatabaseInitialization")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ProcessFieldData")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ValidateDatabase")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/FinancialAnalysis")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")

import utility
from utility import *

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import psycopg2

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

        self.cmbSub.currentIndexChanged.connect(self.loadFedcmbBox)
        self.cmdCreate.clicked.connect(self.openInitialize)
        self.cmdProcess.clicked.connect(self.openProcess)
        self.cmdValidate.clicked.connect(self.openValidate)
        self.cmdFinance.clicked.connect(self.openFinance)
        self.cmdAddlayer.clicked.connect(self.addLayers)
        self.cmdClose.clicked.connect(self.onClose)

    def loadFedcmbBox(self):

        usr = basicOps.usrname
        hst = basicOps.hostname
        paswrd = basicOps.password
        dbase = basicOps.dbasename
        QMessageBox.information(self.iface.mainWindow(),"Add Layers",str([usr,paswrd,hst,dbase]))
        sub = self.cmbSub.currentText()
        bsOps = utility.basicOps()
        fedlist = bsOps.getFeederList(usr, hst, paswrd, dbase, sub)
        self.cmbFed.clear()
        #sysinfo.cmbFed.clear()
        self.cmbFed.addItems(sublist)
        self.cmbFed.setCurrentIndex(-1)

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def addLayers(self):
        usr = self.txtPro.text()
        dbase = self.txtDatabase.text()
        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()
        hst = utility.basicOps.hostname
        paswrd = utility.basicOps.password
        fedcode = utility.basicOps.getFedCode(sub, fed)
        subcode = utility.basicOps.getSubCode(sub)
        subtablename = "esystems." + sub + "_substation"
        poletablename = "esystems." + sub + "_" + fed + "_pole"
        linetablename = "esystems." + sub + "_" + fed + "_line"
        subLayerName = dbase + ": " + sub + "-Substation"
        poleLayerName = dbase + ": " + sub + "-" + fed + "-Pole"
        lineLayerName = dbase + ": " + sub + "-" + fed + "-Line"

        try:
            subUri = QgsDataSourceURI()
            subUri.setConnection(hst, "5432", dbase, usr, paswrd)
            subUri.setDataSource("esystems", subtablename, "geom")
            sublayer = QgsVectorLayer(subUri.subUri(False), subLayerName, "postgres")

            poleUri = QgsDataSourceURI()
            poleUri.setConnection(hst, "5432", dbase, usr, paswrd)
            poleUri.setDataSource("esystems", poletablename, "geom")
            polelayer = QgsVectorLayer(poleUri.poleUri(False), poleLayerName, "postgres")

            lineUri = QgsDataSourceURI()
            lineUri.setConnection(hst, "5432", dbase, usr, paswrd)
            lineUri.setDataSource("esystems", linetablename, "geom")
            linelayer = QgsVectorLayer(lineUri.lineUri(False), lineLayerName, "postgres")

            QgsMapLayerRegistry.instance().addMapLayers([linelayer, polelayer, sublayer])
        except:
            QMessageBox.information(self.iface.mainWindow(),"Add Layers","Layers not added")
        QMessageBox.information(self.iface.mainWindow(),"Add Layers","Layers Added")

    def onClose(self):
        self.close()

    def openInitialize(self):
        proname = self.txtPro.text()
        self.close()
        intialize = frmInitialize_dialog(self.iface)
        intialize.txtPro.setText(utility.basicOps.usrname)
        intialize.txtPBS.setText(utility.basicOps.dbasename)
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
