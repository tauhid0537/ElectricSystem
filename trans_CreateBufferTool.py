# -*- coding: utf-8 -*-


from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *
import qgis
import ogr

import utility
from utility import *

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import psycopg2

import resources
import os
import tempfile
import platform





class CreateBufferTool(QgsMapTool):

    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.canvas = iface.mapCanvas()
        #self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        self.iface = iface
        self.usr = basicOps.usrname
        self.hst = basicOps.hostname
        self.pas = basicOps.password
        self.db = basicOps.dbasename

        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                          "      c None",
                                          ".     c #FF0000",


                                          "+     c #FFFFFF",
                                          "                ",
                                          "       +.+      ",
                                          "      ++.++     ",
                                          "     +.....+    ",
                                          "    +.     .+   ",
                                          "   +.   .   .+  ",
                                          "  +.    .    .+ ",
                                          " ++.    .    .++",
                                          " ... ...+... ...",
                                          " ++.    .    .++",
                                          "  +.    .    .+ ",
                                          "   +.   .   .+  ",
                                          "   ++.     .+   ",
                                          "    ++.....+    ",
                                          "      ++.++     ",
                                          "       +.+      "]))


        """self.cursor = QCursor(QPixmap(":/icons/cursor.png"), 1, 1)"""

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def refresh_layers(self):
        for layer in qgis.utils.iface.mapCanvas().layers():
            layer.triggerRepaint()

    def getCursor(self, usr, hst, pas, db):
        cur = None
        try:
            condb = psycopg2.connect(user = usr, host = hst, password = pas, dbname = db)
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = condb.cursor()
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        return cur


    def canvasReleaseEvent(self, event):
        global transName
        crsSrc = self.canvas.mapRenderer().destinationCrs()
        crsWGS = QgsCoordinateReferenceSystem(4326)

        QApplication.setOverrideCursor(Qt.WaitCursor)
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        #If Shift is pressed, convert coords to EPSG:4326
        if event.modifiers() == Qt.ShiftModifier:
            xform = QgsCoordinateTransform(crsSrc, crsWGS)
            point = xform.transform(QgsPoint(point.x(),point.y()))
        QApplication.restoreOverrideCursor()

        xx = str(point.x())
        yy = str(point.y())

        cur = self.getCursor(self.usr, self.hst, self.pas, self.db)
        sql = "select last_value from trans_proposed_gid_seq"
        #sql = 'select max(gid) from trans_proposed'
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            transName = row[0]

        transformerName = 'Transformer '+str(transName+1)

        sql2 = """INSERT INTO trans_proposed(size_mva, name, geom)
        VALUES(500,'"""+transformerName+ """',ST_GeomFromText('POINT(""" + xx + ' ' + yy + """)',32628));"""
        cur.execute(sql2)
        c.con.commit()

        checksql = 'select * from trans_proposed_buffer'
        cur.execute(checksql)
        whereClause = """name = '"""+transformerName + """'"""

        if cur.rowcount == 0:
            sql4 ="""INSERT INTO trans_proposed_buffer(trans_buff, trans_name, geom)
            select 500 as tans_buff, a.name, ST_Buffer(a.geom,500) from trans_proposed a where a.""" + whereClause + """;"""
            cur.execute(sql4)
            c.con.commit()
        else:
            sql3 = """INSERT INTO trans_proposed_buffer(trans_buff, trans_name, geom)
            with qr1 as(
            select ST_Union(a.geom) as geom from trans_proposed_buffer a inner join trans_proposed b on
            ST_Intersects(ST_Buffer(b.geom,500),a.geom) where b."""+whereClause+""")
            select 500 as tans_buff, a.name,
            ST_Difference(ST_Buffer(a.geom,500),b.geom) as diff_geom
            from trans_Proposed a left join qr1 b on ST_Intersects(ST_Buffer(a.geom,500),b.geom)
            where a.""" + whereClause + """;"""
            cur.execute(sql3)
            c.con.commit()

        self.refresh_layers()