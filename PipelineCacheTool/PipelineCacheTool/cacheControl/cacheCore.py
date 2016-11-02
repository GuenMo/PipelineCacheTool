# coding:utf-8

import maya.cmds as cmds
import pymel.all as pm
import os
import json


###################################################################
# ASSET FUCNKTION
###################################################################
     
def checkRig():
    status = True
    error  = ''
    
    if not pm.objExists('WorldCtrl'):
        status = False
        error += '"WorldCtrl" does not exist.\n'
        
    topNodes = pm.ls(assemblies=True)

    validNode = []
    for top in topNodes:
        if not top.getShape():
            validNode.append(top)
        
    if len(validNode) > 1:
        status = False
        error += 'Top node is one or more exist.\n'
    
    if not pm.objExists(validNode[0].name()+'ModGrp'):
        status = False
        error += '"{}ModGrp" does not exist.\n'.format(validNode[0].name())
        
    return [status, error]

def createAbcForAsset(shaderPath):
    dirname  = os.path.dirname(shaderPath)
    tempAbc  = dirname +'/tempAbc.abc'
    
    pm.select('*ModGrp')
    rootNode = pm.ls(sl=True)[0]
    
    ctrl = pm.PyNode('WorldCtrl')
    pm.currentTime(1)
    ctrl.t.set(0,0,0)
    pm.setKeyframe(ctrl)
    pm.currentTime(2)
    ctrl.t.set(1,0,0)
    pm.setKeyframe(ctrl)
    
    pm.AbcExport(j="-frameRange 1 2 -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root {} -file {}".format(rootNode.name(), tempAbc))
    pm.newFile(f=True)
    pm.AbcImport(tempAbc, mode='open', fitTimeRange=1)
    
    importShader(shaderPath)
    os.remove(tempAbc)

def assignShader():
    try:
        shaderInfoNode = pm.PyNode('shaderInfoNode')
    except:
        print '"shaderInfoNode" not exist!'
    
    numAttr = shaderInfoNode.shaderInfos.numChildren()
    
    for i in range(numAttr):
        shaderInfos = json.loads(shaderInfoNode.attr('shaderInfos{}'.format(i)).get())
        pm.select(shaderInfos.get('geometry'))
        
        surfaceShader = pm.PyNode(shaderInfos.get('surfaceShader'))
        pm.hyperShade(assign=surfaceShader)
        pm.select(cl=True)    
        
        if shaderInfos.get('displacement'):
            displacement = pm.PyNode(shaderInfos.get('displacement'))
            sg = surfaceShader.outColor.outputs()[0]
            displacement.outColor.connect(sg.displacementShader)

    shaderInfoNode.unlock()
    pm.delete(shaderInfoNode)

def createRenderABC(assetName, modName, path):
    try:
        abcPath  = os.path.dirname(path)
        tempAbc  = abcPath +'/{}_abc.abc'.format(assetName)
        rootNode = pm.PyNode(modName)
        
        ctrl = pm.PyNode('WorldCtrl')
        pm.currentTime(1)
        ctrl.t.set(0,0,0)
        pm.setKeyframe(ctrl)
        pm.currentTime(2)
        ctrl.t.set(1,0,0)
        pm.setKeyframe(ctrl)
        
        pm.AbcExport(j="-frameRange 1 2 -uvWrite -worldSpace -writeVisibility -root {} -file {}".format(rootNode.name(), tempAbc))
        pm.newFile(f=True)
        pm.AbcImport(tempAbc, mode='open', fitTimeRange=1)
        return True
    except:
        return False
    
def assignShader2():
    shaderInfoNode = pm.PyNode('shaderInfoNode')    
    numAttr = shaderInfoNode.shaderInfos.numChildren()
    message = ''
    for i in range(numAttr):
        shaderInfos = json.loads(shaderInfoNode.attr('shaderInfos{}'.format(i)).get())
        try:
            pm.select(shaderInfos.get('geometry'))
            
            surfaceShader = pm.PyNode(shaderInfos.get('surfaceShader'))
            pm.hyperShade(assign=surfaceShader)
            pm.select(cl=True)    
            try:
                if shaderInfos.get('displacement'):
                    displacement = pm.PyNode(shaderInfos.get('displacement'))
                    sg = surfaceShader.outColor.outputs()[0]
                    displacement.displacement.connect(sg.displacementShader)
            except:
                message += ( str(shaderInfos.get('displacement')) + '-->' + sg.name()+ '\n')
        except:
            message += ( str(shaderInfos.get('surfaceShader')) + '-->' + str(shaderInfos.get('geometry') )+ '\n')
            
    shaderInfoNode.unlock()
    pm.delete(shaderInfoNode)
    return message


