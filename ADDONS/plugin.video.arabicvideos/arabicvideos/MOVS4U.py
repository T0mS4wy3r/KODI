# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='MOVS4U'
menu_name='_MVF_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['انواع افلام','جودات افلام']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==380: results = MENU(url)
	elif mode==381: results = TITLES(url,text)
	elif mode==382: results = PLAY(url)
	elif mode==383: results = EPISODES(url)
	elif mode==389: results = SEARCH(text)	
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',389,'','','_REMEMBERRESULTS_')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder',menu_name+'المميزة',website0a,381,'','','featured')
	addMenuItem('folder',menu_name+'الجانبية',website0a,381,'','','sider')
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a,'','','','','MOVS4U-MENU-1st')
	html = response.content
	items = re.findall('<header>.*?<h2>(.*?)<',html,re.DOTALL)
	for seq in range(len(items)):
		title = items[seq]
		addMenuItem('folder',website+'___'+menu_name+title,website0a,381,'','','latest'+str(seq))
	block = ''
	html_blocks = re.findall('class="menu"(.*?)id="contenedor"',html,re.DOTALL)
	if html_blocks: block += html_blocks[0]
	html_blocks = re.findall('class="sidebar(.*?)aside',html,re.DOTALL)
	if html_blocks: block += html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	first = True
	for link,title in items:
		title = unescapeHTML(title)
		if title=='الأعلى مشاهدة':
			if first: 
				title = 'الافلام '+title
				first = False
			else: title = 'المسلسلات '+title
		if title not in ignoreLIST:
			addMenuItem('folder',website+'___'+menu_name+title,link,381)
	return html

def TITLES(url,type):
	#DIALOG_OK(url,type)
	#WRITE_THIS(html)
	block,items = [],[]
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','MOVS4U-TITLES-1st')
	html = response.content
	if type=='search':
		html_blocks = re.findall('class="search-page"(.*?)class="sidebar',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('img src="(.*?)".*?href="(.*?)">(.*?)<',block,re.DOTALL)
	elif type=='sider':
		html_blocks = re.findall('class="widget(.*?)class="widget',html,re.DOTALL)
		block = html_blocks[0]
		z = re.findall('href="(.*?)".*?img src="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
		linkLIST,imgLIST,titleLIST = zip(*z)
		items = zip(imgLIST,linkLIST,titleLIST)
	elif type=='featured':
		html_blocks = re.findall('id="slider-movies-tvshows"(.*?)<header>',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('img src="(.*?)".*?href="(.*?)".*?"title">(.*?)<',block,re.DOTALL)
	elif 'latest' in type:
		seq = int(type[-1:])
		html = html.replace('<header>','<end><start>')
		html = html.replace('<div class="sidebar','<end><div class="sidebar')
		html_blocks = re.findall('<start>(.*?)<end>',html,re.DOTALL)
		block = html_blocks[seq]
		if seq==2: items = re.findall('img src="(.*?)".*?href="(.*?)">(.*?)<',block,re.DOTALL)
	else:
		html_blocks = re.findall('class="content"(.*?)class="(pagination|sidebar)',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0][0]
			if '/collection/' in url:
				items = re.findall('img src="(.*?)".*?href="(.*?)">(.*?)<',block,re.DOTALL)
			elif '/quality/' in url:
				items = re.findall('img src="(.*?)".*?href="(.*?)".*?"title">(.*?)<',block,re.DOTALL)
	if not items and block:
		items = re.findall('img src="(.*?)".*?href=.*?href="(.*?)">(.*?)</div>',block,re.DOTALL)
	allTitles = []
	for img,link,title in items:
		if 'serie' in title:
			title = re.findall('^(.*?)<.*?serie">(.*?)<',title,re.DOTALL)
			title = title[0][1]#+' - '+title[0][0]
			if title in allTitles: continue
			allTitles.append(title)
			title = '_MOD_'+title
		title2 = re.findall('^(.*?)<',title,re.DOTALL)
		if title2: title = title2[0]
		title = unescapeHTML(title)
		if '/tvshows/' in link: addMenuItem('folder',menu_name+title,link,383,img)
		elif '/episodes/' in link: addMenuItem('folder',menu_name+title,link,383,img)
		elif '/seasons/' in link: addMenuItem('folder',menu_name+title,link,383,img)
		elif '/collection/' in link: addMenuItem('folder',menu_name+title,link,381,img)
		else: addMenuItem('video',menu_name+title,link,382,img)
	html_blocks = re.findall('class="pagination".*?Page (.*?) of (.*?)<(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		current = html_blocks[0][0]
		last = html_blocks[0][1]
		block = html_blocks[0][2]
		items = re.findall("href='(.*?)'.*?>(.*?)<",block,re.DOTALL)
		for link,title in items:
			if title=='' or title==last: continue
			addMenuItem('folder',menu_name+'صفحة '+title,link,381,'','',type)
		#if title==last:
		link = link.replace('/page/'+title+'/','/page/'+last+'/')
		addMenuItem('folder',menu_name+'اخر صفحة '+last,link,381,'','',type)
	return

def EPISODES(url):
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','MOVS4U-EPISODES-1st')
	html = response.content
	ratingLIST = re.findall('class="C rated".*?>(.*?)<',html,re.DOTALL)
	if ratingLIST and RATING_CHECK(script_name,url,ratingLIST,False):
		addMenuItem('link',menu_name+'المسلسل للكبار والمبرمج منعه','',9999)
		return
	if '/episodes/' in url or '/tvshows/' in url:
		url2 = re.findall('''class='item'><a href="(.*?)"''',html,re.DOTALL)
		if url2:
			url2 = url2[1]
			EPISODES(url2)
			return
	html_blocks = re.findall('''class='episodios'(.*?)id="cast"''',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('''src='(.*?)'.*?class='numerando'>(.*?)<.*?href='(.*?)'>(.*?)<''',block,re.DOTALL)
		for img,episode,link,name in items:
			title = episode+' : '+name+' الحلقة'
			addMenuItem('video',menu_name+title,link,382)
	return

def PLAY(url):
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','MOVS4U-PLAY-1st')
	html = response.content
	ratingLIST = re.findall('class="C rated".*?>(.*?)<',html,re.DOTALL)
	if ratingLIST and RATING_CHECK(script_name,url,ratingLIST): return
	linkLIST = []
	# watch links
	html_blocks = re.findall("""id='player-option-1'(.*?)class=("sheader"|'pag_episodes')""",html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0][0]
		items = re.findall("data-url='(.*?)'.*?class='server'>(.*?)<",block,re.DOTALL)
		for link,title in items:
			link = link+'?named='+title+'__watch'
			linkLIST.append(link)
	# download links
	html_blocks = re.findall('class="remodal"(.*?)class="remodal-close"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('class="___dl_gdrive.*?href="(.*?)".*?">(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = website0a+link
			link = link+'?named='+title+'__download'
			linkLIST.append(link)
	#selection = DIALOG_SELECT('أختر البحث المناسب', linkLIST)
	if len(linkLIST)==0:
		DIALOG_OK('رسالة من المبرمج','الرابط ليس فيه فيديو')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name,'video')
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','+')
	url = website0a+'/?s='+search
	TITLES(url,'search')
	return



