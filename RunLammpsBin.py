# -*- coding: utf-8 -*-
import re
from PyQt4 import QtGui, QtCore, uic
import subprocess
import sys, string, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

cpu='1';opt=0;cluster=0;showBat=""
try:
    ff=file('Default.ini')
    initext = ff.read()
    ff.close( )
    cpuReg=ur"(?<=cpu\=)\d+"
    optReg=ur"(?<=opt\=)\d+"
    clusterReg=ur"(?<=cluster\=)\d+"
    regList=[cpuReg,optReg,clusterReg]
    iniList=[2,1,0]
    for i in range(len(regList)):
        matchTemp = re.search(regList[i], initext)
        if matchTemp:
            iniList[i]=matchTemp.group()
    cpu=iniList[0];opt=int(iniList[1]);cluster=int(iniList[2])

except IOError, e:
    pass

class MyListWidget(QListWidget):
  def __init__(self, parent):
    super(MyListWidget, self).__init__(parent)
    self.setAcceptDrops(True)
    self.setDragDropMode(QAbstractItemView.InternalMove)
  signalshowBat=QtCore.pyqtSignal()
  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls():
      event.acceptProposedAction()
    else:
      super(MyListWidget, self).dragEnterEvent(event)

  def dragMoveEvent(self, event):
    super(MyListWidget, self).dragMoveEvent(event)

  def dropEvent(self, event):
    try:
        _fromUtf8 = QtCore.QString.fromUtf8
    except AttributeError:
        def _fromUtf8(s):
            return s
    global cpu,opt,cluster
    if event.mimeData().hasUrls():
      countFirst=1  #Allow cluster subprocess to setup in the first loop

      for url in event.mimeData().urls():
        self.addItem(url.path())
        #Work space!!!!!!!!
        #"\w+\.\w+\b"
        Regfilename=ur"[^/]+$"
        match = re.search(Regfilename, url.path())
        if match:
            filename = _fromUtf8(match.group())
        Regfilepath=ur".+(?=\/\w+\.\w+\b)"
        match2 = re.search(Regfilepath, url.path())
        if match2:
            filepath= match2.group()
            filepath=str(filepath[1:])

        Regpurefilename=ur"[^/]+(?=\.in\b)"
        match = re.search(Regpurefilename, url.path())
        if match:
            purefilename = match.group()
        Regdatafilename=ur"\b[a-z0-9A-Z_]+(?=_)"
        if cluster==1:
            if countFirst==1:
                f=file(filepath+"/"+'run.sh','w')
                f.write("#!/bin/sh\n")
            else:
                f=file(filepath+"/"+'run.sh','a')
            global showBat
            showBat="/usr/mpi/intel/openmpi-1.4.3-qlc/bin/mpirun -nolocal -np "+cpu+" -hostfile hostfile /home/xichen1/lmp_openmpi -in "+filename
            if opt==1:
                showBat=showBat+' -sf opt '
            match = re.search(Regdatafilename, purefilename)
            if match:
                datafilename = match.group()
                showBat=showBat+' -var filename '+datafilename+'.lammps05 '+purefilename+'.lammpstrj '+purefilename+'.restart '
            showBat2=showBat+" -log "+purefilename+".log"
            showBat=showBat+" -log "+purefilename+".log > log &"

            self.signalshowBat.emit()
            f.write(showBat2+"\n")
            countFirst=countFirst+1
            f.close()

        else:

            f=file(filepath+"/"+filename+'.bat','w')
            if cpu=='1':
                f.write(_fromUtf8("\"../bin/lmp.exe\" "))
            else:
                f.write(_fromUtf8("\"../bin/mpiexec\" -np "+cpu+" -localonly "+"\"../bin/lmp_mpi.exe\" "))
            if opt==1:
                f.write(_fromUtf8(" -sf opt "))
            f.write(_fromUtf8(" -in "+filename))
            match = re.search(Regdatafilename, purefilename)
            if match:
                datafilename = match.group()
                f.write(_fromUtf8(" -var filename "+datafilename+".lammps05 "+purefilename+".lammpstrj "+purefilename+".restart "))
            f.write(_fromUtf8(" -log "+purefilename+".log"))
            f.write(_fromUtf8('\npause'))
            f.close()
            os.chdir( filepath )
            fullpath=str(filepath+'/'+filename)+'.bat'
            pid = subprocess.Popen(fullpath).pid
            #os.remove(str(filepath+"/"+filename+'.bat'))

      countFirst=1
      event.acceptProposedAction()
    else:
      super(MyListWidget,self).dropEvent(event)



class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
    def setupUi(self, MainWindow):

        try:
            _fromUtf8 = QtCore.QString.fromUtf8
        except AttributeError:
            def _fromUtf8(s):
                return s
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(337,  811)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.listWidget = MyListWidget(self)

        self.listWidget.setGeometry(QtCore.QRect(1, 140, 335, 341))
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(160, 20, 113, 29))
        self.lineEdit.setAcceptDrops(False)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(92, 21, 78, 23))
        self.label.setObjectName(_fromUtf8("label"))
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(100, 60, 114, 27))
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 490, 321, 280))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.checkBox_2 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(100, 100, 114, 27))
        self.checkBox_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)


        self.lineEdit.setText(_fromUtf8(cpu))
        self.checkBox.setChecked(opt)
        self.checkBox_2.setChecked(cluster)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.connect(self.lineEdit,QtCore.SIGNAL(_fromUtf8('textChanged(QString)')),self.updatecpu)
        self.connect(self.checkBox,QtCore.SIGNAL(_fromUtf8('toggled(bool)')),self.updateopt)
        self.connect(self.checkBox_2,QtCore.SIGNAL(_fromUtf8('toggled(bool)')),self.updatecluster)
#        self.connect(self.listWidget,QtCore.pyqtSignal(_fromUtf8('signalshowBat')),self.textBrowser.setText(showBat))
        self.listWidget.signalshowBat.connect(self.updateBat)
    def updatecpu(self):
        global cpu
        cpu=self.lineEdit.text()

    def updateopt(self):
        global opt
        opt=self.checkBox.isChecked()
    def updatecluster(self):
        global cluster
        cluster=self.checkBox_2.isChecked()
    def updateBat(self):
        self.textBrowser.setText(QtCore.QString.fromUtf8(showBat))

    def retranslateUi(self, MainWindow):
        try:
            _encoding = QtGui.QApplication.UnicodeUTF8
            def _translate(context, text, disambig):
                return QtGui.QApplication.translate(context, text, disambig, _encoding)
        except AttributeError:
            def _translate(context, text, disambig):
                return QtGui.QApplication.translate(context, text, disambig)

        self.checkBox_2.setText(_translate("MainWindow", "cluster?", None))
        MainWindow.setWindowTitle(_translate("MainWindow", "RunLammps", None))
        self.label.setText(_translate("MainWindow", "CPUs=", None))
        self.checkBox.setText(_translate("MainWindow", "OPT?", None))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Drag file into the box above and enjoy. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Filename example: </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">O2Water_R20.in</span></p></body></html>", None))




if __name__ == '__main__':

  app = QApplication(sys.argv)
  app.setStyle("plastique")

#  window = MyWindow()
  window =Ui_MainWindow()
  window.show()

  sys.exit(app.exec_())
