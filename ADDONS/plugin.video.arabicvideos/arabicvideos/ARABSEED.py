# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='ARABSEED'
headers = {'User-Agent':''}
menu_name='_ARS_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['مصارعه','اعلن معنا – For ads','موبايلات','برامج كمبيوتر','العاب كمبيوتر','اسلاميات','اخرى','اقسام اخري','اشتراكات']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==250: results = MENU(url)
	elif mode==251: results = TITLES(url,text)
	elif mode==252: results = PLAY(url)
	elif mode==253: results = EPISODES(url)
	elif mode==254: results = FILTERS_MENU(url,'CATEGORIES___'+text)
	elif mode==255: results = FILTERS_MENU(url,'FILTERS___'+text)
	elif mode==256: results = SUBMENU(url,text)
	elif mode==259: results = SEARCH(text)	
	else: results = False
	return results

def MENU(website=''):
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a+'/main','','','','','ARABSEED-MENU-1st')
	html = response.content
	html_blocks2 = re.findall('aria-current="page"(.*?)</div>',html,re.DOTALL)
	block2 = html_blocks2[0]
	items2 = re.findall('href="(.*?)".*?>(.*?)<',block2,re.DOTALL)
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',259,'','','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'فلتر محدد',website0a+'/category/اخرى',254)
		addMenuItem('folder',menu_name+'فلتر كامل',website0a+'/category/اخرى',255)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder',menu_name+'المضاف حديثاً',website0a+'/lastest',251,'','','lastest')
	addMenuItem('folder',menu_name+'جديد الافلام',website0a+'/main',256,'','','new_movies')
	addMenuItem('folder',menu_name+'جديد الحلقات',website0a+'/main',256,'','','new_episodes')
	for link,title in items2:
		title = unescapeHTML(title)
		if title not in ignoreLIST:
			addMenuItem('folder',website+'___'+menu_name+title,link,256)
	return html

def SUBMENU(url,type):
	#DIALOG_OK(url,type)
	#WRITE_THIS(html)
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','ARABSEED-SUBMENU-1st')
	html = response.content
	if 'class="MainSlides' in html: addMenuItem('folder',menu_name+'المميزة',url,251,'','','featured')
	if 'class="SliderInSection' in html: addMenuItem('folder',menu_name+'الاكثر مشاهدة',url,251,'','','most')
	if 'class="LinksList' in html:
		html_blocks = re.findall('class="LinksList(.*?)</ul>',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			if len(html_blocks)>1 and type=='new_episodes': block = html_blocks[1]
			items = re.findall('href="(.*?)"(.*?)</a>',block,re.DOTALL)
			#DIALOG_OK(str(len(items)),'')
			for link,title in items:
				title2 = re.findall('</i>.*?<span>(.*?)<',title,re.DOTALL)
				if '<strong>' in title: title2 = re.findall('</i>(.*?)<',title,re.DOTALL)
				if not title2: title2 = re.findall('alt="(.*?)"',title,re.DOTALL)
				if title2:
					title2 = title2[0]
					if 'key=' in link: type = link.split('key=')[1]
					else: type = 'newest'
					addMenuItem('folder',menu_name+title2,link,251,'','',type)
	return

def TITLES(url,type):
	#DIALOG_OK(url,type)
	#WRITE_THIS(html)
	if type=='filters':
		if '?' in url:
			url2,data = url.split('?')
			data2 = {}
			lines = data.split('&')
			for line in lines:
				key,value = line.split('=')
				data2[key] = value
		else: url2,data2 = url,''
		response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'POST',url2,data2,'','','','ARABSEED-TITLES-1st')
	else: response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','ARABSEED-TITLES-2nd')
	html = response.content
	if type=='featured':
		html_blocks = re.findall('class="MainSlides(.*?)class="LinksList',html,re.DOTALL)
		block = html_blocks[0]
		z = re.findall('href="(.*?)" title="(.*?)".*?(src|data-image)="(.*?)"',block,re.DOTALL)
		if z:
			linkLIST,titleLIST,dummyLIST,imgLIST = zip(*z)
			items = zip(linkLIST,imgLIST,titleLIST)
		else: items = []
	else:
		if type=='filters': html_blocks = [html]
		elif type=='most': html_blocks = re.findall('class="SliderInSection(.*?)class="LinksList',html,re.DOTALL)
		else: html_blocks = re.findall('class="Blocks-UL"(.*?)class="AboElSeed"',html,re.DOTALL)
		block = html_blocks[0]
		#items = re.findall('href="(.*?)".*?data-image="(.*?)" alt="(.*?)"',block,re.DOTALL)
		items = re.findall('href="(.*?)".*?src="(.*?)" alt="(.*?)"',block,re.DOTALL)
	allTitles = []
	for link,img,title in items:
		#DIALOG_OK(title,'')
		title = unescapeHTML(title)
		if 'الحلقة' in title:
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = '_MOD_' + episode[0]
				if title not in allTitles:
					allTitles.append(title)
					addMenuItem('folder',menu_name+title,link,253,img)
			else: addMenuItem('video',menu_name+title,link,252,img)
		elif '/selary/' in link or 'مسلسل' in title:
			addMenuItem('folder',menu_name+title,link,253,img)
		else: addMenuItem('video',menu_name+title,link,252,img)
	if type not in ['featured','most']:
		items = re.findall('page-numbers" href="(.*?)">(.*?)<',html,re.DOTALL)
		for link,title in items:
			link = website0a+link
			link = unescapeHTML(link)
			title = unescapeHTML(title)
			addMenuItem('folder',menu_name+'صفحة '+title,link,251,'','',type)
	return

