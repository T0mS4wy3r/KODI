# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='ARABSEED'
headers = {'User-Agent':''}
menu_name='_ARS_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['الرئيسية','مصارعه','افلام','اعلن معنا – For ads']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==250: results = MENU(url)
	elif mode==251: results = TITLES(url)
	elif mode==252: results = PLAY(url)
	elif mode==253: results = EPISODES(url)
	elif mode==254: results = FILTERS_MENU(url,'FILTERS___'+text)
	elif mode==255: results = FILTERS_MENU(url,'CATEGORIES___'+text)
	elif mode==256: results = FILTERING(url)
	elif mode==257: results = SORTING(url)
	elif mode==258: results = FEATURED(url)
	elif mode==259: results = SEARCH(text)	
	else: results = False
	return results

def MENU(website=''):
	html = OPENURL_CACHED(LONG_CACHE,website0a+'/main','',headers,'','ARABSEED-MENU-1st')
	html_blocks2 = re.findall('navigation-menu(.*?)</header>',html,re.DOTALL)
	block2 = html_blocks2[0]
	items2 = re.findall('href="(.*?)".*?>(.*?)<',block2,re.DOTALL)
	server = SERVER(items2[0][0])+'/main'
	addMenuItem('folder',menu_name+'بحث في الموقع','',259,'','','_REMEMBERRESULTS_')
	addMenuItem('folder',menu_name+'فلتر محدد',server,255)
	addMenuItem('folder',menu_name+'فلتر كامل',server,254)
	addMenuItem('folder',menu_name+'المميزة',server,258)
	#addMenuItem('folder',menu_name+'الرئيسية',server,251)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#addMenuItem('folder',website+'___'+menu_name+'فلتر','',254,server)
	#html_blocks = re.findall('class="tabs-menu(.*?)</ul>',html,re.DOTALL)
	#block = html_blocks[0]
	#items = re.findall('<li data-key="(.*?)".*?</i>(.*?)</li>',block,re.DOTALL)
	#for filter,title in items:
	#	link = server+'/wp-content/themes/ArbSeed/ajaxCenter/Home/Filtering.php?key='+filter
	#	addMenuItem('folder',website+'___'+menu_name+title,link,256)
	#if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
	for link,title in items2:
		if 'javascript' in link: continue
		#title = title.strip(' ')
		#if not any(value in title for value in ignoreLIST):
		#	if any(value in title for value in keepLIST):
		if title not in ignoreLIST:
			if 'http' not in link: link = server+link
			addMenuItem('folder',website+'___'+menu_name+title,link,256)
	return html

def FEATURED(url):
	html = OPENURL_CACHED(LONG_CACHE,url,'',headers,'','ARABSEED-FEATURED-1st')
	items = re.findall('class="SliderItem.*?href="(.*?)".*?image: url\((.*?)\).*?<h2>(.*?)<',html,re.DOTALL)
	for link,img,title in items:
		addMenuItem('video',menu_name+title,link,252,img)
	return

