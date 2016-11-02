# coding:utf-8

import pymel.all as pm
import json
import os
import maya.cmds as cmds
import cacheCore as cacheCore
reload(cacheCore)


def getYetiInfo():
    nodes = pm.ls(type='pgYetiMaya')
    yetiInfo = {}
    
    for node in nodes:
        sg = node.instObjGroups.outputs()[0]
        surfaceShader = sg.surfaceShader.inputs()[0]
        yetiInfo[node.getParent().name()] = surfaceShader.name()
    
    return yetiInfo

def exportYeti(path):
    yeitInfo = getYetiInfo()
    
    if pm.objExists('yetiInfoNode'):
        yetiInfoNode = pm.PyNode('yetiInfoNode')
        yetiInfoNode.unlock()
        pm.delete(yetiInfoNode)
    
    attrName = 'yetiInfo'
    yetiInfoNode = pm.createNode('network', n='yetiInfoNode')
    yetiInfoNode.addAttr(attrName,  dt='string')
    jsonHandl = json.dumps(yeitInfo)
    yetiInfoNode.attr(attrName).set(jsonHandl)
    yetiInfoNode.attr(attrName).lock()
    yetiInfoNode.lock()
    
    exportList = [yetiInfoNode]
    for _, shader in yeitInfo.items():
        exportList.append(shader)

    pm.select(exportList)
    try:
        pm.exportSelected(path, pr=1, typ='mayaBinary', force=1, es=1)
        print 'Success Export Shader'
    except:
        print exportList
        print path
    finally:
        yetiInfoNode.unlock()
        pm.delete(yetiInfoNode)

def importYeti(path):
    msg = ''
    try:
        yetiInfo = getYetiInfo()
        if yetiInfo:
            for yetiNode, shader in yetiInfo.items():
                if pm.objExists(yetiNode):
                    pm.delete(yetiNode)
                if pm.objExists(shader):
                    pm.delete(shader)
        
        if pm.objExists('yetiInfoNode'):
            yetiInfoNode = pm.PyNode('yetiInfoNode')
            yetiInfoNode.unlock()
            pm.delete(yetiInfoNode)
            
        cmds.file(path, pr=1,  ignoreVersion=1, i=1, type="mayaBinary", mergeNamespacesOnClash=False, options="v=0;")
        #pm.importFile(path)
        if not pm.objExists('yetiInfoNode'):
            msg += u'"yetiInfoNode"가 존재 하지 않습니다.'
    except:
        return msg
    
    
    if not pm.objExists('time1'):
        timeNode = pm.createNode('time', n='time1')
    
    timeNode = pm.PyNode('time1')
    
    yetiInfoNode = pm.PyNode('yetiInfoNode')
    yetiInfo = json.loads(yetiInfoNode.yetiInfo.get())
    
    for yetiNodeName, shaderName in yetiInfo.items():
        try:
            yetiNode = pm.createNode('pgYetiMaya', n=yetiNodeName + 'Shape')
            yetiParent = yetiNode.getParent()
            yetiParent.rename(yetiNodeName)
            yetiNode.renderDensity.set(1)
            yetiNode.aiOpaque.set(0)
            timeNode.outTime.connect(yetiNode.currentTime)
            
            pm.select(yetiParent)
            surfaceShader = pm.PyNode(shaderName)
            pm.hyperShade(assign=surfaceShader)
        except:
            msg += u'{}노드와 {}쉐이더를  어싸인 하는데 실패 했습니다'.format(yetiNodeName, shaderName)
    
    return msg

def importYetiCache(path):     
    data = cacheCore.loadScInfo(path)
    cacheInfos = data['caches']
    for cacheInfo in cacheInfos:
        yetiNodeName = '{}:{}'.format(cacheInfo['namespace'],cacheInfo['nodeName'])
        cachePath    = cacheInfo['cachePath']
        if pm.objExists(yetiNodeName):
            node = pm.PyNode(yetiNodeName)
            node.cacheFileName.set(cachePath)
            node.fileMode.set(1)            
        else:
            print '{}가 존재 하지 않습니다.'.format(yetiNodeName)
    
def loadYetiAsset(path):
    namespace = os.path.basename(path).partition('.')[0] 
    pm.createReference(path, namespace=namespace)
    
def loadAniCache(path):
    namespace = os.path.basename(path).partition('.')[0] 
    cmds.file(path, ignoreVersion=1, type='Alembic', namespace=namespace, r=1, gl=1, mergeNamespacesOnClash=False)
    
def exportYetiCache(infoPath, cacheRoot, option, namespace):

    startFrame = float(option['startFrame'])
    endFrame   = float(option['endFrame'])
    nodes      = pm.ls(type='pgYetiMaya')
    
    yetiCachesData = {'startFrame':startFrame, 'endFrame':endFrame, 'caches':[]}
    for node in nodes:
        cacheName = node.name().partition(':')[2]
        cachePath = '{}/{}.%04d.fur'.format(cacheRoot, cacheName)
        pm.pgYetiCommand(node, range=[startFrame,endFrame], writeCache = cachePath, samples=1)
        cacheData = {}
        cacheData['namespace']   = namespace
        cacheData['nodeName']    = cacheName
        cacheData['cachePath']   = cachePath
        yetiCachesData['caches'].append(cacheData)
    
    saveYetiInofs(infoPath, yetiCachesData)

def saveYetiInofs(path, data):
    cacheCore.saveScInfo(data, path)

    
    
        
