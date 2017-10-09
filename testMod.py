#-------------------------------------------------------------------------------
# Name:        module2
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
from psycopg2 import connect

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


def run_script(iface):
    insertSubFedName('Mohakhali','MOH','Wireless','WIR')
    print("Finished")

    #pass

if __name__ == '__main__':
    main()
