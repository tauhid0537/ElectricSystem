# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from osgeo import ogr
import qgis

import sys
import os

   
class PoleAttributes:
    
    def poleNumber(self, feature):
        
        poleNum = feature['plno']
        return poleNum;
    
    def transkVA(self, feature):
        trans = ''
        if feature['eqsize'] != None:
            trans = feature['eqsize']
        return trans;
    
    def transPhase(self, feature):
        trans = ''
        if feature['eqphs'] != None:
            trans = feature['eqphs']
        return trans;

    def transNumber(self, feature):
        trans = ''
        if feature['eqid'] != None:
            trans = feature['eqid']
        return trans;

    def RS(self, feature):
        cons = 0
        if feature['rscon'] != None:
            cons = feature['rscon']
        return cons;

    def SC(self, feature):
        cons = 0
        if feature['sccon'] != None:
            cons = feature['sccon']
        return cons;
    
    def LC(self, feature):
        cons = 0
        if feature['lccon'] != None:
            cons = feature['lccon']
        return cons;

    def SI(self, feature):
        cons = 0
        if feature['sicon'] != None:
            cons = feature['sicon']
        return cons;

    def LI(self, feature):
        cons = 0
        if feature['licon'] != None:
            cons = feature['licon']
        return cons;

    def PB(self, feature):
        cons = 0
        if feature['pbcon'] != None:
            cons = feature['pbcon']
        return cons;

    def AG(self, feature):
        cons = 0
        if feature['agcon'] != None:
            cons = feature.GetField("agcon")
        return cons;

    def ST(self, feature):
        cons = 0
        if feature['stcon'] != None:
            cons = feature['stcon']
        return cons;

class Phase:

    def Phase1(self, basePhase):
        ph = ''
        if basePhase == 'RYB':
            ph = 'R'
        elif basePhase == 'ABC':
            ph = 'A'

        return ph;

    def Phase2(self, basePhase):
        ph = ''
        if basePhase == 'RYB':
            ph = 'Y'
        elif basePhase == 'ABC':
            ph = 'B'

        return ph;

    def Phase3(self, basePhase):
        ph = ''
        if basePhase == 'RYB':
            ph = 'B'
        elif basePhase == 'ABC':
            ph = 'C'

        return ph;

    def Phase4(self, basePhase):
        ph = ''
        if basePhase == 'RYB':
            ph = 'R-Y'
        elif basePhase == 'ABC':
            ph = 'A-B'

        return ph;

    def Phase5(self, basePahse):
        ph = ''
        if basePhase == 'RYB':
            ph = 'Y-B'
        elif basePhase == 'ABC':
            ph = 'B-C'

        return ph;
    
    def Phase6(self, basePhase):
        ph = ''
        if basePhase == 'RYB':
            ph = 'B-R'
        elif basePhase == 'ABC':
            ph = 'C-A'

        return ph;

    def Phase7(self, basePhase):
        ph = ''
        if basePhase == 'RYB':
            ph = 'R-Y-B'
        elif basePhase == 'ABC':
            ph = 'A-B-C'

        return ph;

    def PhaseLabel1(self, basePhase):
        ph = ''
        if basePhase == 'RYB':
            ph = 'Phase R'
        elif basePhase == 'ABC':
            ph = 'Phase A'

        return ph;

    def PhaseLabel2(self, basePahse):
        ph = ''
        if basePhase == 'RYB':
            ph = 'Phase Y'
        elif basePhase == 'ABC':
            ph = 'Phase B'

        return ph;

    def PhaseLabel3(self, basePahse):
        ph = ''
        if basePhase == 'RYB':
            ph = 'Phase B'
        elif basePhase == 'ABC':
            ph = 'Phase C'

        return ph;

