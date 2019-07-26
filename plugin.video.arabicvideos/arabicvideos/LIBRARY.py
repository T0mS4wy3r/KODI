# -*- coding: utf-8 -*-

# total cost = 0 ms
# Because they are already included with some other modules
import xbmcplugin,xbmcgui,xbmcaddon,sys,xbmc,os,re,time,thread # total cost = 0ms
import zlib,ssl,random,hashlib,base64,string,httplib,cPickle # total cost = 0ms
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
	import cPickle
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

WEBSITES = { 'AKOAM'		:['https://akoam.net']
			,'ALARAB'		:['https://vod.alarab.com']
			,'ALFATIMI'		:['http://alfatimi.tv']
			,'ALKAWTHAR'	:['http://www.alkawthartv.com']
			,'ALMAAREF'		:['http://www.almaareftv.com/old','http://www.almaareftv.com']
			,'ARABLIONZ'	:['https://arablionz.com']
			,'EGY4BEST'		:['https://egy4best.com']
			,'EGYBEST'		:['https://egy.best']
			,'HALACIMA'		:['https://www.halacima.net']
			,'HELAL'		:['https://4helal.net']
			,'IFILM'		:['http://ar.ifilmtv.com','http://en.ifilmtv.com','http://fa.ifilmtv.com','http://fa2.ifilmtv.com']
			,'LIVETV'		:['http://emadmahdi.pythonanywhere.com/listplay']
			,'MOVIZLAND'	:['https://movizland.online','https://m.movizland.online']
			,'PANET'		:['http://www.panet.co.il']
			,'SERIES4WATCH'	:['https://series4watch.net']
			,'SHAHID4U'		:['https://shahid4u.net']
			,'SHOOFMAX'		:['https://shoofmax.com','https://static.shoofmax.com']
			,'YOUTUBE'		:['https://www.youtube.com']
			}

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
dbfile = os.path.join(addoncachefolder,"webcache_"+addonVersion+".db")

MINUTE = 60
HOUR = 60*MINUTE
LONG_CACHE = 24*HOUR*3
REGULAR_CACHE = 16*HOUR
SHORT_CACHE = 2*HOUR
NO_CACHE = 0
now = time.time()

#LONG_CACHE = 0
#REGULAR_CACHE = 0
#SHORT_CACHE = 0

def SHOW_ERRORS(code=-1,reason=''):
	if code in [0,7]:
		if code==0: message = 'خطأ رقم صفر: هو خطأ غير معروف'
		else: message = 'خطأ رقم 7: هو خطأ DNS ومعناه تعذر ترجمة اسم الموقع الى رقمه'
		message += ' '+'والسبب قد يكون نوع من الحجب لهذا الموقع ولهذا لا يعمل باستخدام كودي. هل تريد معرفة كيف ترفع الحجب؟'
		yes = xbmcgui.Dialog().yesno('بعض المواقع لا تعمل عندك',message,'','','كلا','نعم')
		if yes==1: import PROBLEMS ; PROBLEMS.MAIN(195)
	else:
		yes = xbmcgui.Dialog().yesno('فشل في سحب الصفحة من الانترنيت','Error '+str(code)+': '+reason,'هل تريد معرفة الاسباب والحلول؟','','كلا','نعم')
		if yes==1:
			message = 'قد يكون هناك نوع من الحجب عندك'
			message += '\n'+'أو الانترنيت عندك مفصولة'
			message += '\n'+'أو الربط المشفر لا يعمل عندك'
			message += '\n'+'أو الموقع الاصلي غير متوفر الان'
			message += '\n'+'أو الموقع الاصلي غير هذه الصفحة والمبرمج لا يعلم'
			message += '\n\n'+'جرب مسح الكاش (من قائمة خدمات البرنامج)'
			message += '\n'+'أو أرسل سجل الاخطاء الى المبرمج (من قائمة خدمات البرنامج)'
			message += '\n'+'أو جرب طرق رفع الحجب (من قائمة البرنامج الرئيسية)'
			message += '\n'+'أو جرب طلب هذه الصفحة لاحقا'
			xbmcgui.Dialog().textviewer('فشل في سحب الصفحة من الانترنيت',message)
	return

#SHOW_ERRORS()
#SHOW_ERRORS(5,'dummy reason')
#ERROR
#xbmcgui.Dialog().ok('test',blocking_error)

