# coding:utf-8

import os
from PySide import QtGui
import cacheControl.cacheCore as abcUtils
reload(abcUtils)
import cacheControl.yetiCore as yetiUtils
reload(yetiUtils)


discription = u'''
주의 사항
1. Rig 파일 이름은 [assetName]_rig 여야 합니다.
2. Rig 파일에 한개의 WorldCtrl 가 존재 해야 합니다.
3. Rig 파일에 한개의 [assetName]ModGrp가 존재 해야 합니다. 
4. [assetName]ModGrp 에는 모델링 랜더링에 필요한 \n   object만 있어야 합니다.
(컨스트레인 노드,빈 그룹,로케이터,로우폴리곤,더미... 삭제)
5. mod 폴더에 어셋에 적용할 쉐이터 파일이 있어야 합니다.
( [assetName]_shader.mb )
6. Non-Manifold Edge가 없어야 합니다.
'''

class CreateAssetWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CreateAssetWidget, self).__init__(parent)
        self.initUI()
        self.connections()
        
        self.hair = False
        
    def initUI(self):
        # Window
        self.setWindowTitle('Create Asset Widget')
    
        # Layout
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setContentsMargins(5,5,5,5)
        mainLayout.setSpacing(10)
        
        self.note = QtGui.QTextEdit()
        self.note.setFontPointSize(10)
        self.note.setTextColor(QtGui.QColor(255,0,0))
        self.note.append(discription)
        self.note.setReadOnly(True)
        self.note.setFixedHeight(240)
        
        self.result = QtGui.QTextEdit()
        self.result.setFontPointSize(10)
        self.result.setReadOnly(True)
        
        assetDirLayout = QtGui.QHBoxLayout()
        assetDirLayout.setContentsMargins(3,0,3,0)
        assetDirLayout.setSpacing(3)
        
        self.assetDir     = QtGui.QLineEdit()
        self.assetDirBttn = QtGui.QPushButton('Asset Dir')
        assetDirLayout.addWidget(self.assetDir)
        assetDirLayout.addWidget(self.assetDirBttn)
        
        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.setContentsMargins(3,0,3,0)
        bttnLayout.setSpacing(3)
        self.resetBttn  = QtGui.QPushButton('Reset')
        self.createBttn = QtGui.QPushButton('Create')
        bttnLayout.addWidget(self.resetBttn)
        bttnLayout.addWidget(self.createBttn)
        
        mainLayout.addWidget(self.note)
        mainLayout.addWidget(self.result)
        mainLayout.addLayout(assetDirLayout)
        mainLayout.addLayout(bttnLayout)
        
        self.setLayout(mainLayout)
        
    def connections(self):
        self.resetBttn.clicked.connect(self.reset)
        self.assetDirBttn.clicked.connect(self.getAssetDir)
        self.createBttn.clicked.connect(self.createAsset)
        
    def reset(self):
        self.result.clear()
    
    def getAssetDir(self):
        workspace = abcUtils.getWorkSpace()
        assetDir = QtGui.QFileDialog.getExistingDirectory (self, dir= workspace)
        assetDir = self.setWindowStylePath(assetDir)
        self.assetDir.setText(assetDir)
    
    def createAsset(self):
        assetDir = self.assetDir.text()
        
        # 어셋 경로가 설정되었는지 검사
        if not assetDir:
            self.warningMessage(u'어셋 경로를 설정해 주세요.')
            return
        
        # 어셋 경로가 존재하는지 검사
        if not os.path.exists(assetDir):
            self.warningMessage(u'경로가 존재 하지 않습니다.')
            return
        
        assetName = os.path.basename(assetDir)
        rigDir  = self.setWindowStylePath(os.path.join(assetDir, 'rig'))
        modDir  = self.setWindowStylePath(os.path.join(assetDir, 'mod'))
        renDir  = self.setWindowStylePath(os.path.join(assetDir, 'ren'))
        hairDir = self.setWindowStylePath(os.path.join(assetDir, 'hair'))
        
        assetShaderName     = modDir  + '/' + assetName + '_shader.mb'
        assetRigName        = rigDir  + '/' + assetName + '_rig.mb'
        assetRenName        = renDir  + '/' + assetName + '_ren.mb'
        assetHairShaderName = hairDir + '/' + assetName + '_hairShader.mb'
        
        # shader 파일이 있는지 검사한다.
        if not os.path.exists(assetShaderName):
            self.warningMessage(u'{} 가 존재 하지 않습니다.'.format(assetShaderName))
            return
        
        # rig 파일이 있는지 검사한다.
        if not os.path.exists(assetRigName):
            self.warningMessage(u'{} 가 존재 하지 않습니다.'.format(assetRigName))
            return
        
        # hair shader 파일이 있는지 검사한다.
        if os.path.exists(assetHairShaderName):
            self.hair = True
        
        # step 1
        # open rig file   
        self.writeStep(u'step1.')
        self.writeStep(u'리깅 파일을 오픈 합니다.')
        if abcUtils.openFile(assetRigName): #rig 파일 오픈 성공
            self.writeResult('Succeed')
        else: #rig 파일 오픈 실패
            self.writeError('Failed')
            return
        
        # step 2
        # WorldCtrl
        self.writeStep(u'step2.')
        self.writeStep(u'WorldCtrl 유무를 검사 합니다.')
        if abcUtils.checkWorldCtrl():
            self.writeResult('Succeed')
        else: #rig 파일 오픈 실패
            self.writeError('Failed')
            return
        
        # step 3
        # assetModGrp
        self.writeStep(u'step3.')
        self.writeStep(u'{} 유무를 검사 합니다.'.format(assetName+'ModGrp'))
        if abcUtils.checkModGrp(assetName+'ModGrp'):
            self.writeResult('Succeed')
        else: 
            self.writeError('Failed')
            return
        
        # step 4
        # assetModGrp
        self.writeStep(u'step4.')
        self.writeStep(u'Non-Manifold Edge 유무를 검사 합니다.')
        status , errorEdge = abcUtils.checkNonManifoldEdge() 
        if status:
            self.writeResult('Succeed')
        else: 
            self.writeError('Failed')
            self.writeError(errorEdge)
            return
        
        # step 5
        # create render asset
        self.writeStep(u'step5.')
        self.writeStep(u'ABC 케쉬를 만듭니다.')
        if not os.path.exists(renDir):
            os.makedirs(renDir)
        if abcUtils.createRenderABC(assetName, assetName+'ModGrp', assetRenName):
            self.writeResult('Succeed')
        else:
            self.writeError('Failed')
            return
        
        # step 6
        # import shader
        self.writeStep(u'step6.')
        self.writeStep(u'쉐이더를 임포트 합니다.')
        if abcUtils.importShader2(assetShaderName):
            self.writeResult('Succeed')
        else:
            self.writeError('Failed')
            return
        
        # step 7
        # checkShaderInof
        self.writeStep(u'step7.')
        self.writeStep(u'쉐이더 정보를 검사 합니다.')
        if abcUtils.checkShaderInof():
            self.writeResult('Succeed')
        else:
            self.writeError('Failed')
            return
        
        # step 8
        # assignShader
        self.writeStep(u'step8.')
        self.writeStep(u'쉐이더를 어싸인 합니다.')
        msg = abcUtils.assignShader2()
        if not msg:
            self.writeResult('Succeed')
        else:
            self.writeError('Failed')
            self.writeError(msg)
        
        # step 9
        self.writeStep(u'step9.')
        self.writeStep(u'눈알 쉐이더 투명 하게 설정 합니다.')
        eyeStatus = abcUtils.setEyeballMtl()
        if eyeStatus:
            self.writeResult('Succeed')
        else:
            self.writeError('Failed')
        
        # step 10
        # import hair
        self.writeStep(u'step10.')
        self.writeStep(u'Yeti노드를 만듭니다.')
        if self.hair:
            msg = yetiUtils.importYeti(assetHairShaderName)
            if not msg:
                self.writeResult('Succeed')
            else:
                self.writeError('Failed')
                self.writeError(msg)
        else:
            self.writeError('Failed')
            self.writeError(u'Hiar 파일이 존재 하지 않습니다. 이 작업은 무시하고 진행 됩니다.')
        
        # step 11
        self.writeStep(u'step11.')
        self.writeStep(u'렌더용 {} 어셋을 만듭니다.'.format(assetRenName))
        if abcUtils.saveFile(assetRenName):
            self.writeResult('Succeed')
        else:
            self.writeError('Failed')
        
    def setWindowStylePath(self, path):
        return path.replace("\\", "/")
    
    def writeStep(self, message):
        color = QtGui.QColor(255,255,255)
        self.result.setTextColor(color)
        self.result.append(message)
    
    def writeResult(self, message):
        color = QtGui.QColor(123,252,0)
        self.result.setTextColor(color)
        self.result.append(message)
        
    def writeError(self, message):
        color = QtGui.QColor(255,0,0)
        self.result.setTextColor(color)
        self.result.append(message)
        
    def warningMessage(self, message):
        warningMessage = QtGui.QMessageBox(self)
        warningMessage.setText(message)
        warningMessage.setIcon(QtGui.QMessageBox.Critical)
        warningMessage.exec_()
        return
        
def main(dockable=False):
    global dialog

    try:
        dialog.close()
        dialog.deleteLater()
    except: 
        pass
    
    dialog = CreateAssetWidget()
    dialog.show()
