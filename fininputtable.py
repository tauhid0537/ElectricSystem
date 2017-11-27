from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import csv
import sys
import os
import qgis
import numbers

from datetime import datetime

from utility import *
import utility

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/FinancialAnalysis")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")

from frmInputTable import *
import resources

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class frmInputTable_dialog(QDialog, Ui_frmInputTable):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.usr = basicOps.usrname
        self.dbase = basicOps.dbasename
        self.hst = basicOps.hostname
        self.paswrd = basicOps.password
        self.sub = basicOps.substation
        self.fed = basicOps.feeder
        self.tablename = None

        self.tblView = self.tableView
        self.tblModel = QtGui.QStandardItemModel(self)
        self.tblView.setModel(self.tblModel)

        model = QStandardItemModel()
        self.treeView.setModel(model)
        self.treeView.setUniformRowHeights(True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(os.path.dirname(__file__)+"/Resources/FormIcons/fininputtab.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        mainNode = QStandardItem('Input Tables')
        mainNode.setIcon(icon)

        iconNode1 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/fincashflow.png')
        subNode1 = QStandardItem('Cash Flow Parameters')
        subNode1.setIcon(iconNode1)

        iconNode2 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/finconcost.png')
        subNode2 = QStandardItem('Construction Cost')
        subNode2.setIcon(iconNode2)

        iconNode3 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/fincontar.png')
        subNode3 = QStandardItem('Consumer and Tarrif')
        subNode3.setIcon(iconNode3)

        iconNode4 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/finaddtarrif.png')
        subNode4 = QStandardItem('Additional Revenue')
        subNode4.setIcon(iconNode4)

        iconNode5 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/findisloss.png')
        subNode5 = QStandardItem('Distribution Loss')
        subNode5.setIcon(iconNode5)

        iconNode6 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/finexpense.png')
        subNode6 = QStandardItem('Expense')
        subNode6.setIcon(iconNode6)

        iconNode7 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/finhhgrowth.png')
        subNode7 = QStandardItem('Household Growth')
        subNode7.setIcon(iconNode7)

        iconNode8 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/finsubsidy.png')
        subNode8 = QStandardItem('Subsidy')
        subNode8.setIcon(iconNode8)

        mainNode.appendRow([subNode1])
        mainNode.appendRow([subNode2])
        mainNode.appendRow([subNode3])
        mainNode.appendRow([subNode4])
        mainNode.appendRow([subNode5])
        mainNode.appendRow([subNode6])
        mainNode.appendRow([subNode7])
        mainNode.appendRow([subNode8])
        model.appendRow(mainNode)

        #self.cmdEdit.clicked.connect(self.getText)
        self.cmdSave.clicked.connect(self.savedata)
        self.cmdClose.clicked.connect(self.onClose)
        self.treeView.clicked.connect(self.showTable)

    def getConnection(self):
        condb = psycopg2.connect(user = self.usr, host = self.hst, password = self.paswrd, dbname = self.dbase)
        condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return condb

    def getcursor(self):
        con = self.getConnection()
        cur = con.cursor()
        return cur

    def splitTable(self, tbllayername):
        name = tbllayername.split('.')
        if name is True:
            return name[0], name[1]

    def showTable(self):
        index = self.treeView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index).text()

        if item == 'Cash Flow Parameters':
            self.getTable('fin_cashflow_parameters')
        elif item == 'Construction Cost':
            self.getTable('fin_construction_cost')
        elif item == 'Consumer and Tarrif':
            self.getTable('fin_consumer_tariff')
        elif item == 'Additional Revenue':
            self.getTable('fin_additional_revenue')
        elif item == 'Distribution Loss':
            self.getTable('fin_distribution_loss')
        elif item == 'Expense':
            self.getTable('fin_expense')
        elif item == 'Household Growth':
            self.getTable('fin_households')
        elif item == 'Subsidy':
            self.getTable('fin_subsidy')

    def getTable(self, tablename):
        self.tblModel.clear()
        sql = "select * from sysinp.%s" %tablename

        tabledb = self.getTableinfo(tablename)
        self.tblModel.setHorizontalHeaderLabels(tabledb.split(","))
        cur = self.getcursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for t, row in enumerate(rows):
            for y, col in enumerate(row):
                txt = str(col)
                item = QStandardItem(txt)
                self.tblModel.setItem(t,y,item)

        self.tblView.setModel(self.tblModel)

    def getModelData(self, model):
        modelData = []
        data = []
        text = None
        for row in range(model.rowCount()):
            data.append([])
            for col in range(model.columnCount()):
                index = model.index(row, col)
                d = model.data(index)
                if d != None:
                    num = self.is_number(d)
                    if not num:
                        data[row].append("'" + str(d) + "'")
                    else:
                        data[row].append(str(d))
                else:
                    data[row].append("''")
            finalRow = ",".join(data[row])
            modelData.append(finalRow)
        return modelData

    def is_number(self, s):
        try:
            float(s) # for int, long, float and complex
        except ValueError:
            return False

        return True

    def inserttabledata(self, tablename, model):

        modelData = self.getModelData(model)
        fieldnames = self.getTableinfo(tablename)
        conn = self.getConnection()
        cur = conn.cursor()
        delsql = 'delete from sysinp.' + tablename
        cur.execute(delsql)
        for data in modelData:
            insert_sql = 'insert into sysinp.' + tablename + ' (' + fieldnames + ') VALUES (' + data + ')'
            cur.execute(insert_sql)
        conn.commit()

    def savedata(self):

        index = self.treeView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index).text()

        if item == 'Cash Flow Parameters':
            self.inserttabledata('fin_cashflow_parameters', self.tblModel)
        elif item == 'Construction Cost':
            self.inserttabledata('fin_construction_cost', self.tblModel)
        elif item == 'Consumer and Tarrif':
            self.inserttabledata('fin_consumer_tariff', self.tblModel)
        elif item == 'Additional Revenue':
            self.inserttabledata('fin_additional_revenue', self.tblModel)
        elif item == 'Distribution Loss':
            self.inserttabledata('fin_distribution_loss', self.tblModel)
        elif item == 'Expense':
            self.inserttabledata('fin_expense', self.tblModel)
        elif item == 'Household Growth':
            self.inserttabledata('fin_households', self.tblModel)
        elif item == 'Subsidy':
            self.inserttabledata('fin_subsidy', self.tblModel)

    def getTableinfo(self, tablename):

        sql = "select column_name from information_schema.columns where table_name ='%s'" %tablename
        cur = self.getcursor()
        cur.execute(sql)
        rows = cur.fetchall()
        text = []
        for row in rows:
            text.append(row[0])
        finaltext = ",".join(text)
        return finaltext

    def getProcess(self):
        index = self.treeView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index).text()

        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Input Table")
        msgBox.setText(item)
        ret = msgBox.exec_()

    def onClose(self):
        self.close()