def EXIT_IF_SOURCE(source,code,reason):
	NO_EXIT_LIST = [ 'LIBRARY-PLAY_VIDEO-1st'
					,'LIBRARY-GET_TESTED_PROXIES-1st'
					,'LIBRARY-openURL_PROXY-1st'
					,'LIBRARY-openURL_HTTPSPROXY-1st'
					,'LIBRARY-openURL_WEBPROXYTO-1st'
					,'LIBRARY-openURL_WEBPROXYTO-2nd'
					,'LIBRARY-openURL_KPROXYCOM-1st'
					,'LIBRARY-openURL_KPROXYCOM-2nd'
					,'LIBRARY-openURL_KPROXYCOM-3rd'
					,'PROGRAM-TEST_ALL_WEBSITES-1st'
					,'PROGRAM-TEST_ALL_WEBSITES-2nd'
					,'LIBRARY-GET_M3U8_RESOLUTIONS-1st' ]
	if 'RESOLVERS' not in source and source not in NO_EXIT_LIST:
		SHOW_ERRORS(code,reason)
		EXIT_PROGRAM(source)
	return

def DELETE_DATABASE_FILES():
	for filename in os.listdir(addoncachefolder):
		if 'webcache_' in filename and '.db' in filename:
			filename = os.path.join(addoncachefolder,filename)
			os.remove(filename)
	return ''

def addDir(name,url='',mode='',iconimage='',page='',text=''):
	if iconimage=='': iconimage = icon
	#xbmc.log('[ '+addon_id+' ]:   name:[ '+name+' ]', level=xbmc.LOGNOTICE)
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
	if duration!='':
		duration = '0:0:0:0:0:' + duration
		dummy,days,hours,minutes,seconds = duration.rsplit(':',4)
		duration = int(days)*24*HOUR+int(hours)*HOUR+int(minutes)*60+int(seconds)
		listitem.setInfo('Video', {'duration': duration})
	if IsPlayable=='yes': listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setContent(addon_handle, 'videos')
	xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=listitem,isFolder=False)
	return

def openURL_PROXY(url,data='',headers='',showDialogs='',source=''):
	#
	#
	# kproxy stopped and last used at 24 july 8:34pm to test cookie expiry
	#
	#
	if source=='PROGRAM-TEST_ALL_WEBSITES-2nd': html = '___Error___'
	else: html = openURL_cached(NO_CACHE,url,data,headers,showDialogs,'LIBRARY-openURL_PROXY-1st')
	#html = '___Error___'
	if '___Error___' in html:
		html = openURL_HTTPSPROXY(url,data,headers,showDialogs,'LIBRARY-openURL_PROXY-2nd')
		if '___Error___' in html:
			html = openURL_WEBPROXYTO(url,data,headers,showDialogs,'LIBRARY-openURL_PROXY-3rd')
			if '___Error___' in html:
				html = openURL_KPROXYCOM(url,data,headers,showDialogs,'LIBRARY-openURL_PROXY-4th')
				if '___Error___' in html:
					reason = 'Proxy failed'
					code = -1
					xbmc.log('[ '+addon_id+' ]:   Error: openURL_PROXY failed opening url   Code:[ '+str(code)+' ]   Reason:[ '+reason+' ]'+'   Source:[ '+source+' ]'+'   URL:[ '+url+' ]', level=xbmc.LOGERROR)
					EXIT_IF_SOURCE(source,code,reason)
	return html

def openURL_HTTPSPROXY(url,data='',headers='',showDialogs='',source=''):
	if '?MyProxyUrl=' not in url: url = url+'?MyProxyUrl='
	html = openURL_cached(NO_CACHE,url,data,headers,showDialogs,'LIBRARY-openURL_HTTPSPROXY-1st')
	if '___Error___' in html:
		source = 'LIBRARY-openURL_WEBPROXYTO-2nd'
		reason = 'HTTPS proxy fail'
		code = -1
		xbmc.log('[ '+addon_id+' ]:   Error: openURL_HTTPSPROXY failed opening url   Code:[ '+str(code)+' ]   Reason:[ '+reason+' ]'+'   Source:[ '+source+' ]'+'   URL:[ '+url+' ]', level=xbmc.LOGERROR)
		html = '___Error___:'+str(code)+':'+reason
	return html

