# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmValidate.ui'
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

class Ui_frmValidate(object):
    def setupUi(self, frmValidate):
        frmValidate.setObjectName(_fromUtf8("frmValidate"))
        frmValidate.resize(940, 530)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmValidate.sizePolicy().hasHeightForWidth())
        frmValidate.setSizePolicy(sizePolicy)
        frmValidate.setMaximumSize(QtCore.QSize(940, 530))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/formaccept.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmValidate.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(frmValidate)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 921, 86))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(97, 21, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtPro = QtGui.QLineEdit(self.groupBox)
        self.txtPro.setEnabled(False)
        self.txtPro.setGeometry(QtCore.QRect(170, 18, 125, 22))
        self.txtPro.setToolTip(_fromUtf8(""))
        self.txtPro.setObjectName(_fromUtf8("txtPro"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(319, 21, 51, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(97, 51, 71, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(319, 51, 51, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.txtSub = QtGui.QLineEdit(self.groupBox)
        self.txtSub.setEnabled(False)
        self.txtSub.setGeometry(QtCore.QRect(170, 48, 125, 22))
        self.txtSub.setToolTip(_fromUtf8(""))
        self.txtSub.setObjectName(_fromUtf8("txtSub"))
        self.txtPBS = QtGui.QLineEdit(self.groupBox)
        self.txtPBS.setEnabled(False)
        self.txtPBS.setGeometry(QtCore.QRect(399, 18, 125, 22))
        self.txtPBS.setToolTip(_fromUtf8(""))
        self.txtPBS.setObjectName(_fromUtf8("txtPBS"))
        self.txtFed = QtGui.QLineEdit(self.groupBox)
        self.txtFed.setEnabled(False)
        self.txtFed.setGeometry(QtCore.QRect(399, 48, 125, 22))
        self.txtFed.setToolTip(_fromUtf8(""))
        self.txtFed.setObjectName(_fromUtf8("txtFed"))
        self.frame = QtGui.QFrame(self.groupBox)
        self.frame.setGeometry(QtCore.QRect(11, 12, 62, 62))
        self.frame.setStyleSheet(_fromUtf8("image: url(:/plugins/ElectricSystems/Resources/FormIcons/basicnreca.png);"))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.cmdJumper = QtGui.QPushButton(self.groupBox)
        self.cmdJumper.setGeometry(QtCore.QRect(685, 23, 50, 40))
        self.cmdJumper.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/jumperdraw.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdJumper.setIcon(icon1)
        self.cmdJumper.setIconSize(QtCore.QSize(32, 32))
        self.cmdJumper.setObjectName(_fromUtf8("cmdJumper"))
        self.cmdSave = QtGui.QPushButton(self.groupBox)
        self.cmdSave.setGeometry(QtCore.QRect(740, 23, 50, 40))
        self.cmdSave.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/textsave.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdSave.setIcon(icon2)
        self.cmdSave.setIconSize(QtCore.QSize(32, 32))
        self.cmdSave.setObjectName(_fromUtf8("cmdSave"))
        self.cmdHelp = QtGui.QPushButton(self.groupBox)
        self.cmdHelp.setGeometry(QtCore.QRect(795, 23, 50, 40))
        self.cmdHelp.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basichelp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdHelp.setIcon(icon3)
        self.cmdHelp.setIconSize(QtCore.QSize(32, 32))
        self.cmdHelp.setObjectName(_fromUtf8("cmdHelp"))
        self.cmdClose = QtGui.QPushButton(self.groupBox)
        self.cmdClose.setGeometry(QtCore.QRect(850, 23, 50, 40))
        self.cmdClose.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ElectricSystems/Resources/FormIcons/basicexit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdClose.setIcon(icon4)
        self.cmdClose.setIconSize(QtCore.QSize(32, 32))
        self.cmdClose.setObjectName(_fromUtf8("cmdClose"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(250, 107, 681, 411))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.webView = QtWebKit.QWebView(self.groupBox_2)
        self.webView.setGeometry(QtCore.QRect(4, 4, 673, 403))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.treeView = QtGui.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(10, 107, 231, 411))
        self.treeView.setFrameShadow(QtGui.QFrame.Plain)
        self.treeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.treeView.setIconSize(QtCore.QSize(48, 48))
        self.treeView.setUniformRowHeights(True)
        self.treeView.setAnimated(True)
        self.treeView.setHeaderHidden(True)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        #frmValidate.setCentralWidget(self.centralwidget)

        self.retranslateUi(frmValidate)
        QtCore.QMetaObject.connectSlotsByName(frmValidate)

    def retranslateUi(self, frmValidate):
        frmValidate.setWindowTitle(_translate("frmValidate", "Validate Database", None))
        self.label.setText(_translate("frmValidate", "Project", None))
        self.label_2.setText(_translate("frmValidate", "Database", None))
        self.label_3.setText(_translate("frmValidate", "Substation", None))
        self.label_4.setText(_translate("frmValidate", "Feeder", None))
        self.cmdJumper.setToolTip(_translate("frmValidate", "Create Jumper for Transformer", None))
        self.cmdSave.setToolTip(_translate("frmValidate", "Save Validation Result", None))
        self.cmdHelp.setToolTip(_translate("frmValidate", "Help", None))
        self.cmdClose.setToolTip(_translate("frmValidate", "Close", None))

from PyQt4 import QtWebKit
import resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmValidate = QtGui.QMainWindow()
    ui = Ui_frmValidate()
    ui.setupUi(frmValidate)
    frmValidate.show()
    sys.exit(app.exec_())

