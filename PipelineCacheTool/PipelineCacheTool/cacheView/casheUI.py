# coding:utf-8

from PySide import QtGui, QtCore

from cacheView import exportAniWidget
reload(exportAniWidget)
from cacheView.exportAniWidget import ExportAniWidget

import importWidget
reload(importWidget)
from importWidget import ImportWidget

import createAssetWidget
reload(createAssetWidget)
from createAssetWidget import CreateAssetWidget

from cacheView import exportYetiWidget
reload(exportYetiWidget)
from cacheView.exportYetiWidget import ExportYetiWidget


from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

class AlembicCacheUI(MayaQWidgetDockableMixin, QtGui.QDialog):
    '''
    Maya Dock을 만들어 주는 클래스.
    '''
    def __init__(self, parent=None):
        super(AlembicCacheUI, self).__init__(parent)
        self.setWindowTitle('Pipeline Cache Tool')
        self.setFixedWidth(400)
        
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)
        
        scroll_area = QtGui.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.main_layout.addWidget(scroll_area)
        
        main_widget   = QtGui.QWidget()
        widget_layout = QtGui.QVBoxLayout()
        widget_layout.setContentsMargins(0,0,0,0)
        widget_layout.setAlignment(QtCore.Qt.AlignTop)
        main_widget.setLayout(widget_layout)
        scroll_area.setWidget(main_widget)
        
        # 사용자 위젯을 Maya Dock에 추가 
        interpWidget = AlembicCacheWidget()
        
        widget_layout.addWidget(interpWidget)

                
class AlembicCacheWidget(QtGui.QFrame):
    def __init__(self, parent=None):
        super(AlembicCacheWidget, self).__init__()
        self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        
        # Layout
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setContentsMargins(5,5,5,5)
        mainLayout.setSpacing(5)
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        
        self.tabs = QtGui.QTabWidget()
        mainLayout.addWidget(self.tabs)
        
        self.assetTab      = CreateAssetWidget()
        self.aniExportTab  = ExportAniWidget()
        self.yetiExportTab = ExportYetiWidget()
        self.importTab     = ImportWidget()
        self.tabs.addTab(self.assetTab,      'Asset')
        self.tabs.addTab(self.aniExportTab,  'AniExport')
        self.tabs.addTab(self.yetiExportTab, 'YetiExport')
        self.tabs.addTab(self.importTab,     'Import') 
        
        self.setLayout(mainLayout)


def main(dockable=False):
    global dialog

    try:
        dialog.close()
        dialog.deleteLater()
    except: 
        pass
    
    dialog = AlembicCacheUI()
    
    if dockable:
        dialog.show(dockable=dockable, area='right', floating=False)
    else:
        dialog.show()
