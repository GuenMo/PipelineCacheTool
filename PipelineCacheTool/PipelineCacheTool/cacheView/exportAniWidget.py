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

from functools import partial

class ExportOptionWidget(QWidget):
    def __init__(self, parent=None):
        super(ExportOptionWidget, self).__init__(parent)
        self.initUI()
        self.connectSignals()
    
    def initUI(self):
        # Create Widget
        self.main_Layout = QGridLayout()
        self.main_Layout.setContentsMargins(3,0,3,0)
        self.main_Layout.setSpacing(10)
        self.setLayout(self.main_Layout)
    
        self.option_GroupBox = QGroupBox("Option")
        self.option_Layout = QGridLayout()
        self.timeOption_Label = QLabel("Time range:")
        self.startEndFrame_Label = QLabel("Start/End:")
        self.timeUnit_Label = QLabel("Time Unit:")
        self.directory_Label = QLabel("Directory:")
        self.timeOption1_RadioButton = QRadioButton("Time Slider")
        self.timeOption2_RadioButton = QRadioButton("Start/End")
        self.startFrame_LineEdit = QLineEdit("1")
        self.endFrame_LineEdit = QLineEdit("24")
        self.timeUnit_ComboBox = QComboBox()
        self.fromScene_PushButton = QPushButton("Policy")
        self.fromBrowser_PushButton = QPushButton("Browser")
        self.directory_LineEdit = QLineEdit()
          
        # Set Layout
        self.option_Layout.addWidget(self.timeOption_Label, 1, 0)
        self.option_Layout.addWidget(self.timeOption1_RadioButton, 1, 1)
        self.option_Layout.addWidget(self.timeOption2_RadioButton, 1, 2)
        self.option_Layout.addWidget(self.startEndFrame_Label, 2, 0)
        self.option_Layout.addWidget(self.startFrame_LineEdit, 2, 1)
        self.option_Layout.addWidget(self.endFrame_LineEdit, 2, 2)
        self.option_Layout.addWidget(self.timeUnit_Label, 3, 0)
        self.option_Layout.addWidget(self.timeUnit_ComboBox, 3, 2)
        self.option_Layout.addWidget(self.directory_Label, 4, 0)
        self.option_Layout.addWidget(self.fromScene_PushButton, 4, 1)
        self.option_Layout.addWidget(self.fromBrowser_PushButton, 4, 2)
        self.option_Layout.addWidget(self.directory_LineEdit, 5, 0, 1, 3)
        self.option_GroupBox.setLayout(self.option_Layout)
        self.main_Layout.addWidget(self.option_GroupBox, 0, 0)
        
        self.timeOption_BttnGrp = QButtonGroup(self)
        self.timeOption_BttnGrp.addButton(self.timeOption1_RadioButton)
        self.timeOption_BttnGrp.addButton(self.timeOption2_RadioButton)

        # Set Widget
        self.setWindowTitle("ExportOption")
        self.timeOption1_RadioButton.setChecked(True)
        self.startFrame_LineEdit.setEnabled(False)
        self.endFrame_LineEdit.setEnabled(False)
        self.timeUnit_ComboBox.addItem("Film(24 fps)")
        self.timeUnit_ComboBox.addItem("PAL(25 fps)")
        self.timeUnit_ComboBox.addItem("NTSC(30 fps)")
        self.timeUnit_ComboBox.addItem("Game(15 fps)")
        
    def connectSignals(self):
        self.timeOption1_RadioButton.toggled.connect(self.changeTimeOption)
        self.fromScene_PushButton.clicked.connect(self.setDirectoryFromScene)
        self.fromBrowser_PushButton.clicked.connect(self.setDirectoryFromBrowser)
    
    
    # Methods
    def changeTimeOption(self):
        if self.timeOption1_RadioButton.isChecked():
            self.startFrame_LineEdit.setEnabled(False)
            self.endFrame_LineEdit.setEnabled(False)
        else:
            self.startFrame_LineEdit.setEnabled(True)
            self.endFrame_LineEdit.setEnabled(True)
    
    def setDirectoryFromScene(self):
        # 마야 컴멘드로 현재씬 경로를 가져와 케쉬씬으로 봐꿔준다.
        # scDir = cmds.file(
        cacheDir = 'C:/Users/user/GoogleDrive/Maya'
        self.directory_LineEdit.setText(cacheDir)
    
    def setDirectoryFromBrowser(self):
        winStyleDir = str(QFileDialog.getExistingDirectory (self))
        cacheDir = winStyleDir.replace("\\", "/")
        self.directory_LineEdit.setText(str(cacheDir)) 
        
    def getOption(self):
        option={}
        if self.timeOption1_RadioButton.isChecked():
            start, end = abcUtils.getFrameRange()
            option['startFrame'] = str( start )
            option['endFrame']   = str( end )
        else:
            option['startFrame'] = str( self.startFrame_LineEdit.text() )
            option['endFrame']   = str( self.endFrame_LineEdit.text() )
        option['timeUnit'] = str( self.timeUnit_ComboBox.currentText() )
        
        if str(self.directory_LineEdit.text()).find("\\") == -1:
            option['directory'] = str( self.directory_LineEdit.text() )
        else:
            winStyleDir = str(self.directory_LineEdit.text())
            cacheDir = winStyleDir.replace("\\", "/")
            option['directory'] = cacheDir
        
        if self.directory_LineEdit.text():
            directory = QDir(self.directory_LineEdit.text())
            if QDir.exists(directory):
                return option
            else:
                warningMessage = QMessageBox(self)
                warningMessage.setText('Path does not exist. \nPlease check the path.')
                warningMessage.setIcon(QMessageBox.Critical)
                warningMessage.exec_()
        else:
            warningMessage = QMessageBox(self)
            warningMessage.setText('Please set the path.')
            warningMessage.setIcon(QMessageBox.Warning)
            warningMessage.exec_()
        
