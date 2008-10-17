import xbmc, xbmcgui, urllib, sys, os, time, re, tempfile, shutil

# LeLaLoader
# Downloaderscript for the XBMC LeLa Skin by DjToll
# 10/2008 by Thomas Nesges (http://www.thomasnesges.de)

version='0.4'
scriptName = 'LeLaLoader ' + version

url_lela        = 'http://www.ixmediabox.de/Lela/LeLa.rar'
url_lelalo      = 'http://www.thomasnesges.de/xbmc/py/lelalo.php'
#url_lela        = 'http://localhost:82/LeLa.rar'    # for local tests
#url_lelalo      = 'http://localhost:82/lelalo.php'  # for local tests
scriptdir       = os.getcwd()
skindir         = re.sub('[/\\\\]scripts[/\\\\].*', '/skin/', scriptdir)  # don't like this - any ideas how to spot the skindir?

noScriptUpdate      = False;
noScriptBackup      = False;
keepSkinArchives    = False;
 
textResource = {
    'German': {
        'START':                'LeLa Download starten?\nDas kann einige Minuten dauern\nDu wirst benachrichtigt sobald ich fertig bin',
        'DOWNLOAD_OK':          'Download OK\nArchiv ins Skin-Verzeichnis entpacken?\nDas kann einige Minuten dauern\nDu wirst benachrichtigt sobald ich fertig bin',
        'DOWNLOAD_FAIL':        'Download fehlgeschlagen',
        'EXTRAXT_OK':           'Entpacken erfolgreich\nDu benutzt den Skin Lela derzeit nicht\nDu kannst ihn jetzt in den Einstellungen auswählen',
        'REFRESH_SKIN':         'Entpacken erfolgreich\nDu benutzt den Skin Lela bereits\nMöchtest du die neue Version laden?',
        'EXTRACT_FAIL':         'Entpacken fehlgeschlagen',
        'DELETE_ARCHIVE':       'Archiv löschen?\nGespeichert in ',
        'ERROR':                'Oops!',
        'NOCONNECTION':         'Ist evtl. die Verbindung zum Internet gestört?',
        'NEW_VERSION_ONLINE':   'Es gibt eine neue Version des LeLaLoaders\nUpdaten auf Version ',
        'DOWNLOAD_LELALO_OK':   'Download OK\nDu musst LeLeLoader jetzt neu starten',
        'SKINDIR_NOT_FOUND' :   'Skinverzeichnis nicht gefunden\nVermutet unter: ',
        'BACKUP_FAIL':          'Backup fehlgeschlagen',
    },
    'English': {
        'START':                'Start LeLa Download?\nThis could take a few minutes\nYou will be notified when I\'m done',
        'DOWNLOAD_OK':          'Download OK\nExtraxt Contents to Skin-Directory?\nThis could take a few minutes\nYou will be notified when I\'m done',
        'DOWNLOAD_FAIL':        'Download failed',
        'EXTRAXT_OK':           'Extraction Ok\nYou\'re aren\'t using LeLa at the moment\nYou may choose it in the Settings now',
        'REFRESH_SKIN':         'Extraction Ok\nYou are using skin Lela already\nDo you want to load the new version?',
        'EXTRACT_FAIL':         'Extraction failed',
        'DELETE_ARCHIVE':       'Delete archivefile?\nSaved in ',
        'ERROR':                'Oops!',
        'NOCONNECTION':         'Maybe your Internet connection is broken',
        'NEW_VERSION_ONLINE':   'There is a newer version of LeLaLoader available\nUpdate to version ',
        'DOWNLOAD_LELALO_OK':   'Download OK\nYou have to restart LeLeLoader now',
        'SKINDIR_NOT_FOUND' :   'Skindirectory not found\nGuessed at: ',
        'BACKUP_FAIL':          'Backup failed',
    }
}
language = xbmc.getLanguage()

def text(key):
    if key in textResource[language]:
        return textResource[language][key]
    else:
        if key in textResource['English']:
            return textResource['English'][key]
        else:
            return '@!%#.&!!'