def FILTERING(url):
	#DIALOG_OK(url,'')
	server = SERVER(url)
	html = OPENURL_CACHED(SHORT_CACHE,url,'',headers,'','ARABSEED-FILTERING-1st')
	term = re.findall('term: "(.*?)"',html,re.DOTALL)
	term = term[0]
	html_blocks = re.findall('class="tabs-menu(.*?)</ul>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('<li data-key="(.*?)".*?</i>(.*?)</li>',block,re.DOTALL)
	addMenuItem('folder',menu_name+'الكل',url,257)
	for filter,title in items:
		title = title.strip(' ')
		link = server+'/wp-content/themes/ArbSeed/ajaxCenter/Home/Filtering.php?key='+filter+'&term='+term
		addMenuItem('folder',menu_name+title,link,257)
	return

def SORTING(url):
	#DIALOG_OK(url,'')
	url2,data2 = URLDECODE(url)
	response2 = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST',url2,data2,'',True,'','ARABSEED-SORTING-1st')
	html = response2.content
	html_blocks = re.findall('class="time-filtering(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		addMenuItem('folder',menu_name+'الكل',url,251)
		block = html_blocks[0]
		items = re.findall('<a data-day="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for sortBy,title in items:
			title = 'ترتيب حسب:    '+title
			link = url.replace('&term=','&day='+sortBy+'&term=')
			addMenuItem('folder',menu_name+title,link,251)
	else: TITLES(url)
	return

def TITLES(url):
	#DIALOG_OK(url,'TITLES')
	if '/ajaxCenter/' in url:
		url2,data2 = URLDECODE(url)
		headers2 = headers
		headers2['Content-Type'] = 'application/x-www-form-urlencoded'
		response2 = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST',url2,data2,headers2,True,'','ARABSEED-TITLES-1st')
		html = response2.content
		block = html
	else:
		html = OPENURL_CACHED(SHORT_CACHE,url,'',headers,'','ARABSEED-TITLES-2nd')
		html_blocks = re.findall('class="FilteringArea(.*?)class="pagination',html,re.DOTALL)
		if not html_blocks: return
		block = html_blocks[0]
	itemLIST = ['مشاهدة','فيلم','اغنية','كليب','اعلان','هداف','مباراة','عرض','مهرجان','البوم']
	items = re.findall('class="BlockItem.*?href="(.*?)".*?title="(.*?)".*?data-src="(.*?)"',block,re.DOTALL)
	allTitles = []
	for link,title,img in items:
		#if '/series/' in link: continue
		#link = unquote(link).strip('/')
		#title = title.strip(' ')
		#if '/film/' in link or any(value in title for value in itemLIST):
		#	addMenuItem('video',menu_name+title,link,252,img)
		#elif '/episode/' in link and 'الحلقة' in title:
		title = unescapeHTML(title)
		if any(value in title for value in itemLIST):
			addMenuItem('video',menu_name+title,link,252,img)
		else:
			mod = ''
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = episode[0]
				mod = '_MOD_'
			if title not in allTitles:
				allTitles.append(title)
				title = mod+title
				addMenuItem('folder',menu_name+title,link,253,img)
	html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<li>(.*?)href="(.*?)">(.*?)<',block,re.DOTALL)
		for check,link,title in items:
			if 'active' in check: continue
			#link = unescapeHTML(link)
			#title = title.replace('الصفحة ','')
			if 'http' not in link: link = website0a+link
			title = unescapeHTML(title)
			if title!='': addMenuItem('folder',menu_name+'صفحة '+title,link,251)
	return

def EPISODES(url):
	#DIALOG_OK(url,url)
	episodesCount,items,itemsNEW = -1,[],[]
	html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,'','ARABSEED-EPISODES-1st')
	items = re.findall('episode-block.*?href="(.*?)".*?<span>(.*?)</span>',html,re.DOTALL)
	name = xbmc.getInfoLabel('ListItem.Label')
	for link,episode in items:
		title = 'الحلقة رقم '+episode
		addMenuItem('video',menu_name+title,link,252)
	return
	"""
	items.append(url)
	items = set(items)
	name = xbmc.getInfoLabel('ListItem.Label')
	for link in items:
		#link = link.strip('/')
		#title = '_MOD_' + link.split('/')[-1].replace('-',' ')
		sequence = re.findall('الحلقة-(\d+)',link.split('/')[-1],re.DOTALL)
		if sequence: sequence = sequence[0]
		else: sequence = '0'
		itemsNEW.append([link,title,sequence])
	items = sorted(itemsNEW, reverse=False, key=lambda key: int(key[2]))
	seasonsCount = str(items).count('/season/')
	episodesCount = str(items).count('/episode/')
	if seasonsCount>1 and episodesCount>0 and '/season/' not in url:
		for link,title,sequence in items:
			if '/season/' in link: addMenuItem('folder',menu_name+title,link,253)
	else:
		for link,title,sequence in items:
			if '/season/' not in link: addMenuItem('video',menu_name+title,link,252)
	"""

def PLAY(url):
	#LOG_THIS('NOTICE','EMAD 111')
	linkLIST = []
	parts = url.split('/')
	#DIALOG_OK(url,'PLAY-1st')
	#url = unquote(quote(url))
	hostname = SERVER(url)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'',headers,True,True,'ARABSEED-PLAY-1st')
	html = response.content#.encode('utf8')
	id = re.findall('postId:"(.*?)"',html,re.DOTALL)
	if not id: id = re.findall('post_id=(.*?)"',html,re.DOTALL)
	if not id: id = re.findall('post-id="(.*?)"',html,re.DOTALL)
	if id: id = id[0]
	else: DIALOG_OK('رسالة من المبرمج','يرجى إرسال هذه المشكلة إلى المبرمج  من قائمة خدمات البرنامج')
	if '/post/' in url and 'seed' in url: url = hostname+'/watch/'+id
	#LOG_THIS('NOTICE','EMAD START TIMING 111')
	if True or '/watch/' in html:
		#parts = url.split('/')
		url2 = url+'watch'
		response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url2,'',headers,True,True,'ARABSEED-PLAY-2nd')
		html2 = response.content#.encode('utf8')
		items1 = re.findall('data-embedd="(.*?)".*?alt="(.*?)"',html2,re.DOTALL)
		items2 = re.findall('data-embedd=".*?(http.*?)("|&quot;)',html2,re.DOTALL)
		items3 = re.findall('src=&quot;(.*?)&quot;.*?>(.*?)<',html2,re.DOTALL|re.IGNORECASE)
		items4 = re.findall('data-embedd="(.*?)">\n*.*?server_image">\n(.*?)\n',html2)
		items5 = re.findall('src=&quot;(.*?)&quot;.*?alt="(.*?)"',html2,re.DOTALL|re.IGNORECASE)
		items6 = re.findall('server="(.*?)".*?<span>(.*?)<',html2,re.DOTALL|re.IGNORECASE)
		items = items1+items2+items3+items4+items5+items6
		#LOG_THIS('NOTICE','EMAD START TIMING 444')
		if not items:
			items = re.findall('<span>(.*?)</span>.*?src="(.*?)"',html2,re.DOTALL|re.IGNORECASE)
			items = [(b,a) for a,b in items]
		for server,title in items:
			if '.png' in server: continue
			if '.jpg' in server: continue
			if '&quot;' in server: continue
			quality = re.findall('\d\d\d+',title,re.DOTALL)
			if quality:
				quality = quality[0]
				if quality in title: title = title.replace(quality+'p','').replace(quality,'').strip(' ')
				quality = '____'+quality
			else: quality = ''
			#LOG_THIS('NOTICE','['+str(id)+']  ['+str(hostname)+']  ['+str(title)+']  ['+str(quality)+']')
			if server.isdigit():
				link = hostname+'/wp-content/themes/ArbSeed/Server.php?'+'post='+id+'&index='+server+'?named='+title+'__watch'+quality
			else:
				if 'http' not in server: server = 'http:'+server
				quality = re.findall('\d\d\d+',title,re.DOTALL)
				if quality: quality = '____'+quality[0]
				else: quality = ''
				link = server+'?named=__watch'+quality
			linkLIST.append(link)
	#LOG_THIS('NOTICE','['+quality+']    ['+title+']')
	#selection = DIALOG_SELECT('أختر البحث المناسب', linkLIST)
	#DIALOG_OK('watch 1',	str(len(items)))
	if 'DownloadNow' in html:
		headers2 = headers
		headers2['Content-Type'] = 'application/x-www-form-urlencoded'
		url2 = url+'/download'
		response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url2,'',headers2,True,'','ARABSEED-PLAY-3rd')
		html2 = response.content#.encode('utf8')
		#DIALOG_OK(url2,html2)
		html_blocks = re.findall('<ul class="download-items(.*?)</ul>',html2,re.DOTALL)
		for block in html_blocks:
			items = re.findall('href="(http.*?)".*?<span>(.*?)<.*?<p>(.*?)<',block,re.DOTALL)
			for link,name,quality in items:
				link = link+'?named='+name+'__download'+'____'+quality
				linkLIST.append(link)
	elif '/download/' in html:
		headers2 = headers
		headers2['X-Requested-With'] = 'XMLHttpRequest'
		url2 = hostname + '/ajaxCenter?_action=getdownloadlinks&postId='+id
		response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url2,'',headers2,True,True,'ARABSEED-PLAY-4th')
		html2 = response.content#.encode('utf8')
		if 'download-btns' in html2:
			items3 = re.findall('href="(.*?)"',html2,re.DOTALL)
			for url3 in items3:
				if '/page/' not in url3 and 'http' in url3:
					url3 = url3+'?named=__download'
					linkLIST.append(url3)
				elif '/page/' in url3:
					quality = ''
					response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url3,'',headers,True,True,'ARABSEED-PLAY-5th')
					html4 = response.content#.encode('utf8')
					blocks = re.findall('(<strong>.*?)-----',html4,re.DOTALL)
					for block4 in blocks:
						server4 = ''
						items4 = re.findall('<strong>(.*?)</strong>',block4,re.DOTALL)
						for item4 in items4:
							item = re.findall('\d\d\d+',item4,re.DOTALL)
							if item:
								quality = '____'+item[0]
								break
						for item4 in reversed(items4):
							item = re.findall('\w\w+',item4,re.DOTALL)
							if item:
								server4 = item[0]
								break
						items5 = re.findall('href="(.*?)"',block4,re.DOTALL)
						for link5 in items5:
							link5 = link5+'?named='+server4+'__download'+quality
							linkLIST.append(link5)
			#DIALOG_OK('download 1',	str(len(linkLIST))	)
		elif 'slow-motion' in html2:
			html2 = html2.replace('<h6 ','==END== ==START==')+'==END=='
			html2 = html2.replace('<h3 ','==END== ==START==')+'==END=='
			#LOG_THIS('NOTICE',html2)
			#with open('s:\\emad.html','w') as f: f.write(html2)
			all_blocks = re.findall('==START==(.*?)==END==',html2,re.DOTALL)
			if all_blocks:
				for block4 in all_blocks:
					if 'href=' not in block4: continue
					#DIALOG_OK('download 111',	block4	)
					quality4 = ''
					items4 = re.findall('slow-motion">(.*?)<',block4,re.DOTALL)
					for item4 in items4:
						item = re.findall('\d\d\d+',item4,re.DOTALL)
						if item:
							quality4 = '____'+item[0]
							break
					items4 = re.findall('<td>(.*?)</td>.*?href="(http.*?)"',block4,re.DOTALL)
					if items4:
						for server4,link4 in items4:
							link4 = link4+'?named='+server4+'__download'+quality4
							linkLIST.append(link4)
					else:
						items4 = re.findall('href="(.*?http.*?)".*?name">(.*?)<',block4,re.DOTALL)
						for link4,server4 in items4:
							link4 = link4.strip(' ')+'?named='+server4+'__download'+quality4
							linkLIST.append(link4)
			else:
				items4 = re.findall('href="(.*?)".*?>(\w+)<',html2,re.DOTALL)
				for link4,server4 in items4:
					link4 = link4.strip(' ')+'?named='+server4+'__download'
					linkLIST.append(link4)
	#LOG_THIS('NOTICE','EMAD 222')
	#DIALOG_OK('both: watch & download',	str(len(linkLIST))	)
	#selection = DIALOG_SELECT('أختر البحث المناسب', linkLIST)
	if len(linkLIST)==0: DIALOG_OK('رسالة من المبرمج','الرابط ليس فيه فيديو')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name,'video')
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','%20')
	url = website0a+'/?s='+search
	TITLES(url)
	return

