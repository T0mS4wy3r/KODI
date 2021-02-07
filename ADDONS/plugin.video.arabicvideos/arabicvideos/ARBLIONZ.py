# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='ARBLIONZ'
headers = { 'User-Agent' : '' }
menu_name='_ARL_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['عروض المصارعة','الكل','رياضة و مصارعه','الرئيسية','العاب','برامج كمبيوتر','موبايل و جوال','القسم الاسلامي']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==200: results = MENU(url)
	elif mode==201: results = TITLES(url)
	elif mode==202: results = PLAY(url)
	elif mode==203: results = EPISODES(url)
	elif mode==204: results = FILTERS_MENU(url,'FILTERS___'+text)
	elif mode==205: results = FILTERS_MENU(url,'CATEGORIES___'+text)
	elif mode==209: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',209,'','','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'فلتر محدد',website0a,205)
		addMenuItem('folder',menu_name+'فلتر كامل',website0a,204)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#addMenuItem('folder',menu_name+'فلتر','',114,website0a)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a+'/alz','',headers,True,'','ARBLIONZ-MENU-1st')
	html = response.content#.encode('utf8')
	html_blocks = re.findall('categories-tabs(.*?)advanced-search',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('data-get="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
		for url,title in items:
			link = website0a+'/getposts?type=one&data='+url
			addMenuItem('folder',website+'___'+menu_name+title,link,201)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#WRITE_FILE(html)
	html_blocks = re.findall('navigation-menu(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
	for link,title in items:
		if 'http' not in link: link = website0a+link
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
			addMenuItem('folder',website+'___'+menu_name+title,link,201)
	return html

def TITLES(url):
	if url==website0a: url = url+'/alz'
	#DIALOG_OK(url,'TITLES')
	"""
	# for POST filter:
	if '/getposts?' in url:
		url2,filters2 = url.split('?')
		url2 = url2.replace('/getposts','/ajaxCenter?_action=AjaxFilteringData&_count=50')
		#DIALOG_OK(url2,filters2)
		data2 = {'form':filters2,'FilterWord=':''}
		headers2 = headers
		headers2['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
		headers2['X-Requested-With'] = 'XMLHttpRequest'
		headers2['X-CSRF-TOKEN'] = 'GZ4Od0njTCaGwcGq4IzGqHErY0uZoaUXZC6HeXxx'
		headers2['Cookie'] = 'warblionztv_session=eyJpdiI6ImR0MXNJYlRLQjdaNDkxVndGZ1B2YlE9PSIsInZhbHVlIjoiQTRRVXM1UjlGbFFraUFkOExEOUVQYU41d1NWeHcwenMyVWRFQml2UXI0dkxlZ1Bna3pXS1BWbTA3SmNjdFd3WCIsIm1hYyI6IjUxZTgyNmMyOGEyMjI0NDNlZjhlN2NkZTBmNjdmYzA0NjAwMTJkMzZjODIzNTYyMzk0NDc5MTBjNWIyOTljNjgifQ=='
		response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'POST',url2,data2,headers2,True,'','ARBLIONZ-TITLES-1st')
		html = response.content#.encode('utf8')
	else:
	"""
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'',headers,True,'','ARBLIONZ-TITLES-2nd')
	html = response.content#.encode('utf8')
	if 'getposts' in url: block = html
	else:
		html_blocks = re.findall('page-content(.*?)main-footer',html,re.DOTALL)
		block = html_blocks[0]
	#items = re.findall('class="box.*?src="(.*?)".*?href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	items = re.findall('content-box".*?src="(.*?)".*?href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	allTitles = []
	itemLIST = ['مشاهدة','فيلم','اغنية','كليب','اعلان','هداف','مباراة','عرض','مهرجان','البوم']
	for img,link ,title in items:
		#link = escapeUNICODE(link)
		#link = quote(link)
		if '/series/' in link: continue
		link = link.strip('/')
		title = unescapeHTML(title)
		title = title.strip(' ')
		if '/film/' in link or any(value in title for value in itemLIST):
			addMenuItem('video',menu_name+title,link,202,img)
		elif '/episode/' in link and 'الحلقة' in title:
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = '_MOD_' + episode[0]
				if title not in allTitles:
					addMenuItem('folder',menu_name+title,link,203,img)
					allTitles.append(title)
		elif '/pack/' in link:
			addMenuItem('folder',menu_name+title,link+'/films',201,img)
		else: addMenuItem('folder',menu_name+title,link,203,img)
	html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<a href=["\'](http.*?)["\'].*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = unescapeHTML(link)
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			if 'search?s=' in url:
				page_new = link.split('page=')[1]
				page_old = url.split('page=')[1]
				link = url.replace('page='+page_old,'page='+page_new)
			if title!='': addMenuItem('folder',menu_name+'صفحة '+title,link,201)
	return

def EPISODES(url):
	#DIALOG_OK(url,'')
	episodesCount,items,itemsNEW = -1,[],[]
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'',headers,True,'','ARBLIONZ-EPISODES-1st')
	html = response.content#.encode('utf8')
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
			if '/season/' in link:
				#link = quote(link)
				addMenuItem('folder',menu_name+title,link,203)
	else:
		for link,title,sequence in items:
			if '/season/' not in link:
				#if '%' not in link: link = quote(link)
				#else: link = quote(unquote(link))
				#link = unquote(link)
				title = unquote(title)
				addMenuItem('video',menu_name+title,link,202)
	return

def PLAY(url):
	#LOG_THIS('NOTICE','EMAD 111')
	linkLIST = []
	parts = url.split('/')
	#DIALOG_OK(url,'PLAY-1st')
	#url = unquote(quote(url))
	hostname = website0a
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'',headers,True,True,'ARBLIONZ-PLAY-1st')
	html = response.content#.encode('utf8')
	id = re.findall('postId:"(.*?)"',html,re.DOTALL)
	if not id: id = re.findall('post_id=(.*?)"',html,re.DOTALL)
	if not id: id = re.findall('post-id="(.*?)"',html,re.DOTALL)
	if id: id = id[0]
	else: DIALOG_OK('رسالة من المبرمج','يرجى إرسال هذه المشكلة إلى المبرمج  من قائمة خدمات البرنامج')
	#LOG_THIS('NOTICE','EMAD START TIMING 111')
	if '/watch/' in html:
		#parts = url.split('/')
		url2 = url.replace(parts[3],'watch')
		response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url2,'',headers,True,True,'ARBLIONZ-PLAY-2nd')
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
				link = hostname+'/?postid='+id+'&serverid='+server+'?named='+title+'__watch'+quality
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
		headers2 = { 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8' }
		url2 = url+'/download'
		response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url2,'',headers2,True,'','ARBLIONZ-PLAY-3rd')
		html2 = response.content#.encode('utf8')
		#DIALOG_OK(url2,html2)
		html_blocks = re.findall('<ul class="download-items(.*?)</ul>',html2,re.DOTALL)
		for block in html_blocks:
			items = re.findall('href="(http.*?)".*?<span>(.*?)<.*?<p>(.*?)<',block,re.DOTALL)
			for link,name,quality in items:
				link = link+'?named='+name+'__download'+'____'+quality
				linkLIST.append(link)
	elif '/download/' in html:
		headers2 = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
		url2 = hostname + '/ajaxCenter?_action=getdownloadlinks&postId='+id
		response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url2,'',headers2,True,True,'ARBLIONZ-PLAY-4th')
		html2 = response.content#.encode('utf8')
		if 'download-btns' in html2:
			items3 = re.findall('href="(.*?)"',html2,re.DOTALL)
			for url3 in items3:
				if '/page/' not in url3 and 'http' in url3:
					url3 = url3+'?named=__download'
					linkLIST.append(url3)
				elif '/page/' in url3:
					quality = ''
					response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url3,'',headers,True,True,'ARBLIONZ-PLAY-5th')
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
	search = search.replace(' ','+')
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a+'/alz','',headers,True,'','ARBLIONZ-SEARCH-1st')
	html = response.content#.encode('utf8')
	html_blocks = re.findall('chevron-select(.*?)</div>',html,re.DOTALL)
	if showdialogs and html_blocks:
		block = html_blocks[0]
		items = re.findall('value="(.*?)".*?>(.*?)<',block,re.DOTALL)
		categoryLIST,filterLIST = [],[]
		for category,title in items:
			if title in ['رياضة و مصارعه']: continue
			categoryLIST.append(category)
			filterLIST.append(title)
		selection = DIALOG_SELECT('اختر الفلتر المناسب:', filterLIST)
		if selection == -1 : return
		category = categoryLIST[selection]
	else: category = ''
	url = website0a + '/search?s='+search+'&category='+category+'&page=1'
	TITLES(url)
	return

