# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='MYCIMA'
headers = {'User-Agent':''}
menu_name='_MCM_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['مصارعة حرة']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==360: results = MENU(url)
	elif mode==361: results = TITLES(url,text)
	elif mode==362: results = PLAY(url)
	elif mode==363: results = EPISODES(url,text)
	elif mode==364: results = FILTERS_MENU(url,'CATEGORIES___'+text)
	elif mode==365: results = FILTERS_MENU(url,'FILTERS___'+text)
	elif mode==366: results = SUBMENU(url)
	elif mode==369: results = SEARCH(text,url)
	else: results = False
	return results

def MENU(website=''):
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',website0a,'','',False,'','MYCIMA-MENU-1st')
	hostname = response.headers['Location']
	hostname = hostname.strip('/')
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع',hostname,369,'','','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'فلتر محدد',hostname,364)
		addMenuItem('folder',menu_name+'فلتر كامل',hostname,365)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	headers2 = {'Referer':hostname,'User-Agent':''}
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',hostname,'',headers2,'','','MYCIMA-MENU-2nd')
	html = response.content
	html_blocks = re.findall('class="RightUI"(.*?)anime',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?span>(.*?)<',block,re.DOTALL)
		for link,title in items:
			addMenuItem('folder',website+'___'+menu_name+title,link,366)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks = re.findall('middle--header(.*?)middle--header',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('class="menu-item.*?href="(.*?)">(.*?)<',block,re.DOTALL)
		for link,title in items:
			if hostname not in link:
				server = SERVER(link)
				link = link.replace(server,hostname)
			if '/download-series' in link:
				title = 'تحميل مسلسلات برابط واحد'
				addMenuItem('folder',website+'___'+menu_name+title,link,361)
			else:
				if title=='': continue
				if not any(value in title for value in ignoreLIST):
					addMenuItem('folder',website+'___'+menu_name+title,link,366)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks = re.findall('hoverable activable(.*?)hoverable activable',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?url\((.*?)\).*?span>(.*?)<',block,re.DOTALL)
		for link,img,title in items:
			addMenuItem('folder',website+'___'+menu_name+title,link,366,img)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def SUBMENU(url):
	#DIALOG_OK(url,'')
	headers2 = {'Referer':url,'User-Agent':''}
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'',headers2,'','','MYCIMA-SUBMENU-1st')
	html = response.content
	if 'class="Slider--Grid"' in html:
		addMenuItem('folder',menu_name+'المميزة',url,361,'','','featured')
	html_blocks = re.findall('class="list--Tabsui"(.*?)div',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?i>(.*?)<',block,re.DOTALL)
		for link,title in items:
			addMenuItem('folder',menu_name+title,link,361)
	return

def TITLES(url,type=''):
	#DIALOG_OK(url,'TITLES')
	headers2 = {'Referer':url,'User-Agent':''}
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'',headers2,'','','MYCIMA-TITLES-1st')
	html = response.content
	#LOG_THIS('NOTICE',html)
	#DIALOG_OK(str(html_blocks),html)
	if type=='featured':
		html_blocks = re.findall('class="Slider--Grid"(.*?)class="list--Tabsui"',html,re.DOTALL)
	elif type=='filters':
		html_blocks = [html.replace('\\/','/').replace('\\"','"')]
	else:
		html_blocks = re.findall('class="Grid--MycimaPosts"(.*?)</li></ul></div></div>',html,re.DOTALL)
	allTitles = []
	if html_blocks:
		block = html_blocks[0]
		#DIALOG_OK('TITLES - FILTERS',block)
		items = re.findall('GridItem"><a href="(.*?)" title="(.*?)".*?url\((.*?)\)',block,re.DOTALL)
		for link,title,img in items:
			title = unescapeHTML(title)
			title = escapeUNICODE(title)
			title = title.replace('مشاهدة ','')
			if '/series/' in link: addMenuItem('folder',menu_name+title,link,363,img)
			elif 'حلقة' in title:
				episode = re.findall('(.*?) +حلقة +\d+',title,re.DOTALL)
				if episode: title = '_MOD_' + episode[0]
				if title not in allTitles:
					allTitles.append(title)
					addMenuItem('folder',menu_name+title,link,363,img)
			else:
				addMenuItem('video',menu_name+title,link,362,img)
		if type=='filters':
			nextpage = re.findall('"more_button_page":(.*?),',block,re.DOTALL)
			if nextpage:
				count = nextpage[0]
				link = url+'/offset/'+count
				addMenuItem('folder',menu_name+'صفحة أخرى',link,361,'','','filters')
		elif type=='':
			html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
			if html_blocks:
				block = html_blocks[0]
				items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
				for link,title in items:
					title = 'صفحة '+unescapeHTML(title)
					addMenuItem('folder',menu_name+title,link,361)
	return

def EPISODES(url,type=''):
	headers2 = {'Referer':url,'User-Agent':''}
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'',headers2,'','','MYCIMA-EPISODES-1st')
	html = response.content
	html_blocks = re.findall('class="Seasons--Episodes"(.*?)</singlesection',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		if type=='':
			items = re.findall('href="(.*?)">(.*?)</a>',block,re.DOTALL)
			for link,title in items:
				if 'episode' in title: continue
				addMenuItem('folder',menu_name+title,link,363,'','','episodes')
		if len(menuItemsLIST)==0:
			items = re.findall('href="(.*?)".*?<episodeTitle>(.*?)<',block,re.DOTALL)
			for link,title in items:
				title = title.strip(' ')
				addMenuItem('video',menu_name+title,link,362)
	if len(menuItemsLIST)==0:
		title = re.findall('<title>(.*?)<',html,re.DOTALL)
		if title: title = title[0].replace(' - ماي سيما','').replace('مشاهدة ','')
		else: title = 'ملف التشغيل'
		addMenuItem('video',menu_name+title,url,362)
	return

def PLAY(url):
	linkLIST = []
	headers2 = {'Referer':url,'User-Agent':''}
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url,'',headers2,'','','MYCIMA-PLAY-1st')
	html = response.content
	ratingLIST = re.findall('<span>التصنيف<.*?<a.*?">(.*?)<.*?">(.*?)<',html,re.DOTALL)
	if ratingLIST:
		ratingLIST = [ratingLIST[0][0],ratingLIST[0][1]]
		if RATING_CHECK(script_name,url,ratingLIST): return
	# watch links
	html_blocks = re.findall('class="WatchServersList"(.*?)class="WatchServersEmbed"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('data-url="(.*?)".*?strong>(.*?)<',block,re.DOTALL)
		for link,name in items:
			if name=='سيرفر ماي سيما': name = 'mycima'
			link = link+'?named='+name+'__watch'
			linkLIST.append(link)
	# download links
	html_blocks = re.findall('class="List--Download(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?</i>(.*?)<',block,re.DOTALL)
		for link,quality in items:
			quality = re.findall('\d\d\d+',quality,re.DOTALL)
			if quality: quality = '____'+quality[0]
			else: quality = ''
			link = link+'?named=mycima'+'__download'+quality
			linkLIST.append(link)
	#selection = DIALOG_SELECT('أختر البحث المناسب', linkLIST)
	if len(linkLIST)==0: DIALOG_OK('رسالة من المبرمج','الرابط ليس فيه فيديو')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name,'video')
	return

def SEARCH(search,hostname):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','+')
	linkLIST = ['/','/list/series','/list/anime','/list/tv','/list']
	nameLIST = ['الأفلام','المسلسلات','الانيمي و الكرتون','البرامج تليفزيونية','غير محدد']
	selection = DIALOG_SELECT('اختر النوع المطلوب:', nameLIST)
	if selection == -1 : return ''
	if hostname=='':
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',website0a,'','',False,'','MYCIMA-SEARCH-1st')
		hostname = response.headers['Location']
		hostname = hostname.strip('/')
	url2 = hostname+'/search/'+search+linkLIST[selection]
	TITLES(url2)
	return

def FILTERS_MENU(url,filter):
	#DIALOG_OK(filter,url)
	headers2 = {'Referer':url,'User-Agent':''}
	filter = filter.replace('_FORGETRESULTS_','')
	if '??' in url: url = url.split('//getposts??')[0]
	type,filter = filter.split('___',1)
	if filter=='': filter_options,filter_values = '',''
	else: filter_options,filter_values = filter.split('___')
	if type=='CATEGORIES':
		if all_categories_list[0]+'==' not in filter_options: category = all_categories_list[0]
		for i in range(len(all_categories_list[0:-1])):
			if all_categories_list[i]+'==' in filter_options: category = all_categories_list[i+1]
		new_options = filter_options+'&&'+category+'==0'
		new_values = filter_values+'&&'+category+'==0'
		new_filter = new_options.strip('&&')+'___'+new_values.strip('&&')
		clean_filter = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		url2 = url+'//getposts??'+clean_filter
	elif type=='FILTERS':
		filter_show = RECONSTRUCT_FILTER(filter_options,'modified_values')
		filter_show = unquote(filter_show)
		if filter_values!='': filter_values = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		if filter_values=='': url2 = url
		else: url2 = url+'//getposts??'+filter_values
		url4 = PREPARE_FILTER_FINAL_URL(url2)
		addMenuItem('folder',menu_name+'أظهار قائمة الفيديو التي تم اختيارها ',url4,361,'','','filters')
		addMenuItem('folder',menu_name+' [[   '+filter_show+'   ]]',url4,361,'','','filters')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'',headers2,'','','MYCIMA-FILTERS_MENU-1st')
	html = response.content
	html_blocks = re.findall('<mycima--filter(.*?)</mycima--filter>',html,re.DOTALL)
	block = html_blocks[0]
	select_blocks = re.findall('taxonomy="(.*?)".*?<span>(.*?)<(.*?)<filterbox',block+'<filterbox',re.DOTALL)
	dict = {}
	for category2,name,block in select_blocks:
		if 'interest' in category2: continue
		items = re.findall('data-term="(.*?)".*?<txt>(.*?)</txt>',block,re.DOTALL)
		if '==' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==all_categories_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES___'+new_filter)
				return
			else:
				url4 = PREPARE_FILTER_FINAL_URL(url2)
				if category2==all_categories_list[-1]: addMenuItem('folder',menu_name+'الجميع ',url4,361,'','','filters')
				else: addMenuItem('folder',menu_name+'الجميع ',url2,364,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&&'+category2+'==0'
			new_values = filter_values+'&&'+category2+'==0'
			new_filter = new_options+'___'+new_values
			addMenuItem('folder',menu_name+'الجميع :'+name,url2,365,'','',new_filter+'_FORGETRESULTS_')
		dict[category2] = {}
		for value,option in items:
			if option in ignoreLIST: continue
			if 'http' in option: continue
			if 'الكل' in option: continue
			if 'n-a' in value: continue
			title1,title2 = option,option
			name1 = re.findall('<name>(.*?)</name>',option,re.DOTALL)
			if name1:
				title1 = name1[0]
				name2 = re.findall('<describe>(.*?)</describe>',option,re.DOTALL)
				if name2: title2 = title1+': '+name2[0]
			dict[category2][value] = title2
			new_options = filter_options+'&&'+category2+'=='+title1
			new_values = filter_values+'&&'+category2+'=='+value
			new_filter2 = new_options+'___'+new_values
			if type=='FILTERS':
				addMenuItem('folder',menu_name+title2,url,365,'','',new_filter2+'_FORGETRESULTS_')
			elif type=='CATEGORIES' and all_categories_list[-2]+'==' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'modified_filters')
				#DIALOG_OK(clean_filter,new_values)
				url3 = url+'//getposts??'+clean_filter
				url4 = PREPARE_FILTER_FINAL_URL(url3)
				addMenuItem('folder',menu_name+title2,url4,361,'','','filters')
			else: addMenuItem('folder',menu_name+title2,url,364,'','',new_filter2)
	return

