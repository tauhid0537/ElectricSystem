# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from osgeo import ogr
import qgis
from utilities import *
from dbf import *

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")

class LocalClassInitialization:

    global pbsName

    def createSubstationTable(self):
        #tablePath and tableName should go as parameter
        tablePath = "\path\to\save\dbf"
        tableName = "SysSubstation.dbf"

        dbf = Dbf(tablePath + "\\" + tableName, new = True)
        dbf.addField(
            ("Substation", "C", 30),("SubAssetID", "C", 30),("SubCode", "C", 5),
            ("SubLoc", "C", 30),("SubSrvDate", "D"),("SubX", "F"),("SubY", "F"),
            ("SubTrnNum", "I"),("SubFedNum", "I"),("SubCap", "F"),("SubTypeCat", "C", 30),
            ("SubRem", "C", 100),("SubCon", "C", 20),("SubLG", "F"),
            ("SubLL", "F"),("SubBusV", "F"),("SubReg", "C", 5),("SubMinImp", "F"),
            ("SubMaxImp", "F"),("SubOvrImp", "F"),("SubUndImp", "F"),
            ("SubNote", "C", 50),("SubLstBld", "D"),("SubLstUdt", "D"))
        dbf.close()

    def createFeederTable(self):
        #tablePath and tableName should go as parameter
        tablePath = "\path\to\save\dbf"
        tableName = "SysFeeder.dbf"

        dbf = Dbf(tablePath + "\\" + tableName, new = True)
        dbf.addField(
            ("Substation", "C", 30),("Feeder", "C", 30),("FedCode", "C", 5),
            ("FedLength", "F"),("FedNomV", "F"),("FedBusV", "F"),("FedFltRes", "F"),
            ("FedCon", "C", 20),("FedDes", "C", 50),("FedRS1", "F"),("FedRS2", "F"),
            ("FedRS3", "F"),("FedRST", "F"),("FedSC1", "F"),("FedSC2", "F"),
            ("FedSC3", "F"),("FedSCT", "F"),("FedLC1", "F"),("FedLC2", "F"),
            ("FedLC3", "F"),("FedLCT", "F"),("FedSI1", "F"),("FedSI2", "F"),
            ("FedSI3", "F"),("FedSIT", "F"),("FedLI1", "F"),("FedLI2", "F"),
            ("FedLI3", "F"),("FedLIT", "F"),("FedPB1", "F"),("FedPB2", "F"),
            ("FedPB3", "F"),("FedPBT", "F"),("FedAG1", "F"),("FedAG2", "F"),
            ("FedAG3", "F"),("FedAGT", "F"),("FedST1", "F"),("FedST2", "F"),
            ("FedST3", "F"),("FedSTT", "F"),("FedRSC", "F"),("FedSCC", "F"),
            ("FedLCC", "F"),("FedSIC", "F"),("FedLIC", "F"),("FedPBC", "F"),
            ("FedAGC", "F"),("FedSTC", "F"),("FedCon1", "F"),("FedCon2", "F"),
            ("FedCon3", "F"),("FedConT", "F"),("FedkVA1", "F"),("FedkVA2", "F"),
            ("FedkVA3", "F"),("FedkVAT", "F"),("FedkWH1", "F"),("FedkWH2", "F"),
            ("FedkWH3", "F"),("FedkWHT", "F"),("FedkW1", "F"),("FedkW2", "F"),
            ("FedkW3", "F"),("FedkWT", "F"),("FedkVAR1", "F"),("FedkVAR2", "F"),
            ("FedkVAR3", "F"),("FedkVART", "F"),("FedAmps1", "F"),("FedAmps2", "F"),
            ("FedAmps3", "F"),("FedAmpsT", "F"),("FedPf1", "F"),("FedPf2", "F"),
            ("FedPf3", "F"),("FedPfT", "F"),("FedLstBld", "D"),("FedLstUdt", "D"))
        dbf.close()

    def createConductorTable(self):
        #tablePath and tableName should go as parameter
        tablePath = "\path\to\save\dbf"
        tableName = "SysConductor.dbf"

        dbf = Dbf(tablePath + "\\" + tableName, new = True)
        dbf.addField(
            ("Name", "C", 30),("Constrtn", "C", 50),("Strand", "C", 20),
            ("Dia_mm", "F"),("Area_mm2", "F"),("R_km", "F"),("Gmr_m", "F"),
            ("X_50_km", "F"),("X_60_km", "I"),("MaxAmps", "F"))
        dbf.close()

    def addSubFedName(self, sub, subcode, fed, fedcode):

        table = BasicOps.pDataTable("SysSubstation")
        searchString = "Substation = '" + sub + "'"
        request = QgsFeatureRequest().setFilterExpression(searchString)
        pCursor = table.getFeatures(request)

        if table.selectedFeatureCount() == 0:
            caps = table.dataProvider().capabilities()
            if caps & QgsVectorDataProvider.AddFeatures:
                feat = QgsFeature(layer.pendingFields())
		feat.setAttribute('Substation', sub)
		feat.setAttribute('SubCode', subcode)
		(res, outFeats) = layer.dataProvider().addFeatures([feat])
	    elif table.selectedFeatureCount() > 0:
                updateMap = {}
                provider = table.dataProvider()
                for feat in pCursor:
                    subIdx = feat.fields().indexFromName('Substation')
                    subcodeIdx = feat.fields().indexFromName('SubCode')
                    updateMap[feat.id()] = {subIdx: sub}
                    updateMap[feat.id()] = {subcodeIdx: subcode}
                    
                provider.changeAttributeValues( updateMap )

        table.removeSelection()
        fedtable = BasicOps.pDataTable("SysFeeder")
        searchString = "Substation = '" + sub + "' AND Feeder = '" + fed + "'"
        request = QgsFeatureRequest().setFilterExpression(searchString)
        pCursor = fedtable.getFeatures(request)

        if fedtable.selectedFeatureCount() == 0:
            caps = fedtable.dataProvider().capabilities()
            if caps & QgsVectorDataProvider.AddFeatures:
                feat = QgsFeature(fedtable.pendingFields())
		feat.setAttribute('Substation', sub)
		feat.setAttribute('Feeder', fed)
		feat.setAttribute('FedCode', fedcode)
		(res, outFeats) = fedtable.dataProvider().addFeatures([feat])

	    elif fedtable.selectedFeatureCount() > 0:
                updateMap = {}
                provider = fedtable.dataProvider()
                for feat in pCursor:
                    subIdx = feat.fields().indexFromName('Substation')
                    fedIdx = feat.fields().indexFromName('Feeder')
                    fedcodeIdx = feat.fields().indexFromName('FedCode')
                    updateMap[feat.id()] = {subIdx: sub}
                    updateMap[feat.id()] = {fedIdx: fed}
                    updateMap[feat.id()] = {fedcodeIdx: fedcode}
                        
                provider.changeAttributeValues( updateMap )
        fedtable.removeSelection()
