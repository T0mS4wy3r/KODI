﻿# -*- coding: utf-8 -*-

# import MAIN

# total cost = 0 ms
# Because they are already included with some other modules
import xbmcplugin,xbmcgui,xbmcaddon,xbmc,sys,os,re,time,thread # total cost = 0ms
import zlib,ssl,random,hashlib,base64,string,httplib,cPickle # total cost = 0ms
import socket,struct,traceback # total cost = 0ms
import urllib		# 160ms
import urllib2		# 354ms (contains urllib)
import sqlite3		# 50ms (with threading 71ms)

#import requests   	# 986ms (contains urllib,urllib2,urllib3)
#import threading	# 54ms (with sqlite3 71ms)
#import urllib3		# 621ms (contains urllib)
#import timeit		# 10ms
#import urlresolver	# 2170ms (contains urllib,urllib2,urllib3,requests)
#import platform	# 20ms
#import uuid		# 75ms
#import HTMLParser	# 18ms
#import unicodedata	# 4ms
#import SimpleHTTPServer	# 1922ms
#import BaseHTTPServer		# 44ms

# calculate the average time needed to import a main-module and how many sub-modules will be imported with it
"""
import sys,time
totalelpased = 0
for i in range(20):
	t1 = time.time()
	before_import = sys.modules.keys()
	import traceback
	after_import = sys.modules.keys()
	import_list = list(set(after_import)-set(before_import))
	for modu in import_list:
		del(sys.modules[modu])
	after_delete = sys.modules.keys()
	t2 = time.time()
	elpased = t2-t1
	totalelpased += elpased
before_import_count = len(before_import)
after_import_count = len(after_import)
import_count = len(import_list)
after_delete_count = len(after_delete)
#print('import_count: '+str(import_count))
#print('average time ms: '+str(totalelpased*1000/20))
import xbmcgui
xbmcgui.Dialog().ok('number of modules imported: '+str(import_count),'average time ms: '+str(totalelpased*1000/20))
EXIT_using_ERROR
"""

# to check if main-module will import what sub-modules
# example: importing "requests" will also import "urllib","urllib2" and "urllib3"
"""
import sys
before_import = sys.modules.keys()
import urlresolver
after_import = sys.modules.keys()
import_list = list(set(after_import)-set(before_import))
list = ''
if 'urllib' in after_import: list += 'urllib '
if 'urllib2' in after_import: list += 'urllib2 '
if 'urllib3' in after_import: list += 'urllib3 '
if 'requests' in after_import: list += 'requests '
import xbmcgui
xbmcgui.Dialog().ok('yes exists: ',list)
"""

script_name = 'LIBRARY'

addon_handle = int(sys.argv[1])
addon_id = sys.argv[0].split('/')[2]	# plugin.video.arabicvideos
addon_name = addon_id.split('.')[2]		# arabicvideos
addon_path = sys.argv[2]				# ?mode=12&url=http://test.com
#addon_url = sys.argv[0]+addon_path		# plugin://plugin.video.arabicvideos/?mode=12&url=http://test.com
#addon_path = xbmc.getInfoLabel( "ListItem.FolderPath" )
addon_version = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )

menu_path = urllib2.unquote(addon_path).replace('[COLOR FFC89008]','').replace('[/COLOR]','').strip(' ')
menu_label = xbmc.getInfoLabel('ListItem.Label').replace('[COLOR FFC89008]','').replace('[/COLOR]','').strip(' ')
if menu_label=='': menu_label = 'Main Menu'

kodi_release = xbmc.getInfoLabel("System.BuildVersion")
kodi_version = re.findall('&&(.*?)[ -]','&&'+kodi_release,re.DOTALL)
kodi_version = float(kodi_version[0])
#xbmcgui.Dialog().ok(kodi_release,str(kodi_version))
icon = xbmc.translatePath(os.path.join('special://home/addons/'+addon_id,'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/'+addon_id,'fanart.jpg'))

addoncachefolder = os.path.join(xbmc.translatePath('special://temp'),addon_id)
dbfile = os.path.join(addoncachefolder,"webcache_"+addon_version+".db")
lastvideosfile = os.path.join(addoncachefolder,"lastvideos.lst")
lastrandomfile = os.path.join(addoncachefolder,"lastrandom.lst")
favouritesfile = os.path.join(addoncachefolder,"favourites.lst")
dummyiptvfile = os.path.join(addoncachefolder,"dummy.iptv")

MINUTE = 60
HOUR = 60*MINUTE
LONG_CACHE = 24*HOUR*3
REGULAR_CACHE = 16*HOUR
SHORT_CACHE = 2*HOUR
VERY_SHORT_CACHE = 30*MINUTE
VERY_LONG_CACHE = 24*HOUR*90
NO_CACHE = 0
now = int(time.time())

#LONG_CACHE = 0
#REGULAR_CACHE = 0
#SHORT_CACHE = 0

WEBSITES = { 'AKOAM'		:['https://akoam.net']
			,'AKWAM'		:['https://akwam.net']
			,'ALARAB'		:['https://vod.alarab.com']
			,'ALFATIMI'		:['http://alfatimi.tv']
			,'ALKAWTHAR'	:['https://www.alkawthartv.com']
			,'ALMAAREF'		:['http://www.almaareftv.com/old','http://www.almaareftv.com']
			,'ARABLIONZ'	:['http://arablionz.com']
			,'EGYBESTVIP'	:['https://egybest.vip']
			,'HELAL'		:['https://4helal.tv']
			,'IFILM'		:['http://ar.ifilmtv.com','http://en.ifilmtv.com','http://fa.ifilmtv.com','http://fa2.ifilmtv.com']
			,'PANET'		:['http://www.panet.co.il']
			,'SHAHID4U'		:['https://shahid4u.net']
			,'SHOOFMAX'		:['https://shoofmax.com','https://static.shoofmax.com']
			,'ARABSEED'		:['https://arabseed.net']
			,'YOUTUBE'		:['https://www.youtube.com']
			,'LIVETV'		:['http://emadmahdi.pythonanywhere.com/listplay','http://emadmahdi.pythonanywhere.com/usagereport']
			,'IPTV'			:['https://nowhere.com']
			#,'EGY4BEST'	:['https://egybest.vip']
			#,'EGYBEST'		:['https://egy.best']
			#,'HALACIMA'	:['https://www.halacima.co']
			#,'MOVIZLAND'	:['https://movizland.online','https://m.movizland.online']
			#,'SERIES4WATCH':['https://series4watch.net']  # 'https://s4w.tv'
			}

