# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='TV'
website0a = 'http://emadmahdi.pythonanywhere.com/listplay'


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
	html = openURL_cached(LONG_CACHE,website0a,data,'','','TV-ITEMS-1st')
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
		items = set(items)
		items = sorted(items, reverse=False, key=lambda key: key[0].lower())
		items = sorted(items, reverse=False, key=lambda key: key[3].lower())
		for source,server,id2,name,img in items:
			#if source in ['NT','YU','WS0','RL1','RL2']: continue
			if source!='URL': name = name + '   [COLOR FFC89008]' + source + '[/COLOR]'
			start = name[0:3]
			start = start.replace('al','Al')
			start = start.replace('El','Al')
			start = start.replace('AL','Al')
			start = start.replace('EL','Al')
			start = start.replace('Al-','Al')
			start = start.replace('Al ','Al')
			name = start+name[3:]
			addLink(menu_name+' '+name,source+';;'+server+';;'+id2,104,img,'','IsPlayable=no')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(id):
	xbmcgui.Dialog().notification('جاري تشغيل القناة','')
	import requests
	source,server,id2 = id.split(';;')
	url = ''
	#xbmcgui.Dialog().ok(source,id2)
	#try:
	if source=='URL': url = id2
	elif source=='GA':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playGA' }
		response = requests.request('POST', website0a, data=payload, headers=headers)
		html = response.text
		items = re.findall('"lin.*?3":"(.*?)"',html,re.DOTALL)
		url = items[0].replace('\/','/')
	elif source=='NT':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playNT' }
		response = requests.request('POST', website0a, data=payload, headers=headers, allow_redirects=False)
		url = response.headers['Location']
		url = url.replace('%20',' ')
		url = url.replace('%3D','=')
		if 'Learn' in id2:
			url = url.replace('NTNNile','')
			url = url.replace('learning1','Learning')
	elif source=='PM':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playPM' }
		response = requests.request('POST', website0a, data=payload, headers=headers)
		response = requests.request('POST', response.headers['Location'], headers={'Referer':response.headers['Referer']})
		html = response.text
		#xbmcgui.Dialog().ok('',html)
		items = re.findall('source src="(.*?)"',html,re.DOTALL)
		url = items[0]
	elif source in ['TA','FM','YU','WS1','WS2','RL1','RL2']:
		if source=='TA': id2 = id
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'play'+source }
		response = requests.request('POST', website0a, data=payload, headers=headers, allow_redirects=False)
		url = response.headers['Location']
		#if source=='WS2': url = url + '|User-Agent=&'
		if source=='FM':
			response = requests.request('GET', url, data='', headers='', allow_redirects=False)
			url = response.headers['Location']
			url = url.replace('https','http')
	if '.m3u8' in url:
		headers = { 'User-Agent' : '' }
		titleLIST,linkLIST = M3U8_RESOLUTIONS(url,headers)
		if len(linkLIST)>1:
			selection = xbmcgui.Dialog().select('اختر الملف المناسب:', titleLIST)
			if selection == -1: return
			else: url = linkLIST[selection]
		else: url = linkLIST[0]
	result = PLAY_VIDEO(url,script_name,'no')
	#except:
	#	xbmcgui.Dialog().ok('مشكلة من الموقع الاصلي',page_error)
	return


