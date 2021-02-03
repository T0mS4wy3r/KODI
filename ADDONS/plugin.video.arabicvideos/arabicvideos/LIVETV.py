# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='LIVETV'
website0a = WEBSITES['PYTHON'][0]

def MAIN(mode,url):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==100: results = MENU()
	elif mode==101: results = ITEMS('0',True)
	elif mode==102: results = ITEMS('1',True)
	elif mode==103: results = ITEMS('2',True)
	elif mode==104: results = ITEMS('3',True)
	elif mode==105: results = PLAY(url)
	else: results = False
	return results

def MENU():
	addMenuItem('folder','[COLOR FFC89008]IPT    [/COLOR]'+'للمشتركين بخدمة IPTV','',230)
	addMenuItem('folder','[COLOR FFC89008]TV0   [/COLOR]'+'قنوات من مواقعها الأصلية','',101)
	addMenuItem('folder','[COLOR FFC89008]YUT   [/COLOR]'+'قنوات عربية من يوتيوب','',147)
	addMenuItem('folder','[COLOR FFC89008]YUT   [/COLOR]'+'قنوات أجنبية من يوتيوب','',148)
	addMenuItem('folder','[COLOR FFC89008]IFL    [/COLOR]'+'قناة آي فيلم من موقعهم','',28)
	addMenuItem('live','[COLOR FFC89008]MRF  [/COLOR]'+'قناة المعارف من موقعهم','',41)
	#addMenuItem('live','[COLOR FFC89008]KWT  [/COLOR]'+'قناة الكوثر من موقعهم','',135)
	addMenuItem('live','[COLOR FFC89008]PNT  [/COLOR]'+'قناة هلا من موقع بانيت','',38)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]TV1  [/COLOR]'+'قنوات تلفزيونية عامة','',102)
	addMenuItem('folder','[COLOR FFC89008]TV2  [/COLOR]'+'قنوات تلفزيونية خاصة','',103)
	addMenuItem('folder','[COLOR FFC89008]TV3  [/COLOR]'+'قنوات تلفزيونية للفحص','',104)
	return

def ITEMS(menu,show=True):
	menu_name='_TV'+menu+'_'
	client = dummyClientID(32)
	payload = { 'id' : '' , 'user' : client , 'function' : 'list' , 'menu' : menu }
	#data = urllib.urlencode(payload)
	#LOG_THIS('NOTICE',str(payload))
	#LOG_THIS('NOTICE',str(data))
	#response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST', website0a, payload, '', True,'','LIVETV-ITEMS-1st')
	#html = response.content
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST',website0a,payload,'','','','LIVETV-ITEMS-1st')
	html = response.content
	#html = html.replace('\r','')
	#DIALOG_OK(html,html)
	#file = open('s:/emad.html', 'w')
	#file.write(html)
	#file.close()
	items = re.findall('([^;\r\n]+?);;(.*?);;(.*?);;(.*?);;(.*?);;',html,re.DOTALL)
	if 'Not Allowed' in html:
		if show: addMenuItem('link',menu_name+'هذه الخدمة مخصصة للمبرمج فقط','',9999)
		#if show: DIALOG_OK('','هذه الخدمة مخصصة للمبرمج فقط')
		#addMenuItem('link',menu_name+'للأسف لا توجد قنوات تلفزونية لك','',9999)
		#addMenuItem('link',menu_name+'هذه الخدمة مخصصة للاقرباء والاصدقاء فقط','',9999)
		#addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
		#addMenuItem('link',menu_name+'Unfortunately, no TV channels for you','',9999)
		#addMenuItem('link',menu_name+'It is for relatives & friends only','',9999)
	else:
		for i in range(len(items)):
			name = items[i][3]
			start = name[0:2]
			start = start.replace('al','Al')
			start = start.replace('El','Al')
			start = start.replace('AL','Al')
			start = start.replace('EL','Al')
			name = start+name[2:]
			start = name[0:3]
			start = start.replace('Al-','Al')
			start = start.replace('Al ','Al')
			name = start+name[3:]
			items[i] = items[i][0],items[i][1],items[i][2],name,items[i][4]
		items = set(items)
		items = sorted(items, reverse=False, key=lambda key: key[0].lower())
		items = sorted(items, reverse=False, key=lambda key: key[3].lower())
		for source,server,id2,name,img in items:
			if '#' in source: continue
			#if source in ['NT','YU','WS0','RL1','RL2']: continue
			if source!='URL': name = name+'   [COLOR FFC89008]'+source+'[/COLOR]'
			url = source+';;'+server+';;'+id2+';;'+menu
			addMenuItem('live',menu_name+''+name,url,105,img)
	return

