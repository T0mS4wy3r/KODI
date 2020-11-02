# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='KARBALATV'
menu_name = '_KRB_'
website0a = WEBSITES[script_name][0]
headers = {'User-Agent':''}

def MAIN(mode,url,text):
	if   mode==320: results = MENU(url)
	elif mode==321: results = TITLES(url)
	elif mode==322: results = PLAY(url)
	elif mode==329: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	addMenuItem('folder',menu_name+'بحث في الموقع','',329,'','','_REMEMBERRESULTS_')
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	response = openURL_requests_cached(LONG_CACHE,'GET',website0a+'/video.php','',headers,'','','KARBALATV-MENU-1st')
	html = response.content
	html_blocks = re.findall('class="icono-plus"(.*?)</ul>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		if title=='المكتبة المرئية': continue
		link = website0a+link
		addMenuItem('folder',website+'___'+menu_name+title,link,321)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def TITLES(url):
	#XBMCGUI_DIALOG_OK(url,html)
	response = openURL_requests_cached(REGULAR_CACHE,'GET',url,'',headers,'','','KARBALATV-TITLES-1st')
	html = response.content
	html_blocks = re.findall('class="container"(.*?)class="footer',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)".*?url\((.*?)\).*?pd5">(.*?)<.*?<h3.*?">(.*?)<',block,re.DOTALL)
	if not items: items = re.findall('href="(.*?)".*?src="(.*?)".*?alt="(.*?)".*?<p.*?>(.*?)<',block,re.DOTALL)
	for link,img,count,title in items:
		count = count.replace('عدد ','').replace(' ','')
		link = link.replace('/','')
		img = img.replace("'",'')
		if '.php' not in link: link = 'video.php'+link
		link = website0a+'/'+link
		img = website0a+img
		title = title.strip(' ')
		title = title+' ('+count+')'
		if 'video.php' in link: addMenuItem('folder',menu_name+title,link,321,img)
		elif 'watch.php' in link: addMenuItem('video',menu_name+title,link,322,img)
	html_blocks = re.findall('class="pagination(.*?)class="footer',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = website0a+'/video.php'+link
			addMenuItem('folder',menu_name+'صفحة '+title,link,321)
	return

def PLAY(url):
	response = openURL_requests_cached(SHORT_CACHE,'GET',url,'',headers,'','','KARBALATV-PLAY-1st')
	html = response.content
	#link = re.findall('<audio.*?src="(.*?)"',html,re.DOTALL)
	#if not link: 
	link = re.findall('<video.*?src="(.*?)"',html,re.DOTALL)
	link = website0a+link[0]#+'|User-Agent='+RANDOM_USERAGENT()+'&verifypeer=true'
	PLAY_VIDEO(link,script_name,'video')
	return

def SEARCH(search):
	#search = 'مختار'
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','+')
	url = website0a+'/search.php?q='+search
	TITLES(url)
	return