def openURL_WEBPROXYTO(url,data='',headers='',showDialogs='',source=''):
	# Proxy + DNS
	# http://webproxy.to		http://69.64.52.22
	# cookie will expire after 30 miuntes (only if not used within these 30 minutes)
	response = openURL_requests_cached(30*MINUTE,'GET', 'http://webproxy.to','','',False,'no','LIBRARY-openURL_WEBPROXYTO-1st')
	html2 = response.text
	cookies = response.cookies.get_dict()
	s = cookies['s']
	cookies2 = 's=' + s
	headers2 = { 'Cookie' : cookies2 }
	if headers=='': headers3 = {}
	else: headers3 = headers
	if 'Cookie' in str(headers3): headers3['Cookie'] += ';' + cookies2
	else: headers3['Cookie'] = cookies2
	html = openURL_cached(NO_CACHE,'http://webproxy.to/browse.php?u='+quote(url)+'&b=128',data,headers3,showDialogs,'LIBRARY-openURL_WEBPROXYTO-2nd')
	html = unquote(html).replace('/browse.php?u='+url,'').replace('/browse.php?u=','').replace('&amp;b=128','')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	if '<!-- CONTENT START -->'.lower() in html.lower() or '___Error___' in html:
		source = 'LIBRARY-openURL_WEBPROXYTO-4th'
		reason = 'Cookie expired'
		code = -1
		xbmc.log('[ '+addon_id+' ]:   Error: openURL_WEBPROXYTO failed opening url   Code:[ '+str(code)+' ]   Reason:[ '+reason+' ]'+'   Source:[ '+source+' ]'+'   URL:[ '+url+' ]', level=xbmc.LOGERROR)
		html = '___Error___:'+str(code)+':'+reason
	return html

def openURL_KPROXYCOM(url,data='',headers='',showDialogs='',source=''):
	# Proxy + DNS
	# http://kproxy.com			http://37.187.147.158
	# cookie does not expire (tested for 3 days)
	# servers will expire after 20 miuntes (even if used within these 20 minutes)
	response = openURL_requests_cached(LONG_CACHE,'GET', 'http://kproxy.com','','',False,'no','LIBRARY-openURL_KPROXYCOM-1st')
	html2 = response.text
	cookies = response.cookies.get_dict()
	KP_DAT2 = cookies['KP_DAT2__']
	cookies2 = 'KP_DAT2__=' + KP_DAT2
	headers2 = { 'Cookie' : cookies2 }
	#payload2 = { 'page' : quote(url) }
	#data2 = urllib.urlencode(payload2)
	html2 = openURL_cached(20*MINUTE,'http://kproxy.com/doproxy.jsp?page='+quote(url),'',headers2,'no','LIBRARY-openURL_KPROXYCOM-2nd')
	proxyURL = re.findall('url=(.*?)"',html2,re.DOTALL)
	if proxyURL:
		proxyURL = proxyURL[0]
		if headers=='': headers3 = {}
		else: headers3 = headers
		if 'Cookie' in str(headers3): headers3['Cookie'] += ';' + cookies2
		else: headers3['Cookie'] = cookies2
		html = openURL_cached(NO_CACHE,proxyURL,data,headers3,showDialogs,'LIBRARY-openURL_KPROXYCOM-3rd')
	else:	#if not proxyURL:# or 'kproxy.com'.lower() not in html.lower():
		source = 'LIBRARY-openURL_KPROXYCOM-4th'
		reason = 'Cookie expired'
		code = -1
		xbmc.log('[ '+addon_id+' ]:   Error: openURL_KPROXYCOM failed opening url   Code:[ '+str(code)+' ]   Reason:[ '+reason+' ]'+'   Source:[ '+source+' ]'+'   URL:[ '+url+' ]', level=xbmc.LOGERROR)
		html = '___Error___:'+str(code)+':'+reason
	return html

def openURL_requests_cached(cacheperiod,method,url,data='',headers='',allow_redirects=True,showDialogs='',source=''):
	if cacheperiod==0: return openURL_requests(method,url,data,headers,allow_redirects,showDialogs,source)
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	t = (url,str(data),str(headers),str(allow_redirects),source)
	c.execute('SELECT response FROM responsecache WHERE url=? AND data=? AND headers=? AND allow_redirects=? AND source=?', t)
	rows = c.fetchall()
	conn.close()
	if rows:
		#message = 'found in cache'
		compressed = rows[0][0]
		text = zlib.decompress(compressed)
		response = cPickle.loads(text)
	else:
		#message = 'not found in cache'
		response = openURL_requests(method,url,data,headers,allow_redirects,showDialogs,source)
		code = response.status_code
		if code==200 or (code>=300 and code<=399):
			conn = sqlite3.connect(dbfile)
			c = conn.cursor()
			conn.text_factory = str
			text = cPickle.dumps(response)
			compressed = zlib.compress(text)
			t = (now+cacheperiod,url,str(data),str(headers),str(allow_redirects),source,sqlite3.Binary(compressed))
			c.execute("INSERT INTO responsecache VALUES (?,?,?,?,?,?,?)",t)
			conn.commit()
			conn.close()
	#xbmcgui.Dialog().notification(message,'')
	return response

