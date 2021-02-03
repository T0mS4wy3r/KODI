# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='FAJERSHOW'
menu_name='_FJS_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['التصنيفات','انشاء حساب','طلبات الزوّار']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==390: results = MENU(url)
	elif mode==391: results = TITLES(url,text)
	elif mode==392: results = PLAY(url)
	elif mode==393: results = EPISODES(url)
	elif mode==399: results = SEARCH(text)	
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',399,'','','_REMEMBERRESULTS_')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a,'','','','','FAJERSHOW-MENU-1st')
	html = response.content
	items = re.findall('<header>.*?<h2>(.*?)<',html,re.DOTALL)
	for seq in range(len(items)):
		title = items[seq]
		addMenuItem('folder',website+'___'+menu_name+title,website0a,391,'','','latest'+str(seq))
	addMenuItem('folder',menu_name+'المميزة',website0a,391,'','','featured')
	addMenuItem('folder',menu_name+'أعلى الأفلام تقييماً',website0a,391,'','','top_imdb_movies')
	addMenuItem('folder',menu_name+'أعلى المسلسلات تقييماً',website0a,391,'','','top_imdb_series')
	addMenuItem('folder',menu_name+'أفلام مميزة',website0a+'/movies',391,'','','featured_movies')
	addMenuItem('folder',menu_name+'مسلسلات مميزة',website0a+'/tvshows',391,'','','featured_tvshows')
	block = ''
	html_blocks = re.findall('class="menu"(.*?)id="contenedor"',html,re.DOTALL)
	if html_blocks: block += html_blocks[0]
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a+'/movies','','','','','FAJERSHOW-MENU-2nd')
	html = response.content
	html_blocks = re.findall('class="releases"(.*?)aside',html,re.DOTALL)
	if html_blocks: block += html_blocks[0]
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	first = True
	for link,title in items:
		title = unescapeHTML(title)
		if title=='الأعلى مشاهدة':
			if first: 
				title = 'الافلام '+title
				first = False
			else: title = 'المسلسلات '+title
		if title not in ignoreLIST:
			if title=='أفلام': addMenuItem('folder',website+'___'+menu_name+title,website0a+'/movies',391,'','','all_movies_tvshows')			
			elif title=='مسلسلات': addMenuItem('folder',website+'___'+menu_name+title,website0a+'/tvshows',391,'','','all_movies_tvshows')
			else: addMenuItem('folder',website+'___'+menu_name+title,link,391)
	return html

