# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='TV'
website0a = 'http://emadmahdi.pythonanywhere.com/listplay'

def MAIN(mode,url):
	if mode==100: ITEMS(1)
	elif mode==101: ITEMS(2)
	elif mode==104: PLAY(url)
	return

def ITEMS(type):
	menu_name='[COLOR FFC89008]TV'+str(type)+' [/COLOR]'
	client = dummyClientID(32)
	payload = { 'id' : '' , 'user' : client , 'function' : 'list'+str(type) }
	data = urllib.urlencode(payload)
	html = openURL(website0a,data,'','','TV-ITEMS-1st')
	#html = html.replace('\r','')
	#xbmcgui.Dialog().ok(html,html)
	#file = open('s:/emad.html', 'w')
	#file.write(html)
	#file.close()
	items = re.findall('(.*?):(.*?):(.*?):(.*?)\r\n',html,re.DOTALL)
	if items:
		items = set(items)
		itemsSorted = sorted(items, reverse=False, key=lambda key: key[1].lower())
		itemsSorted = sorted(itemsSorted, reverse=False, key=lambda key: key[2].lower())
		for source,id,name,img in itemsSorted:
			#xbmcgui.Dialog().ok(id,id)
			if source=='PL': continue
			name = name + ' ' + source
			name = name.replace('Al ','Al')
			name = name.replace('El ','El')
			name = name.replace('AL ','Al')
			name = name.replace('EL ','El')
			addLink(menu_name+name,source+id,104,img,'','no')
	elif html=='Not Allowed':
		addLink(menu_name+'للأسف لا توجد قنوات تلفزونية لك','',9999)
		addLink(menu_name+'هذه الخدمة مخصصة للاقرباء والاصدقاء فقط','',9999)
		addLink(menu_name+'=========================','',9999)
		addLink(menu_name+'Unfortunately, no TV channels for you','',9999)
		addLink(menu_name+'It is for relatives & friends only','',9999)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(id):
	source = id[0:2]
	id2 = id[2:99]
	url = ''
	xbmcgui.Dialog().notification('','Trying Channel ...')
	#xbmcgui.Dialog().ok(source,id2)
	from requests import request as requests_request
	if source=='GA':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playGA' }
		response = requests_request('POST', website0a, data=payload, headers=headers)
		html = response.text
		#xbmcgui.Dialog().ok(html,html)
		items = re.findall('"link3":"(.*?)"',html,re.DOTALL)
		url = items[0].replace('\/','/')
		#url = url.replace('#','')
	elif source=='NT':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playNT' }
		response = requests_request('POST', website0a, data=payload, headers=headers, allow_redirects=False)
		url = response.headers['Location']
		url = url.replace('%20',' ')
		url = url.replace('%3D','=')
		if 'Learn' in id2:
			url = url.replace('NTNNile','')
			url = url.replace('learning1','Learning')
	elif source=='PL':
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'playPL' }
		response = requests_request('POST', website0a, data=payload, headers=headers)
		response = requests_request('POST', response.headers['Location'], headers={'Referer':response.headers['Referer']})
		html = response.text
		#xbmcgui.Dialog().ok('',html)
		items = re.findall('source src="(.*?)"',html,re.DOTALL)
		url = items[0]
	elif source in ['TA','FM','YU','WS']:
		headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'id' : id2 , 'user' : dummyClientID(32) , 'function' : 'play'+source }
		response = requests_request('POST', website0a, data=payload, headers=headers, allow_redirects=False)
		url = response.headers['Location']
	#xbmcgui.Dialog().ok(url,'')
	PLAY_VIDEO(url,script_name,'no')
	return