def openURL_cached(cacheperiod,url,data='',headers='',showDialogs='',source=''):
	#t1 = time.time()
	#xbmcgui.Dialog().ok(unquote(url),source+'     cache(hours)='+str(cacheperiod/60/60))
	#nowTEXT = time.ctime(now)
	#xbmc.log('[ '+addon_id+' ]:   openURL_cached opening url   Source:[ '+source+' ]   URL:[ '+url+' ]', level=xbmc.LOGNOTICE)
	if cacheperiod==0: return openURL(url,data,headers,showDialogs,source)
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	#conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
	t = (url,str(data),str(headers),source)
	c.execute('SELECT html FROM htmlcache WHERE url=? AND data=? AND headers=? AND source=?', t)
	rows = c.fetchall()
	#html = repr(rows[0][0])
	conn.close()
	if rows:
		#message = 'found in cache'
		html = rows[0][0]
		#html = base64.b64decode(html)
		html = zlib.decompress(html)
	else:
		#message = 'not found in cache'
		html = openURL(url,data,headers,showDialogs,source)
		if '___Error___' not in html:
			conn = sqlite3.connect(dbfile)
			c = conn.cursor()
			conn.text_factory = str
			#html2 = base64.b64encode(html)
			compressed = zlib.compress(html)
			t = (now+cacheperiod,url,str(data),str(headers),source,sqlite3.Binary(compressed))
			c.execute("INSERT INTO htmlcache VALUES (?,?,?,?,?,?)",t)
			conn.commit()
			conn.close()
	#t2 = time.time()
	#xbmcgui.Dialog().notification(message,str(int(t2-t1))+' ms')
	return html

def openURL_requests(method,url,data='',headers='',allow_redirects=True,showDialogs='',source=''):
	import requests
	response = requests.request(method, url, data=data, headers=headers, verify=False, allow_redirects=allow_redirects)
	code = response.status_code
	reason = requests.status_codes._codes[code][0].replace('_',' ').capitalize()
	html = response.text
	#xbmcgui.Dialog().ok(str(url),str(code))
	if code!=200 and (code<=300 or code>=399):
		html = '___Error___:'+str(code)+':'+reason
		if 'google-analytics' not in url:
			xbmc.log('[ '+addon_id+' ]:   Error: openURL_requests failed opening url   Code:[ '+str(code)+' ]   Reason:[ '+reason+' ]'+'   Source:[ '+source+' ]'+'   URL:[ '+url+' ]', level=xbmc.LOGERROR)
		EXIT_IF_SOURCE(source,code,reason)
	return response

def GET_TESTED_PROXIES():
	#t1 = time.time()
	#def dummy():
	#	time.sleep(10)
	#	return
	headers = { 'User-Agent' : '' }
	testedPROXIES = {}
	threads = CustomThread()
	for id in PROXIES.keys():
		proxyname,proxyurl = PROXIES[id]
		url = 'https://www.google.com?MyProxyUrl='+proxyurl
		threads.start_new_thread('proxy_'+str(id),False,openURL_cached,NO_CACHE,url,'',headers,'','LIBRARY-GET_TESTED_PROXIES-1st')
		#xbmcgui.Dialog().notification('',str(id))
		#threads.start_new_thread(id,True,dummy)
	threads.wait_finishing_all_threads()
	#t2 = time.time()
	#xbmcgui.Dialog().ok(str(t2-t1),'')
	#return {}
	resultsDICT,statusDICT =	threads.resultsDICT,threads.statusDICT
	for id in resultsDICT.keys():
		status = statusDICT[id]
		html = resultsDICT[id]
		if '___Error___' not in html:
			id = int(id.replace('proxy_',''))
			proxyname,proxyurl = PROXIES[id]
			testedPROXIES[id] = (proxyname,proxyurl)
	return testedPROXIES

