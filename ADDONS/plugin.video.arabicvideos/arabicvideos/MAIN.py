# -*- coding: utf-8 -*-
from LIBRARY import *


script_name = 'MAIN'


type,name99,url99,mode,image99,page99,text = EXTRACT_KODI_PATH()
mode2 = int(mode)
mode3 = int(mode2/10)


#xbmcgui.Dialog().ok('test 111',str(addon_handle))
LOG_THIS('NOTICE','============================================================================================')
if 'mode' not in addon_path:
	message = 'Version: [ '+addon_version+' ]   Kodi: [ '+kodi_release+' ]'
	#message += '\n'+'Label:['+menu_label+']   Path:['+menu_path+']'
	LOG_THIS('NOTICE',LOGGING(script_name)+'   '+message)
else: LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)


if not os.path.exists(addoncachefolder): os.makedirs(addoncachefolder)
if os.path.exists(dbfile): newdb = False
else:
	newdb = True
	CLEAN_KODI_CACHE_FOLDER()
	conn = sqlite3.connect(dbfile)
	conn.close()
	import SERVICES
	SERVICES.KODI_SKIN()
	SERVICES.INSTALL_REPOSITORY(False)
	xbmcgui.Dialog().ok('IPTV','تم مسح الكاش أو تم تحديث البرنامج .. فإذا كنت تستخدم خدمة IPTV .. فيجب أن تجلب ملفات IPTV جديدة .. للتخلص من هذه الرسالة تستطيع الدخول إلى قائمة IPTV ومسح الملفات القديمة')
	import IPTV
	IPTV.CREATE_STREAMS()


#if menu_label!='Main Menu' or (menu_label=='Main Menu' and mode2==260):


if mode3==16 and menu_label!='Main Menu':
	results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text)
	newFILE = str(menuItemsLIST)
	with open(lastrandomfile,'w') as f: f.write(newFILE)
	#LOG_THIS('NOTICE','Write last random file   mode: [ '+mode+' ]   path: [ '+addon_path+' ]')
	#xbmcgui.Dialog().ok('write random list','')
elif mode3==16 and menu_label=='Main Menu':
	with open(lastrandomfile,'r') as f: oldFILE = f.read()
	menuItemsLIST = eval(oldFILE)
	#LOG_THIS('NOTICE','Read last random file   mode: [ '+mode+' ]   path: [ '+addon_path+' ]')
	#xbmcgui.Dialog().ok('read random list','')
else: results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text)


#xbmcgui.Dialog().ok(addon_path,str(addon_handle))


if addon_handle>-1:

	UPDATE_RANDOM_MENUS = mode2 in [165] and 'DELETE' in text
	FILTERING_MENUS = mode2 in [114,204,244,254] and text!=''
	DELETE_LAST_VIDEOS = mode2 in [266,268]
	SEARCH_MODES = mode2 in [19,29,39,49,59,69,79,99,119,139,149,209,229,249,259]

	# kodi defaults
	succeeded,updateListing,cacheToDisc = True,False,True

	if menuItemsLIST:
		#xbmcgui.Dialog().ok(addon_path,str(addon_handle))
		KodiMenuList = []
		for type99,name99,url99,mode99,image99,page99,text99 in menuItemsLIST:
			kodiMenuItem = getKodiMenuItem(type99,name99,url99,mode99,image99,page99,text99)
			KodiMenuList.append(kodiMenuItem)
		xbmcplugin.addDirectoryItems(addon_handle,KodiMenuList,len(KodiMenuList))

	if type=='folder' or SEARCH_MODES or UPDATE_RANDOM_MENUS: succeeded = True
	else: succeeded = False

	if FILTERING_MENUS or DELETE_LAST_VIDEOS or UPDATE_RANDOM_MENUS: updateListing = True
	else: updateListing = False

	xbmcplugin.endOfDirectory(addon_handle,succeeded,updateListing,cacheToDisc)

	#PLAY_VIDEO_MODES = mode2 in [12,24,33,43,53,63,74,82,92,105,112,123,134,143,182,202,212,223,243,252]
	#xbmcgui.Dialog().ok(str(succeeded),str(updateListing),str(cacheToDisc))
	#xbmcgui.Dialog().ok(addon_path,str(addon_handle))


	#DELETE_LAST_VIDEOS = mode2 in [266,268]
	#if DELETE_LAST_VIDEOS: succeeded = True ; updateListing = True






