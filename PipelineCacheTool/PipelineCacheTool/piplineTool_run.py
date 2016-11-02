# coding:utf-8

import sys

def piplineTool_run():
    try:
        filePath = __file__
        appPath = filePath.rpartition('\\')[0]
    except:
        print 'Environ Value {} not exist.'.format(appPath)
    
    else:
        path = appPath
        
        if not path in sys.path:
            sys.path.append(path)
        
        import cacheView.casheUI as cacheToolUI
        reload(cacheToolUI)
        cacheToolUI.main(True)
        
if __name__ == 'piplineTool_run':  
    piplineTool_run()



