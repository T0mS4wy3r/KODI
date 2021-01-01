# -*- coding: utf-8 -*-

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
DIALOG_OK('number of modules imported: '+str(import_count),'average time ms: '+str(totalelpased*1000/20))
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
DIALOG_OK('yes exists: ',list)
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
#DIALOG_OK(kodi_release,str(kodi_version))

logfolder = xbmc.translatePath('special://logpath')
logfile = os.path.join(logfolder,'kodi.log')
oldlogfile = os.path.join(logfolder,'kodi.old.log')

addoncachefolder = os.path.join(xbmc.translatePath('special://temp'),addon_id)
dbfile = os.path.join(addoncachefolder,"webcache_"+addon_version+".db")
lastvideosfile = os.path.join(addoncachefolder,"lastvideos.lst")
lastmenufile = os.path.join(addoncachefolder,"lastmenu.lst")
favouritesfile = os.path.join(addoncachefolder,"favourites.lst")
dummyiptvfile = os.path.join(addoncachefolder,"dummy.iptv")
fulliptvfile = os.path.join(addoncachefolder,"fulliptvfile.m3u")
messagesfile = os.path.join(addoncachefolder,"messages.txt")

addonfolder = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
iconfile = os.path.join(addonfolder,'icon.png')
thumbfile = os.path.join(addonfolder,'thumb.png')
fanartfile = os.path.join(addonfolder,'fanart.jpg')
changelogfile = os.path.join(addonfolder,'changelog.txt')
useragentfile = os.path.join(addonfolder,'resources','useragents.txt')

homefolder = xbmc.translatePath('special://home')
addonsfolder = os.path.join(homefolder,'addons')
settingsfile = os.path.join(homefolder,'userdata','addon_data',addon_id,'settings.xml')

MINUTE = 60
HOUR = 60*MINUTE
DAY = 24*HOUR
MONTH = 30*DAY

NO_CACHE = 0
VERY_SHORT_CACHE = 30*MINUTE
SHORT_CACHE = 2*HOUR
REGULAR_CACHE = 16*HOUR
LONG_CACHE = DAY*3
VERY_LONG_CACHE = DAY*30
PERMANENT_CACHE = MONTH*12

now = int(time.time())

DNS_SERVERS = ['8.8.8.8','1.1.1.1']

WEBSITES = { 'AKOAM'		:['https://akoam.net']
			,'AKWAM'		:['https://akwam.net']
			,'AKOAMCAM'		:['https://akoam.cam']
			,'ALARAB'		:['https://vod.alarab.com']
			,'ALFATIMI'		:['http://alfatimi.tv']
			,'ARABSEED'		:['https://arabseed.net']
			,'ALKAWTHAR'	:['https://www.alkawthartv.com']
			,'ALMAAREF'		:['http://www.almaareftv.com/old','http://www.almaareftv.com']
			,'ARABLIONZ'	:['http://arablionz.com']
			,'BOKRA'		:['http://shoofvod.com','https://shahidlive.co']
			,'HELAL'		:['https://4helal.me']	#4helal.tv #4helal.cc
			,'IFILM'		:['http://ar.ifilmtv.com','http://en.ifilmtv.com','http://fa.ifilmtv.com','http://fa2.ifilmtv.com']
			,'PANET'		:['http://www.panet.co.il']
			,'SHAHID4U'		:['https://shahid4u.com']  #  https://shahid4u.tv  https://shahid4u.net
			,'SHOOFMAX'		:['https://shoofmax.com','https://static.shoofmax.com']
			,'YOUTUBE'		:['https://www.youtube.com']
			,'PYTHON'		:['http://emadmahdi.pythonanywhere.com/listplay','http://emadmahdi.pythonanywhere.com/usagereport','http://emadmahdi.pythonanywhere.com/sendemail','http://emadmahdi.pythonanywhere.com/getmessages']
			,'IPTV'			:['https://nowhere.com']
			,'CIMANOW'		:['https://cima-now.com']
			,'SHIAVOICE'	:['https://shiavoice.com']
			,'KARBALATV'	:['https://karbala-tv.net']
			,'MYCIMA'		:['https://mycima.co']
			#,'EGYBESTVIP'	:['https://egybest.vip']
			#,'EGYBEST'		:['https://egy.best']
			#,'EGY4BEST'	:['https://egybest.vip']
			#,'HALACIMA'	:['https://www.halacima.co']
			#,'MOVIZLAND'	:['https://movizland.online','https://m.movizland.online']
			#,'SERIES4WATCH':['https://series4watch.net']  # 'https://s4w.tv'
			}

def MAIN():
	#DIALOG_OK('MAIN','MAIN')
	LOG_THIS('NOTICE','============================================================================================')
	script_name = 'MAIN'
	if not os.path.exists(dbfile):
		if not os.path.exists(addoncachefolder): os.makedirs(addoncachefolder)
		LOG_THIS('NOTICE','  .  Addon upgrade or Cache delete or new addon install  .  path: [ '+addon_path+' ]')
		CLEAN_KODI_CACHE_FOLDER()
		conn = sqlite3.connect(dbfile)
		conn.close()
		import SERVICES
		SERVICES.KODIEMAD_WEBSITE()
		DIALOG_OK('برنامج عماد للفيديوهات العربية','تم تثبيت أو تحديث الإصدار الجديد لبرنامج عماد للفيديوهات العربية . أو تم مسح كاش البرنامج . الآن سيقوم البرنامج ببعض الفحوصات لضمان عمل البرنامج بصورة صحيحة ومتكاملة')
		ENABLE_MPD(False)
		ENABLE_RTMP(False)
		SERVICES.CHECK_INSTALLED_REPOSITORIES(False)
		SERVICES.HTTPS_TEST(False)
		import IPTV
		if IPTV.isIPTVFiles(False):
			DIALOG_OK('رسالة من المبرمج','إذا كنت تستخدم خدمة IPTV الموجودة في هذا البرنامج فسوف يقوم البرنامج الآن أوتوماتيكيا بجلب ملفات IPTV جديدة')
			IPTV.CREATE_STREAMS(False)
	type,name99,url99,mode,image99,page99,text,context = EXTRACT_KODI_PATH()
	#DIALOG_OK(context,'')
	mode0 = int(mode)
	mode1 = int(mode0%10)
	mode2 = int(mode0/10)
	#message += '\n'+'Label:['+menu_label+']   Path:['+menu_path+']'
	#DIALOG_OK('['+menu_path+']','['+addon_path+']')
	#DIALOG_OK('['+menu_label+']','['+menu_path+']')
	if mode0==260: message = '  Version: [ '+addon_version+' ]  Kodi: [ '+kodi_release+' ]'
	else:
		menu_label2 = menu_label.replace('   ','  ').replace('   ','  ').replace('   ','  ')
		menu_path2 = menu_path.replace('   ','  ').replace('   ','  ').replace('   ','  ')
		message = '  Label: [ '+menu_label2+' ]  Mode: [ '+mode+' ]  Path: [ '+menu_path2+' ]'
	LOG_THIS('NOTICE',LOGGING(script_name)+message)
	if '_' in context: context1,context2 = context.split('_',1)
	else: context1,context2 = context,''
	if context1=='6':
		if context2=='': DIALOG_NOTIFICATION('يرجى الانتظار','جاري فحص ملف التحميل',sound=False)
		results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text,context)
		xbmc.executebuiltin("Container.Refresh")
		#EXIT_PROGRAM('LIBRARY-MAIN-1st')
		return
	elif context1 in ['1','2','3','4','5'] and context2!='':
		import FAVOURITES
		FAVOURITES.FAVOURITES_DISPATCHER(context)
		#"Container.Refresh" used because there is no addon_handle number to use for ending directory
		#"Container.Update" used to open a menu list using specific addon_path
		#xbmc.executebuiltin("Container.Update("+sys.argv[0]+addon_path.split('&context=')[0]+'&context=0'+")")
		#DIALOG_OK('[1111111111 '+context1+']','['+context2+']')
		xbmc.executebuiltin("Container.Refresh")
		#DIALOG_OK('[2222222222 '+context1+']','['+context2+']')
		#EXIT_PROGRAM('LIBRARY-MAIN-2nd')
		return
	if mode0==266:
		import MENUS
		MENUS.DELETE_LAST_VIDEOS_MENU(text)
		xbmc.executebuiltin("Container.Refresh")
		#EXIT_PROGRAM('LIBRARY-MAIN-3rd')
		return
	# '_REMEMBERRESULTS_'	use file to read/write the previous menu list
	# '_FORGETRESULTS_'		no go back to the previous menu list
	YOUTUBE_CHANNELS_SEARCH = mode0==145
	GLOBAL_SEARCH = mode0==262
	SITES_SEARCH = mode0 in [19,29,39,49,59,69,79,99,119,139,149,209,229,239,249,259,309,319,329]
	SEARCH_MODES = SITES_SEARCH or YOUTUBE_CHANNELS_SEARCH
	RANDOM_MODES = mode2==16 and mode0!=160
	if SEARCH_MODES or RANDOM_MODES:
		name88 = name99.replace('[COLOR FFC89008]','').replace('[/COLOR]','')
		if RANDOM_MODES: cond1 = menu_label in ['..','Main Menu']
		elif SEARCH_MODES: cond1 = menu_label!=name88
		#previous_path = xbmc.getInfoLabel('ListItem.FolderPath')
		#previous_path = unquote(previous_path)
		#DIALOG_OK(str(menu_label),str(name))
		#if '_REMEMBERRESULTS_' in text and (menu_label!=name or menu_label in ['..','Main Menu']) and os.path.exists(lastmenufile):
		if '_REMEMBERRESULTS_' in text and cond1 and os.path.exists(lastmenufile):
			LOG_THIS('NOTICE','  .  Reading last menu   Path: [ '+addon_path+' ]')
			with open(lastmenufile,'r') as f: oldFILE = f.read()
			menuItemsLIST[:] = eval(oldFILE)
		else:
			LOG_THIS('NOTICE','  .  Writing last menu   Path: [ '+addon_path+' ]')
			results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text,context)
			newFILE = str(menuItemsLIST)
			with open(lastmenufile,'w') as f: f.write(newFILE)
	else: results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text,context)
	# kodi defaults: succeeded,updateListing,cacheToDisc = True,False,True
	# updateListing = True => means this list is temporary and will be overwritten by the next list
	# updateListing = False => means this list is permanent and the new list will generate new menu
	succeeded,updateListing,cacheToDisc = True,False,True
	if '_FORGETRESULTS_' in text: updateListing = True
	SITES_MODES = mode2 in [1,2,3,4,5,6,7,9,11,13,14,20,22,24,25,30,31,32]
	IPTV_MODES = mode2==23 and text!=''
	if type=='folder' and menu_label!='..' and (SITES_MODES or IPTV_MODES):
		ADD_TO_LAST_VIDEO_FILES()
	if type=='folder' and addon_handle>-1:
		KodiMenuList = []
		for menuItem in menuItemsLIST:
			kodiMenuItem = getKodiMenuItem(menuItem)
			KodiMenuList.append(kodiMenuItem)
		addItems_succeeded = xbmcplugin.addDirectoryItems(addon_handle,KodiMenuList)
		xbmcplugin.setContent(addon_handle,'tvshows')
		xbmcplugin.endOfDirectory(addon_handle,succeeded,updateListing,cacheToDisc)
	return