def MAIN():
	# -*- coding: utf-8 -*-
	#from LIBRARY import *
	LOG_THIS('NOTICE','============================================================================================')
	script_name = 'MAIN'

	if not os.path.exists(addoncachefolder): os.makedirs(addoncachefolder)
	if not os.path.exists(dbfile):
		LOG_THIS('NOTICE','  .  New Arabic Videos version installed  .  path: [ '+addon_path+' ]')
		xbmcgui.Dialog().ok('رسالة من المبرمج','تم مسح الكاش الموجود في البرنامج . أو تم تحديث البرنامج إلى الإصدار الجديد . سيقوم البرنامج الآن ببعض الفحوصات لضمان عمل البرنامج بصورة صحيحة ومتكاملة')
		CLEAN_KODI_CACHE_FOLDER()
		conn = sqlite3.connect(dbfile)
		conn.close()
		import SERVICES
		SERVICES.KODI_SKIN()
		#xbmcgui.Dialog().notification('رسالة من المبرمج','فحص اضافات adaptive + rtmp')
		#xbmcgui.Dialog().notification('رسالة من المبرمج','فحص مخزن عماد')
		#xbmcgui.Dialog().ok('',str(iptv))
		ENABLE_MPD(False)
		ENABLE_RTMP(False)
		SERVICES.INSTALL_REPOSITORY(True)
		SERVICES.HTTPS_TEST()
		#iptv = IPTV.isIPTVFiles(False)
		#if iptv: 
		xbmcgui.Dialog().ok('رسالة من المبرمج','إذا كنت تستخدم خدمة IPTV الموجودة في هذا البرنامج فسوف يقوم البرنامج الآن أوتوماتيكيا بجلب ملفات IPTV جديدة')
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
	if favourite not in ['','1','2','3','4','NOREFRESH']:
		message = message+'   .  Favourite: [ '+favourite+' ]'
	LOG_THIS('NOTICE',LOGGING(script_name)+message)

	#xbmcgui.Dialog().ok('['+menu_path+']','['+mode+']')
	#xbmcgui.Dialog().ok('['+menu_label+']','['+menu_path+']')

	UPDATE_RANDOM_MENUS = mode2==16 and mode0 not in [160,165]
	UPDATE_RANDOM_SUBMENUS = mode2==16 and 'UPDATE' in text
	SEARCH_MODES = mode0 in [19,29,39,49,59,69,79,99,119,139,149,209,229,239,249,259]
	SITES_MODES = mode2 in [1,2,3,4,5,6,7,9,11,13,14,20,22,24,25]
	IPTV_MODES = mode2==23 and text!=''
	YOUTUBE_UPDATE = mode2==14 and 'UPDATE' in text

	#xbmcgui.Dialog().ok(addon_path,str(addon_handle))

	if favourite not in ['','1','2','3','4','NOREFRESH']:
		import FAVOURITES
		FAVOURITES.FAVOURITES_DISPATCHER(favourite)
		#"Container.Refresh" used because there is no addon_handle number to use for ending directory
		#"Container.Update" used to open a menu list using specific addon_path
		#xbmc.executebuiltin("Container.Update("+sys.argv[0]+addon_path.split('&favourite=')[0]+")")
		if 'NOREFRESH' not in favourite: xbmc.executebuiltin("Container.Refresh")
		EXIT_PROGRAM('MAIN-MAIN-1st',False)

	if mode0==266:
		import MENUS
		MENUS.DELETE_LAST_VIDEOS_MENU(text)
		xbmc.executebuiltin("Container.Refresh")
		EXIT_PROGRAM('MAIN-MAIN-2nd',False)

	if (SEARCH_MODES and menu_label not in ['..','Main Menu']) or (UPDATE_RANDOM_MENUS and menu_label!='Main Menu'):
		LOG_THIS('NOTICE','  .  Writing random list  .  path: [ '+addon_path+' ]')
		results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text,favourite)
		new_menuItemsLIST = []
		for type88,name88,url88,mode88,image88,page88,text88,favourite88 in menuItemsLIST:
			new_menuItemsLIST.append((type88,name88,url88,mode88,image88,page88,text88,'NOREFRESH'))
		newFILE = str(new_menuItemsLIST)
		with open(lastrandomfile,'w') as f: f.write(newFILE)
		menuItemsLIST[:] = new_menuItemsLIST
	elif (SEARCH_MODES and menu_label in ['..','Main Menu']) or (UPDATE_RANDOM_MENUS and menu_label=='Main Menu'):
		LOG_THIS('NOTICE','  .  Reading random list  .  path: [ '+addon_path+' ]')
		with open(lastrandomfile,'r') as f: oldFILE = f.read()
		menuItemsLIST[:] = eval(oldFILE)
	else: results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text,favourite)

	#xbmcgui.Dialog().ok(addon_path,str(mode0))

	if addon_handle>-1:

		if type=='folder' and menu_label!='..' and (SITES_MODES or IPTV_MODES): ADD_TO_LAST_VIDEO_FILES()

		FILTERING_MENUS = mode0 in [114,204,244,254] and text!=''
		DELETE_LAST_VIDEOS = mode0 in [266,268]

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
		if FILTERING_MENUS or DELETE_LAST_VIDEOS or UPDATE_RANDOM_SUBMENUS or YOUTUBE_UPDATE: updateListing = True
		else: updateListing = False


		#LOG_THIS('NOTICE',str(succeeded)+'  '+str(updateListing)+'  '+str(cacheToDisc))
		xbmcplugin.endOfDirectory(addon_handle,succeeded,updateListing,cacheToDisc)

		#PLAY_VIDEO_MODES = mode2 in [12,24,33,43,53,63,74,82,92,105,112,123,134,143,182,202,212,223,243,252]
		#xbmcgui.Dialog().ok(str(succeeded),str(updateListing),str(cacheToDisc))
		#xbmcgui.Dialog().ok(addon_path,str(addon_handle))

	#xbmcgui.Dialog().ok(str(addon_handle),addon_path)
	return

def MAIN_DISPATCHER(type,name,url,mode,image,page,text,favourite):
	mode = int(mode)
	mode2 = int(mode/10)
	#xbmcgui.Dialog().ok(str(mode),str(mode2))
	results = None
	if   mode2==0:  import SERVICES 	; results = SERVICES.MAIN(mode,text)
	elif mode2==1:  import ALARAB 		; results = ALARAB.MAIN(mode,url,text)
	elif mode2==2:  import IFILM 		; results = IFILM.MAIN(mode,url,page,text)
	elif mode2==3:  import PANET 		; results = PANET.MAIN(mode,url,page,text)
	elif mode2==4:  import ALMAAREF 	; results = ALMAAREF.MAIN(mode,url,text)
	elif mode2==5:  import SHOOFMAX 	; results = SHOOFMAX.MAIN(mode,url,text)
	elif mode2==6:  import ALFATIMI 	; results = ALFATIMI.MAIN(mode,url,text)
	elif mode2==7:  import AKOAM 		; results = AKOAM.MAIN(mode,url,text)
	elif mode2==8:  import HALACIMA 	; results = HALACIMA.MAIN(mode,url,page,text)
	elif mode2==9:  import HELAL 		; results = HELAL.MAIN(mode,url,text)
	elif mode2==10: import LIVETV 		; results = LIVETV.MAIN(mode,url)
	elif mode2==11: import SHAHID4U 	; results = SHAHID4U.MAIN(mode,url,text)
	elif mode2==12: import EGYBEST 		; results = EGYBEST.MAIN(mode,url,page,text)
	elif mode2==13: import ALKAWTHAR	; results = ALKAWTHAR.MAIN(mode,url,page,text)
	elif mode2==14: import YOUTUBE 		; results = YOUTUBE.MAIN(mode,url,text,type,page)
	elif mode2==15: import SERVICES 	; results = SERVICES.MAIN(mode,text)
	elif mode2==16: import RANDOMS	 	; results = RANDOMS.MAIN(mode,url,text)
	elif mode2==17: import SERVICES 	; results = SERVICES.MAIN(mode,text)
	elif mode2==18: import MOVIZLAND	; results = MOVIZLAND.MAIN(mode,url,text)
	elif mode2==19: import SERVICES 	; results = SERVICES.MAIN(mode,text)
	elif mode2==20: import ARABLIONZ	; results = ARABLIONZ.MAIN(mode,url,text)
	elif mode2==21: import SERIES4WATCH ; results = SERIES4WATCH.MAIN(mode,url,text)
	elif mode2==22: import EGYBESTVIP 	; results = EGYBESTVIP.MAIN(mode,url,page,text)
	elif mode2==23: import IPTV 		; results = IPTV.MAIN(mode,url,text,type)
	elif mode2==24: import AKWAM 		; results = AKWAM.MAIN(mode,url,text)
	elif mode2==25: import ARABSEED 	; results = ARABSEED.MAIN(mode,url,text)
	elif mode2==26: import MENUS 		; results = MENUS.MAIN(mode,url,text)
	elif mode2==27: import FAVOURITES 	; results = FAVOURITES.MAIN(mode,favourite)
	elif mode2==28: import IPTV 		; results = IPTV.MAIN(mode,url,text,type)
	return results

def LOG_MENU_LABEL(script_name,label,mode,path):
	id = '	[ '+addon_name.upper()+'-'+addon_version+'-'+script_name+' ]'
	message = id+'	Label: [ '+label+' ]	Mode: [ '+str(mode)+' ]	Path: [ '+path+' ]'
	xbmc.log(message, level=xbmc.LOGNOTICE)
	return

def LOG_THIS(level,message):
	#xbmc.log('EMAD 111'+message+'EMAD 222', level=xbmc.LOGNOTICE)
	if level=='ERROR': loglevel = xbmc.LOGERROR
	else: loglevel = xbmc.LOGNOTICE
	lines = message.split('   ')
	tabs,tab = '','      '
	shift = tab+tab+tab+tab+'  '
	if kodi_version>17.9: shift = shift+'           '
	#xbmcgui.Dialog().ok(str(kodi_version),'')
	#loglines = lines[0] + '\r'
	loglines = lines[0]
	for line in lines[1:]:
		if '\n' in line: line = line.replace('\n','\n'+tabs)
		#if 'Resolver 2:' in line or 'Resolver 3:' in line:
		#	line = line.replace('\nResolver 2:','\n'+tabs+'Resolver 2:')
		#	line = line.replace('\nResolver 3:','\n'+tabs+'Resolver 3:')
		tabs = tabs+tab
		loglines += '\r'+shift+tabs+line
	loglines += '_'
	if '%' in loglines: loglines = unquote(loglines)
	xbmc.log(loglines,level=loglevel)
	return

