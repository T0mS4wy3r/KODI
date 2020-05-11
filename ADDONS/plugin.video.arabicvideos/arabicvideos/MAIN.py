# -*- coding: utf-8 -*-
from LIBRARY import *


script_name = 'MAIN'


#xbmcgui.Dialog().ok('test 111',str(addon_handle))


name,url,mode,image,page,text = EXTRACT_KODI_PATH(addon_path)


LOG_THIS('NOTICE','============================================================================================')
if 'mode' not in addon_path:
	message = 'Version: [ '+addon_version+' ]   Kodi: [ '+kodi_release+' ]'
	#message += '\n'+'Label:['+menu_label+']   Path:['+menu_path+']'
	LOG_THIS('NOTICE',LOGGING(script_name)+'   '+message)
else: LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)

#response = openURL_requests('GET','http://example.com||MyDNSUrl=')
#html = response.text
#xbmcgui.Dialog().ok('',str(html))
#html = openURL('http://example.com||MyProxyUrl=http://198.50.147.158:3128')
#xbmcgui.Dialog().ok('',str(html))
#html = openURL('http://example.com||MyProxyUrl=')
#xbmcgui.Dialog().ok('',str(html))


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


"""
conn = sqlite3.connect(dbfile)
c = conn.cursor()
if newdb:
	#c.execute('PRAGMA auto_vacuum = NONE')
	c.execute('CREATE TABLE htmlcache (expiry,url,data,headers,source,html)')
	c.execute('CREATE TABLE responsecache (expiry,url,data,headers,allow_redirects,source,response)')
	c.execute('CREATE TABLE serverscache (expiry,linkLIST,serversLIST,urlLIST)')
else:
	c.execute('DELETE FROM htmlcache WHERE expiry<'+str(now))
	c.execute('DELETE FROM responsecache WHERE expiry<'+str(now))
	c.execute('DELETE FROM serverscache WHERE expiry<'+str(now))
conn.commit()
conn.close()
"""

	
if not (menu_label=='..' and mode=='164' and text=='VOD'):
	results = MAIN_DISPATCHER(mode,url,text,page)


if addon_handle==-1: sys.exit(0)


if int(mode) in [161,163,164] or (int(mode) in [166] and 'RANDOM' in text) or mode=='238':
	menuItemsLIST2 = []
	for type,name,url,mode2,image,text1,text2 in menuItemsLIST:
		if 'صفحة' not in name: menuItemsLIST2.append([type,name,url,mode2,image,text1,text2])
	if int(mode) in [161]: header_count = 2
	else: header_count = 3
	count = 6+header_count
	size = len(menuItemsLIST2)
	if size>count: size = count-header_count
	else: size = size-header_count
	if size>0: menuItemsLIST = menuItemsLIST2[0:header_count]+random.sample(menuItemsLIST2[header_count:],size)


for type,name,url,mode2,image,text1,text2 in menuItemsLIST:
	addKodiMenuItem(type,name,url,mode2,image,text1,text2)


search_modes = [19,29,39,49,59,69,79,99,119,139,149,209,229,249,259]
website_mainmenu_modes = [11,51,61,64,91,111,132,181,201,211,251]
filter_modes = [114,204,244,254]
menu_update1 = (int(mode) in filter_modes+[266,268])
menu_update2 = (int(mode)==165 and 'DELETE' in text)
allowed_empty_modes1 = (int(mode) in search_modes+website_mainmenu_modes+[265])
allowed_empty_modes2 = (len(menuItemsLIST)>0)
#xbmcgui.Dialog().ok(mode,text)
if menu_update1 or menu_update2: xbmcplugin.endOfDirectory(addon_handle,True,True,True)
elif allowed_empty_modes1 or allowed_empty_modes2: xbmcplugin.endOfDirectory(addon_handle,True,False,True)
else: xbmcplugin.endOfDirectory(addon_handle,False,False,True)





"""
#if menu_label=='Main Menu' and mode!='260': menuItemsLIST = []
#if 'قنوات' not in menu_label and mode=='161':
#	xbmcplugin.endOfDirectory(addon_handle,False,False,True)
#	sys.exit(0)
#else:

if menu_label=='..':
	remianing = int(mode)%10
	if remianing==9 and text=='': sys.exit(0)
	if mode=='164' and text=='VOD': sys.exit(0)
#else: MAIN_DISPATCHER(mode,url,text,page)


#if menu_label=='Main Menu' and mode!='260': menuItemsLIST = []
#else: 

if menu_label=='..':
	remianing = int(mode)%10
	if remianing==9 and text=='': sys.exit()
	if mode=='164' and text=='VOD': sys.exit()
#if menu_label=='Main Menu' and mode!='260': sys.exit()
#if menu_label=='': sys.exit()
#if mode=='161' and menu_label=='': sys.exit()


mode2 = int(mode)
mode3 = int(mode2/10)
WEBSITES_TV = [27,41,135]
IPTV = [231,232,237,239]
PLAY = [12,24,33,43,53,63,74,82,92,105,112,123,134,143,182,202,212,223,243,252]
NOT_FOLDER_MODES = WEBSITES_TV+IPTV+PLAY
if mode3 not in [0,15,17,19] and mode2 not in NOT_FOLDER_MODES:
	#if menu_label!='Main Menu':
	xbmcplugin.endOfDirectory(addon_handle)
"""


#try: xbmcplugin.endOfDirectory(addon_handle)
#except: pass

#raise SystemExit
#sys.exit(0)

#if addon_handle > -1:
#xbmc.Player().play()



