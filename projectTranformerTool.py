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

from frmAddTransformer import *
from addTransformer import *

class transformerTool(QgsMapTool):
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.canvas = iface.mapCanvas()
        self.iface = iface
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
        self.setLayerName = self.dbase + ": settlement"
        self.strLayerName = self.dbase + ": structure"
        self.villayerName = self.dbase + ": village"
        self.lodlayerName = self.dbase + ": loadCenter"

        self.setProName = self.dbase + ": " + self.sub + "-" + self.fed + "-settlement-project-" + extensionProject.ProjectNumber
        self.strProName = self.dbase + ": " + self.sub + "-" + self.fed + "-structure-project-" + extensionProject.ProjectNumber
        self.cenProName = self.dbase + ": " + self.sub + "-" + self.fed + "-village-project-" + extensionProject.ProjectNumber
        self.trnProName = self.dbase + ": " + self.sub + "-" + self.fed + "-pole-project-" + extensionProject.ProjectNumber
        self.linProName = self.dbase + ": " + self.sub + "-" + self.fed + "-line-project-" + extensionProject.ProjectNumber

        transForm = frmAddTransformer_dialog(self.iface)
        transForm.txtPro.setText(basicOps.usrname)
        transForm.txtPro.setDisabled(True)
        transForm.txtDatabase.setText(basicOps.dbasename)
        transForm.txtDatabase.setDisabled(True)
        transForm.txtSub.setText(basicOps.substation)
        transForm.txtSub.setDisabled(True)
        transForm.txtFed.setText(basicOps.feeder)
        transForm.txtFed.setDisabled(True)
        transForm.txtProNum.setText(extensionProject.ProjectNumber)
        transForm.txtProNum.setDisabled(True)
        trnSize = self.transformerMinMaxSize()

        transForm.txtMinTrn.setText(str(trnSize[0]))
        transForm.txtMaxTrn.setText(str(trnSize[1]))

        transForm.exec_()


    def reset(self,  emitSignal = False):
        pass

    def powerDemand(self, consumer, consumption):
        pd = consumer *(1 - (0.4 * consumer) + 0.4 * pow((pow(consumer, 2) + 40), 0.5)) * (0.0059256 * pow(consumption, 0.885))
        return pd

    def refresh_layers(self):
        for layer in qgis.utils.iface.mapCanvas().layers():
            layer.triggerRepaint()

    def transformerMinMaxSize(self):
        minSize = 0
        maxSize = 0
        vol = str(extensionProject.LineVoltage)
        splitVol = vol.split(".")
        volt = splitVol[0]
        strselwhrClause = "item = 'Equipment' AND type = 'Transformer' AND voltage = '" + volt + "'"
        tableName = "sysinp.fin_construction_cost"
        sql = """with qr1 as(select CAST((COALESCE(size,'0')) AS INTEGER) size  from  """ + tableName + """ where """ + strselwhrClause + """) select min(size), max(size) from qr1"""
        cur = self.getcursor()
        cur.execute(sql)
        row = cur.fetchone()
        minSize = row[0]
        maxSize = row[1]
        return minSize, maxSize

    def getTrnsformerSizeList(self):
        trnlist = []
        vol = str(extensionProject.LineVoltage)
        splitVol = vol.split(".")
        volt = splitVol[0]
        strselwhrClause = "item = 'Equipment' AND type = 'Transformer' AND voltage = '" + volt + "'"
        sql = "select CAST((COALESCE(size,'0')) AS INTEGER) size  from  sysinp.fin_construction_cost where " + strselwhrClause
        cur = self.getcursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            trnlist.append(row[0])
        return trnlist

    def getConnection(self):
        condb = psycopg2.connect(user = self.usr, host = self.hst, password = self.paswrd, dbname = self.dbase)
        condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return condb

    def getcursor(self):
        con = self.getConnection()
        cur = con.cursor()
        return cur

    def checkAllLayers(self, householdSource):
        message = None
        check = False
        bsOps = utility.basicOps()
        if householdSource == "settlement":
            if (bsOps.checkLayer(self.lineLayerName) == True and
            bsOps.checkLayer(self.poleLayerName) == True and
            bsOps.checkLayer(self.setLayerName) == True and
            bsOps.checkLayer(self.trnProName) == True and
            bsops.checkLayer(self.linProName) == True and
            bsOps.checkLayer(self.setProName) == True):
                check = True
            else:
                message = "The Following Layers Must Exist in the Map:\n\nFeeder Line\r\nFeeder Pole\r\nSettlement\r\nProject Line\r\nProject Pole\r\nProject Settlement"
        elif householdSource == "structure":
            if (bsOps.checkLayer(self.lineLayerName) == True and
            bsOps.checkLayer(self.poleLayerName) == True and
            bsOps.checkLayer(self.strLayerName) == True and
            bsOps.checkLayer(self.trnProName) == True and
            bsOps.checkLayer(self.linProName) == True and
            bsOps.checkLayer(self.strProName) == True):
                check = True
                message = None
            else:
                message = "The Following Layers Must Exist in the Map:\n\nFeeder Line\r\nFeeder Pole\r\nStructure\r\nProject Line\r\nProject Pole\r\nProject Structure"
        elif householdSource == "village":
            if (bsOps.checkLayer(self.lineLayerName) == True and
            bsOps.checkLayer(self.poleLayerName) == True and
            bsOps.checkLayer(self.villayerName) == True and
            bsOps.checkLayer(self.trnProName) == True and
            bsops.checkLayer(self.linProName) == True and
            bsOps.checkLayer(self.cenProName) == True):
                check = True
            else:
                message = "The Following Layers Must Exist in the Map: \n\nFeeder Line\r\nFeeder Pole\r\nVillage Area\r\nProject Line\r\nProject Load Center"
        else:
            message = "Unknown Household Data Source"
        return check, message

    def getProNum(self):
        projectNumber = None
        layers = qgis.utils.iface.mapCanvas().layers()
        for layer in layers:
            name = layer.name()
            if "project" in name:
                fullName = name.split('-')
                projectNumber = fullName[4].strip()
        return projectNumber

    def transformerOnStructure(self, x, y, dist):
        cur = self.getcursor()
        totalHH = 0
        totalStr = 0
        sql2 = """with qr1 as(
        select ST_Buffer(ST_GeomFromText('POINT(""" + x + ' ' + y + """)',3857),"""+ str(dist) + """) geom)
        select count(*) from """+ extensionProject.lbTablename +""" a inner join qr1 b on ST_Within(a.geom, b.geom)"""
        cur.execute(sql2)
        rows2 = cur.fetchall()
        for row2 in rows2:
            totalStr = totalStr + row2[0]
        hhdensql = "select percentage from sysinp.fin_households where item = 'Household Ratio'"
        cur.execute(hhdensql)
        row = cur.fetchone()
        totalHH = round((totalStr * (row[0]/100)), 0)
        return totalHH

    def getConsumerkVA(self, totalHH):
        hhsql = "select percentage from sysinp.fin_households where item = 'Potential Household'"
        cur = self.getcursor()
        cur.execute(hhsql)
        row = cur.fetchone()
        totalConsumer = totalHH * (row[0]/100)

        sql = "select consumer, ratio, ini_consumption from sysinp.fin_consumer_tariff"
        cur.execute(sql)
        rows = cur.fetchall()

        kVA = 0
        rs = 0
        sc = 0
        lc = 0
        li = 0
        si = 0
        pb = 0
        ag = 0
        st = 0
        rsCon = 0
        scCon = 0
        lcCon = 0
        siCon = 0
        liCon = 0
        pbCon = 0
        agCon = 0
        stCon = 0

        for row in rows:
            if row[0] == 'RS_Con':
                rs = rs + round(totalConsumer * (row[1])/100)
                rsCon =  rsCon + row[2]
            elif row[0] == 'SC_Con':
                sc = sc + round(totalConsumer * (row[1])/100)
                scCon = scCon + row[2]
            elif row[0] == 'LC_Con':
                lc = lc + round(totalConsumer * (row[1])/100)
                lcCon = lcCon + row[2]
            elif row[0] == 'LI_Con':
                li = li + round(totalConsumer * (row[1])/100)
                liCon = liCon + row[2]
            elif row[0] == 'SI_Con':
                si = si + round(totalConsumer * (row[1])/100)
                siCon = siCon + row[2]
            elif row[0] == 'PB_Con':
                pb = pb + round(totalConsumer * (row[1])/100)
                pbCon = pbCon + row[2]
            elif row[0] == 'AG_Con':
                ag = ag + round(totalConsumer * (row[1])/100)
                agCon = agCon + row[2]
            elif row[0] == 'ST_Con':
                st = st + round(totalConsumer * (row[1])/100)
                stCon = stCon + row[2]

        avgCon = ((rs * rsCon) + (sc * scCon) + (lc * lcCon) + (si * siCon) + (li * liCon) + (pb * pbCon) + (ag * agCon) + (st * stCon))/totalConsumer
        kW = self.powerDemand(totalConsumer, avgCon)
        #QMessageBox.information(self.iface.mainWindow(),"Test Tool","kW is: " + str(kW))
        kVA = kW/0.9

        return rs, sc, lc, si, li, pb, ag, st, kVA

    def checkRow(self, cur, table, searchString):
        hasRow = False
        sql = "select * from "+ table+ "where " + searchString
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if row[0] != None:
                hasRow = True
        return hasRow

    def canvasPressEvent(self, event):
        #QMessageBox.information(self.iface.mainWindow(),"Test Tool",self.lineLayerName + " , "+ self.strLayerName + " , "+ self.trnProName + "!!!")
        #checkLayers = self.checkAllLayers(extensionProject.HouseholdSource)
        #msg = checkLayers[1]

        #if msg is not None:
        #    QMessageBox.information(self.iface.mainWindow(),"Test Tool", msg)
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

        conn = self.getConnection()
        cur = conn.cursor()

        sql = "select last_value from exprojects."+ extensionProject.PoleTableName +"_seq"
        cur.execute(sql)
        rows = cur.fetchall()
        newNumber = 0
        for row in rows:
            lstNumber = row[0]
            newNumber = lstNumber + 1
        transID = "pro-" + str(extensionProject.ProjectNumber) + "-trn-" + str(newNumber)
        poleID = "del-d2b-pro-" + str(extensionProject.ProjectNumber) + "-pole-" + str(newNumber)

        totalHousehold = self.transformerOnStructure(xx, yy, extensionProject.BufferDistance)
        #QMessageBox.information(self.iface.mainWindow(),"Test Tool","Total Household for connection: " + str(totalHousehold))

        gConkVA = self.getConsumerkVA(totalHousehold)
        rs = gConkVA[0]
        sc = gConkVA[1]
        lc = gConkVA[2]
        si = gConkVA[3]
        li = gConkVA[4]
        pb = gConkVA[5]
        ag = gConkVA[6]
        st = gConkVA[7]
        kVA = gConkVA[8]
        cons = str(kVA) + "," + str(rs) + "," + str(sc) + "," + str(lc) + "," + str(si) + "," + str(li) + "," + str(pb) + "," + str(st)

        if kVA < extensionProject.MinimumTransformerkVA:
            QMessageBox.information(self.iface.mainWindow(),"Test Tool","Proposed Transformer size {0} kVA is less than ".format(str(kVA))+ str(extensionProject.MinimumTransformerkVA) + " kVA\n\nPlease increase buffer size and try again")
        elif kVA > extensionProject.MaximumTransformerkVA:
            QMessageBox.information(self.iface.mainWindow(),"Test Tool","Proposed Transformer size {0} kVA is greater than ".format(str(kVA))+ str(extensionProject.MaximumTransformerkVA) + " kVA\n\nPlease decrease buffer size and try again")
        else:
            bsops = utility.basicOps()
            fedcode = bsops.getFedCode(cur, self.sub, self.fed)
            subcode = bsops.getSubCode(cur, self.sub)
            poletablename = "exprojects." + extensionProject.PoleTableName

            trnSize = self.transformerMinMaxSize()
            minTrn = trnSize[0]
            maxSize = trnSize[1]
            searchkVA = kVA
            currentkVA = minTrn
            currentDiff = abs(currentkVA - searchkVA)
            trnlist = self.getTrnsformerSizeList()

            for t in trnlist:
                diff = abs(t - searchkVA)
                if diff < currentDiff:
                    currentDiff = diff
                    currentkVA = t
            allValue = str(round(currentkVA))
            trValue = allValue.split('.')
            transkVA = int(trValue[0])
            if transkVA >= minTrn:
                sql3 = """INSERT INTO """ + poletablename + """ (substation, feeder, pole_use, pole_phase, equip_type, equip_id, equip_phase,equip_unit, equip_size, rs_con, sc_con, lc_con,
                si_con, li_con, pb_con, ag_con, st_con, geom)
                VALUES('"""+self.sub+ """','""" + self.fed + """',
                'Primary','""" + extensionProject.PhaseConfiguration + """',1,'Transformer','"""+transID +"""','R-Y-B',"""+ str(transkVA) + ""","""+ str(rs) + """,""" + str(sc) + """
                ,""" + str(lc) + ""","""+ str(si)+""","""+str(li)+""","""+str(pb)+""","""+str(ag)+""","""+str(st)+""",ST_GeomFromText('POINT(""" + xx + ' ' + yy + """)',3857));"""
                cur.execute(sql3)
                conn.commit()

            buffTableName = "exprojects." + extensionProject.BufferTableName
            checksql = 'select * from ' + buffTableName
            cur.execute(checksql)
            whereClause = "equip_id = '"+transID + "'"
            buff = str(extensionProject.BufferDistance)
            splitbuff = buff.split(".")
            bufferdist = splitbuff[0]

            if cur.rowcount == 0:
                sql4 ="""INSERT INTO """ +buffTableName + """(project_no,buff_dist, equip_id, geom)
                select '""" + str(extensionProject.ProjectNumber) + """' as project_no, '""" + bufferdist + """' as buff_dist, '""" + transID + """' as equip_id, ST_Buffer(geom, """ + str(extensionProject.BufferDistance) + """) as geom
                from """+ poletablename + """ where """ + whereClause + ";"
                cur.execute(sql4)
                conn.commit()
            else:
                sql3 = """INSERT INTO """ + buffTableName + """( project_no, buff_dist, equip_id, geom)
                with qr1 as(
                select ST_Union(a.geom) as geom from """ + buffTableName + """ a inner join """ + poletablename + """ b on
                ST_Intersects(ST_Buffer(b.geom, """ + str(extensionProject.BufferDistance) + """),a.geom) where b.""" + whereClause+ """)
                select '""" + str(extensionProject.ProjectNumber) + """' as project_no, '""" + bufferdist + """' as buff_dist, a.equip_id,
                ST_Difference(ST_Buffer(a.geom,""" + str(extensionProject.BufferDistance) + """),b.geom) as diff_geom
                from """+ poletablename + """ a left join qr1 b on ST_Intersects(ST_Buffer(a.geom,""" + str(extensionProject.BufferDistance) + """),b.geom)
                where a.""" + whereClause + """;"""
                cur.execute(sql3)
                conn.commit()

            structuretablename = "exprojects." + extensionProject.HHSourceTableName
            lbStructureTableName = extensionProject.lbTablename

            sql5 = """INSERT INTO """ + structuretablename + """(household, structure, geom)
            select a.structure, a.household, a.geom
            from """ + lbStructureTableName + """ a left join """ + buffTableName + """ b on ST_Within(a.geom, b.geom)
            where b.equip_id = '""" + transID + "';"
            cur.execute(sql5)
            conn.commit()

            self.refresh_layers()