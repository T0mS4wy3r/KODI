# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'https://4helal.net'
#website0a = 'https://hd.4helal.tv'
#website0a = 'https://4helal.tv'
#website0a = 'https://www.4helal.tv'

script_name='HELAL'
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
	addDir(menu_name+'الأحدث',website0a+'/?type=latest',91)
	addDir(menu_name+'الأعلى تقيماً',website0a+'/?type=imdb',91)
	addDir(menu_name+'الأكثر مشاهدة',website0a+'/?type=view',91)
	addDir(menu_name+'المثبت',website0a+'/?type=pin',91)
	addDir(menu_name+'جديد الافلام',website0a+'/?type=newMovies',91)
	addDir(menu_name+'جديد الحلقات',website0a+'/?type=newEpisodes',91)
	#addLink('[COLOR FFC89008]=============[/COLOR]','',9999,'','','IsPlayable=no')
	#addDir(menu_name+'جديد الموقع',website0a,91)
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','HELAL-MENU-1st')
	#upper menu
	html_blocks = re.findall('class="mainmenu(.*?)nav',html,re.DOTALL)
	if html_blocks: block1 = html_blocks[0]
	else: block1 = ''
	#bottom menu
	html_blocks = re.findall('class="f-cats(.*?)div',html,re.DOTALL)
	if html_blocks: block2 = html_blocks[0].replace('</a></li>',' أخرى</a></li>')
	else: block2 = ''
	#xbmcgui.Dialog().ok(block,str(items))
	block = block1 + block2
	items = re.findall('<li><a href="(.*?)".*?>(.*?)<',block,re.DOTALL)
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
		headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 't' : search }
		data = urllib.urlencode(payload)
		html = openURL_cached(REGULAR_CACHE,url,data,headers,'','HELAL-ITEMS-1st')
	else:
		headers = { 'User-Agent' : '' }
		html = openURL_cached(REGULAR_CACHE,url,'',headers,'','HELAL-ITEMS-2nd')
	#xbmcgui.Dialog().ok('',str(html))
	html_blocks = re.findall('id="movies-items(.*?)class="clear',html,re.DOTALL)
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
		elif '/video/' in link: addLink(menu_name+title,link,92,img)
		else: addDir(menu_name+title,link,91,img)
	html_blocks = re.findall('class="pagination(.*?)div',html,re.DOTALL)
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
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','HELAL-EPISODES-1st')
	html_blocks = re.findall('id="episodes-panel(.*?)div',html,re.DOTALL)
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
	html = openURL_cached(LONG_CACHE,url,'',headers,'','HELAL-PLAY-1st')
	if any(value in html for value in adultLIST):
		xbmcgui.Dialog().notification('قم بتشغيل فيديو غيره','هذا الفيديو للكبار فقط ولا يعمل هنا')
		return
	html_blocks = re.findall('id="links-panel(.*?)div',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)"',block,re.DOTALL)
		for link in items:
			linkLIST.append(link)
	html_blocks = re.findall('nav-tabs"(.*?)video-panel-more',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('id="ajax-file-id.*?value="(.*?)"',block,re.DOTALL)
	id = items[0]
	#xbmcgui.Dialog().ok('',id)
	items = re.findall('data-server-src="(.*?)"',block,re.DOTALL)
	for link in items:
		if 'http' not in link: link = 'http:' + link
		link = unquote(link)
		linkLIST.append(link)
	"""
	items = re.findall('data-server="(.*?)"',block,re.DOTALL)
	for link in items:
		url2 = website0a + '/ajax.php?id='+id+'&ajax=true&server='+link
		#link = openURL_cached(LONG_CACHE,url2,'',headers,'','HELAL-PLAY-2nd')
		#linkLIST.append(link)
		urlLIST.append(url2)
		html = openURL_cached(LONG_CACHE,url2,'',headers,'','HELAL-PLAY-3rd')
		#xbmcgui.Dialog().ok(url2,html)
	count = len(urlLIST)
	import concurrent.futures
	with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
		responcesDICT = dict( (executor.submit(openURL, urlLIST[i], '', headers,'','HELAL-PLAY-2nd'), i) for i in range(0,count) )
	for response in concurrent.futures.as_completed(responcesDICT):
		linkLIST.append( response.result() )
	"""
	import RESOLVERS
	RESOLVERS.PLAY(linkLIST,script_name)
	return

def LATEST():
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','HELAL-LATEST-1st')
	html_blocks = re.findall('id="index-last-movie(.*?)id="index-slider-movie',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('src="(.*?)".*?href="(.*?)" title="(.*?)"',block,re.DOTALL)
	for img,link,title in items:
		if '/video/' in link: addLink(menu_name+title,link,92,img)
		else: addDir(menu_name+title,link,91,img)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def SEARCH(search=''):
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','+')
	url = website0a + '/search.php?'+search
	ITEMS(url)
	return



