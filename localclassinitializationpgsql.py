#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      islat
#
# Created:     25/08/2017
# Copyright:   (c) islat 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from osgeo import ogr
import qgis
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
#from config import config

def createSysSubstationTables(self):
    con = None
    con = psycopg2.connect(dbname='testpython', user='postgres', host='localhost', password='postgres')
    cur = con.cursor()

    tableSQL = """
    CREATE TABLE syssubstation
    (
    objectid int NOT NULL DEFAULT nextval('syssubstation_objectid_seq'::regclass),
    substation varchar(30), subassetid varchar(30), subcode varchar(5),
    subloc varchar(30), subsrvdate date, subx float(6), suby float(6),
    subtrnnum int, subfednum int, subcap float(6), subtypecat varchar(30),
    subrem varchar(100), subcon varchar(20), sublg float(6), subll float(6),
    subbusv float(6), subreg varchar(5), subminimp float(6), submaximp float(6),
    subovrimp float(6), subundimp float(6), subnote varchr(50), sublstbld date,
    sublstudt date
    );"""
    cur.execute(tableSQL)
    con.commit()
    cur.close()
    con.close()

def createSysFeederTable(self):
    con = None
    con = psycopg2.connect(dbname = 'testpython', user = 'postgres', host = 'localhost', password = 'postgres')
    cur = con.cursor()
    tablesql = """
    CREATE TABLE sysfeeder
    (
    objectid int NOT NULL DEFAULT nextval('sysfeeder_objectid_seq'::regclass),
    substation varchar(30), feeder varchar(30), fedcode varchar(5),
    fedlength float(6), fednomv float(6), fedbusv float(6), fedfltres float(6),
    fedcon vachar(20), feddes varchar(50), fedrs1 float(6), fedrs2 float(6),
    fedrs3 float(6), fedrs1 float(6), fedsc1 float(6), fedsc2 float(6),
    fedsc3 float(6), fedsc1 float(6), fedlc1 float(6), fedlc2 float(6), fedlc3 float(6),
    fedlct float(6), fedsi1 float(6),fedsi2 float(6), fedsi3 float(6),
    fedsit float(6), fedli1 float(6), fedli2 float(6), fedli3 float(6),
    fedlit float(6), fedpb1 float(6), fedpb2 float(6), fedpb3 float(6), fedpbt float(6),
    fedag1 float(6), fedag2 float(6), fedag3 float(6), fedagt float(6),
    fedst1 float(6), fedst2 float(6), fedst3 float(6), fedstt float(6),
    fedrsc1 float(6), fedscc float(6), fedlcc float(6), fedsic float(6),
    fedlic float(6), fedpbc float(6), fedagc float(6), fedstc float(6),
    fedcon1 float(6), fedcon2 float(6), fedcon3 float(6), fedcont float(6),
    fedkva1 float(6), fedkva2 float(6), fedkva3 float(6), fedkvat float(6),
    fedkwh1 float(6), fedkwh2 float(6), fedkwh3 float(6), fedkwhT float(6),
    fedkvar1 float(6), fedkvar2 float(6), fedkvar3 float(6), fedkvart float(6),
    fedamps1 float(6), fedamps2 float(6), fedamps3 float(6), fedampst float(6),
    fedpf1 float(6), fedpf2 float(6), fedpf3 float(6), fedpfT float(6),
    fedlstbld date, fedlstudt date
    );"""
    cur.execute(tablesql)
    con.commit()
    cur.close()
    con.close()

def createConductorTable(self):
    con = None
    con = psycopg2.connect(dbname = 'testpython', user = 'postgres', host = 'localhost', password = 'postgres')
    cur = con.cursor()
    tableSQL = """
    CREATE TABLE sysconductor
    (
    objectid int NOT NULL DEFAULT nextval('sysconductor_objectid_seq'::regclass),
    name varchar(30), constrtn varchar(50), strand varchar(20),
    dia_mm float(6), area_mm2 float(6), r_km float(6), gmr_m float(6),
    x_50_km vachar(20), x_60_km varchar(50), maxamps float(6)
    );
    """
    cur.execute(tableSQL)
    con.commit()
    cur.close()
    con.close()

def insertSubFedName(self, sub, subcode, fed, fedcode):
    con = None
    con = psycopg2.connect(dbname = 'testPython', user = 'postgres', host = 'localhost', password = 'postgres')
    cur = con.cursor()
    whereClause = "Substation = '" + sub + "';"
    fedTablewhereClause = "Substation = '" + sub + "' AND Feeder = '" + fed + "';"
    subTableSQL = """ SELECT * FROM syssubstation WHERE """ + whereClause
    cur.execute(subTableSQL)
    if cur.rowcount == 0:
        subvals = ["'"+sub+"'", "'"+subcode+"'"]
        subValues = ','.join(subvals)
        sql = """INSERT INTO syssubstation(substation,subcode)
        VALUES(%s);""" % subValues
        cur.execute(sql)
        con.commit()

    fedTableSQL = "SELECT * FROM sysfeeder WHERE " + fedTablewhereClause
    cur.execute(fedTableSQL)
    if cur.rowcount == 0:
        fedvals = ["'"+sub+"'", "'"+fed+"'", "'"+fedcode+"'"]
        fedValues = ','.join(fedcals)
        sql2 = """INSERT INTO sysfeeder(substation, feeder, fedcode)
        VALUES(%s);""" %fedValues
        cur.execute(sql2)
        con.commit()

    cur.close()
    con.close()


