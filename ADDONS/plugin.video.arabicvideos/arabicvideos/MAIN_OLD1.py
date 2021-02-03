


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


"""	
#if not (menu_label=='..'):# and mode=='164' and text=='VOD'):
#	results = MAIN_DISPATCHER(type,name,url,mode,image,page,text)
#if addon_handle==-1: sys.exit(0)



#if 'RANDOM' in text:
#if int(mode) in [161,163,164] or 'RANDOM' in text:
#if int(mode) in [167]:
if 0:
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
"""




# To force the appearance of "Busy" message
# In addMenuItem use type 'video' ... do not use 'link' or 'live' or 'folder'
# or use:
#	xbmc.executebuiltin('ActivateWindow(busydialog)')
#	xbmc.executebuiltin('Dialog.Close(busydialog)')
#
# no need to do anything more
# then add its mode2 to this list ... this will force kodi not to play it as a video
# 7: get versions	&	232: get IPTV files
#NEED_BUSY_MESSAGE = mode2 in [7,232]
#if NEED_BUSY_MESSAGE: succeeded = False


#DIALOG_OK(mode,text)


#SKIP_VIDEO_PLAY = mode2 in [176]
#if SKIP_VIDEO_PLAY: succeeded = False

#PLAY_VIDEO_MODES = mode2 in [12,24,33,43,53,63,74,82,92,105,112,123,134,143,182,202,212,223,243,252]
#if PLAY_VIDEO_MODES: succeeded = False

#SERVICES_MODES = mode3 not in [0,15,17,19]
#if SERVICES_MODES: succeeded = False

#SEARCH_MODES = mode2 in [19,29,39,49,59,69,79,99,119,139,149,209,229,249,259]
#if SEARCH_MODES: succeeded = True

#SITES_PLAY_MODES = mode2 in [27,41,135]
#if SITES_PLAY_MODES: succeeded = False

#IPTV_PLAY_MODES = mode2 in [235]
#if IPTV_PLAY_MODES: succeeded = False


#xbmcplugin.endOfDirectory(addon_handle,True,False,True)
#sys.exit(0)


# ==========================================================
# ==========================================================
# ==========================================================


"""
lastvideos_modes = [265,267]
search_modes = [19,29,39,49,59,69,79,99,119,139,149,209,229,249,259]
website_mainmenu_modes = [11,51,61,64,91,111,132,181,201,211,251]
filter_modes = [114,204,244,254]
menu_update1 = (int(mode) in filter_modes+[266])
menu_update2 = (int(mode)==165 and '_FORGETRESULTS_' in text)
allowed_empty_modes1 = (int(mode) in search_modes+website_mainmenu_modes+[265])
allowed_empty_modes2 = (len(menuItemsLIST)>0)
#DIALOG_OK(mode,text)
if menu_update1 or menu_update2: xbmcplugin.endOfDirectory(addon_handle,True,True,True)
elif allowed_empty_modes1 or allowed_empty_modes2: xbmcplugin.endOfDirectory(addon_handle,True,False,True)
else: xbmcplugin.endOfDirectory(addon_handle,False,False,True)


# defaults:		succeeded,updateListing,cacheToDisc = True,False,True
#succeeded – True=script completed successfully(Default)/ False=Script did not.
#updateListing – True=this folder should update the current listing/False=Folder is a subfolder(Default).
#cacheToDisc – True=Folder will cache if extended time(default)/False=this folder will never cache to disc.
"""







"""
search_modes = [19,29,39,49,59,69,79,99,119,139,149,209,229,249,259]
sites_mainmenu_modes = [11,51,61,64,91,111,132,181,201,211,251]
filter_modes = [114,204,244,254]

succeeded = True
if int(mode) not in search_modes+sites_mainmenu_modes+[265]: succeeded = False
if len(menuItemsLIST)==0: succeeded = False
if int(mode) not in filter_modes+[266]: succeeded = False
if int(mode)!=165 or '_FORGETRESULTS_' not in text: succeeded = False

updateListing = False
if int(mode) not in filter_modes+[266]: updateListing = True
if int(mode)!=165 or '_FORGETRESULTS_' not in text: updateListing = True

cacheToDisc = True
xbmcplugin.endOfDirectory(addon_handle,succeeded,updateListing,cacheToDisc)
"""








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
#else: MAIN_DISPATCHER(type,name,url,mode,image,page,text)


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


#response = OPENURL_REQUESTS('GET','http://example.com||MyDNSUrl=')
#html = response.content
#DIALOG_OK('',str(html))
#html = OPENURL('http://example.com||MyProxyUrl=http://198.50.147.158:3128')
#DIALOG_OK('',str(html))
#html = OPENURL('http://example.com||MyProxyUrl=')
#DIALOG_OK('',str(html))
