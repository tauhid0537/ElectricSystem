# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmReportViewer.ui'
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

class Ui_frmReport(object):
    def setupUi(self, frmReport):
        frmReport.setObjectName(_fromUtf8("frmReport"))
        frmReport.resize(974, 655)
        self.centralwidget = QtGui.QWidget(frmReport)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 951, 83))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(94, 19, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtPro = QtGui.QLineEdit(self.groupBox)
        self.txtPro.setEnabled(False)
        self.txtPro.setGeometry(QtCore.QRect(170, 16, 160, 22))
        self.txtPro.setToolTip(_fromUtf8(""))
        self.txtPro.setObjectName(_fromUtf8("txtPro"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(348, 19, 51, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(94, 49, 71, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(348, 49, 51, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.txtSub = QtGui.QLineEdit(self.groupBox)
        self.txtSub.setEnabled(False)
        self.txtSub.setGeometry(QtCore.QRect(170, 46, 160, 22))
        self.txtSub.setToolTip(_fromUtf8(""))
        self.txtSub.setObjectName(_fromUtf8("txtSub"))
        self.txtPBS = QtGui.QLineEdit(self.groupBox)
        self.txtPBS.setEnabled(False)
        self.txtPBS.setGeometry(QtCore.QRect(416, 16, 160, 22))
        self.txtPBS.setToolTip(_fromUtf8(""))
        self.txtPBS.setObjectName(_fromUtf8("txtPBS"))
        self.txtFed = QtGui.QLineEdit(self.groupBox)
        self.txtFed.setEnabled(False)
        self.txtFed.setGeometry(QtCore.QRect(416, 46, 160, 22))
        self.txtFed.setToolTip(_fromUtf8(""))
        self.txtFed.setObjectName(_fromUtf8("txtFed"))
        self.frame = QtGui.QFrame(self.groupBox)
        self.frame.setGeometry(QtCore.QRect(10, 10, 62, 62))
        self.frame.setStyleSheet(_fromUtf8("image: url(:/plugins/ElectricSystems/Resources/FormIcons/basicnreca.png);"))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.cmdClose = QtGui.QPushButton(self.groupBox)
        self.cmdClose.setGeometry(QtCore.QRect(877, 20, 50, 40))
        self.cmdClose.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basicexit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdClose.setIcon(icon)
        self.cmdClose.setIconSize(QtCore.QSize(32, 32))
        self.cmdClose.setObjectName(_fromUtf8("cmdClose"))
        self.cmdHelp = QtGui.QPushButton(self.groupBox)
        self.cmdHelp.setGeometry(QtCore.QRect(820, 20, 50, 40))
        self.cmdHelp.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basichelp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdHelp.setIcon(icon1)
        self.cmdHelp.setIconSize(QtCore.QSize(32, 32))
        self.cmdHelp.setObjectName(_fromUtf8("cmdHelp"))
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(760, 20, 50, 40))
        self.pushButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/print.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setGeometry(QtCore.QRect(10, 110, 951, 491))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        '''frmReport.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(frmReport)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 974, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        frmReport.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(frmReport)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frmReport.setStatusBar(self.statusbar)'''

        self.retranslateUi(frmReport)
        QtCore.QMetaObject.connectSlotsByName(frmReport)

    def retranslateUi(self, frmReport):
        frmReport.setWindowTitle(_translate("frmReport", "Report Viewer", None))
        self.label.setText(_translate("frmReport", "Project", None))
        self.label_2.setText(_translate("frmReport", "Database", None))
        self.label_3.setText(_translate("frmReport", "Substation", None))
        self.label_4.setText(_translate("frmReport", "Feeder", None))
        self.cmdClose.setToolTip(_translate("frmReport", "Close", None))
        self.cmdHelp.setToolTip(_translate("frmReport", "Help", None))

from PyQt4 import QtWebKit
import resources
