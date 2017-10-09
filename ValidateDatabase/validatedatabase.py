from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import csv
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ValidateDatabase")
from frmValidate import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
import resources

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class frmValidate_dialog(QDialog, Ui_frmValidate):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        model = QStandardItemModel()
        self.treeView.setModel(model)
        self.treeView.setUniformRowHeights(True)

        #os.path.dirname(os.path.abspath(__file__))
        #icon = QIcon(os.path.dirname(os.path.abspath(__file__)) + "/Icons/validate.png")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/validate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        mainNode = QStandardItem('Validate')
        #iconMain = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/validate.png')
        mainNode.setIcon(icon)
        
        iconNode1 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/valtopology.png')
        subNode1 = QStandardItem('Topology')
        subNode1.setIcon(iconNode1)
        
        iSub1Node1 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/valsubloc.png')
        sub1Node1 = QStandardItem('Substation Location')
        sub1Node1.setIcon(iSub1Node1)
        
        iSub1Node2 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/valpoleloc.png')
        sub1Node2 = QStandardItem('Pole Location')
        sub1Node2.setIcon(iSub1Node2)
        
        iSub1Node3 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/vallineloc.png')
        sub1Node3 = QStandardItem('Line Location')
        sub1Node3.setIcon(iSub1Node3)
        
        iSub1Node4 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/vallinepoletopo.png')
        sub1Node4 = QStandardItem('Line-Pole Topology')
        sub1Node4.setIcon(iSub1Node4)
        
        iSub1Node5 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/vallinelinetopo.png')
        sub1Node5 = QStandardItem('Line-Line Topology')
        sub1Node5.setIcon(iSub1Node5)

        subNode1.appendRow([sub1Node1])
        subNode1.appendRow([sub1Node2])
        subNode1.appendRow([sub1Node3])
        subNode1.appendRow([sub1Node4])
        subNode1.appendRow([sub1Node5])
        
        iconNode2 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/valattribute.png')
        subNode2 = QStandardItem('Attribute')
        subNode2.setIcon(iconNode2)
        
        iSub2Node1 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/valsubloc.png')
        sub2Node1 = QStandardItem('Substation')
        sub2Node1.setIcon(iSub2Node1)
        
        iSub2Node2 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/valpoleloc.png')
        sub2Node2 = QStandardItem('Pole')
        sub2Node2.setIcon(iSub2Node2)
        
        iSub2Node3 = QtGui.QIcon('C:/Users/aselim.CORPORATE/.qgis2/python/plugins/ElectricSystems/Resources/FormIcons/vallineloc.png')
        sub2Node3 = QStandardItem('Line')
        sub2Node3.setIcon(iSub2Node3)
        
        subNode2.appendRow([sub2Node1])
        subNode2.appendRow([sub2Node2])
        subNode2.appendRow([sub2Node3])

        mainNode.appendRow([subNode1])
        mainNode.appendRow([subNode2])
        model.appendRow(mainNode)
        
        #mainIndex = model.indexFromItem(mainNode)
        #self.treeView.expand(mainIndex)
        #sub1Index = model.indexFromItem(subNode1)
        #self.treeView.expand(sub1Index)
        #sub2Index = model.indexFromItem(subNode2)
        #self.treeView.expand(sub2Index)

        self.cmdJumper.clicked.connect(self.getText)
        self.cmdClose.clicked.connect(self.onClose)
        self.treeView.clicked.connect(self.getProcessName)

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def getProcessName(self):
        index = self.treeView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index).text()

        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText(item)
        ret = msgBox.exec_()



    def onClose(self):
        self.close()