def LOGGING(script_name):
	function_name = sys._getframe(1).f_code.co_name
	if function_name=='<module>': function_name = 'MAIN'
	return '[ '+addon_name.upper()+'-'+addon_version+'-'+script_name+'-'+function_name+' ]'

class CustomePlayer(xbmc.Player):
	def __init__( self, *args, **kwargs ):
		self.status = ''
	def onPlayBackStopped(self):
		self.status='failed'
	def onPlayBackStarted(self):
		self.status='playing'
		time.sleep(1)
	def onPlayBackError(self):
		self.status='failed'
	def onPlayBackEnded(self):
		self.status='failed'

class CustomThread():
	def __init__(self,showDialogs=False):
		self.showDialogs = showDialogs
		self.finishedLIST,self.failedLIST = [],[]
		self.statusDICT,self.resultsDICT = {},{}
		self.starttimeDICT,self.finishtimeDICT,self.elpasedtimeDICT = {},{},{}
		#sys.stderr.write('9999: 0000:'+str(self.statusDICT.values()))
	def start_new_thread(self,id,func,*args):
		id = str(id)
		self.statusDICT[id] = 'running'
		if self.showDialogs: xbmcgui.Dialog().notification('',id)
		thread.start_new_thread(self.run,(id,func,args))
		#sys.stderr.write('9999: 1111:'+str(self.statusDICT.values()))
	def run(self,id,func,args):
		id = str(id)
		self.starttimeDICT[id] = time.time()
		try:
			#sys.stderr.write('9999: 6666:'+str(self.statusDICT.values()))
			self.resultsDICT[id] = func(*args)
			#sys.stderr.write('9999: 7777:'+str(self.statusDICT.values()))
			self.finishedLIST.append(id)
			self.statusDICT[id] = 'finished'
			#sys.stderr.write('9999: 2222:'+str(self.statusDICT.values()))
		except Exception as err:
			#traceback.print_exc(file=sys.stderr)
			errortrace = traceback.format_exc()
			sys.stderr.write(errortrace)
			self.resultsDICT[id] = '___Error___:-1:Threads function "'+func.func_name+'" failed due to '+str(err)
			self.resultsDICT[id] += '\n====================\n'+errortrace+'===================='
			self.failedLIST.append(id)
			self.statusDICT[id] = 'failed'
			#sys.stderr.write('9999: 3333:'+str(self.statusDICT.values()))
		self.finishtimeDICT[id] = time.time()
		self.elpasedtimeDICT[id] = self.finishtimeDICT[id] - self.starttimeDICT[id]
		#sys.stderr.write('9999: 4444:'+str(self.statusDICT.values()))
	def wait_finishing_all_threads(self):
		while 'running' in self.statusDICT.values():
			time.sleep(1.000)
			#sys.stderr.write('9999: 5555:'+str(self.statusDICT.values()))

def SHOW_ERRORS(source,code,reason,showDialogs):
	if '-' in source: site = source.split('-',1)[0]
	else: site = source
	#if code==104: xbmcgui.Dialog().ok('لديك خطأ اسبابه كثيرة','يرجى منك التواصل مع المبرمج عن طريق هذا الرابط','https://github.com/emadmahdi/KODI/issues')
	dns = (code in [7,10054,11001])
	blocked1 = (code in [0,104,10061,111])
	blocked2 = ('Blocked by Cloudflare' in reason)
	blocked3 = ('Blocked by 5 seconds browser check' in reason)
	messageARABIC = 'فشل في سحب الصفحة من الأنترنيت'
	messageENGLISH = 'Error '+str(code)+': '+reason
	if dns or blocked1 or blocked2 or blocked3:
		block_meessage = 'نوع من الحجب ضد كودي مصدره الأنترنيت الخاص بك.'
		if showDialogs: block_meessage += ' هل تريد تفاصيل اكثر ؟'
		if dns:
			messageARABIC = 'لديك خطأ DNS ومعناه تعذر ترجمة اسم الموقع إلى رقمه'
			messageARABIC += ' والسبب قد يكون '+block_meessage
		else: messageARABIC = 'هذا الموقع فيه '+block_meessage
		LOG_THIS('ERROR',LOGGING(script_name)+'   Source: [ '+source+' ]   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   messageARABIC: [ '+messageARABIC+' ]]   messageENGLISH: [ '+messageENGLISH+' ]')
		if showDialogs:
			yes = xbmcgui.Dialog().yesno(site+'   '+TRANSLATE(site),messageARABIC,messageENGLISH,'','كلا','نعم')
			if yes==1: import SERVICES ; SERVICES.MAIN(195)
	elif showDialogs:
		messageARABIC2 = messageARABIC+' . هل تريد معرفة الأسباب والحلول ؟'
		yes = xbmcgui.Dialog().yesno(site+'   '+TRANSLATE(site),messageARABIC2,messageENGLISH,'','كلا','نعم')
		if yes==1:
			messageDETAILS = 'قد يكون هناك نوع من الحجب عندك'
			messageDETAILS += '\n'+'أو الأنترنيت عندك مفصولة'
			messageDETAILS += '\n'+'أو الربط المشفر لا يعمل عندك'
			messageDETAILS += '\n'+'أو الموقع الأصلي غير متوفر الآن'
			messageDETAILS += '\n'+'أو الموقع الأصلي غير هذه الصفحة والمبرمج لا يعلم'
			messageDETAILS += '\n\n'+'جرب مسح الكاش (من قائمة خدمات البرنامج)'
			messageDETAILS += '\n'+'أو أرسل سجل الأخطاء والاستخدام إلى المبرمج (من قائمة خدمات البرنامج)'
			messageDETAILS += '\n'+'أو جرب طرق رفع الحجب (مثلا VPN , Proxy , DNS)'
			messageDETAILS += '\n'+'أو جرب طلب هذا الموقع لاحقا'
			xbmcgui.Dialog().textviewer('فشل في سحب الصفحة من الأنترنيت',messageDETAILS)
	return messageARABIC,messageENGLISH

NO_EXIT_LIST = [ 'LIBRARY-openURL_PROXY-1st'
				,'LIBRARY-openURL_HTTPSPROXIES-1st'
				,'LIBRARY-openURL_WEBPROXIES-1st'
				,'LIBRARY-openURL_WEBPROXIES-2nd'
				,'LIBRARY-openURL_WEBPROXYTO-1st'
				,'LIBRARY-openURL_WEBPROXYTO-2nd'
				,'LIBRARY-openURL_KPROXYCOM-1st'
				,'LIBRARY-openURL_KPROXYCOM-2nd'
				,'LIBRARY-openURL_KPROXYCOM-3rd'
				,'LIBRARY-CHECK_HTTPS_PROXIES-1st'
				,'LIBRARY-EXTRACT_M3U8-1st'
				,'LIBRARY-PLAY_VIDEO-1st'
				,'SERVICES-TEST_ALL_WEBSITES-1st'
				,'SERVICES-TEST_ALL_WEBSITES-2nd'
				,'EGYBESTVIP-PLAY-2nd'
				,'EGYBESTVIP-PLAY-3rd'
				,'HELAL-ITEMS-1st'
				,'YOUTUBE-RANDOM_USERAGENT-1st'
				,'LIBRARY-HTTPS-1st'
				,'IPTV-CHECK_ACCOUNT-1st'
				]
"""				,'AKOAM-MENU-1st'
				,'AKWAM-MENU-1st'
				,'ALARAB-MENU-1st'
				,'ALFATIMI-MENU-1st'
				,'ALKAWTHAR-MENU-1st'
				,'ALMAAREF-MENU-1st'
				,'ARABLIONZ-MENU-1st'
				,'ARABSEED-MENU-1st'
				,'EGYBESTVIP-MENU-1st'
				,'HELAL-MENU-1st'
				,'IFILM-MENU-1st'
				,'PANET-MENU-1st'
				,'SHAHID4U-MENU-1st'
				,'SHOOFMAX-MENU-1st'
"""

def EXIT_IF_SOURCE(source,code,reason,showDialogs):
	if showDialogs: SHOW_ERRORS(source,code,reason,showDialogs)
	condition1 = source not in NO_EXIT_LIST and 'RESOLVERS' not in source and '-MENU-1st' not in source
	if condition1: EXIT_PROGRAM(source)
	#condition2 = 'Blocked by Cloudflare' in reason
	#condition3 = 'Blocked by 5 seconds browser check' in reason
	return

def EXIT_PROGRAM(source='',showLog=True):
	if showLog: LOG_THIS('NOTICE',LOGGING(script_name)+'   Exit: Forced exit   Source: [ '+source+' ]')
	time.sleep(0.100)
	sys.exit(0)
	#raise SystemExit
	return