# Proxies were taken from http://free-proxy.cz
PROXIES = {
		 0:('فرنسا 1'			,'http://51.79.26.40:80')		# HTTPS France	4564kB/s 100% 4ms
		,1:('فرنسا 2'			,'http://51.79.26.40:8080')		# HTTPS France	5291kB/s 100% 9ms
		,2:('كندا كيبيك'		,'http://198.50.147.158:3128')	# HTTPS Canada	3725kB/s 100% 13ms
		,3:('اليونان 2'			,'http://178.128.229.122:80')	# HTTPS Greece	3078kB/s 100% 37ms
		,4:('اميركا نيوجيرسي'	,'http://198.211.102.155:8080')	# HTTPS USA		4675kB/s 100% 46ms
		,5:('اميركا ماسشيوستس'	,'http://140.82.63.13:8080')	# HTTPS USA		5879kB/s 100% 57ms
		,6:('اميركا نيويورك'	,'http://159.203.87.130:3128')	# HTTPS USA		6057kB/s 100% 118ms
		,7:('اميركا مشيغان'		,'http://155.138.141.68:8080')	# HTTPS USA		4445kB/s 100% 132ms
		,8:('كندا اونتاريو'		,'http://149.248.59.104:8080')	# HTTPS Canada	3447kB/s 100% 175ms
		,9:('اميركا كاليفورنيا'	,'http://159.203.204.101:8888')	# HTTPS USA		1514kB/s 100% 352ms
		,10:('المانيا'			,'http://5.9.142.124:3128')		# HTTPS Germany	1121kB/s 100% 385ms
		,11:('الصين'			,'http://49.51.155.45:8081')	# HTTPS China	        92.2% 473ms
		,12:('اوربا'			,'http://35.204.241.76:3128')	# HTTPS Europe	1271kB/s 100% 484ms
		,13:('بريطانيا'			,'http://45.77.90.217:8080')	# HTTPS UK		1183kB/s 100% 501ms
		,14:('روسيا'			,'http://195.182.135.237:3128')	# HTTPS Russia	819kB/s  100% 653ms
		,15:('اليونان 1'		,'http://178.128.229.122:8080')	# HTTPS Greece	4383kB/s 100% 657ms
		#,16:('اليونان 1'		,'http://178.128.229.122:8080')	# HTTPS Greece	4383kB/s 100% 657ms
		}

