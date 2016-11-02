# coding:utf-8

import sys
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    
import cacheControl.cacheCore as abcUtils
reload(abcUtils)
import cacheControl.yetiCore as yetiUtils
reload(yetiUtils)

class ImportWidget(QWidget):
    def __init__(self, parent=None):
        super(ImportWidget, self).__init__(parent)
        self.initUI()
        self.connectSignals()
    
    def initUI(self):
        # Create Widget
        self.main_Layout = QVBoxLayout()
        self.main_Layout.setContentsMargins(3,3,3,3)
        self.main_Layout.setSpacing(5)
        self.setLayout(self.main_Layout)
    
        ##############################################################
        operationLayout      = QHBoxLayout()
        self.operationLabel  = QLabel('Operation:')
        self.newRadioBttn    = QRadioButton('New')
        self.newRadioBttn.setChecked(True)
        self.updateRadioBttn = QRadioButton('Update')
        self.bttnGroup       = QButtonGroup()
        self.bttnGroup.addButton(self.newRadioBttn)
        self.bttnGroup.addButton(self.updateRadioBttn)
        operationLayout.addWidget(self.operationLabel)
        operationLayout.addWidget(self.newRadioBttn)
        operationLayout.addWidget(self.updateRadioBttn)
        
        scInofLayout       = QHBoxLayout()
        self.dirScInfoLine = QLineEdit()
        self.dirScInfoBttn = QPushButton('ScInfo')
        scInofLayout.addWidget(self.dirScInfoLine)
        scInofLayout.addWidget(self.dirScInfoBttn)
        
        sceneLayout     = QHBoxLayout()
        self.dirMscLine = QLineEdit()
        self.dirMscBttn = QPushButton('Scene')
        self.dirMscLine.setEnabled(False)
        self.dirMscBttn.setEnabled(False)
        sceneLayout.addWidget(self.dirMscLine)
        sceneLayout.addWidget(self.dirMscBttn)
        
        bttnLayout = QHBoxLayout()
        self.excuteBttn = QPushButton('New')
        self.excuteBttn.setFixedWidth(100)
        bttnLayout.addWidget(self.excuteBttn)
        bttnLayout.addSpacerItem(QSpacerItem(5,5,QSizePolicy.Expanding))
        bttnLayout.setContentsMargins(0,0,0,0)
        bttnLayout.setSpacing(5)
        bttnLayout.setAlignment(Qt.AlignTop)
          
        aniImportBox = QGroupBox('Ani Import')
        aniImportBoxLayout = QVBoxLayout()
        aniImportBox.setLayout(aniImportBoxLayout)
        aniImportBoxLayout.addLayout(operationLayout)
        aniImportBoxLayout.addLayout(scInofLayout)
        aniImportBoxLayout.addLayout(sceneLayout)
        aniImportBoxLayout.addLayout(bttnLayout)
        
        
        ###############################################################
        yetiImportBox = QGroupBox('Yeti Import')
        yetiImportBoxLayout = QHBoxLayout()
        self.dirYetiInfoBttn = QPushButton('YetiInfo')
        yetiImportBoxLayout.addWidget(self.dirYetiInfoBttn)
        yetiImportBox.setLayout(yetiImportBoxLayout)

        
        # Set Layout
        self.main_Layout.addWidget(aniImportBox)
        self.main_Layout.addWidget(yetiImportBox)
        self.main_Layout.addStretch()
        
        # Set Widget
        self.setWindowTitle('Import')
    
    def connectSignals(self):
        self.bttnGroup.buttonClicked.connect(self.changeOperation)
        self.dirScInfoBttn.clicked.connect(self.findScinfo)
        self.dirMscBttn.clicked.connect(self.findMayaScene)
        self.excuteBttn.clicked.connect(self.excute)
        self.dirYetiInfoBttn.clicked.connect(self.findYetiInfo)
    
    def findScinfo(self):
        fileDir = QFileDialog.getOpenFileName(self, caption = 'Open ScInof', filter=('*.json'))[0]
        scInfoFile = fileDir.replace("\\", "/")
        self.dirScInfoLine.setText(scInfoFile)
        
    def findMayaScene(self):
        fileDir = QFileDialog.getOpenFileName(self, caption = 'Open ScInof', filter=('*.mb'))[0]
        mayaFile = fileDir.replace("\\", "/")
        self.dirMscLine.setText(mayaFile)
        
    def changeOperation(self, button):
        operation = button.text()
        if operation == 'New':
            self.dirMscLine.setEnabled(False)
            self.dirMscBttn.setEnabled(False)
            self.excuteBttn.setText(operation)
        elif operation == 'Update':
            self.dirMscLine.setEnabled(True)
            self.dirMscBttn.setEnabled(True)
            self.excuteBttn.setText(operation)
    
    def warningMessage(self, msg):
        warningMessage = QMessageBox(self)
        warningMessage.setText(msg)
        warningMessage.setIcon(QMessageBox.Critical)
        warningMessage.exec_()
    
    def excute(self):
        operation = self.excuteBttn.text()
        if operation == 'New':
            if self.dirScInfoLine.text():
                scInfoFile = self.dirScInfoLine.text()
                abcUtils.importAbc(operation, scInfoFile)
            else:
                self.warningMessage('Please set the "ScInfo.json" path.')
        elif operation == 'Update':
            if self.dirScInfoLine.text() and self.dirMscLine.text():
                scInfoFile = self.dirScInfoLine.text()
                mayaScFile = self.dirMscLine.text()
                
                openStatus = abcUtils.openFile(mayaScFile)
                if openStatus:
                    print scInfoFile
            else:
                self.warningMessage('Please set the "ScInfo.json" path and "Maya Scene File" path.')
    # Yeti
    def findYetiInfo(self):
        fileDirs = QFileDialog.getOpenFileNames(self, caption = 'Open ScInof', filter=('*.json'))[0]
        yetiInfoFiles = []
        for fileDir in fileDirs:
            yetiInfoFile = fileDir.replace("\\", "/")
            yetiInfoFiles.append(yetiInfoFile)
            yetiUtils.importYetiCache(yetiInfoFile)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    exportWidget = ImportWidget()
    exportWidget.show()
    sys.exit(app.exec_())
