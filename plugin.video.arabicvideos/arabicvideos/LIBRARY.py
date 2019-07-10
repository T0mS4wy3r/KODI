# -*- coding: utf-8 -*-

import xbmcplugin,xbmcgui,xbmcaddon,sys,xbmc,os,re,time,thread,zlib		# total cost = 0ms
import urllib		# 160ms
import urllib2		# 354ms (contains urllib)
import sqlite3		# 50ms (with threading 71ms)
#import requests   	# 986ms (contains urllib,urllib2,urllib3)
#import threading	# 54ms (with sqlite3 71ms)
#import urllib3		# 621ms (contains urllib)
#import timeit		# 10ms
#import base64		# 29ms
#import httplib		# 280ms
#import urlresolver	# 2170ms (contains urllib,urllib2,urllib3,requests)




# calculate the average time needed to import a main-module and how many sub-modules will be imported with it
"""
import sys,time
totalelpased = 0
for i in range(20):
	t1 = time.time()
	before_import = sys.modules.keys()
	import urlresolver
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
xbmcgui.Dialog().ok(str(import_count),'average time ms: '+str(totalelpased*1000/20))
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




addon_handle = int(sys.argv[1])
addon_id = sys.argv[0].split('/')[2] 		# plugin.video.arabicvideos
addon_path = sys.argv[0]+sys.argv[2] 		# plugin://plugin.video.arabicvideos/?mode=12&url=http://test.com
#addon_path = xbmc.getInfoLabel( "ListItem.FolderPath" )
addonVersion = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )

menupath = urllib2.unquote(addon_path)
menulabel = xbmc.getInfoLabel('ListItem.Label').replace('[COLOR FFC89008]','').replace('[/COLOR]','')
if menulabel=='' or menupath=='plugin://plugin.video.arabicvideos/': menulabel = 'Main Menu'

kodiVersion = xbmc.getInfoLabel( "System.BuildVersion" )	
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

addoncachefolder = os.path.join(xbmc.translatePath('special://temp'),addon_id)
dbfile = os.path.join(addoncachefolder,"webcache_"+addonVersion+"_.db")

LONG_CACHE = 60*60*24*3
REGULAR_CACHE = 60*60*16
SHORT_CACHE = 60*60*2
NO_CACHE = 0
now = time.time()

#LONG_CACHE = 0
#REGULAR_CACHE = 0
#SHORT_CACHE = 0

page_error = 'الصفحة غير متوفرة الان ... قد يكون الموقع الاصلي غير متوفر الان او هذه الصفحة قد تغيرت والمبرمج لا يعرف ... الرجاء المحاولة لاحقا او ابلاغ المبرمج بالمشكلة'
https_problem = 'مشكلة ... الاتصال المشفر (الربط المشفر) لا يعمل عندك على كودي ... وعندك كودي غير قادر على استخدام المواقع المشفرة'

def DELETE_DATABASE_FILES():
	for filename in os.listdir(addoncachefolder):
		if 'webcache_' in filename and '_.db' in filename:
			filename = os.path.join(addoncachefolder,filename)
			os.remove(filename)
	return ''

def addDir(name,url='',mode='',iconimage='',page='',text=''):
	if iconimage=='': iconimage = icon
	#xbmc.log('['+addon_id+']:  name:['+name+']', level=xbmc.LOGNOTICE)
	name2 = re.findall('&&_(\D\D\w)__MOD_(.*?)&&','&&'+name+'&&',re.DOTALL)
	if name2: name = ';[COLOR FFC89008]'+name2[0][0]+' [/COLOR]'+name2[0][1]
	name2 = re.findall('&&_(\D\D\w)_(.*?)&&','&&'+name+'&&',re.DOTALL)
	if name2: name = ',[COLOR FFC89008]'+name2[0][0]+' [/COLOR]'+name2[0][1]
	u = 'plugin://'+addon_id+'/?mode='+str(mode)
	if url!='': u = u + '&url=' + quote(url)
	#xbmcgui.Dialog().ok(quote(url),'addDir')
	if page!='': u = u + '&page=' + quote(page)
	if text!='': u = u + '&text=' + quote(text)
	listitem=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setInfo( type="Video", infoLabels={ "Title": name } )
	listitem.setProperty('fanart_image', fanart)
	#listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=listitem,isFolder=True)
	return

def addLink(name,url,mode,iconimage='',duration='',text=''):
	if iconimage=='': iconimage = icon
	name2 = re.findall('&&_(\D\D\w)__MOD_(.*?)&&','&&'+name+'&&',re.DOTALL)
	if name2: name = escapeUNICODE('\u02d1')+'[COLOR FFC89008]'+name2[0][0]+' [/COLOR]'+name2[0][1]
	name2 = re.findall('&&_(\D\D\w)_(.*?)&&','&&'+name+'&&',re.DOTALL)
	if name2: name = ' [COLOR FFC89008]'+name2[0][0]+' [/COLOR]'+name2[0][1]
	if 'IsPlayable=no' in text: IsPlayable = 'no'
	else: IsPlayable='yes'
	u = 'plugin://'+addon_id+'/?mode='+str(mode)
	if url!='': u = u + '&url=' + quote(url)
	#xbmcgui.Dialog().ok(quote(url),'addLink')
	if text!='': u = u + '&text=' + quote(text)
	listitem=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setProperty('fanart_image', fanart)
	listitem.setInfo('Video', {'mediatype': 'video'})
	if duration != '' :
		if len(duration)<=2 : duration = '00:' + duration
		if len(duration)<=5 : duration = '00:' + duration
		duration = sum(x * int(t) for x, t in zip([3600,60,1], duration.split(":"))) 	
		listitem.setInfo('Video', {'duration': duration})
	if IsPlayable=='yes': listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setContent(addon_handle, 'videos')
	xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=listitem,isFolder=False)
	return

def openURL_KPROXY(url,data='',headers='',showDialogs='',source=''):
	#xbmcgui.Dialog().ok(url,html)
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	html = openURL(url,data,headers,showDialogs,source)
	if '___Error___' in html:
		try:
			import requests
			response = requests.request('GET', 'http://www.kproxy.com', headers='', data='', allow_redirects=True)
			html = response.text
			cookies = response.cookies.get_dict()
			KP_DAT2 = cookies['KP_DAT2__']
			cookies2 = 'KP_DAT2__=' + KP_DAT2
			headers2 = { 'Cookie' : cookies2 }
			payload2 = { 'page' : quote(url) }
			data2 = urllib.urlencode(payload2)
			html = openURL('http://www.kproxy.com/doproxy.jsp',data2,headers2,source)
			proxyURL = re.findall('url=(.*?)"',html,re.DOTALL)[0]
			if headers=='': headers3 = {}
			else: headers3 = headers
			try: headers3['Cookie'] = headers3['Cookie']+';'+ cookies2
			except: headers3['Cookie'] = cookies2
			html = openURL(proxyURL,data,headers3,showDialogs,source)
		except:
			xbmcgui.Dialog().ok('مشكلة من الموقع الاصلي',page_error)
			xbmc.log('['+addon_id+']:   Error opening kproxy:   [ '+url+' ]', level=xbmc.LOGNOTICE)
			raise Exception('Page not found requested by:   '+source)
	return html

def openURL_cached(cacheperiod,url,data='',headers='',showDialogs='',source=''):
	#t1 = time.time()
	xbmc.log('['+addon_id+']:   Opening page:   [ '+url+' ]', level=xbmc.LOGNOTICE)
	#xbmcgui.Dialog().ok(unquote(url),source+'     cache(hours)='+str(cacheperiod/60/60))
	if cacheperiod==0: return openURL(url,data,headers,showDialogs,source)
	#nowTEXT = time.ctime(now)
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	#conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
	t = (url,str(data),str(headers),source)
	c.execute('SELECT html FROM htmlcache WHERE url=? AND data=? AND headers=? AND source=?', t)
	rows = c.fetchall()
	#html = repr(rows[0][0])
	if rows:
		message = 'found in cache'
		html = rows[0][0]
		#html = base64.b64decode(html)
		html = zlib.decompress(html)
	else:
		message = 'not found in cache'
		html = openURL(url,data,headers,showDialogs,source)
		#html2 = base64.b64encode(html)
		html2 = zlib.compress(html)
		t = (now+cacheperiod,url,str(data),str(headers),source,sqlite3.Binary(html2))
		c.execute("INSERT INTO htmlcache VALUES (?,?,?,?,?,?)",t)
		conn.commit()
	conn.close()
	#t2 = time.time()
	#xbmcgui.Dialog().notification(message,str(int(t2-t1))+' ms')
	return html

def openURL(url,data='',headers='',showDialogs='',source=''):
	if showDialogs=='': showDialogs='yes'
	request = urllib2.Request(url)
	if data=='' and headers=='': request = urllib2.Request(url)
	elif data=='' and headers!='': request = urllib2.Request(url,headers=headers)
	elif data!='' and headers=='': request = urllib2.Request(url,data=data)
	elif data!='' and headers!='': request = urllib2.Request(url,headers=headers,data=data)
	html,code,reason = '','200','OK'
	try:
		response = urllib2.urlopen(request,timeout=60)
		html = response.read()
		code = str(response.code)
		response.close
	except urllib2.HTTPError as error:
		code = str(error.code)
		reason = str(error.reason)
	except urllib2.URLError as error:
		code = str(error.reason[0])
		reason = str(error.reason[1])
	if code!='200':
		#if 'google-analytics' not in url:
		#	xbmc.log('['+addon_id+']:   Open URL Error:   Code:[ '+code+' ]   Reason:[ '+reason+' ]'+'   Source:[ '+source+' ]'+'   URL:[ '+url+' ]', level=xbmc.LOGNOTICE)
		message,send,showDialogs = '','no','no'
		html = '___Error___ {}: {!r}'.format(code, reason)
		if 'google-analytics' in url: send = showDialogs
		if showDialogs=='yes':
			xbmcgui.Dialog().ok('خطأ في الاتصال',html)
			if code=='502' or code=='7':
				xbmcgui.Dialog().ok('Website is not available','لا يمكن الوصول الى الموقع والسبب قد يكون من جهازك او من الانترنيت الخاصة بك او من الموقع كونه مغلق للصيانة او التحديث لذا يرجى المحاولة لاحقا')
				send = 'no'
			elif code=='404':
				xbmcgui.Dialog().ok('File not found','الملف غير موجود والسبب غالبا هو من المصدر ومن الموقع الاصلي الذي يغذي هذا البرنامج')
			if send=='yes':
				yes = xbmcgui.Dialog().yesno('سؤال','هل تربد اضافة رسالة مع الخطأ لكي تشرح فيها كيف واين حصل الخطأ وترسل التفاصيل الى المبرمج ؟','','','كلا','نعم')
				if yes: message = ' \\n\\n' + KEYBOARD('Write a message   اكتب رسالة')
		if send=='yes': SEND_EMAIL('Error: From Arabic Videos',html+message,showDialogs,url,source)
		if 'RESOLVERS' not in source and source not in ['PROGRAM-HTTPS-1st','LIBRARY-PLAY_VIDEO-1st','PROGRAM-VERSION-1st']:
			if 'https://' in url and source in ['PROGRAM-HTTPS-1st']:
				xbmcgui.Dialog().ok('الاتصال المشفر',https_problem)
			else: xbmcgui.Dialog().ok('مشكلة من الموقع الاصلي',page_error)
			#xbmcgui.Dialog().ok('',html)
			raise Exception('['+addon_id+']:   Error opening page:   Code:[ '+code+' ]   Reason:[ '+reason+' ]'+'   Source:[ '+source+' ]'+'   URL:[ '+url+' ]')
	return html

def quote(url):
	return urllib2.quote(url,':/')

def unquote(url):
	return urllib2.unquote(url)

def unescapeHTML(string):
	if '&' in string and ';' in string:
		string = string.decode('utf8')
		import HTMLParser
		string = HTMLParser.HTMLParser().unescape(string)
		string = string.encode('utf8')
	return string

def escapeUNICODE(string):
	if '\u' in string:
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
		if ord(letter) < 256: unicode_letter = '\u00'+hex(ord(letter)).replace('0x','')
		elif ord(letter) < 4096: unicode_letter = '\u0'+hex(ord(letter)).replace('0x','')
		else: unicode_letter = '\u'+unicodedata.decomposition(letter).split(' ')[1]
		new_string += unicode_letter
	new_string = new_string.replace('\u06CC','\u0649')
	new_string = new_string.decode('unicode_escape')
	new_string = new_string.encode('utf-8')
	return new_string

def KEYBOARD(label='Search'):
	search =''
	keyboard = xbmc.Keyboard(search, label)
	keyboard.doModal()
	if keyboard.isConfirmed(): search = keyboard.getText()
	search = search.strip(' ')
	if len(search.decode('utf8'))<2:
		#xbmcgui.Dialog().ok('Wrong entry. Try again','خطأ في الادخال. أعد المحاولة')
		return ''
	new_search = mixARABIC(search)
	return new_search

def PLAY_VIDEO(url3,website='',showWatched='yes'):
	#showWatched = 'no'
	#url3 = 's:\emad.m3u8'
	result = 'canceled0'
	if len(url3)==2: url,subtitle = url3
	else: url,subtitle = url3,''
	#url = url + '|User-Agent=&'
	#xbmcgui.Dialog().ok(url,'video url')
	if subtitle!='': urlmessage = '[ '+url+' ]   Subtitle:[ '+subtitle+' ]'
	else: urlmessage = '[ '+url+' ]'
	xbmc.log('['+addon_id+']:   Started playing video:   '+urlmessage, level=xbmc.LOGNOTICE)
	if 'https' in url:
		worked = HTTPS(False)
		if not worked:
			xbmcgui.Dialog().ok('الاتصال مشفر','مشكلة ... هذا الفيديو يحتاج الى اتصال مشفر (ربط مشفر) ولكن للأسف الاتصال المشفر لا يعمل على جهازك')
			return 'https'
	play_item = xbmcgui.ListItem(path=url)
	play_item.setProperty('inputstreamaddon', '')
	play_item.setMimeType('mime/x-type')
	myplayer = CustomePlayer()
	videofiletype = re.findall('(.ts|.mp4|.m3u|.m3u8|.mpd|.mkv|.flv|.mp3)(|\?.*?|/\?.*?|\|.*?)&&',url+'&&',re.DOTALL)
	if videofiletype: videofiletype = videofiletype[0][0]
	else: videofiletype = ''
	if videofiletype=='.ts':
		#when set to "False" it makes glarabTV fails and make WS2TV opens fast
		play_item.setContentLookup(False)
	if videofiletype=='.mpd' or '/dash/' in url:
		play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
		play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
	if subtitle!='':
		play_item.setSubtitles([subtitle])
		#xbmc.log('['+addon_id+']:  Added subtitle to video: ['+subtitle+']', level=xbmc.LOGNOTICE)
	if showWatched=='yes':
		#title = xbmc.getInfoLabel('ListItem.Title')
		#label = xbmc.getInfoLabel('ListItem.Label')
		#play_item.setInfo( "video", { "Title": label } )
		#play_item.setPath(url)
		#play_item.setInfo('Video', {'duration': 3600})
		xbmcplugin.setResolvedUrl(addon_handle, True, play_item)
	else:
		label = xbmc.getInfoLabel('ListItem.Label')
		play_item.setInfo( "video", { "Title": label } )
		myplayer.play(url,play_item)
		#xbmc.Player().play(url,play_item)
	play_item.setContentLookup(False)
	#logfilename = xbmc.translatePath('special://logpath')+'kodi.log'
	timeout,step,result = 60,2,'tried'
	for i in range(0,timeout,step):
		xbmc.sleep(step*1000)
		result = myplayer.status
		if result=='playing':
			xbmc.log('['+addon_id+']:   Success: Video is playing:   '+urlmessage, level=xbmc.LOGNOTICE)
			xbmcgui.Dialog().notification('الفيديو يعمل','','',500)
			break
		elif result=='failed':
			xbmc.log('['+addon_id+']:   Failure: Error playing video:   '+urlmessage, level=xbmc.LOGNOTICE)
			break
		xbmcgui.Dialog().notification(myplayer.status +'جاري تشغيل الفيديو','باقي '+str(timeout-i)+' ثانية')
	else:
		myplayer.stop()
		result = 'timeout'
		xbmc.log('['+addon_id+']:   Timeout: Unknown playing issue:   '+urlmessage, level=xbmc.LOGNOTICE)
	if result!='playing': xbmcgui.Dialog().notification('الفيديو لم يعمل','')
	addonVersion = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
	import random
	randomNumber = str(random.randrange(111111111111,999999999999))
	url2 = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addonVersion+'&av='+addonVersion+'&an=ARABIC_VIDEOS&ea='+website+'&z='+randomNumber
	openURL(url2,'','','no','LIBRARY-PLAY_VIDEO-1st')
	return result

def SEND_EMAIL(subject,message,showDialogs='yes',url='',source='',text=''):
	if 'problem=yes' in text: problem='yes'
	else: problem='no'
	sendit,html = 1,''
	if showDialogs=='yes':
		sendit = xbmcgui.Dialog().yesno('هل ترسل هذه الرسالة الى المبرمج',message.replace('\\n','\n'),'','','كلا','نعم')
		if sendit==0: 
			xbmcgui.Dialog().ok('تم الغاء الارسال','تم الغاء الارسال بناء على طلبك')
			return ''
	if sendit==1:
		addonVersion = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
		kodiVersion = xbmc.getInfoLabel( "System.BuildVersion" )	
		kodiName = xbmc.getInfoLabel( "System.FriendlyName" )
		message = message+' \\n\\n==== ==== ==== \\nAddon Version: '+addonVersion+' :\\nEmail Sender: '+dummyClientID(32)+' :\\nKodi Version: '+kodiVersion+' :\\nKodi Name: '+kodiName
		#xbmc.sleep(4000)
		#playerTitle = xbmc.getInfoLabel( "Player.Title" )
		#playerPath = xbmc.getInfoLabel( "Player.Filenameandpath" )
		#if playerTitle != '': message += ' :\\nPlayer Title: '+playerTitle
		#if playerPath != '': message += ' :\\nPlayer Path: '+playerPath
		#xbmcgui.Dialog().ok(playerTitle,playerPath)
		if url != '': message += ' :\\nURL: ' + url
		if source != '': message += ' :\\nSource: ' + source
		message += ' :\\n'
		if problem=='yes':
			if showDialogs=='yes': xbmcgui.Dialog().notification('جاري الارسال','الرجاء الانتظار')
			logfile = xbmc.translatePath('special://logpath')+'kodi.log'
			f = open(logfile,'rb')
			size = os.path.getsize(logfile)
			if size>60000: f.seek(-60000, os.SEEK_END)
			data = f.readlines()
			logfileNEW = ''.join(data[-300:])
			import base64
			logfileNEW = base64.b64encode(logfileNEW)
		url = 'http://emadmahdi.pythonanywhere.com/sendemail'
		payload = { 'subject' : quote(subject) , 'message' : quote(message) , 'logfile' : logfileNEW }
		data = urllib.urlencode(payload)
		html = openURL_cached(NO_CACHE,url,data,'','','LIBRARY-SEND_EMAIL-1st')
		result = html[0:6]
		if showDialogs=='yes':
			if result == 'Error ':
				xbmcgui.Dialog().notification('فشل في الارسال','للأسف')
				xbmcgui.Dialog().ok('Failed sending the message','خطأ وفشل في ارسال الرسالة')
			else:
				xbmcgui.Dialog().notification('بنجاح','تم الارسال')
				xbmcgui.Dialog().ok('Message sent','تم ارسال الرسالة بنجاح')
	return html

def M3U8_RESOLUTIONS(url,headers=''):
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','LIBRARY-GET_M3U8_RESOLUTIONS-1st')
	items = re.findall('RESOLUTION=\d+[x|X](\d+).*?\n(.*?)\n',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,str(items))
	items = set(items)
	items = sorted(items, reverse=True, key=lambda key: int(key[0]))
	if items:
		titleLIST,linkLIST = [],[]
		for resolution,link in items:
			if 'http' not in link: link = url.rsplit('/',1)[0] + '/' + link
			titleLIST.append(resolution)
			linkLIST.append(link)
		#z = zip(titleLIST,linkLIST)
		#z = set(z)
		#z = sorted(z, reverse=True, key=lambda key: key[0])
		#titleLIST,linkLIST = zip(*z)
		#titleLIST,linkLIST = list(titleLIST),list(linkLIST)
	else: titleLIST,linkLIST = [url],[url]
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
	import hashlib
	md5full = hashlib.md5(hashComponents).hexdigest()
	md5 = md5full[0:length]
	#xbmcgui.Dialog().ok(node,md5)
	return md5
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
	#	#html = response.text
	#	#xbmcgui.Dialog().ok(html,html)
	#url = 'http://emadmahdi.pythonanywhere.com/saveinput'
	#payload = { 'file' : 'savehash' , 'input' : md5full + '  ::  ' + hashComponents }
	#data = urllib.urlencode(payload)
	#return ''

def HTTPS(show=True):
	if show: cacheperiod = NO_CACHE
	else: cacheperiod = LONG_CACHE
	html = openURL_cached(cacheperiod,'https://www.google.com','','','','PROGRAM-HTTPS-1st')
	#xbmcgui.Dialog().ok('Checking SSL',html)
	if 'html' in html:
		worked = True
		if show: xbmcgui.Dialog().ok('الاتصال المشفر','جيد جدا ... الاتصال المشفر (الربط المشفر) يعمل عندك على كودي ... وعندك كودي قادر على استخدام المواقع المشفرة')
	else:
		worked = False
		xbmc.log('['+addon_id+']:   HTTPS Failed:   Label:[ '+menulabel+' ]   Path:[ '+menupath+' ]', level=xbmc.LOGNOTICE)
		if show: xbmcgui.Dialog().ok('الاتصال المشفر',https_problem)
	return worked

class CustomePlayer(xbmc.Player):
	def __init__( self, *args, **kwargs ):
		self.status = ''
	def onPlayBackStopped(self):
		self.status='failed'
	def onPlayBackStarted(self):
		self.status='playing'
		xbmc.sleep(1000)
	def onPlayBackError(self):
		self.status='failed'
	def onPlayBackEnded(self):
		self.status='failed'


class CustomThread:
	def __init__(self):
		self.statusDICT,self.resultsDICT = {},{}
	def start_new_thread(self,id,func,*args):
		self.statusDICT[id] = 'running'
		thread.start_new_thread(self.run,(id,func,args))
		time.sleep(0.001)
	def wait_finishing_all_threads(self):
		while 'running' in self.statusDICT.values():
			time.sleep(0.100)
	def run(self,id,func,args):
		self.resultsDICT[id] = func(*args)
		self.statusDICT[id] = 'finished'





# open file using one line example
"""
with open('S:\emad3.html', 'w') as file: file.write(block)
"""


# open file using manu line example
"""
#file = open('/data/emad.html', 'w')
#file.write(html)
#file.close()
"""


# encode & decode examples
"""
decode('utf8')
decode('unicode_escape')
decode('ascii')
decode('windows-1256')
"""


# timing using time.time()
"""
t1 = time.time()
t2 = time.time()
xbmcgui.Dialog().ok(str(t2-t1), '')
"""


# timing using timeit.timeit()
"""
timeit.timeit('import LIBRARY',number=1)
"""


# logfile open, read, and close
"""
playing = str(myplayer.isPlaying())
logfile = file(logfilename, 'rb')
logfile.seek(-4000, os.SEEK_END)
logfile = logfile.read()
logfile2 = logfile.split('['+addon_id+']:  Started playing video:')
if len(logfile2)==1: continue
else: logfile2 = logfile2[-1]
if 'CloseFile' in logfile2 or 'Attempt to use invalid handle' in logfile2:
	result = 'failed'
	xbmc.log('['+addon_id+']:   Failure: Video failed playing:  '+urlmessage, level=xbmc.LOGNOTICE)
	#break
