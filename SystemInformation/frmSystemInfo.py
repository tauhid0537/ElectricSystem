# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmSystemInfo.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_frmSysInfo(object):
    def setupUi(self, frmSysInfo):
        frmSysInfo.setObjectName(_fromUtf8("frmSysInfo"))
        frmSysInfo.resize(453, 410)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmSysInfo.sizePolicy().hasHeightForWidth())
        frmSysInfo.setSizePolicy(sizePolicy)
        frmSysInfo.setMaximumSize(QtCore.QSize(453, 410))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/formprocess.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmSysInfo.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(frmSysInfo)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 130, 431, 171))
        self.tabWidget.setIconSize(QtCore.QSize(24, 24))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.dataSysInfo = QtGui.QTableView(self.tab_2)
        self.dataSysInfo.setGeometry(QtCore.QRect(2, 3, 421, 131))
        self.dataSysInfo.setMaximumSize(QtCore.QSize(421, 150))
        self.dataSysInfo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.dataSysInfo.setFrameShadow(QtGui.QFrame.Plain)
        self.dataSysInfo.setObjectName(_fromUtf8("dataSysInfo"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/formaccept.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_2, icon1, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.txtDatabase = QtGui.QLineEdit(self.tab)
        self.txtDatabase.setGeometry(QtCore.QRect(170, 39, 221, 20))
        self.txtDatabase.setObjectName(_fromUtf8("txtDatabase"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(17, 42, 141, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(17, 71, 151, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.cmbSysPhase = QtGui.QComboBox(self.tab)
        self.cmbSysPhase.setGeometry(QtCore.QRect(170, 69, 221, 22))
        self.cmbSysPhase.setAutoFillBackground(False)
        self.cmbSysPhase.setStyleSheet(_fromUtf8(""))
        self.cmbSysPhase.setObjectName(_fromUtf8("cmbSysPhase"))
        self.cmbSysPhase.addItem(_fromUtf8(""))
        self.cmbSysPhase.addItem(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab, icon2, _fromUtf8(""))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 431, 111))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(17, 48, 131, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(17, 77, 141, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.txtUserName = QtGui.QLineEdit(self.groupBox)
        self.txtUserName.setGeometry(QtCore.QRect(146, 46, 211, 20))
        self.txtUserName.setObjectName(_fromUtf8("txtUserName"))
        self.txtPassword = QtGui.QLineEdit(self.groupBox)
        self.txtPassword.setGeometry(QtCore.QRect(146, 75, 211, 20))
        self.txtPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.txtPassword.setObjectName(_fromUtf8("txtPassword"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(17, 19, 131, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.txtHost = QtGui.QLineEdit(self.groupBox)
        self.txtHost.setGeometry(QtCore.QRect(146, 17, 211, 20))
        self.txtHost.setObjectName(_fromUtf8("txtHost"))
        self.cmdGetDatabase = QtGui.QPushButton(self.groupBox)
        self.cmdGetDatabase.setGeometry(QtCore.QRect(368, 35, 50, 40))
        self.cmdGetDatabase.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/getdatabase.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdGetDatabase.setIcon(icon3)
        self.cmdGetDatabase.setIconSize(QtCore.QSize(32, 32))
        self.cmdGetDatabase.setDefault(False)
        self.cmdGetDatabase.setFlat(False)
        self.cmdGetDatabase.setObjectName(_fromUtf8("cmdGetDatabase"))
        self.groupBox_6 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 308, 431, 91))
        self.groupBox_6.setTitle(_fromUtf8(""))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.frame = QtGui.QFrame(self.groupBox_6)
        self.frame.setGeometry(QtCore.QRect(14, 15, 61, 61))
        self.frame.setStyleSheet(_fromUtf8("image: url(:/plugins/ElectricSystems/Resources/FormIcons/basicnreca.png);"))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.cmdUseDatabase = QtGui.QPushButton(self.groupBox_6)
        self.cmdUseDatabase.setGeometry(QtCore.QRect(150, 26, 50, 40))
        self.cmdUseDatabase.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/usedatabase.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdUseDatabase.setIcon(icon4)
        self.cmdUseDatabase.setIconSize(QtCore.QSize(32, 32))
        self.cmdUseDatabase.setDefault(False)
        self.cmdUseDatabase.setFlat(False)
        self.cmdUseDatabase.setObjectName(_fromUtf8("cmdUseDatabase"))
        self.cmdCreateDatabase = QtGui.QPushButton(self.groupBox_6)
        self.cmdCreateDatabase.setGeometry(QtCore.QRect(220, 26, 50, 40))
        self.cmdCreateDatabase.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/createdatabase.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdCreateDatabase.setIcon(icon5)
        self.cmdCreateDatabase.setIconSize(QtCore.QSize(32, 32))
        self.cmdCreateDatabase.setDefault(False)
        self.cmdCreateDatabase.setFlat(False)
        self.cmdCreateDatabase.setObjectName(_fromUtf8("cmdCreateDatabase"))
        self.cmdHelp = QtGui.QPushButton(self.groupBox_6)
        self.cmdHelp.setGeometry(QtCore.QRect(290, 26, 50, 40))
        self.cmdHelp.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basichelp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdHelp.setIcon(icon6)
        self.cmdHelp.setIconSize(QtCore.QSize(32, 32))
        self.cmdHelp.setDefault(False)
        self.cmdHelp.setFlat(False)
        self.cmdHelp.setObjectName(_fromUtf8("cmdHelp"))
        self.cmdClose = QtGui.QPushButton(self.groupBox_6)
        self.cmdClose.setGeometry(QtCore.QRect(360, 26, 50, 40))
        self.cmdClose.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basicexit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdClose.setIcon(icon7)
        self.cmdClose.setIconSize(QtCore.QSize(32, 32))
        self.cmdClose.setDefault(False)
        self.cmdClose.setFlat(False)
        self.cmdClose.setObjectName(_fromUtf8("cmdClose"))
        #frmSysInfo.setCentralWidget(self.centralwidget)

        self.retranslateUi(frmSysInfo)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmSysInfo)

    def retranslateUi(self, frmSysInfo):
        frmSysInfo.setWindowTitle(_translate("frmSysInfo", "System Information", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("frmSysInfo", "Existing Database", None))
        self.txtDatabase.setToolTip(_translate("frmSysInfo", "Enter Database Name", None))
        self.label_4.setText(_translate("frmSysInfo", "Database Name", None))
        self.label_3.setText(_translate("frmSysInfo", "System Phase Configuration", None))
        self.cmbSysPhase.setToolTip(_translate("frmSysInfo", "Select System Phase Configuration", None))
        self.cmbSysPhase.setItemText(0, _translate("frmSysInfo", "RYB", None))
        self.cmbSysPhase.setItemText(1, _translate("frmSysInfo", "ABC", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("frmSysInfo", "Create Database", None))
        self.label.setText(_translate("frmSysInfo", "User Name", None))
        self.label_2.setText(_translate("frmSysInfo", "Password", None))
        self.txtUserName.setToolTip(_translate("frmSysInfo", "Enter User Name", None))
        self.txtPassword.setToolTip(_translate("frmSysInfo", "Enter Password", None))
        self.label_5.setText(_translate("frmSysInfo", "Host", None))
        self.txtHost.setToolTip(_translate("frmSysInfo", "Enter Host Name", None))
        self.cmdGetDatabase.setToolTip(_translate("frmSysInfo", "Get Database", None))
        self.cmdUseDatabase.setToolTip(_translate("frmSysInfo", "Use Database", None))
        self.cmdCreateDatabase.setToolTip(_translate("frmSysInfo", "Create Database", None))
        self.cmdHelp.setToolTip(_translate("frmSysInfo", "Help", None))
        self.cmdClose.setToolTip(_translate("frmSysInfo", "Close", None))

import resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmSysInfo = QtGui.QMainWindow()
    ui = Ui_frmSysInfo()
    ui.setupUi(frmSysInfo)
    frmSysInfo.show()
    sys.exit(app.exec_())