def MAIN_DISPATCHER(type,name,url,mode,image,page,text,context):
	mode = int(mode)
	mode2 = int(mode/10)
	#DIALOG_OK(str(mode),str(mode2))
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
	elif mode2==27: import FAVOURITES 	; results = FAVOURITES.MAIN(mode,context)
	elif mode2==28: import IPTV 		; results = IPTV.MAIN(mode,url,text,type)
	elif mode2==29: import YTB_CHANNELS	; results = YTB_CHANNELS.MAIN(mode,url,page,text)
	elif mode2==30: import CIMANOW		; results = CIMANOW.MAIN(mode,url,text)
	elif mode2==31: import SHIAVOICE	; results = SHIAVOICE.MAIN(mode,url,text)
	elif mode2==32: import KARBALATV	; results = KARBALATV.MAIN(mode,url,text)
	elif mode2==33: import DOWNLOAD		; results = DOWNLOAD.MAIN(mode,url,context)
	elif mode2==34: import SERVICES 	; results = SERVICES.MAIN(mode,text)
	elif mode2==35: import AKOAMCAM		; results = AKOAMCAM.MAIN(mode,url,text)
	elif mode2==36: import MYCIMA		; results = MYCIMA.MAIN(mode,url,text)
	elif mode2==37: import BOKRA		; results = BOKRA.MAIN(mode,url,text)
	return results

def LOG_MENU_LABEL(script_name,label,mode,path):
	id = '	[ '+addon_name.upper()+'-'+addon_version+'-'+script_name+' ]'
	message = id+'	Label: [ '+label+' ]	Mode: [ '+str(mode)+' ]	Path: [ '+path+' ]'
	xbmc.log(message, level=xbmc.LOGNOTICE)
	return

def LOG_THIS(level,message):
	#xbmc.log('EMAD 111'+message+'EMAD 222', level=xbmc.LOGNOTICE)
	message = message.replace('[COLOR FFFFFF00]','').replace('[COLOR FFC89008]','')
	message = message.replace('[/COLOR]','')
	if level=='ERROR':
		loglevel = xbmc.LOGERROR
		lines = message.strip('.   ').split('   ')
	else:
		loglevel = xbmc.LOGNOTICE
		lines = message.split('    ')
	#message = message.replace('   ','\t')
	tab = '    '
	tabs = tab+tab+tab
	shift = tabs+tab+'  '
	if kodi_version>17.999: shift = shift+'           '
	#DIALOG_OK(str(kodi_version),'')
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
	#DIALOG_OK(str(function_name),'')
	#if function_name=='<module>': return '.  [  '+script_name+'-'+function_name+' ]'
	#function_name = 'MAIN'
	if script_name=='MAIN' and function_name=='MAIN':
		return '[ '+addon_name.upper()+'-'+addon_version+'-'+script_name+'-'+function_name+' ]'
	return '.   '+function_name

class CustomPlayer(xbmc.Player):
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
	def __init__(self,showDialogs=False,logErrors=True):
		self.showDialogs = showDialogs
		self.logErrors = logErrors
		self.finishedLIST,self.failedLIST = [],[]
		self.statusDICT,self.resultsDICT = {},{}
		self.starttimeDICT,self.finishtimeDICT,self.elpasedtimeDICT = {},{},{}
	def start_new_thread(self,id,func,*args):
		id = str(id)
		self.statusDICT[id] = 'running'
		if self.showDialogs: DIALOG_NOTIFICATION('',id,sound=False)
		thread.start_new_thread(self.run,(id,func,args))
	def run(self,id,func,args):
		id = str(id)
		self.starttimeDICT[id] = time.time()
		#LOG_THIS('NOTICE','thread started id: '+id)
		try:
			self.resultsDICT[id] = func(*args)
			self.finishedLIST.append(id)
			self.statusDICT[id] = 'finished'
			#LOG_THIS('NOTICE','thread finished id: '+id)
		except Exception as err:
			#LOG_THIS('NOTICE','thread failed id: '+id)
			if self.logErrors:
				errortrace = traceback.format_exc()
				sys.stderr.write(errortrace)
				#traceback.print_exc(file=sys.stderr)
			self.failedLIST.append(id)
			self.statusDICT[id] = 'failed'
		self.finishtimeDICT[id] = time.time()
		self.elpasedtimeDICT[id] = self.finishtimeDICT[id] - self.starttimeDICT[id]
	def wait_finishing_all_threads(self):
		while 'running' in self.statusDICT.values(): time.sleep(1.000)

def SHOW_NETWORK_ERRORS(code,reason,source,showDialogs):
	if '-' in source: site = source.split('-',1)[0]
	else: site = source
	#if code==104: DIALOG_OK('لديك خطأ اسبابه كثيرة','يرجى منك التواصل مع المبرمج عن طريق هذا الرابط','https://github.com/emadmahdi/KODI/issues')
	dns = (code in [7,10054,11001])
	blocked1 = (code in [0,104,10061,111])
	blocked2 = ('Blocked by Cloudflare' in reason)
	blocked3 = ('Blocked by 5 seconds browser check' in reason)
	settings = xbmcaddon.Addon(id=addon_id)
	proxy_status = settings.getSetting('proxy.status')
	dns_status = settings.getSetting('dns.status')
	if proxy_status=='ASK' or dns_status=='ASK':
		messageARABIC = '[COLOR FFFFFF00]هل تريد أن يحاول البرنامج إصلاح المشكلة ؟[/COLOR]'
	else: messageARABIC = ''
	messageARABIC += ' فشل بسحب الصفحة من الأنترنيت'
	messageENGLISH = 'Error '+str(code)+': '+reason
	if blocked1 or blocked2 or blocked3:
		messageARABIC += ' . الموقع فيه حجب ضد كودي مصدره الأنترنيت الخاص بك'
	if dns:
		messageARABIC += ' . لديك خطأ DNS ومعناه تعذر ترجمة اسم الموقع إلى رقمه'
	LOG_THIS('ERROR',LOGGING(script_name)+'   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   messageARABIC: [ '+messageARABIC+' ]]   messageENGLISH: [ '+messageENGLISH+' ]')
	#DIALOG_OK(proxy_status,dns_status)
	if proxy_status=='ASK' or dns_status=='ASK':
		trytofix = DIALOG_YESNO(site+'   '+TRANSLATE(site),messageARABIC,messageENGLISH,'','كلا','نعم')
	else:
		trytofix = False
		if showDialogs: DIALOG_OK(site+'   '+TRANSLATE(site),messageARABIC,messageENGLISH)
	return trytofix
	"""
	if dns or blocked1 or blocked2 or blocked3:
		block_meessage = 'نوع من الحجب ضد كودي مصدره الأنترنيت الخاص بك.'
		if showDialogs: block_meessage += ' هل تريد تفاصيل اكثر ؟'
		if dns:
			messageARABIC = 'لديك خطأ DNS ومعناه تعذر ترجمة اسم الموقع إلى رقمه'
			messageARABIC += ' والسبب قد يكون '+block_meessage
		else: messageARABIC = 'هذا الموقع فيه '+block_meessage
		LOG_THIS('ERROR',LOGGING(script_name)+'   Source: [ '+source+' ]   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   messageARABIC: [ '+messageARABIC+' ]]   messageENGLISH: [ '+messageENGLISH+' ]')
		if showDialogs:
			yes = DIALOG_YESNO(site+'   '+TRANSLATE(site),messageARABIC,messageENGLISH,'','كلا','نعم')
			if yes==1: import SERVICES ; SERVICES.MAIN(195)
	elif showDialogs:
		messageARABIC2 = messageARABIC+' . هل تريد معرفة الأسباب والحلول ؟'
		yes = DIALOG_YESNO(site+'   '+TRANSLATE(site),messageARABIC2,messageENGLISH,'','كلا','نعم')
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
			DIALOG_TEXTVIEWER('فشل في سحب الصفحة من الأنترنيت',messageDETAILS)
	"""

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
				,'LIBRARY-SEND_ANALYTICS_EVENT-1st'
				,'LIBRARY-HTTPS-1st'
				,'LIBRARY-GET_PROXIES_LIST-1st'
				,'SERVICES-TEST_ALL_WEBSITES-1st'
				,'SERVICES-TEST_ALL_WEBSITES-2nd'
				,'SERVICES-GET_LATEST_VERSION_NUMBERS-1st'
				,'IPTV-CHECK_ACCOUNT-1st'
				,'IPTV-CHECK_ACCOUNT-1st'
				,'EGYBESTVIP-PLAY-2nd'
				,'EGYBESTVIP-PLAY-3rd'
				,'HELAL-ITEMS-1st'
				,'YOUTUBE-RANDOM_USERAGENT-1st'
				,'MENUS-SHOW_MESSAGES-1st'
				,'SERVICES-ANALYTICS_REPORT-1st'
				]