def openURL(url,data='',headers='',showDialogs='',source=''):
	if showDialogs=='': showDialogs='yes'
	html,code,reason = '',200,'OK'
	url2,proxy = url,False
	if '?MyProxyUrl=' in url:
		url2,proxyurl = url.split('?MyProxyUrl=')
		if headers=='': headers = { 'User-Agent' : '' }
		elif 'User-Agent' not in str(headers): headers['User-Agent'] = ''
		if 'http' not in proxyurl:
			randomNumber = random.randrange(0,16) # (0,6) means 6 servers
			proxyname,proxyurl = PROXIES[randomNumber]
			#proxyname,proxyurl = PROXIES[6] # 6 means 7th server
		proxy_handler = urllib2.ProxyHandler({ "http":proxyurl , "https":proxyurl })
		opener = urllib2.build_opener(proxy_handler)
		urllib2.install_opener(opener)
	else: url2 = url
	if   data=='' and headers=='': request = urllib2.Request(url2)
	elif data=='' and headers!='': request = urllib2.Request(url2,headers=headers)
	elif data!='' and headers=='': request = urllib2.Request(url2,data=data)
	elif data!='' and headers!='': request = urllib2.Request(url2,headers=headers,data=data)
	try:
		#ctx = ssl.create_default_context()
		#ctx.check_hostname = False
		#ctx.verify_mode = ssl.CERT_NONE
		#ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		if '?MyProxyUrl=' not in url:
			ctx = ssl._create_unverified_context()
			response = urllib2.urlopen(request,timeout=60,context=ctx)
		else: response = urllib2.urlopen(request,timeout=60)
		html = response.read()
		code = response.code
		response.close
	except urllib2.HTTPError as error:
		code = error.code
		reason = error.reason
	except urllib2.URLError as error:
		code = error.reason[0]
		reason = error.reason[1]
	if code!=200:
		message,send,showDialogs = '','no','no'
		html = '___Error___:'+str(code)+':'+reason
		"""	
		if 'google-analytics' in url2: send = showDialogs
		if showDialogs=='yes':
			xbmcgui.Dialog().ok('خطأ في الاتصال',html)
			if code==502 or code==7:
				xbmcgui.Dialog().ok('Website is not available','لا يمكن الوصول الى الموقع والسبب قد يكون من جهازك او من الانترنيت الخاصة بك او من الموقع كونه مغلق للصيانة او التحديث لذا يرجى المحاولة لاحقا')
				send = 'no'
			elif code==404:
				xbmcgui.Dialog().ok('File not found','الملف غير موجود والسبب غالبا هو من المصدر ومن الموقع الاصلي الذي يغذي هذا البرنامج')
			if send=='yes':
				yes = xbmcgui.Dialog().yesno('سؤال','هل تربد اضافة رسالة مع الخطأ لكي تشرح فيها كيف واين حصل الخطأ وترسل التفاصيل الى المبرمج ؟','','','كلا','نعم')
				if yes: message = ' \\n\\n' + KEYBOARD('Write a message   اكتب رسالة')
		if send=='yes': SEND_EMAIL('Error: From Arabic Videos',html+message,showDialogs,url,source)
		"""
		xbmc.log('[ '+addon_id+' ]:   Error: openURL failed opening url   Code:[ '+str(code)+' ]   Reason:[ '+reason+' ]'+'   Source:[ '+source+' ]'+'   URL:[ '+url+' ]', level=xbmc.LOGERROR)
		EXIT_IF_SOURCE(source,code,reason)
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
	#url3 = 's:\emad.m3u8999'
	result,subtitlemessage = 'canceled0',''
	if len(url3)==3:
		url,subtitle,httpd = url3
		if subtitle!='': subtitlemessage = '   Subtitle:[ '+subtitle+' ]'
	else: url,subtitle,httpd = url3,'',''
	xbmc.log('[ '+addon_id+' ]:   Playing video   URL:[ '+url+' ]'+subtitlemessage, level=xbmc.LOGNOTICE)
	videofiletype = re.findall('(\.ts|\.mp4|\.m3u|\.m3u8|\.mpd|\.mkv|\.flv|\.mp3)(|\?.*?|/\?.*?|\|.*?)&&',url+'&&',re.DOTALL)
	if videofiletype: videofiletype = videofiletype[0][0]
	else: videofiletype = ''
	if videofiletype=='.m3u8':
		headers = { 'User-Agent' : '' }
		titleLIST,linkLIST = M3U8_RESOLUTIONS(url,headers)
		if len(linkLIST)>1:
			selection = xbmcgui.Dialog().select('اختر الملف المناسب:', titleLIST)
			if selection == -1:
				xbmcgui.Dialog().notification('تم الغاء التشغيل','')
				return result
		else: selection = 0
		url = linkLIST[selection]
		if titleLIST[0]!='-1':
			xbmc.log('[ '+addon_id+' ]:   Playing selected video   Selection:[ '+titleLIST[selection]+' ]   URL:[ '+url+' ]'+subtitlemessage, level=xbmc.LOGNOTICE)
	url = url + '|User-Agent=&'
	if 'https://' in url and '/dash/' not in url: url = url + 'verifypeer=false'
	play_item = xbmcgui.ListItem(path=url)
	play_item.setProperty('inputstreamaddon', '')
	play_item.setMimeType('mime/x-type')
	myplayer = CustomePlayer()
	if videofiletype in ['.ts','.mkv','.mp4','.mp3','.flv']:
		#when set to "False" it makes glarabTV fails and make WS2TV opens fast
		play_item.setContentLookup(False)
	if 'rtmp' in url: ENABLE_RTMP(False)
	if videofiletype=='.mpd' or '/dash/' in url:
		ENABLE_MPD(False)
		play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
		play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
	if subtitle!='':
		play_item.setSubtitles([subtitle])
		#xbmc.log('[ '+addon_id+' ]:   Added subtitle to video   Subtitle:[ '+subtitle+' ]', level=xbmc.LOGNOTICE)
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
			xbmcgui.Dialog().notification('الفيديو يعمل','','',500)
			xbmc.log('[ '+addon_id+' ]:   Success: Video is playing   URL:[ '+url+' ]'+subtitlemessage, level=xbmc.LOGNOTICE)
			break
		elif result=='failed':
			xbmcgui.Dialog().notification('الفيديو لم يعمل','')
			xbmc.log('[ '+addon_id+' ]:   Error: Failed playing video   URL:[ '+url+' ]'+subtitlemessage, level=xbmc.LOGERROR)
			break
		xbmcgui.Dialog().notification(myplayer.status +'جاري تشغيل الفيديو','باقي '+str(timeout-i)+' ثانية')
	else:
		xbmcgui.Dialog().notification('الفيديو لم يعمل','')
		myplayer.stop()
		result = 'timeout'
		xbmc.log('[ '+addon_id+' ]:   Error: Timeout unknown problem   URL:[ '+url+' ]'+subtitlemessage, level=xbmc.LOGERROR)
	if result=='playing':
		addonVersion = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
		randomNumber = str(random.randrange(111111111111,999999999999))
		url2 = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addonVersion+'&av='+addonVersion+'&an=ARABIC_VIDEOS&ea='+website+'&z='+randomNumber
		html = openURL(url2,'','','no','LIBRARY-PLAY_VIDEO-1st')
	if httpd!='':
		#xbmcgui.Dialog().ok('click ok to shutdown the http server','')
		#html = openURL_cached(NO_CACHE,'http://localhost:64000/shutdown','','','','LIBRARY-PLAY_VIDEO-2nd')
		httpd.shutdown()
		#xbmcgui.Dialog().ok('http server is down','')
	EXIT_PROGRAM('LIBRARY-PLAY_VIDEO-3rd')
	#if 'https://' in url and result in ['failed','timeout']:
	#	working = HTTPS(False)
	#	if not working:
	#		xbmcgui.Dialog().ok('الاتصال مشفر','مشكلة ... هذا الفيديو يحتاج الى اتصال مشفر (ربط مشفر) ولكن للأسف الاتصال المشفر لا يعمل على جهازك')
	#		return 'https'

