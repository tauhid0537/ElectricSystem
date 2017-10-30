# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmProcessFieldData.ui'
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

class Ui_frmProcessData(object):
    def setupUi(self, frmProcessData):
        frmProcessData.setObjectName(_fromUtf8("frmProcessData"))
        frmProcessData.resize(464, 265)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/formgps.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmProcessData.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(frmProcessData)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 442, 87))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(12, 23, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtPro = QtGui.QLineEdit(self.groupBox)
        self.txtPro.setGeometry(QtCore.QRect(95, 20, 121, 22))
        self.txtPro.setObjectName(_fromUtf8("txtPro"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(228, 23, 51, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(12, 53, 71, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(228, 53, 51, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.txtSub = QtGui.QLineEdit(self.groupBox)
        self.txtSub.setGeometry(QtCore.QRect(95, 50, 121, 22))
        self.txtSub.setObjectName(_fromUtf8("txtSub"))
        self.txtPBS = QtGui.QLineEdit(self.groupBox)
        self.txtPBS.setGeometry(QtCore.QRect(308, 20, 121, 22))
        self.txtPBS.setObjectName(_fromUtf8("txtPBS"))
        self.txtFed = QtGui.QLineEdit(self.groupBox)
        self.txtFed.setGeometry(QtCore.QRect(308, 50, 121, 22))
        self.txtFed.setObjectName(_fromUtf8("txtFed"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 100, 441, 61))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.cmbGroup = QtGui.QComboBox(self.groupBox_2)
        self.cmbGroup.setGeometry(QtCore.QRect(95, 22, 121, 22))
        self.cmbGroup.setObjectName(_fromUtf8("cmbGroup"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(10, 25, 91, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(228, 25, 81, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.dtpSurvey = QtGui.QDateEdit(self.groupBox_2)
        self.dtpSurvey.setGeometry(QtCore.QRect(308, 22, 121, 22))
        self.dtpSurvey.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.dtpSurvey.setObjectName(_fromUtf8("dtpSurvey"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 168, 441, 84))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.frame = QtGui.QFrame(self.groupBox_3)
        self.frame.setGeometry(QtCore.QRect(10, 10, 62, 62))
        self.frame.setStyleSheet(_fromUtf8("image: url(:/plugins/ElectricSystems/Resources/FormIcons/basicnreca.png);"))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.cmdHelp = QtGui.QPushButton(self.groupBox_3)
        self.cmdHelp.setGeometry(QtCore.QRect(260, 20, 50, 40))
        self.cmdHelp.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basichelp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdHelp.setIcon(icon1)
        self.cmdHelp.setIconSize(QtCore.QSize(32, 32))
        self.cmdHelp.setObjectName(_fromUtf8("cmdHelp"))
        self.cmdGetData = QtGui.QPushButton(self.groupBox_3)
        self.cmdGetData.setGeometry(QtCore.QRect(150, 20, 50, 40))
        self.cmdGetData.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/featuregps.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdGetData.setIcon(icon2)
        self.cmdGetData.setIconSize(QtCore.QSize(32, 32))
        self.cmdGetData.setObjectName(_fromUtf8("cmdGetData"))
        self.cmdClose = QtGui.QPushButton(self.groupBox_3)
        self.cmdClose.setGeometry(QtCore.QRect(370, 20, 50, 40))
        self.cmdClose.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basicexit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdClose.setIcon(icon3)
        self.cmdClose.setIconSize(QtCore.QSize(32, 32))
        self.cmdClose.setObjectName(_fromUtf8("cmdClose"))
        #frmProcessData.setCentralWidget(self.centralwidget)

        self.retranslateUi(frmProcessData)
        QtCore.QMetaObject.connectSlotsByName(frmProcessData)

    def retranslateUi(self, frmProcessData):
        frmProcessData.setWindowTitle(_translate("frmProcessData", "Process Field Data", None))
        self.groupBox.setTitle(_translate("frmProcessData", "Dataset", None))
        self.label.setText(_translate("frmProcessData", "Project Name", None))
        self.txtPro.setToolTip(_translate("frmProcessData", "Project Name", None))
        self.label_2.setText(_translate("frmProcessData", "Database", None))
        self.label_3.setText(_translate("frmProcessData", "Substation", None))
        self.label_4.setText(_translate("frmProcessData", "Feeder", None))
        self.txtSub.setToolTip(_translate("frmProcessData", "Project Name", None))
        self.txtPBS.setToolTip(_translate("frmProcessData", "Project Name", None))
        self.txtFed.setToolTip(_translate("frmProcessData", "Project Name", None))
        self.groupBox_2.setTitle(_translate("frmProcessData", "Field Survey Infomation", None))
        self.label_5.setText(_translate("frmProcessData", "Select Group", None))
        self.label_6.setText(_translate("frmProcessData", "Date of Survey", None))
        self.cmdHelp.setToolTip(_translate("frmProcessData", "Help", None))
        self.cmdGetData.setToolTip(_translate("frmProcessData", "Get Data", None))
        self.cmdClose.setToolTip(_translate("frmProcessData", "Close", None))

import resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmProcessData = QtGui.QMainWindow()
    ui = Ui_frmProcessData()
    ui.setupUi(frmProcessData)
    frmProcessData.show()
    sys.exit(app.exec_())