class ReferenceWisget(QWidget):
    def __init__(self, parent=None):
        super(ReferenceWisget, self).__init__(parent)
        self.initUI()
        self.connectSignals()
        
    def initUI(self):
        # Create Widget
        self.setWindowTitle('Reference List')
        
        self.mainLayout      = QGridLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(3,0,3,0)
        self.mainLayout.setSpacing(10)
        self.setLayout(self.mainLayout)
        
        self.refGroupBox     = QGroupBox('Used Reference')
        self.grpBoxlayout    = QGridLayout()
        self.refListWidget   = QListWidget()
        self.loadButton      = QPushButton('Load/Reload')
        self.selectAllButton = QPushButton('Select All')
        
        # Set Layout
        self.grpBoxlayout.addWidget(self.refListWidget, 0,0,1,2)
        self.grpBoxlayout.addWidget(self.loadButton, 1,0)
        self.grpBoxlayout.addWidget(self.selectAllButton, 1,1)
        
        self.refGroupBox.setLayout(self.grpBoxlayout)
        self.mainLayout.addWidget(self.refGroupBox, 0, 1)
    
    def connectSignals(self):
        self.loadButton.clicked.connect(self.loadRef)
        self.selectAllButton.clicked.connect(self.selectAll)
        
    # Methods
    
    def loadRef(self):        
        self.refListWidget.clear()
        
        self.listItem = []
        cameraNodes = abcUtils.getCameras()
        refereceNodes = abcUtils.getRefereces()
        
        for camera in cameraNodes:
            camItemWidget = QListWidgetItem(self.refListWidget) 
            camItem = ReferenceItemWiget(namespace = camera['namespace'],
                                         rootNode  = camera['rootNode'], 
                                         abcAsset  = camera['abcAsset'],
                                         abcPath   = camera['abcPath'],
                                         label     = camera['label'], 
                                         nodeType  = camera['nodeType'])
            camItemWidget.setSizeHint(camItem.sizeHint())
            
            self.refListWidget.addItem(camItemWidget)
            self.refListWidget.setItemWidget(camItemWidget, camItem)
            self.listItem.append(camItem)
        
        for refNode in refereceNodes:
            itemWidget = QListWidgetItem(self.refListWidget) 
            item = ReferenceItemWiget(namespace = refNode['namespace'], 
                                      rootNode  = refNode['rootNode'], 
                                      abcAsset  = refNode['abcAsset'],
                                      abcPath   = refNode['abcPath'],
                                      label     = refNode['label'], 
                                      nodeType  = refNode['nodeType'])
            itemWidget.setSizeHint(item.sizeHint())
            
            self.refListWidget.addItem(itemWidget)
            self.refListWidget.setItemWidget(itemWidget, item)
            self.listItem.append(item)

    def selectAll(self):
        if self.refListWidget.count() > 0 :
            for item in self.listItem:
                item.checkBox.setChecked(True)
                
    def checkedCount(self):
        count = 0
        if self.refListWidget.count() > 0:
            for item in self.listItem:
                if item.checkBox.isChecked():
                    count += 1
        return count
        
    def getAbcList(self):
        checkedItemList = []
        if self.refListWidget.count() > 0 and self.checkedCount() > 0:
            for item in self.listItem:
                if item.checkBox.isChecked():
                    checkedItemList.append(item.getItemInfo())
        return checkedItemList