def CLEAN_KODI_CACHE_FOLDER():
	exceptionLIST = [lastvideosfile,favouritesfile]
	for filename in os.listdir(addoncachefolder):
		filename_full = os.path.join(addoncachefolder,filename)
		if filename_full not in exceptionLIST:
			try: os.remove(filename_full)
			except: pass
	return

contentsDICT = {}
menuItemsLIST = []

def addMenuItem(type,name,url,mode,image='',page='',text='',favourite=''):
	website = ''
	if '::' in name: website,name = name.split('::',1)
	if type=='folder' and website!='' and '_' in name:
		nameonly = name.split('_')[2]
		nameonly = nameonly.replace('ـ','').replace('  ',' ').replace('إ','ا').replace('آ','ا')
		nameonly = nameonly.replace('ة','ه').replace('و ','و').replace('أ','ا')
		nameonly = nameonly.replace('لأ','لا').replace('لإ','لا').replace('لآ','لا')
		nameonly = nameonly.strip(' ')
		cond1 = ('العاب' not in nameonly and 'خيال' not in nameonly and 'حاليه' not in nameonly)
		cond2 = ('الان' not in nameonly and 'البوم' not in nameonly)
		if cond1 and cond2: nameonly = nameonly.replace('ال','')
		nameonly = nameonly.replace('اخري','اخرى').replace('اجنبى','اجنبي').replace('عائليه','عائلي')
		nameonly = nameonly.replace('اجنبيه','اجنبي').replace('عربيه','عربي').replace('رومانسيه','رومانسي')
		nameonly = nameonly.replace(' | افلام اون لاين','').replace('انيميشن','انميشن').replace('غربيه','غربي')
		nameonly = nameonly.replace('تاريخي','تاريخ').replace('خيال علمي','خيال').replace('موسيقيه','موسيقى')
		nameonly = nameonly.replace('هندى','هندي').replace('هنديه','هندي').replace('وثائقيه','وثائقي')
		nameonly = nameonly.replace('تليفزيونيه','تلفزيون').replace('تلفزيونيه','تلفزيون')
		nameonly = nameonly.replace('الحاليه','حاليه').replace('موسیقی','موسيقى').replace('الانمي','انمي')
		nameonly = nameonly.replace('المسلسلات','مسلسلات').replace('البرامج','برامج')
		nameonly = nameonly.replace('حروب','حرب')
		#if 'PANET' in website: xbmcgui.Dialog().ok(nameonly,website)
		website = TRANSLATE(website)
		if nameonly not in contentsDICT.keys(): contentsDICT[nameonly] = {}
		name = name.replace('VOD_','').replace('_MOD_','')
		if name.count('_')>1: name = name.split('_',2)[2]
		if name=='': name = '....'
		contentsDICT[nameonly][website] = [type,name,url,mode,image,page,text,favourite]
	menuItemsLIST.append([type,name,url,mode,image,page,text,favourite])
	return

def getKodiMenuItem(menuItem):
	type,name,url,mode,image,text1,text2,favourite = menuItem
	if type=='folder': start1,start2 = ';',','
	else: start1,start2 = escapeUNICODE('\u02d1'),' '
	name2 = re.findall('&&_(\D\D\w)__MOD_(.*?)&&','&&'+name+'&&',re.DOTALL)
	if name2: name = start1+'[COLOR FFC89008]'+name2[0][0]+'  [/COLOR]'+name2[0][1]
	name2 = re.findall('&&_(\D\D\w)_(.*?)&&','&&'+name+'&&',re.DOTALL)
	if name2: name = start2+'[COLOR FFC89008]'+name2[0][0]+'  [/COLOR]'+name2[0][1]
	path = 'plugin://'+addon_id+'/?type='+type.strip(' ')
	path = path+'&mode='+str(mode).strip(' ')
	if type=='folder' and text1!='': path = path+'&page='+quote(text1.strip(' '))
	if favourite!='': path = path+'&favourite='+favourite.strip(' ')
	if name!='': path = path+'&name='+quote(name.strip(' '))
	if text2!='': path = path+'&text='+quote(text2.strip(' '))
	if image!='': path = path+'&image='+quote(image.strip(' '))
	else: image = icon
	if url!='': path = path+'&url='+quote(url.strip(' '))
	listitem = xbmcgui.ListItem(name)
	listitem.setArt({'icon':image,'thumb':image,'fanart':image,})
	context_menu = []
	if mode in [235,238] and type=='live':
		run_path = 'plugin://'+addon_id+'?mode=238&text=short_epg&url='+url
		run_text = '[COLOR FFFFFF00]البرامج القادمة[/COLOR]'
		run_item = (run_text,'XBMC.RunPlugin('+run_path+')')
		context_menu.append(run_item)
	elif mode in [265]:
		import MENUS
		length = MENUS.LAST_VIDEOS_MENU(text2,True)
		if length>0:
			run_path = 'plugin://'+addon_id+'?mode=266&text='+text2
			run_text = '[COLOR FFFFFF00]مسح قائمة آخر 30 '+TRANSLATE(text2)+'[/COLOR]'
			run_item = (run_text,'XBMC.RunPlugin('+run_path+')')
			context_menu.append(run_item)
	import FAVOURITES
	context_menu += FAVOURITES.GET_FAVOURITES_CONTEXT_MENU(path)
	listitem.addContextMenuItems(context_menu)
	if type in ['link','live']: isFolder = False
	elif type=='video':
		isFolder = False
		listitem.setInfo('video',{'mediatype':'video'})
		if text1!='':
			duration = '0:0:0:0:0:'+text1
			dummy,days,hours,minutes,seconds = duration.rsplit(':',4)
			duration = int(days)*24*HOUR+int(hours)*HOUR+int(minutes)*60+int(seconds)
			listitem.setInfo('video',{'duration':duration})
		listitem.setProperty('IsPlayable','true')
		xbmcplugin.setContent(addon_handle,'videos')
	elif type=='folder':
		isFolder = True
		listitem.setInfo(type="video",infoLabels={"Title":name})
	#xbmcplugin.addDirectoryItem(handle=addon_handle,url=path,listitem=listitem,isFolder=isFolder)
	return (path,listitem,isFolder)

def EXTRACT_KODI_PATH(path=''):
	args1 = {'type':'','mode':'','url':'','text':'','page':'','name':'','image':'','favourite':''}
	if path=='': path = addon_path
	if '?' in path: path = path.split('?')[1]
	url2,args2 = URLDECODE(path)
	args = dict(args1.items()+args2.items())
	mode = args['mode']
	url = urllib2.unquote(args['url'])
	text = urllib2.unquote(args['text'])
	page = urllib2.unquote(args['page'])
	type = urllib2.unquote(args['type'])
	name = urllib2.unquote(args['name'])
	image = urllib2.unquote(args['image'])
	favourite = args['favourite']
	#name = xbmc.getInfoLabel('ListItem.Label')
	#image = xbmc.getInfoLabel('ListItem.Icon')
	if mode=='': type = 'folder' ; mode = '260'
	return type,name,url,mode,image,page,text,favourite

def openURL_requests_cached(expiry,method,url,data,headers,allow_redirects,showDialogs,source):
	if expiry==0: return openURL_requests(method,url,data,headers,allow_redirects,showDialogs,source)
	response = READ_FROM_SQL3('OPENURL_REQUESTS',[method,url,data,headers,allow_redirects,showDialogs,source])
	if response: return response
	response = openURL_requests(method,url,data,headers,allow_redirects,showDialogs,source)
	html = response.content
	#xbmcgui.Dialog().ok(str(type(response)),html)
	if '___Error___' not in html:
		WRITE_TO_SQL3('OPENURL_REQUESTS',[method,url,data,headers,allow_redirects,showDialogs,source],response,expiry)
	return response

def openURL_cached(expiry,url,data,headers,showDialogs,source):
	#xbmcgui.Dialog().ok('OPENURL_CACHED 111','')
	#xbmcgui.Dialog().ok('11','')
	if expiry==0: return openURL(url,data,headers,showDialogs,source)
	#xbmcgui.Dialog().ok('22','')
	html = READ_FROM_SQL3('OPENURL',[url,data,headers,showDialogs,source])
	#xbmcgui.Dialog().ok('OPENURL_CACHED 222',html)
	if html: return html
	html = openURL(url,data,headers,showDialogs,source)
	if '___Error___' not in html:
		WRITE_TO_SQL3('OPENURL',[url,data,headers,showDialogs,source],html,expiry)
	return html

