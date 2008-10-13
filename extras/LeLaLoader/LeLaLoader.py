import xbmc, xbmcgui, urllib, sys, os, time

version='0.2'
scriptName = 'LeLaLoader ' + version

url = 'http://www.ixmediabox.de/Lela/LeLa.rar'
#url = 'http://localhost:82/LeLa.rar'
localpath = 'Q:/skin/'
localfile = 'LeLa.rar'
 
class LeLaLoader(xbmcgui.Dialog):
    def __init__(self):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(scriptName, 'Start LeLa Download?'):
            if not os.path.isdir(localpath):
                os.makedirs(localpath)
            self.download(url, localpath + localfile)
    
    def download(self, source, dest):
        try:
            urllib.urlretrieve(source, dest)
            dialog2 = xbmcgui.Dialog()
            try:
                if dialog2.yesno(scriptName, 'Download OK\nExtraxt Contents to ' + localpath + '?'):
                    xbmc.executebuiltin("XBMC.extract(%s,%s)" % (localpath + localfile, localpath))
                    self.message('Extraction Ok')
            except:
                self.message('Extraction Failed\n' + str(sys.exc_value))
        except:
            self.message('Download Failed\n' + str(sys.exc_value))
    
    def message(self, message):
        dialog = xbmcgui.Dialog()
        dialog.ok(scriptName, message)
    
lelaloader = LeLaLoader()
lelaloader.doModal()
del lelaloader