# -*- coding: utf-8 -*-
from LIBRARY import *

#import LIBRARY
#LIBRARY.MAIN()

LOG_THIS('NOTICE','============================================================================================')
script_name = 'MAIN'
if not os.path.exists(addoncachefolder): os.makedirs(addoncachefolder)
if not os.path.exists(dbfile):
	LOG_THIS('NOTICE','  .  New Arabic Videos version installed  .  path: [ '+addon_path+' ]')
	XBMCGUI_DIALOG_OK('برنامج عماد للفيديوهات العربية','تم تحديث برنامج عماد للفيديوهات العربية إلى الإصدار الجديد . أو تم مسح الكاش الموجود في البرنامج . سيقوم البرنامج الآن ببعض الفحوصات لضمان عمل البرنامج بصورة صحيحة ومتكاملة')
	import SERVICES
	SERVICES.CHANGELOG()
	CLEAN_KODI_CACHE_FOLDER()
	conn = sqlite3.connect(dbfile)
	conn.close()
	SERVICES.KODI_SKIN()
	#XBMCGUI_DIALOG_NOTIFICATION('رسالة من المبرمج','فحص اضافات adaptive + rtmp')
	#XBMCGUI_DIALOG_NOTIFICATION('رسالة من المبرمج','فحص مخزن عماد')
	#XBMCGUI_DIALOG_OK('',str(iptv))
	ENABLE_MPD(False)
	ENABLE_RTMP(False)
	SERVICES.INSTALL_REPOSITORY(True)
	SERVICES.HTTPS_TEST()
	#iptv = IPTV.isIPTVFiles(False)
	#if iptv: 
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','إذا كنت تستخدم خدمة IPTV الموجودة في هذا البرنامج فسوف يقوم البرنامج الآن أوتوماتيكيا بجلب ملفات IPTV جديدة')
	import IPTV
	IPTV.CREATE_STREAMS(False)
type,name99,url99,mode,image99,page99,text,favourite = EXTRACT_KODI_PATH()
mode0 = int(mode)
mode1 = int(mode0%10)
mode2 = int(mode0/10)
#message += '\n'+'Label:['+menu_label+']   Path:['+menu_path+']'
if mode0==260: message = '  Version: [ '+addon_version+' ]  Kodi: [ '+kodi_release+' ]'
else:
	menu_label2 = menu_label.replace('   ','  ').replace('   ','  ').replace('   ','  ')
	menu_path2 = menu_path.replace('   ','  ').replace('   ','  ').replace('   ','  ')
	message = '  Label: [ '+menu_label2+' ]  Mode: [ '+mode+' ]  Path: [ '+menu_path2+' ]'
if favourite not in ['','1','2','3','4','5']:
	message = message+'   .  Favourite: [ '+favourite+' ]'
LOG_THIS('NOTICE',LOGGING(script_name)+message)
#XBMCGUI_DIALOG_OK('['+menu_path+']','['+mode+']')
#XBMCGUI_DIALOG_OK('['+menu_label+']','['+menu_path+']')
UPDATE_RANDOM_MENUS = mode2==16 and mode0 not in [160,165]
UPDATE_RANDOM_SUBMENUS = mode2==16 and '_REMEMBERRESULTS_' in text
SEARCH_MODES = mode0 in [19,29,39,49,59,69,79,99,119,139,149,209,229,239,249,259,309,319,329]
SITES_MODES = mode2 in [1,2,3,4,5,6,7,9,11,13,14,20,22,24,25,30,31,32]
IPTV_MODES = mode2==23 and text!=''
YOUTUBE_UPDATE = False# mode2==14 and '_REMEMBERRESULTS_' in text
#XBMCGUI_DIALOG_OK(addon_path,str(addon_handle))
if favourite not in ['','1','2','3','4','5']:
	import FAVOURITES
	FAVOURITES.FAVOURITES_DISPATCHER(favourite)
	#"Container.Refresh" used because there is no addon_handle number to use for ending directory
	#"Container.Update" used to open a menu list using specific addon_path
	#xbmc.executebuiltin("Container.Update("+sys.argv[0]+addon_path.split('&favourite=')[0]+")")
	#XBMCGUI_DIALOG_OK(text,mode)
	xbmc.executebuiltin("Container.Refresh")
	EXIT_PROGRAM('MAIN-MAIN-1st',False)