def openURL(url,data,headers,showDialogs,source):
	#xbmcgui.Dialog().ok(str(type(data)),str(data))
	if data=='' or 'dict' in str(type(data)): method = 'GET'
	else:
		method = 'POST'
		items = data.split('&')
		data = {}
		for item in items:
			key,value = item.split('=')
			data[key] = value
	response = openURL_requests(method,url,data,headers,True,showDialogs,source)
	html = str(response.content)
	return html

class dummy_object(): pass

def openURL_requests(method,url,data,headers,allow_redirects,showDialogs,source):
	if data=='': data = {}
	if headers=='': headers = {}
	if allow_redirects=='': allow_redirects = True
	if showDialogs=='': showDialogs = True
	#xbmcgui.Dialog().ok(url,'requests 11')
	#url = url + '||MyProxyUrl=http://188.166.59.17:8118'
	import requests
	proxies,timeout = {},40
	url2,proxyurl,dnsurl,sslurl = EXTRACT_URL(url)
	#xbmcgui.Dialog().ok(str(url),url2)
	if dnsurl!=None:
		import urllib3.util.connection
		original_create_connection = urllib3.util.connection.create_connection
		def patched_create_connection(address,*args,**kwargs):
			host,port = address
			ip = DNS_RESOLVER(host,dnsurl)
			if ip: host = ip[0]
			address = (host,port)
			return original_create_connection(address,*args,**kwargs)
		urllib3.util.connection.create_connection = patched_create_connection
	if proxyurl!=None:
		if headers=='': headers = { 'User-Agent' : '' }
		elif 'User-Agent' not in headers: headers['User-Agent'] = ''
		if proxyurl=='': proxyname,proxyurl = RANDOM_HTTPS_PROXY()
		# if testing proxies then timeout=10
		if url2=='https://www.google.com': timeout = 10
		proxies={"http":proxyurl,"https":proxyurl}
	if sslurl!=None: verify = True
	else: verify = False
	try:
		if method=='POST' and allow_redirects==True:
			url3 = url2
			for i in range(10):
				response = requests.request(method,url3,data=data,headers=headers,verify=verify,allow_redirects=False,timeout=timeout,proxies=proxies)
				if response.status_code<300 or response.status_code>399: break
				url3 = response.headers['Location']
		else: response = requests.request(method,url2,data=data,headers=headers,verify=verify,allow_redirects=allow_redirects,timeout=timeout,proxies=proxies)
		code,reason = response.status_code,response.reason
		succeded = True
		#response.raise_for_status()
	except requests.exceptions.HTTPError as err:
		# it works only if response.raise_for_status() is executed
		# code,reason = re.findall('(\d+).*?: (.*?):',err.message)[0]
		succeded = False
	except requests.exceptions.Timeout as err:
		reason,code = str(err.message).split(': ')[1],-1
		succeded = False
	except requests.exceptions.ConnectionError as err:
		reason,code = re.findall('>: (.*?):.*?(\d+)',err.message[0])[0]
		succeded = False
	except requests.exceptions.RequestException as err:
		reason,code = err.message,-1
		succeded = False
	except:
		#err_class = sys.exc_info()[0]
		#err_function = sys.exc_info()[1]
		#err_traceback = sys.exc_info()[2]
		# to find the code & reason from any class
		#print dir(err)
		#for i in dir(err):
		#    print i+' ===>> '+str(eval('err.'+i))
		reason,code = 'Unknown Error',-1
		succeded = False
	if 'google-analytics' not in url2 and succeded==False: traceback.print_exc(file=sys.stderr)
	else:
		#errortrace = traceback.format_exc()
		#sys.stderr.write(errortrace)
		#code = '-1'
		#reason = 'System encoding bug'
		pass
	code = int(code)
	response2 = dummy_object()
	if succeded:
		response2.headers = response.headers
		response2.cookies = response.cookies
		response2.url     = response.url
		response2.content = response.content
	else:
		response2.headers = {}
		response2.cookies = {}
		response2.url     = ''
		response2.content = '___Error___:'+str(code)+':'+reason
	response = response2
	html = str(response.content)
	htmlLower = html.lower()
	condition1 = code!=200 and int(code/100)*100!=300
	condition2 = 'cloudflare' in htmlLower and 'ray id: ' in htmlLower
	#if condition2: xbmcgui.Dialog().ok('','Cloudflare')
	condition3 = '___Error___' in htmlLower
	condition4 = '5 sec' in htmlLower and 'browser' in htmlLower and code!=200
	if condition1 or condition2 or condition3 or condition4:
		if condition2:
			#xbmcgui.Dialog().ok('','Cloudflare')
			reason2 = 'Blocked by Cloudflare'
			if 'recaptcha' in htmlLower: reason2 += ' using Google reCAPTCHA'
			reason = reason2+' ( '+reason+' )'
			html = '___Error___:'+str(code)+':'+reason
			response.content = html
		elif condition4:
			#xbmcgui.Dialog().ok('','5 seconds')
			reason4 = 'Blocked by 5 seconds browser check'
			reason = reason4+' ( '+reason+' )'
			html = '___Error___:'+str(code)+':'+reason
			response.content = html
		#elif 'google-analytics' in url:
		if code in [7,11001,10054] and dnsurl==None:
			LOG_THIS('ERROR',LOGGING(script_name)+'   DNS failed   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
			url = url+'||MyDNSUrl='
			response = openURL_requests(method,url,data,headers,allow_redirects,showDialogs,source)
			return response
		elif code==8 and sslurl==None:
			LOG_THIS('ERROR',LOGGING(script_name)+'   SSL failed   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
			url = url+'||MySSLUrl='
			response = openURL_requests(method,url,data,headers,allow_redirects,showDialogs,source)
			return response
		else:
			LOG_THIS('ERROR',LOGGING(script_name)+'   Failed opening url   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]'+'   URL: [ '+url+' ]')
		EXIT_IF_SOURCE(source,code,reason,showDialogs)
	return response

def EXTRACT_URL(url):
	allitems = url.split('||')
	url2,proxyurl,dnsurl,sslurl = allitems[0],None,None,None
	for item in allitems:
		if 'MyProxyUrl=' in item: proxyurl = item.split('=')[1]
		elif 'MyDNSUrl=' in item: dnsurl = item.split('=')[1]
		elif 'MySSLUrl=' in item: sslurl = item.split('=')[1]
	#if 'akoam.' in url2:
	#	https = url2.split(':')[0]
	#	proxyurl = https+'://159.203.87.130:3128'
	return url2,proxyurl,dnsurl,sslurl

def SERVER(url):
	return '/'.join(url.split('/')[:3])

def HOSTNAME(url,full=True):
	if '//' in url: url = url.split('/')[2].split(':')[0]
	if not full:
		url = url.replace('.net','').replace('.com','').replace('.org','').replace('.co','')
		url = url.replace('www.','')
	return url

def quote(url):
	return urllib2.quote(url,':/')
	#return urllib.quote(url,':/')

def unquote(url):
	return urllib2.unquote(url)
	#return urllib.unquote(url)

def unescapeHTML(string):
	if '&' in string and ';' in string:
		string = string.decode('utf8')
		import HTMLParser
		string = HTMLParser.HTMLParser().unescape(string)
		string = string.encode('utf8')
	return string

def escapeUNICODE(string):
	if '\\u' in string:
		string = string.decode('unicode_escape')
		string = string.encode('utf8')
	return string

def mixARABIC(string):
	import unicodedata
	#if '\u' in string:
	#	string = string.decode('unicode_escape')
	#	unicode_strings=re.findall(r'\u[0-9A-F]',string)	
	#	for unicode in unicode_strings
	#		char = unichar(
	#		replace(    , char)
	string = string.decode('utf8')
	new_string = ''
	for letter in string:
		#xbmcgui.Dialog().ok(unicodedata.decomposition(letter),hex(ord(letter)))
		if ord(letter) < 256: unicode_letter = '\\u00'+hex(ord(letter)).replace('0x','')
		elif ord(letter) < 4096: unicode_letter = '\\u0'+hex(ord(letter)).replace('0x','')
		else: unicode_letter = '\\u'+unicodedata.decomposition(letter).split(' ')[1]
		new_string += unicode_letter
	new_string = new_string.replace('\u06CC','\u0649')
	new_string = new_string.decode('unicode_escape')
	new_string = new_string.encode('utf-8')
	return new_string

def KEYBOARD(header='لوحة المفاتيح',default=''):
	#text = ''
	#kb = xbmc.Keyboard(default,header)
	#keyboard.setDefault(default)
	#keyboard.setHeading(header)
	#kb.doModal()
	#if kb.isConfirmed(): text = kb.getText()
	text = xbmcgui.Dialog().input(header,default,type=xbmcgui.INPUT_ALPHANUM)
	text = text.strip(' ')
	if len(text.decode('utf8'))<1:
		xbmcgui.Dialog().ok('رسالة من المبرمج','تم إلغاء الإدخال')
		return ''
	text = mixARABIC(text)
	return text

def ADD_TO_LAST_VIDEO_FILES():
	#vod_play_modes = [12,24,33,43,53,63,74,82,92,112,123,134,143,182,202,212,223,235,243,252]
	#live_play_modes = [235,105]
	#if int(mode)in vod_play_modes: filename = lastvodfile
	#elif int(mode)in live_play_modes: filename = lastlivefile
	#else: filename = ''
	type,name,url99,mode99,image99,page99,text99,favourite = EXTRACT_KODI_PATH()
	newItem = (type,name,url99,mode99,image99,page99,text99)
	if os.path.exists(lastvideosfile):
		with open(lastvideosfile,'r') as f: oldFILE = f.read()
		#oldFILE = oldFILE.replace('u\'','\'')
		oldFILE = eval(oldFILE)
	else: oldFILE = {}
	newFILE = {}
	for TYPE in oldFILE.keys():
		if TYPE!=type: newFILE[TYPE] = oldFILE[TYPE]
		else:
			if name!='..' and name!='':
				oldLIST = oldFILE[TYPE]
				if newItem in oldLIST:
					index = oldLIST.index(newItem)
					del oldLIST[index]
				newLIST = [newItem]+oldLIST
				newLIST = newLIST[:30]
				newFILE[TYPE] = newLIST
			else: newFILE[TYPE] = oldFILE[TYPE]
	if type not in newFILE.keys(): newFILE[type] = [newItem]
	newFILE = str(newFILE)
	with open(lastvideosfile,'w') as f: f.write(newFILE)
	return

def PLAY_VIDEO(url3,website='',type='video'):
	#LOG_THIS('NOTICE',LOGGING(script_name)+'   EEEEE starting PLAY_VIDEO')
	#t1 = time.time()
	ADD_TO_LAST_VIDEO_FILES()
	#t2 = time.time()
	#xbmcgui.Dialog().ok(str((t2-t1)*1000),'')
	#url3 = 's:\emad.m3u8999'
	result,subtitlemessage = 'canceled0',''
	if len(url3)==3:
		url,subtitle,httpd = url3
		if subtitle!='': subtitlemessage = '   Subtitle: [ '+subtitle+' ]'
	else: url,subtitle,httpd = url3,'',''
	url = url.replace(' ','%20')
	#url = quote(url)
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Preparing to play video   URL: [ '+url+' ]'+subtitlemessage)
	videofiletype = re.findall('(\.ts|\.mp4|\.m3u|\.m3u8|\.mpd|\.mkv|\.flv|\.mp3)(|\?.*?|/\?.*?|\|.*?)&&',url+'&&',re.DOTALL)
	if videofiletype: videofiletype = videofiletype[0][0]
	else: videofiletype = ''
	if videofiletype=='.m3u8' and website!='IPTV':
		headers = { 'User-Agent' : '' }
		#xbmcgui.Dialog().ok('11','')
		titleLIST,linkLIST = EXTRACT_M3U8(url,headers)
		#xbmcgui.Dialog().ok('22','')
		if len(linkLIST)>1:
			selection = xbmcgui.Dialog().select('اختر الملف المناسب:', titleLIST)
			if selection == -1:
				xbmcgui.Dialog().notification('تم الغاء التشغيل','')
				return result
		else: selection = 0
		url = linkLIST[selection]
		if titleLIST[0]!='-1':
			LOG_THIS('NOTICE',LOGGING(script_name)+'   Video Selected   Selection: [ '+titleLIST[selection]+' ]   URL: [ '+url+' ]')
	if 'http' in url.lower() and '/dash/' not in url and 'youtube.mpd' not in url:
		if 'https://' in url.lower():
			if '|' not in url: url = url+'|verifypeer=false'
			else: url = url+'&verifypeer=false'
		if 'user-agent' not in url.lower() and website!='IPTV':
			if '|' not in url: url = url+'|User-Agent=&'
			else: url = url+'&User-Agent=&'
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Got final url   URL: [ '+url+' ]')
	play_item = xbmcgui.ListItem()
	#play_item = xbmcgui.ListItem(path=url)
	play_item.setProperty('inputstreamaddon', '')
	play_item.setMimeType('mime/x-type')
	play_item.setInfo('Video', {'mediatype': 'video'})
	type99,name,url99,mode99,image,page99,text99,favourite = EXTRACT_KODI_PATH()
	#img = xbmc.getInfoLabel('ListItem.icon')
	play_item.setArt({'icon':image,'thumb':image,'fanart':fanart})
	play_item.setInfo( "Video",{'Title':name,'Label':name})
	#name = xbmc.getInfoLabel('ListItem.Label')
	#name = name.strip(' ')
	myplayer = CustomePlayer()
	if videofiletype in ['.ts','.mkv','.mp4','.mp3','.flv']:
		#when set to "False" it makes glarabTV fails and make WS2TV opens fast
		play_item.setContentLookup(False)
	#if videofiletype in ['.m3u8']: play_item.setContentLookup(False)
	if 'rtmp' in url: enabled = ENABLE_RTMP(True)
	if videofiletype=='.mpd' or '/dash/' in url:
		enabled = ENABLE_MPD(True)
		play_item.setProperty('inputstreamaddon','inputstream.adaptive')
		play_item.setProperty('inputstream.adaptive.manifest_type','mpd')
	if subtitle!='':
		play_item.setSubtitles([subtitle])
		#xbmc.log(LOGGING(script_name)+'      Added subtitle to video   Subtitle:['+subtitle+']', level=xbmc.LOGNOTICE)
	if type=='video':
		#title = xbmc.getInfoLabel('ListItem.Title')
		#play_item.setInfo('Video', {'duration': 3600})
		play_item.setPath(url)
		xbmcplugin.setResolvedUrl(addon_handle,True,play_item)
	elif type=='live':
		myplayer.play(url,play_item)
		#xbmc.Player().play(url,play_item)
	play_item.setContentLookup(False)
	#logfilename = xbmc.translatePath('special://logpath')+'kodi.log'
	timeout,step,result = 60,1,'tried'
	for i in range(0,timeout,step):
		xbmc.sleep(step*1000)
		result = myplayer.status
		if result=='playing':
			xbmcgui.Dialog().notification('الفيديو يعمل','','',500)
			LOG_THIS('NOTICE',LOGGING(script_name)+'   Success: Video is playing   URL: [ '+url+' ]'+subtitlemessage)
			break
		elif result=='failed':
			xbmcgui.Dialog().notification('الفيديو لم يعمل','')
			LOG_THIS('ERROR',LOGGING(script_name)+'   Failed playing video   URL: [ '+url+' ]'+subtitlemessage)
			break
		xbmcgui.Dialog().notification(myplayer.status +'جاري تشغيل الفيديو','باقي '+str(timeout-i)+' ثانية')
	else:
		result = 'timeout'
		myplayer.stop()
		xbmcgui.Dialog().notification('الفيديو لم يعمل','')
		LOG_THIS('ERROR',LOGGING(script_name)+'   Timeout unknown problem   URL: [ '+url+' ]'+subtitlemessage)
	if httpd!='':
		#xbmcgui.Dialog().ok('click ok to shutdown the http server','')
		#html = openURL_cached(NO_CACHE,'http://localhost:55055/shutdown','','','','LIBRARY-PLAY_VIDEO-2nd')
		httpd.shutdown()
		#xbmcgui.Dialog().ok('http server is down','')
	if result=='playing':
		#addon_version = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
		randomNumber = str(random.randrange(111111111111,999999999999))
		url2 = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addon_version+'&av='+addon_version+'&an=ARABIC_VIDEOS&ea='+website+'&z='+randomNumber
		html = openURL_requests('GET',url2,'','',True,False,'LIBRARY-PLAY_VIDEO-1st')
		#except: pass
	#LOG_THIS('NOTICE',LOGGING(script_name)+'   EEEEE finished PLAY_VIDEO')
	if result in ['tried','failed','timeout','playing']: EXIT_PROGRAM('LIBRARY-PLAY_VIDEO-2nd',False)
	#EXIT_PROGRAM('LIBRARY-PLAY_VIDEO-3rd')
	#if 'https://' in url and result in ['failed','timeout']:
	#	working = HTTPS(False)
	#	if not working:
	#		xbmcgui.Dialog().ok('الاتصال مشفر','مشكلة ... هذا الفيديو يحتاج الى اتصال مشفر (ربط مشفر) ولكن للأسف الاتصال المشفر لا يعمل على جهازك')
	#		return 'https'
	return result

def EXTRACT_M3U8(url,headers=''):
	#headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
	#url = 'https://vd84.mycdn.me/video.m3u8'
	#with open('S:\\test2.m3u8', 'r') as f: html = f.read()
	html = openURL_cached(NO_CACHE,url,'',headers,'','LIBRARY-EXTRACT_M3U8-1st')
	#xbmcgui.Dialog().ok('11','')
	if 'TYPE=AUDIO' in html: return ['-1'],[url]
	if 'TYPE=VIDEO' in html: return ['-1'],[url]
	#if 'TYPE=SUBTITLES' in html: return ['-1'],[url]
	#xbmc.log(item, level=xbmc.LOGNOTICE)
	titleLIST,linkLIST,qualityLIST,bitrateLIST = [],[],[],[]
	lines = re.findall('EXT-X-STREAM-INF:(.*?)[\n\r]+(.*?)[\n\r]+',html+'\n\r',re.DOTALL)
	if not lines: return ['-1'],[url]
	#xbmcgui.Dialog().ok('22','')
	for line,link in lines:
		lineDICT,bitrate,quality = {},-1,-1
		videofiletype = re.findall('(\.ts|\.mp4|\.m3u|\.m3u8|\.mpd|\.mkv|\.flv|\.mp3)(|\?.*?|/\?.*?|\|.*?)&&',link+'&&',re.DOTALL)
		if videofiletype: title = videofiletype[0][0][1:]+'   '
		else: title = ''
		line = line.lower()
		items = line.split(',')
		for item in items:
			if '=' in item:
				key,value = item.split('=')
				lineDICT[key] = value
		if 'average-bandwidth' in line:
			bitrate = int(lineDICT['average-bandwidth'])/1024
			#title += 'AvgBW: '+str(bitrate)+'kbps   '
			title += str(bitrate)+'kbps   '
		elif 'bandwidth' in line:
			bitrate = int(lineDICT['bandwidth'])/1024
			#title += 'BW: '+str(bitrate)+'kbps   '
			title += str(bitrate)+'kbps   '
		if 'resolution' in line:
			quality = int(lineDICT['resolution'].split('x')[1])
			#title += 'Res: '+str(quality)+'   '
			title += str(quality)+'   '
		title = title.strip('   ')
		if title=='': title = 'Unknown'
		if 'http' not in link: link = url.rsplit('/',1)[0]+'/'+link
		titleLIST.append(title)
		linkLIST.append(link)
		qualityLIST.append(quality)
		bitrateLIST.append(bitrate)
	z = zip(titleLIST,linkLIST,qualityLIST,bitrateLIST)
	#z = set(z)
	z = sorted(z, reverse=True, key=lambda key: key[3])
	titleLIST,linkLIST,qualityLIST,bitrateLIST = zip(*z)
	titleLIST,linkLIST = list(titleLIST),list(linkLIST)
	#selection = xbmcgui.Dialog().select('', titleLIST)
	#selection = xbmcgui.Dialog().select('', linkLIST)
	#xbmcgui.Dialog().ok('99','')
	return titleLIST,linkLIST

def dummyClientID(length):
	#import uuid
	#macfull = hex(uuid.getnode())		# e1f2ace4a35e
	#mac = '-'.join(mac_num[i:i+2].upper() for i in range(0,11,2))		# E1:F2:AC:E4:A3:5E
	import platform
	hostname = platform.node()			# empc12/localhosting
	os_type = platform.system()			# Windows/Linux
	os_version = platform.release()		# 10.0/3.14.22
	os_bits = platform.machine()		# AMD64/aarch64
	#processor = platform.processor()	# Intel64 Family 9 Model 68 Stepping 16, GenuineIntel/''
	settings = xbmcaddon.Addon(id=addon_id)
	savednode = settings.getSetting('node')
	if savednode=='':
		import uuid
		node = str(uuid.getnode())		# 326509845772831
		settings.setSetting('node',node)
	else:
		node = savednode
	hashComponents = node+':'+hostname+':'+os_type+':'+os_version+':'+os_bits
	md5full = hashlib.md5(hashComponents).hexdigest()
	md5 = md5full[0:length]
	#xbmcgui.Dialog().ok(node,md5)
	return md5
	"""
	#settings = xbmcaddon.Addon(id=addon_id)
	#settings.setSetting('user.hash','')
	#settings.setSetting('user.hash2','')
	#settings.setSetting('user.hash3','')
	#settings.setSetting('user.hash4','')
	#else: file = 'saverealhash4'
	#url = 'http://emadmahdi.pythonanywhere.com/saveinput'
	#input = md5full + '  ::  Found at:' + str(i) + '  ::  ' + hashComponents
	#	#payload = { 'file' : file , 'input' : input }
	#	#data = urllib.urlencode(payload)
	#	#html = openURL_cached(NO_CACHE,url,data,'','','LIBRARY-DUMMYCLIENTID-1st')
	#headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
	#payload = "file="+file+"&input="+input
	#import requests
	#response = requests.request("POST", url, data=payload, headers=headers)
	#	#html = response.content
	#	#xbmcgui.Dialog().ok(html,html)
	#url = 'http://emadmahdi.pythonanywhere.com/saveinput'
	#payload = { 'file' : 'savehash' , 'input' : md5full + '  ::  ' + hashComponents }
	#data = urllib.urlencode(payload)
	#return ''
	"""

def DNS_RESOLVER(url,dnsserver=''):
	if url.replace('.','').isdigit(): return [url]
	if dnsserver=='': dnsserver = '8.8.8.8'
	packet = struct.pack(">H", 12049)  # Query Ids (Just 1 for now)
	packet += struct.pack(">H", 256)  # Flags
	packet += struct.pack(">H", 1)  # Questions
	packet += struct.pack(">H", 0)  # Answers
	packet += struct.pack(">H", 0)  # Authorities
	packet += struct.pack(">H", 0)  # Additional
	split_url = url.decode('utf-8').split(".")
	for part in split_url:
		parts = part.encode('utf-8')
		packet += struct.pack("B", len(part))
		for byte in part:
			packet += struct.pack("c", byte.encode('utf-8'))
	packet += struct.pack("B", 0)  # End of String
	packet += struct.pack(">H", 1)  # Query Type
	packet += struct.pack(">H", 1)  # Query Class
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(bytes(packet), (dnsserver, 53))
	data, addr = sock.recvfrom(1024)
	sock.close()
	raw_header = struct.unpack_from(">HHHHHH", data, 0)
	ancount = raw_header[3]
	offset = len(url)+18
	answer = []
	for _ in range(ancount):
		offset2 = offset
		bytes_read = 1
		jump = False
		while True:
			byte = struct.unpack_from(">B", data, offset2)[0]
			if byte == 0:
				offset2 += 1
				break
			# If the field has the first two bits equal to 1, it's a pointer
			if byte >= 192:
				next_byte = struct.unpack_from(">B", data, offset2 + 1)[0]
				# Compute the pointer
				offset2 = ((byte << 8) + next_byte - 0xc000) - 1
				jump = True
			offset2 += 1
			if jump == False: bytes_read += 1
		if jump == True: bytes_read += 1
		offset = offset + bytes_read
		aux = struct.unpack_from(">HHIH", data, offset)
		offset = offset + 10
		x_type = aux[0]
		rdlength = aux[3]
		if x_type == 1: # A type
			rdata = struct.unpack_from(">"+"B"*rdlength, data, offset)
			ip = ''
			for byte in rdata: ip += str(byte) + '.'
			ip = ip[0:-1]
			answer.append(ip)
		if x_type in [1,2,5,6,15,28]: offset = offset + rdlength
	if not answer: LOG_THIS('ERROR',LOGGING(script_name)+'   DNS_RESOLVER failed getting ip   URL: [ '+url+' ]')
	return answer

def RATING_CHECK(script_name,url,ratingLIST):
	#xbmcgui.Dialog().ok(url,str(ratingLIST))
	if ratingLIST:
		blockedLIST = ['R','MA','16','17','18','كبار']
		cond1 = any(value in ratingLIST[0] for value in blockedLIST)
		cond2 = 'not rated' not in ratingLIST[0].lower()
		if cond1 and cond2:
			LOG_THIS('ERROR',LOGGING(script_name)+'   Blocked adults video   URL: [ '+url+' ]')
			xbmcgui.Dialog().notification('رسالة من المبرمج','الفيديو للكبار فقط وأنا منعته')
			return True
	return False

"""
#inputstream.adaptive:	mpd, hls, ism
#inputstream.rtmp:		rtmp
#xbmc.executebuiltin('InstallAddon(inputstream.rtmp)',wait=True)import inputstreamhelper
import inputstreamhelper
helper = inputstreamhelper.Helper('hls')
installed = helper.check_inputstream()
xbmcgui.Dialog().ok('is installed',str(installed))
if not installed:
	yes = xbmcgui.Dialog().yesno('Addon not installed','install now ?','','','كلا','نعم')
	if yes: helper._install_inputstream()
"""

def ENABLE_MPD(checkvideo_msg=False):
	enabled = xbmc.getCondVisibility('System.HasAddon(inputstream.adaptive)')
	if not enabled:
		if checkvideo_msg: yes = xbmcgui.Dialog().yesno('رسالة من المبرمج','هذا الفيديو لا يعمل عندك . انت بحاجة إلى إضافة اسمها inputstream.adaptive لكي تستطيع تشغيل فيديوهات نوع mpd hls ism . هل تريد تنصيب وتفعيل هذه الإضافة الآن ؟','','','كلا','نعم')
		else: yes = xbmcgui.Dialog().yesno('رسالة من المبرمج','inputstream.adaptive \n\r هذه ألإضافة عندك غير مفعلة أو غير موجودة . يجب تنصيبها وتفعيلها لكي تعمل عندك فيديوهات نوع mpd hls ism  . هل تريد تنصيب وتفعيل هذه الإضافة الآن ؟','','','كلا','نعم')
		if yes:
			xbmc.executebuiltin('InstallAddon(inputstream.adaptive)',wait=True)
			result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"inputstream.adaptive","enabled":true}}')
			if 'OK' in result: xbmcgui.Dialog().ok('رسالة من المبرمج','تم التنصيب والتفعيل وهذه الإضافة inputstream.adaptive جاهزة للاستخدام')
			else: xbmcgui.Dialog().ok('رسالة من المبرمج','فشل في التنصيب أو التفعيل . البرنامج غير قادر على تنصيب أو تفعيل هذه الإضافة . والحل هو تنصيبها وتفعيلها من خارج البرنامج')
	elif not checkvideo_msg: xbmcgui.Dialog().ok('رسالة من المبرمج','فحص اضافة inputstream.adaptive \n\r هذه ألإضافة عندك موجودة ومفعلة وجاهزة للاستخدام')
	return