def EXIT_IF_SOURCE(source,code,reason,showDialogs,allow_dns_fix,allow_proxy_fix):
	# To force exit use
	# EXIT_IF_SOURCE('','','','')
	if showDialogs and (allow_dns_fix or allow_proxy_fix): SHOW_NETWORK_ERRORS(code,reason,source,showDialogs)
	if source not in NO_EXIT_LIST and code!=200:
		LOG_THIS('ERROR',LOGGING(script_name)+'   Forced Exit   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]')
		raise SystemError('Forced Exit')
		#sys.exit('Forced Exit')
	return
	#condition1 = source not in NO_EXIT_LIST and 'RESOLVERS' not in source and 'MENU-1st' not in source
	#condition2 = 'Blocked by Cloudflare' in reason
	#condition3 = 'Blocked by 5 seconds browser check' in reason

def CLEAN_KODI_CACHE_FOLDER(exceptionLIST1=[]):
	exceptionLIST2 = [lastvideosfile,favouritesfile,dummyiptvfile,fulliptvfile]
	exceptionLIST = exceptionLIST1+exceptionLIST2
	#delete = DIALOG_YESNO('مسح ملفات الفيديو القديمة','سوف يتم ايضا مسح ملفات الفيديو القديمة التي انت انزلتها باستخدام هذا البرنامج . هل تريد مسحها ام لا ؟','','','كلا','نعم')
	for filename in os.listdir(addoncachefolder):
		#if not delete and 'file_' in filename: continue
		if 'file_' in filename: continue
		filename_full = os.path.join(addoncachefolder,filename)
		if filename_full not in exceptionLIST:
			try: os.remove(filename_full)
			except: pass
	return

contentsDICT = {}
menuItemsLIST = []

def addMenuItem(type,name,url,mode='',image='',page='',text='',context=''):
	name = name.replace('\r','').replace('\n','').replace('\t','')
	url = url.replace('\r','').replace('\n','').replace('\t','')
	if '___' in name: website,name = name.split('___',1)
	else: website,name = '',name
	if type=='folder' and website!='':
		nameonly = name
		if nameonly=='': nameonly = '....'
		elif nameonly.count('_')>1: nameonly = nameonly.split('_',2)[2]
		nameonly = nameonly.replace('ـ','').replace('  ',' ').replace('ة','ه').replace('و ','و')
		nameonly = nameonly.replace('أ','ا').replace('إ','ا').replace('آ','ا')
		nameonly = nameonly.replace('لأ','لا').replace('لإ','لا').replace('لآ','لا')
		list1 = ['العاب','خيال','البوم','الان','اطفال','حاليه','الغاز']
		if not any(value in nameonly for value in list1): nameonly = nameonly.replace('ال','')
		nameonly = nameonly.strip(' ')
		nameonly = nameonly.replace('اخري','اخرى').replace('اجنبى','اجنبي').replace('عائليه','عائلي')
		nameonly = nameonly.replace('اجنبيه','اجنبي').replace('عربيه','عربي').replace('رومانسيه','رومانسي')
		nameonly = nameonly.replace(' | افلام اون لاين','').replace('انيميشن','انميشن').replace('غربيه','غربي')
		nameonly = nameonly.replace('تاريخي','تاريخ').replace('خيال علمي','خيال').replace('موسيقيه','موسيقى')
		nameonly = nameonly.replace('هندى','هندي').replace('هنديه','هندي').replace('وثائقيه','وثائقي')
		nameonly = nameonly.replace('تليفزيونيه','تلفزيون').replace('تلفزيونيه','تلفزيون')
		nameonly = nameonly.replace('الحاليه','حاليه').replace('موسیقی','موسيقى').replace('الانمي','انمي')
		nameonly = nameonly.replace('المسلسلات','مسلسلات').replace('البرامج','برامج')
		nameonly = nameonly.replace('حروب','حرب').replace('الاناشيد','اناشيد')
		website = TRANSLATE(website)
		if nameonly not in contentsDICT.keys(): contentsDICT[nameonly] = {}
		contentsDICT[nameonly][website] = [type,name,url,mode,image,page,text,context]
	menuItemsLIST.append([type,name,url,mode,image,page,text,context])
	return

def getKodiMenuItem(menuItem):
	type,name,url,mode,image,text1,text2,context = menuItem
	if type=='folder': start1,start2 = ';',','
	else: start1,start2 = escapeUNICODE('\u02d1'),' '
	name2 = re.findall('&&_(\D\D\w)__MOD_(.*?)&&','&&'+name+'&&',re.DOTALL)
	if name2: name = start1+'[COLOR FFC89008]'+name2[0][0]+'  [/COLOR]'+name2[0][1]
	name2 = re.findall('&&_(\D\D\w)_(.*?)&&','&&'+name+'&&',re.DOTALL)
	if name2: name = start2+'[COLOR FFC89008]'+name2[0][0]+'  [/COLOR]'+name2[0][1]
	path = 'plugin://'+addon_id+'/?type='+type.strip(' ')
	path = path+'&mode='+str(mode).strip(' ')
	if type=='folder' and text1!='': path = path+'&page='+quote(text1.strip(' '))
	if context!='': path = path+'&context='+context.strip(' ')
	if name!='': path = path+'&name='+quote(name)#.strip(' '))
	if text2!='': path = path+'&text='+quote(text2.strip(' '))
	listitem = xbmcgui.ListItem(name)
	if image!='':
		listitem.setArt({'icon':image,'thumb':image,'fanart':'',})
		path = path+'&image='+quote(image.strip(' '))
	else:
		listitem.setArt({'icon':iconfile,'thumb':thumbfile,'fanart':'',})
	#listitem.setInfo(type="video",infoLabels={"Title":name})
	if url!='': path = path+'&url='+quote(url.strip(' '))
	context_menu = []
	if mode in [235,238] and type=='live' and 'EPG' in context:
		run_path = 'plugin://'+addon_id+'?mode=238&text=SHORT_EPG&url='+url
		run_text = '[COLOR FFFFFF00]البرامج القادمة[/COLOR]'
		run_item = (run_text,'XBMC.RunPlugin('+run_path+')')
		context_menu.append(run_item)
	elif mode in [265]:
		import MENUS
		length = MENUS.LAST_VIDEOS_MENU(text2,True)
		if length>0:
			run_path = 'plugin://'+addon_id+'?mode=266&text='+text2
			run_text = '[COLOR FFFFFF00]مسح قائمة آخر 50 '+TRANSLATE(text2)+'[/COLOR]'
			run_item = (run_text,'XBMC.RunPlugin('+run_path+')')
			context_menu.append(run_item)
	import FAVOURITES
	context_menu += FAVOURITES.GET_FAVOURITES_CONTEXT_MENU(path)
	if type=='video' and mode!=331:
		run_path = path+'&context=6'
		run_text = '[COLOR FFFFFF00]تحميل ملف الفيديو[/COLOR]'
		run_item = (run_text,'XBMC.RunPlugin('+run_path+')')
		context_menu.append(run_item)
	if mode==331:
		context_menu.append(('[COLOR FFFFFF00]حذف ملف الفيديو[/COLOR] ','XBMC.RunPlugin('+path+'&context=6_REMOVE'+')'))
	listitem.addContextMenuItems(context_menu)
	if type in ['link','live']: isFolder = False
	elif type=='video':
		isFolder = False
		listitem.setInfo('video',{'mediatype':'video'})
		if text1!='':
			duration = '0:0:0:0:0:'+text1
			dummy,days,hours,minutes,seconds = duration.rsplit(':',4)
			duration2 = int(days)*24*HOUR+int(hours)*HOUR+int(minutes)*60+int(seconds)
			listitem.setInfo('video',{'duration':duration2})
		listitem.setProperty('IsPlayable','true')
		xbmcplugin.setContent(addon_handle,'videos')
	elif type=='folder':
		isFolder = True
	#listitem.setInfo(type="video",infoLabels={"Title":name})
	#xbmcplugin.addDirectoryItem(handle=addon_handle,url=path,listitem=listitem,isFolder=isFolder)
	return (path,listitem,isFolder)

def EXTRACT_KODI_PATH(path=''):
	args1 = {'type':'','mode':'','url':'','text':'','page':'','name':'','image':'','context':''}
	if path=='': path = addon_path
	if '?' in path: path = path.split('?',1)[1]
	url2,args2 = URLDECODE(path)
	args = dict(args1.items()+args2.items())
	mode = args['mode']
	url = unquote(args['url'])
	text = unquote(args['text'])
	page = unquote(args['page'])
	type = unquote(args['type'])
	name = unquote(args['name'])
	image = unquote(args['image'])
	context = args['context']
	#name = xbmc.getInfoLabel('ListItem.Label')
	#image = xbmc.getInfoLabel('ListItem.Icon')
	if mode=='': type = 'folder' ; mode = '260'
	return type,name,url,mode,image,page,text,context

def OPENURL_REQUESTS_CACHED(expiry,method,url,data,headers,allow_redirects,showDialogs,source,allow_dns_fix=True,allow_proxy_fix=True):
	#response = OPENURL_REQUESTS_PROXIES(method,url,data,headers,allow_redirects,showDialogs,source)
	if expiry==0: return OPENURL_REQUESTS(method,url,data,headers,allow_redirects,showDialogs,source,allow_dns_fix,allow_proxy_fix)
	response = READ_FROM_SQL3('OPENURL_REQUESTS',[method,url,data,headers,allow_redirects,showDialogs,source])
	if response: return response
	#DIALOG_OK('start',url)
	response = OPENURL_REQUESTS(method,url,data,headers,allow_redirects,showDialogs,source,allow_dns_fix,allow_proxy_fix)
	#DIALOG_OK('finish',url)
	code = response.code
	reason = response.reason
	if response.succeeded:
		WRITE_TO_SQL3('OPENURL_REQUESTS',[method,url,data,headers,allow_redirects,showDialogs,source],response,expiry)
	return response