def FILTERS_MENU(url,filter):
	filter = filter.replace('_FORGETRESULTS_','')
	#DIALOG_OK(filter,url)
	menu_list = ['category','genre','release-year']
	if '?' in url: url = url.split('/wp-content/themes/ArbSeed/ajaxCenter/Home/AdvFiltering.php?')[0]
	type,filter = filter.split('___',1)
	if filter=='': filter_options,filter_values = '',''
	else: filter_options,filter_values = filter.split('___')
	if type=='CATEGORIES':
		if menu_list[0]+'=' not in filter_options: category = menu_list[0]
		for i in range(len(menu_list[0:-1])):
			if menu_list[i]+'=' in filter_options: category = menu_list[i+1]
		new_options = filter_options+'&'+category+'=0'
		new_values = filter_values+'&'+category+'=0'
		new_filter = new_options.strip('&')+'___'+new_values.strip('&')
		clean_filter = RECONSTRUCT_FILTER(filter_values,'all')
		#DIALOG_OK('','')
		filter_show = RECONSTRUCT_FILTER(filter_options,'modified_values')
		if filter_show=='': url2 = url
		else: url2 = url+'/wp-content/themes/ArbSeed/ajaxCenter/Home/AdvFiltering.php?'+clean_filter
	elif type=='FILTERS':
		filter_show = RECONSTRUCT_FILTER(filter_options,'modified_values')
		filter_show = unquote(filter_show)
		if filter_values!='': filter_values = RECONSTRUCT_FILTER(filter_values,'all')
		if filter_values=='' or filter_show=='': url2 = url
		else: url2 = url+'/wp-content/themes/ArbSeed/ajaxCenter/Home/AdvFiltering.php?'+filter_values
		#DIALOG_OK(url2,filter_values)
		addMenuItem('folder',menu_name+'أظهار قائمة الفيديو التي تم اختيارها ',url2,251)
		addMenuItem('folder',menu_name+' [[   '+filter_show+'   ]]',url2,251)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = OPENURL_CACHED(LONG_CACHE,url,'',headers,'','ARABSEED-FILTERS_MENU-1st')
	html_blocks = re.findall('class="filteringMore">.(.*?)</ul>',html,re.DOTALL)
	#DIALOG_OK('',str(html_blocks))
	block = html_blocks[0]
	select_blocks = re.findall('dropdown-button.*?</i>(.*?)</span>.*?data-tax="(.*?)"(.*?)</div>',block,re.DOTALL)
	dict = {}
	for name,category2,block in select_blocks:
		name = name.replace('--','')
		items = re.findall('data-term="(.*?)".*?</i>(.*?)</li>',block,re.DOTALL)
		#if '=' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==menu_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES___'+new_filter)
				return
			else:
				#DIALOG_OK(url,url2)
				if category2==menu_list[-1]: addMenuItem('folder',menu_name+'الكل ',url2,251)
				else: addMenuItem('folder',menu_name+'الكل ',url2,255,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&'+category2+'=0'
			new_values = filter_values+'&'+category2+'=0'
			new_filter = new_options+'___'+new_values
			addMenuItem('folder',menu_name+'الكل :'+name,url2,254,'','',new_filter+'_FORGETRESULTS_')
		dict[category2] = {}
		for value,option in items:
			if 'الكل' in option: continue
			if option in ignoreLIST: continue
			#if 'value' not in value: value = option
			#else: value = re.findall('"(.*?)"',value,re.DOTALL)[0]
			dict[category2][value] = option
			new_options = filter_options+'&'+category2+'='+option
			new_values = filter_values+'&'+category2+'='+value
			new_filter2 = new_options+'___'+new_values
			title = option+' :'#+dict[category2]['0']
			title = option+' :'+name
			if type=='FILTERS': addMenuItem('folder',menu_name+title,url,254,'','',new_filter2+'_FORGETRESULTS_')
			elif type=='CATEGORIES' and menu_list[-2]+'=' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'all')
				url3 = url+'/wp-content/themes/ArbSeed/ajaxCenter/Home/AdvFiltering.php?'+clean_filter
				addMenuItem('folder',menu_name+title,url3,251)
			else: addMenuItem('folder',menu_name+title,url,255,'','',new_filter2)
	return

