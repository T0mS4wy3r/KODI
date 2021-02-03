# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='BOKRA'
menu_name='_BKR_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==370: results = MENU(url)
	elif mode==371: results = TITLES(url,text)
	elif mode==372: results = PLAY(url)
	elif mode==379: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a,'','','','','BOKRA-MENU-1st')
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',379,'','','_REMEMBERRESULTS_')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = response.content
	ignoreLIST = ['افلام للكبار','بكرا TV']
	html_blocks = re.findall('class="container"(.*?)script type=',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
		for link,title in items:
			title = title.strip(' ')
			link = website0a+link
			if not any(value in title for value in ignoreLIST):
				addMenuItem('folder',website+'___'+menu_name+title,link,371)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks = re.findall('class="row cat Tags"(.*?)class="row cat zone220"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)" title="(.*?)"',block,re.DOTALL)
		for link,title in items:
			link = website0a+link
			if not any(value in title for value in ignoreLIST):
				addMenuItem('folder',website+'___'+menu_name+title,link,371)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	global menuItemsLIST
	last_items = menuItemsLIST[2:8]
	del menuItemsLIST[2:8]
	menuItemsLIST[:] = menuItemsLIST+last_items
	return html

def TITLES(url,type=''):
	#DIALOG_OK(url,'TITLES')
	#LOG_THIS('NOTICE',html)
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','BOKRA-TITLES-1st')
	html = response.content
	if 'vidpage_' in url:
		link = re.findall('href="(/Album-.*?)"',html,re.DOTALL)
		if link:
			link = website0a+link[0]
			TITLES(link)
			return
	html_blocks = re.findall('class=" subcats"(.*?)class="col-md-3',html,re.DOTALL)
	if type=='' and html_blocks and html_blocks[0].count('href')>1:
		addMenuItem('folder',menu_name+'الجميع',url,371,'','','titles')
		block = html_blocks[0]
		items = re.findall('href="(.*?)" title="(.*?)"',block,re.DOTALL)
		for link,title in items:
			link = website0a+'/'+link
			title = title.strip(' ')
			addMenuItem('folder',menu_name+title,link,371)
	else:
		allTitles = []
		html_blocks = re.findall('class="col-md-3(.*?)col-xs-12',html,re.DOTALL)
		if not html_blocks: html_blocks = re.findall('class="col-sm-8"(.*?)col-xs-12',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('href="(.*?)".*?src="(.*?)".*?<h4>(.*?)<',block,re.DOTALL)
			for link,img,title in items:
				link = website0a+link
				title = title.strip(' ')
				if '/al_' in link:
					addMenuItem('folder',menu_name+title,link,371,img)
				elif 'الحلقة' in title and ('/Cat-' in url or '/Search/' in url):
					episode = re.findall('(.*?) - +الحلقة +\d+',title,re.DOTALL)
					if episode: title = '_MOD_مسلسل '+episode[0]
					if title not in allTitles:
						allTitles.append(title)
						addMenuItem('folder',menu_name+title,link,371,img)
				else: addMenuItem('video',menu_name+title,link,372,img)
		html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('class="".*?href="(.*?)">(.*?)<',block,re.DOTALL)
			for link,title in items:
				link = website0a+link
				title = 'صفحة '+unescapeHTML(title)
				addMenuItem('folder',menu_name+title,link,371,'','','titles')
	return

def PLAY(url):
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url,'','','','','BOKRA-PLAY-1st')
	html = response.content
	ratingLIST = re.findall('label-success mrg-btm-5 ">(.*?)<',html,re.DOTALL)
	if ratingLIST and RATING_CHECK(script_name,url,ratingLIST): return
	#url2 = url.replace('vidpage_','Play/')
	url2 = re.findall('var url = "(.*?)"',html,re.DOTALL)
	url2 = website0a+url2[0]
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url2,'','','','','BOKRA-PLAY-2nd')
	html2 = response.content
	url3 = re.findall('src="(.*?)"',html2,re.DOTALL)
	if url3:
		url3 = url3[0]
		if 'http:' not in url3: url3 = 'http:'+url3
		import RESOLVERS
		RESOLVERS.PLAY([url3],script_name,'video')
	else: DIALOG_OK('رسالة من المبرمج','للأسف ملف الفيديو غير موجود في الموقع الأصلي')
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','+')
	url = website0a+'/Search/'+search
	TITLES(url)
	return