def OPENURL_PROXY(proxy,method,url,data,headers,allow_redirects,showDialogs,source):
	proxy_host,proxy_port = proxy.split(':')
	#DIALOG_NOTIFICATION('مشكلة إنترنيت . سأحاول إصلاحها','سأجرب '+name,sound=False,time=2000)
	#LOG_THIS('NOTICE',LOGGING(script_name)+'   Trying '+name+' server   Proxy: [ '+proxy+' ]   URL: [ '+url+' ]')
	url = url+'||MyProxyUrl='+proxy
	response = OPENURL_REQUESTS(method,url,data,headers,allow_redirects,showDialogs,source,True,True)
	if url in response.content: response.succeeded = False
	if not response.succeeded:
		#LOG_THIS('NOTICE',LOGGING(script_name)+'   Failed '+name+' server   Proxy: [ '+proxy+' ]   URL: [ '+url+' ]')
		raise SystemError('HTTP Request Failure')
	#else: LOG_THIS('NOTICE',LOGGING(script_name)+'   Succeeded:   Proxy: [ '+proxy+' ]   URL: [ '+url+' ]')
	return response

def GET_PROXIES_LIST(url):
	url = url.decode('base64')
	#DIALOG_OK(url,'GET_PROXIES_LIST')
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url,'','',True,False,'LIBRARY-GET_PROXIES_LIST-1st',True,False)
	proxies2 = []
	if response.succeeded:
		html = response.content
		proxies = html.replace('\r','').strip('\n').split('\n')
		proxies2 = []
		for proxy in proxies: 
			if proxy.count('.')==3: proxies2.append(proxy)
	return proxies2

def OPENURL_REQUESTS_PROXIES(*args):
	pubproxy = 'aHR0cDovLzQ1LjMzLjE3LjEyNy9hcGkvcHJveHk/dHlwZT1odHRwJnNwZWVkPTEwJmxhc3RfY2hlY2s9MTAmaHR0cHM9dHJ1ZSZwb3N0PXRydWUmbGltaXQ9MTAmZm9ybWF0PXR4dCZsZXZlbD1hbm9ueW1vdXM='
	proxyscrape = 'aHR0cHM6Ly9hcGkucHJveHlzY3JhcGUuY29tLz9yZXF1ZXN0PWRpc3BsYXlwcm94aWVzJnByb3h5dHlwZT1odHRwJnRpbWVvdXQ9MTAwMDAmc3NsPXllcyZhbm9ueW1pdHk9YW5vbnltb3Vz'
	proxies_1 = GET_PROXIES_LIST(pubproxy)
	proxies_2 = GET_PROXIES_LIST(proxyscrape)
	proxiesLIST = proxies_1+proxies_2
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Got proxies list   1st+2nd: [ '+str(len(proxies_1))+'+'+str(len(proxies_2))+' ]')
	response = dummy_object()
	response.succeeded = False
	if proxiesLIST:
		totla_count = len(proxiesLIST)
		trying_count = len(proxiesLIST)
		if totla_count>=trying_count: proxiesLIST2 = random.sample(proxiesLIST,trying_count)
		else: proxiesLIST2 = random.sample(proxiesLIST,totla_count)
		id,timeout = 0,10
		threads = CustomThread(False,False)
		#threads.wait_finishing_all_threads()
		t1 = time.time()
		while time.time()-t1<=timeout and not threads.finishedLIST:
			if id<trying_count:
				proxy = proxiesLIST2[id]
				threads.start_new_thread(id,OPENURL_PROXY,proxy,*args)
				id += 1
			time.sleep(1)
			#LOG_THIS('NOTICE',LOGGING(script_name)+'   Trying:   Proxy: [ '+proxy+' ]')
		finishedLIST = threads.finishedLIST
		if finishedLIST:
			resultsDICT = threads.resultsDICT
			fastest_id = finishedLIST[0]
			response = resultsDICT[fastest_id]
			proxy = proxiesLIST2[int(fastest_id)]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Success:   Proxy: [ '+proxy+' ]')
		#LOG_THIS('NOTICE','proxiesLIST2 :: '+str(proxiesLIST2))
		#LOG_THIS('NOTICE','proxiesLIST :: '+str(proxiesLIST))
		#LOG_THIS('NOTICE','finishedLIST :: '+str(threads.finishedLIST))
		#LOG_THIS('NOTICE','failedLIST :: '+str(threads.failedLIST))
		#LOG_THIS('NOTICE','resultsDICT :: '+str(threads.resultsDICT))
		#LOG_THIS('NOTICE','elpasedtimeDICT :: '+str(threads.elpasedtimeDICT))
		#LOG_THIS('NOTICE','sortedLIST :: '+str(sortedLIST))
		#LOG_THIS('NOTICE',LOGGING(script_name)+'   '+fastest_proxy+'   '+str(sortedLIST))
	return response

"""
# test proxies one after the other not all at the same time
# in the settings it save the last working proxy
def OPENURL_REQUESTS_PROXIES(method,url,data,headers,allow_redirects,showDialogs,source):
	settings = xbmcaddon.Addon(id=addon_id)
	last_proxy = settings.getSetting('proxy.last')
	if last_proxy!='':
		response = OPENURL_PROXY(method,url,data,headers,allow_redirects,showDialogs,source,last_proxy,'البروكسي القديم')
		if response.succeeded: return response
	proxies = READ_FROM_SQL3('SETTINGS','PROXIES')
	#proxies = ['11.12.3.4:8969','22.2.3.4:5929']
	if not proxies:
		pubproxy = 'aHR0cDovLzQ1LjMzLjE3LjEyNy9hcGkvcHJveHk/dHlwZT1odHRwJnNwZWVkPTEwJmxhc3RfY2hlY2s9MTAmaHR0cHM9dHJ1ZSZwb3N0PXRydWUmbGltaXQ9MTAmZm9ybWF0PXR4dCZsZXZlbD1hbm9ueW1vdXM='
		proxyscrape = 'aHR0cHM6Ly9hcGkucHJveHlzY3JhcGUuY29tLz9yZXF1ZXN0PWRpc3BsYXlwcm94aWVzJnByb3h5dHlwZT1odHRwJnRpbWVvdXQ9MTAwMDAmc3NsPXllcyZhbm9ueW1pdHk9YW5vbnltb3Vz'
		proxies_1 = GET_PROXIES_LIST(pubproxy)
		proxies_2 = GET_PROXIES_LIST(proxyscrape)
		proxies = proxies_1+proxies_2
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Got new proxies   1st+2nd: [ '+str(len(proxies_1))+'+'+str(len(proxies_2))+' ]')
	#for i in range(9): random.shuffle(proxies)
	response = dummy_object()
	response.succeeded = False
	count = len(proxies)
	if count>=6: proxies2 = random.sample(proxies,6)
	else: proxies2 = random.sample(proxies,count)
	for i in range(len(proxies2)):
		proxy = proxies2[i]
		response = OPENURL_PROXY(method,url,data,headers,allow_redirects,showDialogs,source,proxy,'بروكسي جديد رقم [ '+str(i+1)+' ]')
		if response.succeeded: break
		else: proxies.remove(proxy)
	failed = count-len(proxies)
	if response.succeeded: settings.setSetting('proxy.last',proxy)
	else: settings.setSetting('proxy.last','')
	DELETE_FROM_SQL3('SETTINGS','PROXIES')
	if proxies: WRITE_TO_SQL3('SETTINGS','PROXIES',proxies,SHORT_CACHE)
	return response
"""

def OPENURL_CACHED(expiry,url,data,headers,showDialogs,source):
	#DIALOG_OK('OPENURL_CACHED 111','')
	if expiry==0: return OPENURL(url,data,headers,showDialogs,source)
	html = READ_FROM_SQL3('OPENURL',[url,data,headers,showDialogs,source])
	if html: return html
	html = OPENURL(url,data,headers,showDialogs,source)
	if '___Error___' not in html:
		WRITE_TO_SQL3('OPENURL',[url,data,headers,showDialogs,source],html,expiry)
	return html

def OPENURL(url,data,headers,showDialogs,source):
	#DIALOG_OK(str(type(data)),str(data))
	if data=='' or 'dict' in str(type(data)): method = 'GET'
	else:
		method = 'POST'
		data = unquote(data)
		items = data.split('&')
		data = {}
		for item in items:
			key,value = item.split('=',1)
			data[key] = value
	response = OPENURL_REQUESTS(method,url,data,headers,True,showDialogs,source)
	html = str(response.content)
	return html

class dummy_object(): pass

def USE_DNS_SERVER(connection,dns_server):
	original_create_connection = connection.create_connection
	def patched_create_connection(address,*args,**kwargs):
		host,port = address
		ip = DNS_RESOLVER(host,dns_server)
		if ip: host = ip[0]
		else:
			DNS_SERVERS.remove(dns_server)
			dns_server2 = DNS_SERVERS[0]
			LOG_THIS('NOTICE',LOGGING(script_name)+'   DNS failed   Will try the other DNS:[ '+dns_server2+' ]   Host:[ '+str(host)+' ]')
			ip = DNS_RESOLVER(host,dns_server2)
			if ip: host = ip[0]
		#DIALOG_OK(str(host),str(ip))
		address = (host,port)
		return original_create_connection(address,*args,**kwargs)
	connection.create_connection = patched_create_connection
	return original_create_connection

