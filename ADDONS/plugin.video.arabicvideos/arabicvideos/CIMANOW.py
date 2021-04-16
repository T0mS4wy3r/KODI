# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='CIMANOW'
menu_name='_CMN_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['قائمتي']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==300: results = MENU(url)
	elif mode==301: results = SUBMENU(url)
	elif mode==302: results = TITLES(url)
	elif mode==303: results = SEASONS(url)
	elif mode==304: results = EPISODES(url)
	elif mode==305: results = PLAY(url)
	elif mode==309: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',309,'','','_REMEMBERRESULTS_')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a,'','','','','CIMANOW-MENU-1st')
	html = response.content
	html_blocks = re.findall('<ul>(.*?)</ul>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
			addMenuItem('folder',website+'___'+menu_name+title,link,301)
	return html

def SUBMENU(url):
	seq = 0
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'','','','','CIMANOW-SUBMENU-1st')
	html = response.content
	html_blocks = re.findall('(<section>.*?</section>)',html,re.DOTALL)
	if html_blocks:
		for block in html_blocks:
			seq += 1
			items = re.findall('<section>.<span>(.*?)<(.*?)href="(.*?)"',block,re.DOTALL)
			for title,test,link in items:
				if 'em><a' not in test:
					#DIALOG_OK('',str(block))
					if block.count('/category/')>0:
						categories = re.findall('href="(.*?)"',block,re.DOTALL)
						for link in categories:
							title = link.split('/')[-2]
							addMenuItem('folder',menu_name+title,link,301)
						continue
					else: link = url+'?sequence='+str(seq)
				#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
				#if any(value in title for value in keepLIST):
				if not any(value in title for value in ignoreLIST):
					addMenuItem('folder',menu_name+title,link,302)
	else: TITLES(url,html)
	return

def TITLES(url,html=''):
	if html=='':
		response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','CIMANOW-TITLES-1st')
		html = response.content
	if '?sequence=' in url:
		url,seq = url.split('?sequence=')
		html_blocks = re.findall('(<section>.*?</section>)',html,re.DOTALL)
		block = html_blocks[int(seq)-1]
	else:
		html_blocks = re.findall('"posts"(.*?)"pagination"',html,re.DOTALL)
		block = html_blocks[0]
	items = re.findall('<a.*?href="(.*?)"(.*?)src="(.*?)"',block,re.DOTALL)
	allTitles = []
	for link,data,img in items:
		title = re.findall('<em>(.*?)</em>(.*?)</li>.*?</em>(.*?)<em>',data,re.DOTALL)
		if title: title = title[0][2].replace('\n','').strip(' ')
		if not title or title=='':
			title = re.findall('title">.*?</em>(.*?)<',data,re.DOTALL)
			if title: title = title[0].replace('\n','').strip(' ')
			if not title or title=='':
				title = re.findall('title">(.*?)<',data,re.DOTALL)
				title = title[0].replace('\n','').strip(' ')
		title = unescapeHTML(title)
		#if title=='': continue
		if title not in allTitles:
			allTitles.append(title)
			block2 = link+data+img
			if '/selary/' in block2 or 'مسلسل' in block2 or '"episode"' in block2:
				if 'برامج' in data: title = 'برنامج '+title
				elif 'مسلسل' in data or 'موسم' in data: title = 'مسلسل '+title
				addMenuItem('folder',menu_name+title,link,303,img)
			else: addMenuItem('video',menu_name+title,link,305,img)
	html_blocks = re.findall('"pagination"(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<li><a href="(.*?)">(.*?)<',block,re.DOTALL)
		for link,title in items:
			addMenuItem('folder',menu_name+'صفحة '+title,link,302)
	return

def SEASONS(url):
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','CIMANOW-SEASONS-1st')
	html = response.content
	name = re.findall('<title>(.*?)</title>',html,re.DOTALL)
	name = name[0].replace('| سيما ناو','').replace('Cima Now','').strip(' ').replace('  ',' ')
	html_blocks = re.findall('"seasons"(.*?)</section>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
		for link,title in items:
			title = name+' '+title.replace('\n','').strip(' ')
			addMenuItem('folder',menu_name+title,link,304)
	return

def EPISODES(url):
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','CIMANOW-EPISODES-1st')
	html = response.content
	html_blocks = re.findall('"details"(.*?)"related"',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)".*?src=.*?src="(.*?)".*?alt="(.*?)"',block,re.DOTALL)
	for link,img,title in items:
		title = title.replace('\n','').strip(' ')
		addMenuItem('video',menu_name+title,link,305,img)
	return

def PLAY(url):
	"""
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url,'','','','','CIMANOW-PLAY-1st')
	html = response.content
	redirect_link = re.findall('class="shine" href="(.*?)"',html,re.DOTALL)
	redirect_link = redirect_link[0]
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',redirect_link,'','','','','CIMANOW-PLAY-2nd')
	redirect_html = response.content
	cookies = response.cookies.get_dict()
	PHPSESSID = cookies['PHPSESSID']
	verify_link = re.findall("href = '(.*?)'",redirect_html,re.DOTALL)
	verify_link = verify_link[0]
	headers = {'Referer':redirect_link,'Cookie':'PHPSESSID='+PHPSESSID}
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',verify_link,'',headers,'','','CIMANOW-PLAY-3rd')
	verify_html = response.content
	#ad_link = re.findall('id="ad" target="_blank" href="(.*?)"',verify_html,re.DOTALL)
	#ad_link = ad_link[0]
	#response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',ad_link,'','','','','CIMANOW-PLAY-4th')
	#ad_html = response.content
	url2 = re.findall('"downloadbtn" style="display: none;" href="(.*?)"',verify_html,re.DOTALL)
	url2 = url2[0]+'/'
	headers = {'Referer':'https://web.cimavids.live/'}
	"""
	url2 = url+'watching/'
	server = SERVER(url2)
	headers = {'Referer':server}
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url2,'',headers,'','','CIMANOW-PLAY-5th')
	html2 = response.content
	linkLIST = []
	# download links
	html_blocks = re.findall('"download"(.*?)</section>',html2,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)".*?</i>(.*?)</a>',block,re.DOTALL)
	for link,title in items:
		title = title.replace('\n','').strip(' ')
		quality = re.findall('\d\d\d+',title,re.DOTALL)
		if quality:
			quality = '____'+quality[0]
			title = 'cimanow'
		else: quality = ''
		link2 = link+'?named='+title+'__download'+quality
		linkLIST.append(link2)
	# watch links
	link = re.findall('ajax\({url: "(.*?)"',html2,re.DOTALL)[0]
	html_blocks = re.findall('"watch"(.*?)</div>',html2,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('data-index="(.*?)".*?data-id="(.*?)".*?>(.*?)</li>',block,re.DOTALL)
	for index,id,title in items:
		title = title.replace('\n','').strip(' ')
		title = title.replace('Cima Now','CimaNow')
		link2 = link+'?action=switch&index='+index+'&id='+id+'?named='+title+'__watch'
		linkLIST.append(link2)
	#selection = DIALOG_SELECT('أختر البحث المناسب',linkLIST)
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
	url = website0a + '/?s='+search
	TITLES(url)
	return




