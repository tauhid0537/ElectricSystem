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

from frmAddLine import *
from addLine import *

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
        self.paswrd = basicOps.password

        self.lineLayerName = self.dbase + ": " + self.sub + "-" + self.fed + "-line"
        self.poleLayerName = self.dbase + ": " + self.sub + "-" + self.fed + "-pole"
        self.linProName = self.dbase + ": " + self.sub + "-" + self.fed + "-line-project-" + extensionProject.ProjectNumber

        vol = str(extensionProject.LineVoltage)
        splitVol = vol.split(".")
        volt = splitVol[0]

        sql = "select sysphase from sysinp.phase_con"
        sql2 = "select size from sysinp.fin_construction_cost where item = 'Electric Line' and type = '"+extensionProject.LineType+ "' and voltage = '" + volt + "'"
        cur = self.getcursor()
        cur.execute(sql)
        row = cur.fetchone()
        self.basePhase = row[0]

        cur.execute(sql2)
        sizes = cur.fetchall()
        lsizes = []
        for size in sizes:
            lsizes.append(size[0])


        lineForm = frmAddLine_dialog(self.iface)
        lineForm.txtPro.setText(basicOps.usrname)
        lineForm.txtPro.setDisabled(True)
        lineForm.txtPBS.setText(basicOps.dbasename)
        lineForm.txtPBS.setDisabled(True)
        lineForm.txtSub.setText(basicOps.substation)
        lineForm.txtSub.setDisabled(True)
        lineForm.txtFed.setText(basicOps.feeder)
        lineForm.txtFed.setDisabled(True)
        lineForm.txtProNum.setText(extensionProject.ProjectNumber)
        lineForm.txtProNum.setDisabled(True)
        lineForm.cmbConPhase.clear()
        lineForm.cmbConSize.clear()
        if self.basePhase == "RYB":
            lineForm.cmbConPhase.addItem('R')
            lineForm.cmbConPhase.addItem('Y')
            lineForm.cmbConPhase.addItem('B')
            lineForm.cmbConPhase.addItem('R-Y')
            lineForm.cmbConPhase.addItem('Y-B')
            lineForm.cmbConPhase.addItem('B-R')
            lineForm.cmbConPhase.addItem('R-Y-B')
        elif self.basePhase == "ABC":
            lineForm.cmbConPhase.addItem('A')
            lineForm.cmbConPhase.addItem('B')
            lineForm.cmbConPhase.addItem('C')
            lineForm.cmbConPhase.addItem('A-B')
            lineForm.cmbConPhase.addItem('B-C')
            lineForm.cmbConPhase.addItem('C-A')
            lineForm.cmbConPhase.addItem('A-B-C')

        lineForm.cmbConSize.addItems(lsizes)
        lineForm.cmbConPhase.setCurrentIndex(-1)
        lineForm.cmbConSize.setCurrentIndex(-1)
        lineForm.exec_()



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

    def getConnection(self):
        condb = psycopg2.connect(user = self.usr, host = self.hst, password = self.paswrd, dbname = self.dbase)
        condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return condb

    def getcursor(self):
        con = self.getConnection()
        cur = con.cursor()
        return cur

    def phaseConSize(self, proPhase):
        conSize1 = ""
        conSize2 = ""
        conSize3 = ""

        phase = utility.phase()
        if proPhase == phase.phase1(self.basePhase):
            conSize1 = extensionProject.PrimaryConductor

        elif proPhase == phase.phase2(self.basePhase):
            conSize2 = extensionProject.PrimaryConductor

        elif proPhase == phase.phase3(self.basePhase):
            conSize3 = extensionProject.PrimaryConductor

        elif proPhase == phase.phase4(self.basePhase):
            conSize1 = extensionProject.PrimaryConductor
            conSize2 = extensionProject.PrimaryConductor

        elif proPhase == phase.phase5(self.basePhase):
            conSize2 = extensionProject.PrimaryConductor
            conSize3 = extensionProject.PrimaryConductor

        elif proPhase == phase.phase6(self.basePhase):
            conSize3 = extensionProject.PrimaryConductor
            conSize1 = extensionProject.PrimaryConductor

        elif proPhase == phase.phase7(self.basePhase):
            conSize1 = extensionProject.PrimaryConductor
            conSize2 = extensionProject.PrimaryConductor
            conSize3 = extensionProject.PrimaryConductor

        return conSize1, conSize2, conSize3


    def canvasMoveEvent(self,event):
        x = event.pos().x()
        y = event.pos().y()

        startingPoint = QPoint(x,y)
        snapper = QgsMapCanvasSnapper(self.canvas)

        ## Try to get a point from the foreground snapper.
        ## If we don't get one we try the backround snapper and
        ## at last we do not snap.
        (retval,result) = snapper.snapToCurrentLayer(startingPoint, QgsSnapper.SnapToVertex)
        if result <> []:
            point = QgsPoint(result[0].snappedVertex)
        else:
            (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
            if result <> []:
                point = QgsPoint(result[0].snappedVertex)
            else:
                point = self.canvas.getCoordinateTransform().toMapCoordinates(event.pos().x(), event.pos().y());

        points = list(self.points)
        points.append(point)
        #points = self.interpolate ( points )
        self.setRubberBandPoints(points)

    def createLine(self, xy):
        canvas = qgis.utils.iface.mapCanvas()
        condb = self.getConnection()

        cur = condb.cursor()
        self.bsOps = utility.basicOps()
        fedcode = self.bsOps.getFedCode(cur, self.sub, self.fed)
        subcode = self.bsOps.getSubCode(cur, self.sub)

        sql = "select last_value from exprojects."+ extensionProject.LineTableName +"_seq"
        cur.execute(sql)
        rows = cur.fetchall()
        newNumber = 0
        for row in rows:
            lstNumber = row[0]
            newNumber = lstNumber + 1
        lineID = subcode + "-" + fedcode + "-pro-" + extensionProject.ProjectNumber + "-" + str(newNumber)
        linetablename = "exprojects." + extensionProject.LineTableName
        myXY = ','.join(map(str, xy))
        QMessageBox.information(self.iface.mainWindow(),"Add Project Layers",extensionProject.PhaseConfiguration)
        conSize = self.phaseConSize(extensionProject.PhaseConfiguration)
        conSize1 = conSize[0]
        conSize2 = conSize[1]
        conSize3 = conSize[2]
        QMessageBox.information(self.iface.mainWindow(),"Add Project Layers","Ph1- " + conSize1 + ", Ph2- " + conSize2 + ", Ph3- " + conSize3)

        sql2 = """INSERT INTO """ + linetablename + """ (substation, feeder, section_id, line_voltage,line_type, phase, con_size_1, con_size_2, con_size_3, geom)
        VALUES('""" + self.sub + """','""" + self.fed + """','""" + lineID + """','""" + str(extensionProject.LineVoltage)  +"""','""" + extensionProject.LineType + """','""" + extensionProject.PhaseConfiguration + """',
        '"""+ conSize1 + """','""" + conSize2 + """','""" + conSize3 + """',ST_GeomFromText('LINESTRING(""" + myXY + """)',3857));"""
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