def EXIT_PROGRAM(source=''):
	xbmc.log('[ '+addon_id+' ]:   Exit: Program exited normally   Source:[ '+source+' ]', level=xbmc.LOGNOTICE)
	time.sleep(2)
	sys.exit()
	#raise SystemExit

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
			if size>300000: f.seek(-300000, os.SEEK_END)
			data = f.readlines()
			logfileNEW = ''.join(data[-400:])
			logfileNEW = base64.b64encode(logfileNEW)
		url = 'http://emadmahdi.pythonanywhere.com/sendemail'
		payload = { 'subject' : quote(subject) , 'message' : quote(message) , 'logfile' : logfileNEW }
		data = urllib.urlencode(payload)
		html = openURL_cached(NO_CACHE,url,data,'','','LIBRARY-SEND_EMAIL-1st')
		result = html[0:6]
		if showDialogs=='yes':
			if result == 'Error ':
				xbmcgui.Dialog().notification('للأسف','فشل في الارسال')
				xbmcgui.Dialog().ok('Failed sending the message','خطأ وفشل في ارسال الرسالة')
			else:
				xbmcgui.Dialog().notification('تم الارسال','بنجاح')
				xbmcgui.Dialog().ok('Message sent','تم ارسال الرسالة بنجاح')
	return html

def M3U8_RESOLUTIONS(url,headers=''):
	html = openURL_cached(NO_CACHE,url,'',headers,'','LIBRARY-GET_M3U8_RESOLUTIONS-1st')
	if 'TYPE=AUDIO' in html: return ['-1'],[url]
	if 'TYPE=VIDEO' in html: return ['-1'],[url]
	#if 'TYPE=SUBTITLES' in html: return ['-1'],[url]
	items1 = re.findall('RESOLUTION=\d+[x|X](\d+).*?\n(.*?)\n',html,re.DOTALL)
	items2 = re.findall('BANDWIDTH=(\d+).*?\n(.*?)\n',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,str(items1))
	if items1:
		items1 = set(items1)
		items1 = sorted(items1, reverse=True, key=lambda key: int(key[0]))
		titleLIST,linkLIST = [],[]
		for resolution,link in items1:
			if 'http' not in link: link = url.rsplit('/',1)[0] + '/' + link
			titleLIST.append(resolution)
			linkLIST.append(link)
	elif items2:
		items2 = set(items2)
		items2 = sorted(items2, reverse=True, key=lambda key: int(key[0]))
		titleLIST,linkLIST = [],[]
		for bitrate,link in items2:
			if 'http' not in link: link = url.rsplit('/',1)[0] + '/' + link
			bitrate = str(int(bitrate)/1024)+' kbps'
			titleLIST.append(bitrate)
			linkLIST.append(link)
	else: titleLIST,linkLIST = ['-1'],[url]
	#z = zip(titleLIST,linkLIST)
	#z = set(z)
	#z = sorted(z, reverse=True, key=lambda key: key[0])
	#titleLIST,linkLIST = zip(*z)
	#titleLIST,linkLIST = list(titleLIST),list(linkLIST)
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
	if show: html = openURL('https://www.google.com','','','','PROGRAM-HTTPS-1st')
	else: html = openURL_cached(LONG_CACHE,'https://www.google.com','','','','PROGRAM-HTTPS-2nd')
	if '___Error___' in html:
		worked = False
		https_problem = 'مشكلة ... الاتصال المشفر (الربط المشفر) لا يعمل عندك على كودي ... وعندك كودي غير قادر على استخدام المواقع المشفرة'
		xbmc.log('[ '+addon_id+' ]:   HTTPS Failed   Label:[ '+menulabel+' ]   Path:[ '+menupath+' ]', level=xbmc.LOGNOTICE)
		if show: xbmcgui.Dialog().ok('فشل في الاتصال المشفر',https_problem)
	else:
		worked = True
		if show: xbmcgui.Dialog().ok('الاتصال المشفر','جيد جدا ... الاتصال المشفر (الربط المشفر) يعمل عندك على كودي ... وعندك كودي قادر على استخدام المواقع المشفرة')
	return worked