class TransformerByPhase:

    def kVA1(self, transkVA, transPhase, basePhase):
        kva = 0
        if transPhase == Phase.Phase1(basePhase):
            kva = float(transphase)
        
        elif transPhase == Phase.Phase4(basePhase):
            if transkVA.index('-') != -1:
                kvap = transkVA.split('-')
                kva = float(kvap[0])
            else:
                kva = float(transkVA)/2

        elif transPhase == Phase.Phase6(basePhase):
            if transkVA.index('-') != -1:
                kvap = transkVA.split('-')
                kva = float(kvap[1])
            else:
                kva = float(transkVA)/2

        elif transPhase == Phase.Phase7(basePhase):
            if transkVA.index('-') != -1:
                kvas = transkVA.split('-')
                kva = float(kvas[0])
            else:
                kva = float(transkVA)/3

        return kva;

    def kVA2(self, transkVA, transPhase, basePhase):
        kva = 0
        if transPhase == Phase.Phase2(basePhase):
            kva = float(transphase)
        
        elif transPhase == Phase.Phase4(basePhase):
            if transkVA.index('-') != -1:
                kvap = transkVA.split('-')
                kva = float(kvap[1])
            else:
                kva = float(transkVA)/2

        elif transPhase == Phase.Phase5(basePhase):
            if transkVA.index('-') != -1:
                kvap = transkVA.split('-')
                kva = float(kvap[0])
            else:
                kva = float(transkVA)/2

        elif transPhase == Phase.Phase7(basePhase):
            if transkVA.index('-') != -1:
                kvas = transkVA.split('-')
                kva = float(kvas[1])
            else:
                kva = float(transkVA)/3

        return kva;

    def kVA3(self, transkVA, transPhase, basePhase):
        kva = 0
        if transPhase == Phase.Phase3(basePhase):
            kva = float(transphase)
        
        elif transPhase == Phase.Phase5(basePhase):
            if transkVA.index('-') != -1:
                kvap = transkVA.split('-')
                kva = float(kvap[1])
            else:
                kva = float(transkVA)/2

        elif transPhase == Phase.Phase6(basePhase):
            if transkVA.index('-') != -1:
                kvap = transkVA.split('-')
                kva = float(kvap[0])
            else:
                kva = float(transkVA)/2

        elif transPhase == Phase.Phase7(basePhase):
            if transkVA.index('-') != -1:
                kvas = transkVA.split('-')
                kva = float(kvas[2])
            else:
                kva = float(transkVA)/3

        return kva;

