# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'http://www.alkawthartv.com'
script_name = 'ALKAWTHAR'
menu_name='[COLOR FFC89008]KWT [/COLOR]'

def MAIN(mode,url,page,text):
	if mode==130: MENU()
	#elif mode==131: TITLES(url)
	elif mode==132: CATEGORIES(url)
	elif mode==133: EPISODES(url,page)
	elif mode==134: PLAY(url)
	elif mode==135: LIVE()
	elif mode==139: SEARCH(text,page)
	return

def MENU():
	addLink(menu_name+'البث الحي لقناة الكوثر','',135,'','','IsPlayable=False')
	addDir(menu_name+'بحث في الموقع','',139,'',1)
	addDir(menu_name+'المسلسلات',website0a+'/category/543',132,'',1)
	addDir(menu_name+'الافلام',website0a+'/category/628',132,'',1)
	addDir(menu_name+'برامج الصغار والشباب',website0a+'/category/517',132,'',1)
	addDir(menu_name+'ابرز البرامج',website0a+'/category/1763',132,'',1)
	addDir(menu_name+'المحاضرات',website0a+'/category/943',132,'',1)
	addDir(menu_name+'عاشوراء',website0a+'/category/1353',132,'',1)
	addDir(menu_name+'البرامج الاجتماعية',website0a+'/category/501',132,'',1)
	addDir(menu_name+'البرامج الدينية',website0a+'/category/509',132,'',1)
	addDir(menu_name+'البرامج الوثائقية',website0a+'/category/553',132,'',1)
	addDir(menu_name+'البرامج السياسية',website0a+'/category/545',132,'',1)
	addDir(menu_name+'كتب',website0a+'/category/291',132,'',1)
	addDir(menu_name+'تعلم الفارسية',website0a+'/category/88',132,'',1)
	addDir(menu_name+'ارشيف البرامج',website0a+'/category/1279',132,'',1)
	"""
	html = openURL(website0a,'','','','ALKAWTHAR-MENU-1st')
	html_blocks=re.findall('dropdown-menu(.*?)dropdown-toggle',html,re.DOTALL)
	block = html_blocks[1]
	items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		title = title.strip(' ')
		typeLIST = ['/religious','/social','/political']
		if any(value in link for value in typeLIST):
			title = 'البرامج ' + title
		url = website0a + link
		if '/category' in url:
			addDir(menu_name+title,url,132,'',1)
		elif '/conductor' not in url:
			addDir(menu_name+title,url,131,'',1)
	"""
	xbmcplugin.endOfDirectory(addon_handle)
	return

"""
def TITLES(url):
	typeLIST = ['/religious','/social','/political','/films','/series']
	html = openURL(url,'','','','ALKAWTHAR-TITLES-1st')
	html_blocks = re.findall('titlebar(.*?)titlebar',html,re.DOTALL)
	block = html_blocks[0]
	if any(value in url for value in typeLIST):
		items = re.findall("src='(.*?)'.*?href='(.*?)'.*?>(.*?)<",block,re.DOTALL)
		for img,link,title in items:
			title = title.strip(' ')
			link = website0a + link
			addDir(menu_name+title,link,133,img,1)
	elif '/docs' in url:
		items = re.findall("src='(.*?)'.*?<h2>(.*?)</h2>.*?href='(.*?)'",block,re.DOTALL)
		for img,title,link in items:
			title = title.strip(' ')
			link = website0a + link
			addDir(menu_name+title,link,133,img,1)
	xbmcplugin.endOfDirectory(addon_handle)
	return
"""

