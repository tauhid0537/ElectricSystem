from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import qgis

import csv
import sys
import os

from os import listdir
from os.path import isfile, join

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
        self.cmdClear.clicked.connect(self.removeAllLayers)
        self.cmdGetLb.clicked.connect(self.loadLbase)
        self.cmdAddLb.clicked.connect(self.addLbase)

    def loadFedcmbBox(self):

        usr = basicOps.usrname
        hst = basicOps.hostname
        paswrd = basicOps.password
        dbase = basicOps.dbasename

        #QMessageBox.information(self.iface.mainWindow(),"Add Layers",str([usr,paswrd,hst,dbase]))
        curdb = self.getCursor(usr, hst, paswrd, dbase)
        sub = self.cmbSub.currentText()
        bsOps = utility.basicOps()
        fedlist = bsOps.getFeederList(curdb, sub)
        self.cmbFed.clear()
        #sysinfo.cmbFed.clear()
        self.cmbFed.addItems(fedlist)
        self.cmbFed.setCurrentIndex(-1)
        #QMessageBox.information(self.iface.mainWindow(),"Add Layers",str([basicOps.usrname,basicOps.password,basicOps.hostname,basicOps.dbasename]))

    def refresh_layers(self):
        for layer in qgis.utils.iface.mapCanvas().layers():
            layer.triggerRepaint()

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def getCursor(self, usr, hst, pas, db):
        cur = None
        try:
            condb = psycopg2.connect(user = usr, host = hst, password = pas, dbname = db)
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = condb.cursor()
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        return cur

    def loadLbase(self):
        self.cmbLayers.clear()
        lblist = []
        usr = self.txtPro.text()
        dbase = self.txtDatabase.text()
        hst = basicOps.hostname
        paswrd = basicOps.password
        cur = self.getCursor(usr, hst, paswrd, dbase)
        cur.execute("""SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'landbase'""")
        rows = cur.fetchall()
        for row in rows:
            lblist.append(row[0])
        self.cmbLayers.addItems(lblist)
        self.cmbLayers.setCurrentIndex(-1)

        slddir = os.path.dirname(__file__) + "/Resources/SLD"
        slds=os.listdir(slddir)
        onlyslds=[x.split('.')[0] for x in slds]
        #onlyfiles = [f for f in listdir(slddir) if isfile(join(slddir, f))]

        self.cmbLegend.clear()
        self.cmbLegend.addItems(onlyslds)
        self.cmbLegend.setCurrentIndex(-1)

    def addLbase(self):
        usr = self.txtPro.text()
        dbase = self.txtDatabase.text()
        hst = basicOps.hostname
        paswrd = basicOps.password
        cur = self.getCursor(usr, hst, paswrd, dbase)
        lname = self.cmbLayers.currentText()
        legname = self.cmbLegend.currentText()

        uri = QgsDataSourceURI()
        uri.setConnection(hst,"5432",dbase,usr,paswrd)
        uri.setDataSource("landbase",lname,"geom")
        llayer = QgsVectorLayer(uri.uri(), lname, "postgres")
        sld = os.path.dirname(__file__) + "/Resources/SLD/" + legname + ".sld"

        llayer.loadSldStyle(sld)
        QgsMapLayerRegistry.instance().addMapLayer(llayer)
        #layer.triggerRepaint()
        self.refresh_layers()

    def addSubLayer(self):
        usr = self.txtPro.text()
        dbase = self.txtDatabase.text()
        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()
        hst = basicOps.hostname
        paswrd = basicOps.password
        cur = self.getCursor(usr, hst, paswrd, dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)
        subLayer =sub + "_substation"
        subLayerName = dbase + ": " + sub + "-substation"

        uri = QgsDataSourceURI()
        uri.setConnection(hst,"5432",dbase,usr,paswrd)
        uri.setDataSource("esystems",subLayer,"geom")
        sublayer = QgsVectorLayer(uri.uri(), subLayerName, "postgres")

        QgsMapLayerRegistry.instance().addMapLayer(sublayer)
        self.refresh_layers()

    def addPoleLayer(self):
        usr = self.txtPro.text()
        dbase = self.txtDatabase.text()
        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()
        hst = basicOps.hostname
        paswrd = basicOps.password
        cur = self.getCursor(usr, hst, paswrd, dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)
        poletablename = subcode + "_" + fedcode + "_pole"
        poleLayerName = dbase + ": " + sub + "-" + fed + "-pole"
        uri = QgsDataSourceURI()
        uri.setConnection(hst,"5432",dbase,usr,paswrd)
        uri.setDataSource("esystems",poletablename,"geom")
        polelayer = QgsVectorLayer(uri.uri(), poleLayerName, "postgres")
        #QMessageBox.information(self.iface.mainWindow(),"Add Layers",str(hst))
        QgsMapLayerRegistry.instance().addMapLayer(polelayer)
        self.refresh_layers()

    def addLineLayer(self):
        usr = self.txtPro.text()
        dbase = self.txtDatabase.text()
        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()
        hst = basicOps.hostname
        paswrd = basicOps.password
        cur = self.getCursor(usr, hst, paswrd, dbase)
        bsOps = utility.basicOps()
        fedcode = bsOps.getFedCode(cur, sub, fed)
        subcode = bsOps.getSubCode(cur, sub)
        linetablename = subcode + "_" + fedcode + "_line"
        lineLayerName = dbase + ": " + sub + "-" + fed + "-line"
        uri = QgsDataSourceURI()
        uri.setConnection(hst, "5432", dbase, usr, paswrd)
        uri.setDataSource("esystems", linetablename, "geom")
        linelayer = QgsVectorLayer(uri.uri(), lineLayerName, "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(linelayer)
        self.refresh_layers()

    def addLayers(self):
        try:
            self.addLineLayer()
            self.addPoleLayer()
            self.addSubLayer()
        except EnvironmentError as e:
            QMessageBox.information(self.iface.mainWindow(),"Add Layers","Failed to add Layers!\n{0}".format(e))

    def removeAllLayers(self):
        QgsMapLayerRegistry.instance().removeAllMapLayers()

    def onClose(self):
        self.close()

    def openInitialize(self):
        proname = self.txtPro.text()
        self.close()
        usr = basicOps.usrname
        dbase = basicOps.dbasename
        intialize = frmInitialize_dialog(self.iface)
        intialize.txtPro.setText(usr)
        intialize.txtPBS.setText(dbase)
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