def ENABLE_RTMP(checkvideo_msg=False):
	enabled = xbmc.getCondVisibility('System.HasAddon(inputstream.rtmp)')
	if not enabled:
		if checkvideo_msg: yes = xbmcgui.Dialog().yesno('رسالة من المبرمج','هذا الفيديو لا يعمل عندك . انت بحاجة إلى إضافة اسمها inputstream.rtmp لكي تستطيع تشغيل فيديوهات نوع rtmp . هل تريد تنصيب وتفعيل هذه الإضافة الآن ؟','','','كلا','نعم')
		else: yes = xbmcgui.Dialog().yesno('رسالة من المبرمج','inputstream.rtmp \n\r هذه ألإضافة عندك غير مفعلة أو غير موجودة . يجب تنصيبها وتفعيلها لكي تعمل عندك فيديوهات نوع rtmp  . هل تريد تنصيب وتفعيل هذه الإضافة الآن ؟','','','كلا','نعم')
		if yes:
			xbmc.executebuiltin('InstallAddon(inputstream.rtmp)',wait=True)
			result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"inputstream.rtmp","enabled":true}}')
			if 'OK' in result: xbmcgui.Dialog().ok('رسالة من المبرمج','تم التنصيب والتفعيل وهذه الإضافة inputstream.rtmp جاهزة للاستخدام')
			else: xbmcgui.Dialog().ok('رسالة من المبرمج','فشل في التنصيب أو التفعيل . البرنامج غير قادر على تنصيب أو تفعيل هذه الإضافة . والحل هو تنصيبها وتفعيلها من خارج البرنامج')
	elif not checkvideo_msg: xbmcgui.Dialog().ok('رسالة من المبرمج','فحص اضافة inputstream.rtmp \n\r هذه ألإضافة عندك موجودة ومفعلة وجاهزة للاستخدام')
	return