def checkNonManifoldEdge():
    allShape = pm.ls(type='mesh')

    errorEdges = []
    for shape in allShape:
        nonMainfold = pm.polyInfo(shape, nme=True)
        if nonMainfold:
            for e in nonMainfold:
                errorEdges.append( e )
    if not errorEdges:
        return (True, [])
    else:
        error = '\n'.join(str(e) for e in errorEdges)
        return (False, error)

def checkShaderInof():
    return pm.objExists('shaderInfoNode')

def deleteShader(mod):
    try:
        pm.select(mod)
        lambert = pm.PyNode('lambert1')
        pm.hyperShade(assign=lambert )
        pm.select(cl=True)
        pm.mel.eval('MLdeleteUnused;')
        return True
    except:
        return False

def importShader2(path):
    try:
        #pm.importFile(path)
        cmds.file(path, pr=1,  ignoreVersion=1, i=1, type="mayaBinary", mergeNamespacesOnClash=False, options="v=0;")
        return True
    except:
        return False
    
def checkWorldCtrl():
    return pm.objExists('WorldCtrl')

def checkModGrp(modGrp):
    return pm.objExists(modGrp)

def importShader(path):
    try:
        pm.importFile(path)
        print 'Success import {}'.format(path)
    except:
        print 'Failed import {}'.format(path)
        return
    assignShader()
    
def setEyeballMtl():
    eyeMtls = pm.ls(type='jf_nested_dielectric')
    try:
        if eyeMtls:
            for mtl in eyeMtls:
                sg = mtl.outColor.outputs()[0]
                if sg:
                    for mesh in sg.members():
                        if pm.objExists(mesh):
                            mesh.aiOpaque.set(0)
        return True
    except:
        return False

###################################################################
# EXPORT FUCNKTION
###################################################################

def getFrameRange():
    start = pm.playbackOptions(q=True, minTime=True)
    end   = pm.playbackOptions(q=True, maxTime=True) 
    return [start, end]

def getCameras():
    camShapes   = pm.ls(type='camera')
    defalutCams = [] 
    usedCams    = []
    itemsInfo   = []
    
    for dc in ['persp', 'top', 'front', 'side', 'back', 'left', 'bottom']:
        if pm.objExists(dc):
            defalutCams.append(pm.PyNode(dc))
    
    for shape in camShapes:
        usedCams.append(shape.getParent())
    validCams = list( set(usedCams) - set(defalutCams) )
    
    for node in validCams:
        itemsInfo.append({'namespace':'', 'rootNode':node.name(), 'abcAsset':'', 'abcPath':'','label':node.name(), 'nodeType':'cam'})
    
    return itemsInfo

def getRefereces():
    rnNodes = pm.ls(type='reference')
    itemsInfo = []
    for node in rnNodes:
        try:
            namespace = node.associatedNamespace(baseName =True)
            rigAsset  = node.fileName(resolvedName=False, includePath=False, includeCopyNumber=False)
            assetDir  = os.path.dirname(rigAsset).replace('rig', 'ren')
            abcAsset  = node.fileName(resolvedName=False, includePath=True, includeCopyNumber=False).replace('_rig.mb', '_ren.mb')
            abcAsset  = assetDir+'/'+abcAsset
            
            nodeType = 'ref'
            if isBackground(rigAsset):
                nodeType = 'bg'
                abcAsset = rigAsset
            abcAsset = abcAsset.replace('//', '/')
            
            nodes = node.nodes()
            rootNode = ''
            for node in nodes:
                if node.name().endswith('ModGrp'):
                    rootNode = node.name()
            
            itemsInfo.append({'namespace':namespace, 'rootNode':rootNode, 'abcAsset':abcAsset, 'abcPath':'', 'label':namespace, 'nodeType':nodeType})
        except:
            print 'Error {}'.format(node.name())
    return itemsInfo

def isBackground(path):
    status = True
    if 'assets/ch' in path:
        status = False
    if 'assets/prop' in path:
        status = False
    return status
    
def exportAbc(options, exportList, operation):
    exportAbcCommand = 'AbcExport '
    startFrame = options['startFrame']
    endFrame   = options['endFrame']
    
    for cache in exportList:
        print cache
        if cache['nodeType'] != 'bg':
            cacheFile = cache['abcPath'] 
            rootNode  = cache['rootNode']
            exportAbcCommand += abcCommandSegment(startFrame, endFrame, rootNode, cacheFile) + " "
    exportAbcCommand += ';'
    
    if operation == 'print':
        print exportAbcCommand
        return
    try:
        pm.mel.eval(exportAbcCommand)
    except:
        pm.error('AbcExport Error!!')
    