class getValue:

    def doubleFromTable(self, tableName, searchString, dataField):

        value = 0

        if BasicOps.pDataTable(tableName).fieldNameIndex(dataField) == -1:
            value = ""
        else:
            pTable = BasicOps.pDataTable(tableName)
            request = QgsFeatureRequest().setFilterExpression(searchString)
            pCursor = pTable.getFeatures(request)

            for row in pCursor:
                if row[dataField] != None:
                    value = float(row[dataField])
        pTable.removeSelection()

        return value;

    def stringFromTable(self, tableName, searchString, dataField):

        value = ""

        if BasicOps.pDataTable(tableName).fieldNameIndex(dataField) == -1:
            value = ""
        else:
            pTable = BasicOps.pDataTable(tableName)
            request = QgsFeatureRequest().setFilterExpression(searchString)
            pCursor = pTable.getFeatures(request)

            for row in pCursor:
                if row[dataField] != None:
                    value = str(row[dataField])
        pTable.removeSelection()

        return value;
    

    def feederFieldValue(fieldName):

        fedVal = 0
        pTableFed = BasicOps.pDataTable("SysFeeder")
        searchString = "Substation = '" + BasicOps.subname + "' AND Feeder = '" + BasicOps.fedname + "'"
        
        request = QgsFeatureRequest().setFilterExpression(searchString)
        pCursor = pTableFed.getFeatures(request)
        count = pTableFed.selectedFeatureCount()

        if count == 1:
            for row in pCursor:
                if pTableFed.fieldNameIndex(fieldName) != -1:
                    if row[fieldName] != None:
                        fedVal = row[fieldName]
        pTableFed.removeSelection()

        return fedVal;
    

    def getValString(self, tableName, searchField, searchString, dataField):

        value = ""

        search = searchField + " = '" + searchString + "'"
        request = QgsFeatureRequest().setFilterExpression(searchString)
        pCursor = BasicOps.pDataTable(tableName).getFeatures(request)

        for row in pCursor:
            if row[dataField] != None:
                value = str(row[dataField])

        BasicOps.pDataTable(tableName).removeSelection()
        return value;

    def getValDouble(self, tableName, searchField, searchString, dataField):
        value = 0
        search = searchField + " = '" + searchString + "'"
        request = QgsFeatureRequest().setFilterExpression(search)
        pCursor = BasicOps.pDataTable(tableName).getFeatures(request)

        for row in pCursor:
            if row[dataField] != None:
                value = float(row[dataField])
        BasicOps.pDataTable(tableName).removeSelection()
        return value;
    

    def subCode(self):

        pTable = BasicOps.pDataTable("SysSubstation")
        searchString = "Substation = '" + BasicOps.subname + "'"
        request = QgsFeatureRequest().setFilterExpression(searchString)
        pCursor = pTable.getFeatures(request)

        subcode = ""

        for row in pCursor:
            if row['SubCode'] != None:
                subcode = row['SubCode']
        pTable.removeSelection()
        return subcode;

    def fedCode(self):
        pTable = BasicOps.pDataTable("SysFeeder")
        searchString = "Substation = '" + BasicOps.subname + "' AND Feeder = '" + BasicOps.fedname + "'"
        
        request = QgsFeatureRequest().setFilterExpression(searchString)
        pCursor = pTable.getFeatures(request)

        fedcode = ""

        for row in pCursor:
            if row['FedCode'] != None:
                subcode = row['FedCode']
        pTable.removeSelection()
        return subcode;

    def getMultiValue(self, tableName, searchString, dataField):

        #layer.dataProvider().fields().count()

        allValues = []
        table = BasicOps.pDataTable(tableName)

        request = QgsFeatureRequest().setFilterExpression(searchString)
        pCursor = table.getFeatures(request)

        ListID = []

        if table.selectedFeatureCount() > 0:
            for row in pCursor:
                val = ""
                if row[dataField] != None:
                    val = row[dataField]
                    val.strip()
                    allValues.append(val)
            if len(allValues) > 0:
                ListID = set(allValues)
        return ListID;

    def doubleFromRow(self, tableName, pRow, fieldName):

        value = 0

        table = BasicOps.pDataTable(tableName)

        if table.fieldNameIndex(fieldName) == -1:
            value = ""
        else:
            if pRow[fieldName] != None:
                value = float(pRow[fieldName])
        table.removeSelection()
        return value;

    def stringFromRow(self, tableName, pRow, fieldName):

        value = ""

        table = BasicOps.pDataTable(tableName)

        if table.fieldNameIndex(fieldName) == -1:
            value = ""
        else:
            if pRow[fieldName] != None:
                value = str(pRow[fieldName])
        table.removeSelection()
        return value;

    def stringfromFeature(self, layerName, feature, fieldName):

        value = ""

        if BasicOps.pLayer(layerName).fieldNameIndex(fieldName) == -1:
            value = ""
        else:
            if feature[fieldName] != None:
                value = str(feature[fieldName])

        return value;
    
    def doublefromFeature(self, layerName, feature, fieldName):

        value = 0

        if BasicOps.pLayer(layerName).fieldNameIndex(fieldName) == -1:
            value = 0
        else:
            if feature[fieldName] != None:
                value = float(feature[fieldName])

        return value;

    def sumValueLayer(self, layerName, fieldName, searchString):

        value = 0
        layer = BasicOps.pLayer(layerName)

        if layer.fieldNameIndex(fieldName) == -1:
            value = 0
        else:
            if searchString != "":
                request = QgsFeatureRequest().setFilterExpression(searchString)
                #selection = layer.getFeatures(request)

            selection = layer.getFeatures(request)
            for feat in selection:
                if feat[fieldName] != None:
                    value = value + float(feat[fieldName])
            layer.removeSelection()

        return value;

    def getConductorLineLength(self, layerName, conductorSize, phaseNumber):

        length = 0
        selected= 0
        layer = BasicOps.pLayer(layerName)

        if phaseNumber == "Three Phase":
            searchString = "cons1 = '" + conductorSize + "'"
            request = QgsFeatureRequest().setFilterExpression(searchString)
            selection = layer.getFeatures(request)
            selected = layer.selectedFeatureCount()
        elif phaseNumber == "Two Phase":
            searchString = "cons1 = '" + conductorSize + "' AND cons2 = '" + conductorSize + "'"
            request = QgsFeatureRequest().setFilterExpression(searchString)
            selection = layer.getFeatures(request)
            selected = layer.selectedFeatureCount()

            if selected == 0:
                searchString = "cons2 = '" + conductorSize + "' AND cons3 = '" + conductorSize + "'"
                request = QgsFeatureRequest().setFilterExpression(searchString)
                selection = layer.getFeatures(request)
                selected = layer.selectedFeatureCount()

                if selected == 0:
                    searchString = "cons3 = '" + conductorSize + "' AND cons1 = '" + conductorSize + "'"
                    request = QgsFeatureRequest().setFilterExpression(searchString)
                    selection = layer.getFeatures(request)
                    selected = layer.selectedFeatureCount()
        elif phaseNumber == "Single Phase":
            
            searchString = "cons1 = '" + conductorSize + "' OR cons2 = '" + conductorSize + "' OR cons3 = '" + conductorSize + "'"
            request = QgsFeatureRequest().setFilterExpression(searchString)
            selection = layer.getFeatures(request)
            selected = layer.selectedFeatureCount()
        if selected > 0:
            for feat in selection:
                geom = feat.geometry()
                length = length + geom.length()

        layer.removeSelection()
        return length;

