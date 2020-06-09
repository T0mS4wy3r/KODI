# -*- coding: utf-8 -*-
from LIBRARY import *

script_name = 'MAIN'


type,name99,url99,mode,image99,page99,text,favourite = EXTRACT_KODI_PATH()
mode0 = int(mode)
mode1 = int(mode0%10)
mode2 = int(mode0/10)


#xbmcgui.Dialog().ok('['+menu_label+']','['+menu_path+']')


LOG_THIS('NOTICE','============================================================================================')
#message += '\n'+'Label:['+menu_label+']   Path:['+menu_path+']'
if mode0==260: message = '  Version: [ '+addon_version+' ]  Kodi: [ '+kodi_release+' ]'
else:
	menu_label2 = menu_label.replace('   ','  ').replace('   ','  ').replace('   ','  ')
	menu_path2 = menu_path.replace('   ','  ').replace('   ','  ').replace('   ','  ')
	message = '  Label: [ '+menu_label2+' ]  Mode: [ '+mode+' ]  Path: [ '+menu_path2+' ]'
LOG_THIS('NOTICE',LOGGING(script_name)+message)


if favourite!='':
	import FAVOURITES
	FAVOURITES.FAVOURITES_DISPATCHER(favourite)
	# "Container.Refresh" used because there is no addon_handle number to use for ending directory
	xbmc.executebuiltin("Container.Refresh")
	LOG_THIS('NOTICE','  Favourite: [ '+favourite+' ]')
	sys.exit(0)


SITES_MODES = mode2 in [1,2,3,4,5,6,7,9,11,13,14,20,22,24,25]
IPTV_MODES = mode2==23 and text!=''
if type=='folder' and menu_label!='..' and (SITES_MODES or IPTV_MODES): ADD_TO_LAST_VIDEO_FILES()


if not os.path.exists(addoncachefolder): os.makedirs(addoncachefolder)
if not os.path.exists(dbfile):
	CLEAN_KODI_CACHE_FOLDER()
	conn = sqlite3.connect(dbfile)
	conn.close()
	import SERVICES
	SERVICES.KODI_SKIN()
	SERVICES.INSTALL_REPOSITORY(False)
	xbmcgui.Dialog().ok('IPTV','تم مسح الكاش أو تحديث البرنامج . فإذا كنت تستخدم IPTV فقم بجلب ملفات IPTV جديدة أو للتخلص من هذه الرسالة ادخل إلى قائمة IPTV وامسح الملفات القديمة')
	import IPTV
	IPTV.CREATE_STREAMS()


#xbmcgui.Dialog().ok(addon_path,str(addon_handle))


SEARCH_MODES = mode0 in [19,29,39,49,59,69,79,99,119,139,149,209,229,239,249,259]
UPDATE_RANDOM_MENUS = mode2==16 and 'UPDATE' in text


if (SEARCH_MODES and menu_label not in ['..','Main Menu']) or (UPDATE_RANDOM_MENUS and menu_label!='Main Menu'):
	LOG_THIS('NOTICE','  .  Writing random list  .  path: [ '+addon_path+' ]')
	results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text)
	newFILE = str(menuItemsLIST)
	with open(lastrandomfile,'w') as f: f.write(newFILE)
elif (SEARCH_MODES and menu_label in ['..','Main Menu']) or (UPDATE_RANDOM_MENUS and menu_label=='Main Menu'):
	LOG_THIS('NOTICE','  .  Reading random list  .  path: [ '+addon_path+' ]')
	with open(lastrandomfile,'r') as f: oldFILE = f.read()
	menuItemsLIST[:] = eval(oldFILE)
else: results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text)


#xbmcgui.Dialog().ok(addon_path,str(addon_handle))


if addon_handle>-1:

	FILTERING_MENUS = mode0 in [114,204,244,254] and text!=''
	DELETE_LAST_VIDEOS = mode0 in [266,268]

	# kodi defaults
	succeeded,updateListing,cacheToDisc = True,False,True

	if menuItemsLIST:
		#LOG_THIS('NOTICE','start')
		#xbmcgui.Dialog().ok(addon_path,str(addon_handle))
		KodiMenuList = []
		for menuItem in menuItemsLIST:
			kodiMenuItem = getKodiMenuItem(menuItem)
			KodiMenuList.append(kodiMenuItem)
		addItems_succeeded = xbmcplugin.addDirectoryItems(addon_handle,KodiMenuList)

	if type=='folder' or SEARCH_MODES or UPDATE_RANDOM_MENUS: succeeded = True
	else: succeeded = False

	# updateListing = True => means this list is temporary and will be overwritten by the next list
	# updateListing = False => means this list is permanent and the new list will generate new menu
	if FILTERING_MENUS or DELETE_LAST_VIDEOS or UPDATE_RANDOM_MENUS: updateListing = True
	else: updateListing = False

	#if UPDATE_RANDOM_MENUS: xbmc.executebuiltin("Container.Refresh")



	

	#LOG_THIS('NOTICE',str(succeeded)+'  '+str(updateListing)+'  '+str(cacheToDisc))
	xbmcplugin.endOfDirectory(addon_handle,succeeded,updateListing,cacheToDisc)

	#PLAY_VIDEO_MODES = mode2 in [12,24,33,43,53,63,74,82,92,105,112,123,134,143,182,202,212,223,243,252]
	#xbmcgui.Dialog().ok(str(succeeded),str(updateListing),str(cacheToDisc))
	#xbmcgui.Dialog().ok(addon_path,str(addon_handle))

	#xbmc.executebuiltin("Container.Update")
	#xbmc.executebuiltin("Container.Refresh")



