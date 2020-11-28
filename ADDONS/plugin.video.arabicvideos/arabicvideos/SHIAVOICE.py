# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='SHIAVOICE'
menu_name = '_SHV_'
website0a = WEBSITES[script_name][0]
headers = {'User-Agent':None}

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==310: results = MENU(url)
	elif mode==311: results = TITLES(url)
	elif mode==312: results = PLAY(url)
	elif mode==313: results = SEARCH_ITEMS(url)
	elif mode==314: results = LATEST(text)
	elif mode==319: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	addMenuItem('folder',menu_name+'بحث في الموقع','',319,'','','_REMEMBERRESULTS_')
	#addMenuItem('folder',menu_name+'فلتر','',114,website0a)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a,'','','','','SHIAVOICE-MENU-1st')
	html = response.content
	html_blocks = re.findall('id="menulinks"(.*?)</ul>',html,re.DOTALL)
	block = html_blocks[0]
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	items = re.findall('<h5>(.*?)</h5>',html,re.DOTALL)
	for seq in range(len(items)):
		title = items[seq].strip(' ')
		addMenuItem('folder',website+'___'+menu_name+title,website0a,314,'','',str(seq+1))
	addMenuItem('folder',website+'___'+menu_name+'مقاطع شهر',website0a,314,'','','0')
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	items = re.findall('href="(.*?)".*?<B>(.*?)</B>',block,re.DOTALL)
	for link,title in items:
		#title = title.strip(' ')
		#url = website0a+'/wp-content/themes/CimaNow/Interface/filter.php'
		addMenuItem('folder',website+'___'+menu_name+title,link,311)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def LATEST(seq):
	#t1 = time.time()
	#LOG_THIS('NOTICE','start')
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',website0a,'','','','','SHIAVOICE-LATEST-1st')
	html = response.content
	#LOG_THIS('NOTICE','elpased = '+str(time.time()-t1))
	if seq=='0':
		html_blocks = re.findall('class="tab-content"(.*?)</table>',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?title="(.*?)".*?</i>(.*?)<',block,re.DOTALL)
		for link,name,title in items:
			title = title.strip(' ')
			name = name.strip(' ')
			title = title+' ('+name+')'
			addMenuItem('video',menu_name+title,link,312)
	elif seq in ['1','2','3']:
		html_blocks = re.findall('(<h5>.*?)<div class="col-lg',html,re.DOTALL)
		seq2 = int(seq)-1
		block = html_blocks[seq2]
		if seq=='1': items = re.findall('href="(.*?)".*?src="(.*?)".*?<strong>(.*?)<.*?</i>(.*?)<',block,re.DOTALL)
		else: items = re.findall('href="(.*?)".*?src="(.*?)".*?<strong>(.*?)<.*?href=".*?">(.*?)<',block,re.DOTALL)
		for link,img,title,name in items:
			title = title.strip(' ')
			name = name.strip(' ')
			title = title+' ('+name+')'
			addMenuItem('folder',menu_name+title,link,311,img)
	elif seq in ['4','5','6']:
		html_blocks = re.findall('(<h5>.*?)</table>',html,re.DOTALL)
		seq = int(seq)-4
		block = html_blocks[seq]
		items = re.findall('src="(.*?)".*?href="(.*?)".*?title="(.*?)".*?<strong>(.*?)<.*?-cell">(.*?)<',block,re.DOTALL)
		for img,link,name1,title,name2 in items:
			title = title.strip(' ')
			name1 = name1.strip(' ')
			name2 = name2.strip(' ')
			if name1: name = name1
			else: name = name2
			title = title+' ('+name+')'
			addMenuItem('video',menu_name+title,link,312,img)
	return

def TITLES(url):
	#DIALOG_OK(url,'')
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','SHIAVOICE-TITLES-1st')
	html = response.content
	html_blocks = re.findall('ibox-heading"(.*?)class="float-right',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('src="(.*?)".*?href="(.*?)".*?<strong>(.*?)<.*?catsum-mobile">(.*?)<',block,re.DOTALL)
	if items:
		for img,link,title,count in items:
			count = count.replace(' الصوتية: ',':')
			title = title.strip(' ')
			title = title+' ('+count+')'
			addMenuItem('folder',menu_name+title,link,311,img)
	else: EPISODES(html)
	return

def EPISODES(html):
	html_blocks = re.findall('class="ibox-content"(.*?)class="pagination',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(http.*?)".*?</i>(.*?)<.*?cell">(.*?)<.*?cell">(.*?)<.*?cell">(.*?)<',block,re.DOTALL)
	for link,title,name,count,duration in items:
		#DIALOG_OK('',link+','+title+','+name+','+count+','+duration)
		title = title.strip(' ')
		name = name.strip(' ')
		title = title+' ('+name+')'
		addMenuItem('video',menu_name+title,link,312,'',duration)
	return

def SEARCH_ITEMS(url):
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','SHIAVOICE-TITLES-1st')
	html = response.content
	html_blocks = re.findall('class="ibox-content p-1"(.*?)class="ibox-content"',html,re.DOTALL)
	if not html_blocks:
		EPISODES(html)
		return
	block = html_blocks[0]
	items = re.findall('href="(http.*?)".*?<strong>(.*?)<',block,re.DOTALL)
	for link,title in items:
		title = title.strip(' ')
		addMenuItem('video',menu_name+title,link,312)
	return

def PLAY(url):
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url,'','','','','SHIAVOICE-PLAY-1st')
	html = response.content
	link = re.findall('<audio.*?src="(.*?)"',html,re.DOTALL)
	if not link: link = re.findall('<video.*?src="(.*?)"',html,re.DOTALL)
	link = link[0]
	PLAY_VIDEO(link,script_name,'video')
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','+')
	typeList = ['&t=a','&t=c','&t=s']
	if showdialogs:
		searchTitle = ['قارئ','إصدار / مجلد','مقطع الصوتي']
		selection = DIALOG_SELECT('أختر البحث المناسب', searchTitle)
		if selection == -1: return
	else: selection = 2
	type = typeList[selection]
	url = website0a+'/search.php?q='+search+type
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','SHIAVOICE-SEARCH-1st')
	html = response.content
	html_blocks = re.findall('class="ibox-content"(.*?)class="ibox-content"',html,re.DOTALL)
	block = html_blocks[0]
	if selection in [0,1]:
		items = re.findall('href="(http.*?)".*?src="(.*?)".*?href=".*?">(.*?)<.*?">(.*?)<',block,re.DOTALL)
		for link,img,title,name in items:
			title = title.strip(' ')
			name = name.strip(' ')
			title = title+' ('+name+')'
			addMenuItem('folder',menu_name+title,link,313,img)
	elif selection==2:
		items = re.findall('href="(http.*?)".*?</i>(.*?)</a></td><td>(.*?)<',block,re.DOTALL)
		for link,title,name in items:
			title = title.strip(' ')
			name = name.strip(' ')
			title = title+' ('+name+')'
			addMenuItem('video',menu_name+title,link,312)
	return