class ConsumerByPhase:

    def Consumer1(self, consumerList, consumerIndex, lisePhase, basePhase):

        consumerP = 0
        consumer = consumerList[consumerIndex]

        if linePhase == Phase.Phase1(basePhase):
            consumerP = consumer
        elif linePhase == Phase.Phase4(basePhase) | linePhase == Phase.Phase6(basePhase):
            consumerP = consumer / 2
        elif linePhase == Phase.Phase7(basePhase):
            consumerP = consumer / 3

        return consumerP;

    def Consumer2(self, consumerList, consumerIndex, lisePhase, basePhase):

        consumerP = 0
        consumer = consumerList[consumerIndex]

        if linePhase == Phase.Phase2(basePhase):
            consumerP = consumer
        elif linePhase == Phase.Phase4(basePhase) | linePhase == Phase.Phase5(basePhase):
            consumerP = consumer / 2
        elif linePhase == Phase.Phase7(basePhase):
            consumerP = consumer / 3

        return consumerP;

    def Consumer3(self, consumerList, consumerIndex, lisePhase, basePhase):

        consumerP = 0
        consumer = consumerList[consumerIndex]

        if linePhase == Phase.Phase3(basePhase):
            consumerP = consumer
        elif linePhase == Phase.Phase5(basePhase) | linePhase == Phase.Phase6(basePhase):
            consumerP = consumer / 2
        elif linePhase == Phase.Phase7(basePhase):
            consumerP = consumer / 3

        return consumerP;

