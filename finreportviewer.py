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

from frmReportViewer import *
import resources

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class frmReportViewer_dialog(QDialog, Ui_frmReport):
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

        self.cmdPrint.clicked.connect(self.printReport)
        self.cmdHelp.clicked.connect(self.onHelp)
        self.cmdClose.clicked.connect(self.onClose)

    def printReport(self):
        inputfile = extensionProject.reportfile
        reportName = self.sub + '_' + self.fed +'_' + extensionProject.ProjectNumber
        outfile = os.path.dirname(__file__) + "/AnalysisResult/"+reportName+"_"+"ConstructionCost.pdf"
        if os.path.exists(outfile):
            os.remove(outfile)
        web = self.webView
        printer = QtGui.QPrinter()
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setPageSize(QtGui.QPrinter.A4)
        printer.setOrientation(QtGui.QPrinter.Landscape)
        printer.setColorMode(QtGui.QPrinter.Color)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(outfile)
        web.print_(printer)
        QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "Report Generated into the AnalysisResult folder under the plugin root folder.")

    def getConnection(self):
        condb = psycopg2.connect(user = self.usr, host = self.hst, password = self.paswrd, dbname = self.dbase)
        condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return condb

    def getcursor(self):
        con = self.getConnection()
        cur = con.cursor()
        return cur

    def onClose(self):
        self.close()

    def onHelp(self):
        QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "U N D E R   C O N S T R U C T I O N !!!")