def OPENURL_REQUESTS(method,url,data,headers,allow_redirects,showDialogs,source,allow_dns_fix=True,allow_proxy_fix=True):
	if data=='': data = {}
	if headers=='': headers = {'User-Agent':None}
	if allow_redirects=='': allow_redirects = True
	if showDialogs=='': showDialogs = True
	#url = url + '||MyProxyUrl=http://188.166.59.17:8118'
	import requests
	url2,proxyurl,dnsurl,sslurl = EXTRACT_URL(url)
	settings = xbmcaddon.Addon(id=addon_id)
	dns_server = settings.getSetting('dns.server')
	dns_status = settings.getSetting('dns.status')
	proxy_status = settings.getSetting('proxy.status')
	if dns_status=='':
		dns_status = 'ASK'
		dns_server = DNS_SERVERS[0]
		settings.setSetting('dns.status',dns_status)
		settings.setSetting('dns.server',dns_server)
	if proxy_status in ['','ENABLED','DISABLED']:
		proxy_status = 'ASK'
		settings.setSetting('proxy.status',proxy_status)
	if dnsurl=='': dnsurl = dns_server
	if dnsurl==None and dns_status=='ALWAYS' and allow_dns_fix: dnsurl = dns_server
	if 'IFILM' in source: timeout = 20
	elif proxyurl!=None: timeout = 10
	else: timeout = 5
	if proxyurl!=None:
		proxies = {"http":proxyurl,"https":proxyurl}
		proxy_server = proxyurl
	else: proxies,proxy_server = {},''
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Proxy:[ '+proxy_status+'='+proxy_server+' ]   DNS:[ '+dns_status+'='+dns_server+' ]   SSL:[ '+str(sslurl!=None)+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
	if sslurl!=None: DIALOG_NOTIFICATION('تفعيل تشفير SSL','لإصلاح مشكلة الإنترنيت',sound=False,time=2000)
	if dnsurl!=None and dns_status!='STOP':
		DIALOG_NOTIFICATION('تفعيل DNS رقم: '+dnsurl,'لإصلاح مشكلة الإنترنيت',sound=False,time=2000)
		import urllib3.util.connection as connection
		original_create_connection = USE_DNS_SERVER(connection,dns_server)
		#DIALOG_OK(str(type(dns_server)),str(dns_server))
	if sslurl!=None: verify = True
	else: verify = False
	"""
	if 'pythonanywhere' in url2:
		try:
			sock22 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result22 = sock22.connect_ex(('emadmahdi.pythonanywhere.com',80))
		except:
	"""
	try:
		if method=='POST' and allow_redirects==True:
			url3 = url2
			for i in range(10):
				#DIALOG_OK(url3,'11111')
				response = requests.request(method,url3,data=data,headers=headers,verify=verify,allow_redirects=False,timeout=timeout,proxies=proxies)
				#DIALOG_OK(url3,'22222')
				if response.status_code<300 or response.status_code>399: break
				url3 = response.headers['Location']
		else: response = requests.request(method,url2,data=data,headers=headers,verify=verify,allow_redirects=allow_redirects,timeout=timeout,proxies=proxies)
		code,reason = response.status_code,response.reason
		response.raise_for_status()
		succeeded = True
	except requests.exceptions.HTTPError as err:
		#DIALOG_OK(url3,'44444')
		# it works only if response.raise_for_status() is executed
		# code,reason = re.findall('(\d+).*?: (.*?):',err.message)[0]
		succeeded = False
	except requests.exceptions.Timeout as err:
		#DIALOG_OK(url3,'55555')
		reason,code = str(err.message).split(': ')[1],-1
		succeeded = False
	except requests.exceptions.ConnectionError as err:
		#DIALOG_OK(str(err.message),str(err.message[0]))
		#LOG_THIS('ERROR',str(err.message))
		reason,code = 'Unknown Error',-1
		try:
			error = err.message[0]
			reason,code = error,-1
			if 'Errno' in error: code,reason = re.findall("\[Errno (\d+)\] (.*?)'",error)[0]
			elif ', error(' in error: code,reason = re.findall(", error\((\d+), '(.*?)'",error)[0]
			elif error.count(':')>=2: reason,code = re.findall(': (.*?):.*?(\d+)',error)[0]
			#DIALOG_OK(str(code),reason)
		except: pass
		succeeded = False
	except requests.exceptions.RequestException as err:
		#DIALOG_OK(url3,'77777')
		reason,code = err.message,-1
		succeeded = False
	except:
		#err_class = sys.exc_info()[0]
		#err_function = sys.exc_info()[1]
		#err_traceback = sys.exc_info()[2]
		# to find the code & reason from any class
		#print dir(err)
		#for i in dir(err):
		#    print i+' ===>> '+str(eval('err.'+i))
		reason,code = 'Unknown Error',-1
		succeeded = False
	if dnsurl!=None and dns_status!='STOP': connection.create_connection = original_create_connection
	if dns_status=='ALWAYS' and allow_dns_fix: dnsurl = None
	#LOG_THIS('ERROR',LOGGING(script_name)+'   4444444444444444444')
	#DIALOG_OK('1111','')
	if not succeeded and 'google-analytics' not in url2 and proxyurl==None:
		errortrace = traceback.format_exc()
		sys.stderr.write(errortrace)
	else:
		#code = '-1'
		#reason = 'System encoding bug'
		pass
	try: response.close()
	except: pass
	code = int(code)
	response2 = dummy_object()
	#DIALOG_OK('OPENURL_REQUESTS',str(response.content))
	if succeeded:
		response2.headers = response.headers
		response2.cookies = response.cookies
		response2.url     = response.url
		response2.content = response.content
		response2.code    = code
		response2.reason  = reason
		response2.succeeded = True
	else:
		response2.headers = {}
		response2.cookies = {}
		response2.url     = ''
		response2.content = '___Error___:'+str(code)+':'+reason
		response2.code = code
		response2.reason = reason
		response2.succeeded = False
	original_request = proxyurl==None and dnsurl==None and sslurl==None
	fixing_request = proxyurl!=None or dnsurl!=None or sslurl!=None
	if original_request and not response2.succeeded and 'google-analytics' not in url2:# and ('GET_PROXIES_LIST' in source and allow_proxy_fix):
		try: html = response.content
		except: html = response2.content
		htmlLower = html.lower()
		if 'cloudflare' in htmlLower and 'ray id: ' in htmlLower:
			reason2 = 'Blocked by Cloudflare'
			if 'recaptcha' in htmlLower: reason2 += ' using Google reCAPTCHA'
			reason = reason2+' ( '+reason+' )'
			response2.content = '___Error___:'+str(code)+':'+reason
		elif '5 sec' in htmlLower and 'browser' in htmlLower:
			reason2 = 'Blocked by 5 seconds browser check'
			reason = reason2+' ( '+reason+' )'
			response2.content = '___Error___:'+str(code)+':'+reason
		elif code in [104,111] or 'Max retries exceeded' in reason:
			reason2 = 'Blocked by your network provider'
			reason = reason2+' ( '+reason+' )'
			response2.content = '___Error___:'+str(code)+':'+reason
		if not response2.succeeded and code==8:
			LOG_THIS('ERROR',LOGGING(script_name)+'   Failed without SSL   Will enable SSL to fix this   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
			url3 = url+'||MySSLUrl='
			response3 = OPENURL_REQUESTS(method,url3,data,headers,allow_redirects,showDialogs,source)
			if response3.succeeded: response2 = response3
			else: LOG_THIS('ERROR',LOGGING(script_name)+'   SSL failed   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
		if not response2.succeeded and 'google-analytics' not in url and (allow_dns_fix or allow_proxy_fix):
			LOG_THIS('ERROR',LOGGING(script_name)+'   Direct connection failed   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
			if proxy_status=='ASK' or dns_status=='ASK':
				yes = SHOW_NETWORK_ERRORS(code,reason,source,True)
			else: yes = True
			if yes:
				if dns_status in ['ASK','AUTO'] and allow_dns_fix:
					#DIALOG_NOTIFICATION('لإصلاح مشكلة الإنترنيت','تم تفعيل سيرفر DNS',sound=False,time=2000)
					url3 = url2+'||MyDNSUrl='
					response3 = OPENURL_REQUESTS(method,url3,data,headers,allow_redirects,showDialogs,source)
					if response3.succeeded: response2 = response3
					else:
						LOG_THIS('ERROR',LOGGING(script_name)+'   All DNS failed:   DNS: [ '+dns_server+' ]   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
						DIALOG_NOTIFICATION('فشلت سيرفرات DNS','لإصلاح مشكلة الإنترنيت',sound=False,time=2000)
				if not response2.succeeded and proxy_status in ['ASK','AUTO'] and allow_proxy_fix:
					DIALOG_NOTIFICATION('تفعيل سيرفرات البروكسي','لإصلاح مشكلة الإنترنيت',sound=False,time=2000)
					response3 = OPENURL_REQUESTS_PROXIES(method,url2,data,headers,allow_redirects,showDialogs,source)
					if response3.succeeded: response2 = response3
					else:
						LOG_THIS('ERROR',LOGGING(script_name)+'   All proxies failed:   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
						DIALOG_NOTIFICATION('فشلت سبرفرات البروكسي','لإصلاح مشكلة الإنترنيت',sound=False,time=2000)
				"""
				if not response2.succeeded and (dns_status!='STOP' or proxy_status!='STOP'):
					LOG_THIS('ERROR',LOGGING(script_name)+'   All fixing attempts failed   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
					DIALOG_NOTIFICATION('للأسف فشلت عندك جميع','محاولات إصلاح الإنترنيت',sound=False,time=2000)
				if not response2.succeeded and code in [-1,7,11001,10054]:
					LOG_THIS('ERROR',LOGGING(script_name)+'   DNS failed   Will use this DNS server "'+dns_server+'" to fix this   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
					DIALOG_NOTIFICATION('مشكلة إنترنيت . سأحاول إصلاحها','سأجرب DNS رقم  '+dns_server,sound=False,time=2000)
					url3 = url+'||MyDNSUrl='
					response3 = OPENURL_REQUESTS(method,url3,data,headers,allow_redirects,showDialogs,source)
					if response3.succeeded: response2 = response3
					else: LOG_THIS('ERROR',LOGGING(script_name)+'   DNS used but failed   DNS: [ '+dns_server+' ]   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
				"""
			if proxy_status=='ASK' or dns_status=='ASK': showDialogs = False
		#DIALOG_OK(source,str(showDialogs))
		EXIT_IF_SOURCE(source,code,reason,showDialogs,allow_dns_fix,allow_proxy_fix)
	elif original_request and not response2.succeeded and 'google-analytics' in url2:
		LOG_THIS('ERROR',LOGGING(script_name)+'   Failed sending analytics event   URL: [ '+url2+' ]')
	if original_request and response2.succeeded and 'pythonanywhere' in url2:
		#DIALOG_OK(source,str(showDialogs))
		#LOG_THIS('ERROR',LOGGING(script_name)+'   Sending analytics event   URL: [ '+url2+' ]')		
		response3 = SEND_ANALYTICS_EVENT('PYTHON')
	#LOG_THIS('NOTICE',LOGGING(script_name)+'   Finished   Success: [ '+str(response2.succeeded)+' ]   URL: [ '+url2+' ]')
	return response2

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

def ARABIC_HEX(str1):
	str2 = repr(str1.encode('utf8')).replace("'",'')
	return str2

def unescapeHTML(string):
	if '&' in string and ';' in string:
		string = string.decode('utf8')
		import HTMLParser
		string = HTMLParser.HTMLParser().unescape(string)
		string = string.encode('utf8')
	return string

def remove_special_chars(string):
	string2 = ''.join(x for x in string if x.isalnum())
	return string2

def windows_filename(filename):
	filename2 = ''.join(i for i in filename if i not in '\/":*?<>|'+escapeUNICODE('\u02d1'))
	return filename2

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
		#DIALOG_OK(unicodedata.decomposition(letter),hex(ord(letter)))
		if ord(letter) < 256: unicode_letter = '\\u00'+hex(ord(letter)).replace('0x','')
		elif ord(letter) < 4096: unicode_letter = '\\u0'+hex(ord(letter)).replace('0x','')
		else: unicode_letter = '\\u'+unicodedata.decomposition(letter).split(' ')[1]
		new_string += unicode_letter
	new_string = new_string.replace('\u06CC','\u0649')
	new_string = new_string.decode('unicode_escape')
	new_string = new_string.encode('utf-8')
	return new_string

def KEYBOARD(header='لوحة المفاتيح',default='',allow_empty=False):
	#text = ''
	#kb = xbmc.Keyboard(default,header)
	#keyboard.setDefault(default)
	#keyboard.setHeading(header)
	#kb.doModal()
	#if kb.isConfirmed(): text = kb.getText()
	#dialog = xbmcgui.WindowXMLDialog('DialogKeyboard22.xml',addonfolder,'default','720p')
	#dialog.show()
	#dialog.doModal()
	#dialog.getControl(99991).setPosition(0,0)
	#dialog.getControl(311).setLabel(text)
	#dialog.getControl(5).setText(logfileNEW)
	#width = xbmcgui.getScreenWidth()
	#height = xbmcgui.getScreenHeight()
	#resolution = (0.0+width)/height
	#dialog.getControl(5).setWidth(width-180)
	#dialog.getControl(5).setHeight(height-180)
	#text = dialog.getControl(312).getLabel()
	#del dialog
	text = DIALOG_INPUT(header,default,type=xbmcgui.INPUT_ALPHANUM)
	text = text.replace('  ',' ').replace('  ',' ').replace('  ',' ')
	if text=='' and not allow_empty:
		DIALOG_OK('رسالة من المبرمج','تم إلغاء الإدخال')
		return ''
	if text not in ['',' ']:
		text = text.strip(' ')
		text = mixARABIC(text)
	return text

def ADD_TO_LAST_VIDEO_FILES():
	#vod_play_modes = [12,24,33,43,53,63,74,82,92,112,123,134,143,182,202,212,223,235,243,252]
	#live_play_modes = [235,105]
	#if int(mode)in vod_play_modes: filename = lastvodfile
	#elif int(mode)in live_play_modes: filename = lastlivefile
	#else: filename = ''
	type,name,url99,mode99,image99,page99,text99,context = EXTRACT_KODI_PATH()
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
				newLIST = newLIST[:50]
				newFILE[TYPE] = newLIST
			else: newFILE[TYPE] = oldFILE[TYPE]
	if type not in newFILE.keys(): newFILE[type] = [newItem]
	newFILE = str(newFILE)
	with open(lastvideosfile,'w') as f: f.write(newFILE)
	return

def EXTRACT_M3U8(url,headers=''):
	#headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
	#url = 'https://vd84.mycdn.me/video.m3u8'
	#with open('S:\\test2.m3u8', 'r') as f: html = f.read()
	html = OPENURL_CACHED(SHORT_CACHE,url,'',headers,'','LIBRARY-EXTRACT_M3U8-1st')
	#DIALOG_OK('11','')
	if 'TYPE=AUDIO' in html: return ['-1'],[url]
	if 'TYPE=VIDEO' in html: return ['-1'],[url]
	#if 'TYPE=SUBTITLES' in html: return ['-1'],[url]
	#xbmc.log(item, level=xbmc.LOGNOTICE)
	titleLIST,linkLIST,qualityLIST,bitrateLIST = [],[],[],[]
	lines = re.findall('\#EXT-X-STREAM-INF:(.*?)[\n\r](.*?)[\n\r]',html+'\n\r',re.DOTALL)
	if not lines: return ['-1'],[url]
	#DIALOG_OK('22','')
	for line,link in lines:
		lineDICT,bitrate,quality = {},-1,-1
		videofiletype = re.findall('(\.avi|\.ts|\.mp4|\.m3u|\.m3u8|\.mpd|\.mkv|\.flv|\.mp3)(|\?.*?|/\?.*?|\|.*?)&&',link.lower()+'&&',re.DOTALL|re.IGNORECASE)
		if videofiletype: title = videofiletype[0][0][1:]+'  '
		else: title = ''
		line = line.lower()
		items = line.split(',')
		for item in items:
			if '=' in item:
				key,value = item.split('=')
				lineDICT[key] = value
		if 'average-bandwidth' in line:
			bitrate = int(lineDICT['average-bandwidth'])/1024
			#title += 'AvgBW: '+str(bitrate)+'kbps  '
			title += str(bitrate)+'kbps  '
		elif 'bandwidth' in line:
			bitrate = int(lineDICT['bandwidth'])/1024
			#title += 'BW: '+str(bitrate)+'kbps  '
			title += str(bitrate)+'kbps  '
		if 'resolution' in line:
			quality = int(lineDICT['resolution'].split('x')[1])
			#title += 'Res: '+str(quality)+'  '
			title += str(quality)+'  '
		title = title.strip('  ')
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
	#DIALOG_OK('99','')
	#selection = DIALOG_SELECT('', titleLIST)
	#selection = DIALOG_SELECT('', linkLIST)
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
	#DIALOG_OK(node,md5)
	return md5
	"""
	#settings = xbmcaddon.Addon(id=addon_id)
	#settings.setSetting('user.hash','')
	#settings.setSetting('user.hash2','')
	#settings.setSetting('user.hash3','')
	#settings.setSetting('user.hash4','')
	#else: file = 'saverealhash4'
	#url = 'http://emadmahdi.pythonanywhere.com/saveinput'
	#input = md5full + '  ___  Found at:' + str(i) + '  ___  ' + hashComponents
	#	#payload = { 'file' : file , 'input' : input }
	#	#data = urllib.urlencode(payload)
	#	#html = OPENURL_CACHED(NO_CACHE,url,data,'','','LIBRARY-DUMMYCLIENTID-1st')
	#headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
	#payload = "file="+file+"&input="+input
	#import requests
	#response = requests.request("POST", url, data=payload, headers=headers)
	#	#html = response.content
	#	#DIALOG_OK(html,html)
	#url = 'http://emadmahdi.pythonanywhere.com/saveinput'
	#payload = { 'file' : 'savehash' , 'input' : md5full + '  ___  ' + hashComponents }
	#data = urllib.urlencode(payload)
	#return ''
	"""

def DNS_RESOLVER(url,dns_server):
	if url.replace('.','').isdigit(): return [url]
	try:
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
		sock.sendto(bytes(packet), (dns_server, 53))
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
	except: answer = []
	if not answer: LOG_THIS('ERROR',LOGGING(script_name)+'   DNS_RESOLVER failed   URL: [ '+url+' ]')
	return answer

def RATING_CHECK(script_name,url,ratingLIST):
	if PRIVILEGED('__ALLOW_RESTRUCTED__'): return False
	elif ratingLIST:
		if script_name=='BOKRA': blockedLIST = ['كبار']
		else: blockedLIST = ['r','ma','16','17','18','كبار','adult']
		for rating in ratingLIST:
			rating = rating.lower().decode('utf8').encode('utf8')
			cond1 = any(value in rating for value in blockedLIST)
			cond2 = 'not rated' not in rating
			if cond1 and cond2:
				LOG_THIS('ERROR',LOGGING(script_name)+'   Blocked adults video   URL: [ '+url+' ]')
				DIALOG_NOTIFICATION('رسالة من المبرمج','الفيديو للكبار فقط وأنا منعته',sound=False)
				return True
	return False
	"""
		found = False
		for rating in ratingLIST:
			rating = rating.lower().decode('utf8').encode('utf8')
			#DIALOG_OK('',rating)
			for blocked in blockedLIST:
				if len(blocked)<=2: blocked = '_'+blocked+'_'
				found = re.findall('[ -:_=\'\"\|]'+blocked+'[ -:_=\'\"\|]',rating,re.DOTALL)
				#DIALOG_OK(rating,str(found))
				if found: break
			if found: break
	if found:
		LOG_THIS('ERROR',LOGGING(script_name)+'   Blocked adults video   URL: [ '+url+' ]')
		DIALOG_NOTIFICATION('رسالة من المبرمج','الفيديو للكبار فقط وأنا منعته',sound=False)
		return True
	return False
	"""

"""
#inputstream.adaptive:	mpd, hls, ism
#inputstream.rtmp:		rtmp
#xbmc.executebuiltin('InstallAddon(inputstream.rtmp)',wait=True)

import inputstreamhelper
helper = inputstreamhelper.Helper('hls')
installed = helper.check_inputstream()
DIALOG_OK('is installed',str(installed))
if not installed:
	yes = DIALOG_YESNO('Addon not installed','install now ?','','','كلا','نعم')
	if yes: helper._install_inputstream()
"""

def ENABLE_MPD(showDialogs=True):
	if showDialogs=='': showDialogs = True
	enabled = xbmc.getCondVisibility('System.HasAddon(inputstream.adaptive)')
	if enabled and showDialogs: DIALOG_OK('رسالة من المبرمج','فحص اضافة inputstream.adaptive \n\r هذه ألإضافة عندك موجودة ومفعلة وجاهزة للاستخدام')
	elif not enabled:
		if showDialogs: yes = DIALOG_YESNO('رسالة من المبرمج','inputstream.adaptive \n\r هذه ألإضافة عندك غير مفعلة أو غير موجودة . يجب تنصيبها وتفعيلها لكي تعمل عندك فيديوهات نوع mpd hls ism  . هل تريد تنصيب وتفعيل هذه الإضافة الآن ؟','','','كلا','نعم')
		else: yes = True
		if yes:
			xbmc.executebuiltin('InstallAddon(inputstream.adaptive)',wait=True)
			result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"inputstream.adaptive","enabled":true}}')
			if 'OK' in result: DIALOG_OK('رسالة من المبرمج','تم التنصيب والتفعيل وهذه الإضافة inputstream.adaptive جاهزة للاستخدام')
			elif showDialogs: DIALOG_OK('رسالة من المبرمج','فشل في التنصيب أو التفعيل . البرنامج غير قادر على تنصيب أو تفعيل هذه الإضافة . والحل هو تنصيبها وتفعيلها من خارج البرنامج')
	return

def ENABLE_RTMP(showDialogs=True):
	if showDialogs=='': showDialogs = True
	enabled = xbmc.getCondVisibility('System.HasAddon(inputstream.rtmp)')
	if enabled and showDialogs: DIALOG_OK('رسالة من المبرمج','فحص اضافة inputstream.rtmp \n\r هذه ألإضافة عندك موجودة ومفعلة وجاهزة للاستخدام')
	elif not enabled:
		if showDialogs: yes = DIALOG_YESNO('رسالة من المبرمج','inputstream.rtmp \n\r هذه ألإضافة عندك غير مفعلة أو غير موجودة . يجب تنصيبها وتفعيلها لكي تعمل عندك فيديوهات نوع rtmp  . هل تريد تنصيب وتفعيل هذه الإضافة الآن ؟','','','كلا','نعم')
		else: yes = True
		if yes:
			xbmc.executebuiltin('InstallAddon(inputstream.rtmp)',wait=True)
			result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"inputstream.rtmp","enabled":true}}')
			if 'OK' in result: DIALOG_OK('رسالة من المبرمج','تم التنصيب والتفعيل وهذه الإضافة inputstream.rtmp جاهزة للاستخدام')
			elif showDialogs: DIALOG_OK('رسالة من المبرمج','فشل في التنصيب أو التفعيل . البرنامج غير قادر على تنصيب أو تفعيل هذه الإضافة . والحل هو تنصيبها وتفعيلها من خارج البرنامج')
	return

def WRITE_TO_SQL3(table,column,data,expiry):
	if expiry==NO_CACHE: return
	dataType = str(type(data))
	#DIALOG_OK(str(data),dataType)
	#size = 1
	#if   'str' in dataType: size = len(data)
	#elif 'list' in dataType: size = len(data)
	#elif 'dict' in dataType: size = len(data.values())
	#else:
	#if size==None: return
	try:
		html = data.content
		if '___Error___' in html or html=='': return
	except: pass
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
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Cache: [ Found ]   Table: [ '+table+' ]   Column: [ '+str(column)+' ]')
	#else: LOG_THIS('NOTICE',LOGGING(script_name)+'   Cache: [ Not Found ]   Table: [ '+table+' ]   Column: [ '+str(column)+' ]')
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

def URLDECODE(url):
	#DIALOG_OK(url,'URLDECODE')
	if '=' in url:
		if '?' in url: url2,filters = url.split('?')
		else: url2,filters = '',url
		filters = filters.split('&')
		data2 = {}
		for filter in filters:
			#DIALOG_OK(filter,str(filters))
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
	,'AKOAMCAM'		:'موقع أكوام كام'
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
	,'CIMANOW'		:'موقع سيما ناو'
	,'SHIAVOICE'	:'موقع صوت الشيعة'
	,'KARBALATV'	:'موقع قناة كربلاء'
	,'YTB_CHANNELS'	:'مواقع يوتيوب'
	,'MYCIMA'		:'موقع ماي سيما'
	,'BOKRA'		:'موقع بكرا'
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

def PLAY_VIDEO(url3,website='',type=''):
	if type=='': type = 'video'
	#DIALOG_OK(url3,website)
	#url3 = unescapeHTML(url3)
	result,subtitlemessage,httpd = 'canceled0','',''
	if len(url3)==3:
		url,subtitle,httpd = url3
		if subtitle!='': subtitlemessage = '   Subtitle: [ '+subtitle+' ]'
	else: url,subtitle,httpd = url3,'',''
	videofiletype = re.findall('(\.avi|\.ts|\.mp4|\.m3u|\.m3u8|\.mpd|\.mkv|\.flv|\.mp3)(|\?.*?|/\?.*?|\|.*?)&&',url.lower()+'&&',re.DOTALL|re.IGNORECASE)
	if videofiletype: videofiletype = videofiletype[0][0]
	else: videofiletype = ''
	if website not in ['DOWNLOAD','IPTV']:
		if website!='DOWNLOAD': url = url.replace(' ','%20')
		#url = quote(url)
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Preparing to play/download video   URL: [ '+url+' ]'+subtitlemessage)
		if videofiletype=='.m3u8' and website not in ['IPTV','YOUTUBE']:
			headers = {'User-Agent':''}
			titleLIST,linkLIST = EXTRACT_M3U8(url,headers)
			if len(linkLIST)>1:
				selection = DIALOG_SELECT('اختر الملف المناسب:', titleLIST)
				#DIALOG_OK(str(selection),website)
				if selection == -1:
					DIALOG_NOTIFICATION('تم إلغاء التشغيل','',sound=False)
					return result
			else: selection = 0
			url = linkLIST[selection]
			if titleLIST[0]!='-1':
				LOG_THIS('NOTICE',LOGGING(script_name)+'   Video Selected   Selection: [ '+titleLIST[selection]+' ]   URL: [ '+url+' ]')
		if 'http' in url.lower() and '/dash/' not in url and 'youtube.mpd' not in url:
			if 'verifypeer=' not in url and 'https://' in url.lower():
				if '|' not in url: url = url+'|verifypeer=false'
				else: url = url+'&verifypeer=false'
			if 'user-agent' not in url.lower() and website!='IPTV':
				if '|' not in url: url = url+'|User-Agent=&'
				else: url = url+'&User-Agent=&'
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Got final url   URL: [ '+url+' ]')
	play_item = xbmcgui.ListItem()
	#play_item = xbmcgui.ListItem('test')
	type99,name,url99,mode99,image,page99,text99,context = EXTRACT_KODI_PATH()
	if website not in ['DOWNLOAD','IPTV']:
		#play_item = xbmcgui.ListItem(path=url)
		play_item.setProperty('inputstreamaddon', '')
		play_item.setMimeType('mime/x-type')
		play_item.setInfo('Video', {'mediatype': 'video'})
		#img = xbmc.getInfoLabel('ListItem.icon')
		play_item.setArt({'icon':image,'thumb':image,'fanart':fanartfile})
		play_item.setInfo( "Video",{'Title':name})
		#name = xbmc.getInfoLabel('ListItem.Label')
		#name = name.strip(' ')
		if videofiletype in ['.avi','.ts','.mkv','.mp4','.mp3','.flv']:
			#when set to "False" it makes glarabTV fails and make WS2TV opens fast
			play_item.setContentLookup(False)
		#if videofiletype in ['.m3u8']: play_item.setContentLookup(False)
		if 'rtmp' in url: enabled = ENABLE_RTMP(False)
		if videofiletype=='.mpd' or '/dash/' in url:
			enabled = ENABLE_MPD(False)
			play_item.setProperty('inputstreamaddon','inputstream.adaptive')
			play_item.setProperty('inputstream.adaptive.manifest_type','mpd')
		if subtitle!='':
			play_item.setSubtitles([subtitle])
			#xbmc.log(LOGGING(script_name)+'      Added subtitle to video   Subtitle:['+subtitle+']', level=xbmc.LOGNOTICE)
	if type=='video' and website=='DOWNLOAD':
		result = 'play_download'
		website = 'PLAY_DL_FILES'
	elif type=='video' and context.startswith('6'):
		result = 'download'
		website = website+'_DL'
	# VERY IMPORTANT
	#	myplayer = CustomPlayer() is needed for both setResolvedUrl() and Player()
	#	and should be used with xbmc.sleep(step*1000)
	myplayer = CustomPlayer()
	if type=='video' and not context.startswith('6'):
		#title = xbmc.getInfoLabel('ListItem.Title')
		#play_item.setInfo('Video', {'duration': 3600})
		#xbmcplugin.setContent(addon_handle,'videos')
		#play_item.setInfo('video',{'mediatype':'video'})
		#play_item.setProperty('IsPlayable','true')
		#play_item.setInfo(type='Video',infoLabels={"Title":'Title'})
		play_item.setPath(url)
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Playing video file using setResolvedUrl()   URL: [ '+url+' ]')
		xbmcplugin.setResolvedUrl(addon_handle,True,play_item)
	elif type=='live':
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Playing video file using play()   URL: [ '+url+' ]')
		myplayer.play(url,play_item)
		#xbmc.Player().play(url,play_item)
		#DIALOG_OK(url,type)
	ADD_TO_LAST_VIDEO_FILES()
	#logfilename = xbmc.translatePath('special://logpath')+'kodi.log'
	if result!='download':
		timeout,step,result = 60,1,'tried'
		for i in range(0,timeout,step):
			# VERY IMPORTANT
			#	if using time.sleep() instead of xbmc.sleep() then the player status
			#	"myplayer.status" will stop working for both setResolvedUrl() and Player()
			xbmc.sleep(step*1000)
			result = myplayer.status
			if result=='playing':
				DIALOG_NOTIFICATION('الفيديو يعمل','',time=1000,sound=False)
				LOG_THIS('NOTICE',LOGGING(script_name)+'   Success: video is playing   URL: [ '+url+' ]'+subtitlemessage)
				break
			elif result=='failed':
				LOG_THIS('ERROR',LOGGING(script_name)+'   Failed playing video   URL: [ '+url+' ]'+subtitlemessage)
				DIALOG_NOTIFICATION('الفيديو لم يعمل','',time=1000,sound=False)
				break
			DIALOG_NOTIFICATION('جاري تشغيل الفيديو','باقي '+str(timeout-i)+' ثانية',sound=False)
		else:
			result = 'timeout'
			myplayer.stop()
			DIALOG_NOTIFICATION('الفيديو لم يعمل','',sound=False)
			LOG_THIS('ERROR',LOGGING(script_name)+'   Timeout unknown problem   URL: [ '+url+' ]'+subtitlemessage)
	cond1 = result in ['playing','play_download']
	cond2 = result=='download' and videofiletype in ['.ts','.mkv','.mp4','.mp3','.flv','.m3u8','avi']
	if cond1 or cond2:
		#addon_version = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
		response = SEND_ANALYTICS_EVENT(website)
		#html = response.content
	if httpd!='':
		#DIALOG_OK('click ok to shutdown the http server','')
		#html = OPENURL_CACHED(NO_CACHE,'http://localhost:55055/shutdown','','','','LIBRARY-PLAY_VIDEO-2nd')
		time.sleep(1)
		httpd.shutdown()
		#DIALOG_OK('http server is down','')
	if result=='download':
		import DOWNLOAD
		DOWNLOAD.DOWNLOAD_VIDEO(url,videofiletype)
	#if result in ['download','tried','failed','timeout','playing']: EXIT_PROGRAM('LIBRARY-PLAY_VIDEO-2nd',False)
	#EXIT_PROGRAM('LIBRARY-PLAY_VIDEO-3rd')
	#if 'https://' in url and result in ['failed','timeout']:
	#	working = HTTPS(False)
	#	if not working:
	#		DIALOG_OK('الاتصال مشفر','مشكلة ... هذا الفيديو يحتاج الى اتصال مشفر (ربط مشفر) ولكن للأسف الاتصال المشفر لا يعمل على جهازك')
	#		return 'https'
	#sys.exit()
	return result

def SEND_ANALYTICS_EVENT(script_name):
	randomNumber = str(random.randrange(111111111111,999999999999))
	url = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addon_version+'&av='+addon_version+'&an=ARABIC_VIDEOS&ea='+script_name+'&el='+str(kodi_version)+'&z='+randomNumber
	response = OPENURL_REQUESTS('GET',url,'','','',False,'LIBRARY-SEND_ANALYTICS_EVENT-1st')
	#DIALOG_OK(url,response.content)
	return response

def SEARCH_OPTIONS(search):
	options,showdialogs = '',True
	if search.count('_')>=2:
		search,options = search.split('_',1)
		options = '_'+options
		if '_NODIALOGS_' in options: showdialogs = False
		else: showdialogs = True
	#DIALOG_OK(search,options)
	return search,options,showdialogs

def DIALOG_OK(*args,**kwargs):
	return xbmcgui.Dialog().ok(*args,**kwargs)

def DIALOG_YESNO(*args,**kwargs):
	return xbmcgui.Dialog().yesno(*args,**kwargs)

def DIALOG_SELECT(*args,**kwargs):
	return xbmcgui.Dialog().select(*args,**kwargs)

def DIALOG_NOTIFICATION(*args,**kwargs):
	return xbmcgui.Dialog().notification(*args,**kwargs)

def DIALOG_TEXTVIEWER(*args,**kwargs):
	#return xbmcgui.Dialog().textviewer(*args,**kwargs)
	return DIALOG_TEXTVIEWER_FULLSCREEN(args[0],args[1],'big','left')

def DIALOG_CONTEXTMENU(*args,**kwargs):
	return xbmcgui.Dialog().contextmenu(*args,**kwargs)

def DIALOG_BROWSESINGLE(*args,**kwargs):
	return xbmcgui.Dialog().browseSingle(*args,**kwargs)

def DIALOG_INPUT(*args,**kwargs):
	return xbmcgui.Dialog().input(*args,**kwargs)

def DIALOG_PROGRESS(*args,**kwargs):
	return xbmcgui.DialogProgress(*args,**kwargs)

def DIALOG_BUSY(job):
	if kodi_version>17.999: dialog = 'busydialognocancel'
	else: dialog = 'busydialog'
	if job=='start': xbmc.executebuiltin('ActivateWindow('+dialog+')')
	elif job=='stop': xbmc.executebuiltin('Dialog.Close('+dialog+')')
	return

def DIALOG_TEXTVIEWER_FULLSCREEN(header,text,size,direction):
	#return
	#dialog = xbmcgui.WindowXML('Font22.xml',addonfolder)
	#dialog.show()
	dialog = xbmcgui.WindowXMLDialog('DialogTextViewerFullScreen.xml',addonfolder)
	dialog.show()
	#dialog.getControl(99991).setPosition(0,0)
	dialog.getControl(1).setLabel(header)
	if size=='big' and direction=='center':
		dialog.getControl(51).setVisible(False)
		dialog.getControl(52).setVisible(False)
		dialog.getControl(53).setVisible(False)
		dialog.getControl(54).setText(text)
	elif size=='small' and direction=='left':
		dialog.getControl(51).setVisible(False)
		dialog.getControl(52).setVisible(False)
		dialog.getControl(53).setText(text)
		dialog.getControl(54).setVisible(False)
	elif size=='big' and direction=='right':
		dialog.getControl(51).setVisible(False)
		dialog.getControl(52).setText(text)
		dialog.getControl(53).setVisible(False)
		dialog.getControl(54).setVisible(False)
	elif size=='big' and direction=='left':
		dialog.getControl(51).setText(text)
		dialog.getControl(52).setVisible(False)
		dialog.getControl(53).setVisible(False)
		dialog.getControl(54).setVisible(False)
	#width = xbmcgui.getScreenWidth()
	#height = xbmcgui.getScreenHeight()
	#resolution = (0.0+width)/height
	#dialog.getControl(5).setWidth(width-180)
	#dialog.getControl(5).setHeight(height-180)
	result = dialog.doModal()
	del dialog
	return result

def RANDOM_USERAGENT():
	results = READ_FROM_SQL3('SETTINGS','USERAGENT')
	#DIALOG_OK(results,'')
	#LOG_THIS('NOTICE','EMAD ======== useragent: '+results)
	if results: useragent = results ; return useragent
	# Latest and most common user agents (always updated)
	url = 'https://techblog.willshouse.com/2012/01/03/most-common-user-agents/'
	headers = {'Referer':url}
	response = OPENURL_REQUESTS_CACHED(VERY_LONG_CACHE,'GET',url,'',headers,'','','YOUTUBE-RANDOM_USERAGENT-1st')
	html = response.content
	count = html.count('Mozilla')
	#LOG_THIS('NOTICE',html)
	#DIALOG_OK(str(count),html)
	if '___Error___' in html or count<200:
		with open(useragentfile,'r') as f: text = f.read()
	else:
		text = re.findall('get-the-list.*?>(.*?)<',html,re.DOTALL)
		text = text[0]
	a = re.findall('(Mozilla.*?)\n',text,re.DOTALL)
	b = random.sample(a,1)
	useragent = b[0]
	#DIALOG_OK(useragent,str(len(a)))
	WRITE_TO_SQL3('SETTINGS','USERAGENT',useragent,SHORT_CACHE)
	return useragent

def HANDLE_EXIT_ERRORS(error):
	if str(error) not in ['Forced Exit']:
		errortrace = traceback.format_exc()
		sys.stderr.write(errortrace)
		lines = errortrace.splitlines()
		error_line = lines[-1]
		file_line = lines[-3].replace('.py','')
		#DIALOG_OK('',file_line))
		if '\\' in file_line: file_line = file_line.rsplit('\\',1)[1]
		elif '/' in file_line: file_line = file_line.rsplit('/',1)[1]
		error_source = re.findall('(.*?)", line (\d+), in (.*?)&&',file_line+'&&',re.DOTALL)
		if error_source: file,lineno,function = error_source[0]
		else: file,lineno,function = 'مجهول','مجهول','مجهول'
		DIALOG_NOTIFICATION('خطأ '+function+' '+lineno+' '+file,error_line,time=2000)
	return

def PRIVILEGED(priv):
	settings = xbmcaddon.Addon(id=addon_id)
	privs = settings.getSetting('user.privs')
	priv = priv.encode('base64').replace('\n','')
	user = dummyClientID(32)
	md5 = hashlib.md5(priv+user).hexdigest()[0:32]
	if md5 in privs: return True
	return False




