# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmAddLine.ui'
#
# Created: Wed Nov 29 15:41:34 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_frmAddLine(object):
    def setupUi(self, frmAddLine):
        frmAddLine.setObjectName(_fromUtf8("frmAddLine"))
        frmAddLine.resize(352, 428)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/AddLine.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmAddLine.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(frmAddLine)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.txtPro = QtGui.QLineEdit(self.centralwidget)
        self.txtPro.setGeometry(QtCore.QRect(160, 30, 161, 20))
        self.txtPro.setObjectName(_fromUtf8("txtPro"))
        self.txtPBS = QtGui.QLineEdit(self.centralwidget)
        self.txtPBS.setGeometry(QtCore.QRect(160, 60, 161, 20))
        self.txtPBS.setObjectName(_fromUtf8("txtPBS"))
        self.txtSub = QtGui.QLineEdit(self.centralwidget)
        self.txtSub.setGeometry(QtCore.QRect(160, 90, 161, 20))
        self.txtSub.setObjectName(_fromUtf8("txtSub"))
        self.txtFed = QtGui.QLineEdit(self.centralwidget)
        self.txtFed.setGeometry(QtCore.QRect(160, 120, 161, 20))
        self.txtFed.setObjectName(_fromUtf8("txtFed"))
        self.txtProNum = QtGui.QLineEdit(self.centralwidget)
        self.txtProNum.setGeometry(QtCore.QRect(160, 180, 161, 20))
        self.txtProNum.setObjectName(_fromUtf8("txtProNum"))
        self.cmbConPhase = QtGui.QComboBox(self.centralwidget)
        self.cmbConPhase.setGeometry(QtCore.QRect(160, 210, 161, 22))
        self.cmbConPhase.setObjectName(_fromUtf8("cmbConPhase"))
        self.cmbConSize = QtGui.QComboBox(self.centralwidget)
        self.cmbConSize.setGeometry(QtCore.QRect(160, 240, 161, 22))
        self.cmbConSize.setObjectName(_fromUtf8("cmbConSize"))
        self.cmdOK = QtGui.QPushButton(self.centralwidget)
        self.cmdOK.setGeometry(QtCore.QRect(150, 320, 51, 41))
        self.cmdOK.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/formaccept.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdOK.setIcon(icon1)
        self.cmdOK.setIconSize(QtCore.QSize(32, 32))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdHelp = QtGui.QPushButton(self.centralwidget)
        self.cmdHelp.setGeometry(QtCore.QRect(210, 320, 51, 41))
        self.cmdHelp.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basichelp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdHelp.setIcon(icon2)
        self.cmdHelp.setIconSize(QtCore.QSize(32, 32))
        self.cmdHelp.setObjectName(_fromUtf8("cmdHelp"))
        self.cmdClose = QtGui.QPushButton(self.centralwidget)
        self.cmdClose.setGeometry(QtCore.QRect(270, 320, 51, 41))
        self.cmdClose.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basicexit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdClose.setIcon(icon3)
        self.cmdClose.setIconSize(QtCore.QSize(32, 32))
        self.cmdClose.setObjectName(_fromUtf8("cmdClose"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 51, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 90, 61, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 120, 46, 13))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 180, 81, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 210, 101, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 240, 121, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(30, 310, 62, 62))
        self.frame_2.setStyleSheet(_fromUtf8("image: url(:/plugins/ElectricSystems/Resources/FormIcons/basicnreca.png);"))
        self.frame_2.setFrameShape(QtGui.QFrame.Panel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 311, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 160, 311, 121))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        """frmAdLine.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(frmAdLine)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 352, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        frmAdLine.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(frmAdLine)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frmAdLine.setStatusBar(self.statusbar)"""

        self.retranslateUi(frmAddLine)
        QtCore.QMetaObject.connectSlotsByName(frmAddLine)

    def retranslateUi(self, frmAddLine):
        frmAddLine.setWindowTitle(_translate("frmAddLine", "Add Line", None))
        self.label.setText(_translate("frmAddLine", "Project Name", None))
        self.label_2.setText(_translate("frmAddLine", "Database", None))
        self.label_3.setText(_translate("frmAddLine", "Substation", None))
        self.label_4.setText(_translate("frmAddLine", "Feeder", None))
        self.label_5.setText(_translate("frmAddLine", "Project Number", None))
        self.label_6.setText(_translate("frmAddLine", "Phase Configuration", None))
        self.label_7.setText(_translate("frmAddLine", "Primary Conductor Size", None))
        self.groupBox.setTitle(_translate("frmAddLine", "Dataset", None))
        self.groupBox_2.setTitle(_translate("frmAddLine", "Project Parameters", None))

import resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmAddLine = QtGui.QMainWindow()
    ui = Ui_frmAddLine()
    ui.setupUi(frmAddLine)
    frmAddLine.show()
    sys.exit(app.exec_())

