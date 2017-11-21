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
import json
import contextlib

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
            curdb.execute('CREATE SEQUENCE sysinp.cashflowpara_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.finaddrev_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.fin_construction_cost_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.fincontar_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.findistloss_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.finexpense_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.finhh_id_seq;')
            curdb.execute('CREATE SEQUENCE sysinp.finsub_id_seq;')
            curdb.execute('CREATE SEQUENCE exprojects.seq;')
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

            cashflowparatab = """CREATE TABLE IF NOT EXISTS sysinp.fin_cashflow_parameters (
            objectid integer PRIMARY KEY not null DEFAULT nextval('sysinp.cashflowpara_id_seq'),
            category varchar(100), unit varchar(30), value double precision);"""
            curdb.execute(cashflowparatab)

            finaddrevtab = """CREATE TABLE IF NOT EXISTS sysinp.fin_additional_revenue (
            id integer PRIMARY KEY not null DEFAULT nextval('sysinp.finaddrev_id_seq'),
            category varchar(50), unit varchar(50), value double precision);"""
            curdb.execute(finaddrevtab)

            finconcosttab ="""CREATE TABLE IF NOT EXISTS sysinp.fin_construction_cost (
            id integer PRIMARY KEY not null DEFAULT nextval('sysinp.fin_construction_cost_id_seq'),
            item varchar(50), type varchar(50), category varchar(50), category_alias varchar(100),
            voltage double precision, size varchar(30), rate double precision, unit varchar(30));"""
            curdb.execute(finconcosttab)

            fincontartab = """CREATE TABLE IF NOT EXISTS sysinp.fin_consumer_tariff (
            objectid BIGINT PRIMARY KEY DEFAULT nextval('sysinp.fincontar_id_seq'),
            consumer varchar(50), ini_penetration double precision,
            mid_penetration double precision, fin_penetration double precision, mid_consumer_gr double precision, fin_consumer_gr double precision,
            ini_consumption double precision, mid_consumption_gr double precision, fin_consumption_gr double precision, connnect_charge double precision,
            fixed_charge double precision, energy_charge double precision, ratio double precision);"""
            curdb.execute(fincontartab)

            findistlosstab = """CREATE TABLE IF NOT EXISTS sysinp.fin_distribution_loss (
            id integer PRIMARY KEY not null DEFAULT nextval('sysinp.findistloss_id_seq'),
            region varchar(12), technical double precision, collection double precision);"""
            curdb.execute(findistlosstab)

            finexpensetab = """CREATE TABLE IF NOT EXISTS sysinp.fin_expense (
            id integer PRIMARY KEY DEFAULT nextval('sysinp.finexpense_id_seq'),
            category varchar(50), unit varchar(50), value double precision);"""
            curdb.execute(finexpensetab)

            finhhtab = """CREATE TABLE IF NOT EXISTS sysinp.fin_households (
            id integer PRIMARY KEY not null DEFAULT nextval('sysinp.finhh_id_seq'),
            item varchar(50), percentage double precision);"""
            curdb.execute(finhhtab)

            finsubsidytab = """CREATE TABLE IF NOT EXISTS sysinp.fin_subsidy(
            id integer PRIMARY KEY not null DEFAULT nextval('sysinp.finsub_id_seq'),
            type varchar(50), unit varchar(50), value double precision);"""
            curdb.execute(finsubsidytab)

            finexpprotab = """CREATE TABLE IF NOT EXISTS exprojects.fout_expansion_projects(
            id integer PRIMARY KEY not null DEFAULT nextval('exprojects.seq'),
            substation varchar(30), feeder varchar(30), project_number varchar(50), project_name varchar(250),
            household_source varchar(30), line_type varchar(30), line_voltage double precision, household_type varchar(30));"""
            curdb.execute(finexpprotab)

            finoutconcosttab = """CREATE TABLE IF NOT EXISTS exprojects.fout_construction_cost(
            id integer PRIMARY KEY not null DEFAULT nextval('exprojects.seq'),
            separator varchar(50), item varchar(100), type varchar(100), details varchar(250),
            quantity double precision, quantity_unit varchar(10), amount double precision, amount_unit varchar(30));"""
            curdb.execute(finoutconcosttab)

            finconsfintab = """CREATE TABLE IF NOT EXISTS exprojects.fout_consumer_finance(
            id integer PRIMARY KEY not null DEFAULT nextval('exprojects.seq'),
            item varchar(100), unit varchar(50), year0 double precision, year1 double precision,
            year2 double precision, year3 double precision, year4 double precision, year5 double precision,
            year6 double precision, year7 double precision, year8 double precision, year9 double precision,
            year10 double precision);"""
            curdb.execute(finconsfintab)

            finprosummtab = """CREATE TABLE IF NOT EXISTS exprojects.fout_project_summery(
            objectid integer PRIMARY KEY DEFAULT nextval('exprojects.seq'),
            item varchar(100), unit varchar(50), year1 double precision, year2 double precision,
            year3 double precision, year4 double precision, year5 double precision, year6 double precision,
            year7 double precision, year8 double precision, year9 double precision, year10 double precision);"""
            curdb.execute(finprosummtab)
            curdb.execute('''INSERT INTO sysinp.fin_additional_revenue(category, unit, value) VALUES ('Non Electric Revenue', 'Percentage of Total Revenue', 12);''')
            curdb.execute('''INSERT INTO sysinp.fin_cashflow_parameters(category, unit, value) VALUES ('Analysis Term', 'Year', 10);''')
            curdb.execute('''INSERT INTO sysinp.fin_cashflow_parameters(category, unit, value) VALUES ('Analysis Term', 'Year', 10);''')
            curdb.execute('''INSERT INTO sysinp.fin_cashflow_parameters(category, unit, value) VALUES ('Analysis Mid Term', 'Year', 5);''')
            curdb.execute('''INSERT INTO sysinp.fin_cashflow_parameters(category, unit, value) VALUES ('Analysis Payment Year', 'Year', 5);''')
            curdb.execute('''INSERT INTO sysinp.fin_cashflow_parameters(category, unit, value) VALUES ('DDiscount Rate', 'Percentage', 10);''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Electric Line','Primary Distribution','Three Phase',33000,'200 mm ACSR',31258,'USD Per kM');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Electric Line','Primary Distribution','Three Phase',33000,'150 mm ACSR',27597,'USD Per kM');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Electric Line','Primary Distribution','Three Phase',33000,'100 mm ACSR',23936,'USD Per kM');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Electric Line','Primary Distribution','Three Phase',33000,'50 mm ACSR',20275,'USD Per kM');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Electric Line','Primary Distribution','Three Phase',11000,'100 mm ACSR',20927,'USD Per kM');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Electric Line','Primary Distribution','Three Phase',11000,'50 mm ACSR',17266,'USD Per kM');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Electric Line','Secondary Distribution','Three Phase',400,'100 mm AAC',16625,'USD Per kM');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Electric Line','Secondary Distribution','Three Phase',400,'50 mm AAC',13578,'USD Per kM');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Electric Line','Secondary Distribution','Three Phase',240,NULL,248,'USD Per Consumer');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',33000,'315',20366,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',33000,'200',16989,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',33000,'100',11955,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',33000,'50',10692,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',33000,'25',10556,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',11000,'315',19714,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',11000,'200',14646,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',11000,'100',10186,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',11000,'50',8176,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,voltage,size,rate,unit) VALUES ('Equipment','Transformer','Three Phase',11000,'25',7573,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,rate,unit) VALUES ('Consumer','Service Drop','RS_Con','Residential',0,255,'USD Per Consumer');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,rate,unit) VALUES ('Consumer','Service Drop','SC_Con','Small Commercial',0,255,'USD Per Consumer');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,rate,unit) VALUES ('Consumer','Service Drop','LC_Con','Large Commercial',0,0,'USD Per Consumer');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,rate,unit) VALUES ('Consumer','Service Drop','SI_Con','Small Industrial',0,512,'USD Per Consumer');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,rate,unit) VALUES ('Consumer','Service Drop','LI_Con','Large Industrial',0,0,'USD Per Consumer');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,rate,unit) VALUES ('Consumer','Service Drop','PB_Con','Public Building',0,0,'USD Per Consumer');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,rate,unit) VALUES ('Consumer','Service Drop','AG_Con','Agricultural',0,0,'USD Per Consumer');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,rate,unit) VALUES ('Consumer','Service Drop','ST_Con','Street Light',0,0,'USD Per Consumer');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,size,rate,unit) VALUES ('Equipment','Breaker','Three Phase','BRK',11000,'250Amps',20366,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,size,rate,unit) VALUES ('Equipment','Capacitor','Three Phase','CAP',11000,'320 kVAR',21300,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,size,rate,unit) VALUES ('Equipment','Fuse','Three Phase','FUS',11000,'300 Amps',25300,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,size,rate,unit) VALUES ('Equipment','Recloser','Three Phase','REC',11000,'400 Amps',12500,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,size,rate,unit) VALUES ('Equipment','Sectionalizer','Three Phase','SEC',11000,'250 Amps',32500,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,size,rate,unit) VALUES ('Equipment','Switch','Three Phase','SWC',11000,'360 Amps',12500,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,size,rate,unit) VALUES ('Equipment','Regulator','Three Phase','REG',11000,'400 kVA',45200,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,size,rate,unit) VALUES ('Equipment','Step Up Transformer','Three Phase','SUT',11000,'2000 kVA',36200,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_construction_cost(item,type,category,category_alias,voltage,size,rate,unit) VALUES ('Equipment','Step Down Transformer','Three Phase','SDT',11000,'1000 kVA',24500,'USD Per Unit');''')
            curdb.execute('''INSERT INTO sysinp.fin_consumer_tariff(consumer,ini_penetration,mid_penetration,fin_penetration,mid_consumer_gr,fin_consumer_gr,ini_consumption,mid_consumption_gr,fin_consumption_gr,connnect_charge,fixed_charge,energy_charge,ratio) VALUES ('RS_Con',40,60,80,12.5,7.7,50,5,3,99.28,3.29,0.056,84.1);''')
            curdb.execute('''INSERT INTO sysinp.fin_consumer_tariff(consumer,ini_penetration,mid_penetration,fin_penetration,mid_consumer_gr,fin_consumer_gr,ini_consumption,mid_consumption_gr,fin_consumption_gr,connnect_charge,fixed_charge,energy_charge,ratio) VALUES ('SC_Con',40,60,80,12.5,7.7,160,5,3,99.28,5.26,0.17,8);''')
            curdb.execute('''INSERT INTO sysinp.fin_consumer_tariff(consumer,ini_penetration,mid_penetration,fin_penetration,mid_consumer_gr,fin_consumer_gr,ini_consumption,mid_consumption_gr,fin_consumption_gr,connnect_charge,fixed_charge,energy_charge,ratio) VALUES ('LC_Con',40,60,80,12.5,7.7,400,5,3,250.24,15.25,0.18,0.15);''')
            curdb.execute('''INSERT INTO sysinp.fin_consumer_tariff(consumer,ini_penetration,mid_penetration,fin_penetration,mid_consumer_gr,fin_consumer_gr,ini_consumption,mid_consumption_gr,fin_consumption_gr,connnect_charge,fixed_charge,energy_charge,ratio) VALUES ('SI_Con',40,60,80,12.5,7.7,150,5,3,125.56,10.25,0.17,3);''')
            curdb.execute('''INSERT INTO sysinp.fin_consumer_tariff(consumer,ini_penetration,mid_penetration,fin_penetration,mid_consumer_gr,fin_consumer_gr,ini_consumption,mid_consumption_gr,fin_consumption_gr,connnect_charge,fixed_charge,energy_charge,ratio) VALUES ('LI_Con',40,60,80,12.5,7.7,800,5,3,625.35,92.75,0.15,0.15);''')
            curdb.execute('''INSERT INTO sysinp.fin_consumer_tariff(consumer,ini_penetration,mid_penetration,fin_penetration,mid_consumer_gr,fin_consumer_gr,ini_consumption,mid_consumption_gr,fin_consumption_gr,connnect_charge,fixed_charge,energy_charge,ratio) VALUES ('PB_Con',40,60,80,12.5,7.7,120,5,3,99.28,3.29,0.068,0.5);''')
            curdb.execute('''INSERT INTO sysinp.fin_consumer_tariff(consumer,ini_penetration,mid_penetration,fin_penetration,mid_consumer_gr,fin_consumer_gr,ini_consumption,mid_consumption_gr,fin_consumption_gr,connnect_charge,fixed_charge,energy_charge,ratio) VALUES ('AG_Con',40,60,80,12.5,7.7,150,5,3,125.56,10.25,0.088,3.1);''')
            curdb.execute('''INSERT INTO sysinp.fin_consumer_tariff(consumer,ini_penetration,mid_penetration,fin_penetration,mid_consumer_gr,fin_consumer_gr,ini_consumption,mid_consumption_gr,fin_consumption_gr,connnect_charge,fixed_charge,energy_charge,ratio) VALUES ('ST_Con',40,60,80,12.5,7.7,80,5,3,99.28,3.29,0.056,1);''')
            curdb.execute('''INSERT INTO sysinp.fin_distribution_loss(region, technical, collection) VALUES ('Urban', 8, 100);''')
            curdb.execute('''INSERT INTO sysinp.fin_distribution_loss(region, technical, collection) VALUES ('Rural', 8, 100);''')
            curdb.execute('''INSERT INTO sysinp.fin_expense(category,unit,value) VALUES ('Power Cost','Per kWH',0.134178250865);''')
            curdb.execute('''INSERT INTO sysinp.fin_expense(category,unit,value) VALUES ('O & M','Per Consumer',75.0616502515);''')
            curdb.execute('''INSERT INTO sysinp.fin_expense(category,unit,value) VALUES ('A & G','Per Consumer',70);''')
            curdb.execute('''INSERT INTO sysinp.fin_expense(category,unit,value) VALUES ('Commercial','Per Consumer',20);''')
            curdb.execute('''INSERT INTO sysinp.fin_expense(category,unit,value) VALUES ('Depreciation','Percentage of Construction Cost',3.0838987);''')
            curdb.execute('''INSERT INTO sysinp.fin_expense(category,unit,value) VALUES ('Interest','Percentage of Construction Cost',3);''')
            curdb.execute('''INSERT INTO sysinp.fin_expense(category,unit,value) VALUES ('VAT','Percentage of Power Cost',2);''')
            curdb.execute('''INSERT INTO sysinp.fin_subsidy(type,unit,value) VALUES ('Capital Subsidy','Percentage',50);''')
            curdb.execute('''INSERT INTO sysinp.fin_subsidy(type,unit,value) VALUES ('Operational Subsidy-First Year','Percentage',0);''')
            curdb.execute('''INSERT INTO sysinp.fin_subsidy(type,unit,value) VALUES ('Operational Subsidy-Upto Mid Year','Percentage',0);''')
            curdb.execute('''INSERT INTO sysinp.fin_subsidy(type,unit,value) VALUES ('Operational Subsidy-Upto Final Year','Percentage',0);''')
            curdb.execute('''INSERT INTO sysinp.fin_subsidy(type,unit,value) VALUES ('Service Drop Subsidy','Year',5);''')
            curdb.execute('''INSERT INTO sysinp.fin_households(item,percentage) VALUES ('Household Ratio',88.2);''')
            curdb.execute('''INSERT INTO sysinp.fin_households(item,percentage) VALUES ('Household Growth',11.8);''')
            curdb.execute('''INSERT INTO sysinp.fin_households(item,percentage) VALUES ('Potential Household',100);''')


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

    def writeText(self):
        index = self.tableView.selectedIndexes()[0]
        dbname = self.tableView.model().data(index)
        hostname = self.txtHost.text()
        password = self.txtPassword.text()
        username = self.txtUserName.text()
        data = {}
        data['login'] = []
        data['login'].append({
        'host': hostname,
        'user': username,
        'password': password,
        'database': dbname
        })
        fname = os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons/login.json"
        if os.path.exists(fname):
            os.remove(fname)
            with open(fname, 'w') as outfile:
                json.dump(data, outfile, indent = 2)
                outfile.close()
        else:
            with open(fname, 'w') as outfile:
                json.dump(data, outfile, indent= 2)
                outfile.close()

    def useDb(self):
        index = self.tableView.selectedIndexes()[0]
        dbname = self.tableView.model().data(index)

        hostname = self.txtHost.text()
        basicOps.hostname = hostname
        password = self.txtPassword.text()
        basicOps.password = password
        basicOps.dbasename = dbname
        username = self.txtUserName.text()
        basicOps.usrname = username
        pbsname = dbname
        self.writeText()
        self.close()

        sysinfo = frmMain_dialog(self.iface)
        gbops = utility.basicOps()

        sublist = gbops.getSubList(username, hostname, password, dbname)
        sysinfo.cmbSub.clear()
        sysinfo.cmbSub.addItems(sublist)
        sysinfo.cmbSub.setCurrentIndex(-1)

        sysinfo.txtPro.setText(self.txtUserName.text())
        sysinfo.txtDatabase.setText(dbname)
        sysinfo.exec_()