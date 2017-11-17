from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import csv
import sys
import os
import qgis

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

        self.cmdEdit.clicked.connect(self.getText)
        self.cmdClose.clicked.connect(self.onClose)
        self.treeView.clicked.connect(self.getProcess)

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def getProcess(self):
        index = self.treeView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index).text()

        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Input Table")
        msgBox.setText(item)
        ret = msgBox.exec_()

    def onClose(self):
        self.close()