def CATEGORIES(url):
	category = url.split('/')[-1]
	html = openURL(url,'','','','ALKAWTHAR-CATEGORIES-1st')
	html_blocks = re.findall('parentcat(.*?)</div>',html,re.DOTALL)
	if not html_blocks:
		EPISODES(url,'1')
		return
	block = html_blocks[0]
	items = re.findall("href='(.*?)'.*?>(.*?)<",block,re.DOTALL)
	for link,title in items:
		#categoryNew = url.split('/')[-1]
		#if category==categoryNew: continue
		title = title.strip(' ')
		link = website0a + link
		addDir(menu_name+title,link,132,'',1)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def EPISODES(url,page):
	#xbmcgui.Dialog().ok(url, page)
	html = openURL(url,'','','','ALKAWTHAR-EPISODES-1st')
	items = re.findall('totalpagecount=[\'"](.*?)[\'"]',html,re.DOTALL)
	if items[0]=='':
		xbmcgui.Dialog().ok('فرع فارغ','لا يوجد حاليا ملفات فيديو في هذا الفرع')
		return
	totalpages = int(items[0])
	name = re.findall('main-title.*?</a> >(.*?)<',html,re.DOTALL)
	if name: name = name[0].replace('\n','').strip(' ')
	else: name = xbmc.getInfoLabel('ListItem.Label')
	#xbmcgui.Dialog().ok(name, str(''))
	if '/category/' in url:
		category = url.split('/')[-1]
		url2 = website0a + '/category/' + category + '/' + page
		html = openURL(url2,'','','','ALKAWTHAR-EPISODES-3rd')
		html_blocks = re.findall('currentpagenumber(.*?)javascript',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('src="(.*?)".*?full(.*?)>.*?href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for img,type,link,title in items:
			if 'video' not in type: continue
			if 'مسلسل' in title and 'حلقة' not in title: continue
			title = title.replace('\r\n','')
			title = title.strip(' ')
			if 'مسلسل' in name and 'حلقة' in title and 'مسلسل' not in title:
				title = name + ' - ' + title
			link = website0a + link
			if category=='628':
				addDir(menu_name+title,link,133,img,1)
			else:
				addLink(menu_name+title,link,134,img)
	elif '/episode/' in url:
		html_blocks = re.findall('playlist(.*?)col-md-12',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall("video-track-text.*?loadVideo\('(.*?)','(.*?)'.*?>(.*?)<",block,re.DOTALL)
			for link,img,title in items:
				title = title.strip(' ')
				addLink(menu_name+title,link,134,img)
		elif '/category/628' in html:
				title = 'ملف التشغيل - ' + name
				addLink(menu_name+title,url,134)
		else:
			items = re.findall('id="Categories.*?href=\'(.*?)\'',html,re.DOTALL)
			category = items[0].split('/')[-1]
			url = website0a + '/category/' + category
			CATEGORIES(url)
			return
		totalpages = 0
		"""
			episodeID = url.split('/')[-1]
			items = re.findall('id="Categories.*?href=\'(.*?)\'',html,re.DOTALL)
			category = items[0].split('/')[-1]
			url2 = website0a + '/ajax/category/' + category + '/' + page
			html = openURL(url2,'','','','ALKAWTHAR-EPISODES-2nd')
			items = re.findall('src="(.*?)".*?href="(.*?)"> <h5>(.*?)<',html,re.DOTALL)
			for img,link,title in items:
				link = website0a + link
				episodeIDnew = link.split('/')[-1]
				if episodeIDnew==episodeID: continue
				title = title.strip(' ')
				addLink(menu_name+title,link,134,img)
		"""
	title = 'صفحة '
	for i in range(1,1+totalpages):
		if page!=str(i):
			addDir(menu_name+title+str(i),url,133,'',i)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	#xbmcgui.Dialog().ok(url, '')
	if '/news/' in url or '/episode/' in url:
		html = openURL(url,'','','','ALKAWTHAR-PLAY-1st')
		items = re.findall("mobilevideopath.*?value='(.*?)'",html,re.DOTALL)
		url = items[0]
	PLAY_VIDEO(url,script_name,'yes')
	return

def LIVE():
	html = openURL(website0a+'/live','','','','ALKAWTHAR-LIVE-1st')
	items = re.findall('file: "(.*?)"',html,re.DOTALL)
	url = items[0]
	PLAY_VIDEO(url,script_name,'no')
	return

def SEARCH(search,page):
	if search=='': search = KEYBOARD()
	if search == '': return
	if page=='': page = 1
	new_search = search.replace(' ','+')
	url = 'https://www.google.ca/search?q=site:alkawthartv.com+'+new_search+'&start='+str((page-1)*10)
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','ALKAWTHAR-SEARCH-1st')
	items = re.findall('rtl" href="/url\?q=(.*?)&.*?>(.*?)</a></h3>',html,re.DOTALL)
	#xbmcgui.Dialog().ok(str(items), str(items))
	found = False
	for link,title in items:
		title = title.replace('<b>','').replace('</b>','')
		title = title.replace('\xab','').replace('\xbb','')
		#xbmcgui.Dialog().ok(title, title)
		#xbmc.log('EMAD1 '+title+' 1EMAD',level=xbmc.LOGNOTICE)
		title = unescapeHTML(title)
		if '/category/' in link:	# or '/program/' in link:
			vars = link.split('/')
			category = vars[4]
			url = website0a + '/category/' + category
			if len(vars)>5:
				page1 = vars[5]
				addDir(menu_name+title,url,133,'',page1)
				found = True
			else:
				addDir(menu_name+title,url,132)
				found = True
		elif '/episode/' in link:
			addDir(menu_name+title,link,133,'',1)
			found = True
		#else:
		#	addDir(menu_name+title,url,132)
		#	found = True
	if found:
		name = 'صفحة '
		for i in range(1,8):
			if i==page: continue
			title = name + ' ' + str(i)
			addDir(menu_name+title,'',136,'',i)
	xbmcplugin.endOfDirectory(addon_handle)
	#else: xbmcgui.Dialog().ok('no results','لا توجد نتائج للبحث')
	return


