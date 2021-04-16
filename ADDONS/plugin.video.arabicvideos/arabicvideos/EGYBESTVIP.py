# -*- coding: utf-8 -*-
from LIBRARY import *

#website0a = 'https://egy.best'
#website0a = 'https://egy1.best'
#website0a = 'https://egybest1.com'
#website0a = 'https://egybest.vip'
#website0a = 'https://egy4best.com'
#website0a = 'https://egybest-vip.shofda.com'
#website0a = 'https://rome.egybest.nl'
#website0a = 'https://vi.egybest.vip'

script_name = 'EGYBESTVIP'
menu_name='_EGV_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,page,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==220: results = MENU(url)
	elif mode==221: results = TITLES(url,page)
	elif mode==222: results = SUBMENU(url)
	elif mode==223: results = PLAY(url)
	elif mode==224: results = FILTERS_MENU(url)
	elif mode==229: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',229,'','','_REMEMBERRESULTS_')
		#addMenuItem('folder',menu_name+'فلتر محدد',website0a,226,'','','CATEGORIES___')
		#addMenuItem('folder',menu_name+'فلتر كامل',website0a,226,'','','FILTERS___')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a,'','','','','EGYBEST-MENU-1st')
	html = response.content
	html_blocks = re.findall('class="i i-home"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)"(.*?)</a>',block,re.DOTALL)
	for link,title in items:
		if '</i>' in title: title = title.split('</i>')[1]
		addMenuItem('folder',website+'___'+menu_name+title,link,222)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks = re.findall('class="ba(.*?)<script',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('pda bdb"><strong>(.*?)<.*?href="(.*?)"',html,re.DOTALL)
	for title,link in items:
		addMenuItem('folder',website+'___'+menu_name+title,link,221)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	items = re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for link,title in items:
		if 'html' not in link: continue
		if not link.endswith('/'): addMenuItem('folder',website+'___'+menu_name+title,link,221)
	return html
	"""
	#addMenuItem('folder',menu_name+'اضغط هنا لاضافة اسم دخول وكلمة السر','',225)
	#addMenuItem('folder',menu_name+'تحذير','',226)
	#DIALOG_OK(website0a, html)
	#html_blocks=re.findall('id="menu"(.*?)mainLoad',html,re.DOTALL)
	#block = html_blocks[0]
	#items=re.findall('href="(.*?)".*?i>(.*?)\n',block,re.DOTALL)
	#for url,title in items:
	#	if url!=website0a: addMenuItem('folder',menu_name+title,url,224)
	addMenuItem('folder',menu_name+'بحث في الموقع','',229,'','','_REMEMBERRESULTS_')
	addMenuItem('folder',website+'___'+menu_name+'الأكثر مشاهدة',website0a+'/trending',221)
	addMenuItem('folder',website+'___'+menu_name+'الافلام',website0a+'/movies',224)
	addMenuItem('folder',website+'___'+menu_name+'المسلسلات',website0a+'/tv',224)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = OPENURL_CACHED(LONG_CACHE,website0a,'','','','EGYBESTVIP-MENU-1st')
	html_blocks=re.findall('class="ba mgb(.*?)>EgyBest</a>',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for link,title in items:
		addMenuItem('folder',website+'___'+menu_name+title,link,221)
	return html
	# egybest1.com
	html_blocks=re.findall('id="menu"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	#items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	items=re.findall('<a href="(.*?)".*?[1/][i"]>(.*?)</a',block,re.DOTALL)
	for link,title in items:
		if 'torrent' not in link: addMenuItem('folder',menu_name+title,link,221)
	html_blocks=re.findall('class="card(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		if 'torrent' not in link: addMenuItem('folder',menu_name+title,link,221)
	"""

def SUBMENU(url):
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'','','','','EGYBESTVIP-SUBMENU-1st')
	html = response.content
	html_blocks = re.findall('class="rs_scroll"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)".*?</i>(.*?)</a>',block,re.DOTALL)
	for link,title in items:
		addMenuItem('folder',menu_name+title,link,224)
	return