def FILTERS_MENU(url,filter):
	filter = filter.replace('_FORGETRESULTS_','')
	#DIALOG_OK(filter,url)
	# for POST filter:		menu_list = ['CategoryCheckBox','YearCheckBox','GenreCheckBox','QualityCheckBox']
	menu_list = ['category','release-year','genre','Quality']
	if '?' in url: url = url.split('/getposts?')[0]
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
		clean_filter = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		url2 = url+'/getposts?'+clean_filter
	elif type=='FILTERS':
		filter_show = RECONSTRUCT_FILTER(filter_options,'modified_values')
		filter_show = unquote(filter_show)
		if filter_values!='': filter_values = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		if filter_values=='': url2 = url
		else: url2 = url+'/getposts?'+filter_values
		addMenuItem('folder',menu_name+'أظهار قائمة الفيديو التي تم اختيارها ',url2,201)
		addMenuItem('folder',menu_name+' [[   '+filter_show+'   ]]',url2,201)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = OPENURL_CACHED(LONG_CACHE,url+'/alz','',headers,'','ARBLIONZ-FILTERS_MENU-1st')
	#DIALOG_TEXTVIEWER(url,html)
	html_blocks = re.findall('AjaxFilteringData(.*?)FilterWord',html,re.DOTALL)
	block = html_blocks[0]
	# for POST filter:		select_blocks = re.findall('</i>(.*?)<.*?name="(.*?)"(.*?)<h2',block,re.DOTALL)
	select_blocks = re.findall('</i>(.*?)<.*?data-forTax="(.*?)"(.*?)<h2',block,re.DOTALL)
	#DIALOG_OK('',str(select_blocks))
	dict = {}
	for name,category2,block in select_blocks:
		#name = name.replace('--','')
		name = name.replace('اختيار ','')
		name = name.replace('سنة الإنتاج','السنة')
		items = re.findall('value="(.*?)".*?</div>(.*?)<',block,re.DOTALL)
		if '=' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==menu_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES___'+new_filter)
				return
			else:
				if category2==menu_list[-1]: addMenuItem('folder',menu_name+'الجميع ',url2,201)
				else: addMenuItem('folder',menu_name+'الجميع ',url2,205,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&'+category2+'=0'
			new_values = filter_values+'&'+category2+'=0'
			new_filter = new_options+'___'+new_values
			addMenuItem('folder',menu_name+'الجميع :'+name,url2,204,'','',new_filter+'_FORGETRESULTS_')
		dict[category2] = {}
		for value,option in items:
			option = option.replace('\n','')
			if option in ignoreLIST: continue
			#if option=='الكل': continue
			#option = '['+option+']'
			#if 'الكل' in option: DIALOG_OK('','['+str(option)+']')
			#if 'value' not in value: value = option
			#else: value = re.findall('"(.*?)"',value,re.DOTALL)[0]
			dict[category2][value] = option
			new_options = filter_options+'&'+category2+'='+option
			new_values = filter_values+'&'+category2+'='+value
			new_filter2 = new_options+'___'+new_values
			title = option+' :'#+dict[category2]['0']
			title = option+' :'+name
			if type=='FILTERS': addMenuItem('folder',menu_name+title,url,204,'','',new_filter2+'_FORGETRESULTS_')
			elif type=='CATEGORIES' and menu_list[-2]+'=' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'modified_filters')
				url3 = url+'/getposts?'+clean_filter
				addMenuItem('folder',menu_name+title,url3,201)
			else: addMenuItem('folder',menu_name+title,url,205,'','',new_filter2)
	return