class LeLaLoader(xbmcgui.Dialog):
    def __init__(self):
        urllib.urlcleanup()
        if noScriptUpdate:
            self.downloadLeLa()
        else:
            if not self.checkOnlineVersion():
                self.downloadLeLa()
    
    def downloadLeLa(self):
        if dialog.yesno(scriptName, text('START') ):
            tmp = tempfile.NamedTemporaryFile() # can't be reopened to write (on windows)
            tmprar = tmp.name + '-lela.rar'     # can "
            try:
                refresh = 0
                urllib.urlretrieve(url_lela, tmprar)
                try:
                    if dialog.yesno(scriptName, text('DOWNLOAD_OK')):
                        xbmc.executebuiltin("XBMC.extract(%s,%s)" % (tmprar, skindir))
                        if xbmc.getSkinDir() == 'LeLa':
                            refresh = dialog.yesno(scriptName, text('REFRESH_SKIN'))
                        else:
                            dialog.ok(scriptName, text('EXTRAXT_OK'))
                except:
                    dialog.ok(scriptName, text('EXTRACT_FAIL') + '\n' + str(sys.exc_value))
                if keepSkinArchives:
                    if dialog.yesno(scriptName, text('DELETE_ARCHIVE') + tmprar):
                        os.unlink(tmprar)
                else:
                    os.unlink(tmprar)
                if refresh:
                    xbmc.executebuiltin('XBMC.ReloadSkin()')
            except:
                os.unlink(tmprar)
                dialog.ok(scriptName, text('DOWNLOAD_FAIL') + '\n' + str(sys.exc_value))
            tmp.close

    def checkOnlineVersion(self):
        sock = urllib.urlopen(url_lelalo + '?op=version')
        onlineVersion = sock.read()
        sock.close()
        
        o_major, o_minor = onlineVersion.split('.')
        l_major, l_minor = version.split('.')
        
        if (o_major > l_major) or ((o_major == l_major) and (o_minor > l_minor)):
            if dialog.yesno(scriptName, text('NEW_VERSION_ONLINE') + onlineVersion + '?'):
                tmp = tempfile.NamedTemporaryFile() # can't be reopened to write (on windows)
                tmpzip = tmp.name + '-lelalo.zip'
                urllib.urlretrieve(url_lelalo + '?op=download', tmpzip)
                try:
                    if not noScriptBackup:
                        for oldfile in ['LeLaLoader.png', 'LeLaLoader.tbn', 'LeLaLoader.py']:
                            if os.path.isfile(scriptdir + '/' +  oldfile):
                                if not os.path.isdir(scriptdir + '/Backup/pre0.3'):
                                    os.makedirs(scriptdir + '/Backup/pre0.3')
                                shutil.move(scriptdir + '/' +  oldfile, scriptdir + '/Backup/pre0.3')

                        if not os.path.isdir(scriptdir + '/Backup/' + version):
                            os.makedirs(scriptdir + '/Backup/' + version)
                        dirList = os.listdir(scriptdir)
                        for file in dirList:
                            if file != 'Backup':
                                shutil.copy(scriptdir + '/' + file, scriptdir + '/Backup/' + version + '/')  
                except:
                    dialog.ok(scriptName, text('BACKUP_FAIL'))
                    raise
                xbmc.executebuiltin("XBMC.extract(%s,%s)" % (tmpzip, scriptdir))
                dialog.ok(scriptName, text('DOWNLOAD_LELALO_OK'))
                os.unlink(tmpzip)
                return 1
        return 0

dialog = xbmcgui.Dialog()
try:
    if not os.path.isdir(skindir):
        dialog.ok(scriptName, text('SKINDIR_NOT_FOUND') + skindir)
    else:
        lelaloader = LeLaLoader()
        del lelaloader
except:
    type, value, traceback = sys.exc_info()
    dialog.ok(scriptName, text('ERROR') + '\n' + str(value) + '\nLine: ' + str(traceback.tb_lineno))