elif 'Opening stream' in logfile2:
	result = 'playing'
	xbmc.log('['+addon_id+']:   Success: Video is playing successfully:  '+urlmessage, level=xbmc.LOGNOTICE)
	#break
"""


# to change the numbers name to digits
"""
lowLIST = [  ['']  ]
lowLIST.append(['الاولى','الأولى','الحادية','الحاديه','الواحدة','الواحده','الحادي','الواحد'])
lowLIST.append(['الثانية','الثانيه'])
lowLIST.append(['الثالثة','الثالثه'])
lowLIST.append(['الرابعة','الرابعه'])
lowLIST.append(['الخامسة','الخامسه'])
lowLIST.append(['السادسة','السادسه'])
lowLIST.append(['السابعة','السابعه'])
lowLIST.append(['الثامنة','الثامنه'])
lowLIST.append(['التاسعة','التاسعه'])
lowLIST.append(['العاشرة','العاشره'])
lowLIST.append(['العشرون','العشرين'])
lowLIST.append(['الثلاثون','الثلاثين'])
lowLIST.append(['الاربعون','الاربعين'])
lowLIST.append(['الخمسون','الخمسين'])
highLIST = [  ['']  ]
highLIST.append(['عشرة','عشر'])
highLIST.append(['و العشرون','و العشرين','والعشرون','والعشرين'])
highLIST.append(['و العشرون','و العشرين','والعشرون','والعشرين'])
highLIST.append(['و الثلاثون','و الثلاثين','والثلاثون','والثلاثين'])
highLIST.append(['و الاربعون','و الاربعين','والاربعون','والاربعين'])
cleanLIST = ['و الاخيرة','و الاخيره','والاخيرة','والاخيره','الاخيرة','الاخيره','كاملة','كامله']