def TITLES(url,type):
	#DIALOG_OK(url,type)
	#WRITE_THIS(html)
	block,items = [],[]
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','FAJERSHOW-TITLES-1st')
	html = response.content
	if type in ['featured_movies','featured_tvshows']:
		html_blocks = re.findall('class="content"(.*?)id="archive-content"',html,re.DOTALL)
		if html_blocks: block = html_blocks[0]
		#DIALOG_OK(url,block)
	elif type=='all_movies_tvshows':
		html_blocks = re.findall('id="archive-content"(.*?)class="pagination"',html,re.DOTALL)
		if html_blocks: block = html_blocks[0]
	elif type=='top_imdb_movies':
		html_blocks = re.findall("class='top-imdb-list tleft(.*?)class='top-imdb-list tright",html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			#DIALOG_OK(str(len(block)),type)
			items = re.findall("img src='(.*?)'.*?href='(.*?)'>(.*?)<",block,re.DOTALL)
	elif type=='top_imdb_series':
		html_blocks = re.findall("class='top-imdb-list tright(.*?)footer",html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			#DIALOG_OK(str(len(block)),type)
			items = re.findall("img src='(.*?)'.*?href='(.*?)'>(.*?)<",block,re.DOTALL)
	elif type=='search':
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
		html = html.replace('</div></div></div>','</div></div></div><end>')
		html_blocks = re.findall('<start>(.*?)<end>',html,re.DOTALL)
		block = html_blocks[seq]
		if seq==6:
			z = re.findall('img src="(.*?)" alt="(.*?)".*?href="(.*?)"',block,re.DOTALL)
			imgLIST,titleLIST,linkLIST = zip(*z)
			items = zip(imgLIST,linkLIST,titleLIST)
	else:
		html_blocks = re.findall('class="content"(.*?)class="(pagination|sidebar)',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0][0]
			if '/collection/' in url:
				items = re.findall('img src="(.*?)".*?href="(.*?)">(.*?)<',block,re.DOTALL)
			elif '/quality/' in url:
				items = re.findall('img src="(.*?)".*?href="(.*?)".*?"title">(.*?)<',block,re.DOTALL)
	#DIALOG_OK(str(len(items)),type)
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
		if '/tvshows/' in link: addMenuItem('folder',menu_name+title,link,393,img)
		elif '/episodes/' in link: addMenuItem('folder',menu_name+title,link,393,img)
		elif '/seasons/' in link: addMenuItem('folder',menu_name+title,link,393,img)
		elif '/collection/' in link: addMenuItem('folder',menu_name+title,link,391,img)
		else: addMenuItem('video',menu_name+title,link,392,img)
	if type not in ['featured_movies','featured_tvshows']:
		html_blocks = re.findall('class="pagination".*?صفحة (.*?) من (.*?)<(.*?)</div>',html,re.DOTALL)
		if html_blocks:
			current = html_blocks[0][0]
			last = html_blocks[0][1]
			block = html_blocks[0][2]
			items = re.findall("href='(.*?)'.*?>(.*?)<",block,re.DOTALL)
			for link,title in items:
				if title=='' or title==last: continue
				addMenuItem('folder',menu_name+'صفحة '+title,link,391,'','',type)
			#if title==last:
			link = link.replace('/page/'+title+'/','/page/'+last+'/')
			addMenuItem('folder',menu_name+'اخر صفحة '+last,link,391,'','',type)
	return

def EPISODES(url):
	#DIALOG_OK(url,'')
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','FAJERSHOW-EPISODES-1st')
	html = response.content
	ratingLIST = re.findall('class="C rated".*?>(.*?)<',html,re.DOTALL)
	if ratingLIST and RATING_CHECK(script_name,url,ratingLIST): return
	if '/episodes/' in url or '/tvshows/' in url:# or '/seasons/' in url:
		url2 = re.findall('''class='item'><a href="(.*?)"''',html,re.DOTALL)
		if url2:
			url2 = url2[1]
			EPISODES(url2)
			return
	html_blocks = re.findall('''class=['"]episodio(.*?)</div></div>''',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('''src='(.*?)'.*?class='numerando'>(.*?)<.*?href='(.*?)'>(.*?)<''',block,re.DOTALL)
		for img,episode,link,name in items:
			title = episode+' : '+name+' الحلقة'
			addMenuItem('video',menu_name+title,link,392)
	return

def PLAY(url):
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','FAJERSHOW-PLAY-1st')
	html = response.content
	ratingLIST = re.findall('class="C rated".*?>(.*?)<',html,re.DOTALL)
	if ratingLIST and RATING_CHECK(script_name,url,ratingLIST): return
	linkLIST = []
	# watch links
	html_blocks = re.findall("""id="player-option-1"(.*?)class=["|'](sheader|pag_episodes)["|']""",html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0][0]
		items = re.findall('data-type="(.*?)" data-post="(.*?)" data-nume="(.*?)".*?class="vid_title">(.*?)<',block,re.DOTALL)
		for type,post,nume,title in items:
			#link = 'https://show.alfajertv.com/wp-admin/admin-ajax.php'
			link = website0a+'/wp-admin/admin-ajax.php?action=doo_player_ajax&post='+post+'&nume='+nume+'&type='+type
			link = link+'?named='+title+'__watch'
			linkLIST.append(link)
	# download links
	#WRITE_THIS(html)
	html_blocks = re.findall("""id='download' class(.*?)class=["|']sbox["|']""",html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall("img src='(.*?)'.*?href='(.*?)'.*?'quality'>(.*?)<",block,re.DOTALL)
		#DIALOG_OK(str(items),str(block))
		for img,link,quality in items:
			if '=' in img:
				host = img.split('=')[1]
				title = HOSTNAME(host,True)
			else: title = ''
			link = link+'?named='+title+'__download____'+quality
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



