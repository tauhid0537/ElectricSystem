# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmAddTransformer.ui'
#
# Created: Mon Oct 23 15:37:02 2017
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

class Ui_frmAddTransformer(object):
    def setupUi(self, frmAddTransformer):
        frmAddTransformer.setObjectName(_fromUtf8("frmAddTransformer"))
        frmAddTransformer.resize(378, 467)
        self.centralwidget = QtGui.QWidget(frmAddTransformer)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.txtPro = QtGui.QLineEdit(self.centralwidget)
        self.txtPro.setGeometry(QtCore.QRect(130, 30, 201, 20))
        self.txtPro.setObjectName(_fromUtf8("txtPro"))
        self.txtDatabase = QtGui.QLineEdit(self.centralwidget)
        self.txtDatabase.setGeometry(QtCore.QRect(130, 60, 201, 20))
        self.txtDatabase.setObjectName(_fromUtf8("txtDatabase"))
        self.txtSub = QtGui.QLineEdit(self.centralwidget)
        self.txtSub.setGeometry(QtCore.QRect(130, 90, 201, 20))
        self.txtSub.setObjectName(_fromUtf8("txtSub"))
        self.txtFed = QtGui.QLineEdit(self.centralwidget)
        self.txtFed.setGeometry(QtCore.QRect(130, 120, 201, 20))
        self.txtFed.setObjectName(_fromUtf8("txtFed"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 61, 16))
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
        self.txtProNum = QtGui.QLineEdit(self.centralwidget)
        self.txtProNum.setGeometry(QtCore.QRect(220, 180, 113, 20))
        self.txtProNum.setObjectName(_fromUtf8("txtProNum"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 180, 81, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.txtMinTrn = QtGui.QLineEdit(self.centralwidget)
        self.txtMinTrn.setGeometry(QtCore.QRect(220, 210, 113, 20))
        self.txtMinTrn.setObjectName(_fromUtf8("txtMinTrn"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 210, 161, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.txtMaxTrn = QtGui.QLineEdit(self.centralwidget)
        self.txtMaxTrn.setGeometry(QtCore.QRect(220, 240, 113, 20))
        self.txtMaxTrn.setObjectName(_fromUtf8("txtMaxTrn"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 240, 161, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.txtBuffDist = QtGui.QLineEdit(self.centralwidget)
        self.txtBuffDist.setGeometry(QtCore.QRect(220, 270, 113, 20))
        self.txtBuffDist.setObjectName(_fromUtf8("txtBuffDist"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(30, 270, 141, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.cmdOK = QtGui.QPushButton(self.centralwidget)
        self.cmdOK.setGeometry(QtCore.QRect(150, 350, 50, 40))
        self.cmdOK.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/formaccept.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdOK.setIcon(icon)
        self.cmdOK.setIconSize(QtCore.QSize(32, 32))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdHelp = QtGui.QPushButton(self.centralwidget)
        self.cmdHelp.setGeometry(QtCore.QRect(220, 350, 50, 40))
        self.cmdHelp.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basichelp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdHelp.setIcon(icon1)
        self.cmdHelp.setIconSize(QtCore.QSize(32, 32))
        self.cmdHelp.setObjectName(_fromUtf8("cmdHelp"))
        self.cmdClose = QtGui.QPushButton(self.centralwidget)
        self.cmdClose.setGeometry(QtCore.QRect(290, 350, 50, 40))
        self.cmdClose.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basicexit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdClose.setIcon(icon2)
        self.cmdClose.setIconSize(QtCore.QSize(32, 32))
        self.cmdClose.setObjectName(_fromUtf8("cmdClose"))
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(40, 340, 62, 62))
        self.frame_2.setStyleSheet(_fromUtf8("image: url(:/plugins/ElectricSystems/Resources/FormIcons/basicnreca.png);"))
        self.frame_2.setFrameShape(QtGui.QFrame.Panel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 341, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 160, 341, 141))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 320, 341, 91))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        """#frmAddTransformer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(frmAddTransformer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 378, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        #frmAddTransformer.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(frmAddTransformer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frmAddTransformer.setStatusBar(self.statusbar)"""

        self.retranslateUi(frmAddTransformer)
        QtCore.QMetaObject.connectSlotsByName(frmAddTransformer)

    def retranslateUi(self, frmAddTransformer):
        frmAddTransformer.setWindowTitle(_translate("frmAddTransformer", "Add Transformer", None))
        self.label.setText(_translate("frmAddTransformer", "User Name:", None))
        self.label_2.setText(_translate("frmAddTransformer", "Database:", None))
        self.label_3.setText(_translate("frmAddTransformer", "Substation:", None))
        self.label_4.setText(_translate("frmAddTransformer", "Feeder:", None))
        self.label_5.setText(_translate("frmAddTransformer", "Project Number:", None))
        self.label_6.setText(_translate("frmAddTransformer", "Minimum Transformer Size in kVA", None))
        self.label_7.setText(_translate("frmAddTransformer", "Maximum Transformer Size in kVA", None))
        self.label_8.setText(_translate("frmAddTransformer", "Tranformer Buffer in Meter", None))
        self.groupBox.setTitle(_translate("frmAddTransformer", "Dataset", None))
        self.groupBox_2.setTitle(_translate("frmAddTransformer", "Project Parameter", None))

import resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmAddTransformer = QtGui.QMainWindow()
    ui = Ui_frmAddTransformer()
    ui.setupUi(frmAddTransformer)
    frmAddTransformer.show()
    sys.exit(app.exec_())