def RECONSTRUCT_FILTER(filters,mode):
	#DIALOG_OK(filters,'RECONSTRUCT_FILTER 11')
	# mode=='modified_values'		only non empty values
	# mode=='modified_filters'		only non empty filters
	# mode=='all'					all filters (includes empty filter)
	filters = filters.replace('=&','=0&')
	filters = filters.strip('&')
	filtersDICT = {}
	if '=' in filters:
		items = filters.split('&')
		for item in items:
			var,value = item.split('=')
			filtersDICT[var] = value
	new_filters = ''
	# for POST filter:		url_filter_list = ['CategoryCheckBox','YearCheckBox','GenreCheckBox','QualityCheckBox']
	url_filter_list = ['category','release-year','genre','Quality']
	for key in url_filter_list:
		if key in filtersDICT.keys(): value = filtersDICT[key]
		else: value = '0'
		if '%' not in value: value = quote(value)
		if mode=='modified_values' and value!='0': new_filters = new_filters+' + '+value
		elif mode=='modified_filters' and value!='0': new_filters = new_filters+'&'+key+'='+value
		elif mode=='all': new_filters = new_filters+'&'+key+'='+value
	new_filters = new_filters.strip(' + ')
	new_filters = new_filters.strip('&')
	new_filters = new_filters.replace('=0','=')
	new_filters = new_filters.replace('Quality','quality')
	#DIALOG_OK(filters,'RECONSTRUCT_FILTER 22')
	return new_filters

"""
filters:	1st method		(used now in website)
adding filter to search
POST:	https://arblionz.art/ajaxCenter?_action=AjaxFilteringData&_count=50
	data:	['CategoryCheckBox','YearCheckBox','GenreCheckBox','QualityCheckBox']
	headers:	Cookie + XREF-TOKEN


filters:	2nd method		(old method but still working)		(used in this program)
GET:	https://arblionz.art/getposts?quality=WEB-DL&release-year=2020



filters:	3rd method		(old method but still working)
GET:	https://arblionz.art/release-year/2019
GET:	https://arblionz.art/quality/4K%20BluRay
"""


