from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import csv
import sys
import os
from datetime import datetime

from utility import *
import utility


sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ValidateDatabase")
from frmValidate import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Resources/FormIcons")
import resources

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class frmValidate_dialog(QDialog, Ui_frmValidate):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.usr = basicOps.usrname
        self.dbase = basicOps.dbasename
        self.hst = basicOps.hostname
        self.paswrd = basicOps.password
        self.sub = basicOps.substation
        self.fed = basicOps.feeder

        model = QStandardItemModel()
        self.treeView.setModel(model)
        self.treeView.setUniformRowHeights(True)


        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(os.path.dirname(__file__)+"/Resources/FormIcons/validate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        mainNode = QStandardItem('Validate')
        mainNode.setIcon(icon)

        iconNode1 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/valtopology.png')
        subNode1 = QStandardItem('Topology')
        subNode1.setIcon(iconNode1)

        iSub1Node1 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/valsubloc.png')
        sub1Node1 = QStandardItem('Substation Location')
        sub1Node1.setIcon(iSub1Node1)

        iSub1Node2 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/valpoleloc.png')
        sub1Node2 = QStandardItem('Pole Location')
        sub1Node2.setIcon(iSub1Node2)

        iSub1Node3 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/vallineloc.png')
        sub1Node3 = QStandardItem('Line Location')
        sub1Node3.setIcon(iSub1Node3)

        iSub1Node4 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/vallinepoletopo.png')
        sub1Node4 = QStandardItem('Line-Pole Topology')
        sub1Node4.setIcon(iSub1Node4)

        iSub1Node5 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/vallinelinetopo.png')
        sub1Node5 = QStandardItem('Line-Line Topology')
        sub1Node5.setIcon(iSub1Node5)

        subNode1.appendRow([sub1Node1])
        subNode1.appendRow([sub1Node2])
        subNode1.appendRow([sub1Node3])
        subNode1.appendRow([sub1Node4])
        subNode1.appendRow([sub1Node5])

        iconNode2 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/valattribute.png')
        subNode2 = QStandardItem('Attribute')
        subNode2.setIcon(iconNode2)

        iSub2Node1 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/valsubloc.png')
        sub2Node1 = QStandardItem('Substation')
        sub2Node1.setIcon(iSub2Node1)

        iSub2Node2 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/valpoleloc.png')
        sub2Node2 = QStandardItem('Pole')
        sub2Node2.setIcon(iSub2Node2)

        iSub2Node3 = QtGui.QIcon(os.path.dirname(__file__) + '/Resources/FormIcons/vallineloc.png')
        sub2Node3 = QStandardItem('Line')
        sub2Node3.setIcon(iSub2Node3)

        subNode2.appendRow([sub2Node1])
        subNode2.appendRow([sub2Node2])
        subNode2.appendRow([sub2Node3])

        mainNode.appendRow([subNode1])
        mainNode.appendRow([subNode2])
        model.appendRow(mainNode)

        self.cmdJumper.clicked.connect(self.getText)
        self.cmdClose.clicked.connect(self.onClose)
        self.treeView.clicked.connect(self.getProcessName)

    def getText(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Main Form")
        msgBox.setText("It is Working...")
        ret = msgBox.exec_()

    def getProcessName(self):
        index = self.treeView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index).text()

        if item == 'Substation Location':
            self.webView.setHtml('')
            htmlfile = self.subLocValidation()
            local_url = QUrl.fromLocalFile(htmlfile)
            self.webView.load(local_url)
        elif item == 'Pole Location':
            self.webView.setHtml('')
            htmlfile = self.duplicatePoleLocation()
            local_url = QUrl.fromLocalFile(htmlfile)
            self.webView.load(local_url)
        elif item == 'Line Location':
            self.webView.setHtml('')
            htmlfile = self.duplicateLineLocation()
            local_url = QUrl.fromLocalFile(htmlfile)
            self.webView.load(local_url)
        elif item == 'Line-Pole Topology':
            self.webView.setHtml('')
            htmlfile = self.linePoleValidation()
            local_url = QUrl.fromLocalFile(htmlfile)
            self.webView.load(local_url)
        elif item == 'Line-Line Topology':
            self.webView.setHtml('')
            htmlfile = self.lineLineValidation()
            local_url = QUrl.fromLocalFile(htmlfile)
            self.webView.load(local_url)
        elif item == 'Substation':
            self.webView.setHtml('')
            htmlfile = self.subAttrValidate()
            local_url = QUrl.fromLocalFile(htmlfile)
            self.webView.load(local_url)
        elif item == 'Line':
            self.webView.setHtml('')
            htmlfile = self.lineAttrValidate()
            local_url = QUrl.fromLocalFile(htmlfile)
            self.webView.load(local_url)
        elif item == 'Pole':
            self.webView.setHtml('')
            htmlfile = self.poleAttrValidate()
            local_url = QUrl.fromLocalFile(htmlfile)
            self.webView.load(local_url)

        #msgBox = QtGui.QMessageBox()
        #msgBox.setWindowTitle("Main Form")
        #msgBox.setText(item)
        #ret = msgBox.exec_()

    def getCursor(self, usr, hst, pas, db):
        cur = None
        try:
            condb = psycopg2.connect(user = usr, host = hst, password = pas, dbname = db)
            condb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = condb.cursor()
        except psycopg2.Error as e:
            QMessageBox.critical(self.iface.mainWindow(),"Connection Error",str("Unable to connect!\n{0}").format(e))
        return cur

    def subLocValidation(self):
        msg = None
        subTable = 'esystems.' + self.sub + '_substation'
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, self.sub, self.fed)
        subcode = bsops.getSubCode(cur, self.sub)
        linetable = 'esystems.' + subcode + '_' + fedcode + '_line'
        htmlfilepath = os.path.dirname(__file__) + "/ValidationResults/"+self.sub+"_"+"validation.html"
        htmlfirst = """<html>
        <meta http-equiv='X-UA-Compatible' content='IE=edge' />
        <style type='text/css'>
        BODY
        {
        font-family:'Verdana';
        font-size:8pt;
        margin :2px;
        margin-left:10px;
        margin-right:10px;
        padding: 0px;
        }
        </style>
        <body>
        <p><b>Validation Started: """ + str(datetime.now()) + """</b></p>
        <p>Validating Substation Location...</p>
        """
        if os.path.exists(htmlfilepath):
            os.remove(htmlfilepath)
        htmlfile = open(htmlfilepath, 'w')
        htmlfile.write(htmlfirst)
        subsql = "select count(*) from " + subTable
        cur.execute(subsql)
        r = cur.fetchone()
        if r[0] > 1:
            msg = "<p style='color:red;'>ERROR : Multiple Substation Locations Found</p>"
            htmlfile.write(msg)
        elif r[0] == 0:
            msg = "<p style='color:red;'>ERROR : Substation DOES NOT Exist</p>"
            htmlfile.write(msg)

        sublocsql = "select count(*) from " + subTable + " a inner join " + linetable + " b on ST_Intersects(a.geom, b.geom)"
        cur.execute(sublocsql)
        row = cur.fetchone()

        if row[0] == 0:
            msg = "<p style='color:red;'>ERROR: Substation Not Connected to Feeder</p>"
            htmlfile.write(msg)
        elif row[0] ==1:
            msg = "<p style='color:green;'>Substation Connected to Line<br/>"
            htmlfile.write(msg)
        elif row[0] > 1:
            msg = "<p style='color:red;'>ERROR : Multiple Lines Connected to Substation</p>"
            htmlfile.write(msg)
        htmlfile.write("<p><b>Process Completed: " + str(datetime.now()) + "</b></p>")
        htmlfile.write("</body>")
        htmlfile.write("</html>")
        htmlfile.close()

        return htmlfilepath

    def duplicatePoleLocation(self):
        msg = None
        subTable = 'esystems.' + self.sub + '_substation'
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, self.sub, self.fed)
        subcode = bsops.getSubCode(cur, self.sub)
        linetable = 'esystems.' + subcode + '_' + fedcode + '_line'
        poletable = 'esystems.' + subcode + '_' + fedcode + '_pole'
        htmlfilepath = os.path.dirname(__file__) + "/ValidationResults/" + self.sub +"_" + self.fed + "_validation.html"
        htmlfirst = """<html>
        <meta http-equiv='X-UA-Compatible' content='IE=edge' />
        <style type='text/css'>
        BODY
        {
        font-family:'Verdana';
        font-size:8pt;
        margin :2px;
        margin-left:10px;
        margin-right:10px;
        padding: 0px;
        }
        </style>
        <body>
        <p><b>Validation Started: """ + str(datetime.now()) + """</b></p>
        <p>Validating Pole Geometry...</p>
        """
        if os.path.exists(htmlfilepath):
            os.remove(htmlfilepath)
        htmlfile = open(htmlfilepath, 'w')
        htmlfile.write(htmlfirst)

        polesql = "select a.objectid, a.pole_number from " + poletable + " a inner join " + poletable + " b on ST_Intersects(a.geom, b.geom) and (a.objectid <> b.objectid)"
        cur.execute(polesql)
        rows = cur.fetchall()
        if cur.rowcount > 0:
            for row in rows:
                if row[1] is None:
                    id = 'ObjectID- ' + row[0]
                    msg = "<p style='color:red;'>ERROR : Multiple Pole on the Same Location. Pole Number: " + id + "</p>"
                    htmlfile.write(msg)
                else:
                    msg = "<p style='color:red;'>ERROR : Multiple Pole on the Same Location. Pole Number: " + row[1] + "</p>"
                    htmlfile.write(msg)
        else:
             msg = "<p style='color:green;'>No Problem with pole Locations</p>"
             htmlfile.write(msg)

        htmlfile.write("<p><b>Process Completed: " + str(datetime.now()) + "</b></p>")
        htmlfile.write("</body>")
        htmlfile.write("</html>")
        htmlfile.close()

        return htmlfilepath

    def duplicateLineLocation(self):
        msg = None
        subTable = 'esystems.' + self.sub + '_substation'
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, self.sub, self.fed)
        subcode = bsops.getSubCode(cur, self.sub)
        linetable = 'esystems.' + subcode + '_' + fedcode + '_line'
        poletable = 'esystems.' + subcode + '_' + fedcode + '_pole'
        htmlfilepath = os.path.dirname(__file__) + "/ValidationResults/" + self.sub +"_" + self.fed + "_line_validation.html"
        htmlfirst = """<html>
        <meta http-equiv='X-UA-Compatible' content='IE=edge' />
        <style type='text/css'>
        BODY
        {
        font-family:'Verdana';
        font-size:8pt;
        margin :2px;
        margin-left:10px;
        margin-right:10px;
        padding: 0px;
        }
        </style>
        <body>
        <p><b>Validation Started: """ + str(datetime.now()) + """</b></p>
        <p>Validating Line Geometry...</p>
        """
        if os.path.exists(htmlfilepath):
            os.remove(htmlfilepath)
        htmlfile = open(htmlfilepath, 'w')
        htmlfile.write(htmlfirst)

        linesql = "select a.objectid, a.section_id from " + linetable + " a inner join " + linetable + " b on ST_Equals(a.geom, b.geom) and (a.objectid <> b.objectid)"
        cur.execute(linesql)
        rows = cur.fetchall()
        if cur.rowcount > 0:
            for row in rows:
                if row[1] is None:
                    id = 'ObjectID- ' + row[0]
                    msg = "<p style='color:red;'>ERROR : Multiple Line Section on the same Location. Line Section Number: " + id + "</p>"
                    htmlfile.write(msg)
                else:
                    msg = "<p style='color:red;'>ERROR : Multiple Line Section on the same Location. Line Section Number: " + row[1] + "</p>"
                    htmlfile.write(msg)
        else:
             msg = "<p style='color:green;'>No Problem with Line Locations</p>"
             htmlfile.write(msg)

        htmlfile.write("<p><b>Process Completed: " + str(datetime.now()) + "</b></p>")
        htmlfile.write("</body>")
        htmlfile.write("</html>")
        htmlfile.close()

        return htmlfilepath

    def linePoleValidation(self):
        msg = None
        subTable = 'esystems.' + self.sub + '_substation'
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, self.sub, self.fed)
        subcode = bsops.getSubCode(cur, self.sub)
        linetable = 'esystems.' + subcode + '_' + fedcode + '_line'
        poletable = 'esystems.' + subcode + '_' + fedcode + '_pole'
        htmlfilepath = os.path.dirname(__file__) + "/ValidationResults/" + self.sub +"_" + self.fed + "_line-pole_validation.html"
        htmlfirst = """<html>
        <meta http-equiv='X-UA-Compatible' content='IE=edge' />
        <style type='text/css'>
        BODY
        {
        font-family:'Verdana';
        font-size:8pt;
        margin :2px;
        margin-left:10px;
        margin-right:10px;
        padding: 0px;
        }
        </style>
        <body>
        <p><b>Validation Started: """ + str(datetime.now()) + """</b></p>
        <p>Validating Pole-Line Topology checking...</p>
        """
        if os.path.exists(htmlfilepath):
            os.remove(htmlfilepath)
        htmlfile = open(htmlfilepath, 'w')
        htmlfile.write(htmlfirst)

        polesql = "select a.objectid, a.pole_number from " + poletable + " a where not exists(SELECT 1 FROM " + linetable + " b WHERE ST_Intersects(a.geom, b.geom))"
        cur.execute(polesql)
        rows = cur.fetchall()
        if cur.rowcount > 0:
            for row in rows:
                if row[1] is None:
                    id = 'ObjectID- ' + row[0]
                    msg = "<p style='color:red;'>ERROR : Pole not connected with any Line Section Pole Number: " + id + "</p>"
                    htmlfile.write(msg)
                else:
                    msg = "<p style='color:red;'>ERROR : Pole not connected with any Line Section Pole Number: " + row[1] + "</p>"
                    htmlfile.write(msg)
        else:
             msg = "<p style='color:green;'>Pole-Line Topology Checked</p>"
             htmlfile.write(msg)

        htmlfile.write("<p>Validating Line-Pole Topology checking...</p>")
        frompolesql = "select a.objectid, a.section_id from " + linetable + " a where not exists(SELECT 1 FROM " + poletable + " b where ST_Intersects(ST_StartPoint(a.geom), b.geom))"
        cur.execute(frompolesql)
        rows = cur.fetchall()
        if cur.rowcount > 0:
            for row in rows:
                if row[1] is None:
                    id = 'ObjectID- ' + row[0]
                    msg = "<p style='color:red;'>ERROR : No From Pole for Line Section, Line Number: " + id + "</p>"
                    htmlfile.write(msg)
                else:
                    msg = "<p style='color:red;'>ERROR : No From Pole for Line Section, Line Number: " + row[1] + "</p>"
                    htmlfile.write(msg)
        else:
             msg = "<p style='color:green;'>From Pole and Line Topology Checked</p>"
             htmlfile.write(msg)

        topolesql = "select a.objectid, a.section_id from " + linetable + " a where not exists(SELECT 1 FROM " + poletable + " b where ST_Intersects(ST_EndPoint(a.geom), b.geom))"
        cur.execute(topolesql)
        rows = cur.fetchall()
        if cur.rowcount > 0:
            for row in rows:
                if row[1] is None:
                    id = 'ObjectID- ' + row[0]
                    msg = "<p style='color:red;'>ERROR : No To Pole for Line Section, Line Number: " + id + "</p>"
                    htmlfile.write(msg)
                else:
                    msg = "<p style='color:red;'>ERROR : No To Pole for Line Section, Line Number: " + row[1] + "</p>"
                    htmlfile.write(msg)
        else:
             msg = "<p style='color:green;'>To Pole and Line Topology Checked</p>"
             htmlfile.write(msg)

        htmlfile.write("<p><b>Process Completed: " + str(datetime.now()) + "</b></p>")
        htmlfile.write("</body>")
        htmlfile.write("</html>")
        htmlfile.close()

        return htmlfilepath

    def lineLineValidation(self):
        msg = None
        subTable = 'esystems.' + self.sub + '_substation'
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, self.sub, self.fed)
        subcode = bsops.getSubCode(cur, self.sub)
        linetable = 'esystems.' + subcode + '_' + fedcode + '_line'
        poletable = 'esystems.' + subcode + '_' + fedcode + '_pole'
        htmlfilepath = os.path.dirname(__file__) + "/ValidationResults/" + self.sub +"_" + self.fed + "_line-line_validation.html"
        htmlfirst = """<html>
        <meta http-equiv='X-UA-Compatible' content='IE=edge' />
        <style type='text/css'>
        BODY
        {
        font-family:'Verdana';
        font-size:8pt;
        margin :2px;
        margin-left:10px;
        margin-right:10px;
        padding: 0px;
        }
        </style>
        <body>
        <p><b>Validation Started: """ + str(datetime.now()) + """</b></p>
        <p>Validating Line-Line Topology...</p>
        """
        if os.path.exists(htmlfilepath):
            os.remove(htmlfilepath)
        htmlfile = open(htmlfilepath, 'w')
        htmlfile.write(htmlfirst)

        linelinesql = "select a.objectid, a.section_id from "+ linetable + " a where not exists(SELECT 1 FROM " + linetable + " b WHERE (a.objectid != b.objectid) AND ST_Intersects(a.geom, b.geom))"
        cur.execute(linelinesql)
        rows = cur.fetchall()
        if cur.rowcount > 0:
            for row in rows:
                if row[1] is None:
                    id = 'ObjectID- ' + row[0]
                    msg = "<p style='color:red;'>ERROR : Line Section not connected with any Line Section Line Number: " + id + "</p>"
                    htmlfile.write(msg)
                else:
                    msg = "<p style='color:red;'>ERROR : Line Section not connected with any Line Section Line Number: " + row[1] + "</p>"
                    htmlfile.write(msg)
        msg = "Line-Line Topology Checked</br>"
        htmlfile.write(msg)
        htmlfile.write("<p><b>Process Completed: " + str(datetime.now()) + "</b></p>")
        htmlfile.write("</body>")
        htmlfile.write("</html>")
        htmlfile.close()

        return htmlfilepath

    def subAttrValidate(self):
        #SELECT objectid, substation, sub_code, sub_type_cat, sub_no_of_fed, sub_cap, sub_trn_num, location, remarks, geom FROM esystems.delduar_substation
        msg = None
        subTable = 'esystems.' + self.sub + '_substation'
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, self.sub, self.fed)
        subcode = bsops.getSubCode(cur, self.sub)
        linetable = 'esystems.' + subcode + '_' + fedcode + '_line'
        poletable = 'esystems.' + subcode + '_' + fedcode + '_pole'
        htmlfilepath = os.path.dirname(__file__) + "/ValidationResults/" + self.sub +"_attribute_validation.html"
        htmlfirst = """<html>
        <meta http-equiv='X-UA-Compatible' content='IE=edge' />
        <style type='text/css'>
        BODY
        {
        font-family:'Verdana';
        font-size:8pt;
        margin :2px;
        margin-left:10px;
        margin-right:10px;
        padding: 0px;
        }
        </style>
        <body>
        <p><b>Validation Started: """ + str(datetime.now()) + """</b></p>
        <p>Validating Substation Attribute ...</p>
        """
        if os.path.exists(htmlfilepath):
            os.remove(htmlfilepath)
        htmlfile = open(htmlfilepath, 'w')
        htmlfile.write(htmlfirst)

        subsql = "SELECT substation, sub_code, sub_type_cat, sub_no_of_fed, sub_cap, sub_trn_num, location, remarks, geom FROM "+subTable
        cur.execute(subsql)

        if cur.rowcount == 1:
            row = cur.fetchone()
            if row[0].strip() != basicOps.substation:
                htmlfile.write("<p style='color:blue;'>Substation Name does not Match</p><br/>")
            if row[1].strip() != subcode:
                htmlfile.write("<p style='color:blue;'>Substation Code does not Match</p><br/>")
            if row[2].strip() is None:
                htmlfile.write("<p style='color:blue;'>Substation Type Missing</p><br/>")
            if row[3] == 0:
                htmlfile.write("<p style='color:blue;'>No Feeder for Substation in the Substation Table</p><br/>")
            if row[4] ==0:
                htmlfile.write("<p style='color:blue;'>No Substation Capacity Found in the Substation Table</p><br/>")
            if row[5] ==0:
                htmlfile.write("<p style='color:blue;'>No Transformer for Substation in the Substation Table</p><br/>")
            if row[4] ==0:
                htmlfile.write("<p style='color:blue;'>No Location information found in the Substation Table</p><br/>")
        elif cur.rowcount >1:
            htmlfile.write("<p style='color:red;'>ERROR : Multiple Substation Locations Found</p><br/>")
        else:
            htmlfile.write("<p style='color:red;'>ERROR : Substation does not exist</p><br/>")

        htmlfile.write("<p><b>Process Completed: " + str(datetime.now()) + "</b></p>")
        htmlfile.write("</body>")
        htmlfile.write("</html>")
        htmlfile.close()

        return htmlfilepath

    def checkPhase(self, secPh, prSecPh):
        match = False
        if secPh is not None or prSecPh is not None:
            if secPh == prSecPh:
                match = True
            else:
                if prSecPh is not None:
                    if '-' in prSecPh:
                        phases = prSecPh.split('-')
                        for idx in range(len(phases)):
                            if secPh == phases[idx]:
                                match = True
        return match
    def getSysPhase(self):
        ph = None
        sql = "select sysphase from sysinp.phase_con"
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        cur.execute(sql)
        row = cur.fetchone()
        ph = row[0]
        return ph


    def lineAttrValidate(self):
        msg = None
        subTable = 'esystems.' + self.sub + '_substation'
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, self.sub, self.fed)
        subcode = bsops.getSubCode(cur, self.sub)
        linetable = 'esystems.' + subcode + '_' + fedcode + '_line'
        poletable = 'esystems.' + subcode + '_' + fedcode + '_pole'
        htmlfilepath = os.path.dirname(__file__) + "/ValidationResults/" + self.sub +"_attribute_validation.html"
        htmlfirst = """<html>
        <meta http-equiv='X-UA-Compatible' content='IE=edge' />
        <style type='text/css'>
        BODY
        {
        font-family:'Verdana';
        font-size:8pt;
        margin :2px;
        margin-left:10px;
        margin-right:10px;
        padding: 0px;
        }
        </style>
        <body>
        <p><b>Validation Started: """ + str(datetime.now()) + """</b></p>
        <p>Validating Line Attribute ...</p>
        """
        if os.path.exists(htmlfilepath):
            os.remove(htmlfilepath)
        htmlfile = open(htmlfilepath, 'w')
        htmlfile.write(htmlfirst)

        linesql = """SELECT objectid, substation, feeder, line_align, line_voltage, line_type, section_id, phase, trans_code, sec_con, trans_ref, con_size_1,
        con_size_2, con_size_3, con_size_n, line_status, data_source, remarks FROM """ + linetable
        cur.execute(linesql)
        if cur.rowcount == 0:
            htmlfile.write("<p style='color:red;'>ERROR : No Lines in Line Table</p><br/>")
        elif cur.rowcount > 0:
            rows = cur.fetchall()
            for row in rows:
                if row[6] is None:
                    id = 'Object ID-' + row[0]
                    htmlfile.write("<b>Line Section : " + id + "</b><br/>")
                    htmlfile.write("<p style='color:red;'><b>ERROR : Line Section ID Missing</b></p><br/>")
                else:
                    htmlfile.write("<b>Line Section : " + row[6] + "</b><br/>")
                    sql1 = "select count(*) from " + linetable + " where section_id = '" + row[6] + "'"
                    cur.execute(sql1)
                    r1 = cur.fetchone()
                    if r1[0] >1:
                        htmlfile.write("<p style='color:red;'>Duplicte Section ID </p><br/>")

                if row[1] != basicOps.substation:
                    htmlfile.write("<p style='color:red;'>ERROR : Incorect Substation Name</p><br/>")
                if row[2] != basicOps.feeder:
                    htmlfile.write("<p style='color:red;'>ERROR : Incorect Feeder Name</p><br/>")
                if row[3] is None:
                    htmlfile.write("No Section Alignment<br/>")
                if row[4] == 0:
                    htmlfile.write("<p style='color:red;'>ERROR : No Section Voltage</p><br/>")
                if row[5] is None:
                    htmlfile.write("No Section Type<br/>")
                if row[7] is None:
                    htmlfile.write("<p style='color:red;'>ERROR : No Section Phase</p><br/>")
                if row[7] is not None:
                    sql2 = """select a.objectid , a.section_id SectionID, a.phase Phase, b.objectid p_id, b.section_id ParentSecID, b.phase ParentPhase from """ + linetable + """ a inner join """ + linetable + """ b
                    on ST_Equals(ST_StartPoint(a.geom), ST_EndPoint(b.geom)) and a.objectid != b.objectid and a.section_id = '""" + row[6] + "'"
                    cur.execute(sql2)
                    if cur.rowcount > 0:
                        r2 = cur.fetchone()
                        prPhase = r2[5]
                        secPh = row[7]
                        match = self.checkPhase(secPh, prPhase)
                        if not match:
                            htmlfile.write("<p style='color:red;'>ERROR : Section Phase does not Match with Parent Section</p><br/>")
                    else:
                        htmlfile.write("<p style='color:red;'>ERROR : No Parent Section Phase</p><br/>")

                if row[8] is None:
                    htmlfile.write("No Transposition Code<br/>")
                if row[9] is None:
                    htmlfile.write("ERROR : No Section Configuration<br/>")
                if row[10] == 'Secondary Distribution':
                    sql3 = "select count(*) from " + poletable + "a inner join " + linetable + "b on ST_Equals(ST_StartPoint(b.geom),a.geom) and b.objectid = " + row[0]
                    cur.execute(sql3)
                    if cur.rowcont == 0:
                        htmlfile.write("<p style='color:red;'>ERROR : No Transformer Reference</p><br/>")
                sysphase = self.getSysPhase()
                con1 = row[11]
                con2 = row[12]
                con3 = row[13]
                conN = row[14]
                if sysphase == 'RYB':
                    if row[7] is not None:
                        if row[7] == 'R':
                            if con1 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Conductor Size for Phase 1</p><br/>")
                            if con2 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 2</p><br/>")
                            if con3 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 3</p><br/>")
                        if row[7] == 'Y':
                            if con2 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 2</p><br/>")
                            if con1 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 1</p><br/>")
                            if con3 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 3</p><br/>")
                        if row[7] == 'B':
                            if con3 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 3</p><br/>")
                            if con1 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 1</p><br/>")
                            if con2 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 2</p><br/>")
                        if row[7] == 'R-Y':
                            if con1 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 1</p><br/>")
                            if con2 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 2</p><br/>")
                            if con3 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 3</p><br/>")
                        if row[7] == 'Y-B':
                            if con2 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 2</p><br/>")
                            if con3 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 3</p><br/>")
                            if con1 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 1</p><br/>")
                        if row[7] == 'B-R':
                            if con3 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 3</p><br/>")
                            if con1 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 1</p><br/>")
                            if con2 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 2</p><br/>")
                        if row[7] == 'R-Y-B':
                            if con1 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 1</p><br/>")
                            if con2 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 2</p><br/>")
                            if con3 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 3</p><br/>")
                if sysphase == 'ABC':
                    if row[7] is not None:
                        if row[7] == 'A':
                            if con1 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Conductor Size for Phase 1</p><br/>")
                            if con2 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 2</p><br/>")
                            if con3 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 3</p><br/>")
                        if row[7] == 'B':
                            if con2 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 2</p><br/>")
                            if con1 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 1</p><br/>")
                            if con3 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 3</p><br/>")
                        if row[7] == 'C':
                            if con3 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 3</p><br/>")
                            if con1 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 1</p><br/>")
                            if con2 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 2</p><br/>")
                        if row[7] == 'A-B':
                            if con1 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 1</p><br/>")
                            if con2 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 2</p><br/>")
                            if con3 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 3</p><br/>")
                        if row[7] == 'B-C':
                            if con2 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 2</p><br/>")
                            if con3 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 3</p><br/>")
                            if con1 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 1</p><br/>")
                        if row[7] == 'C-A':
                            if con3 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 3</p><br/>")
                            if con1 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 1</p><br/>")
                            if con2 is not None:
                                htmlfile.write("<p style='color:red;'>ERROR : Should not be the value for Phase 2</p><br/>")
                        if row[7] == 'A-B-C':
                            if con1 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 1</p><br/>")
                            if con2 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 2</p><br/>")
                            if con3 is None:
                                htmlfile.write("<p style='color:red;'>ERROR : No Size for Conductor 3</p><br/>")
                if row[15] is None:
                    htmlfile.write("No line status for section<br/>")
                if row[16] is None:
                    htmlfile.write("No Data Source for Line Section<br/>")
        htmlfile.write("<p><b>Process Completed: " + str(datetime.now()) + "</b></p>")
        htmlfile.write("</body>")
        htmlfile.write("</html>")
        htmlfile.close()

        return htmlfilepath

    def poleAttrValidate(self):
        #SELECT objectid, substation, feeder, line_align, line_voltage, line_type, section_id, phase, trans_code, sec_con, trans_ref, con_size_1,
        #con_size_2, con_size_3, con_size_n, line_status, data_source, remarks, geom  FROM esystems.del_d2b_line
        msg = None
        subTable = 'esystems.' + self.sub + '_substation'
        cur = self.getCursor(self.usr, self.hst, self.paswrd, self.dbase)
        bsops = utility.basicOps()
        fedcode = bsops.getFedCode(cur, self.sub, self.fed)
        subcode = bsops.getSubCode(cur, self.sub)
        linetable = 'esystems.' + subcode + '_' + fedcode + '_line'
        poletable = 'esystems.' + subcode + '_' + fedcode + '_pole'
        htmlfilepath = os.path.dirname(__file__) + "/ValidationResults/" + self.sub +"_attribute_validation.html"
        htmlfirst = """<html>
        <meta http-equiv='X-UA-Compatible' content='IE=edge' />
        <style type='text/css'>
        BODY
        {
        font-family:'Verdana';
        font-size:8pt;
        margin :2px;
        margin-left:10px;
        margin-right:10px;
        padding: 0px;
        }
        </style>
        <body>
        <p><b>Validation Started: """ + str(datetime.now()) + """</b></p>
        <p>Validating Pole Attribute ...</p>
        """
        if os.path.exists(htmlfilepath):
            os.remove(htmlfilepath)
        htmlfile = open(htmlfilepath, 'w')
        htmlfile.write(htmlfirst)

        polesql = """SELECT objectid, substation, feeder, gps_no, fed_on_pole, pole_number, pole_use, pole_phase, pole_height, pole_class, pole_structure, pole_fitting,
        pole_guy, pole_guytype, pole_guyag, pole_status, equip_type, reference_pole, equip_id, equip_unit, equip_mount, equip_size,
        equip_phase, equip_status, equip_use, trans_ref, rs_con, sc_con, lc_con, si_con, li_con, pb_con, ag_con, st_con, location, data_source,
        remarks FROM """ + poletable
        cur.execute(polesql)
        if cur.rowcount == 0:
            htmlfile.write("<p style='color:red;'>ERROR : No Pole in Pole Table</p><br/>")
        elif cur.rowcount > 0:
            rows = cur.fetchall()
            for row in rows:
                if row[5] is None:
                    id = 'Object ID-' + row[0]
                    htmlfile.write("<b>Pole Number : " + id + "</b><br/>")
                    htmlfile.write("<p style='color:red;'><b>ERROR : Pole Number is Missing</b></p><br/>")
                else:
                    htmlfile.write("<b>Pole Number : " + row[5] + "</b><br/>")
                    sql1 = "select count(*) from " + poletable + " where pole_number = '" + row[5] + "'"
                    cur.execute(sql1)
                    r1 = cur.fetchone()
                    if r1[0] >1:
                        htmlfile.write("<p style='color:red;'>ERROR : Duplicte Pole Number </p><br/>")
                if row[1] != basicOps.substation:
                    htmlfile.write("<p style='color:red;'>ERROR : Incorect Substation Name</p><br/>")
                if row[2] != basicOps.feeder:
                    htmlfile.write("<p style='color:red;'>ERROR : Incorect Feeder Name</p><br/>")
                if row[3] is None:
                    htmlfile.write("No GPS Location Number<br/>")
                if row[5] == 0:
                    htmlfile.write("No Feeder Number<br/>")
                if row[6] is None:
                    htmlfile.write("<p style='color:red;'>ERROR : No Pole Use</p><br/>")
                if row[7] is None:
                    htmlfile.write("<p style='color:red;'>ERROR : No Pole Phase</p><br/>")
                if row[8] == 0:
                    htmlfile.write("No Feeder Height<br/>")
                if row[9] is None:
                    htmlfile.write("No Pole Class<br/>")
                if row[10] is None:
                    htmlfile.write("No Pole Structure<br/>")
                if row[11] is None:
                    htmlfile.write("No Pole Fitting<br/>")
                if row[16] is not None or row[16] != 'No Equipment':
                    if row[17] is None:
                        htmlfile.write("<p style='color:red;'>ERROR : No Reference Pole</p><br/>")
                    if row[18] is None:
                        htmlfile.write("<p style='color:red;'>ERROR : No Equipment ID</p><br/>")
                    if row[19] == 0:
                        htmlfile.write("<p style='color:red;'>ERROR : No Equipment Unit</p><br/>")
                    if row[20] is None:
                        htmlfile.write("No Equipment Mount<br/>")
                    if row[21] is None:
                        htmlfile.write("<p style='color:red;'>ERROR : No Equipment Size</p><br/>")
                    if row[22] is None:
                        htmlfile.write("<p style='color:red;'>ERROR : No Equipment Phase</p><br/>")
                    if row[23] is None:
                        htmlfile.write("No Equipment Connection Status<br/>")
                    if row[24] is None:
                        htmlfile.write("No Equipment Use<br/>")
                if row[34] is None:
                    htmlfile.write("No Pole Location<br/>")
                if row[35] is None:
                    htmlfile.write("No Pole Data Source<br/>")
        htmlfile.write("<p><b>Process Completed: " + str(datetime.now()) + "</b></p>")
        htmlfile.write("</body>")
        htmlfile.write("</html>")
        htmlfile.close()

        return htmlfilepath

    def onClose(self):
        self.close()
