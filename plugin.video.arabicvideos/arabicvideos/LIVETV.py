# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='LIVETV'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url):
	if mode==100: ITEMS(0)
	elif mode==101: ITEMS(1)
	elif mode==102: ITEMS(2)
	elif mode==104: PLAY(url)
	return

def ITEMS(type):
	menu_name='_TV'+str(type)+'_'
	client = dummyClientID(32)
	payload = { 'id' : '' , 'user' : client , 'function' : 'list_'+str(type) }
	data = urllib.urlencode(payload)
	#response = openURL_requests_cached(SHORT_CACHE,'POST', website0a, payload, '', True,'','LIVETV-ITEMS-1st')
	#html = response.text
	html = openURL_cached(LONG_CACHE,website0a,data,'','','LIVETV-ITEMS-1st')
	#html = html.replace('\r','')
	#xbmcgui.Dialog().ok(html,html)
	#file = open('s:/emad.html', 'w')
	#file.write(html)
	#file.close()
	items = re.findall('([^;\r\n]+?);;(.*?);;(.*?);;(.*?);;(.*?);;',html,re.DOTALL)
	if 'Not Allowed' in html:
		addLink(menu_name+'هذه الخدمة مخصصة للمبرمج فقط','',9999,'','','IsPlayable=no')
		#addLink(menu_name+'للأسف لا توجد قنوات تلفزونية لك','',9999,'','','IsPlayable=no')
		#addLink(menu_name+'هذه الخدمة مخصصة للاقرباء والاصدقاء فقط','',9999,'','','IsPlayable=no')
		#addLink(menu_name+'=========================','',9999,'','','IsPlayable=no')
		#addLink(menu_name+'Unfortunately, no TV channels for you','',9999,'','','IsPlayable=no')
		#addLink(menu_name+'It is for relatives & friends only','',9999,'','','IsPlayable=no')
	else:
		for i in range(len(items)):
			name = items[i][3]
			start = name[0:3]
			start = start.replace('al','Al')
			start = start.replace('El','Al')
			start = start.replace('AL','Al')
			start = start.replace('EL','Al')
			start = start.replace('Al-','Al')
			start = start.replace('Al ','Al')
			name = start+name[3:]
			items[i] = items[i][0],items[i][1],items[i][2],name,items[i][4]
		items = set(items)
		items = sorted(items, reverse=False, key=lambda key: key[0].lower())
		items = sorted(items, reverse=False, key=lambda key: key[3].lower())
		for source,server,id2,name,img in items:
			#if source in ['NT','YU','WS0','RL1','RL2']: continue
			if source!='URL': name = name + '   [COLOR FFC89008]' + source + '[/COLOR]'
			addLink(menu_name+' '+name,source+';;'+server+';;'+id2,104,img,'','IsPlayable=no')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(id):
	xbmcgui.Dialog().notification('جاري تشغيل القناة','')
	source,server,id2 = id.split(';;')
	url = ''
	#xbmcgui.Dialog().ok(source,id2)
	#try:
	if source=='URL': url = id2
	elif source=='GA':
		#xbmcgui.Dialog().ok(url,html)
		#xbmc.log(html, level=xbmc.LOGNOTICE)
		payload = { 'id' : '__ID2__' , 'user' : dummyClientID(32) , 'function' : 'playGA1' }
		response = openURL_requests_cached(LONG_CACHE,'POST',website0a,payload,'',False,'','LIVETV-PLAY-1st')
		proxyname,proxyurl = RANDOM_HTTPS_PROXY()
		url = response.headers['Location']+'||MyProxyUrl='+proxyurl
		response = openURL_requests_cached(30*MINUTE,'GET',url,'','',False,'','LIVETV-PLAY-2nd')
		cookies = response.cookies.get_dict()
		session = cookies['ASP.NET_SessionId']
		#html = response.text
		#session = re.findall('SessionID = "(.*?)"',html,re.DOTALL)
		#session = session[0]
		payload = { 'id' : '__ID2__' , 'user' : dummyClientID(32) , 'function' : 'playGA2' }
		response = openURL_requests_cached(LONG_CACHE,'POST',website0a,payload,'',False,'','LIVETV-PLAY-3rd')
		url = response.headers['Location'].replace('__ID2__',id2)
		headers = { 'Cookie' : 'ASP.NET_SessionId='+session }
		response = openURL_requests_cached(NO_CACHE,'GET',url,'',headers,False,'','LIVETV-PLAY-4th')
		html = response.text
		url = re.findall('resp":"(.*?)"',html,re.DOTALL)
		url = url[0]
		items = re.findall('http.*?m3u8',url,re.DOTALL)
		url = url.replace(items[0],'http://38.'+server+'777/'+id2+'_HD.m3u8')
		"""
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playGA' }
		response = openURL_requests_cached(NO_CACHE,'POST', website0a, payload, headers, False,'','LIVETV-PLAY-1st')
		url = response.headers['Location']
		html = response.text
		html = re.findall('\.(.*?)\.',html,re.DOTALL)
		html = base64.b64decode(html[0])
		items = re.findall('"lin.*?3":"(.*?)"',html,re.DOTALL)
		url = items[0].replace('\/','/')
		"""
	elif source=='NT':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playNT' }
		response = openURL_requests_cached(REGULAR_CACHE,'POST', website0a, payload, headers, False,'','LIVETV-PLAY-5th')
		url = response.headers['Location']
		url = url.replace('%20',' ')
		url = url.replace('%3D','=')
		if 'Learn' in id2:
			url = url.replace('NTNNile','')
			url = url.replace('learning1','Learning')
	elif source=='PL':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playPL' }
		response = openURL_requests_cached(REGULAR_CACHE,'POST', website0a, payload, headers, True,'','LIVETV-PLAY-6th')
		response = openURL_requests_cached(NO_CACHE,'POST', response.headers['Location'], '', {'Referer':response.headers['Referer']}, True,'','LIVETV-PLAY-7th')
		html = response.text
		items = re.findall('source src="(.*?)"',html,re.DOTALL)
		url = items[0]
	elif source in ['TA','FM','YU','WS1','WS2','RL1','RL2']:
		if source=='TA': id2 = id
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'play'+source }
		response = openURL_requests_cached(NO_CACHE,'POST', website0a, payload, headers, False,'','LIVETV-PLAY-8th')
		url = response.headers['Location']
		if source=='FM':
			#xbmcgui.Dialog().ok(url,'')
			response = openURL_requests_cached(NO_CACHE,'GET', url, '', '', False,'','LIVETV-PLAY-9th')
			url = response.headers['Location']
			url = url.replace('https','http')
	result = PLAY_VIDEO(url,script_name,'no')
	#except:
	#	xbmcgui.Dialog().ok('هذه القناة فيها مشكلة من الموقع الاصلي',page_error)
	return