def ENABLE_MPD(showDialogs=True):
	#result = xbmc.executeJSONRPC('{ "jsonrpc":"2.0", "method":"Addons.SetAddonEnabled", "id":1, "params": { "addonid":"inputstream.adaptive", "enabled":false }}')
	#xbmcgui.Dialog().ok('',str(result))
	enabled = xbmc.getCondVisibility('System.HasAddon(inputstream.adaptive)')
	if enabled==0:
		yes = xbmcgui.Dialog().yesno('هذه الاضافة عندك غير مفعلة','يجب تفعيل اضافة inputstream.adaptive لكي تعمل عندك فيديوهات نوع mpd فهل تريد تفعيل هذه الاضافة الان ؟','','','كلا','نعم')
		if yes==1:
			result = xbmc.executeJSONRPC('{ "jsonrpc":"2.0", "method":"Addons.SetAddonEnabled", "id":1, "params": { "addonid":"inputstream.adaptive", "enabled":true }}')
			if 'OK' in result: xbmcgui.Dialog().ok('تم التفعيل','')
			else: xbmcgui.Dialog().ok('التفعيل فشل','اضافة inputstream.adaptive غير موجودة عندك ويجب ان تقوم بتصيبها قبل محاولة تفعيلها')
	elif showDialogs==True: xbmcgui.Dialog().ok('هذه الاضافة عندك مفعلة','')
	return

def ENABLE_RTMP(showDialogs=True):
	#result = xbmc.executeJSONRPC('{ "jsonrpc":"2.0", "method":"Addons.SetAddonEnabled", "id":1, "params": { "addonid":"inputstream.rtmp", "enabled":false }}')
	#xbmcgui.Dialog().ok('',str(result))
	enabled = xbmc.getCondVisibility('System.HasAddon(inputstream.rtmp)')
	if enabled==0:
		yes = xbmcgui.Dialog().yesno('هذه الاضافة عندك غير مفعلة','يجب تفعيل اضافة inputstream.rtmp لكي تعمل عندك فيديوهات نوع rtmp فهل تريد تفعيل هذه الاضافة الان ؟','','','كلا','نعم')
		if yes==1:
			result = xbmc.executeJSONRPC('{ "jsonrpc":"2.0", "method":"Addons.SetAddonEnabled", "id":1, "params": { "addonid":"inputstream.rtmp", "enabled":true }}')
			if 'OK' in result: xbmcgui.Dialog().ok('تم التفعيل','')
			else: xbmcgui.Dialog().ok('التفعيل فشل','اضافة inputstream.rtmp غير موجودة عندك ويجب ان تقوم بتصيبها قبل محاولة تفعيلها')
	elif showDialogs==True: xbmcgui.Dialog().ok('هذه الاضافة عندك مفعلة','')
	return

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

class CustomThread():
	def __init__(self):
		self.statusDICT,self.resultsDICT = {},{}
	def start_new_thread(self,id,showNotification,func,*args):
		if showNotification: xbmcgui.Dialog().notification('',str(id))
		self.statusDICT[id] = 'running'
		thread.start_new_thread(self.run,(id,func,args))
		time.sleep(0.001)
	def wait_finishing_all_threads(self):
		while 'running' in self.statusDICT.values():
			time.sleep(0.100)
	def run(self,id,func,args):
		try:
			self.resultsDICT[id] = func(*args)
			self.statusDICT[id] = 'finished'
		except:
			self.resultsDICT[id] = '___Error___:-1:Threads function fail'
			self.statusDICT[id] = 'failed'






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
logfile2 = logfile.split('[ '+addon_id+' ]:  Started playing video:')
if len(logfile2)==1: continue
else: logfile2 = logfile2[-1]
if 'CloseFile' in logfile2 or 'Attempt to use invalid handle' in logfile2:
	result = 'failed'
	xbmc.log('[ '+addon_id+' ]:   Failure: Video failed playing  '+urlmessage, level=xbmc.LOGNOTICE)
	#break
elif 'Opening stream' in logfile2:
	result = 'playing'
	xbmc.log('[ '+addon_id+' ]:   Success: Video is playing successfully  '+urlmessage, level=xbmc.LOGNOTICE)
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


