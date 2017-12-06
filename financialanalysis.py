from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *

from qgis.core import *
from qgis.gui import *
import qgis

#locale.setlocale(locale.LC_ALL, 'en_US')

import os
import sys
import csv
from os import listdir
from os.path import isfile, join
import numpy

import math

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import psycopg2

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ToolForms")

import utility
from utility import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/FinancialAnalysis")
from frmFinance import *
from frmInputTable import *
from fininputtable import *
from frmReportViewer import *
from finreportviewer import *

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
#import resources

class frmFinance_dialog(QDialog, Ui_frmFinance):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.proNum = None
        self.proName = None
        self.proSite = None
        self.proLineType = None
        self.proLineVol = None
        self.proPopSource = None
        self.proConSize = None
        self.proAvgLineLength = None

        self.usr = basicOps.usrname
        self.dbase = basicOps.dbasename
        self.hst = basicOps.hostname
        self.paswrd = basicOps.password
        self.sub = basicOps.substation
        self.fed = basicOps.feeder

        self.bufftablename = None
        self.linetablename = None
        self.poletablename = None
        self.structuretablename= None
        self.bufflayername = None
        self.linelayername = None
        self.polelayername = None
        self.structurelayername= None
        self.extCurrency = None

        sql = "select sysphase from sysinp.phase_con"
        cur = self.getcursor()
        cur.execute(sql)
        row = cur.fetchone()
        self.basePhase = row[0]

        self.tblView = self.tableView
        self.tblModel = QtGui.QStandardItemModel(self)
        self.tblView.setModel(self.tblModel)

        self.getTableforModel()

        self.cmbProSite.clear()
        self.cmbProSite.addItem('Urban')
        self.cmbProSite.addItem('Rural')
        self.cmbProSite.setCurrentIndex(-1)

        self.cmbPrLineType.clear()
        self.cmbPrLineType.addItem('Primary Distribution')
        self.cmbPrLineType.addItem('Secondary Distribution')
        self.cmbPrLineType.setCurrentIndex(-1)

        self.cmbPrLineVolt.clear()
        self.cmbPrLineVolt.addItem('33000')
        self.cmbPrLineVolt.addItem('11000')
        self.cmbPrLineVolt.addItem('400')
        self.cmbPrLineVolt.setCurrentIndex(-1)

        self.cmbScConSize.clear()
        cur = self.getcursor()
        sql = "select size from sysinp.fin_construction_cost where type = 'Secondary Distribution'"
        cur.execute(sql)
        fedlist = []
        rows = cur.fetchall()
        for row in rows:
            fedlist.append(row[0])

        self.cmbScConSize.addItems(fedlist)
        self.cmbScConSize.setCurrentIndex(-1)

        self.cmdInputTable.clicked.connect(self.openInputTable)
        self.cmdCalCon.clicked.connect(self.onProjectCost)
        self.cmdRepCon.clicked.connect(self.showProjectCostReport)
        self.cmdCalFin.clicked.connect(self.fianncialAnalysis)
        self.cmdCreatePro.clicked.connect(self.createProject)
        self.cmdAddPro.clicked.connect(self.addProLayers)
        self.cmdDelPro.clicked.connect(self.deleteSelectedTableRow)
        self.cmdClose.clicked.connect(self.onClose)

    def printer(self):
        printer = QtGui.QPrinter()
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setPageSize(QtGui.QPrinter.A4)
        printer.setColorMode(QtGui.QPrinter.Color)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName('report.pdf')
        self.page().mainFrame().print_(printer)

    def onProjectCost(self):
        poleTable = "exprojects." + self.poletablename
        lineTable = "exprojects." + self.linetablename
        extensionProject.SecondaryConductor = self.cmbScConSize.currentText()
        extensionProject.SecondaryLength = float(self.txtAvgTrLen.text())

        self.calculateConstructionCost(poleTable, lineTable,"sysinp.fin_construction_cost","sysinp.fin_households","sysinp.fin_subsidy", "sysinp.fin_cashflow_parameters")
        self.createConstructionCostReport()

        proname = self.txtPro.text()
        frmReport = frmReportViewer_dialog(self.iface)
        frmReport.txtPro.setText(proname)
        frmReport.txtPBS.setText(basicOps.dbasename)
        frmReport.txtSub.setText(basicOps.substation)
        frmReport.txtFed.setText(basicOps.feeder)
        frmReport.webView.setHtml('')
        htmlfile = extensionProject.reportfile
        local_url = QUrl.fromLocalFile(htmlfile)
        frmReport.webView.load(local_url)
        frmReport.exec_()

    def showProjectCostReport(self):
        sql = "select "
        self.createConstructionCostReport()
        reportName = self.sub + '_' + self.fed +'_' + extensionProject.ProjectNumber
        #cur = self.getcursor()

        htmlfilepath = os.path.dirname(__file__) + "/AnalysisResult/"+reportName+"_"+"ConstructionCost.html"
        if os.path.exists(htmlfilepath):
            proname = self.txtPro.text()
            frmReport = frmReportViewer_dialog(self.iface)
            frmReport.txtPro.setText(proname)
            frmReport.txtPBS.setText(basicOps.dbasename)
            frmReport.txtSub.setText(basicOps.substation)
            frmReport.txtFed.setText(basicOps.feeder)
            frmReport.webView.setHtml('')
            htmlfile = htmlfilepath
            local_url = QUrl.fromLocalFile(htmlfile)
            frmReport.webView.load(local_url)
            frmReport.exec_()
        else:
            QMessageBox.warning(self.iface.mainWindow(),"Financial Analysis", "Construction Cost Report does not Exist\n\nPlease Calculate Construction Cost First")
        #extensionProject.reportfile = htmlfilepath
        #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "Cost Report Created")

    def fianncialAnalysis(self):
        conn = self.getConnection()
        cur = conn.cursor()
        poleTable = "exprojects." + self.poletablename
        lineTable = "exprojects." + self.linetablename
        extensionProject.SecondaryConductor = self.cmbScConSize.currentText()
        extensionProject.SecondaryLength = float(self.txtAvgTrLen.text())

        inCostTab = "sysinp.fin_construction_cost"
        inConsumerTab = "sysinp.fin_consumer_tariff"
        inDistLossTab = "sysinp.fin_distribution_loss"
        inExpenseTab = "sysinp.fin_expense"
        inHouseRatTab = "sysinp.fin_households"
        inSubsidyTab = "sysinp.fin_subsidy"
        inCashFlowPar = "sysinp.fin_cashflow_parameters"
        inOtherRevTab = "sysinp.fin_additional_revenue"

        outCostTab = "exprojects.fout_construction_cost"
        outConsumerTab = "exprojects.fout_consumer_finance"
        outSummaryTab = "exprojects.fout_project_summery"

        self.calculateConstructionCost(poleTable,lineTable,inCostTab,inHouseRatTab,inSubsidyTab,inCashFlowPar)

        #Cash Flow Parameters
        extensionProject.AnalysisYear = self.getVal(inCashFlowPar, "value", "category", "Analysis Term")
        extensionProject.MidAnalysisYear = self.getVal(inCashFlowPar, "value", "category", "Analysis Mid Term")
        extensionProject.InterestYear = self.getVal(inCashFlowPar, "value", "category", "Interest Payment Year")
        discountRate = (self.getVal(inCashFlowPar, "value", "category", "Discount Rate")) / 100
        if extensionProject.AnalysisYear == 0:
            QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "Cash Flow Analysis Year is Zero\n\nPlease Update Cash Flow Parameters Table")
        else:
            #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "Analysis Year: " + str(extensionProject.AnalysisYear))
            #Construction cost for this project
            totConstCost = self.getVal(outCostTab, "amount", "item","Total Construction Cost")

            #Distribution Loss
            distLoss = (self.getVal(inDistLossTab, "technical", "region", extensionProject.HouseholdType)) / 100
            colEff = (self.getVal(inDistLossTab, "collection", "region", extensionProject.HouseholdType)) / 100

            #Subsidy
            subCap = (self.getVal(inSubsidyTab, "value", "type", "Capital Subsidy")) / 100
            subIni = (self.getVal(inSubsidyTab, "value", "type", "Operational Subsidy-First Year")) / 100
            subMid = (self.getVal(inSubsidyTab, "value", "type", "Operational Subsidy-Upto Mid Year")) / 100
            subFin = (self.getVal(inSubsidyTab, "value", "type", "Operational Subsidy-Upto Final Year")) / 100
            subSrv = self.getVal(inSubsidyTab, "value", "type", "Service Drop Subsidy")

            #Household Ratio
            hhRatio = (self.getVal(inHouseRatTab, "percentage", "item", "Household Ratio")) / 100
            hhGrMidYear = (self.getVal(inHouseRatTab, "percentage", "item", "Household Growth Upto Mid Year")) / 100
            hhGrFinYear = (self.getVal(inHouseRatTab, "percentage", "item", "Household Growth Upto Final Year")) / 100
            hhPotential = (self.getVal(inHouseRatTab, "percentage", "item", "Potential Household")) / 100

            # Clear Output Tables
            cur.execute("delete from " + outConsumerTab)
            cur.execute("delete from " + outSummaryTab)

            #Get Line Length of project line in km
            linesql = " select st_length(geom) length from "+ lineTable
            cur.execute(linesql)
            row = cur.fetchone()
            lineLength = round(row[0]/1000,3)

            #Consumption
            dicConsumption = {}

            rs = self.getVal(inConsumerTab, "ini_consumption", "consumer", "RS_Con")
            sc = self.getVal(inConsumerTab, "ini_consumption", "consumer", "SC_Con")
            lc = self.getVal(inConsumerTab, "ini_consumption", "consumer", "LC_Con")
            si = self.getVal(inConsumerTab, "ini_consumption", "consumer", "SI_Con")
            li = self.getVal(inConsumerTab, "ini_consumption", "consumer", "LI_Con")
            pb = self.getVal(inConsumerTab, "ini_consumption", "consumer", "PB_Con")
            ag = self.getVal(inConsumerTab, "ini_consumption", "consumer", "AG_Con")
            st = self.getVal(inConsumerTab, "ini_consumption", "consumer", "ST_Con")

            dicConsumption["RS_Con"] = rs
            dicConsumption["SC_Con"] = sc
            dicConsumption["LC_Con"] = lc
            dicConsumption["SI_Con"] = si
            dicConsumption["LI_Con"] = li
            dicConsumption["PB_Con"] = pb
            dicConsumption["AG_Con"] = ag
            dicConsumption["ST_Con"] = st

            #Initial Penetration
            dicIniPen = {}

            penRS = (self.getVal(inConsumerTab, "ini_penetration", "consumer", "RS_Con")) / 100
            penSC = (self.getVal(inConsumerTab, "ini_penetration", "consumer", "SC_Con")) / 100
            penLC = (self.getVal(inConsumerTab, "ini_penetration", "consumer", "LC_Con")) / 100
            penSI = (self.getVal(inConsumerTab, "ini_penetration", "consumer", "SI_Con")) / 100
            penLI = (self.getVal(inConsumerTab, "ini_penetration", "consumer", "LI_Con")) / 100
            penPB = (self.getVal(inConsumerTab, "ini_penetration", "consumer", "PB_Con")) / 100
            penAG = (self.getVal(inConsumerTab, "ini_penetration", "consumer", "AG_Con")) / 100
            penST = (self.getVal(inConsumerTab, "ini_penetration", "consumer", "ST_Con")) / 100

            dicIniPen["RS_Con"] = penRS
            dicIniPen["SC_Con"] = penSC
            dicIniPen["LC_Con"] = penLC
            dicIniPen["SI_Con"] = penSI
            dicIniPen["LI_Con"] = penLI
            dicIniPen["PB_Con"] = penPB
            dicIniPen["AG_Con"] = penAG
            dicIniPen["ST_Con"] = penST

            #Get total potential consumer by category from proposed pole layer
            dicConsumer = {}
            totRSCon = round(self.getSumValLayer(poleTable, "RS_Con"), 0)
            totSCCon = round(self.getSumValLayer(poleTable, "SC_Con"), 0)
            totLCCon = round(self.getSumValLayer(poleTable, "LC_Con"), 0)
            totSICon = round(self.getSumValLayer(poleTable, "SI_Con"), 0)
            totLICon = round(self.getSumValLayer(poleTable, "LI_Con"), 0)
            totPBCon = round(self.getSumValLayer(poleTable, "PB_Con"), 0)
            totAGCon = round(self.getSumValLayer(poleTable, "AG_Con"), 0)
            totSTCon = round(self.getSumValLayer(poleTable, "ST_Con"), 0)

            totalHousehold = totRSCon + totSCCon + totLCCon + totSICon + totLICon + totPBCon + totAGCon + totSTCon

            dicConsumer["RS_Con"] = totRSCon * penRS
            dicConsumer["SC_Con"] = totSCCon * penSC
            dicConsumer["LC_Con"] = totLCCon * penLC
            dicConsumer["SI_Con"] = totSICon * penSI
            dicConsumer["LI_Con"] = totLICon * penLI
            dicConsumer["PB_Con"] = totPBCon * penPB
            dicConsumer["AG_Con"] = totAGCon * penAG
            dicConsumer["ST_Con"] = totSTCon * penST

            #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "Total Consumer: " + str(totalHousehold))

            # Service Drop
            dicServiceDrop = {}
            sdcostRS = self.getVal(inConsumerTab, "rate", "", "RS_Con")
            sdcostSC = self.getVal(inConsumerTab, "rate", "category", "SC_Con")
            sdcostLC = self.getVal(inConsumerTab, "rate", "category", "LC_Con")
            sdcostSI = self.getVal(inConsumerTab, "rate", "category", "SI_Con")
            sdcostLI = self.getVal(inConsumerTab, "rate", "category", "LI_Con")
            sdcostPB = self.getVal(inConsumerTab, "rate", "category", "PB_Con")
            sdcostAG = self.getVal(inConsumerTab, "rate", "category", "AG_Con")
            sdcostST = self.getVal(inConsumerTab, "rate", "category", "ST_Con")

            dicServiceDrop["RS_Con"] = sdcostRS
            dicServiceDrop["SC_Con"] = sdcostSC
            dicServiceDrop["LC_Con"] = sdcostLC
            dicServiceDrop["SI_Con"] = sdcostSI
            dicServiceDrop["LI_Con"] = sdcostLI
            dicServiceDrop["PB_Con"] = sdcostPB
            dicServiceDrop["AG_Con"] = sdcostAG
            dicServiceDrop["ST_Con"] = sdcostST

            #Consumer Alias
            dicConsumerAlias = {}
            conAliassql = "select category, category_alias from " + inCostTab + " where item = 'Consumer'"
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                contype = row[0]
                consAlias = row[1]
                dicConsumerAlias[contype] = consAlias

            # year 0 Calculation: Subsidy
            self.updateRow(outConsumerTab, "item = 'Total Expense'", "Year0", totConstCost)
            capSubsidyY0 = round((totConstCost *subCap), 0)
            self.updateRow(outConsumerTab, "item = 'Capital Subsidy'", "Year0", capSubsidyY0)
            self.updateRow(outConsumerTab, "item = 'Total Subsidy'", "Year0", capSubsidyY0)
            self.updateRow(outConsumerTab, "item = 'Total Revenue'", "Year0", capSubsidyY0)
            netRevSub = capSubsidyY0 - totConstCost
            self.updateRow(outConsumerTab, "item = 'Net Revenue'", "Year0", netRevSub)
            capSubRest = totConstCost - capSubsidyY0

            #Cashflow into an array
            cashFlow = [extensionProject.AnalysisYear]

            # Start Loop
            yearHousehold = 0
            y = 0
            while(y <= extensionProject.AnalysisYear):
                y= y + 1
                if y == 1:
                    yearHousehold = totalHousehold
                else:
                    if extensionProject.MidYearAnalysis != 0:
                        if y <= extensionProject.MidYearAnalysis:
                            yearHousehold = yearHousehold * (1 + hhGrMidYear)
                        else:
                            yearHousehold = yearHousehold * (1 + hhGrFinYear)
                    else:
                        yearHousehold = yearHousehold * (1 + hhGrFinYear)
            newConsumer = 0
            yearConsumer = 0
            yearPowUsage = 0
            yearTechLoss = 0
            yearSrvDrop = 0
            yearPowRev = 0
            yearConRev = 0
            yearFixRev = 0
            yearPurPower = 0

            consumerTarsql = """SELECT consumer, ini_penetration, mid_penetration, fin_penetration,
            mid_consumer_gr, fin_consumer_gr, ini_consumption, mid_consumption_gr, fin_consumption_gr, connnect_charge, fixed_charge, energy_charge, ratio from """ + inConsumerTab
            cur.execute(consumerTarsql)
            contarRows = cur.fetchall()
            for tarrow in contarRows:
                conType = tarrow[0]
                conRatio = tarrow[12] / 100
                iniPen = tarrow[1] / 100
                midPen = tarrow[2] / 100
                finPen = tarrow[3] / 100

                midConGr = tarrow[7] / 100
                finConGr = tarrow[8] / 100

                conChargeReg = tarrow[9]
                conChargeSub = tarrow[9]
                fixedCharge = tarrow[10]
                powCharge = tarrow[11]

                newConsump = 0
                powUsage = 0
                techLoss = 0
                srvDropCost = 0
                powRev = 0
                conRev = 0
                fixRev = 0
                consumpGrowth = 0

                dicConsumerAlias[conType]
                calPen = dicIniPen[conType]
                oldConsumer = dicConsumer[conType]
                oldConsump = dicConsumption[conType]
                srvDropRate = dicServiceDrop[conType]

                if y <= subSrv:
                    srvDropRate = 0
                    conChargeReg = conChargeSub
                if y == 1:
                    newConsumer = totalHousehold * iniPen * conRatio
                    yearConsumer = yearConsumer + newConsumer
                    calPen = iniPen
                    newConsump = oldConsump

                    powUsage = (newConsumer * newConsump) * 12
                    techLoss = distLoss * (powUsage / (1 - distLoss))

                    yearPowUsage = yearPowUsage + powUsage
                    yearTechLoss = yearTechLoss + techLoss

                    #Revenue
                    powRev = powUsage * powCharge;
                    conRev = newConsumer * conChargeReg;
                    fixRev = newConsumer * fixCharge * 12;

                    yearPowRev = yearPowRev + powRev
                    yearConRev = yearConRev + conRev
                    yearFixRev = yearFixRev + fixRev
                else:
                    if extensionProject.MidYearAnalysis != 0:
                        if y <= extensionProject.MidYearAnalysis:
                            midYear = extensionProject.MidAnalysisYear - 1
                            midYearDiff = 1 / midYear
                            if calPen == 0:
                                conGrowth = pow((midPen / 1),midYearDiff) - 1
                                calPen = calPen * (1 + conGrowth)
                            else:
                                conGrowth = pow((midPen / iniPen),midYearDiff) - 1
                                calPen = calPen * (1 + conGrowth)
                            consumpGrowth = midConGr
                        else:
                            finYear = extensionProject.AnalysisYear - extensionProject.MidYearAnalysis
                            finYearDiff = 1 / finYear
                            if calPen == 0:
                                conGrowth = pow((finPen / 1),finYearDiff) - 1
                                calPen = calPen * (1 + conGrowth)
                            else:
                                conGrowth = pow((finPen / midPen),finYearDiff) - 1
                                calPen = calPen * (1 + conGrowth)
                            consumpGrowth = finConGr
                    else:
                        finYear = extensionProject.AnalysisYear - 1
                        finYearDiff = 1 / finYear
                        if calPen == 0:
                            conGrowth = pow((finPen / 1),finYearDiff) - 1
                            calPen = calPen * (1 + conGrowth)
                        else:
                            conGrowth = pow((finPen / iniPen),finYearDiff) - 1
                            calPen = calPen * (1 + conGrowth)
                        consumpGrowth = finConGr

                    newConsumer = yearHousehold * calPen * conRatio
                    addConsumer = newConsumer - oldConsumer
                    yearConsumer = yearConsumer + newConsumer

                    #Consumption
                    newConsump = oldConsump + (oldConsump * consumpGrowth)
                    powUsage = newConsumer * newConsump * 12
                    techLoss = distLoss * (powUsage / (1 - distLoss))
                    srvDropCost = addConsumer * srvDropRate

                    yearPowUsage = yearPowUsage + powUsage
                    yearTechLoss = yearTechLoss + techLoss
                    yearSrvDrop = yearSrvDrop + srvDropCost

                    #Revenue
                    powRev = powUsage * powCharge
                    conRev = addConsumer * conChargeReg
                    fixRev = newConsumer * fixCharge * 12

                    yearPowRev = yearPowRev + powRev
                    yearConRev = yearConRev + conRev
                    yearFixRev = yearFixRev + fixRev

                del dicConsumer[conType]
                dicConsumer[conType] = newConsumer
                del dicConsumption[conType]
                dicConsumption[conType] = newConsump
                del dicIniPen[conType]
                dicIniPen[conType] = calPen

                typCons = consAlias + " Consumption"
                typUsag = consAlias + " Usage"
                typSrvD = consAlias + " Service Drop"
                typPowR = consAlias + " Power Revenue"
                typConC = consAlias + " Connection Charge"
                typFixC = consAlias + " Fixed Charge"

                self.updateRow(outConsumerTab, "item = '" + consAlias + "'","Year" + str(y), round(newConsumer, 0))
                self.updateRow(outConsumerTab, "item = '" + typCons + "'","Year" + str(y), round(newConsump, 0))
                self.updateRow(outConsumerTab, "item = '" + typUsag + "'","Year" + str(y), round(powUsage, 0))
                self.updateRow(outConsumerTab, "item = '" + typSrvD + "'","Year" + str(y), round(srvDropCost, 0))
                self.updateRow(outConsumerTab, "item = '" + typPowR + "'","Year" + str(y), round(powRev, 0))
                self.updateRow(outConsumerTab, "item = '" + typConC + "'","Year" + str(y), round(conRev, 0))
                self.updateRow(outConsumerTab, "item = '" + typFixC + "'","Year" + str(y), round(fixRev, 0))
            yearPurPower = yearPowUsage + yearTechLoss
            self.updateRow(outConsumerTab, "item = 'Total Consumer'","Year" + str(y), round(yearConsumer, 0))
            self.updateRow(outConsumerTab, "item = 'Total Energy Usage'","Year" + str(y), round(yearPowUsage, 0))
            self.updateRow(outConsumerTab, "item = 'Technical Loss'","Year" + str(y), round(yearTechLoss, 0))
            self.updateRow(outConsumerTab, "item = 'Power Purchase'","Year" + str(y), round(yearPurPower, 0))
            self.updateRow(outConsumerTab, "item = 'Total Service Drop Expense'","Year" + str(y), round(yearSrvDrop, 0))
            self.updateRow(outConsumerTab, "item = 'Total Power Revenue'","Year" + str(y), round(yearPowRev, 0))
            self.updateRow(outConsumerTab, "item = 'Total Connection Charge'","Year" + str(y), round(yearConRev, 0))
            self.updateRow(outConsumerTab, "item = 'Total Fixed Charge'","Year" + str(y), round(yearFixRev, 0))

            #Add to Summary Table
            self.updateRow(outSummaryTab, "item = 'Total Consumer'","Year" + str(y), round(yearConsumer, 0))
            self.updateRow(outConsumerTab, "item = 'Power Purchase'","Year" + str(y), round(yearPurPower, 0))

            #expense
            expensesql = "SELECT category, unit, value FROM " + inExpenseTab
            cur.execute(expensesql)
            exrows = cur.fetchall()
            powerRate = 0
            totalOpCost = 0
            for exrow in exrows:
                costCate = exrow[0]
                costUnit = exrow[1]
                costValu = exrow[2]

                if "Power Cost" in costCate:
                    powerRate = costValu
                costItem = 0
                if "Interest" in costCate:
                    if y < extensionProject.InterestYear:
                        costItem = 0
                    else:
                        if "Percentage of Construction" in costUnit:
                            costItem = round((totConstCost * (costValu / 100)), 0)
                        if "Line" in costUnit:
                            costItem = round((lineLength * costValu), 0)
                else:
                    if "kWH Purchased" in costUnit:
                        costItem = round((yearPurPower * costValu), 0)
                    if "kWH Sold" in costUnit:
                        costItem = round((yearPowUsage * costValu), 0)
                    if "Consumer" in costUnit:
                        costItem = round((yearConsumer * costValu), 0)
                    if "Percentage of Construction" in costUnit:
                        costItem = round((totConstCost * (costValu / 100)), 0)
                    if "Line" in costUnit:
                        costItem = round((lineLength * costValu), 0)
                    if "Percentage of Power Cost" in costUnit:
                        powerCost = yearPurPower * powerRate
                        costItem = round((powerCost * (costValu / 100)), 0)
                totalOpCost = totalOpCost + costItem
                self.updateRow(outConsumerTab, "item = '" + costCate + "'", "Year" + str(y), costItem)
            self.updateRow(outConsumerTab, "item = 'Total Operating Expense'", "Year" + str(y), totalOpCost)
            totalExpense = round((totalOpCost + yearSrvDrop), 0)
            self.updateRow(outConsumerTab, "item = 'Total Expense'", "Year" + str(y), totalExpense)

            #Subsidy
            subYear = round((capSubRest / extensionProject.AnalysisYear), 0)
            self.updateRow(outConsumerTab, "item = 'Capital Subsidy'", "Year" + str(y), subYear)
            subIniYear = 0
            subMidYear = 0
            subFinYear = 0
            self.updateRow(outConsumerTab, "item = 'First Year'", "Year" + str(y), subIniYear)
            self.updateRow(outConsumerTab, "item = 'Upto Mid Year'", "Year" + str(y), subMidYear)
            self.updateRow(outConsumerTab, "item = 'Upto Final Year'", "Year" + str(y), subFinYear)
            totalSubsidy = subYear + subIniYear + subMidYear + subFinYear
            self.updateRow(outConsumerTab, "item = 'Total Subsidy'", "Year" + str(y), totalSubsidy)

            #Collection Efficiency
            totalColEff = ((yearPowRev + yearFixRev) * colEff) - (yearPowRev + yearFixRev)
            self.updateRow(outConsumerTab, "item = 'Collection Efficiency'", "Year" + str(y), round(totalColEff, 0))

            #Revenue from Power
            totalPowerRelRev = yearPowRev + yearFixRev + yearConRev + totalColEff

            #Other Revenue
            totalAddRev = 0
            othrsql = "SELECT category, unit, value  FROM " + inOtherRevTab
            cur.execute(othrsql)
            othrrows = cur.fetchall()
            for otrrow in othrrows:
                revCate = otrrow[0]
                revUnit = otrrow[1]
                revValue = otrrow[2]
                revItem = 0
                if "Percentage of Total Revenue" in revUnit:
                    revItem = totalPowerRelRev * (revValue / 100)
                if "Percentage of Power Revenue" in revUnit:
                    revItem = yearPowRev * (revValue / 100)
                self.updateRow(outConsumerTab, "item = '" + revCate + "'", "Year" + str(y), round(revItem, 0))
                totalAddRev = totalAddRev + revItem
            self.updateRow(outConsumerTab, "item = 'Total Additional Revenue'", "Year" + str(y), round(totalAddRev, 0))
            totalRevenue = totalPowerRelRev + totalAddRev
            self.updateRow(outConsumerTab, "item = 'Total Revenue'", "Year" + str(y), round(totalRevenue, 0))
            netRevenue = totalRevenue - totalExpense
            self.updateRow(outConsumerTab, "item = 'Net Revenue'", "Year" + str(y), round(netRevenue, 0))

            self.updateRow(outSummaryTab, "item = 'Total Expense'", "Year" + str(y), round(totalExpense, 0))
            self.updateRow(outSummaryTab, "item = 'Total Revenue'", "Year" + str(y), round(totalRevenue, 0))
            self.updateRow(outSummaryTab, "item = 'Net Revenue'", "Year" + str(y), round(netRevenue, 0))

            cashFlow[y-1] = netRevenue
        NPV = round(npv(discountRate, cashFlow), 0)
        self.updateRow(outSummaryTab, "item = 'Net Present Value (NPV)'", "Year1", NPV)
        self.updateRow(outConsumerTab, "item = 'Net Present Value (NPV)'", "Year1", NPV)
        QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "NPV- "+str(NPV))





    def updateRow(self, table, searchString, updateField, updateValue):
        sql = "UPDATE " + table + " SET "+updateField+" = '" + updateValue + "' WHERE " + searchString
        conn = self.getConnection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def getSumValLayer(self, table, searchfield):
        sql3 = "select sum(" + searchfield + ") consumer from " + table
        cur = self.getcursor()
        cur.execute(sql3)
        row = cur.fetchone()
        val = row[0]
        return val


    def calculateConstructionCost(self, propoletable, prolinetable, conCostTab, hhGrowthTab, subsidyTab, cashFlowTab):
        dicConsumerAlias = {}
        dicConSrvDrop = {}
        sql = "select category, category_alias, rate from " + conCostTab + " where item = 'Consumer'"
        conn = self.getConnection()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            contype = row[0]
            conalias = row[1]
            consrvdrop = row[2]
            dicConsumerAlias[contype] = conalias
            dicConSrvDrop[contype] = consrvdrop

        cur.execute("delete from exprojects.fout_construction_cost")
        cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, item, type) VALUES ('Project Information', 'Substation', '" + self.sub + "')")
        cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, item, type) VALUES ('Project Information', 'Feeder', '" + self.fed + "')")
        cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, item, type) VALUES ('Project Information', 'Project Number: ', '" + extensionProject.ProjectNumber + "')")
        cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, item, type) VALUES ('Project Information', 'Project Name', '" + extensionProject.ProjectName + "')")
        cur.execute("INSERT INTO exprojects.fout_construction_cost(separator) VALUES ('')")
        cur.execute("INSERT INTO exprojects.fout_construction_cost(item) VALUES ('Expected Consumer')")

        sql2 = "select category, rate from "+ conCostTab + " where item = 'Consumer'"
        cur.execute(sql2)
        items = cur.fetchall()
        totalConsumer = 0
        totalServiceDrop = 0
        for item in items:
            constype = item[0]
            servdrop = item[1]
            sql3 = "select sum(" + constype + ") consumer from exprojects." + self.poletablename
            cur.execute(sql3)
            consumer = cur.fetchone()
            totalConsumer = totalConsumer + consumer[0]
            srvDrop = round(consumer[0]*servdrop,0)
            totalServiceDrop = totalServiceDrop + srvDrop
            conAlias = dicConsumerAlias[constype]
            if consumer[0] >0 :
                cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, type, quantity) VALUES ('Consumer', '" + conAlias + "', '" + str(consumer[0]) + "')")
        cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, type, quantity) VALUES ('Consumer', 'Total Consumer', '" + str(totalConsumer) + "')")

        totalTrnPrice = 0
        totalNumTrn = 0
        volt = str(extensionProject.LineVoltage)
        volts = volt.split('.')
        voltage = int(volts[0])
        #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", str(voltage)+"v")
        sql4 = "select category, size, rate, unit from " + conCostTab + " where item = 'Equipment' and type = 'Transformer' and voltage = " + str(voltage)
        #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "sql- "+sql4)
        cur.execute(sql4)
        rows2 = cur.fetchall()
        if cur.rowcount > 0:
            cur.execute("INSERT INTO exprojects.fout_construction_cost(separator) VALUES (' ')")
            cur.execute("INSERT INTO exprojects.fout_construction_cost(item) VALUES ('Proposed Equipment')")

            for row2 in rows2:
                allsize = row2[1].split('.')
                trnSize = allsize[0]
                #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "trnize- "+trnSize)
                trnRate = row2[2]
                trnUnit = row2[3]
                trnPhase = row2[0]
                strPhase1 = ""
                strPhase2 = ""
                strPhase3 = ""
                strPhase4 = ""
                strPhase5 = ""
                strPhase6 = ""
                strPhase7 = ""
                numTrn = 0
                phase = utility.phase()

                if trnPhase == "Three Phase":
                    strPhase7 = phase.phase7(self.basePhase)
                    sql5 = "select sum(equip_unit) numTrn from exprojects." + self.poletablename + " where equip_size = '" + trnSize + "' and equip_phase = '" + strPhase7 + "'"
                    #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "sql- "+sql5)
                    cur.execute(sql5)
                    trans = cur.fetchone()
                    if trans[0] is not None:
                        numTrn = numTrn + trans[0]
                elif trnPhase == "Two Phase":
                    strPhase4 = Phase.phase4(self.basePhase)
                    strPhase5 = Phase.phase5(self.basePhase)
                    strPhase6 = Phase.phase6(self.basePhase)
                    sql5 = "select sum(equip_unit) numTrn from exprojects." + self.poletablename + " where equip_size = '" + trnSize + "' and equip_phase = '" + strPhase4 + "' or equip_phase = '" + strPhase5 + "' or equip_phase = '" + strPhase6 + "'"
                    cur.execute(sql5)
                    trans = cur.fetchone()
                    numTrn = trans[0]
                elif trnPhase == "Single Phase":
                    strPhase1 = Phase.phase1(self.basePhase)
                    strPhase2 = Phase.phase2(self.basePhase)
                    strPhase3 = Phase.phase3(self.basePhase)
                    sql5 = "select sum(equip_unit) numTrn from exprojects." + self.poletablename + " where equip_size = '" + trnSize + "' and equip_phase = '" + strPhase1 + "' or equip_phase = '" + strPhase2 + "' or equip_phase = '" + strPhase3 + "'"
                    cur.execute(sql5)
                    trans = cur.fetchone()
                    numTrn = trans[0]

                if numTrn > 0:
                    trnkVA = str(trnSize) + " kVA - " + trnPhase
                    lineV = extensionProject.LineVoltage/1000
                    trnType = str(lineV) + "/0.4 kV"
                    trnPrice = round(numTrn * trnRate, 0)
                    totalNumTrn = totalNumTrn + numTrn

                    allUnit = trnUnit.split(' ')
                    self.extCurrency = allUnit[0]
                    cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, item, type, details, quantity, amount, amount_unit)VALUES ('Equipment', 'Transformer', '"+trnType+"','"+trnkVA+"','"+str(numTrn)+"','"+str(trnPrice)+"','USD')")
                    #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", str(trnPrice))
        else:
            QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "No Transformer Definition Found in Construction Cost Table")
        totalPriCost = 0
        whereClause = "item = 'Electric Line' and type = 'Primary Distribution' and voltage = " + str(voltage)
        sql6 = "select category, size, rate, unit from " + conCostTab + " where " + whereClause
        cur.execute(sql6)
        linerows = cur.fetchall()
        if cur.rowcount > 0:
            cur.execute("INSERT INTO exprojects.fout_construction_cost(separator) VALUES (' ')")
            cur.execute("INSERT INTO exprojects.fout_construction_cost(item) VALUES ('Proposed Line')")
            for linerow in linerows:
                lineSize = linerow[1]
                lineRate = linerow[2]
                lineUnit = linerow[3]
                linePhase = linerow[0]

                lineLen = self.getConductorLineLength(self.linetablename, lineSize, linePhase)
                #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", str(lineRate))
                if lineLen > 0:
                    lineV = extensionProject.LineVoltage / 1000
                    lineType = str(lineV) + " kV Primary Line - " + linePhase
                    lineLength = round(lineLen/1000, 3)
                    linePrice = round(lineLength * lineRate,0)
                    totalPriCost = totalPriCost + linePrice
                    #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", str(self.extCurrency))
                    insertsql ="INSERT INTO exprojects.fout_construction_cost(separator, type, details, quantity,quantity_unit, amount, amount_unit)VALUES ('Electric Line', '"+lineType+"','"+lineSize+"','"+str(lineLength)+"','km','"+str(linePrice)+"', 'USD')"
                    #QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", insertsql)
                    cur.execute(insertsql)
        else:
            QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "No Transformer Definition Found in Construction Cost Table")

        whereClause = "item = 'Electric Line' and type = 'Secondary Distribution' and size = '" + extensionProject.SecondaryConductor + "'"
        sql7 = "select rate, unit from " + conCostTab + " where " + whereClause
        cur.execute(sql7)
        seclinerows = cur.fetchall()
        totalSecCost = 0
        if cur.rowcount > 0:
            for seclinerow in seclinerows:
                seclineRate = seclinerow[0]
                seclineUnit = seclinerow[1]

                secLineLength = round(extensionProject.SecondaryLength * totalNumTrn, 3)
                totalSecCost = totalSecCost + round(seclineRate * secLineLength, 0)
                if totalSecCost > 0:
                    cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, type, details, quantity,quantity_unit, amount, amount_unit)VALUES ('Electric Line', 'Secondary Line','"+extensionProject.SecondaryConductor+"','"+str(secLineLength)+"','km','"+str(totalSecCost)+"','USD')")
        else:
            QMessageBox.information(self.iface.mainWindow(),"Financial Analysis", "No Secondary Line Definition Found in Construction Cost Table")
        if totalServiceDrop > 0:
            cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, type, details, amount, amount_unit)VALUES ('Electric Line', 'Service Drop','-','"+str(totalServiceDrop)+"','USD')")
        #hhGrowthTab, subsidyTab, cashFlowTab
        finYear= self.getVal(cashFlowTab, "value","category","Analysis Term")
        midYear = self.getVal(cashFlowTab, "value","category","Analysis Mid Term")
        subYear =self.getVal(subsidyTab, "value","type","Service Drop Subsidy")
        hhGrMidYear = self.getVal(hhGrowthTab,"percentage", "item", "Household Growth")
        hhGrFinYear = self.getVal(hhGrowthTab,"percentage", "item", "Household Growth")

        srvDropSubsidy = self.calculateServiceDropSubsidy(totalConsumer, hhGrMidYear, hhGrFinYear, subYear, midYear, finYear, dicConSrvDrop)

        if srvDropSubsidy < 0:
            srvDropSubsidy = 0
        if srvDropSubsidy > 0:
            cur.execute("INSERT INTO exprojects.fout_construction_cost(separator) VALUES (' ')")
            typ = "Service Drop Subsidy upto " + str(subYear) + " Year"
            cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, type, details, amount, amount_unit)VALUES ('Subsidy', '"+typ+"','-','"+str(round(srvDropSubsidy))+"','USD')")
        totalConsCost = round((totalTrnPrice + totalServiceDrop + totalPriCost + totalSecCost + srvDropSubsidy), 0)
        if totalConsCost > 0:
            cur.execute("INSERT INTO exprojects.fout_construction_cost(separator) VALUES (' ')")
            cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, item, amount, amount_unit)VALUES ('Project Cost', 'Total Construction Cost','"+str(totalConsCost)+"','USD')")
        perConsumerCost = round((totalConsCost/totalConsumer), 0)
        if perConsumerCost > 0:
            cur.execute("INSERT INTO exprojects.fout_construction_cost(separator) VALUES (' ')")
            cur.execute("INSERT INTO exprojects.fout_construction_cost(separator, item, amount, amount_unit)VALUES ('Project Cost', 'Per Consumer Cost','"+str(perConsumerCost)+"','USD')")
        conn.commit()
        #self.createConstructionCostReport()

    def calculateServiceDropSubsidy(self, yearHH, hhMidGrowth, hhFinGrowth, serviceDropYear, analysisMidYear, analysisFinYear, dicserdrop):
        totalServDropSubsidy = 0
        if serviceDropYear > 0:
            yearServHH = 0
            hhGrMidYear = hhMidGrowth / 100
            hhGrFinYear = hhFinGrowth / 100
            y = 0
            while (y <= serviceDropYear):
                y= y + 1
                if y == 1:
                    yearServHH = yearHH
                else:
                    if analysisMidYear != 0:
                        if y <= analysisMidYear:
                            yearServHH = yearServHH * (1 + hhGrMidYear)
                        else:
                            yearServHH == yearServHH * (1 + hhGrFinYear)
                    else:
                        yearServHH = yearServHH + (1 + hhGrFinYear)
            sql = "SELECT consumer, ini_penetration, mid_penetration, fin_penetration, ratio FROM sysinp.fin_consumer_tariff"
            cur = self.getcursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                conType = row[0]
                iniPen = row[1] / 100
                midPen = row[2] / 100
                finPen = row[3] / 100
                conRatio = row[4] / 100
                calPen = iniPen
                i = 0
                while(i<=serviceDropYear):
                    i = i + 1
                    if i > 1 :
                        if analysisMidYear != 0:
                            if i <= analysisMidYear:
                                midYear = analysisMidYear -1
                                midYearDiff = 1 / midYear
                                if calPen == 0:
                                    conGrowth = pow((midPen/1),midYearDiff) - 1
                                    calPen = calPen * (1 + conGrowth)
                                else:
                                    conGrowth = pow((midPen/iniPen), midYearDiff) - 1
                                    calPen = calPen * (1 + conGrowth)
                            else:
                                finYear = analysisFinYear - analysisMidYear
                                finYearDiff = 1 / finYear
                                if calPen == 0:
                                    conGrowth = pow((finPen/1), finYearDiff) -1
                                    calPen = calPen * (1 + conGrowth)
                                else:
                                    conGrowth = pow((finPen/midPen),finYearDiff) - 1
                                    calPen = calPen * (1 + conGrowth)
                        else:
                            finYear = analysisFinYear -1
                            finYearDiff = 1/finYear
                            if calPen == 0:
                                conGrowth = pow((finPen/1), finYearDiff) -1
                                calPen = calPen * (1 + conGrowth)
                            else:
                                conGrowth = pow((finPen / iniPen), finYearDiff) - 1
                                calPen = calPen * (1 + conGrowth)
                    oldConsumer = yearHH * conRatio
                    newConsumer = yearServHH * calPen * conRatio
                    addConsumer = newConsumer - oldConsumer
                    srvDropRate = dicserdrop[conType]
                    servDropCost = addConsumer * srvDropRate
                    totalServDropSubsidy = totalServDropSubsidy + servDropCost
            return totalServDropSubsidy


    def getVal(self, table, valField, searchfield, searchString):
        sql = "SELECT " + valField + " FROM " + table + " where " + searchfield + " = '" + searchString + "'"
        cur = self.getcursor()
        cur.execute(sql)
        row = cur.fetchone()
        val = row[0]
        return val

    def getConductorLineLength(self, tablename, conductorSize, phase):
        length = 0
        cur = self.getcursor()
        r =None
        sql = None
        if phase == "Three Phase":
            whereClause = "con_size_1 = '" + conductorSize + "'"
            sql = "select sum(st_length(geom)) length from exprojects." + self.linetablename + " where " + whereClause
            cur.execute(sql)
            r = cur.fetchone()
            length = r[0]
        elif phase == "Two Phase":
            whereClause = "con_size_1 = '" + conductorSize + "' AND con_size_2 = '" + conductorSize + "'"
            sql = "select sum(st_length(geom)) length from exprojects." + self.linetablename + " where " + whereClause
            cur.execute(sql)
            r = cur.fetchone()
            length = r[0]
            if length == 0:
                whereClause1 = "con_size_2 = '" + conductorSize + "' AND con_size_3 = '" + conductorSize + "'"
                sql2 = "select sum(st_length(geom)) length from exprojects." + self.linetablename + " where " + whereClause
                cur.execute(sql2)
                r = cur.fetchone()
                length = r[0]
                if length == 0:
                    whereClause2 = "con_size_3 = '" + conductorSize + "' AND con_size_1 = '" + conductorSize + "'"
                    sql3 = "select sum(st_length(geom)) length from exprojects." + self.linetablename + " where " + whereClause
                    cur.execute(sql3)
                    r = cur.fetchone()
                    length = r[0]

        elif phase == "Single Phase":
            whereClause = "con_size_1 = '" + conductorSize + "' or con_size_2 = '" + conductorSize + "'" + "or con_size_2 = '" + conductorSize + "'"
            sql = "select sum(st_length(geom)) length from exprojects." + self.linetablename + " where " + whereClause
            cur.execute(sql)
            r = cur.fetchone()
            length = r[0]
        return length

    def createConstructionCostReport(self):
        msg = None
        reportName = self.sub + '_' + self.fed +'_' + extensionProject.ProjectNumber
        cur = self.getcursor()

        htmlfilepath = os.path.dirname(__file__) + "/AnalysisResult/"+reportName+"_"+"ConstructionCost.html"
        extensionProject.reportfile = htmlfilepath
        htmlfirst = """<html>
        <meta http-equiv='X-UA-Compatible' content='IE=edge' />
        <style type='text/css'>
        BODY
        {
        font-family:'Verdana';
        font-size:8pt;
        margin :2px;
        margin-left:10px;
        margin-right:10px;
        padding: 0px;
        }
        .maintable
        {
        font-family:'Verdana';
        font-size:9px;
        border: 1px solid rgb(138,204,192);
        margin-top:8px;
        margin-bottom:8px;
        width: 100%;
        }
        .maintable .tr1
        {
        background-color:rgb(138,204,192);
        text-align:left;
        font-weight:bold;
        }
        .maintable .tr2
        {
        background-color:rgb(196,231,221);
        text-align:left;
        font-weight:normal;
        }
        .maintable .td1
        {
        border: 0px solid white;
        }
        .maintable .td2
        {
        border: 0px solid white;
        font-weight:normal;
        }
        .maintable .td3
        {
        border: 1px solid white;
        }
        </style>
        <body>
        <table border='0' cellspacing = '0' style='text-align:left;width:100%;border: 0px solid white;'>
        <tr style='Height: 30px;'>
        <td><font size='2' face='Verdana'><b>Expansion Project Construction Cost</b></td>
        </tr>
        </table>
        <table class = 'maintable' border='1' cellspacing='1' cellpadding='2' style='width:100%;'>
        <tr>
        <td class='td3' style = 'width:40%'>
        <b>Project Information</b>
        <table class = 'maintable' border='1' cellspacing='2' cellpadding='3' style='width:98%;'>
        """
        if os.path.exists(htmlfilepath):
            os.remove(htmlfilepath)
        htmlfile = open(htmlfilepath, 'w')
        htmlfile.write(htmlfirst)

        proClause = "separator = 'Project Information'"
        prosql = " select item, type from exprojects.fout_construction_cost where " + proClause
        cur.execute(prosql)
        prorows = cur.fetchall()
        for prorow in prorows:
            itemStr = prorow[0]
            typeStr = prorow[1]
            htmlfile.write("<tr class='tr1'>")
            htmlfile.write("<td class = 'td1' style = 'width:50%'>" + itemStr + "</td>")
            htmlfile.write("<td class = 'td2' style = 'width:50%'>" + typeStr + "</td>")
            htmlfile.write("</tr>")
        htmlfile.write("</table>")

        htmlfile.write("<b>Expected Consumer During Project Construction</b>")
        htmlfile.write("<table class = 'maintable' border='1' cellspacing= '2' cellpadding = '3' style='width:98%;'>")
        htmlfile.write("<tr class='tr1'>")
        htmlfile.write("<th class='td1' style = 'width:50%'>Consumer Type</th>")
        htmlfile.write("<th class='td1' style = 'width:50%'>Number</th>")
        htmlfile.write("</tr>")

        consumerClause = "separator = 'Consumer'"
        csql = " select type, quantity from exprojects.fout_construction_cost where " + consumerClause
        cur.execute(csql)
        consumers = cur.fetchall()
        for consumer in consumers:
            typStr = consumer[0]
            quantitycons = str(consumer[1])
            htmlfile.write("<tr class='tr2'>")
            htmlfile.write("<td class = 'td2'>" + typStr + "</td>")
            htmlfile.write("<td class = 'td2' style='text-align:right'>" + quantitycons + "</td>")
            htmlfile.write("</tr>")
        htmlfile.write("</table>")

        htmlfile.write("<b>Proposed Equipment</b>")
        htmlfile.write("<table class = 'maintable' border='1' cellspacing= '2' cellpadding = '3' style='width:98%;'>")
        htmlfile.write("<tr class='tr1'>")
        htmlfile.write("<th class='td1' style = 'width:20%'>Type</th>")
        htmlfile.write("<th class='td1' style = 'width:20%'>Voltage</th>")
        htmlfile.write("<th class='td1' style = 'width:20%'>Detail</th>")
        htmlfile.write("<th class='td1' style = 'width:20%'>Number</th>")
        htmlfile.write("<th class='td1' style = 'width:20%'>Cost (USD)</th>")
        htmlfile.write("</tr>")

        equipClause = "separator = 'Equipment'"
        eqsql = " select item, type, details, quantity, amount from exprojects.fout_construction_cost where " + equipClause
        cur.execute(eqsql)
        equipments = cur.fetchall()

        for equipment in equipments:
            eitmStr = equipment[0]
            etypStr = equipment[1]
            edetailStr = equipment[2]
            equantityStr = equipment[3]
            ecost = equipment[4]
            htmlfile.write("<tr class='tr2'>")
            htmlfile.write("<td class = 'td2'>" + eitmStr + "</td>")
            htmlfile.write("<td class = 'td2'>" + etypStr + "</td>")
            htmlfile.write("<td class = 'td2'>" + edetailStr + "</td>")
            htmlfile.write("<td class = 'td2' style='text-align:right'>" + str(equantityStr) + "</td>")
            htmlfile.write("<td class = 'td2' style='text-align:right'>" + str(ecost) + "</td>")
            htmlfile.write("</tr>")
        htmlfile.write("</table>")

        htmlfile.write("<b>Proposed Line</b>")
        htmlfile.write("<table class = 'maintable' border='1' cellspacing= '2' cellpadding = '3' style='width:98%;'>")
        htmlfile.write("<tr class='tr1'>")
        htmlfile.write("<th class='td1' style = 'width:25%'>Type</th>")
        htmlfile.write("<th class='td1' style = 'width:25%'>Detail</th>")
        htmlfile.write("<th class='td1' style = 'width:25%'>Length (kM)</th>")
        htmlfile.write("<th class='td1' style = 'width:25%'>Cost (USD)</th>")
        htmlfile.write("</tr>")

        lineClause = "separator = 'Electric Line'"
        linesql = " select type, details, quantity, amount from exprojects.fout_construction_cost where " + lineClause
        cur.execute(linesql)
        lines = cur.fetchall()
        for line in lines:
            typStr = line[0]
            detail = line[1]
            quantity = str(line[2])
            cost = str(line[3])

            htmlfile.write("<tr class='tr2'>")
            htmlfile.write("<td class = 'td2'>" + typStr + "</td>")
            htmlfile.write("<td class = 'td2'>" + detail + "</td>")
            htmlfile.write("<td class = 'td2' style='text-align:right'>" + quantity + "</td>")
            htmlfile.write("<td class = 'td2' style='text-align:right'>" + cost + "</td>")
            htmlfile.write("</tr>")
        htmlfile.write("</table>")

        subsClause = "separator = 'Subsidy'"
        subssql = " select type, amount from exprojects.fout_construction_cost where " + subsClause
        cur.execute(subssql)
        if cur.rowcount > 0:
            subsidys = cur.fetchall()
            htmlfile.write("<b>Connection Subsidy Included in Project Cost</b>")
            htmlfile.write("<table class = 'maintable' border='1' cellspacing= '2' cellpadding = '3' style='width:98%;'>")
            htmlfile.write("<tr class='tr1'>")
            htmlfile.write("<th class='td1' style = 'width:50%'>Cost Head</th>")
            htmlfile.write("<th class='td1' style = 'width:50%'>Cost (USD)</th>")
            htmlfile.write("</tr>")
            for sub in subsidys:
                itemStr = sub[0]
                cost = str(sub[1])
                htmlfile.write("<tr class='tr2'>")
                htmlfile.write("<td class = 'td2'>" + itemStr + "</td>")
                htmlfile.write("<td class = 'td2' style='text-align:right'>" + cost + "</td>")
                htmlfile.write("</tr>")
            htmlfile.write("</table>")

        htmlfile.write("<b>Project Cost</b>")
        htmlfile.write("<table class = 'maintable' border='1' cellspacing= '2' cellpadding = '3' style='width:98%;'>")
        htmlfile.write("<tr class='tr1'>")
        htmlfile.write("<th class='td1' style = 'width:50%'>Cost Head</th>")
        htmlfile.write("<th class='td1' style = 'width:50%'>Cost (USD)</th>")
        htmlfile.write("</tr>")

        costClause = "separator = 'Project Cost'"
        costsql = " select item, amount from exprojects.fout_construction_cost where " + costClause
        cur.execute(costsql)
        costs = cur.fetchall()
        for cost in costs:
            itemStr = cost[0]
            cst = str(cost[1])

            htmlfile.write("<tr class='tr2'>")
            htmlfile.write("<td class = 'td2'>" + itemStr + "</td>")
            htmlfile.write("<td class = 'td2' style='text-align:right'>" + cst + "</td>")
            htmlfile.write("</tr>")
        htmlfile.write("</table>")
        htmlfile.write("</td>")
        htmlfile.write("</tr>")
        htmlfile.write("</table>")
        htmlfile.write("</body>")
        htmlfile.write("</html>")
        htmlfile.close()

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def onClose(self):
        self.close()

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

    def getprojectTableinfo(self):

        sql = "select column_name from information_schema.columns where table_name ='fout_expansion_projects'"
        cur = self.getcursor()
        cur.execute(sql)
        rows = cur.fetchall()
        text = []
        i = -1
        for row in rows:
            i = i + 1
            if i > 0:
                text.append(row[0])
        finaltext = ",".join(text)
        return finaltext

    def getTableforModel(self):
        self.tblModel.clear()
        sql = "SELECT substation, feeder, project_number, project_name, household_source, line_type, line_voltage, household_type FROM exprojects.fout_expansion_projects"

        tabledb = self.getprojectTableinfo()
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

    def createProject(self):
        self.proNum = self.txtProNum.text()
        extensionProject.ProjectNumber = self.proNum
        self.proName = self.txtProName.text()
        extensionProject.ProjectName = self.proName
        self.proSite = self.cmbProSite.currentText()
        extensionProject.HHSourceType = self.proSite
        self.proLineType = self.cmbPrLineType.currentText()
        extensionProject.LineType = self.proLineType
        self.proLineVol = self.cmbPrLineVolt.currentText()
        extensionProject.LineVoltage = int(self.proLineVol)
        if self.radSet.isChecked():
            self.proPopSource = 'settlement'
        elif self.radStr.isChecked():
            self.proPopSource = 'structure'
        elif self.radVil.isChecked():
            self.proPopSource = 'village'

        extensionProject.HHSourceType =  self.proPopSource

        self.proConSize = self.cmbScConSize.currentText()
        self.proAvgLineLength = self.txtAvgTrLen.text()

        sql = """ insert into exprojects.fout_expansion_projects (substation, feeder, project_number, project_name, household_source, line_type, line_voltage, household_type)
        values( '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s')""" %(basicOps.substation, basicOps.feeder, self.proNum, self.proName, self.proPopSource, self.proLineType, self.proLineVol, self.proSite)
        cur = self.getcursor()
        cur.execute(sql)

        self.createProjectTables(basicOps.substation, basicOps.feeder, self.proNum)

        self.addLayer(self.bufftablename, self.bufflayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.structuretablename, self.structurelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.linetablename, self.linelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.poletablename, self.polelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.refresh_layers()

        self.getTableforModel()

        QMessageBox.information(self.iface.mainWindow(),"Financial Analysis",'Project Tables Created')

    def createProjectTables(self, sub, fed, pro):

        cur = self.getcursor()
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)

        self.bufftablename = subcode + '_' + fedcode + '_buffer_project_' + pro
        self.bufflayername = self.dbase + ": " + sub + "-" + fed + "-buffer-project-" + pro
        extensionProject.BufferTableName = self.bufftablename

        self.linetablename = subcode + '_' + fedcode + '_line_project_' + pro
        self.linelayername = self.dbase + ": " + sub + "-" + fed + "-line-project-" + pro
        extensionProject.LineTableName = self.linetablename

        self.poletablename = subcode + '_' + fedcode + '_pole_project_' + pro
        self.polelayername = self.dbase + ": " + sub + "-" + fed + "-pole-project-" + pro
        extensionProject.PoleTableName = self.poletablename

        if self.proPopSource == 'structure':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-structure-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename
        elif self.proPopSource == 'village':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-village-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename
        elif self.proPopSource == 'settlement':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-settlement-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename

        seqbuffsql = "create sequence exprojects."+self.bufftablename+"_seq;"
        buffsql = """CREATE TABLE exprojects."""+self.bufftablename+"""
        (
          objecid integer NOT NULL DEFAULT nextval('exprojects."""+self.bufftablename+"""_seq'::regclass),
          project_no character varying(30),
          buff_dist integer,
          geom geometry(Polygon,3857),
          equip_id character varying(30)
        )
        """

        cur.execute(seqbuffsql)
        cur.execute(buffsql)

        seqlinesql = "create sequence exprojects."+self.linetablename+"_seq;"
        linesql = """CREATE TABLE exprojects."""+self.linetablename+"""
        (
          objectid integer NOT NULL DEFAULT nextval('exprojects."""+self.linetablename+"""_seq'::regclass),
          substation character varying(30),
          feeder character varying(30),
          line_align character varying(20),
          line_voltage integer,
          line_type character varying(30),
          section_id character varying(30),
          phase character varying(5),
          trans_code character varying(10),
          sec_con character varying(20),
          trans_ref character varying(75),
          con_size_1 character varying(30),
          con_size_2 character varying(30),
          con_size_3 character varying(30),
          con_size_n character varying(30),
          line_status character varying(100),
          data_source character varying(30),
          remarks character varying(50),
          geom geometry(LineString,3857)
        )
        """
        cur.execute(seqlinesql)
        cur.execute(linesql)

        seqpolesql = "create sequence exprojects."+self.poletablename+"_seq;"
        polesql = """CREATE TABLE exprojects."""+self.poletablename+"""
        (
          objectid integer NOT NULL DEFAULT nextval('exprojects."""+self.poletablename+"""_seq'::regclass),
          substation character varying(30),
          feeder character varying(30),
          gps_no character varying(15),
          fed_on_pole integer,
          pole_number character varying(75),
          pole_use character varying(30),
          pole_phase character varying(5),
          pole_height integer,
          pole_class character varying(20),
          pole_structure character varying(30),
          pole_fitting character varying(10),
          pole_guy character varying(5),
          pole_guytype character varying(20),
          pole_guyag character varying(20),
          pole_status character varying(100),
          equip_type character varying(30),
          reference_pole character varying(75),
          equip_id character varying(30),
          equip_unit integer,
          equip_mount character varying(30),
          equip_size character varying(20),
          equip_phase character varying(10),
          equip_status character varying(20),
          equip_use character varying(20),
          trans_ref character varying(75),
          rs_con double precision,
          sc_con double precision,
          lc_con double precision,
          si_con double precision,
          li_con double precision,
          pb_con double precision,
          ag_con double precision,
          st_con double precision,
          location character varying(30),
          data_source character varying(30),
          remarks character varying(50),
          geom geometry(Point,3857)
        )
        """
        cur.execute(seqpolesql)
        cur.execute(polesql)

        #seqstrucsql = 'create sequence exprojects.%s'+'_seq;' %structuretablename
        structuresql = None
        if self.proPopSource == 'structure':
            structuresql = """CREATE TABLE exprojects."""+self.structuretablename+"""
            (
              gid serial NOT NULL,
              household numeric,
              structure numeric,
              geom geometry(Point,3857)
            )
            """
        else:
            structuresql = """CREATE TABLE exprojects."""+self.structuretablename+"""
            (
              gid serial NOT NULL,
              household numeric,
              structure numeric,
              geom geometry(POLYGON,3857)
            )
            """

        cur.execute(structuresql)

    def deleteProjectTables(self, sub, fed, pro):

        conn = self.getConnection()
        cur = conn.cursor()

        buffsql = 'drop table exprojects.%s' %(self.bufftablename)
        linesql = 'drop table exprojects.%s' %(self.linetablename)
        polesql = 'drop table exprojects.%s' %(self.poletablename)
        strucsql = 'drop table exprojects.%s' %(self.structuretablename)
        buffseqsql = 'drop sequence exprojects.%s_seq' %(self.bufftablename)
        lineseqsql = 'drop sequence exprojects.%s_seq' %(self.linetablename)
        poleseqsql = 'drop sequence exprojects.%s_seq' %(self.poletablename)
        strucseqsql = 'drop sequence exprojects.%s_seq' %(self.structuretablename)

        cur.execute(buffsql)
        cur.execute(linesql)
        cur.execute(polesql)
        cur.execute(strucsql)
        cur.execute(buffseqsql)
        cur.execute(lineseqsql)
        cur.execute(strucseqsql)
        conn.commit()

    def deleteSelectedTableRow(self):
        index = self.tblView.selectionModel().currentIndex().row()
        subIndex = self.tblView.selectedIndexes()[0]
        fedIndex = self.tblView.selectedIndexes()[1]
        proIndex = self.tblView.selectedIndexes()[2]
        sub = self.tableView.model().data(subIndex)
        fed =self.tableView.model().data(fedIndex)
        pro = self.tableView.model().data(proIndex)
        sql = "delete from exprojects.fout_expansion_projects where substation = '%s' and feeder = '%s' and project_number = '%s'" %(sub, fed, pro)
        cur = self.getcursor()

        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)

        self.bufftablename = subcode + '_' + fedcode + '_buffer_project_' + pro
        self.linetablename = subcode + '_' + fedcode + '_line_project_' + pro
        self.poletablename = subcode + '_' + fedcode + '_pole_project_' + pro
        if self.proPopSource == 'structure':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_project_' + pro
        elif self.proPopSource == 'village':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_project_' + pro
        elif self.proPopSource == 'settlement':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_project_' + pro

        cur.execute(sql)
        self.deleteProjectTables(sub, fed, pro)

        QMessageBox.information(self.iface.mainWindow(),"Financial Analysis",'Project Number %s for Substation %s, Feeder %s is deleted from project table.' %(pro, sub, fed))
        self.getTableforModel()

    def addProLayers(self):
        index = self.tblView.selectionModel().currentIndex().row()
        subIndex = self.tblView.selectedIndexes()[0]
        fedIndex = self.tblView.selectedIndexes()[1]
        proIndex = self.tblView.selectedIndexes()[2]
        pronameIdx = self.tblView.selectedIndexes()[3]
        strIndex = self.tblView.selectedIndexes()[4]
        linetypIdx = self.tblView.selectedIndexes()[5]
        linevolIdx = self.tblView.selectedIndexes()[6]
        hhtypeIdx = self.tblView.selectedIndexes()[7]

        structure = self.tableView.model().data(strIndex)
        self.proPopSource = structure
        extensionProject.HouseholdSource = structure

        sub = self.tableView.model().data(subIndex)
        fed =self.tableView.model().data(fedIndex)
        pro = self.tableView.model().data(proIndex)
        extensionProject.ProjectNumber = pro

        proname = self.tableView.model().data(pronameIdx)
        extensionProject.ProjectName = proname

        linetype = self.tableView.model().data(linetypIdx)
        extensionProject.LineType = linetype

        linevol = self.tableView.model().data(linevolIdx)
        splittxt = linevol.split('.')
        extensionProject.LineVoltage = int(splittxt[0])

        hhtype = self.tableView.model().data(hhtypeIdx)
        extensionProject.HHSourceType = hhtype

        cur = self.getcursor()
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, sub, fed)
        subcode = bsops.getSubCode(cur, sub)

        self.poletablename = subcode + "_" + fedcode + "_pole_project_"+pro
        self.polelayername = self.dbase + ": " + sub + "-" + fed + "-pole-project-" + pro
        extensionProject.PoleTableName = self.poletablename

        self.linetablename = subcode + "_" + fedcode + "_line_project_"+pro
        self.linelayername = self.dbase + ": " + sub + "-" + fed + "-line-project-" + pro
        extensionProject.LineTableName = self.linetablename

        self.bufftablename = subcode + "_" + fedcode + "_buffer_project_" + pro
        self.bufflayername = self.dbase + ": " + sub + "-" + fed + "-buffer-project-" + pro
        extensionProject.BufferTableName = self.bufftablename

        if self.proPopSource == 'structure':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-structure-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename
        elif self.proPopSource == 'village':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-village-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename
        elif self.proPopSource == 'settlement':
            self.structuretablename = subcode + '_' + fedcode + '_' + self.proPopSource + '_project_' + pro
            self.structurelayername = self.dbase + ": " + sub + "-" + fed + "-settlement-project-" + pro
            extensionProject.HHSourceTableName = self.structuretablename

        self.addLayer(self.bufftablename, self.bufflayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.structuretablename, self.structurelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.linetablename, self.linelayername, self.hst, self.dbase, self.usr, self.paswrd)
        self.addLayer(self.poletablename, self.polelayername, self.hst, self.dbase, self.usr, self.paswrd)

        self.refresh_layers()


    def removelayer(self, layername):
        layers = qgis.utils.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == layername:
                QgsMapLayerRegistry.instance().removeMapLayer( layer.id() )

    def addLayer(self, tablename, layername, hst, dbase, usr, paswrd):
        layers = qgis.utils.iface.mapCanvas().layers()
        foundlayer = False
        for layer in layers:
            if layer.name() == layername:
                foundlayer = True
        if not foundlayer:
            uri = QgsDataSourceURI()
            uri.setConnection(hst, "5432", dbase, usr, paswrd)
            uri.setDataSource("exprojects",tablename,"geom")
            polelayer = QgsVectorLayer(uri.uri(), layername, "postgres")
            QgsMapLayerRegistry.instance().addMapLayer(polelayer)
        else:
            QMessageBox.information(self.iface.mainWindow(),"Add Project Layers","{0} layer already exists!".format(layername))



    def refresh_layers(self):
        for layer in qgis.utils.iface.mapCanvas().layers():
            layer.triggerRepaint()

    def openInputTable(self):
        proname = self.txtPro.text()

        self.close()
        gpsForm = frmInputTable_dialog(self.iface)
        gpsForm.txtPro.setText(proname)
        gpsForm.txtPBS.setText(basicOps.dbasename)
        gpsForm.txtSub.setText(basicOps.substation)
        gpsForm.txtFed.setText(basicOps.feeder)
        gpsForm.exec_()