def CLEAN_EPSIODE_NAME(title):
	#return title
	title2 = title.strip(' ').replace('  ',' ').replace('  ',' ')
	title2 = title2.replace('ـ','')
	episode = re.findall('(الحلقة|الحلقه) (\d+)',title2,re.DOTALL)
	if episode:
		for word in cleanLIST:
			title2 = title2.replace(word,'')
		number = int(episode[0][1])
		high,low = int(number/10),int(number%10)
		episode2 = []
		if low==0: high,low = 0,high+9
		for highTEXT in highLIST[high]:
			if highTEXT!='': highTEXT=' '+highTEXT
			for lowTEXT in lowLIST[low]:
				findTEXT = episode[0][0]+' '+episode[0][1]+' '+lowTEXT+highTEXT
				episode2 = re.findall(findTEXT,title2,re.DOTALL)
				if episode2: break
			if episode2: break
		if episode2: title2 = title2.replace(episode2[0],'')
		else: title2 = title2.replace(episode[0][0]+' '+episode[0][1],'')
		title2 = title2.strip(' ').replace('  ',' ').replace('  ',' ')
	#xbmcgui.Dialog().ok(title,title2)
	return title2
"""


# threading.Thread example
"""
items = re.findall('getVideoPlayer\(\'(.*?)\'',block,re.DOTALL)
for server in items:
	payload = { 'Ajax' : '1' , 'art' : artID , 'server' : server }
	data = urllib.urlencode(payload)
	#dataLIST.append(data)
	t = threading.Thread(target=linkFUNC,args=(data,linkLIST))
	t.start()
	threads.append(t)
for i in threads:
	i.join()
"""


# concurrent.futures threading example
"""
count = len(dataLIST)
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
	responcesDICT = dict( (executor.submit(openURL, url2, dataLIST[i], headers,'','HALACIMA-PLAY-3rd'), i) for i in range(count) )
for response in concurrent.futures.as_completed(responcesDICT):
	html = response.result()
	html = html.replace('SRC=','src=')
	links = re.findall('src=\'(.*?)\'',html,re.DOTALL)
	#if 'http' not in link: link = 'http:' + link
	linkLIST.append(links[0])
"""


