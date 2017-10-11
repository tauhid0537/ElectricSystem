import sys
import os
from qgis.core import *

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import psycopg2


class basicOps:
    usrname = None
    hostname = None
    password = None
    dbasename = None
    drvpath = None
    proname = None

    def getSubCode(self):
        subcode = None
        try:
            condb = psycopg2.connect(user = usrname, host = hostname, password = password, dbname = dbasename)
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        else:
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            curdb = condb.cursor()
            subcodeqrySQL = "select sub_code from sysinp.sys_substation where substation = '%s';" % (sub)
            curdb.execute(subcodeqrySQL)
            if curdb.rowcount == 1:
                row = curdb.fetchone()
                subcode = row[0]
        return subcode

    def getFedCode(self):
        fedcode = None
        try:
            condb = psycopg2.connect(user = usrname, host = hostname, password = password, dbname = dbasename)
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        else:
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            curdb = condb.cursor()
            fedcodeqrySQL = "select fed_code from sysinp.sys_feeder where substation = '%s' and feeder = '%s';" % (sub, fed)
            curdb.execute(fedcodeqrySQL)
            if curdb.rowcount == 1:
                row = curdb.fetchone()
                fedcode = row[0]
        return fedcode

    def getSubList(self, usr, hst, pas, dbase):
        subList = []
        try:
            condb = psycopg2.connect(user = usr, host = hst, password = pas, dbname = dbase)
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        else:
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            curdb = condb.cursor()
            subqrySQL = "select substation from sysinp.sys_substation;"
            curdb.execute(subqrySQL)
            rows = curdb.fetchall()
            for row in rows:
                subList.append(row[0])
        return subList

    def getFeederList(self, hst, usr, pas, dbase, sub):
        fedList = []
        try:
            condb = psycopg2.connect(user = usr, host = hst, password = pas, dbname = dbase)
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        else:
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            curdb = condb.cursor()
            fedqrySQL = "select feeder from sysinp.sys_feeder where substation = '%s';" % (sub)
            curdb.execute(fedqrySQL)
            rows = curdb.fetchall()
            for row in rows:
                fedList.insert(row[0])
        return fedList

