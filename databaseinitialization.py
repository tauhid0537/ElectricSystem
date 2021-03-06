from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import csv
import sys
import os
import json

import ogr
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import psycopg2

import utility
from utility import *

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

        self.usr = basicOps.usrname
        self.dbase = basicOps.dbasename
        self.hst = basicOps.hostname
        self.paswrd = basicOps.password

        #self.cmdFolder.clicked.connect(self.createFolder)
        self.txtSub.textChanged.connect(self.subTextChanged)
        self.txtFed.textChanged.connect(self.fedTextChanged)
        self.cmdShapefile.clicked.connect(self.createSpatialTables)
        self.cmdDomain.clicked.connect(self.openDomainForm)
        self.cmdConductor.clicked.connect(self.openConductorForm)
        self.cmdClose.clicked.connect(self.onClose)

    def subTextChanged(self):
        subname = self.txtSub.text()
        subcode = subname[:3].lower()
        self.txtSubCode.setText(subcode)

    def fedTextChanged(self):
        fedname = self.txtFed.text()
        fedcode = fedname[:3].lower()
        self.txtFedCode.setText(fedcode)

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

        try:
            condb = psycopg2.connect(user = self.usr, host = self.hst, password = self.paswrd, dbname = self.dbase)
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n %s" %(e)))
        else:
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            curdb = condb.cursor()

            fedCheckSQL = "select * from sysinp.sys_feeder where substation = '%s' and feeder = '%s';" % (sub, fed)
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
                subgeomIndexSQL = """create index """+ subName + """_gix on esystems.""" + subName + """ using GIST(geom);"""
                subobjidIndexSQL = """create index """+ subName + """_objidix on esystems.""" + subName + """ using btree(objectid);"""
                subinsertSQL1 = "insert into sysinp.sys_substation (substation, sub_code) values('%s', '%s');" % (sub, subcode)
                try:
                    curdb.execute(subinsertSQL1)
                except psycopg2.Error as e:
                    QMessageBox.critical(self.iface.mainWindow(),"System Substation Table Data Insert Error",str("Unable to Create Substation!\n{0}").format(e))
                try:
                    curdb.execute("create sequence esystems."+subName+"_id_seq;")
                    curdb.execute(createsubSQL)
                    curdb.execute(subgeomIndexSQL)
                    curdb.execute(subobjidIndexSQL)

                except psycopg2.Error as e:
                    QMessageBox.critical(self.iface.mainWindow(),"Substation Table Creation Error",str("Unable to Create Substation!\n{0}").format(e))
            else:
                QMessageBox.critical(self.iface.mainWindow(),"Database initialization",str("Substation table already exists!\n{0}").format(subName))

            curdb.execute(fedpoleSQL)
            row1 = curdb.fetchone()
            if row1[0] is None:
                createFedPoleSQL = "create table esystems."+poleName + """(objectid integer PRIMARY KEY not null DEFAULT nextval('esystems.""" + poleName + """_id_seq'::regclass),
                    substation character varying(30) COLLATE pg_catalog."default",
                    feeder character varying(30) COLLATE pg_catalog."default",
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
                polegeomIndexSQL = """create index """+ poleName + """_gix on esystems.""" + poleName + """ using GIST(geom);"""
                poleobjidIndexSQL = """create index """+ poleName + """_objidix on esystems.""" + poleName + """ using btree(objectid);"""
                try:
                    curdb.execute("create sequence esystems."+poleName+"_id_seq;")
                    curdb.execute(createFedPoleSQL)
                    curdb.execute(polegeomIndexSQL)
                    curdb.execute(poleobjidIndexSQL)
                except psycopg2.Error as e:
                    QMessageBox.critical(self.iface.mainWindow(),"Pole Table Creation Error",str("Unable to Create Pole Table!\n{0}").format(e))
            else:
                QMessageBox.critical(self.iface.mainWindow(),"Database initialization",str("Pole table already exists!\n{0}").format(poleName))

            curdb.execute(fedlineSQL)
            row2 = curdb.fetchone()
            if row2[0] is None:
                createfedLineSQL = "create table esystems."+lineName + """(objectid integer PRIMARY KEY not null DEFAULT nextval('esystems.""" + lineName + """_id_seq'::regclass),
                    substation character varying(30) COLLATE pg_catalog."default",
                    feeder character varying(30) COLLATE pg_catalog."default",
                    line_align character varying(20) COLLATE pg_catalog."default",
                    line_voltage integer,
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
                linegeomIndexSQL = """create index """+ lineName + """_gix on esystems.""" + lineName + """ using GIST(geom);"""
                lineobjidIndexSQL = """create index """+ lineName + """_objidix on esystems.""" + lineName + """ using btree(objectid);"""
                try:
                    curdb.execute("create sequence esystems."+lineName+"_id_seq;")
                    curdb.execute(createfedLineSQL)
                    curdb.execute(linegeomIndexSQL)
                    curdb.execute(lineobjidIndexSQL)
                except psycopg2.Error as e:
                    QMessageBox.critical(self.iface.mainWindow(),"Line Table Creation Error",str("Unable to Create Line Table!\n{0}").format(e))
            else:
                QMessageBox.critical(self.iface.mainWindow(),"Database initialization",str("Line table already exists!\n{0}").format(lineName))
            try:
                    subCheckSQL = "select * from sysinp.sys_substation where substation = '%s';" % (sub)
                    curdb.execute(subCheckSQL)
                    if curdb.rowcount == 0:
                        subinsertSQL = "insert into sysinp.sys_substation (substation, sub_code) values('%s', '%s');" % (sub, subcode)
                        curdb.execute(subinsertSQL)
            except psycopg2.Error as e:
                QMessageBox.critical(self.iface.mainWindow(),"System Substation Table Insert Error",str("Unable to insert data into system substation table!\n{0}").format(e))
            try:
                    curdb.execute(fedCheckSQL)
                    if curdb.rowcount == 0:
                        fedinsertSQL ="insert into sysinp.sys_feeder (substation, feeder, fed_code) values('%s', '%s', '%s');" % (sub, fed, fedcode)
                        curdb.execute(fedinsertSQL)
            except psycopg2.Error as e:
                QMessageBox.critical(self.iface.mainWindow(),"System Feeder Table Insert Error",str("Unable to insert data into system feeder table!\n{0}").format(e))
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


