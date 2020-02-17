# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='ARABLIONZ'
headers = { 'User-Agent' : '' }
menu_name='_ARL_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,text):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if mode==200: MENU()
	elif mode==201: TITLES(url)
	elif mode==202: PLAY(url)
	elif mode==203: EPISODES(url)
	elif mode==204: FILTER_MENU(url)
	elif mode==205: FILTER_SELECT(url)
	elif mode==209: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',209)
	#addDir(menu_name+'فلتر','',114,website0a)
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','ARABLIONZ-MENU-1st')
	html_blocks = re.findall('categories-tabs(.*?)advanced-search',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('data-get="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	for link,title in items:
		url = website0a+'/getposts?type=one&data='+link
		addDir(menu_name+title,url,201)
	html_blocks = re.findall('navigation-menu(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(http.*?)">(.*?)<',block,re.DOTALL)
	ignoreLIST = ['مسلسلات انمي مترجمة','الرئيسية']
	#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
	for link,title in items:
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
		#	if any(value in title for value in keepLIST):
			addDir(menu_name+title,link,201)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url):
	#xbmcgui.Dialog().ok(url,url)
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','ARABLIONZ-TITLES-1st')
	if 'getposts' in url: block = html
	else:
		html_blocks = re.findall('page-content(.*?)main-footer',html,re.DOTALL)
		block = html_blocks[0]
	items = re.findall('src="(.*?)".*?href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	allTitles = []
	itemLIST = ['مشاهدة','فيلم','اغنية','كليب','اعلان','هداف','مباراة','عرض','مهرجان','البوم']
	for img,link,title in items:
		if '/series/' in link: continue
		link = unquote(link).strip('/')
		title = unescapeHTML(title)
		title = title.strip(' ')
		if '/film/' in link or any(value in title for value in itemLIST):
			addLink(menu_name+title,link,202,img)
		elif '/episode/' in link and 'الحلقة' in title:
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = '_MOD_' + episode[0]
				if title not in allTitles:
					addDir(menu_name+title,link,203,img)
					allTitles.append(title)
		else: addDir(menu_name+title,link,203,img)
	html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<a href=["\'](http.*?)["\'].*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = unescapeHTML(link)
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			if title!='': addDir(menu_name+'صفحة '+title,link,201)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def EPISODES(url):
	episodesCount,items,itemsNEW = -1,[],[]
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','ARABLIONZ-EPISODES-1st')
	html_blocks = re.findall('ti-list-numbered(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		itemsNEW = []
		blocks = ''.join(html_blocks)
		items = re.findall('href="(.*?)"',blocks,re.DOTALL)
	items.append(url)
	items = set(items)
	#name = xbmc.getInfoLabel('ListItem.Label')
	for link in items:
		link = link.strip('/')
		title = '_MOD_' + link.split('/')[-1].replace('-',' ')
		sequence = re.findall('الحلقة-(\d+)',link.split('/')[-1],re.DOTALL)
		if sequence: sequence = sequence[0]
		else: sequence = '0'
		itemsNEW.append([link,title,sequence])
	items = sorted(itemsNEW, reverse=False, key=lambda key: int(key[2]))
	seasonsCount = str(items).count('/season/')
	episodesCount = str(items).count('/episode/')
	if seasonsCount>1 and episodesCount>0 and '/season/' not in url:
		for link,title,sequence in items:
			if '/season/' in link: addDir(menu_name+title,link,203)
	else:
		for link,title,sequence in items:
			if '/season/' not in link: addLink(menu_name+title,link,202)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	linkLIST = []
	parts = url.split('/')
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','ARABLIONZ-PLAY-1st')
	# watch links
	if '/watch/' in html:
		url2 = url.replace(parts[3],'watch')
		html2 = openURL_cached(REGULAR_CACHE,url2,'',headers,'','ARABLIONZ-PLAY-2nd')
		html_blocks = re.findall('stream-servers(.*?)</div>',html2,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('data-embedd="(.*?)".*?alt="(.*?)"',block,re.DOTALL)
			if items:
				id = re.findall('post_id=(.*?)"',html2,re.DOTALL)
				if id:
					id2 = id[0]
					for link,title in items:
						link = website0a+'/?postid='+id2+'&serverid='+link+'&name='+title+'__watch'
						linkLIST.append(link)
			else:
				items = re.findall('data-embedd=".*?(http.*?)("|&quot;)',block,re.DOTALL)
				for link,dummy in items:
					linkLIST.append(link)
	# download links
	if '/download/' in html:
		url2 = url.replace(parts[3],'download')
		html2 = openURL_cached(REGULAR_CACHE,url2,'',headers,'','ARABLIONZ-PLAY-3rd')
		id = re.findall('postId:"(.*?)"',html2,re.DOTALL)
		if id:
			id2 = id[0]
			headers2 = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
			url2 = website0a + '/ajaxCenter?_action=getdownloadlinks&postId='+id2
			html2 = openURL_cached(REGULAR_CACHE,url2,'',headers2,'','ARABLIONZ-PLAY-4th')
			html_blocks = re.findall('<h3.*?(\d+)(.*?)</div>',html2,re.DOTALL)
			if html_blocks:
				for resolution,block in html_blocks:
					items = re.findall('<td>(.*?)<.*?href="(.*?)"',block,re.DOTALL)
					for name,link in items:
						linkLIST.append(link+'?name='+name+' '+resolution+'__download')
			else:
				html_blocks = re.findall('<h6(.*?)</table>',html2,re.DOTALL)
				if not html_blocks: html_blocks = [html2]
				for block in html_blocks:
					"""
					name = re.findall('serversTitle.*?>(.*?)<',block,re.DOTALL)
					if name:
						name = name[-1].replace('الدقة ','').replace('\n','')
						if name!='': name = name + ' ـ '
					else: name = ''
					"""
					name = ''
					items = re.findall('href="(http.*?)"',block,re.DOTALL)
					for link in items:
						server = '&&' + link.split('/')[2].lower() + '&&'
						server = server.replace('.com&&','').replace('.co&&','')
						server = server.replace('.net&&','').replace('.org&&','')
						server = server.replace('.live&&','').replace('.online&&','')
						server = server.replace('&&hd.','').replace('&&www.','')
						server = server.replace('&&','')
						link = link + '?name=' + name + server + '__download'
						linkLIST.append(link)
	if len(linkLIST)==0:
		xbmcgui.Dialog().ok('','الرابط ليس فيه فيديو')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name)
	return

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','+')
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','ARABLIONZ-SEARCH-1st')
	html_blocks = re.findall('advanced-search secondary(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('data-cat="(.*?)".*?checkmark-bold">(.*?)</span>',block,re.DOTALL)
		categoryLIST,filterLIST = [],[]
		for category,title in items:
			categoryLIST.append(category)
			filterLIST.append(title)
		selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', filterLIST)
		if selection == -1 : return
		category = categoryLIST[selection]
		url = website0a + '/search?s='+search+'&category='+category
		TITLES(url)
	else: xbmcplugin.endOfDirectory(addon_handle)
	return



