from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import qgis

import csv
import sys
import os
import json

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

        self.usr = basicOps.usrname
        self.dbase = basicOps.dbasename
        self.hst = basicOps.hostname
        self.paswrd = basicOps.password

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
        curdb = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        sub = self.cmbSub.currentText()
        bsOps = utility.basicOps()
        fedlist = bsOps.getFeederList(curdb, sub)
        self.cmbFed.clear()
        self.cmbFed.addItems(fedlist)
        self.cmbFed.setCurrentIndex(-1)

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
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        cur.execute("""SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'landbase'""")
        rows = cur.fetchall()
        for row in rows:
            lblist.append(row[0])
        self.cmbLayers.addItems(lblist)
        self.cmbLayers.setCurrentIndex(-1)

        slddir = os.path.dirname(__file__) + "/Resources/SLD"
        slds=os.listdir(slddir)
        onlyslds=[x.split('.')[0] for x in slds]

        self.cmbLegend.clear()
        self.cmbLegend.addItems(onlyslds)
        self.cmbLegend.setCurrentIndex(-1)

    def addLbase(self):
        lname = self.cmbLayers.currentText()
        legname = self.cmbLegend.currentText()

        uri = QgsDataSourceURI()
        uri.setConnection(self.hst,"5432",self.dbase,self.usr,self.paswrd)
        uri.setDataSource("landbase",lname,"geom")
        llayer = QgsVectorLayer(uri.uri(), lname, "postgres")
        sld = os.path.dirname(__file__) + "/Resources/SLD/" + legname + ".sld"

        llayer.loadSldStyle(sld)
        QgsMapLayerRegistry.instance().addMapLayer(llayer)
        self.refresh_layers()

    def addSubLayer(self):

        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()

        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)
        subLayer =sub + "_substation"
        subLayerName = self.dbase + ": " + sub + "-substation"
        layers = qgis.utils.iface.mapCanvas().layers()
        foundlayer = False

        uri = QgsDataSourceURI()
        uri.setConnection(self.hst,"5432",self.dbase,self.usr,self.paswrd)
        uri.setDataSource("esystems",subLayer,"geom")
        sublayer = QgsVectorLayer(uri.uri(), subLayerName, "postgres")

        QgsMapLayerRegistry.instance().addMapLayer(sublayer)
        self.refresh_layers()

    def addPoleLayer(self):
        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()

        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)
        poletablename = subcode + "_" + fedcode + "_pole"
        poleLayerName = self.dbase + ": " + sub + "-" + fed + "-pole"
        layers = qgis.utils.iface.mapCanvas().layers()
        foundlayer = False

        uri = QgsDataSourceURI()
        uri.setConnection(self.hst,"5432",self.dbase,self.usr,self.paswrd)
        uri.setDataSource("esystems",poletablename,"geom")
        polelayer = QgsVectorLayer(uri.uri(), poleLayerName, "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(polelayer)
        self.refresh_layers()

    def addProLayer(self, typ):
        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()

        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)
        if typ == "pole":
            poletablename = subcode + "_" + fedcode + "_pole_project_1"
            poleLayerName = self.dbase + ": " + sub + "-" + fed + "-pole-project-1"
            extensionProject.PoleTableName = poletablename
        elif typ == "line":
            poletablename = subcode + "_" + fedcode + "_pole_project_1"
            poleLayerName = self.dbase + ": " + sub + "-" + fed + "-line-project-1"
            extensionProject.LineTableName = poletablename
        elif typ == "buffer":
            poletablename = subcode + "_" + fedcode + "_buffer_project_1"
            poleLayerName = self.dbase + ": " + sub + "-" + fed + "-buffer-project-1"
            extensionProject.BufferTableName = poletablename
        elif typ == "structure":
            poletablename = subcode + "_" + fedcode + "_structure_project_1"
            poleLayerName = self.dbase + ": " + sub + "-" + fed + "-structure-project-1"
            extensionProject.HHSourceTableName = poletablename
        elif typ == "village":
            poletablename = subcode + "_" + fedcode + "_village_project_1"
            poleLayerName = self.dbase + ": " + sub + "-" + fed + "-village-project-1"
            extensionProject.HHSourceTableName = poletablename
        elif typ == "settlement":
            poletablename = subcode + "_" + fedcode + "_settlement_project_1"
            poleLayerName = self.dbase + ": " + sub + "-" + fed + "-settlement-project-1"
            extensionProject.HHSourceTableName = poletablename
        layers = qgis.utils.iface.mapCanvas().layers()
        foundlayer = False

        uri = QgsDataSourceURI()
        uri.setConnection(self.hst, "5432", self.dbase, self.usr, self.paswrd)
        uri.setDataSource("exprojects",poletablename,"geom")
        polelayer = QgsVectorLayer(uri.uri(), poleLayerName, "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(polelayer)
        self.refresh_layers()

    def addLineLayer(self):
        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()

        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsOps = utility.basicOps()
        fedcode = bsOps.getFedCode(cur, sub, fed)
        subcode = bsOps.getSubCode(cur, sub)
        linetablename = subcode + "_" + fedcode + "_line"
        lineLayerName = self.dbase + ": " + sub + "-" + fed + "-line"
        layers = qgis.utils.iface.mapCanvas().layers()
        foundlayer = False

        uri = QgsDataSourceURI()
        uri.setConnection(self.hst, "5432", self.dbase, self.usr, self.paswrd)
        uri.setDataSource("esystems", linetablename, "geom")
        linelayer = QgsVectorLayer(uri.uri(), lineLayerName, "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(linelayer)
        self.refresh_layers()

    def addLayers(self):

        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()

        basicOps.substation = self.cmbSub.currentText()
        basicOps.feeder = self.cmbFed.currentText()
        #basicOps.dbasename = dbase
        subLayerName = self.dbase + ": " + sub + "-substation"
        lineLayerName = self.dbase + ": " + sub + "-" + fed + "-line"
        poleLayerName = self.dbase + ": " + sub + "-" + fed + "-pole"
        line = False
        pole = False
        subs = False
        layers = qgis.utils.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == subLayerName:
                subs = True
            if layer.name() == poleLayerName:
                pole = True
            if layer.name() == lineLayerName:
                line = True
        try:
            #self.addProLayer("pole")
            #self.addProLayer("line")
            #self.addProLayer("buffer")
            #self.addProLayer("structure")
            if not line:
                self.addLineLayer()
            else:
                QMessageBox.information(self.iface.mainWindow(),"Add Layers","{0} layer already exists!".format(lineLayerName))
            if not pole:
                self.addPoleLayer()
            else:
                QMessageBox.information(self.iface.mainWindow(),"Add Layers","{0} layer already exists!".format(poleLayerName))
            if not subs:
                self.addSubLayer()
            else:
                QMessageBox.information(self.iface.mainWindow(),"Add Layers","{0} layer already exists!".format(subLayerName))
        except EnvironmentError as e:
            QMessageBox.information(self.iface.mainWindow(),"Add Layers","Failed to add Layers!\n{0}".format(e))

    def removeAllLayers(self):
        QgsMapLayerRegistry.instance().removeAllMapLayers()

    def onClose(self):
        self.close()

    def openInitialize(self):
        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()

        self.close()

        intialize = frmInitialize_dialog(self.iface)
        intialize.txtPro.setText(self.usr)
        intialize.txtPBS.setText(self.dbase)
        intialize.exec_()

    def openProcess(self):
        sub = self.cmbSub.currentText()
        basicOps.substation = sub
        fed = self.cmbFed.currentText()
        basicOps.feeder = fed

        subLayerName = self.dbase + ": " + sub + "-substation"
        lineLayerName = self.dbase + ": " + sub + "-" + fed + "-line"
        poleLayerName = self.dbase + ": " + sub + "-" + fed + "-pole"
        line = False
        pole = False
        subs = False
        layers = qgis.utils.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == subLayerName:
                subs = True
            if layer.name() == poleLayerName:
                pole = True
            if layer.name() == lineLayerName:
                line = True
        if subs and pole and line:
            self.close()
            intialize = frmProcessFieldData_dialog(self.iface)
            intialize.txtPro.setText(self.usr)
            intialize.txtPBS.setText(self.dbase)
            intialize.txtSub.setText(basicOps.substation)
            intialize.txtFed.setText(basicOps.feeder)
            intialize.exec_()
        else:
            QMessageBox.information(self.iface.mainWindow(),"Open Data Processing Form","Layers not added, Please add Layers then try again!")

    def openValidate(self):
        proname = self.txtPro.text()
        sub = self.cmbSub.currentText()
        basicOps.substation = sub
        fed = self.cmbFed.currentText()
        basicOps.feeder = fed
        subLayerName = self.dbase + ": " + sub + "-substation"
        lineLayerName = self.dbase + ": " + sub + "-" + fed + "-line"
        poleLayerName = self.dbase + ": " + sub + "-" + fed + "-pole"
        line = False
        pole = False
        subs = False
        layers = qgis.utils.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == subLayerName:
                subs = True
            if layer.name() == poleLayerName:
                pole = True
            if layer.name() == lineLayerName:
                line = True
        if subs and pole and line:
            self.close()
            validate = frmValidate_dialog(self.iface)
            validate.txtPro.setText(proname)
            validate.txtPBS.setText(basicOps.dbasename)
            validate.txtSub.setText(sub)
            validate.txtFed.setText(fed)
            validate.exec_()
        else:
            QMessageBox.information(self.iface.mainWindow(),"Open Validation Form","Layers not added, Please add Layers then try again!")

    def openFinance(self):
        proname = self.txtPro.text()
        sub = self.cmbSub.currentText()
        fed = self.cmbFed.currentText()

        self.close()
        validate = frmFinance_dialog(self.iface)
        validate.txtPro.setText(proname)
        validate.txtPBS.setText(self.dbase)
        validate.txtSub.setText(sub)
        validate.txtFed.setText(sub)
        validate.exec_()
