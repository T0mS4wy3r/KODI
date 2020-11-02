from LIBRARY import *

MAIN()



"""
#sys.exit()



text = '12345678901234567901234567890'

xbmcgui.Dialog().yesno(text+text,text+text+text+text)

#xbmcgui.Dialog().notification(text,text,time=11111)



pDialog = xbmcgui.DialogProgress()
pDialog.create('header',text+text+text+text)
time.sleep(10)



url = 'https://karbala-tv.net/storagefiles/videofiles/5f4cbdfda3beb.mp4'

play_item = xbmcgui.ListItem()
play_item.setPath(url)
		
#play_item.setProperty('inputstreamaddon', '')
#play_item.setProperty('inputstreamaddon','inputstream.adaptive')
#play_item.setProperty('inputstream.adaptive.manifest_type','mp4')

#play_item.setMimeType('video/mp4')
#play_item.setInfo('Video', {'mediatype': 'video'})
#play_item.setContentLookup(True)


xbmc.Player().play(url,play_item)

#xbmcplugin.setResolvedUrl(addon_handle,True,play_item)


#time.sleep(5)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"videoplayer.errorinaspect","value":"20"}}')
#XBMCGUI_DIALOG_OK('done','')


aaa = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.GetSettings", "params": {"level": "expert"}, "id": "1"}')
bbb = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":"1", "setting.level":{"default":"expert"}}')
xbmc.log(str(aaa), level=xbmc.LOGNOTICE)
xbmcgui.Dialog().textviewer(str(bbb),str(aaa))


#sys.exit(0)

#import TEST

#XBMCGUI_DIALOG_OK(str('__init__'),str(''))
"""

