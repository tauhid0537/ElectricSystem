from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/SystemInformation")
from systeminformation import *
#import testLineTool
import trans_CreateBufferTool
import testCreateLine

class ElectricSystems:

    def __init__(self, iface):
        self.iface = iface
        self.mapCanvas = iface.mapCanvas()

    def form_add_submenu(self, submenu):
        if self.ElectricSystems != None:
            self.ElectricSystems.addMenu(submenu)
        else:
            self.iface.addPluginToMenu("&ElectricSystems", submenu.menuAction())

    def initGui(self):
	# menu declear
        self.ElectricSystems = QMenu(QCoreApplication.translate("ElectricSystems", "Electric Systems"))
        self.iface.mainWindow().menuBar().insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.ElectricSystems)

        icon = QIcon(os.path.dirname(__file__) + "/Resources/FormIcons/basicsysteminfo.png")
        self.frmSystemInfo_action = QAction(icon, u"System Information", self.iface.mainWindow())
        QObject.connect(self.frmSystemInfo_action, SIGNAL("triggered()"), self.open_frmSystemInfo_dialog)

        self.action = QAction("Create Line" , self.iface.mainWindow())
        self.action.setIcon(QIcon(os.path.dirname(__file__) + "/Resources/FormIcons/formcreate.png"))
        self.action.setWhatsThis("Create Line")
        self.action.setStatusTip("Create Line")

        self.action.triggered.connect(self.run)

        self.tool = testCreateLine.lineCreateTool(self.iface)

        self.ElectricSystems.addAction(self.frmSystemInfo_action)
        self.ElectricSystems.addAction(self.action)

		#Toolbar declaration
        self.toolbar = self.iface.addToolBar(u'Electric Systems')

        self.openfrmSystemInfoAction = QAction(
            QIcon(os.path.dirname(__file__) + "/Resources/FormIcons/basicsysteminfo.png"),
            u"System Information",
            self.iface.mainWindow())

        self.openfrmSystemInfoAction.triggered.connect(self.open_frmSystemInfo_dialog)
        self.toolbar.addAction(self.openfrmSystemInfoAction)

        self.lineTool = QAction(
            QIcon(os.path.dirname(__file__) + "/Resources/FormIcons/formcreate.png"),
            u"Create Line",
            self.iface.mainWindow()
            )
        self.lineTool.triggered.connect(self.run)
        self.toolbar.addAction(self.lineTool)


    def open_frmSystemInfo_dialog(self):
        sysinfo = frmSystemInfo_dialog(self.iface)

#        sysinfo.getTextFile()
        sysinfo.exec_()

    def run(self):
        self.iface.mapCanvas().setMapTool(self.tool)

    def unload(self):
        if self.ElectricSystems != None:
            self.iface.mainWindow().menuBar().removeAction(self.ElectricSystems.menuAction())
            self.ElectricSystems.deleteLater()
            self.iface.mainWindow().removeToolBar(self.toolbar)
        else:
            self.iface.removePluginMenu("&ElectricSystems", self.ElectricSystems.menuAction())
            self.ElectricSystems.deleteLater()