def EPISODES(url):
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','ARABSEED-EPISODES-1st')
	html = response.content
	name = re.findall('class="Title">(.*?)<',html,re.DOTALL)
	if 'الحلقة' in name[0]: name = name[0].split('الحلقة')[0].strip(' ')
	elif 'حلقة' in name[0]: name = name[0].split('حلقة')[0].strip(' ')
	else: name = name[0]
	html_blocks = re.findall('class="EpisodesArea"(.*?)style="clear: both;"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?<em>(.*?)<',block,re.DOTALL)
		for link,episode in reversed(items):
			title = name+' - الحلقة رقم '+episode
			addMenuItem('video',menu_name+title,link,252)
	else: addMenuItem('video',menu_name+'ملف التشغيل',url,252)
	return

def PLAY(url):
	watchURL = url+'watch/'
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',watchURL,'','','','','ARABSEED-PLAY-1st')
	html = response.content
	linkLIST = []
	html_blocks = re.findall('class="fal fa-play"(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<span>(.*?)<.*?src="(.*?)"',block,re.DOTALL|re.IGNORECASE)
		for title,link in items:
			link = unquote(link)
			if 'http' not in link: link = 'http:'+link
			quality = re.findall('\d\d\d+',title,re.DOTALL)
			if quality:
				quality = quality[0]
				if quality in title:
					title = title.replace(quality+'p','').replace(quality,'')
					title = title.replace('- ','').strip(' ')
				quality = '____'+quality
			else: quality = ''
			title = CLEAN_STREAM_NAME(title,link)
			link = link+'?named='+title+'__watch'+quality
			linkLIST.append(link)
	downloadURL = url+'download/'
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',downloadURL,'','','','','ARABSEED-PLAY-2nd')
	html = response.content
	html_blocks = re.findall('class="DownloadArea"(.*?)class="LinksList"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?<span>(.*?)<.*?<p>(.*?)<',block,re.DOTALL)
		for link,title,quality in items:
			link = unquote(link)
			title = CLEAN_STREAM_NAME(title,link)
			link = link+'?named='+title+'__download____'+quality
			linkLIST.append(link)
	#selection = DIALOG_SELECT('أختر البحث المناسب', linkLIST)
	linksTEXT = str(linkLIST)
	#LOG_THIS('',linksTEXT)
	notvideosLIST = ['.zip?','.rar?','.txt?','.pdf?','.tar?','.iso?','.zip.','.rar.','.txt.','.pdf.','.tar.','.iso.']
	if len(linkLIST)==0 or any(value in linksTEXT for value in notvideosLIST):
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
	url = website0a+'/find/?find='+search
	TITLES(url,'search')
	return

