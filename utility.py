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

    def getSubCode(self, cur, sub):
        subcode = None
        subcodeqrySQL = "select sub_code from sysinp.sys_substation where substation = '%s';" % (sub)
        cur.execute(subcodeqrySQL)
        if cur.rowcount == 1:
            row = cur.fetchone()
            subcode = row[0]
        return subcode

    def getFedCode(self, cur, sub, fed):
        fedcode = None
        fedcodeqrySQL = "select fed_code from sysinp.sys_feeder where substation = '%s' and feeder = '%s';" % (sub, fed)
        cur.execute(fedcodeqrySQL)
        if cur.rowcount == 1:
            row = cur.fetchone()
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

    def getFeederList(self, cur, sub):
        fedList = []
        fedqrySQL = "select feeder from sysinp.sys_feeder where substation = '%s';" % (sub)
        cur.execute(fedqrySQL)
        rows = cur.fetchall()
        i = -1
        for row in rows:
            i = i + 1
            fedList.append(row[0])

        return fedList

    def getLbaseList(self, cur):
        lbList = []
        lbqrySQL = "SELECT table_name FROM landbase.tables WHERE table_schema='public';"
        cur.execute(lbqrySQL)
        rows = cur.fetchall()
        i = -1
        for row in rows:
            i = i + 1
            lbList.append(row[0])
        return lbList