class BasicOps:

    global proname, pbsname, subname, fedname, drvpath, phasecon, syspath, datadev, gdbpath;

    def pDataTable(self, tableName):

        table = QgsVectorLayer(BasicOps.drvPath+ ":\\"+BasicOps.proname+"\\"+ ptableName+ "\\.dbf", tableName, 'ogr')

        return table;
    
    
    def addTabletoCanvas(self):
        table = QgsVectorLayer(r'D:\Temp\buff_structure_pro.dbf', 'Transformer Buffer', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(table)
    
    def pLayer(self, layerName):

        canvas = qgis.utils.iface.mapCanvas()

        layers = canvas.layers()
        v = len(layers)
        pPoleLayer = None

        for layer in layers:
            if layer.name() == layerName:
                pPoleLayer = layer

        return pPoleLayer;

    def pDataTable(self, tableName):

        canvas = qgis.utils.iface.mapCanvas()

        layers = canvas.layers()
        v = len(layers)
        pDataTable = None

        for layer in layers:
            if layer.name() == tableName:
                pDataTable = layer

        return pDataTable;

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
            QMessageBox.information(self.iface.mainWindow(),"Create Shapefile","Electric Pole Shapefile Created")
        else:
            QMessageBox.critical(self.iface.mainWindow(),"Create Shapefile","Electric Pole Shapefile Not Created")

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
            QMessageBox.information(self.iface.mainWindow(),"Create Shapefile","Electric Line Shapefile Created")
        else:
            QMessageBox.critical(self.iface.mainWindow(),"Create Shapefile","Electric Line Shapefile Not Created")

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
            QMessageBox.information(self.iface.mainWindow(),"Create Shapefile","Substation Shapefile Created")
        else:
            QMessageBox.critical(self.iface.mainWindow(),"Create Shapefile","Substation Shapefile Not Created")

    def removeMapLayer(self, layerName):
        QgsMapLayerRegistry.removeMapLayer(layerName)

    def removeAllMapLayers(self):
        QgsMapLayerRegistry.removeAllMapLayers()

    def checkLayer(self, layerName):

        layerExist = False
        canvas = qgis.utils.iface.mapCanvas() 
        layers = canvas.layers()

        for layer in layers:
            if layer.name() == layerName:
                layerExist = True

        return layerExist;

    def creatPNG(self, fileName):
        
        mainPath = '/path/to/folder/'
        #filename = 'filename'
        imageType = "png"
        imageWidth_mm = 1920
        imageHeight_mm = 1080
        dpi = 300

        map_settings = iface.mapCanvas().mapSettings()
        c = QgsComposition(map_settings)
        c.setPaperSize(400, 160)
        c.setPrintResolution(dpi)

        #set page background to transparent
        transparent_fill =QgsFillSymbolV2.createSimple({ 'outline_style': 'no', 'style': 'no'})
        c.setPageStyleSymbol( transparent_fill )

        x, y = 0, 0
        w, h = c.paperWidth(), c.paperHeight()
        composerMap = QgsComposerMap(c, x ,y, w, h)
        composerMap.setBackgroundEnabled(False)
        c.addItem(composerMap)

        dpmm = dpi / 25.4
        width = int(dpmm * c.paperWidth())
        height = int(dpmm * c.paperHeight())

        # create output image and initialize it
        image = QImage(QSize(width, height), QImage.Format_ARGB32)
        image.setDotsPerMeterX(dpmm * 1000)
        image.setDotsPerMeterY(dpmm * 1000)
        image.fill(Qt.transparent)

        imagePainter = QPainter(image)

        c.setPlotStyle(QgsComposition.Print)
        c.renderPage( imagePainter, 0 )
        imagePainter.end()

        imageFilename =  mainPath + fileName + '.' + imageType
        image.save(imageFilename, imageType)

    def updateFeature(self, layer, feature, fieldName, fieldValue):

        updateResult = ""

        if layer.fieldNameIndex(fieldName) == -1:
            value = "ERROR : Field does not Exist: " + fieldName;
        else:
            try:
                layer.startEditing()
                feature[fieldName] = fieldValue
                layer.commitChanges()
                updateResult = "Field " + fieldName + " Ready for Update with Value " + fieldValue
            except:
                updateResult = "ERROR : Field " + fieldName + " cannot be Updated with Value " + fieldValue

        return updateResult;
    
class extensionProject:
    projectNumber = ""
    projectName = ""
    householdSource = ""
    lineType = ""
    lineVoltage = 0
    primaryConductor = ""
    secondaryConductor = ""
    phaseConfiguration = ""
    bufferDistance = 0
    minimumTransformerkVA = 0
    maximuTransformerkVA = 0
    secondaryLength = 0
    householdType = 0
    analysisYear = 0
    midAnalysisYear = 0
    interestYear = 0
    equipmentType = ""
    equipmentSize = ""