def FILTERS_MENU(url,filter):
	#DIALOG_OK(filter,url)
	headers2 = {'Referer':url,'User-Agent':''}
	headers2 = ''
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
		addMenuItem('folder',menu_name+'أظهار قائمة الفيديو التي تم اختيارها ',url4,251,'','','filters')
		addMenuItem('folder',menu_name+' [[   '+filter_show+'   ]]',url4,251,'','','filters')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'POST',url,'',headers2,'','','ARABSEED-FILTERS_MENU-1st')
	html = response.content
	html_blocks = re.findall('class="TaxPageFilter"(.*?)class="TermBTNs"',html,re.DOTALL)
	block = html_blocks[0]
	select_blocks1 = re.findall('class="TaxPageFilterItem".*?<em>(.*?)</em>.*?data-tax="(.*?)"(.*?)</ul></div></div>',block+'</ul></div></div>',re.DOTALL)
	select_blocks2 = re.findall('class="RatingFilter".*?<h4>(.*?)</h4>.*?(<ul>)(.*?)</ul>',block,re.DOTALL)
	select_blocks = select_blocks1+select_blocks2
	dict = {}
	for name,category2,block in select_blocks:
		#if 'interest' in category2: continue
		items = re.findall('data-name="(.*?)".*?data-tax="(.*?)".*?data-term="(.*?)"',block,re.DOTALL)
		if name=='اخرى': name = 'الاقسام'
		if not items:
			items2 = re.findall('data-rate="(.*?)".*?<em>(.*?)</em>',block,re.DOTALL)
			items = []
			for option,value in items2: items.append([option,'',value])
			category2 = 'rate'
			name = 'التقييم'
		else: category2 = items[0][1]
		if '==' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==all_categories_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES___'+new_filter)
				return
			else:
				url4 = PREPARE_FILTER_FINAL_URL(url2)
				if category2==all_categories_list[-1]: addMenuItem('folder',menu_name+'الجميع ',url4,251,'','','filters')
				else: addMenuItem('folder',menu_name+'الجميع ',url2,254,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&&'+category2+'==0'
			new_values = filter_values+'&&'+category2+'==0'
			new_filter = new_options+'___'+new_values
			addMenuItem('folder',menu_name+'الجميع :'+name,url2,255,'','',new_filter+'_FORGETRESULTS_')
		dict[category2] = {}
		for option,dummy,value in items:
			if option in ignoreLIST: continue
			if 'الكل' in option: continue
			#if 'http' in option: continue
			#if 'n-a' in value: continue
			title1,title2 = option,option
			title2 = name+': '+title1
			dict[category2][value] = title2
			new_options = filter_options+'&&'+category2+'=='+title1
			new_values = filter_values+'&&'+category2+'=='+value
			new_filter2 = new_options+'___'+new_values
			if type=='FILTERS':
				addMenuItem('folder',menu_name+title2,url,255,'','',new_filter2+'_FORGETRESULTS_')
			elif type=='CATEGORIES' and all_categories_list[-2]+'==' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'modified_filters')
				#DIALOG_OK(clean_filter,new_values)
				url3 = url+'//getposts??'+clean_filter
				url4 = PREPARE_FILTER_FINAL_URL(url3)
				addMenuItem('folder',menu_name+title2,url4,251,'','','filters')
			else: addMenuItem('folder',menu_name+title2,url,254,'','',new_filter2)
	return

all_categories_list = ['category','country','release-year']
all_filters_list = ['category','country','genre','release-year','language','quality','rate']

def PREPARE_FILTER_FINAL_URL(url):
	ajaxlink = '/wp-content/themes/Elshaikh2021/Ajaxat/Home/FilteringHome.php'
	url = url.replace('//getposts',ajaxlink)
	url = url.replace('/category/اخرى','')
	if ajaxlink not in url: url = url+ajaxlink
	url = url.replace('release-year','year')
	url = url.replace('??','?')
	url = url.replace('&&','&')
	url = url.replace('==','=')
	#DIALOG_OK('','PREPARE_FILTER_FINAL_URL')
	return url

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





