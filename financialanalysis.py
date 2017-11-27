from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *
import qgis

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

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/FinancialAnalysis")
from frmFinance import *
from frmInputTable import *
from fininputtable import *

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
#import resources

class frmFinance_dialog(QDialog, Ui_frmFinance):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.proNum = None
        self.proName = None
        self.proSite = None
        self.proLineType = None
        self.proLineVol = None
        self.proPopSource = None
        self.proConSize = None
        self.proAvgLineLength = None

        self.usr = basicOps.usrname
        self.dbase = basicOps.dbasename
        self.hst = basicOps.hostname
        self.paswrd = basicOps.password
        self.sub = basicOps.substation
        self.fed = basicOps.feeder

        self.bufftablename = None
        self.linetablename = None
        self.poletablename = None
        self.structuretablename= None
        self.bufflayername = None
        self.linelayername = None
        self.polelayername = None
        self.structurelayername= None

        self.tblView = self.tableView
        self.tblModel = QtGui.QStandardItemModel(self)
        self.tblView.setModel(self.tblModel)

        self.getTableforModel()

        self.cmbProSite.clear()
        self.cmbProSite.addItem('Urban')
        self.cmbProSite.addItem('Rural')
        self.cmbProSite.setCurrentIndex(-1)

        self.cmbPrLineType.clear()
        self.cmbPrLineType.addItem('Primary Distribution')
        self.cmbPrLineType.addItem('Secondary Distribution')
        self.cmbPrLineType.setCurrentIndex(-1)

        self.cmbPrLineVolt.clear()
        self.cmbPrLineVolt.addItem('33000')
        self.cmbPrLineVolt.addItem('11000')
        self.cmbPrLineVolt.addItem('400')
        self.cmbPrLineVolt.setCurrentIndex(-1)

        self.cmbScConSize.clear()
        cur = self.getcursor()
        sql = "select size from sysinp.fin_construction_cost where type = 'Secondary Distribution'"
        cur.execute(sql)
        fedlist = []
        rows = cur.fetchall()
        for row in rows:
            fedlist.append(row[0])

        self.cmbScConSize.addItems(fedlist)
        self.cmbScConSize.setCurrentIndex(-1)

        self.cmdInputTable.clicked.connect(self.openInputTable)
        self.cmdCreatePro.clicked.connect(self.createProject)
        self.cmdAddPro.clicked.connect(self.addProLayers)
        self.cmdDelPro.clicked.connect(self.deleteSelectedTableRow)
        self.cmdClose.clicked.connect(self.onClose)


    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def onClose(self):
        self.close()

    def getTableinfo(self, tablename):

        sql = "select column_name from information_schema.columns where table_name ='%s'" %tablename
        cur = self.getcursor()
        cur.execute(sql)
        rows = cur.fetchall()
        text = []
        for row in rows:
            text.append(row[0])
        finaltext = ",".join(text)
        return finaltext

    def getConnection(self):
        condb = psycopg2.connect(user = self.usr, host = self.hst, password = self.paswrd, dbname = self.dbase)
        condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return condb

    def getcursor(self):
        con = self.getConnection()
        cur = con.cursor()
        return cur

    def splitTable(self, tbllayername):
        name = tbllayername.split('.')
        if name is True:
            return name[0], name[1]

    def getprojectTableinfo(self):

        sql = "select column_name from information_schema.columns where table_name ='fout_expansion_projects'"
        cur = self.getcursor()
        cur.execute(sql)
        rows = cur.fetchall()
        text = []
        i = -1
        for row in rows:
            i = i + 1
            if i > 0:
                text.append(row[0])
        finaltext = ",".join(text)
        return finaltext

    def getTableforModel(self):
        self.tblModel.clear()
        sql = "SELECT substation, feeder, project_number, project_name, household_source, line_type, line_voltage, household_type FROM exprojects.fout_expansion_projects"

        tabledb = self.getprojectTableinfo()
        self.tblModel.setHorizontalHeaderLabels(tabledb.split(","))
        cur = self.getcursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for t, row in enumerate(rows):
            for y, col in enumerate(row):
                txt = str(col)
                item = QStandardItem(txt)
                self.tblModel.setItem(t,y,item)

        self.tblView.setModel(self.tblModel)

    def createProject(self):
        self.proNum = self.txtProNum.text()
        extensionProject.ProjectNumber = self.proNum
        self.proName = self.txtProName.text()
        extensionProject.ProjectName = self.proName
        self.proSite = self.cmbProSite.currentText()
        extensionProject.HHSourceType = self.proSite
        self.proLineType = self.cmbPrLineType.currentText()
        extensionProject.LineType = self.proLineType
        self.proLineVol = self.cmbPrLineVolt.currentText()
        extensionProject.LineVoltage = int(self.proLineVol)
        if self.radSet.isChecked():
            self.proPopSource = 'settlement'
        elif self.radStr.isChecked():
            self.proPopSource = 'structure'
        elif self.radVil.isChecked():
            self.proPopSource = 'village'

        extensionProject.HHSourceType =  self.proPopSource

        self.proConSize = self.cmbScConSize.currentText()
        self.proAvgLineLength = self.txtAvgTrLen.text()

        sql = """ insert into exprojects.fout_expansion_projects (substation, feeder, project_number, project_name, household_source, line_type, line_voltage, household_type)
        values( '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s')""" %(basicOps.substation, basicOps.feeder, self.proNum, self.proName, self.proPopSource, self.proLineType, self.proLineVol, self.proSite)
        cur = self.getcursor()
        cur.execute(sql)

        self.createProjectTables(basicOps.substation, basicOps.feeder, self.proNum)

        self.addLayer(self.bufftablename, self.bufflayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.structuretablename, self.structurelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.linetablename, self.linelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.poletablename, self.polelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.refresh_layers()

        self.getTableforModel()

        QMessageBox.information(self.iface.mainWindow(),"Financial Analysis",'Project Tables Created')

    def createProjectTables(self, sub, fed, pro):

        cur = self.getcursor()
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)

        self.bufftablename = subcode + '_' + fedcode + '_buffer_project_' + pro
        self.bufflayername = self.dbase + ": " + sub + "-" + fed + "-buffer-project-" + pro
        extensionProject.BufferTableName = self.bufftablename

        self.linetablename = subcode + '_' + fedcode + '_line_project_' + pro
        self.linelayername = self.dbase + ": " + sub + "-" + fed + "-line-project-" + pro
        extensionProject.LineTableName = self.linetablename

        self.poletablename = subcode + '_' + fedcode + '_pole_project_' + pro
        self.polelayername = self.dbase + ": " + sub + "-" + fed + "-pole-project-" + pro
        extensionProject.PoleTableName = self.poletablename

        if self.proPopSource == 'structure':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_structure_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-buffer-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename
        elif self.proPopSource == 'village':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_village_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-village-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename
        elif self.proPopSource == 'settlement':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_settlement_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-settlement-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename

        seqbuffsql = "create sequence exprojects."+self.bufftablename+"_seq;"
        buffsql = """CREATE TABLE exprojects."""+self.bufftablename+"""
        (
          objecid integer NOT NULL DEFAULT nextval('exprojects."""+self.bufftablename+"""_seq'::regclass),
          project_no character varying(30),
          buff_dist integer,
          geom geometry(Polygon,3857),
          equip_id character varying(30)
        )
        """

        cur.execute(seqbuffsql)
        cur.execute(buffsql)

        seqlinesql = "create sequence exprojects."+self.linetablename+"_seq;"
        linesql = """CREATE TABLE exprojects."""+self.linetablename+"""
        (
          objectid integer NOT NULL DEFAULT nextval('exprojects."""+self.linetablename+"""_seq'::regclass),
          substation character varying(30),
          feeder character varying(30),
          line_align character varying(20),
          line_voltage integer,
          line_type character varying(30),
          section_id character varying(30),
          phase character varying(5),
          trans_code character varying(10),
          sec_con character varying(20),
          trans_ref character varying(75),
          con_size_1 character varying(30),
          con_size_2 character varying(30),
          con_size_3 character varying(30),
          con_size_n character varying(30),
          line_status character varying(100),
          data_source character varying(30),
          remarks character varying(50),
          geom geometry(LineString,3857)
        )
        """
        cur.execute(seqlinesql)
        cur.execute(linesql)

        seqpolesql = "create sequence exprojects."+self.poletablename+"_seq;"
        polesql = """CREATE TABLE exprojects."""+self.poletablename+"""
        (
          objectid integer NOT NULL DEFAULT nextval('exprojects."""+self.poletablename+"""_seq'::regclass),
          substation character varying(30),
          feeder character varying(30),
          gps_no character varying(15),
          fed_on_pole integer,
          pole_number character varying(75),
          pole_use character varying(30),
          pole_phase character varying(5),
          pole_height integer,
          pole_class character varying(20),
          pole_structure character varying(30),
          pole_fitting character varying(10),
          pole_guy character varying(5),
          pole_guytype character varying(20),
          pole_guyag character varying(20),
          pole_status character varying(100),
          equip_type character varying(30),
          reference_pole character varying(75),
          equip_id character varying(30),
          equip_unit integer,
          equip_mount character varying(30),
          equip_size character varying(20),
          equip_phase character varying(10),
          equip_status character varying(20),
          equip_use character varying(20),
          trans_ref character varying(75),
          rs_con double precision,
          sc_con double precision,
          lc_con double precision,
          si_con double precision,
          li_con double precision,
          pb_con double precision,
          ag_con double precision,
          st_con double precision,
          location character varying(30),
          data_source character varying(30),
          remarks character varying(50),
          geom geometry(Point,3857)
        )
        """
        cur.execute(seqpolesql)
        cur.execute(polesql)

        #seqstrucsql = 'create sequence exprojects.%s'+'_seq;' %structuretablename
        structuresql = None
        if self.proPopSource == 'structure':
            structuresql = """CREATE TABLE exprojects."""+self.structuretablename+"""
            (
              gid serial NOT NULL,
              household numeric,
              structure numeric,
              geom geometry(Point,3857)
            )
            """
        else:
            structuresql = """CREATE TABLE exprojects."""+self.structuretablename+"""
            (
              gid serial NOT NULL,
              household numeric,
              structure numeric,
              geom geometry(POLYGON,3857)
            )
            """

        cur.execute(structuresql)

    def deleteProjectTables(self, sub, fed, pro):

        conn = self.getConnection()
        cur = conn.cursor()

        buffsql = 'drop table exprojects.%s' %(self.bufftablename)
        linesql = 'drop table exprojects.%s' %(self.linetablename)
        polesql = 'drop table exprojects.%s' %(self.poletablename)
        strucsql = 'drop table exprojects.%s' %(self.structuretablename)
        buffseqsql = 'drop sequence exprojects.%s_seq' %(self.bufftablename)
        lineseqsql = 'drop sequence exprojects.%s_seq' %(self.linetablename)
        poleseqsql = 'drop sequence exprojects.%s_seq' %(self.poletablename)
        strucseqsql = 'drop sequence exprojects.%s_seq' %(self.structuretablename)

        cur.execute(buffsql)
        cur.execute(linesql)
        cur.execute(polesql)
        cur.execute(strucsql)
        cur.execute(buffseqsql)
        cur.execute(lineseqsql)
        cur.execute(strucseqsql)
        conn.commit()

    def deleteSelectedTableRow(self):
        index = self.tblView.selectionModel().currentIndex().row()
        subIndex = self.tblView.selectedIndexes()[0]
        fedIndex = self.tblView.selectedIndexes()[1]
        proIndex = self.tblView.selectedIndexes()[2]
        sub = self.tableView.model().data(subIndex)
        fed =self.tableView.model().data(fedIndex)
        pro = self.tableView.model().data(proIndex)
        sql = "delete from exprojects.fout_expansion_projects where substation = '%s' and feeder = '%s' and project_number = '%s'" %(sub, fed, pro)
        cur = self.getcursor()

        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)

        self.bufftablename = subcode + '_' + fedcode + '_buffer_project_' + pro
        self.linetablename = subcode + '_' + fedcode + '_line_project_' + pro
        self.poletablename = subcode + '_' + fedcode + '_pole_project_' + pro
        if self.proPopSource == 'structure':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_structure_project_' + pro
        elif self.proPopSource == 'village':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_village_project_' + pro
        elif self.proPopSource == 'settlement':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_settlement_project_' + pro

        cur.execute(sql)
        self.deleteProjectTables(sub, fed, pro)

        QMessageBox.information(self.iface.mainWindow(),"Financial Analysis",'Project Number %s for Substation %s, Feeder %s is deleted from project table.' %(pro, sub, fed))
        self.getTableforModel()

    def addProLayers(self):
        index = self.tblView.selectionModel().currentIndex().row()
        subIndex = self.tblView.selectedIndexes()[0]
        fedIndex = self.tblView.selectedIndexes()[1]
        proIndex = self.tblView.selectedIndexes()[2]
        pronameIdx = self.tblView.selectedIndexes()[3]
        strIndex = self.tblView.selectedIndexes()[4]
        linetypIdx = self.tblView.selectedIndexes()[5]
        linevolIdx = self.tblView.selectedIndexes()[6]
        hhtypeIdx = self.tblView.selectedIndexes()[7]

        structure = self.tableView.model().data(strIndex)
        self.proPopSource = structure
        extensionProject.HouseholdSource = structure

        sub = self.tableView.model().data(subIndex)
        fed =self.tableView.model().data(fedIndex)
        pro = self.tableView.model().data(proIndex)
        extensionProject.ProjectNumber = pro

        proname = self.tableView.model().data(pronameIdx)
        extensionProject.ProjectName = proname

        linetype = self.tableView.model().data(linetypIdx)
        extensionProject.LineType = linetype

        linevol = self.tableView.model().data(linevolIdx)
        extensionProject.LineVoltage = int(linevol)

        hhtype = self.tableView.model().data(hhtypeIdx)
        extensionProject.HHSourceType = hhtype



        cur = self.getcursor()
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)

        self.poletablename = subcode + "_" + fedcode + "_pole_project_"+pro
        self.polelayername = self.dbase + ": " + sub + "-" + fed + "-pole-project-" + pro
        extensionProject.PoleTableName = self.poletablename

        self.linetablename = subcode + "_" + fedcode + "_line_project_"+pro
        self.linelayername = self.dbase + ": " + sub + "-" + fed + "-line-project-" + pro
        extensionProject.LineTableName = self.linetablename

        self.bufftablename = subcode + "_" + fedcode + "_buffer_project_" + pro
        self.bufflayername = self.dbase + ": " + sub + "-" + fed + "-buffer-project-" + pro
        extensionProject.BufferTableName = self.bufftablename

        if self.proPopSource == 'structure':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_structure_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-buffer-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename
        elif self.proPopSource == 'village':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_village_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-village-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename
        elif self.proPopSource == 'settlement':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_settlement_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-settlement-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename

        self.addLayer(self.bufftablename, self.bufflayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.structuretablename, self.structurelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.linetablename, self.linelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.poletablename, self.polelayername, self.hst, self.dbase, self.usr, self.paswrd)

        self.refresh_layers()


    def removelayer(self, layername):
        layers = qgis.utils.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == layername:
                QgsMapLayerRegistry.instance().removeMapLayer( layer.id() )

    def addLayer(self, tablename, layername, hst, dbase, usr, paswrd):
        layers = qgis.utils.iface.mapCanvas().layers()
        foundlayer = False
        for layer in layers:
            if layer.name() == layername:
                foundlayer = True
        if not foundlayer:
            uri = QgsDataSourceURI()
            uri.setConnection(hst, "5432", dbase, usr, paswrd)
            uri.setDataSource("exprojects",tablename,"geom")
            polelayer = QgsVectorLayer(uri.uri(), layername, "postgres")
            QgsMapLayerRegistry.instance().addMapLayer(polelayer)
        else:
            QMessageBox.information(self.iface.mainWindow(),"Add Project Layers","{0} layer already exists!".format(layername))

    def refresh_layers(self):
        for layer in qgis.utils.iface.mapCanvas().layers():
            layer.triggerRepaint()

    def openInputTable(self):
        proname = self.txtPro.text()

        self.close()
        gpsForm = frmInputTable_dialog(self.iface)
        gpsForm.txtPro.setText(proname)
        gpsForm.txtPBS.setText(basicOps.dbasename)
        gpsForm.txtSub.setText(basicOps.substation)
        gpsForm.txtFed.setText(basicOps.feeder)
        gpsForm.exec_()

