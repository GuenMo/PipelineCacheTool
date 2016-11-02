# coding:utf-8

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

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

class AlembicCacheUI(MayaQWidgetDockableMixin, QDialog):
    '''
    Maya Dock을 만들어 주는 클래스.
    '''
    def __init__(self, parent=None):
        super(AlembicCacheUI, self).__init__(parent)
        self.setWindowTitle('Pipeline Cache Tool')
        self.setFixedWidth(400)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_layout.addWidget(scroll_area)
        
        main_widget   = QWidget()
        widget_layout = QVBoxLayout()
        widget_layout.setContentsMargins(0,0,0,0)
        widget_layout.setAlignment(Qt.AlignTop)
        main_widget.setLayout(widget_layout)
        scroll_area.setWidget(main_widget)
        
        # 사용자 위젯을 Maya Dock에 추가 
        interpWidget = AlembicCacheWidget()
        
        widget_layout.addWidget(interpWidget)

                
class AlembicCacheWidget(QFrame):
    def __init__(self, parent=None):
        super(AlembicCacheWidget, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        
        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(5,5,5,5)
        mainLayout.setSpacing(5)
        mainLayout.setAlignment(Qt.AlignTop)
        
        self.tabs = QTabWidget()
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
