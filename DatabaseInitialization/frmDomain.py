# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmDomain.ui'
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

class Ui_frmDomain(object):
    def setupUi(self, frmDomain):
        frmDomain.setObjectName(_fromUtf8("frmDomain"))
        frmDomain.resize(440, 545)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmDomain.sizePolicy().hasHeightForWidth())
        frmDomain.setSizePolicy(sizePolicy)
        frmDomain.setMaximumSize(QtCore.QSize(440, 545))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/domain.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmDomain.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(frmDomain)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 420, 191))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.dgvDomain = QtGui.QTableView(self.groupBox)
        self.dgvDomain.setGeometry(QtCore.QRect(4, 20, 412, 167))
        self.dgvDomain.setFrameShape(QtGui.QFrame.StyledPanel)
        self.dgvDomain.setFrameShadow(QtGui.QFrame.Plain)
        self.dgvDomain.setObjectName(_fromUtf8("dgvDomain"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 206, 420, 231))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.dgvCode = QtGui.QTableView(self.groupBox_2)
        self.dgvCode.setGeometry(QtCore.QRect(4, 20, 412, 206))
        self.dgvCode.setFrameShape(QtGui.QFrame.StyledPanel)
        self.dgvCode.setFrameShadow(QtGui.QFrame.Plain)
        self.dgvCode.setObjectName(_fromUtf8("dgvCode"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 446, 420, 86))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setCheckable(False)
        self.groupBox_3.setChecked(False)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.frame = QtGui.QFrame(self.groupBox_3)
        self.frame.setGeometry(QtCore.QRect(11, 12, 62, 62))
        self.frame.setStyleSheet(_fromUtf8("image: url(:/plugins/ElectricSystems/Resources/FormIcons/basicnreca.png);"))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.cmdDomEdit = QtGui.QPushButton(self.groupBox_3)
        self.cmdDomEdit.setGeometry(QtCore.QRect(185, 23, 50, 40))
        self.cmdDomEdit.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/domainedit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdDomEdit.setIcon(icon1)
        self.cmdDomEdit.setIconSize(QtCore.QSize(32, 32))
        self.cmdDomEdit.setObjectName(_fromUtf8("cmdDomEdit"))
        self.cmdDomSave = QtGui.QPushButton(self.groupBox_3)
        self.cmdDomSave.setGeometry(QtCore.QRect(240, 23, 50, 40))
        self.cmdDomSave.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/domainsave.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdDomSave.setIcon(icon2)
        self.cmdDomSave.setIconSize(QtCore.QSize(32, 32))
        self.cmdDomSave.setObjectName(_fromUtf8("cmdDomSave"))
        self.cmdHelp = QtGui.QPushButton(self.groupBox_3)
        self.cmdHelp.setGeometry(QtCore.QRect(295, 23, 50, 40))
        self.cmdHelp.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basichelp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdHelp.setIcon(icon3)
        self.cmdHelp.setIconSize(QtCore.QSize(32, 32))
        self.cmdHelp.setObjectName(_fromUtf8("cmdHelp"))
        self.cmdClose = QtGui.QPushButton(self.groupBox_3)
        self.cmdClose.setGeometry(QtCore.QRect(350, 23, 50, 40))
        self.cmdClose.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basicexit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdClose.setIcon(icon4)
        self.cmdClose.setIconSize(QtCore.QSize(32, 32))
        self.cmdClose.setObjectName(_fromUtf8("cmdClose"))
        #frmDomain.setCentralWidget(self.centralwidget)

        self.retranslateUi(frmDomain)
        QtCore.QMetaObject.connectSlotsByName(frmDomain)

    def retranslateUi(self, frmDomain):
        frmDomain.setWindowTitle(_translate("frmDomain", "Attribute Domain", None))
        self.groupBox.setTitle(_translate("frmDomain", "Domain", None))
        self.groupBox_2.setTitle(_translate("frmDomain", "Coded Values", None))
        self.cmdDomEdit.setToolTip(_translate("frmDomain", "Edit Domain Values", None))
        self.cmdDomSave.setToolTip(_translate("frmDomain", "Save Domain Values", None))
        self.cmdHelp.setToolTip(_translate("frmDomain", "Help", None))
        self.cmdClose.setToolTip(_translate("frmDomain", "Close", None))

import resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmDomain = QtGui.QMainWindow()
    ui = Ui_frmDomain()
    ui.setupUi(frmDomain)
    frmDomain.show()
    sys.exit(app.exec_())

