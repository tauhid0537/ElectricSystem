from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import csv
import sys
import os

import ogr
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import psycopg2

import test2

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Utilities")
import utilities


sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/DatabaseInitialization")
from frmInitialize import *
from frmDomain import *
from frmConductor import *
from IniDomain import *
from IniConductor import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
import resources

class frmInitialize_dialog(QDialog, Ui_frmIntialize):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        #self.cmdFolder.clicked.connect(self.createFolder)
        self.cmdShapefile.clicked.connect(self.createSpatialTables)
        self.cmdDomain.clicked.connect(self.openDomainForm)
        self.cmdConductor.clicked.connect(self.openConductorForm)
        self.cmdClose.clicked.connect(self.onClose)

    def getText1(self):
        floc = utilities.drvpath
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText(floc)
        ret = msgBox.exec_()

    def getText(self):


        usr = test2.basicOps.usrname
        QMessageBox.critical(self.iface.mainWindow(),"Connection Error",usr)

    def createSpatialTables(self):
        sub = self.txtSub.text()
        fed = self.txtFed.text()
        pbs = self.txtPBS.text()
        subcode = self.txtSubCode.text()
        fedcode = self.txtFedCode.text()

        subName = sub.lower()+ "_substation"
        poleName = subcode+"_"+fedcode+"_"+"pole"
        lineName = subcode+"_"+fedcode+"_"+"line"
        subTableSQL = "select to_regclass('esystems."+subName+"');"
        fedpoleSQL = "select to_regclass('esystems."+poleName+"');"
        fedlineSQL = "select to_regclass('esystems."+lineName+"');"
        usr = test2.basicOps.usrname
        hst = test2.basicOps.hostname
        paswrd = test2.basicOps.password
        db = test2.basicOps.dbasename

        try:
            condb = psycopg2.connect(user = usr, host = hst, password = paswrd, dbname = db)
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        else:
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            curdb = condb.cursor()
            curdb.execute(subTableSQL)
            row = curdb.fetchone()
            if row[0] is None:
                createsubSQL = "create table esystems."+subName + """(objectid integer PRIMARY KEY not null DEFAULT nextval('esystems.""" + subName + """_id_seq'::regclass),
                substation character varying(30) COLLATE pg_catalog."default",
                sub_code character varying(5) COLLATE pg_catalog."default",
                sub_type_cat character varying(30) COLLATE pg_catalog."default",
                sub_no_of_fed integer, sub_cap float, sub_trn_num integer,
                location character varying(30) COLLATE pg_catalog."default",
                remarks character varying(50) COLLATE pg_catalog."default",
                geom geometry(POINT, 3857)
                )
                """
                curdb.execute("create sequence esystems."+subName+"_id_seq;")
                curdb.execute(createsubSQL)
            else:
                QMessageBox.critical(self.iface.mainWindow(),"Database initialization",str("Substation table already exists!\n{0}").format(subName))

            curdb.execute(fedpoleSQL)
            row1 = curdb.fetchone()
            if row1[0] is None:
                createFedPoleSQL = "create table esystems."+poleName + """(objectid integer PRIMARY KEY not null DEFAULT nextval('esystems.""" + poleName + """_id_seq'::regclass),
                    substation character varying(30) COLLATE pg_catalog."default",
                    gps_no character varying(15) COLLATE pg_catalog."default",
                    fed_on_pole integer,
                    pole_number character varying(75) COLLATE pg_catalog."default",
                    pole_use character varying(30) COLLATE pg_catalog."default",
                    pole_phase character varying(5) COLLATE pg_catalog."default",
                    pole_height integer,
                    pole_class character varying(20) COLLATE pg_catalog."default",
                    pole_structure character varying(30) COLLATE pg_catalog."default",
                    pole_fitting character varying(10) COLLATE pg_catalog."default",
                    pole_guy character varying(5) COLLATE pg_catalog."default",
                    pole_guytype character varying(20) COLLATE pg_catalog."default",
                    pole_guyag character varying(20) COLLATE pg_catalog."default",
                    pole_status character varying(100) COLLATE pg_catalog."default",
                    equip_type character varying(30) COLLATE pg_catalog."default",
                    reference_pole character varying(75) COLLATE pg_catalog."default",
                    equip_id character varying(30) COLLATE pg_catalog."default",
                    equip_unit integer,
                    equip_mount character varying(30) COLLATE pg_catalog."default",
                    equip_size character varying(20) COLLATE pg_catalog."default",
                    equip_phase character varying(10) COLLATE pg_catalog."default",
                    equip_status character varying(20) COLLATE pg_catalog."default",
                    equip_use character varying(20) COLLATE pg_catalog."default",
                    trans_ref character varying(75) COLLATE pg_catalog."default",
                    rs_con float, sc_con float, lc_con float, si_con float, li_con float,
                    pb_con float, ag_con float, st_con float,
                    location character varying(30) COLLATE pg_catalog."default",
                    data_source character varying(30) COLLATE pg_catalog."default",
                    remarks character varying(50) COLLATE pg_catalog."default",
                    geom geometry(POINT, 3857)
                    )
                    """
                curdb.execute("create sequence esystems."+poleName+"_id_seq;")
                curdb.execute(createFedPoleSQL)
            else:
                QMessageBox.critical(self.iface.mainWindow(),"Database initialization",str("Pole table already exists!\n{0}").format(poleName))

            curdb.execute(fedlineSQL)
            row2 = curdb.fetchone()
            if row2[0] is None:
                createfedLineSQL = "create table esystems."+lineName + """(objectid integer PRIMARY KEY not null DEFAULT nextval('esystems.""" + lineName + """_id_seq'::regclass),
                    substation character varying(30) COLLATE pg_catalog."default",
                    feeder character varying(30) COLLATE pg_catalog."default",
                    line_align character varying(20) COLLATE pg_catalog."default",
                    line_vlotage integer,
                    line_type character varying(30) COLLATE pg_catalog."default",
                    section_id character varying(30) COLLATE pg_catalog."default",
                    phase character varying(5) COLLATE pg_catalog."default",
                    trans_code character varying(10) COLLATE pg_catalog."default",
                    sec_con character varying(20) COLLATE pg_catalog."default",
                    trans_ref character varying(75) COLLATE pg_catalog."default",
                    con_size_1 character varying(30) COLLATE pg_catalog."default",
                    con_size_2 character varying(30) COLLATE pg_catalog."default",
                    con_size_3 character varying(30) COLLATE pg_catalog."default",
                    con_size_n character varying(30) COLLATE pg_catalog."default",
                    line_status character varying(100) COLLATE pg_catalog."default",
                    data_source character varying(30) COLLATE pg_catalog."default",
                    remarks character varying(50) COLLATE pg_catalog."default",
                    geom geometry(LINESTRING, 3857)
                    )
                    """
                curdb.execute("create sequence esystems."+lineName+"_id_seq;")
                curdb.execute(createfedLineSQL)
            else:
                QMessageBox.critical(self.iface.mainWindow(),"Database initialization",str("Line table already exists!\n{0}").format(lineName))
            QMessageBox.information(self.iface.mainWindow(),"Database initialization","Tables Created")


    def onClose(self):
        self.close()

    def openDomainForm(self):
        self.close()
        domainform = frmDomain_dialog(self.iface)
        domainform.exec_()

    def openConductorForm(self):
        proname = self.txtPro.text()
        pbsname = self.txtPBS.text()
        subname = self.txtSub.text()
        fedname = self.txtFed.text()

        self.close()
        conductorform = frmConductor_dialog(self.iface)
        conductorform.txtPro.setText(proname)
        conductorform.txtPBS.setText(pbsname)
        conductorform.txtSub.setText(subname)
        conductorform.txtFed.setText(fedname)
        conductorform.loadTable()
        conductorform.exec_()


