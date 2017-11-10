from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import os
import sys
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/SystemInformation")
from systeminformation import *


import addTransformer
import projectTranformerTool
import projectLineTool

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

        self.action = QAction("Project Line Tool" , self.iface.mainWindow())
        self.action.setIcon(QIcon(os.path.dirname(__file__) + "/Resources/FormIcons/AddLine.png"))
        self.action.setWhatsThis("Project Line Tool")
        self.action.setStatusTip("Project Line Tool")

        self.testAction = QAction("Transformer Tool" , self.iface.mainWindow())
        self.testAction.setIcon(QIcon(os.path.dirname(__file__) + "/Resources/FormIcons/AddTransformer.png"))
        self.testAction.setWhatsThis("Project Transformer Tool")
        self.testAction.setStatusTip("Project Transformer Tool")

        self.action.triggered.connect(self.run)
        self.testAction.triggered.connect(self.runTransTool)

        self.tool = projectLineTool.prjLineTool(self.iface)
        self.transTool = projectTranformerTool.transformerTool(self.iface)

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
            QIcon(os.path.dirname(__file__) + "/Resources/FormIcons/AddLine.png"),
            u"Project Line Tool",
            self.iface.mainWindow()
            )
        self.lineTool.triggered.connect(self.run)
        self.toolbar.addAction(self.lineTool)

        self.trnTool = QAction(
            QIcon(os.path.dirname(__file__) + "/Resources/FormIcons/AddTransformer.png"),
            u"Project Transformer Tool",
            self.iface.mainWindow()
            )
        self.trnTool.triggered.connect(self.runTransTool)
        self.toolbar.addAction(self.trnTool)


    def open_frmSystemInfo_dialog(self):
        sysinfo = frmSystemInfo_dialog(self.iface)

#        sysinfo.getTextFile()
        sysinfo.exec_()

    def run(self):
        self.iface.mapCanvas().setMapTool(self.tool)

    def runTransTool(self):
        self.iface.mapCanvas().setMapTool(self.transTool)

    def unload(self):
        if self.ElectricSystems != None:
            self.iface.mainWindow().menuBar().removeAction(self.ElectricSystems.menuAction())
            self.ElectricSystems.deleteLater()
            self.iface.mainWindow().removeToolBar(self.toolbar)
        else:
            self.iface.removePluginMenu("&ElectricSystems", self.ElectricSystems.menuAction())
            self.ElectricSystems.deleteLater()

