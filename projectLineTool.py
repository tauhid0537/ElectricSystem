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

class prjLineTool(QgsMapTool):
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.canvas = iface.mapCanvas()
        self.iface = iface
        self.rb = QgsRubberBand(self.canvas, True)
        self.rb.setWidth(1)
        self.point = None
        self.points = []
        self.xy = []
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
    def activate(self):
        self.canvas.setCursor(self.cursor)

        self.usr = basicOps.usrname
        self.dbase = basicOps.dbasename
        self.sub = basicOps.substation
        self.fed = basicOps.feeder
        self.hst = basicOps.hostname
        self.pas = basicOps.password

        self.lineLayerName = self.dbase + ": " + self.sub + "-" + self.fed + "-line"
        self.poleLayerName = self.dbase + ": " + self.sub + "-" + self.fed + "-pole"
        self.linProName = self.dbase + ": " + self.sub + "-" + self.fed + "-line-project-" + extensionProject.ProjectNumber

    def setRubberBandPoints(self,points):
        self.resetRubberBand()
        for point in points:
            update = point is points[-1]
            self.rb.addPoint( point, update )

    def resetPoints(self):
        self.points = []
        self.xy = []

    def resetRubberBand(self):
        self.rb.reset(True)

    def refresh_layers(self):
        for layer in qgis.utils.iface.mapCanvas().layers():
            layer.triggerRepaint()

    def canvasMoveEvent(self,event):
        x = event.pos().x()
        y = event.pos().y()

        startingPoint = QPoint(x,y)
        snapper = QgsMapCanvasSnapper(self.canvas)

        ## Try to get a point from the foreground snapper.
        ## If we don't get one we try the backround snapper and
        ## at last we do not snap.
        (retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToVertex)
        if result <> []:
            point = QgsPoint( result[0].snappedVertex )
        else:
            (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
            if result <> []:
                point = QgsPoint( result[0].snappedVertex )
            else:
                point = self.canvas.getCoordinateTransform().toMapCoordinates( event.pos().x(), event.pos().y() );

        points = list( self.points )
        points.append( point )
        #points = self.interpolate ( points )
        self.setRubberBandPoints(points)

    def createLine(self, xy):
        canvas = qgis.utils.iface.mapCanvas()
        condb = psycopg2.connect(user = self.usr, host = self.hst, password = self.pas, dbname = self.dbase)
        condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = condb.cursor()
        self.bsOps = utility.basicOps()
        fedcode = self.bsOps.getFedCode(cur, self.sub, self.fed)
        subcode = self.bsOps.getSubCode(cur, self.sub)

        sql = "select last_value from exprojects.del_d2b_line_project_"+ extensionProject.ProjectNumber +"_seq"
        cur.execute(sql)
        rows = cur.fetchall()
        newNumber = 0
        for row in rows:
            lstNumber = row[0]
            newNumber = lstNumber + 1
        lineID = subcode + "-" + fedcode + "-pro-" + extensionProject.ProjectNumber + "-" + str(newNumber)
        linetablename = "exprojects." +subcode + "_" + fedcode + "_line_project_"+extensionProject.ProjectNumber
        myXY = ','.join(map(str, xy))

        sql2 = """INSERT INTO """ + linetablename + """ (substation, feeder, section_id, line_voltage,line_type, phase, con_size_1, con_size_2, con_size_3, geom)
        VALUES('"""+self.sub+"""','""" + self.fed + """','"""+lineID+"""',"""+str(extensionProject.LineVoltage)+""",'"""+extensionProject.LineType+"""','"""+extensionProject.PhaseConfiguration+"""',
        '"""+extensionProject.PrimaryConductor+"""','"""+extensionProject.PrimaryConductor+"""','"""+extensionProject.PrimaryConductor+"""',ST_GeomFromText('LINESTRING("""+myXY+""")',3857));"""
        cur.execute(sql2)
        condb.commit()

        self.refresh_layers()

    def canvasPressEvent(self, event):
        crsSrc = self.canvas.mapRenderer().destinationCrs()
        crsWGS = QgsCoordinateReferenceSystem(4326)

        #QApplication.setOverrideCursor(Qt.WaitCursor)
        x = event.pos().x()
        y = event.pos().y()

        color = QColor(255,0,0,100)
        self.rb.setColor(color)
        self.rb.setWidth(1)

        if event.button() == Qt.LeftButton:
            startingPoint = QPoint(x, y)

            snapper = QgsMapCanvasSnapper(self.canvas)
            (retval,result) = snapper.snapToCurrentLayer (startingPoint, QgsSnapper.SnapToVertex)
            if result <> []:
                point = QgsPoint( result[0].snappedVertex )
            else:
                (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
                if result <> []:
                    point = QgsPoint( result[0].snappedVertex )
                else:
                    point = self.canvas.getCoordinateTransform().toMapCoordinates(event.pos().x(), event.pos().y());
            if event.modifiers() == Qt.ShiftModifier:
                xform = QgsCoordinateTransform(crsSrc, crsWGS)
                point = xform.transform(QgsPoint(point.x(),point.y()))

            QApplication.restoreOverrideCursor()

            self.points.append(point)
            xy = str(point.x()) + " " + str(point.y())
            self.xy.append(xy)
            self.setRubberBandPoints(self.points)
        else:
            if len(self.points) >= 2:
                self.createLine(self.xy)
            self.resetPoints()
            self.resetRubberBand()
            self.canvas.refresh()
            self.refresh_layers()