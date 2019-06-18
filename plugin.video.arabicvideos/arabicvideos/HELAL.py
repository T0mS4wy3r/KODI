# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'https://4helal.tv'
script_name='4HELAL'
headers = { 'User-Agent' : '' }
menu_name='_HEL_'

def MAIN(mode,url,text):
	if mode==90: MENU()
	elif mode==91: ITEMS(url)
	elif mode==92: PLAY(url)
	elif mode==94: LATEST()
	elif mode==95: EPISODES(url)
	elif mode==99: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',99)
	addDir(menu_name+'المضاف حديثا','',94)
	addDir(menu_name+'جديد الموقع',website0a,91)
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','4HELAL-MENU-1st')
	html_blocks = re.findall('mainmenu(.*?)nav',html,re.DOTALL)
	#upper menu
	block1 = html_blocks[0]
	html_blocks = re.findall('class="f-cats(.*?)div',html,re.DOTALL)
	#bottom menu
	block2 = html_blocks[0].replace('</a></li>',' أخرى</a></li>')
	block = block1 + block2
	items = re.findall('<li><a href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	#xbmcgui.Dialog().ok(block,str(items))
	ignoreLIST = ['افلام للكبار فقط']
	for link,title in items:
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
			addDir(menu_name+title,link,91)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def ITEMS(url):
	if '/search.php' in url:
		parts = url.split('?')
		url,search = parts
		search = search.replace('%20',' ')
		headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 't' : search }
		data = urllib.urlencode(payload)
		html = openURL_cached(REGULAR_CACHE,url,data,headers,'','4HELAL-SEARCH-1st')
	else:
		headers = { 'User-Agent' : '' }
		html = openURL_cached(REGULAR_CACHE,url,'',headers,'','4HELAL-ITEMS-1st')
	html_blocks = re.findall('movies-items(.*?)pagination',html,re.DOTALL)
	if html_blocks: block = html_blocks[0]
	else: block = ''
	items = re.findall('background-image:url\((.*?)\).*?href="(.*?)".*?movie-title">(.*?)<',block,re.DOTALL)
	allTitles = []
	for img,link,title in items:
		if 'الحلقة' in title and '/c/' not in url and '/cat/' not in url:
			episode = re.findall('(.*?) الحلقة [0-9]+',title,re.DOTALL)
			if episode:
				title = '_MOD_'+episode[0]
				if title not in allTitles:
					addDir(menu_name+title,link,95,img)
					allTitles.append(title)
		elif '/video/' in link:
			addLink(menu_name+title,link,92,img)
		else:
			addDir(menu_name+title,link,91,img)
	html_blocks = re.findall('pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<a href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			addDir(menu_name+'صفحة '+title,link,91)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def EPISODES(url):
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','4HELAL-ITEMS-1st')
	html_blocks = re.findall('episodes-panel(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	img = re.findall('image":.*?"(.*?)"',html,re.DOTALL)[0]
	name = re.findall('itemprop="title">(.*?)<',html,re.DOTALL)
	if name: name = name[1]
	else: name = xbmc.getInfoLabel('ListItem.Label')
	#name = name.replace('_MOD_','').replace('HEL ','')
	items = re.findall('href="(.*?)".*?name">(.*?)<',block,re.DOTALL)
	for link,title in items:
		title = name+' - '+title
		addLink(menu_name+title,link,92,img)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	linkLIST,urlLIST = [],[]
	adultLIST = ['R - للكبار فقط','PG-18','PG-16','TV-MA']
	html = openURL_cached(LONG_CACHE,url,'',headers,'','4HELAL-PLAY-1st')
	if any(value in html for value in adultLIST):
		xbmcgui.Dialog().notification('قم بتشغيل فيديو غيره','هذا الفيديو للكبار فقط ولا يعمل هنا')
		return
	html_blocks = re.findall('links-panel(.*?)div',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)"',block,re.DOTALL)
		for link in items:
			linkLIST.append(link)
	html_blocks = re.findall('nav-tabs(.*?)video-panel-more',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('ajax-file-id.*?value="(.*?)"',block,re.DOTALL)
	id = items[0]
	#xbmcgui.Dialog().ok('',id)
	items = re.findall('data-server-src="(.*?)"',block,re.DOTALL)
	for link in items:
		link = unquote(link)
		linkLIST.append(link)
	"""
	items = re.findall('data-server="(.*?)"',block,re.DOTALL)
	for link in items:
		url2 = website0a + '/ajax.php?id='+id+'&ajax=true&server='+link
		#link = openURL_cached(LONG_CACHE,url2,'',headers,'','4HELAL-PLAY-2nd')
		#linkLIST.append(link)
		urlLIST.append(url2)
		html = openURL_cached(LONG_CACHE,url2,'',headers,'','4HELAL-PLAY-2nd')
		#xbmcgui.Dialog().ok(url2,html)
	count = len(urlLIST)
	import concurrent.futures
	with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
		responcesDICT = dict( (executor.submit(openURL, urlLIST[i], '', headers,'','4HELAL-PLAY-2nd'), i) for i in range(0,count) )
	for response in concurrent.futures.as_completed(responcesDICT):
		linkLIST.append( response.result() )
	"""
	import RESOLVERS
	RESOLVERS.PLAY(linkLIST,script_name)
	return

def LATEST():
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','4HELAL-LATEST-1st')
	html_blocks = re.findall('index-last-movie(.*?)index-slider-movie',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('src="(.*?)".*?href="(.*?)" title="(.*?)"',block,re.DOTALL)
	for img,link,title in items:
		if '/video/' in link:
			addLink(menu_name+title,link,92,img)
		else:
			addDir(menu_name+title,link,91,img)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def SEARCH(search=''):
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','%20')
	url = website0a + '/search.php?'+search
	ITEMS(url)
	return



