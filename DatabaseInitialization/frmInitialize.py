# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmInitialize.ui'
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

class Ui_frmIntialize(object):
    def setupUi(self, frmIntialize):
        frmIntialize.setObjectName(_fromUtf8("frmIntialize"))
        frmIntialize.resize(525, 250)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmIntialize.sizePolicy().hasHeightForWidth())
        frmIntialize.setSizePolicy(sizePolicy)
        frmIntialize.setMaximumSize(QtCore.QSize(525, 250))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/formcreate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmIntialize.setWindowIcon(icon)
        #frmIntialize.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(frmIntialize)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 501, 129))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(16, 30, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtPro = QtGui.QLineEdit(self.groupBox)
        self.txtPro.setGeometry(QtCore.QRect(110, 28, 140, 20))
        self.txtPro.setObjectName(_fromUtf8("txtPro"))
        self.txtPBS = QtGui.QLineEdit(self.groupBox)
        self.txtPBS.setGeometry(QtCore.QRect(344, 28, 140, 20))
        self.txtPBS.setObjectName(_fromUtf8("txtPBS"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(264, 30, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(16, 60, 81, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.txtFed = QtGui.QLineEdit(self.groupBox)
        self.txtFed.setGeometry(QtCore.QRect(344, 58, 140, 20))
        self.txtFed.setObjectName(_fromUtf8("txtFed"))
        self.txtSub = QtGui.QLineEdit(self.groupBox)
        self.txtSub.setGeometry(QtCore.QRect(110, 58, 140, 20))
        self.txtSub.setObjectName(_fromUtf8("txtSub"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(264, 59, 61, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(16, 90, 81, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(264, 90, 71, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.txtSubCode = QtGui.QLineEdit(self.groupBox)
        self.txtSubCode.setGeometry(QtCore.QRect(110, 88, 140, 20))
        self.txtSubCode.setObjectName(_fromUtf8("txtSubCode"))
        self.txtFedCode = QtGui.QLineEdit(self.groupBox)
        self.txtFedCode.setGeometry(QtCore.QRect(344, 88, 140, 20))
        self.txtFedCode.setObjectName(_fromUtf8("txtFedCode"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 147, 501, 91))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.frame = QtGui.QFrame(self.groupBox_3)
        self.frame.setGeometry(QtCore.QRect(13, 14, 62, 62))
        self.frame.setStyleSheet(_fromUtf8("image: url(:/plugins/ElectricSystems/Resources/FormIcons/basicnreca.png);"))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.cmdClose = QtGui.QPushButton(self.groupBox_3)
        self.cmdClose.setGeometry(QtCore.QRect(435, 24, 50, 40))
        self.cmdClose.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basicexit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdClose.setIcon(icon1)
        self.cmdClose.setIconSize(QtCore.QSize(32, 32))
        self.cmdClose.setObjectName(_fromUtf8("cmdClose"))
        self.cmdShapefile = QtGui.QPushButton(self.groupBox_3)
        self.cmdShapefile.setGeometry(QtCore.QRect(315, 24, 50, 40))
        self.cmdShapefile.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/databaseshapefile.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdShapefile.setIcon(icon2)
        self.cmdShapefile.setIconSize(QtCore.QSize(32, 32))
        self.cmdShapefile.setObjectName(_fromUtf8("cmdShapefile"))
        self.cmdHelp = QtGui.QPushButton(self.groupBox_3)
        self.cmdHelp.setGeometry(QtCore.QRect(375, 24, 50, 40))
        self.cmdHelp.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basichelp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdHelp.setIcon(icon3)
        self.cmdHelp.setIconSize(QtCore.QSize(32, 32))
        self.cmdHelp.setObjectName(_fromUtf8("cmdHelp"))
        self.cmdDomain = QtGui.QPushButton(self.groupBox_3)
        self.cmdDomain.setGeometry(QtCore.QRect(194, 24, 50, 40))
        self.cmdDomain.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/domain.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdDomain.setIcon(icon4)
        self.cmdDomain.setIconSize(QtCore.QSize(32, 32))
        self.cmdDomain.setObjectName(_fromUtf8("cmdDomain"))
        self.cmdConductor = QtGui.QPushButton(self.groupBox_3)
        self.cmdConductor.setGeometry(QtCore.QRect(255, 24, 50, 40))
        self.cmdConductor.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/voltageconductor.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdConductor.setIcon(icon5)
        self.cmdConductor.setIconSize(QtCore.QSize(32, 32))
        self.cmdConductor.setObjectName(_fromUtf8("cmdConductor"))
        self.cmdFolder = QtGui.QPushButton(self.groupBox_3)
        self.cmdFolder.setGeometry(QtCore.QRect(133, 24, 50, 40))
        self.cmdFolder.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/folderadd.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdFolder.setIcon(icon6)
        self.cmdFolder.setIconSize(QtCore.QSize(32, 32))
        self.cmdFolder.setObjectName(_fromUtf8("cmdFolder"))
        #frmIntialize.setCentralWidget(self.centralwidget)

        self.retranslateUi(frmIntialize)
        QtCore.QMetaObject.connectSlotsByName(frmIntialize)

    def retranslateUi(self, frmIntialize):
        frmIntialize.setWindowTitle(_translate("frmIntialize", "Database Initialization", None))
        self.groupBox.setTitle(_translate("frmIntialize", "Dataset", None))
        self.label.setText(_translate("frmIntialize", "Project Name", None))
        self.txtPro.setToolTip(_translate("frmIntialize", "Project Name", None))
        self.txtPBS.setToolTip(_translate("frmIntialize", "Enter Database Name", None))
        self.label_2.setText(_translate("frmIntialize", "Database", None))
        self.label_4.setText(_translate("frmIntialize", "Substation", None))
        self.txtFed.setToolTip(_translate("frmIntialize", "Enter Feeder Name", None))
        self.txtSub.setToolTip(_translate("frmIntialize", "Enter Substation Name", None))
        self.label_3.setText(_translate("frmIntialize", "Feeder", None))
        self.label_6.setText(_translate("frmIntialize", "Substation Code", None))
        self.label_5.setText(_translate("frmIntialize", "Feeder Code", None))
        self.txtSubCode.setToolTip(_translate("frmIntialize", "Enter Substation Code", None))
        self.txtFedCode.setToolTip(_translate("frmIntialize", "Enter Feeder Code", None))
        self.cmdClose.setToolTip(_translate("frmIntialize", "Close", None))
        self.cmdShapefile.setToolTip(_translate("frmIntialize", "Create Feeder Layers", None))
        self.cmdHelp.setToolTip(_translate("frmIntialize", "Help", None))
        self.cmdDomain.setToolTip(_translate("frmIntialize", "Edit Domains", None))
        self.cmdConductor.setToolTip(_translate("frmIntialize", "Conductor Table", None))
        self.cmdFolder.setToolTip(_translate("frmIntialize", "Create Folders", None))

import resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmIntialize = QtGui.QMainWindow()
    ui = Ui_frmIntialize()
    ui.setupUi(frmIntialize)
    frmIntialize.show()
    sys.exit(app.exec_())