class ReferenceItemWiget(QWidget):
    #assetInfo = {'namespace':namespace, 'modGrp':modGrp, 'abcAsset':abcAsset, 'type':'cam'}
    def __init__(self, namespace = '', 
                 rootNode = '', 
                 abcAsset = '',  
                 abcPath = '',
                 nodeType = 'ref', 
                 label='', 
                 parent=None):
        
        super(ReferenceItemWiget, self).__init__(parent)
        self.namespace = namespace
        self.rootNode  = rootNode
        self.abcAsset  = abcAsset
        self.abcPath   = abcPath
        self.nodeType  = nodeType
        self.label     = label
      
        self.initUI()
        self.connectSignals()
        
    def initUI(self):
        # Create Widget
        self.main_Layout = QGridLayout()
        self.checkBox = QCheckBox(self)
        
        # Set Layout
        self.main_Layout.addWidget(self.checkBox, 0, 0)
        self.setLayout(self.main_Layout)
        
        # set Widget
        self.main_Layout.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("RefItem")
        self.checkBox.setText(self.label)
        self.checkBox.setGeometry(3,0,150,20)
        self.setGeometry(100,100,150,20)
        
    def connectSignals(self):
        pass
    
    def getItemInfo(self):
        return {'namespace':self.namespace, 
                'rootNode':self.rootNode, 
                'abcAsset':self.abcAsset, 
                'abcPath':'', 
                'nodeType':self.nodeType}

class ExportAniWidget(QWidget):
    def __init__(self, parent=None):
        super(ExportAniWidget, self).__init__(parent)
        
        # Window
        self.setWindowTitle('Export Widget')
    
        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(5,5,5,5)
        mainLayout.setSpacing(10)
        
        self.exportOptions = ExportOptionWidget()
        self.referenceList = ReferenceWisget()
        
        bttnLayout = QHBoxLayout()
        bttnLayout.setContentsMargins(0,0,0,0)
        bttnLayout.setSpacing(5)
        bttnLayout.setAlignment(Qt.AlignTop)
        scInfoBttn = QPushButton('Create Scene Info')
        #scInfoBttn.setFixedWidth(100)
        exportBttn = QPushButton('Export ABC')
        #exportBttn.setFixedWidth(100)
        printBttn  = QPushButton('Print Command')
        #printBttn.setFixedWidth(100)
        #bttnLayout.addSpacerItem(QSpacerItem(5,5,QSizePolicy.Expanding))
        bttnLayout.addWidget(scInfoBttn)
        bttnLayout.addWidget(exportBttn)
        bttnLayout.addWidget(printBttn)
        bttnLayout.setContentsMargins(3,0,3,0)
        bttnLayout.setSpacing(10)
        
        mainLayout.addWidget(self.exportOptions)
        mainLayout.addWidget(self.referenceList)
        mainLayout.addLayout(bttnLayout)
        
        self.setLayout(mainLayout)
        
        printBttn.clicked.connect(partial(self.exportABC, 'print'))
        scInfoBttn.clicked.connect(partial(self.exportABC, 'scInfo'))
        exportBttn.clicked.connect(partial(self.exportABC, 'abc'))
    
    def exportABC(self, operation):
        options = self.exportOptions.getOption()
        
        if not options:
            return
        exportItemList = self.referenceList.getAbcList()
        exportList = []
        
        if exportItemList:
            for exportItem in exportItemList:
                if exportItem['nodeType'] == 'ref':
                    exportItem['abcPath'] = self.exportOptions.directory_LineEdit.text()+'/'+ exportItem['namespace'] + '.abc'
                elif exportItem['nodeType'] == 'cam':
                    exportItem['abcPath'] = self.exportOptions.directory_LineEdit.text()+'/'+ exportItem['rootNode'] + '.abc' 
                elif exportItem['nodeType'] == 'bg':
                    exportItem['abcPath'] = self.exportOptions.directory_LineEdit.text()+'/'+ exportItem['namespace'] + '.abc'
                exportList.append(exportItem)
            if operation == 'abc':
                abcUtils.exportAbc(options, exportList, operation)
            elif operation == 'scInfo':
                abcUtils.generateScInfo(options, exportList)
            elif operation == 'print':
                abcUtils.exportAbc(options, exportList, operation)
        else:
            warningMessage = QMessageBox(self)
            warningMessage.setText('Items does not selected. \nPlease select one or more item.')
            warningMessage.setIcon(QMessageBox.Critical)
            warningMessage.exec_()        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    exportWidget = ExportAniWidget()
    exportWidget.show()
    sys.exit(app.exec_())