def FILTERS_MENU(url):
	addMenuItem('folder',menu_name+'الجميع',url,221)
	html = OPENURL_CACHED(LONG_CACHE,url,'','','','EGYBESTVIP-FILTERS_MENU-1st')
	"""
	html_blocks=re.findall('id="main"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".*?</i>(.*?)[\r\n]+',block,re.DOTALL)
	for link,title in items:
		addMenuItem('folder',menu_name+title,link,221)
	"""
	html_blocks = re.findall('class="sub_nav(.*?)id="movies',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".+?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			if link=='#': name = title
			else:
				title = title + '  :  ' + 'فلتر ' + name
				addMenuItem('folder',menu_name+title,link,221)
	else: TITLES(url)
	return

def TITLES(url,page='1'):
	if page=='': page = '1'
	#DIALOG_OK(str(url), str(page))
	if '/search' in url or '?' in url: url2 = url + '&'
	else: url2 = url + '?'
	#url2 = url2 + 'output_format=json&output_mode=movies_list&page='+page
	url2 = url2 + 'page=' + page
	html = OPENURL_CACHED(REGULAR_CACHE,url2,'','','','EGYBESTVIP-TITLES-1st')
	#name = ''
	#if '/season' in url:
	#	name = re.findall('<h1>(.*?)<',html,re.DOTALL)
	#	if name: name = escapeUNICODE(name[0]).strip(' ') + ' - '
	#	else: name = xbmc.getInfoLabel( "ListItem.Label" ) + ' - '
	if '/season' in url:
		html_blocks=re.findall('class="pda"(.*?)div',html,re.DOTALL)
		block = html_blocks[-1]
	# bring seasons
	elif '/series/' in url:
		html_blocks=re.findall('class="owl-carousel owl-carousel(.*?)div',html,re.DOTALL)
		block = html_blocks[0]
	else:
		html_blocks=re.findall('id="movies(.*?)</div>',html,re.DOTALL)
		block = html_blocks[-1]
	items = re.findall('<a href="(.*?)".*?src="(.*?)".*?title">(.*?)<',block,re.DOTALL)
	for link,img,title in items:
		"""
		if '/series' in url and '/season' not in link: continue
		if '/season' in url and '/episode' not in link: continue
		#DIALOG_OK(title, str(link))
		title = name + escapeUNICODE(title).strip(' ')
		"""
		title = unescapeHTML(title)
		"""
		title = title.replace('\n','')
		link = link.replace('\/','/')
		img = img.replace('\/','/')
		if 'http' not in img: img = 'http:' + img
		#DIALOG_NOTIFICATION(img,'')
		url2 = website0a + link
		"""
		if '/movie/' in link or '/episode' in link:
			addMenuItem('video',menu_name+title,link.rstrip('/'),223,img)
		else:
			addMenuItem('folder',menu_name+title,link,221,img)
	if len(items)>=16:
		pagingLIST = ['/movies','/tv','/search','/trending']
		page = int(page)
		if any(value in url for value in pagingLIST):
			for n in range(0,1000,100):
				if int(page/100)*100==n:
					for i in range(n,n+100,10):
						if int(page/10)*10==i:
							for j in range(i,i+10,1):
								if not page==j and j!=0:
									addMenuItem('folder',menu_name+'صفحة '+str(j),url,221,'',str(j))
						elif i!=0: addMenuItem('folder',menu_name+'صفحة '+str(i),url,221,'',str(i))
						else: addMenuItem('folder',menu_name+'صفحة '+str(1),url,221,'',str(1))
				elif n!=0: addMenuItem('folder',menu_name+'صفحة '+str(n),url,221,'',str(n))
				else: addMenuItem('folder',menu_name+'صفحة '+str(1),url,221)
	return

def PLAY(url):
	#global ''
	titleLIST,linkLIST = [],[]
	#DIALOG_OK(url, url[-45:])
	# https://egy4best.com/movie/فيلم-the-lion-king-2019-مترجم
	html = OPENURL_CACHED(LONG_CACHE,url,'','','','EGYBESTVIP-PLAY-1st')
	ratingLIST = re.findall('<td>التصنيف</td>.*?">(.*?)<',html,re.DOTALL)
	if False and ratingLIST and RATING_CHECK(script_name,url,ratingLIST): return
	# https://egybest.vip/movie/فيلم-the-lion-king-2019-مترجم
	watchURL,downloadURL = '',''
	htmlWatch,htmlDownload = html,html
	watch_download = re.findall('show_dl api" href="(.*?)"',html,re.DOTALL)
	if watch_download:
		for link in watch_download:
			if '/watch/' in link: watchURL = link
			elif '/download/' in link: downloadURL = link
		if watchURL!='': htmlWatch = OPENURL_CACHED(LONG_CACHE,watchURL,'','','','EGYBESTVIP-PLAY-2nd')
		if downloadURL!='': htmlDownload = OPENURL_CACHED(LONG_CACHE,downloadURL,'','','','EGYBESTVIP-PLAY-3rd')
	#DIALOG_OK(downloadURL,watchURL)
	# https://uploaded.egybest.download/?id=__the_lion_king_2019
	watchitem = re.findall('id="video".*?data-src="(.*?)"',htmlWatch,re.DOTALL)
	if watchitem:
		url2 = watchitem[0]#+'||MyProxyUrl=http://79.165.242.84:4145'
		if url2!='' and 'uploaded.egybest.download' in url2 and '/?id=_' not in url2:
			html2 = OPENURL_CACHED(LONG_CACHE,url2,'','','','EGYBESTVIP-PLAY-4th')
			watchlist = re.findall('source src="(.*?)" title="(.*?)"',html2,re.DOTALL)
			if watchlist:
				for link,quality in watchlist:
					linkLIST.append(link+'?named=ed.egybest.do__watch__mp4__'+quality)
			else:
				server = url2.split('/')[2]
				linkLIST.append(url2+'?named='+server+'__watch')
		elif url2!='':
			#DIALOG_OK(url2,str(watchitem))
			server = url2.split('/')[2]
			linkLIST.append(url2+'?named='+server+'__watch')
	# https://inflam.cc/VLO1NNdGuy
	# https://facultybooks.org/VLO1NNdGuy
	downloadtable = re.findall('<table class="dls_table(.*?)</table>',htmlDownload,re.DOTALL)
	if downloadtable:
		downloadtable = downloadtable[0]
		downloadlist = re.findall('<td>.*?<td>(.*?)<.*?href="(.*?)"',downloadtable,re.DOTALL)
		if downloadlist:
			for quality,link in downloadlist:
				if 'myegyvip' not in link: continue
				if link.count('/')>=2:
					server = link.split('/')[2]
					linkLIST.append(link+'?named='+server+'__download__mp4__'+quality)
	#selection = DIALOG_SELECT('اختر الفيديو المناسب:', linkLIST)
	#if selection == -1 : return
	newLIST = []
	for link in linkLIST:
		# faselhd	https://movies.egybest.vip/movie/watch/فيلم-the-space-between-us-2017-مترجم/e53047e2cbc712380c0cb5f42ed4038f
		#if 'faselhd' in link: continue
		#if 'egybest.vip?name' in link: continue
		#if 'egybest.vip' in link: continue
		#if 'myegyvip' not in link: continue
		newLIST.append(link)
	#selection = DIALOG_SELECT('أختر البحث المناسب', newLIST)
	if len(newLIST)==0: DIALOG_OK('رسالة من المبرمج','هذا الفيديو يستخدم روابط غير معروفة في هذا البرنامج والمبرمج لم يستطيع إيحاد حل لهذه المشكلة')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(newLIST,script_name,'video')
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	new_search = search.replace(' ','+')
	html = OPENURL_CACHED(SHORT_CACHE,website0a,'','','','EGYBESTVIP-SEARCH-1st')
	token = re.findall('name="_token" value="(.*?)"',html,re.DOTALL)
	if token:
		url = website0a+'/search?_token='+token[0]+'&q='+new_search
		TITLES(url)
		#DIALOG_OK('', '')
	return


