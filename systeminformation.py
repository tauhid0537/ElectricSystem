# -*- coding: utf-8 -*-
#import sip
#sip.setapi('QString', 2)
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import ogr
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import psycopg2
import sqlite3

import csv
import sys
import os
import utility
from utility import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/SystemInformation")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/MainForm")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")

from frmSystemInfo import *
from mainform import *
import resources

#class sqlConnection():

    #con = None
    #con = psycopg2.connect(user = 'postgres', host = 'localhost', password = 'ku940405')

class frmSystemInfo_dialog(QDialog, Ui_frmSysInfo):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['Database Name'])
        self.tableView = self.dataSysInfo
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.cmdClose.clicked.connect(self.onClose)
        self.cmdGetDatabase.clicked.connect(self.getDb)
        self.cmdCreateDatabase.clicked.connect(self.createDb)
        self.cmdUseDatabase.clicked.connect(self.useDb)
        self.txtHost.setText('localhost')
        self.txtUserName.setText('postgres')
        self.txtPassword.setText('postgres')

    def onClose(self):
        self.close()

    def getDb(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Database Name'])
        hostname = self.txtHost.text()
        username = self.txtUserName.text()
        password = self.txtPassword.text()
        try:
            con = psycopg2.connect(user = username, host = hostname, password = password)
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        else:
            cur = con.cursor()
            cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
            for db in cur.fetchall():
                row = []
                item = QStandardItem(db[0])
                row.append(item)
                self.model.appendRow(row)
            cur.close()
            con.close()

    def createDb(self):
        hostname = self.txtHost.text()
        utility.hostname = hostname
        username = self.txtUserName.text()
        utility.usrname = username
        password = self.txtPassword.text()
        utility.password = password
        dbasename = self.txtDatabase.text()
        utility.dbasename = dbasename
        phaseconf = str(self.cmbSysPhase.currentText())
        try:
            con1 = psycopg2.connect(user = username, host = hostname, password = password)
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        else:
            con1.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur1 = con1.cursor()
            cur1.execute('CREATE DATABASE ' + dbasename)
            con1.commit()
            cur1.close()
            con1.close()
        try:
            condb = psycopg2.connect(user = username, host = hostname, password = password, dbname = dbasename)
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        else:
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            curdb = condb.cursor()
            curdb.execute('CREATE EXTENSION postgis;')
            curdb.execute('CREATE EXTENSION pgrouting;')
            curdb.execute('CREATE SCHEMA sysinp;')
            curdb.execute('CREATE SCHEMA esystems;')
            curdb.execute('CREATE SCHEMA exprojects;')
            curdb.execute('CREATE SCHEMA landbase;')
            curdb.execute('CREATE SEQUENCE sysinp.sys_substation_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.sys_feeder_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.conductor_table_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.phase_con_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.domain_id_seq;')
            createsubtab = """CREATE TABLE sysinp.sys_substation
            (id integer PRIMARY KEY not null DEFAULT nextval('sysinp.sys_substation_id_seq'::regclass),
            substation character varying(30) COLLATE pg_catalog."default",
            sub_asset_id character varying(30) COLLATE pg_catalog."default",
            sub_code character varying(5) COLLATE pg_catalog."default",
            sub_loc character varying(30) COLLATE pg_catalog."default",
            sub_serv_date date, sub_x float, sub_y float, sub_trn_num integer,
            sub_cap float,
            sub_type_cat character varying(30) COLLATE pg_catalog."default",
            sub_rem character varying(100) COLLATE pg_catalog."default",
            sub_con character varying(20) COLLATE pg_catalog."default",
            sub_lg float, sub_ll float, sub_bus_v float,
            sub_reg character varying(5) COLLATE pg_catalog."default",
            sub_min_imp float, sub_max_imp float, sub_ovr_imp float,
            sub_und_imp float,
            sub_note character varying(50) COLLATE pg_catalog."default",
            sub_lst_bld date, sub_lst_udt date);"""
            curdb.execute(createsubtab)

            createfedtab = """CREATE TABLE sysinp.sys_feeder
            (id integer PRIMARY KEY not null DEFAULT nextval('sysinp.sys_feeder_id_seq'::regclass),
            substation character varying(30) COLLATE pg_catalog."default",
            feeder character varying(30) COLLATE pg_catalog."default",
            fed_code character varying(5) COLLATE pg_catalog."default",
            fed_length float, fed_nom_v float, fed_bus_v float, fed_flt_res float,
            fed_con character varying(20) COLLATE pg_catalog."default",
            fed_desc character varying(50) COLLATE pg_catalog."default",
            fed_rs1 float, fed_rs2 float, fed_rs3 float, fed_rst float,
            fed_sc1 float, fed_sc2 float, fed_sc3 float, fed_sct float,
            fed_lc1 float, fed_lc2 float, fed_lc3 float, fed_lct float,
            fed_si1 float, fed_si2 float, fed_si3 float, fed_sit float,
            fed_li1 float, fed_li2 float, fed_li3 float, fed_lit float,
            fed_pb1 float, fed_pb2 float, fed_pb3 float, fed_pbt float,
            fed_ag1 float, fed_ag2 float, fed_ag3 float, fed_agt float,
            fed_st1 float, fed_st2 float, fed_st3 float, fed_stt float,
            fed_rsc float, fed_scc float, fed_lcc float, fed_sic float,
            fed_lic float, fed_pbc float, fed_agc float, fed_stc float,
            fed_con1 float, fed_con2 float, fed_con3 float, fed_cont float,
            fed_kva1 float, fed_kva2 float, fed_kva3 float, fed_kvat float,
            fed_kwh1 float, fed_kwh2 float, fed_kwh3 float, fed_kwht float,
            fed_kw1 float, fed_kw2 float, fed_kw3 float, fed_kwt float,
            fed_kvar1 float, fed_kvar2 float, fed_kvar3 float, fed_kvart float,
            fed_amps1 float, fed_amps2 float, fed_amps3 float, fed_ampst float,
            fed_pf1 float, fed_pf2 float, fed_pf3 float, fed_pft float,
            fed_lst_bld date, fed_lst_udt date);"""
            curdb.execute(createfedtab)

            createcontab = """CREATE TABLE sysinp.conductor_table
            (id integer PRIMARY KEY not null DEFAULT nextval('sysinp.conductor_table_id_seq'::regclass),
            name character varying(30) COLLATE pg_catalog."default",
            construc character varying(50) COLLATE pg_catalog."default",
            strand character varying(20) COLLATE pg_catalog."default",
            dia_mm float, area_mm2 float, r_km float, gmr_m float,
            x_50_km float, x_60_km float, max_amps float);"""
            curdb.execute(createcontab)

            createphstab = """CREATE TABLE sysinp.phase_con
            (id integer PRIMARY KEY not null DEFAULT nextval('sysinp.phase_con_id_seq'::regclass),
            sysphase character varying(10) COLLATE pg_catalog."default");"""
            curdb.execute(createphstab)

            sql2 = """INSERT INTO sysinp.phase_con(sysphase)
            VALUES('"""+phaseconf+ """');"""
            curdb.execute(sql2)

            createdomtab = """CREATE TABLE sysinp.domain
            (id integer PRIMARY KEY not null DEFAULT nextval('sysinp.domain_id_seq'::regclass),
            name character varying(50) COLLATE pg_catalog."default",
            descrp character varying(100) COLLATE pg_catalog."default");"""
            curdb.execute(createdomtab)

            fname = os.path.dirname(__file__) + "/Resources/Domains/Domains.txt"

            with open(fname, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    sql = "INSERT INTO sysinp.domain(name, descrp) VALUES ('%s', '%s');" % (row[0], row[1])
                    curdb.execute(sql)

            domainsql = "select name, descrp from sysinp.domain;"
            curdb.execute(domainsql)
            rows = curdb.fetchall()

            for row in rows:
                tableName = row[0]
                fileName = os.path.dirname(__file__) + "/Resources/Domains/" + tableName + ".txt"
                if os.path.exists(fileName):
                    curdb.execute("""create table  sysinp.""" + tableName + """
                    (code character varying(30) COLLATE pg_catalog."default",
                    value character varying(30) COLLATE pg_catalog."default"
                    );""" )
                    with open(fileName, 'r') as f2:
                        reader2 = csv.reader(f2)
                        i = 0
                        for r in reader2:
                            i = i +1
                            if i > 4:
                                domInsertSQL = "insert into sysinp." + tableName + "(code,value) values ('%s', '%s');" % (r[0], r[1])

                                curdb.execute(domInsertSQL)
            condb.commit()
            curdb.close()
            condb.close()

            QMessageBox.information(self.iface.mainWindow(),"Create Database","Database Created Successfully")


    def useDb(self):
        index = self.tableView.selectedIndexes()[0]
        dbname = self.tableView.model().data(index)

        hostname = self.txtHost.text()
        basicOps.hostname = hostname
        password = self.txtPassword.text()
        basicOps.password = password
        #dbasename = self.txtDatabase.text()
        basicOps.dbasename = dbname


        username = self.txtUserName.text()
        #Global.usrname = username
        basicOps.usrname = username
        pbsname = dbname
        self.close()

        sysinfo = frmMain_dialog(self.iface)
        gbops = utility.basicOps()

        sublist = gbops.getSubList(username, hostname, password, dbname)
        #fedlist = gbops.getFeederList(username, hostname, password, dbname)
        sysinfo.cmbSub.clear()
        #sysinfo.cmbFed.clear()
        sysinfo.cmbSub.addItems(sublist)
        sysinfo.cmbSub.setCurrentIndex(-1)
        #self.cmbFed.addItems(fedlist)

        sysinfo.txtPro.setText(self.txtUserName.text())
        sysinfo.txtDatabase.setText(dbname)
        sysinfo.exec_()