def abcCommandSegment(startFrame, endFrame, rootNode, cacheFile):
    abcCommand = '-j "-frameRange %s %s -uvWrite -worldSpace -writeVisibility -root %s -file %s"' %(startFrame, endFrame, rootNode, cacheFile)
    return abcCommand


def generateScInfo(options, exportList):
    scInfoPath    = options['directory'] + '/' +'ScInfo.json'
    scInfoOptions = options.copy()
    scInfoOptions['cache'] = exportList
    saveScInfo(scInfoOptions, scInfoPath)
    
def saveScInfo(dic, fileName):
    fileName = open(fileName, 'w')
    json.dump(dic, fileName, indent=4)
    fileName.close() 
 
def setFrameRange(start, end, timeUnit):
    pm.playbackOptions(minTime=start)
    pm.playbackOptions(maxTime=end)
    
    time = 'film'
    if timeUnit == 'PAL(25 fps)':
        time = 'pal'
    elif timeUnit == 'NTSC(30 fps)':
        time = 'ntsc'
    elif timeUnit == 'Game(15 fps)':
        time = 'game'
    pm.currentUnit(time = time)


    
###################################################################
# IMPORT FUCNKTION
###################################################################
def importAbc(operation, scInfoFile):
    
    scInfo = loadScInfo(scInfoFile)
    
    startFrame = scInfo['startFrame']
    endFrame   = scInfo['endFrame']
    timeUnit   = scInfo['timeUnit']
    
    pm.newFile(f=True)
    setFrameRange(startFrame, endFrame, timeUnit)
    
    cacheInfos = scInfo['cache']
    camList = []
    assetList = []
    bgList  = []
    
    for cache in cacheInfos:
        if cache['nodeType'] == 'cam':
            camList.append(cache)
        elif cache['nodeType'] == 'ref':
            assetList.append(cache)
        elif cache['nodeType'] == 'bg':
            bgList.append(cache)
    
    print camList
    print assetList
    
    importCamera(camList)
    importAsset(assetList)
    importBg(bgList)

def loadScInfo(fileName):
    if os.path.exists(fileName) and fileName.endswith('.json'):
        f = open(fileName, 'r')
        js = json.loads(f.read())
        f.close()
        return js

def importCamera(camInfos):
    if not camInfos:
        return
    for camInfo in camInfos:
        camAbc = camInfo['abcPath']
        pm.AbcImport(camAbc, mode='import', fitTimeRange=1)
    
def importAsset(assetInfos):
    if not assetInfos:
        return
    for assetInfo in assetInfos:
        asset     = assetInfo['abcAsset']
        namespace = assetInfo['namespace']
        abcPath   = assetInfo['abcPath']
        rootNode  = assetInfo['rootNode']
        #pm.createReference(asset, namespace=namespace)
        cmds.file(asset, ignoreVersion=1, type="mayaBinary", namespace=namespace, r=1, gl=1, mergeNamespacesOnClash=False, options="v=0;")
        pm.AbcImport(abcPath, debug=1, connect=rootNode, mode='import', fitTimeRange=1)

def importBg(bgInfos):
    if not bgInfos:
        return
    for bgInfo in bgInfos:
        asset     = bgInfo['abcAsset']
        namespace = bgInfo['namespace']
        #pm.createReference(asset, namespace=namespace)
        cmds.file(asset, ignoreVersion=1, type="mayaBinary", namespace=namespace, r=1, gl=1, mergeNamespacesOnClash=False, options="v=0;")
    
###################################################################
# COMMON FUCNKTION
###################################################################    
    
def openFile(filePath):
    try:
        #pm.openFile(filePath,f=True)
        cmds.file(filePath, ignoreVersion=1, typ="mayaBinary", options="v=0;", o=1, f=1)
        return filePath
    except:
        return False
    
def saveFile(path):
    try:
        pm.saveAs(path, f=True)
        return True
    except:
        return False
    
def getWorkSpace():
    return pm.workspace( q=True, dir=True )

def loadPlugin():
    loadedPlugins = pm.pluginInfo( query=True, listPlugins=True )
    validPlugins = ['AbcImport', 'AbcExport', 'mtoa']
    for plugin in validPlugins:
        if not plugin in loadedPlugins:
            pm.loadPlugin(plugin+'.mll')
    
    
    