def WRITE_TO_SQL3(table,column,data,expiry):
	if expiry==NO_CACHE: return
	dataType = str(type(data))
	#xbmcgui.Dialog().ok(str(data),dataType)
	size = 1
	if   'str' in dataType: size = len(data)
	elif 'list' in dataType: size = len(data)
	elif 'dict' in dataType: size = len(data.values())
	else:
		try:
			html = data.content
			if '___Error___' in html: size = 0
		except: pass
	if size==0: return
	expiry = expiry+now
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	c.execute('CREATE TABLE IF NOT EXISTS '+table+' (expiry,column,data)')
	#data = str(data)
	#data = data.replace('},','},\n')
	text = cPickle.dumps(data)
	compressed = zlib.compress(text)
	t = (expiry,str(column),sqlite3.Binary(compressed))
	c.execute('INSERT INTO '+table+' VALUES (?,?,?)',t)
	conn.commit()
	conn.close()
	return

def READ_FROM_SQL3(table,column):
	if table in ['IPTV_GROUPS','IPTV_ITEMS']: data = []
	elif table in ['IPTV_STREAMS','IMPORT_SECTIONS']: data = {}
	elif table in ['OPENURL']: data = ''
	#elif table in ['OPENURL_REQUESTS']: data = dummy_object()
	#elif table in ['SERVERS']: data = (('',''))
	else: data = None
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	t = (str(column),)
	try:
		c.execute('DELETE FROM '+table+' WHERE expiry<'+str(now))
		c.execute('SELECT data FROM '+table+' WHERE column=?',t)
	except: pass
	rows = c.fetchall()
	conn.commit()
	conn.close()
	if rows:
		compressed = rows[0][0]
		text = zlib.decompress(compressed)
		data = cPickle.loads(text)
		#data = eval(data)
	return data