all_categories_list = ['genre','release-year','nation']
all_filters_list = ['mpaa','genre','release-year','category','Quality','interest','nation','language']

def PREPARE_FILTER_FINAL_URL(url):
	url2 = url.replace('//getposts??','/AjaxCenter/Filtering/').replace('&&','/').replace('==','/')
	return url2

def RECONSTRUCT_FILTER(filters,mode):
	#DIALOG_OK(filters,'IN    '+mode)
	# mode=='modified_values'		only non empty values
	# mode=='modified_filters'		only non empty filters
	# mode=='all'					all filters (includes empty filter)
	filters = filters.strip('&&')
	filtersDICT,new_filters = {},''
	if '==' in filters:
		items = filters.split('&&')
		for item in items:
			var,value = item.split('==')
			filtersDICT[var] = value
	for key in all_filters_list:
		if key in filtersDICT.keys(): value = filtersDICT[key]
		else: value = '0'
		if '%' not in value: value = quote(value)
		if mode=='modified_values' and value!='0': new_filters = new_filters+' + '+value
		elif mode=='modified_filters' and value!='0': new_filters = new_filters+'&&'+key+'=='+value
		elif mode=='all': new_filters = new_filters+'&&'+key+'=='+value
	new_filters = new_filters.strip(' + ')
	new_filters = new_filters.strip('&&')
	#DIALOG_OK(new_filters,'OUT')
	return new_filters

