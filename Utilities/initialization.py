from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from osgeo import ogr
import qgis

import sys
import os

import utilities

class CreateShapefile:

    def createPole(self, path, poleName):
        crs = QgsCoordinateReferenceSystem(4326)

        poleLayer=QgsVectorLayer("point","Pole","memory")
        poleDataProvider = poleLayer.dataProvider()
        poleDataProvider.addAttributes([QgsField("sub",QVariant.String),QgsField("fed",QVariant.String),QgsField("gpsno",QVariant.String),
                          QgsField("fedpole",QVariant.Int),QgsField("plno",QVariant.String),QgsField("plus",QVariant.String),
                          QgsField("plphs",QVariant.String),QgsField("plht",QVariant.Double),QgsField("plcls",QVariant.String),
                          QgsField("plstr",QVariant.String),QgsField("plfit",QVariant.String),QgsField("plguy",QVariant.String),
                          QgsField("plgtyp",QVariant.String),QgsField("plgag",QVariant.String),QgsField("plstat",QVariant.String),
                          QgsField("eqtype",QVariant.String),QgsField("refpole",QVariant.String),QgsField("eqid",QVariant.String),
                          QgsField("equnt",QVariant.Int),QgsField("eqmnt",QVariant.String),QgsField("eqsize",QVariant.String),
                          QgsField("eqphs",QVariant.String),QgsField("eqstat",QVariant.String),QgsField("equse",QVariant.String),
                          QgsField("trref",QVariant.String),QgsField("rscon",QVariant.Double),QgsField("sccon",QVariant.Double),
                          QgsField("lccon",QVariant.Double),QgsField("sicon",QVariant.Double),QgsField("licon",QVariant.Double),
                          QgsField("pbcon",QVariant.Double),QgsField("agcon",QVariant.Double),QgsField("stcon",QVariant.Double),
                          QgsField("location",QVariant.String),QgsField("datsrc",QVariant.String),QgsField("remarks",QVariant.String)])
        poleLayer.updateFields()

        poleError = QgsVectorFileWriter.writeAsVectorFormat(poleLayer, path + "/" + poleName + ".shp", "CP1250", crs, "ESRI Shapefile")
        if poleError == QgsVectorFileWriter.NoError:
            utilities.polecreated = True
        else:
            utilities.polecreated = False

    def createLine(self, path, LineName):
        crs = QgsCoordinateReferenceSystem(4326)
        lineLayer=QgsVectorLayer("LineString","substationfeederline","memory")
        lineDataProvider = lineLayer.dataProvider()
        lineDataProvider.addAttributes([QgsField("sub",QVariant.String),QgsField("fed",QVariant.String),QgsField("lnalgn",QVariant.String),
                          QgsField("lnvol",QVariant.Double),QgsField("lntype",QVariant.String),QgsField("secid",QVariant.String),
                          QgsField("lnphs",QVariant.String),QgsField("trcode",QVariant.String),QgsField("seccon",QVariant.String),
                          QgsField("trref",QVariant.String),QgsField("cons1",QVariant.String),QgsField("cons2",QVariant.String),
                          QgsField("cons3",QVariant.String),QgsField("consn",QVariant.String),QgsField("lnstat",QVariant.String),
                          QgsField("datasrc",QVariant.String),QgsField("remarks",QVariant.String)])
        lineLayer.updateFields()

        lineError = QgsVectorFileWriter.writeAsVectorFormat(lineLayer, path + "/" + LineName + ".shp", "CP1250", crs, "ESRI Shapefile")
        if lineError == QgsVectorFileWriter.NoError:
            utilities.linecreated = True
        else:
            utilities.linecreated = False

    def createSub(self, path, subName):
        crs = QgsCoordinateReferenceSystem(4326)
        subLayer=QgsVectorLayer("point","substationfeedersub","memory")
        subDataProvider = subLayer.dataProvider()
        subDataProvider.addAttributes([QgsField("sub",QVariant.String),QgsField("fed",QVariant.String),QgsField("subtyp",QVariant.String),
                          QgsField("nofed",QVariant.Int),QgsField("capacity",QVariant.Double),QgsField("nooftr",QVariant.Int),
                          QgsField("Loc",QVariant.String),QgsField("remarks",QVariant.String)])
        subLayer.updateFields()

        subError = QgsVectorFileWriter.writeAsVectorFormat(subLayer, path + "/" + subName + ".shp", "CP1250", crs, "ESRI Shapefile")
        if subError == QgsVectorFileWriter.NoError:
            utilities.subcreated = True
        else:
            utilities.subcreated = False

    def updateTables(self, sub, subcode, fed, fedcode):

        subtabLoc = utilities.drvpath + ":\\" + utilities.proname + "\\Database\\" + utilities.pbsname + "\\Tables\\SysSubstation.dbf" 
        table = QgsVectorLayer(subtabLoc, 'SysSubstation', 'ogr')

        searchString = "Substation = '" + sub + "'"
        request = QgsFeatureRequest().setFilterExpression(searchString)
        countFeat = table.selectedFeatures().count()

        if countFeat == 0:
            caps = table.dataProvider().capabilities()
            if caps & QgsVectorDataProvider.AddFeatures:
                feat = QgsFeature(table.pendingFields())
                feat.setAttribute('Substation', sub)
                feat.setAttribute('SubCode', subcode)
                (res, outFeats) = table.dataProvider().addFeatures([feat])
        table.removeSelection()

        fedtabLoc = utilities.drvpath + ":\\" + utilities.proname + "\\Database\\" + utilities.pbsname + "\\Tables\\SysFeeder.dbf" 
        fedtable = QgsVectorLayer(fedtabLoc, 'SysFeeder', 'ogr')

        searchString = "Substation = '" + sub + "' AND Feeder = '" + fed + "'"
        request = QgsFeatureRequest().setFilterExpression(searchString)
        countFeat = fedtable.selectedFeatures().count()

        if countFeat == 0:
            caps = fedtable.dataProvider().capabilities()
            if caps & QgsVectorDataProvider.AddFeatures:
                feat = QgsFeature(fedtable.pendingFields())
                feat.setAttribute('Substation', sub)
                feat.setAttribute('Feeder', fed)
                feat.setAttribute('FedCode', fedcode)
                (res, outFeats) = fedtable.dataProvider().addFeatures([feat])
        fedtable.removeSelection()
