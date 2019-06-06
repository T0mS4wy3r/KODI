# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'http://alfatimi.tv'
script_name = 'ALFATIMI'
menu_name='_FTM_'

def MAIN(mode,url,text):
	if mode==60: MENU()
	elif mode==61: TITLES(url,text)
	elif mode==62: EPISODES(url)
	elif mode==63: PLAY(url)
	elif mode==64: MOSTS(text)
	elif mode==69: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',69)
	addDir(menu_name+'ما يتم مشاهدته الان',website0a,64,'','','recent_viewed_vids')
	addDir(menu_name+'الاكثر مشاهدة',website0a,64,'','','most_viewed_vids')
	addDir(menu_name+'اضيفت مؤخرا',website0a,64,'','','recently_added_vids')
	addDir(menu_name+'فيديو عشوائي',website0a,64,'','','random_vids')
	addDir(menu_name+'افلام ومسلسلات',website0a,61,'','','-1')
	addDir(menu_name+'البرامج الدينية',website0a,61,'','','-2')
	addDir(menu_name+'English Videos',website0a,61,'','','-3')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url,category):
	#xbmcgui.Dialog().ok('', category)
	moviesLIST = ['1239','1250','1245','20','1259','218','485','1238','1258','292']
	englishLIST = ['3030','628']
	if category in ['-1','-2','-3']:
		html = openURL(website0a+'/menu_level.php','','','','ALFATIMI-TITLES-1st')
	else:
		html = openURL(website0a+'/menu_level.php?cat='+category,'','','','ALFATIMI-TITLES-2nd')
	items = re.findall('href=\'(.*?)\'.*?>(.*?)<.*?>(.*?)</span>',html,re.DOTALL)
	startADD = False
	for link,title,count in items:
		title = unescapeHTML(title)
		title = title.strip(' ')
		cat = re.findall('cat=(.*?)&',link,re.DOTALL)[0]
		if category=='-1':
			if cat in moviesLIST:
				addDir(menu_name+title,website0a,61,'','',cat)
		elif category=='-2':
			if cat not in moviesLIST and cat not in englishLIST:
				addDir(menu_name+title,website0a,61,'','',cat)
		elif category=='-3':
			if cat in englishLIST:
				addDir(menu_name+title,website0a,61,'','',cat)
		elif startADD==False:
			if category==cat: startADD = True
		elif count=='1':
			if 'http' not in link: link = 'http:'+link
			addLink(menu_name+title,link,63)
		else: addDir(menu_name+title,website0a,61,'','',cat)
	if category not in ['-1','-2','-3']:
		EPISODES(website0a+'/videos.php?cat='+category)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def EPISODES(url):
	#xbmcgui.Dialog().ok(url , url)
	html = openURL(url,'','','','ALFATIMI-EPISODES-1st')
	html_blocks = re.findall('pagination(.*?)pagination',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('grid_view.*?src="(.*?)".*?<h2.*?href="(.*?)">(.*?)<',block,re.DOTALL)
	link = ''
	for img,link,title in items:
		title = title.strip(' ')
		if 'http' not in link: link = 'http:'+link
		addLink(menu_name+title,link,63,img)
	html_blocks=re.findall('(.*?)div',block,re.DOTALL)
	block=html_blocks[0]
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for link,page in items:
		link = website0a + '/videos.php' + link
		title = unescapeHTML(page)
		title = 'صفحة ' + title
		vars = re.findall('cat=(.*?)&page=(.*?)nnn',link+'nnn',re.DOTALL)
		category = vars[0][0]
		page = vars[0][1]
		#xbmcgui.Dialog().ok(category, page)
		if page=='1':
			addDir(menu_name+title,website0a,61,'','',category)
		else: addDir(menu_name+title,link,62)
	if 'page' in url: xbmcplugin.endOfDirectory(addon_handle)
	return link

def PLAY(url):
	if 'videos.php' in url:
		url = EPISODES(url)
	html = openURL(url,'','','','ALFATIMI-PLAY-1st')
	items = re.findall('playlistfile:"(.*?)"',html,re.DOTALL)
	url = items[0]
	if 'http' not in url: url = 'http:'+url
	#xbmcgui.Dialog().ok(url,'')
	PLAY_VIDEO(url,script_name)
	return

def MOSTS(category):
	payload = { 'mode' : category }
	url = 'http://alfatimi.tv/ajax.php'
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
	data = urllib.urlencode(payload)
	html = openURL(url,data,headers,'','ALFATIMI-GROUPS-1st')
	items = re.findall('href="(.*?)".*?title="(.*?)".*?src="(.*?)".*?href',html,re.DOTALL)
	for link,title,img in items:
		title = title.strip(' ')
		if 'http' not in link: link = 'http:'+link
		addLink(menu_name+title,link,63,img)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search == '': return
	#xbmcgui.Dialog().ok(search, website0a)
	new_search = search.replace(' ','+')
	url = website0a + '/search_result.php?query=' + new_search
	html = openURL(url,'','','','ALFATIMI-SEARCH-1st')
	html_blocks = re.findall('search_subs(.*?)</ul>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('cat=(.*?)&.*?>(.*?)<',block,re.DOTALL)
		for category,title in items:
			addDir(menu_name+title,website0a,61,'','',category)
	xbmcplugin.endOfDirectory(addon_handle)
	#except: xbmcgui.Dialog().ok('no results','لا توجد نتائج للبحث')
	return



