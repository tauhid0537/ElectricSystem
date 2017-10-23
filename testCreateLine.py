from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *
import qgis

#import resources_rc
import os
import sys

class lineCreateTool(QgsMapTool):

    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.canvas = iface.mapCanvas()
        self.iface = iface
        self.rb = QgsRubberBand(self.canvas, True)
        self.rb.setWidth(1)
        self.point = None
        self.points = []
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

    def setRubberBandPoints(self,points):
        self.resetRubberBand()
        for point in points:
            update = point is points[-1]
            self.rb.addPoint( point, update )

    def resetPoints(self):
        self.points = []

    def resetRubberBand(self):
        self.rb.reset(True)

    def refresh_layers(self):
        for layer in qgis.utils.iface.mapCanvas().layers():
            layer.triggerRepaint()

    def createLine(self):
        canvas = qgis.utils.iface.mapCanvas()

        layers = canvas.layers()
        v = len(layers)
        lineLayer = None

        for layer in layers:
            if layer.name() == "All_feeder_Line_RIR_new":
                lineLayer = layer
                lineLayerpath = lineLayer.dataProvider().dataSourceUri()
                lineLayerpath = lineLayerpath [:lineLayerpath.rfind('|')]

        lineLayerCaps = lineLayer.dataProvider().capabilities()
        if lineLayerCaps & QgsVectorDataProvider.AddFeatures:
            lineFeat = QgsFeature(lineLayer.pendingFields())
            lineFeat.setAttributes(['Freetown', 'Test Line1','Overhead'])
            lineFeat.setGeometry(QgsGeometry.fromPolyline(self.points))
            (res, outFeats) = lineLayer.dataProvider().addFeatures([lineFeat])
        self.iface.mapCanvas().refresh()

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
        self.setRubberBandPoints(points )

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
            self.setRubberBandPoints(self.points)
        else:
            if len(self.points) >= 2:
                self.createLine()
            self.resetPoints()
            self.resetRubberBand()
            self.canvas.refresh()
            self.refresh_layers()
