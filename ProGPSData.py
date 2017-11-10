from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import csv
import sys
import os
import math
import json

import sqlite3

from pyproj import Proj, transform

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ProcessFieldData")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")

import utility
from utility import *

from frmGPSData import *
import resources

class frmGPSData_dialog(QDialog, Ui_frmGPSData):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.usr = basicOps.usrname
        self.hst = basicOps.hostname
        self.dbase = basicOps.dbasename
        self.pas = basicOps.password

        self.tabs = QtGui.QTabWidget(self)
        self.tabs = self.tabWidget
        self.lineView = self.dgvLine
        self.lineModel = QtGui.QStandardItemModel(self)
        self.poleView = self.dgvPole
        self.poleModel = QtGui.QStandardItemModel(self)
        self.work = None
        self.i = self.tabWidget.currentIndex()

        self.poleView.setModel(self.poleModel)
        self.lineView.setModel(self.lineModel)

        self.getPoleData()
        self.getlineData()

        self.tabs.currentChanged.connect(self.onTabChange)
        self.cmdGPSSave.clicked.connect(self.dataSave)
        self.cmdCreateFeature.clicked.connect(self.createFeat)
        self.cmdClose.clicked.connect(self.onClose)
        #self.cmdGPSEdit.clicked.connect(self.gpsEdit)

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def onTabChange(self):
        if self.i == 0:
            self.work ="p"

        elif self.i == 1:
            self.work = "l"

        return self.work

    def gpsEdit(self):
        if self.i == 0:
            self.getPoleData()
        elif i == 1:
            self.getlineData()

    def createFeat(self):
        if self.tabWidget.currentIndex() == 0:
            self.savePoleTopgsql()
        if self.tabWidget.currentIndex() == 1:
            self.saveLineTopgsql()

    def dataSave(self):
        if self.tabWidget.currentIndex() == 0:
            self.savePoleData()
        if self.tabWidget.currentIndex() == 1:
            self.saveLineData()

    def populatePoleTable(self):
        self.poleModel.clear()
        poleDB = self.getTableRowName(basicOps.sqlitedb, "vw_Pole_Data")
        self.poleModel.setHorizontalHeaderLabels(poleDB.split(","))
        cur = self.sqliteCursor(basicOps.sqlitedb)
        columnsqry = "PRAGMA table_info(vw_Pole_Data)"
        cur.execute(columnsqry)
        headerNames = []
        for header in cur.fetchall():
            headerNames.append(header[1])
        numberOfColumns = len(cur.fetchall())
        polesql = "select * from vw_Pole_Data"
        cur.execute(polesql)
        data = cur.fetchall()
        k = -1
        for i, row in enumerate(data):
            r = []
            for j, col in enumerate(row):
                item = QStandardItem(col)
                r.append(col)
            self.poleModel.appendRow(r)
        self.poleView.setModel(self.poleModel)

    def sqliteCursor(self,db):
        con = sqlite3.connect(db)
        c= con.cursor()
        return c

    def createLineTable(self, db, qry):
        c = self.sqliteCursor(db)
        c.execute("drop table if exists line_table")
        sql = "create table line_table as " + qry
        c.execute(qry)

    def convertEPSG436ToEPSG3857(self, lon, lat):
        x = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), lon, lat)
        return x

    def refresh_layers(self):
        for layer in qgis.utils.iface.mapCanvas().layers():
            layer.triggerRepaint()

    def getPoleData(self):

        polesql ="""select '%s' as Substation, '%s' as Feeder, latitude, longitude, GPS_No, Feeders_on_Pole,
        Pole_Number, Pole_Use, Pole_Phase, Pole_Height, Pole_Class, Pole_Structure, Pole_Fitting, Pole_Guy, Pole_GuyType, Pole_GuyAg, Pole_Status, Equip_Type,
        Ref_Pole, Equip_ID, Equip_Unit, Equip_Mount, Equip_Size, Equip_Phase, Equip_Status, Equip_Use, Trans_Ref, rs_con, sc_con, lc_con, si_con, li_con, pb_con,
        ag_con, st_con, Location, Data_Source,Remarks FROM vw_Pole_Data""" %(basicOps.substation, basicOps.feeder)

        db = basicOps.sqlitedb
        cur = self.sqliteCursor(db)
        sql = "create table if not exists pole_table as " + polesql
        cur.execute(sql)

        poleDB = self.getTableRowName(basicOps.sqlitedb, "pole_table")
        self.poleModel.setHorizontalHeaderLabels(poleDB.split(","))

        getsql = """select Substation, Feeder, latitude, longitude, GPS_No, Feeders_on_Pole, Pole_Number, Pole_Use,
        Pole_Phase, Pole_Height, Pole_Class, Pole_Structure, Pole_Fitting, Pole_Guy, Pole_GuyType, Pole_GuyAg,
        Pole_Status, Equip_Type, Ref_Pole, Equip_ID, Equip_Unit, Equip_Mount, Equip_Size, Equip_Phase,
        Equip_Status, Equip_Use, Trans_Ref, rs_con, sc_con, lc_con, si_con, li_con, pb_con, ag_con, st_con,
        Location, Data_Source, Remarks from pole_table"""
        cur.execute(getsql)
        rows = cur.fetchall()
        for t, row in enumerate(rows):
            for y, col in enumerate(row):
                item = QStandardItem(col)
                self.poleModel.setItem(t,y,item)

        self.poleView.setModel(self.poleModel)

    def savePoleData(self):
        model = self.poleModel
        db = basicOps.sqlitedb
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("delete from pole_table")

        data = []
        text = None
        for row in range(model.rowCount()):
            data.append([])
            for col in range(model.columnCount()):
                index = model.index(row, col)
                d = model.data(index)
                if d != None:
                    s= d.strip("'")
                    check = s.isnumeric()
                    if not check:
                        data[row].append("'" + str(d) + "'")
                    else:
                        t = d.strip("'")
                        if t.lstrip('-').isnumeric():
                            data[row].append(str(d).strip("'"))
                else:
                    data[row].append("0")
            finalRow = ",".join(data[row])
            insertsql = """insert into pole_table(Substation, Feeder, latitude, longitude, GPS_No, Feeders_on_Pole,
            Pole_Number, Pole_Use, Pole_Phase, Pole_Height, Pole_Class, Pole_Structure, Pole_Fitting, Pole_Guy, Pole_GuyType, Pole_GuyAg, Pole_Status, Equip_Type,
            Ref_Pole, Equip_ID, Equip_Unit, Equip_Mount, Equip_Size, Equip_Phase, Equip_Status, Equip_Use, Trans_Ref, rs_con, sc_con, lc_con, si_con, li_con, pb_con,
            ag_con, st_con, Location, Data_Source,Remarks) values("""+ finalRow+ """)"""
            cur.execute(insertsql)
        con.commit()
        QMessageBox.information(self.iface.mainWindow(),"Process Pole","Pole Processed")

    def getlineData(self):
        linesql = """select S_E, '%s' as Substation, '%s' as Feeder, latitude, longitude,
        Line_Alignment, Line_Voltage, Line_Type, Section_ID, Phase, Trans_Code, Sec_Con, Trans_Ref, Con_Size_1, Con_Size_2, Con_Size_3, Con_Size_N,
        Line_Status, Data_Source, Remarks from vw_line_data""" %(basicOps.substation, basicOps.feeder)

        db = basicOps.sqlitedb
        cur = self.sqliteCursor(db)
        sql = "create table if not exists line_table as " + linesql
        cur.execute(sql)
        lineDB = self.getTableRowName(basicOps.sqlitedb, "line_table")
        self.lineModel.setHorizontalHeaderLabels(lineDB.split(","))

        cur.execute("select * from line_table")
        rows = cur.fetchall()
        for t, row in enumerate(rows):
            for y, col in enumerate(row):
                item = QStandardItem(col)
                self.lineModel.setItem(t,y,item)

        self.lineView.setModel(self.lineModel)

    def saveLineData(self):
        model = self.lineModel
        db = basicOps.sqlitedb
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("delete from line_table")

        data = []
        text = None
        for row in range(model.rowCount()):
            data.append([])
            for col in range(model.columnCount()):
                index = model.index(row, col)
                d = model.data(index)
                if d != None:
                    s= d.strip("'")
                    check = s.strip("'").isnumeric()
                    if not check:
                        data[row].append("'" + str(d) + "'")
                    else:
                        t = d.strip("'")
                        if t.lstrip('-').isnumeric():
                            data[row].append(str(d).strip("'"))
                else:
                    data[row].append("0")
            finalRow = ",".join(data[row])
            insertsql = """insert into line_table(S_E, Substation, Feeder, longitude, latitude, Line_Alignment, Line_Voltage,
            Line_Type, Section_ID, Phase, Trans_Code, Sec_Con, Trans_Ref, Con_Size_1, Con_Size_2, Con_Size_3, Con_Size_N,
            Line_Status, Data_Source, Remarks) values("""+ finalRow+ """)"""
            try:
                cur.execute(insertsql)
            except sqlite3.Error, e:
                QMessageBox.information(self.iface.mainWindow(),"Process Line",e.message)
        con.commit()
        QMessageBox.information(self.iface.mainWindow(),"Process Line","Line Processed")

    def convertGPSNo(self, gps):
        gpsNo = None
        date = self.txtDate.text()
        splitdate = date.split("/")
        gpsNo = splitdate[2]+splitdate[1]+splitdate[0]+str(gps).zfill(3)
        return gpsNo
    def getString(self, val):
        if val is None:
            return "0"
        elif val == "":
            return "0"
        else:
            return str(val)

    def getNumber(self, val):
        if val is None:
            return float(0)
        else:
            return float(val)

    def getCursor(self, usr, hst, pas, db):
        cur = None
        try:
            condb = psycopg2.connect(user = usr, host = hst, password = pas, dbname = db)
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = condb.cursor()
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        return cur

    def savePoleTopgsql(self):
        condb = psycopg2.connect(user = self.usr, host = self.hst, password = self.pas, dbname = self.dbase)
        condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = condb.cursor()
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, basicOps.substation, basicOps.feeder)
        subcode = bsops.getSubCode(cur, basicOps.substation)
        poletablename = subcode + "_" + fedcode + "_pole"

        db = basicOps.sqlitedb
        sqliteCon = sqlite3.connect(db)
        sqliteCur = sqliteCon.cursor()
        csql = """select Substation, Feeder, GPS_No, Feeders_on_Pole, Pole_Number, Pole_Use, Pole_Phase, Pole_Height, Pole_Class, Pole_Structure, Pole_Fitting,
        Pole_Guy, Pole_GuyType, Pole_GuyAg, Pole_Status, Equip_Type, Ref_Pole, Equip_ID, Equip_Unit, Equip_Mount, Equip_Size, Equip_Phase, Equip_Status,
        Equip_Use, Trans_Ref, rs_con, sc_con, lc_con, si_con, li_con, pb_con, ag_con, st_con, Location, Data_Source, Remarks, longitude, latitude from pole_table
        """
        sqliteCur.execute(csql)
        sqliteRows = sqliteCur.fetchall()
        for srow in sqliteRows:
            x =self.convertEPSG436ToEPSG3857(float(srow[36]), float(srow[37]))
            d = "'"+self.getString(srow[0])+ "','" + self.getString(srow[1]) + "','" + self.getString(self.convertGPSNo(srow[2])) + "'," + self.getString(srow[3]) + ",'" + self.getString(srow[4]) + "','" + self.getString(srow[5]) + "','" + self.getString(srow[6]) + "'," + self.getString(srow[7]) + ",'" + self.getString(srow[8]) +"""'
            ,'"""+ self.getString(srow[9]) + "','" + self.getString(srow[10]) + "','" + self.getString(srow[11]) + "','" + self.getString(srow[12]) + "','" + self.getString(srow[13]) + "','" + self.getString(srow[14]) + "','" + self.getString(srow[15]) + "','" + self.getString(srow[16]) + "','" + self.getString(srow[17]) + """'
            ,"""+ self.getString(srow[18]) + ",'" + self.getString(srow[19]) + "','" + self.getString(srow[20]) + "','" + self.getString(srow[21]) + "','" + self.getString(srow[22]) + "','" + self.getString(srow[23]) + "','" + self.getString(srow[24]) + "'," + self.getString(srow[25]) + "," + self.getString(srow[26]) + """
            ,""" + self.getString(srow[27]) + "," + self.getString(srow[28]) + "," + self.getString(srow[29]) + "," + self.getString(srow[30]) + "," + self.getString(srow[31]) + "," + self.getString(srow[32]) + ",'" + self.getString(srow[33]) + "','" + self.getString(srow[34]) + "','" + self.getString(srow[35]) + "'"

            poleinsertsql = """INSERT INTO esystems.""" + poletablename + """(
            substation, feeder, gps_no, fed_on_pole, pole_number,
            pole_use, pole_phase, pole_height, pole_class, pole_structure,
            pole_fitting, pole_guy, pole_guytype, pole_guyag, pole_status,
            equip_type, reference_pole, equip_id, equip_unit, equip_mount,
            equip_size, equip_phase, equip_status, equip_use, trans_ref,
            rs_con, sc_con, lc_con, si_con, li_con, pb_con, ag_con, st_con,
            location, data_source, remarks, geom) VALUES(""" + d + """, ST_GeomFromText('POINT(""" + str(x[0]) + ' ' + str(x[1]) + """)',3857))"""
            cur.execute(poleinsertsql)

        condb.commit()
        self.addPoleLayer()

    def saveLineTopgsql(self):
        condb = psycopg2.connect(user = self.usr, host = self.hst, password = self.pas, dbname = self.dbase)
        condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = condb.cursor()
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, basicOps.substation, basicOps.feeder)
        subcode = bsops.getSubCode(cur, basicOps.substation)
        linetablename = subcode + "_" + fedcode + "_line"

        db = basicOps.sqlitedb
        sqliteCon = sqlite3.connect(db)
        sqliteCur = sqliteCon.cursor()
        csql = """select S_E, Substation, Feeder, latitude, longitude, Line_Alignment, Line_Voltage, Line_Type, Section_ID, Phase, Trans_Code, Sec_Con, Trans_Ref,
        Con_Size_1, Con_Size_2, Con_Size_3, Con_Size_N, Line_Status, Data_Source, Remarks from line_table
        """
        sqliteCur.execute(csql)
        sqliteRows = sqliteCur.fetchall()
        linegps = []
        lineinsertsql = []
        d = None
        i = 0
        #dic = {}
        while(i < len(sqliteRows)):
        #for srow in sqliteRows:
            x =self.convertEPSG436ToEPSG3857(float(sqliteRows[i][4]), float(sqliteRows[i][3]))
            if sqliteRows[i][0] == 'S':
                if len(linegps) > 1:
                    xy = ",".join(linegps)
                    insertsql = """INSERT INTO esystems.""" + linetablename + """(
                    substation, feeder, line_align, line_voltage, line_type,
                    section_id, phase, trans_code, sec_con, trans_ref, con_size_1,
                    con_size_2, con_size_3, con_size_n, line_status, data_source,
                    remarks, geom) VALUES( """ + d + """,ST_GeomFromText('LINESTRING(""" + xy + """)',3857));"""
                    lineinsertsql.append(insertsql)
                    #QMessageBox.information(self.iface.mainWindow(),"Process Line", lineinsertsql+"\n" +str(len(linegps)))
                    #cur.execute(lineinsertsql)
                    linegps = []
                    d = None
                else:
                    linegps.append(str(x[0]) + " " + str(x[1]))
                    d = "'" + self.getString(sqliteRows[i][1]) + "','" + self.getString(sqliteRows[i][2]) + "','" + self.getString(sqliteRows[i][5]) + "','" + self.getString(sqliteRows[i][6]) + "','" + self.getString(sqliteRows[i][7]) + "','" + self.getString(sqliteRows[i][8]) +"""'
                    ,'"""+ self.getString(sqliteRows[i][9]) + "','" + self.getString(sqliteRows[i][10]) + "','" + self.getString(sqliteRows[i][11]) + "','" + self.getString(sqliteRows[i][12]) + "'," + self.getString(sqliteRows[i][13]) + "," + self.getString(sqliteRows[i][14]) + """
                    ,""" + self.getString(sqliteRows[i][15]) + "," + self.getString(sqliteRows[i][16]) + ",'" + self.getString(sqliteRows[i][17]) + """'
                    ,'"""+ self.getString(sqliteRows[i][18]) + "','" + self.getString(sqliteRows[i][19]) + "'"
            else:
                linegps.append(str(x[0]) + " " + str(x[1]))
            QMessageBox.information(self.iface.mainWindow(),"Process Line", str(i)+","+ str(sqliteRows[i][0]))
            i += 1
            #QMessageBox.information(self.iface.mainWindow(),"Process Line", str(i))
            QMessageBox.information(self.iface.mainWindow(),"Process Line", str(len(lineinsertsql)))
        #condb.commit()
        #self.addLineLayer()

    def addPoleLayer(self):
        sub = basicOps.substation
        fed = basicOps.feeder

        cur = self.getCursor(self.usr, self.hst, self.pas, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)
        poletablename = subcode + "_" + fedcode + "_pole"
        poleLayerName = self.dbase + ": " + sub + "-" + fed + "-pole"
        layers = qgis.utils.iface.mapCanvas().layers()
        foundlayer = False

        uri = QgsDataSourceURI()
        uri.setConnection(self.hst,"5432",self.dbase,self.usr,self.pas)
        uri.setDataSource("esystems",poletablename,"geom")
        polelayer = QgsVectorLayer(uri.uri(), poleLayerName, "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(polelayer)
        self.refresh_layers()

    def addLineLayer(self):
        sub = basicOps.substation
        fed = basicOps.feeder

        cur = self.getCursor(self.usr, self.hst, self.pas, self.dbase)
        bsOps = utility.basicOps()
        fedcode = bsOps.getFedCode(cur, sub, fed)
        subcode = bsOps.getSubCode(cur, sub)
        linetablename = subcode + "_" + fedcode + "_line"
        lineLayerName = self.dbase + ": " + sub + "-" + fed + "-line"
        layers = qgis.utils.iface.mapCanvas().layers()
        foundlayer = False

        uri = QgsDataSourceURI()
        uri.setConnection(self.hst, "5432", self.dbase, self.usr, self.pas)
        uri.setDataSource("esystems", linetablename, "geom")
        linelayer = QgsVectorLayer(uri.uri(), lineLayerName, "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(linelayer)
        self.refresh_layers()

    def getTableRowName(self, db, table):
        c= self.sqliteCursor(db)
        c.execute("PRAGMA table_info(" + table + ")")
        rows = c.fetchall()
        text = []
        for row in rows:
            text.append(row[1])
        finaltext = ",".join(text)
        return finaltext

    def onClose(self):
        self.close()



