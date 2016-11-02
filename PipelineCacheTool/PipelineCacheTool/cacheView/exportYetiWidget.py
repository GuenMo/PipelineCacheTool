# coding:utf-8

import sys
from PySide import QtGui, QtCore
import os
import json
import collections

import cacheControl.cacheCore as abcUtils
reload(abcUtils)
import cacheControl.yetiCore as yetiUtils
reload(yetiUtils)



class ExportYetiWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ExportYetiWidget, self).__init__(parent)
        self.initUI()
        self.connectSignals()
    
    def initUI(self):
        # Create Widget
        self.main_Layout = QtGui.QVBoxLayout()
        self.main_Layout.setContentsMargins(3,3,3,3)
        self.main_Layout.setSpacing(5)
        self.setLayout(self.main_Layout)
    
        
        # Ani ScInfo Import 
        scInfoLayout = QtGui.QHBoxLayout()
        scInfoLayout.setSpacing(3)
        scInfoLayout.setContentsMargins(0,0,0,0)
        self.dirScInfoLine = QtGui.QLineEdit()
        self.dirScInfoBttn = QtGui.QPushButton('ScInfo')
        scInfoLayout.addWidget(self.dirScInfoLine)
        scInfoLayout.addWidget(self.dirScInfoBttn)
          
        scInfoImportBox = QtGui.QGroupBox('Ani ScInfo Import')
        scInfoImportBoxLayout = QtGui.QVBoxLayout()
        scInfoImportBoxLayout.setContentsMargins(3,3,3,3)
        scInfoImportBox.setLayout(scInfoImportBoxLayout)
        scInfoImportBoxLayout.addLayout(scInfoLayout)
        
        # Option
        option_GroupBox = QtGui.QGroupBox("Option")
        option_Layout = QtGui.QGridLayout()
        
        self.timeOption_Label = QtGui.QLabel("Time range:")
        self.timeOption1_RadioButton = QtGui.QRadioButton("Time Slider")
        self.timeOption2_RadioButton = QtGui.QRadioButton("Start/End")
        self.timeOption_BttnGrp = QtGui.QButtonGroup(self)
        self.timeOption_BttnGrp.addButton(self.timeOption1_RadioButton)
        self.timeOption_BttnGrp.addButton(self.timeOption2_RadioButton)
        
        self.startEndFrame_Label = QtGui.QLabel("Start/End:")
        self.startFrame_LineEdit = QtGui.QLineEdit("1")
        self.endFrame_LineEdit = QtGui.QLineEdit("24")
        
        self.timeUnit_Label = QtGui.QLabel("Time Unit:")
        self.timeUnit_ComboBox = QtGui.QComboBox()
        
        self.timeOption1_RadioButton.setChecked(True)
        self.startFrame_LineEdit.setEnabled(False)
        self.endFrame_LineEdit.setEnabled(False)
        self.timeUnit_ComboBox.addItem("Film(24 fps)")
        self.timeUnit_ComboBox.addItem("PAL(25 fps)")
        self.timeUnit_ComboBox.addItem("NTSC(30 fps)")
        self.timeUnit_ComboBox.addItem("Game(15 fps)")
        
        option_Layout.addWidget(self.timeOption_Label, 1, 0)
        option_Layout.addWidget(self.timeOption1_RadioButton, 1, 1)
        option_Layout.addWidget(self.timeOption2_RadioButton, 1, 2)
        option_Layout.addWidget(self.startEndFrame_Label, 2, 0)
        option_Layout.addWidget(self.startFrame_LineEdit, 2, 1)
        option_Layout.addWidget(self.endFrame_LineEdit, 2, 2)
        option_Layout.addWidget(self.timeUnit_Label, 3, 0)
        option_Layout.addWidget(self.timeUnit_ComboBox, 3, 2)
        
        option_GroupBox.setLayout(option_Layout)
        
        # Used ABC
        abcGroupBox          = QtGui.QGroupBox('Used ABC')
        grpBoxlayout         = QtGui.QGridLayout()
        self.abcListWidget   = QtGui.QListWidget()
        self.loadButton      = QtGui.QPushButton('Load/Reload')
        self.selectAllButton = QtGui.QPushButton('Select All')
        
        grpBoxlayout.addWidget(self.abcListWidget, 0,0,1,2)
        grpBoxlayout.addWidget(self.loadButton, 1,0)
        grpBoxlayout.addWidget(self.selectAllButton, 1,1)
        abcGroupBox.setLayout(grpBoxlayout)
        
        # Load
        loadGroupBox       = QtGui.QGroupBox('Load')
        loadGroupBoxLayout = QtGui.QHBoxLayout() 
        loadGroupBox.setLayout(loadGroupBoxLayout)
        self.loadYetiBttn = QtGui.QPushButton('Load Yeti Asset')
        self.loadAbcBttn  = QtGui.QPushButton('Load Abc Cache')
        loadGroupBoxLayout.addWidget(self.loadYetiBttn)
        loadGroupBoxLayout.addWidget(self.loadAbcBttn)
        
        # Export
        exportLayout = QtGui.QHBoxLayout()
        exportLayout.setContentsMargins(10,5,10,5)
        self.exportYetiCacheBttn = QtGui.QPushButton('Export Yeti Cache')
        self.exportYetiCacheBttn.setFixedWidth(120)
        exportLayout.addSpacerItem(QtGui.QSpacerItem(5,5,QtGui.QSizePolicy.Expanding))
        exportLayout.addWidget(self.exportYetiCacheBttn)
        
        # Set Layout
        self.main_Layout.addWidget(scInfoImportBox)
        self.main_Layout.addWidget(option_GroupBox)
        self.main_Layout.addWidget(abcGroupBox)
        self.main_Layout.addWidget(loadGroupBox)
        self.main_Layout.addLayout(exportLayout)
        self.main_Layout.addStretch()
        
        # Set Widget
        self.setWindowTitle('Export Yeti')
    
    def connectSignals(self):
        self.dirScInfoBttn.clicked.connect(self.getScInfo)
        self.timeOption1_RadioButton.toggled.connect(self.changeTimeOption)
        self.loadButton.clicked.connect(self.loadAbc)
        self.selectAllButton.clicked.connect(self.selectAllItems)
        self.loadYetiBttn.clicked.connect(self.loadYetiAsset)
        self.loadAbcBttn.clicked.connect(self.loadAbcCache)
        self.exportYetiCacheBttn.clicked.connect(self.exportYetiCache)
    
    '''ani scInfo Import Function'''
    def getScInfo(self):
        fileDir = QtGui.QFileDialog.getOpenFileName(self, caption = 'Open ScInof', filter=('*.json'))[0]
        if fileDir:
            scInfoPath = fileDir.replace("\\", "/")
            self.dirScInfoLine.setText(scInfoPath)
            
            data = self.loadData(scInfoPath)
        
            ScOption = collections.namedtuple('ScOption',['startFrame', 'endFrame', 'timeUnit', 'abcDir'], verbose=False, rename=False)
            scOption = ScOption(startFrame = float(data['startFrame']), 
                                endFrame   = float(data['endFrame']),  
                                timeUnit   = data['timeUnit'], 
                                abcDir     = data['directory'])
            self.setOption(scOption)
    
    def loadData(self, fileName):
        data = {}
        if os.path.exists(fileName):
            fileHandle = open(fileName, 'r')
            data = json.loads(fileHandle.read())
            fileHandle.close()
        return data
    
    ''' Option Function '''
    def changeTimeOption(self):
        if self.timeOption1_RadioButton.isChecked():
            self.startFrame_LineEdit.setEnabled(False)
            self.endFrame_LineEdit.setEnabled(False)
        else:
            self.startFrame_LineEdit.setEnabled(True)
            self.endFrame_LineEdit.setEnabled(True)
            
    def setOption(self, option):
        self.timeOption2_RadioButton.setChecked(True)
        self.startFrame_LineEdit.setText(str(option.startFrame))
        self.endFrame_LineEdit.setText(str(option.endFrame))
        index = self.timeUnit_ComboBox.findText(option.timeUnit)
        self.timeUnit_ComboBox.setCurrentIndex(index)
        
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
        
        if str(self.dirScInfoLine.text()).find("\\") == -1:
            option['directory'] = str( self.dirScInfoLine.text() )
        else:
            winStyleDir = str(self.dirScInfoLine.text())
            cacheDir = winStyleDir.replace("\\", "/")
            option['directory'] = cacheDir
        return option
            
   
    def loadAbc(self):  
        scInfoPath = self.dirScInfoLine.text()
        data = self.loadData(scInfoPath)
        caches = data['cache']
        
        cacheInfos = []
        
        for cache in caches:
            CacheInfo = collections.namedtuple('CacheInfo', ['hairAsset', 'abcPath', 'nodeType', 'namespace'])
            hairAsset = ''
            abcPath   = cache['abcPath']
            nodeType  = cache['nodeType']
            namespace = cache['namespace']
            
            if nodeType == 'ref':
                renAsset = cache['abcAsset']
                hairAsset = renAsset.replace('/ren/', '/hair/')
                hairAsset = hairAsset.replace('_ren.mb', '_hair.mb')
                
            cacheInfo = CacheInfo(hairAsset = hairAsset,
                                  abcPath = abcPath,
                                  nodeType = nodeType,
                                  namespace = namespace)
            cacheInfos.append(cacheInfo)
        
        self.addListItems(cacheInfos)
        
    def addListItems(self, cacheInfos):
        self.abcListWidget.clear()
        self.items = []
        if cacheInfos:
            for caheInfo in cacheInfos:
                itemWidget = QtGui.QListWidgetItem(self.abcListWidget) 
                item = AbcItemWiget(caheInfo)
                self.items.append(item)
                itemWidget.setSizeHint(item.sizeHint())
                self.abcListWidget.addItem(itemWidget)
                self.abcListWidget.setItemWidget(itemWidget, item)
                
    def selectAllItems(self):
        numItems = self.abcListWidget.count()
        if numItems > 0:
            for item in self.items:
                item.checkBox.setChecked(True)
    
    '''Load Function'''
    def loadYetiAsset(self):
        checkedItems = []
        for item in self.items:
            if item.checkBox.isChecked():
                checkedItems.append(item)
        
        if checkedItems:
            for item in checkedItems:
                if item.nodeType == 'ref':
                    yetiUtils.loadYetiAsset(item.hairAsset)
    
    def loadAbcCache(self):
        checkedItems = []
        for item in self.items:
            if item.checkBox.isChecked():
                checkedItems.append(item)
        
        if checkedItems:
            for item in checkedItems:
                yetiUtils.loadAniCache(item.abcPath)
        
    '''Export Yeti Cache'''
    def exportYetiCache(self):
        yetiCacheOption = self.getOption()
        for item in self.items:
            if item.checkBox.isChecked() and item.nodeType == 'ref':
                yetiCacheRoot = os.path.dirname(item.abcPath).replace('alembic', 'hair')
                yetiInfoName  = item.label
                yetiInfoPath  = yetiCacheRoot + '/YetiInfo_' + yetiInfoName + '.json'
                yetiCachePath = yetiCacheRoot + '/' + yetiInfoName
                if not os.path.exists(yetiCacheRoot):
                    os.mkdir(yetiCacheRoot)
                if not os.path.exists(yetiCachePath):
                    os.mkdir(yetiCachePath)
                yetiUtils.exportYetiCache(yetiInfoPath, yetiCachePath, yetiCacheOption, item.namespace)
                    
    def warningMessage(self, msg):
        warningMessage = QtGui.QMessageBox(self)
        warningMessage.setText(msg)
        warningMessage.setIcon(QtGui.QMessageBox.Critical)
        warningMessage.exec_()

class AbcItemWiget(QtGui.QWidget):
    def __init__(self, cacheInfo, parent=None):
        
        super(AbcItemWiget, self).__init__(parent)
        self.namespace = cacheInfo.namespace
        self.hairAsset = cacheInfo.hairAsset
        self.abcPath   = cacheInfo.abcPath
        self.nodeType  = cacheInfo.nodeType
        self.label     = os.path.basename(cacheInfo.abcPath).partition('.')[0]

        self.initUI()
        
    def initUI(self):
        # Create Widget
        self.main_Layout = QtGui.QGridLayout()
        self.checkBox = QtGui.QCheckBox(self)
        
        # Set Layout
        self.main_Layout.addWidget(self.checkBox, 0, 0)
        self.setLayout(self.main_Layout)
        
        # set Widget
        self.main_Layout.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Abc Item')
        self.checkBox.setText(self.label)
        self.checkBox.setGeometry(3,0,150,20)
        self.setGeometry(100,100,150,20)
        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    exportWidget = ExportYetiWidget()
    exportWidget.show()
    sys.exit(app.exec_())