if mode0==266:
	import MENUS
	MENUS.DELETE_LAST_VIDEOS_MENU(text)
	xbmc.executebuiltin("Container.Refresh")
	EXIT_PROGRAM('MAIN-MAIN-2nd',False)
previous_path = xbmc.getInfoLabel('ListItem.FolderPath')
previous_path = unquote(previous_path)
if mode0==262:
	if 'text=' in previous_path:
		search = previous_path.split('text=')[1]
		if '&' in search: search = search.split('&')[0]
		search = search.replace('_REMEMBERRESULTS_','')
	else: search = '_REMEMBERRESULTS_'
	#XBMCGUI_DIALOG_OK(search,'')
	results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,search,favourite)
elif SEARCH_MODES or UPDATE_RANDOM_MENUS:
	#LOG_THIS('NOTICE',path)
	#LOG_THIS('NOTICE',addon_path)
	if '_REMEMBERRESULTS_' in previous_path:
		LOG_THIS('NOTICE','  .  Writing last menu  .  path: [ '+addon_path+' ]')
		results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text,favourite)
		newFILE = str(menuItemsLIST)
		with open(lastrandomfile,'w') as f: f.write(newFILE)
	else:
		LOG_THIS('NOTICE','  .  Reading last menu  .  path: [ '+addon_path+' ]')
		with open(lastrandomfile,'r') as f: oldFILE = f.read()
		menuItemsLIST[:] = eval(oldFILE)
else: results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text,favourite)
#XBMCGUI_DIALOG_OK(addon_path,str(mode0))
if addon_handle>-1:
	if type=='folder' and menu_label!='..' and (SITES_MODES or IPTV_MODES): ADD_TO_LAST_VIDEO_FILES()
	FILTERING_MENUS = mode0 in [114,204,244,254] and text!=''
	DELETE_LAST_VIDEOS = mode0 in [266]
	# kodi defaults
	succeeded,updateListing,cacheToDisc = True,False,True
	if menuItemsLIST:
		KodiMenuList = []
		for menuItem in menuItemsLIST:
			kodiMenuItem = getKodiMenuItem(menuItem)
			KodiMenuList.append(kodiMenuItem)
		addItems_succeeded = xbmcplugin.addDirectoryItems(addon_handle,KodiMenuList)
	if type=='folder' or SEARCH_MODES or UPDATE_RANDOM_SUBMENUS: succeeded = True
	else: succeeded = False
	# updateListing = True => means this list is temporary and will be overwritten by the next list
	# updateListing = False => means this list is permanent and the new list will generate new menu
	if FILTERING_MENUS or DELETE_LAST_VIDEOS or UPDATE_RANDOM_SUBMENUS or YOUTUBE_UPDATE:
		updateListing = True
	else: updateListing = False
	#LOG_THIS('NOTICE',str(succeeded)+'  '+str(updateListing)+'  '+str(cacheToDisc))
	xbmcplugin.endOfDirectory(addon_handle,succeeded,updateListing,cacheToDisc)
	#PLAY_VIDEO_MODES = mode2 in [12,24,33,43,53,63,74,82,92,105,112,123,134,143,182,202,212,223,243,252]
	#XBMCGUI_DIALOG_OK(str(succeeded),str(updateListing),str(cacheToDisc))
	#XBMCGUI_DIALOG_OK(addon_path,str(addon_handle))
#XBMCGUI_DIALOG_OK(str(addon_handle),addon_path)