def PLAY(id):
	#DIALOG_BUSY('start')
	#DIALOG_NOTIFICATION('جاري تشغيل القناة','')
	source,server,id2,menu = id.split(';;')
	url = ''
	#DIALOG_OK(source,id2)
	#try:
	if source=='URL': url = id2
	elif source=='GA':
		#DIALOG_OK(url,html)
		#xbmc.log(html, level=xbmc.LOGNOTICE)
		payload = { 'id' : '__ID2__' , 'user' : dummyClientID(32) , 'function' : 'playGA1' , 'menu' : menu }
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST',website0a,payload,'',False,'','LIVETV-PLAY-1st')
		if 'Not Allowed' in response.content:
			DIALOG_OK('رسالة من المبرمج','هذه الخدمة مخصصة للمبرمج فقط')
			#DIALOG_BUSY('stop')
			return
		#proxyname,proxyurl = RANDOM_HTTPS_PROXY()
		url = response.headers['Location']#+'||MyProxyUrl='+proxyurl
		#DIALOG_OK(url,'')
		response = OPENURL_REQUESTS_CACHED(VERY_SHORT_CACHE,'GET',url,'','',False,'','LIVETV-PLAY-2nd')
		cookies = response.cookies.get_dict()
		session = cookies['ASP.NET_SessionId']
		#html = response.content
		#session = re.findall('SessionID = "(.*?)"',html,re.DOTALL)
		#session = session[0]
		payload = { 'id' : '__ID2__' , 'user' : dummyClientID(32) , 'function' : 'playGA2' , 'menu' : menu }
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST',website0a,payload,'',False,'','LIVETV-PLAY-3rd')
		if 'Not Allowed' in response.content:
			DIALOG_OK('رسالة من المبرمج','هذه الخدمة مخصصة للمبرمج فقط')
			#DIALOG_BUSY('stop')
			return
		url = response.headers['Location'].replace('__ID2__',id2)
		headers = { 'Cookie' : 'ASP.NET_SessionId='+session }
		response = OPENURL_REQUESTS_CACHED(NO_CACHE,'GET',url,'',headers,False,'','LIVETV-PLAY-4th')
		html = response.content
		url = re.findall('resp":"(http.*?m3u8)(.*?)"',html,re.DOTALL)
		link = url[0][0]
		params = url[0][1]
		#url = link+params
		url_HD = 'http://38.'+server+'777/'+id2+'_HD.m3u8'+params
		url_SD1 = url_HD.replace('36:7','40:7').replace('_HD.m3u8','.m3u8')
		url_SD2 = url_HD.replace('36:7','42:7').replace('_HD.m3u8','.m3u8')
		titleLIST = ['HD','SD1','SD2']
		linkLIST = [url_HD,url_SD1,url_SD2]
		selection = 0
		#selection = DIALOG_SELECT('اختر الملف المناسب:', titleLIST)
		if selection == -1:
			#DIALOG_BUSY('stop')
			return
		else: url = linkLIST[selection]
		#DIALOG_OK(items[0],url)
		"""
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playGA' , 'menu' : menu }
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST', website0a, payload, headers, False,'','LIVETV-PLAY-1st')
		url = response.headers['Location']
		html = response.content
		html = re.findall('\.(.*?)\.',html,re.DOTALL)
		html = base64.b64decode(html[0])
		items = re.findall('"lin.*?3":"(.*?)"',html,re.DOTALL)
		url = items[0].replace('\/','/')
		"""
	elif source=='NT':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playNT' , 'menu' : menu }
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST', website0a, payload, headers, False,'','LIVETV-PLAY-5th')
		if 'Not Allowed' in response.content:
			DIALOG_OK('رسالة من المبرمج','هذه الخدمة مخصصة للمبرمج فقط')
			#DIALOG_BUSY('stop')
			return
		url = response.headers['Location']
		url = url.replace('%20',' ')
		url = url.replace('%3D','=')
		if 'Learn' in id2:
			url = url.replace('NTNNile','')
			url = url.replace('learning1','Learning')
	elif source=='PL':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playPL' , 'menu' : menu }
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST', website0a, payload, headers, True,'','LIVETV-PLAY-6th')
		if 'Not Allowed' in response.content:
			DIALOG_OK('رسالة من المبرمج','هذه الخدمة مخصصة للمبرمج فقط')
			#DIALOG_BUSY('stop')
			return
		response = OPENURL_REQUESTS_CACHED(NO_CACHE,'POST', response.headers['Location'], '', {'Referer':response.headers['Referer']}, True,'','LIVETV-PLAY-7th')
		html = response.content
		items = re.findall('source src="(.*?)"',html,re.DOTALL)
		url = items[0]
	elif source in ['TA','FM','YU','WS1','WS2','RL1','RL2']:
		if source=='TA': id2 = id
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'play'+source , 'menu' : menu }
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST', website0a, payload, headers, False,'','LIVETV-PLAY-8th')
		if 'Not Allowed' in response.content:
			DIALOG_OK('رسالة من المبرمج','هذه الخدمة مخصصة للمبرمج فقط')
			#DIALOG_BUSY('stop')
			return
		url = response.headers['Location']
		if source=='FM':
			#DIALOG_OK(url,'')
			response = OPENURL_REQUESTS_CACHED(NO_CACHE,'GET', url, '', '', False,'','LIVETV-PLAY-9th')
			url = response.headers['Location']
			url = url.replace('https','http')
	#DIALOG_BUSY('stop')
	result = PLAY_VIDEO(url,script_name,'live')
	#except:
	#	DIALOG_OK('هذه القناة فيها مشكلة من الموقع الاصلي',page_error)
	return


