# -*- coding: utf-8 -*-


from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

#import resources_rc
import os
import tempfile
import platform

class CopyCoordstool(QgsMapTool):

    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.canvas = iface.mapCanvas()
        #self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        self.iface = iface
        self.rb = QgsRubberBand(self.canvas, True)
        #self.rb.setColor(Qt.Red)
        self.rb.setWidth(1)
        self.points = []
        #self.type = Qgis.Polygon

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
    def resetPoints(self):
        self.points = []
    def refresh(self):
        # redraw, called when settings changed
        if self.points:
            #points = self.interpolate ( self.points )
            self.setRubberBandPoints(self.points )

    def canvasReleaseEvent(self,event):
        pass

    def showSettingsWarning(self):
        pass

    def activate(self):
        ## Set our new cursor.
        self.canvas.setCursor(self.cursor)

        ## Check wether Geometry is a Line or a Polygon
        mc = self.canvas
        layer = mc.currentLayer()

    def resetRubberBand(self):
        self.rb.reset( True)

    def setRubberBandPoints(self,points):
        self.resetRubberBand()
        for point in points:
            update = point is points[-1]
            self.rb.addPoint( point, update )

    def deactivate(self):
        # On Win7/64 it was failing if QGIS was closed with a layer opened
        # for editing with "'NoneType' object has no attribute 'Polygon'"
        # -> test QGis
        if QGis is not None:
            self.rb.reset(QGis.Polygon)
        self.points = []
        pass

    def isZoomTool(self):
        return False


    def isTransient(self):
        return False

    def isEditTool(self):
        return True

    def simplifyPoints( self, points, tolerance):
        geo = QgsGeometry.fromPolyline( points )
        geo = geo.simplify( tolerance );
        return geo.asPolyline()

    def pointScalar( self, p, k):
        return QgsPoint( p.x() * k, p.y() * k)

    def pointsAdd( self, p1, p2):
        return QgsPoint( p1.x() + p2.x(), p1.y() + p2.y() )

    def pointsTangentScaled(self, p1, p2, k ):
        x = p2.x()-p1.x()
        y = p2.y()-p1.y()
        return self.pointScalar( QgsPoint( x, y), k )

    def pointsDist(self, a, b):
        dx = a.x()-b.x()
        dy = a.y()-b.y()
        return math.sqrt( dx*dx + dy*dy )

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

    def createFeature(self):
        layer = self.canvas.currentLayer()
        provider = layer.dataProvider()
        fields = layer.pendingFields()
        f = QgsFeature(fields)

        coords = []
        #coords = self.interpolate ( self.points )

        if self.canvas.mapRenderer().hasCrsTransformEnabled() and layer.crs() != self.canvas.mapRenderer().destinationCrs():
            coords_tmp = coords[:]
            coords = []
            for point in coords_tmp:
                transformedPoint = self.canvas.mapRenderer().mapToLayerCoordinates( layer, point )
                coords.append(transformedPoint)

        ## Add geometry to feature.
        g = QgsGeometry().fromPolyline(coords)
        f.setGeometry(g)
        layer.startEditing()
        layer.addFeature(f)
        layer.commitChanges()
    """
        ## Add attributefields to feature.
        for field in fields.toList():
            ix = fields.indexFromName(field.name())
            f[field.name()] = provider.defaultValue(ix)

        layer.beginEditCommand("Feature added")

        settings = QSettings()
        disable_attributes = settings.value( "/qgis/digitizing/disable_enter_attribute_values_dialog", False, type=bool)
        if disable_attributes:
            layer.addFeature(f)
            layer.endEditCommand()
        else:
            dlg = self.iface.getFeatureForm(layer, f)
            if QGis.QGIS_VERSION_INT >= 20400:
                dlg.setIsAddDialog( True ) # new in 2.4, without calling that the dialog is disabled
            if dlg.exec_():
                if QGis.QGIS_VERSION_INT < 20400:
                    layer.addFeature(f)
                layer.endEditCommand()
            else:
                layer.destroyEditCommand()"""

    def canvasPressEvent(self, event):
        color = QColor(255,0,0,100)
        self.rb.setColor(color)
        self.rb.setWidth(1)
        x = event.pos().x()
        y = event.pos().y()


        if event.button() == Qt.LeftButton:
            startingPoint = QPoint(x,y)
            snapper = QgsMapCanvasSnapper(self.canvas)

            (retval,result) = snapper.snapToCurrentLayer (startingPoint, QgsSnapper.SnapToVertex)
            if result <> []:
                point = QgsPoint( result[0].snappedVertex )
            else:
                (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
                if result <> []:
                    point = QgsPoint( result[0].snappedVertex )
                else:
                    point = self.canvas.getCoordinateTransform().toMapCoordinates( event.pos().x(), event.pos().y() );

            #self.rb.addPoint(point)

            self.points.append(point)
            #points = self.interpolate ( self.points )
            self.setRubberBandPoints(self.points )

        else:
            if len( self.points ) >= 2:
                # refresh without last point
                self.refresh()
                self.createFeature()

            self.resetPoints()
            self.resetRubberBand()
            self.canvas.refresh()






