def RECONSTRUCT_FILTER(filters,mode):
	#DIALOG_OK(filters,'RECONSTRUCT_FILTER 11')
	# mode=='modified_values'		only non empty values
	# mode=='modified_filters'		only non empty filters
	# mode=='all'					all filters (includes empty filter)
	# example:  year=58796&category=2961&language=&country=&genre=
	filters = filters.replace('=&','=0&')
	filters = filters.strip('&')
	filtersDICT = {}
	if '=' in filters: url2,filtersDICT = URLDECODE(filters)
	new_filters = ''
	filter_list = ['release-year','category','language','country','genre']
	for key in filter_list:
		if key in filtersDICT.keys(): value = filtersDICT[key]
		else: value = '0'
		if '%' not in value: value = quote(value)
		if mode=='modified_values' and value!='0': new_filters = new_filters+' + '+value
		elif mode=='modified_filters' and value!='0': new_filters = new_filters+'&'+key+'='+value
		elif mode=='all': new_filters = new_filters+'&'+key+'='+value
	new_filters = new_filters.strip(' + ')
	new_filters = new_filters.strip('&')
	new_filters = new_filters.replace('=0','=')
	new_filters = new_filters.replace('release-year','year')
	#DIALOG_OK(new_filters,'RECONSTRUCT_FILTER 22')
	return new_filters

"""
def SEARCH_OLD(search):
	if '___' in search:
		search = search.split('___')[0]
		category = False
	else: category = True
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','+')
	html = OPENURL_CACHED(LONG_CACHE,website0a,'',headers,'','ARABSEED-SEARCH-1st')
	html_blocks = re.findall('name="category(.*?)</div>',html,re.DOTALL)
	if category and html_blocks:
		block = html_blocks[0]
		items = re.findall('value="(.*?)".*?>(.*?)<',block,re.DOTALL)
		categoryLIST,filterLIST = [''],['الكل']
		for category,title in items:
			if title in ['مصارعه']: continue
			categoryLIST.append(category)
			filterLIST.append(title)
		selection = DIALOG_SELECT('اختر الفلتر المناسب:', filterLIST)
		if selection == -1 : return
		category = categoryLIST[selection]
	else: category = ''
	url = website0a + '/search?s='+search+'&category='+category
	TITLES(url)
	return
"""