def DELETE_FROM_SQL3(table,column=None):
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	if column==None: c.execute('DROP TABLE IF EXISTS '+table)
	else:
		t = (str(column),)
		try: c.execute('DELETE FROM '+table+' WHERE column=?',t)
		except: pass
	conn.commit()
	conn.close()
	return

def BUSY_DIALOG(job):
	if kodi_version>17.9: dialog = 'busydialognocancel'
	else: dialog = 'busydialog'
	if job=='start': xbmc.executebuiltin('ActivateWindow('+dialog+')')
	elif job=='stop': xbmc.executebuiltin('Dialog.Close('+dialog+')')
	return

def URLDECODE(url):
	#xbmcgui.Dialog().ok(url,'URLDECODE')
	if '=' in url:
		if '?' in url: url2,filters = url.split('?')
		else: url2,filters = '',url
		filters = filters.split('&')
		data2 = {}
		for filter in filters:
			#xbmcgui.Dialog().ok(filter,str(filters))
			key,value = filter.split('=')
			data2[key] = value
	else: url2,data2 = url,{}
	return url2,data2

def EVAL(html):
	html = html.replace('null','None').replace('u\'','\'')
	html = html.replace('true','True').replace('false','False')
	return eval(html)

def TRANSLATE(text):
	dict = {
	'folder'		:'مجلد'
	,'video'		:'فيديو'
	,'live'			:'قناة'
	,'AKOAM'		:'موقع أكوام القديم'
	,'AKWAM'		:'موقع أكوام الجديد'
	,'ALARAB'		:'موقع كل العرب'
	,'ALFATIMI'		:'موقع المنبر الفاطمي'
	,'ALKAWTHAR'	:'موقع قناة الكوثر'
	,'ALMAAREF'		:'موقع قناة المعارف'
	,'ARABLIONZ'	:'موقع عرب ليونز'
	,'EGYBESTVIP'	:'موقع ايجي بيست vip'
	,'HELAL'		:'موقع هلال يوتيوب'
	,'IFILM'		:'موقع قناة اي فيلم'
	,'IFILM_ARABIC'	:'موقع قناة اي فيلم العربي'
	,'IFILM_ENGLISH':'موقع قناة اي فيلم انكليزي'
	,'PANET'		:'موقع بانيت'
	,'SHAHID4U'		:'موقع شاهد فوريو'
	,'SHOOFMAX'		:'موقع شوف ماكس'
	,'ARABSEED'		:'موقع عرب سييد'
	,'YOUTUBE'		:'موقع يوتيوب'
	,'LIVETV'		:'ملف'
	,'IPTV'			:'ملف'
	,'LIBRARY'		:'ملف'
	#,'EGY4BEST'	:''
	#,'EGYBEST'		:''
	#,'HALACIMA'	:''
	#,'MOVIZLAND'	:''
	#,'SERIES4WATCH':''
	}
	if text in dict.keys(): return dict[text]
	return ''







