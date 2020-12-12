# -*- coding: utf-8 -*-
from LIBRARY import *

headers = { 'User-Agent' : '' }
script_name='AKWAM'
menu_name='_AKW_'
website0a = WEBSITES[script_name][0]
#noEpisodesLIST = ['فيلم','كليب','العرض الاسبوعي','مسرحية','مسرحيه','اغنية','اعلان','لقاء']
#proxy = '||MyProxyUrl=https://159.203.87.130:3128'
#proxy = '||MyProxyUrl='+PROXIES[6][1]
proxy = ''
ignoreLIST = ['برامج','ألعاب','المصارعة الحرة','الأجهزة اللوحية','الكورسات التعليمية','برامج التصميم','العاب قتال','العاب الكمبيوتر PC','البرامج','قيامة عثمان','الألعاب','الموقع القديم','اضيف حديثاً']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==240: results = MENU(url)
	elif mode==241: results = TITLES(url,text)
	elif mode==242: results = EPISODES(url)
	elif mode==243: results = PLAY(url)
	elif mode==244: results = FILTERS_MENU(url,'FILTERS___'+text)
	elif mode==245: results = FILTERS_MENU(url,'CATEGORIES___'+text)
	elif mode==246: results = FILTERS_DEFINED(url)
	elif mode==247: results = FILTERS_FULL(url)
	elif mode==249: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	addMenuItem('folder',menu_name+'بحث في الموقع','',249,'','','_REMEMBERRESULTS_')
	if website=='': addMenuItem('folder',website+'___'+menu_name+'فلتر محدد',website0a,246)
	if website=='': addMenuItem('folder',website+'___'+menu_name+'فلتر كامل',website0a,247)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#addMenuItem('folder',website+'___'+menu_name+'المزيد',website0a,242,'','','more')
	#addMenuItem('folder',website+'___'+menu_name+'الاخبار',website0a,242,'','','news')
	html = OPENURL_CACHED(REGULAR_CACHE,website0a,'',headers,'','AKWAM-MENU-1st')
	url2 = re.findall('recently-container.*?href="(.*?)"',html,re.DOTALL)
	if url2: url2 = url2[0]
	else: url2 = website0a
	addMenuItem('folder',website+'___'+menu_name+'اضيف حديثا',url2,241)
	url2 = re.findall('@id":"(.*?)"',html,re.DOTALL)
	if url2: url2 = url2[0]
	else: url2 = website0a
	addMenuItem('folder',website+'___'+menu_name+'المميزة',url2,241,'','','featured')
	html_blocks = re.findall('main-categories-list(.*?)main-categories-list',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?class="font.*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title not in ignoreLIST: addMenuItem('folder',menu_name+title,link,241)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks = re.findall('class="categories-box(.*?)<footer',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?">(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = unescapeHTML(link)
			if title not in ignoreLIST: addMenuItem('folder',menu_name+title,link,241)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def FILTERS_DEFINED(website=''):
	html = OPENURL_CACHED(LONG_CACHE,website0a,'',headers,'','AKWAM-MENU-1st')
	html_blocks = re.findall('class="menu(.*?)<nav',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?text">(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title not in ignoreLIST:
				title = title+' مصنفة'
				addMenuItem('folder',menu_name+title,link,245)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def FILTERS_FULL(website=''):
	html = OPENURL_CACHED(LONG_CACHE,website0a,'',headers,'','AKWAM-MENU-1st')
	html_blocks = re.findall('class="menu(.*?)<nav',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?text">(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title not in ignoreLIST:
				title = title+' مفلترة'
				addMenuItem('folder',menu_name+title,link,244)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def TITLES(url,type=''):
	#DIALOG_OK(url,type)
	html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,True,'AKWAM-TITLES-1st')
	if type=='featured': html_blocks = re.findall('swiper-container(.*?)swiper-button-prev',html,re.DOTALL)
	else: html_blocks = re.findall('class="widget"(.*?)main-footer',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('img src="(.*?)" class.*?href="(.*?)".*?text-white">(.*?)<',block,re.DOTALL)
		for img,link,title in items:
			if 'data-src' in img: img = img.split('data-src="')[1]
			if '/series/' in link or '/shows/' in link:
				addMenuItem('folder',menu_name+title,link,242,img)
			elif '/programs/' not in link and '/games/' not in link:
				addMenuItem('video',menu_name+title,link,243,img)
	html_blocks = re.findall('pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title=='&lsaquo;': title = 'سابقة'
			if title=='&rsaquo;': title = 'لاحقة'
			link = unescapeHTML(link)
			addMenuItem('folder',menu_name+'صفحة '+title,link,241)
	return

def SEARCH(search):
	# https://akwam.net/search?q=%D8%A8%D8%AD%D8%AB
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	new_search = search.replace(' ','%20')
	url = website0a + '/search?q='+new_search
	#DIALOG_OK(url,'SEARCH_AKOAM')
	results = TITLES(url)
	return

def EPISODES(url):
	#DIALOG_OK(url,'EPISODES_AKWAM')
	html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,True,'AKWAM-EPISODES-1st')
	if '-episodes' not in html:
		img = xbmc.getInfoLabel('ListItem.Icon')
		addMenuItem('video',menu_name+'رابط التشغيل',url,243,img)
	else:
		html_blocks = re.findall('-episodes">(.*?)col-lg-8',html,re.DOTALL)
		block = html_blocks[0]
		episodes = re.findall('href="(http.*?)".*?>(.*?)<.*?src="(.*?)"',block,re.DOTALL)
		for link,title,img in episodes:
			if 'الحلقات' in title or 'مواسم اخرى' in title: continue
			if '/series/' in link: addMenuItem('folder',menu_name+title,link,242,img)
			else: addMenuItem('video',menu_name+title,link,243,img)
	return

def PLAY(url):
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	#with open('S:\\emad.html', 'w') as f: f.write(html)
	html = OPENURL_CACHED(LONG_CACHE,url,'',headers,True,'AKWAM-PLAY-1st')
	ratingLIST = re.findall('class="badge.*?>.*?(\w*).*?<',html,re.DOTALL)
	if RATING_CHECK(script_name,url,ratingLIST): return
	buttons = re.findall('li><a href="#(.*?)".*?>(.*?)<',html,re.DOTALL)
	#buttons = (['',''],['',''])
	linkLIST,titleLIST,blocks,qualities = [],[],[],[]
	if buttons:
		filetype = 'mp4'
		for button,quality in buttons:
			html_blocks = re.findall('tab-content quality" id="'+button+'".*?</div>.\s*</div>',html,re.DOTALL)
			block = html_blocks[0]
			blocks.append(block)
			qualities.append(quality)
	else:
		html_blocks = re.findall('class="qualities(.*?)<h3.*?>(.*?)<',html,re.DOTALL)
		block,filename = html_blocks[0]
		notvideosLIST = ['zip','rar','txt','pdf','htm','tar','iso','html']
		filetype = filename.rsplit('.',1)[1].strip(' ')
		if filetype in notvideosLIST:
			DIALOG_OK('رسالة من المبرمج','الملف ليس فيديو ولا صوت')
			return
		blocks.append(block)
		qualities.append('')
	for i in range(len(blocks)):
		links = re.findall('href="(.*?)".*?icon-(.*?)"',blocks[i],re.DOTALL)
		for link,icon in links:
			if 'torrent' in icon: continue
			#elif 'play' in icon: continue
			elif 'download' in icon: type = 'download'
			elif 'play' in icon: type = 'watch'
			else: type = 'unknown'
			#title = qualities[i]+' ملف '+type
			#titleLIST.append(title)
			link = link+'?named=__'+type+'____'+qualities[i]+'__akwam'
			linkLIST.append(link)
	#selection = DIALOG_SELECT('TEST',titleLIST)
	#selection = DIALOG_SELECT('TEST',linkLIST)
	import RESOLVERS
	RESOLVERS.PLAY(linkLIST,script_name,'video')
	return

def FILTERS_MENU(url,filter):
	filter = filter.replace('_FORGETRESULTS_','')
	#DIALOG_OK(filter,url)
	menu_list = ['section','rating','category','year']
	if '?' in url: url = url.split('?')[0]
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
		url2 = url+'?'+clean_filter
	elif type=='FILTERS':
		filter_show = RECONSTRUCT_FILTER(filter_options,'modified_values')
		filter_show = unquote(filter_show)
		if filter_values!='': filter_values = RECONSTRUCT_FILTER(filter_values,'all')
		if filter_values=='': url2 = url
		else: url2 = url+'?'+filter_values
		addMenuItem('folder',menu_name+'أظهار قائمة الفيديو التي تم اختيارها',url2,241,'','1')
		addMenuItem('folder',menu_name+' [[   '+filter_show+'   ]]',url2,241,'','1')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = OPENURL_CACHED(LONG_CACHE,url,'',headers,True,'AKWAM-FILTERS_MENU-1st')
	html_blocks = re.findall('<form id(.*?)</form>',html,re.DOTALL)
	block = html_blocks[0]
	select_blocks = re.findall('<select.*?name="(.*?)".*?">(.*?)<(.*?)</select>',block,re.DOTALL)
	#DIALOG_OK('',str(select_blocks))
	dict = {}
	for category2,name,block in select_blocks:
		#name = name.replace('--','')
		items = re.findall('<option(.*?)>(.*?)<',block,re.DOTALL)
		if '=' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==menu_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES___'+new_filter)
				return
			else:
				if category2==menu_list[-1]: addMenuItem('folder',menu_name+'الجميع',url2,241,'','1')
				else: addMenuItem('folder',menu_name+'الجميع',url2,245,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&'+category2+'=0'
			new_values = filter_values+'&'+category2+'=0'
			new_filter = new_options+'___'+new_values
			addMenuItem('folder',menu_name+'الجميع : '+name,url2,244,'','',new_filter+'_FORGETRESULTS_')
		dict[category2] = {}
		for value,option in items:
			if option in ignoreLIST: continue
			if 'value' not in value: value = option
			else: value = re.findall('"(.*?)"',value,re.DOTALL)[0]
			dict[category2][value] = option
			new_options = filter_options+'&'+category2+'='+option
			new_values = filter_values+'&'+category2+'='+value
			new_filter2 = new_options+'___'+new_values
			title = option+' : '#+dict[category2]['0']
			title = option+' : '+name
			if type=='FILTERS': addMenuItem('folder',menu_name+title,url,244,'','',new_filter2+'_FORGETRESULTS_')
			elif type=='CATEGORIES' and menu_list[-2]+'=' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'all')
				url3 = url+'?'+clean_filter
				addMenuItem('folder',menu_name+title,url3,241,'','1')
			else: addMenuItem('folder',menu_name+title,url,245,'','',new_filter2)
	return

def RECONSTRUCT_FILTER(filters,mode):
	#DIALOG_OK(filters,'RECONSTRUCT_FILTER 11')
	# mode=='modified_values'		only non empty values
	# mode=='modified_filters'		only non empty filters
	# mode=='all'					all filters (includes empty filter)
	#filters = filters.replace('=&','=0&')
	filters = filters.strip('&')
	filtersDICT = {}
	if '=' in filters:
		items = filters.split('&')
		for item in items:
			var,value = item.split('=')
			filtersDICT[var] = value
	new_filters = ''
	url_filter_list = ['section','category','rating','year','language','formats','quality']
	for key in url_filter_list:
		if key in filtersDICT.keys(): value = filtersDICT[key]
		else: value = '0'
		#if '%' not in value: value = quote(value)
		if mode=='modified_values' and value!='0': new_filters = new_filters+' + '+value
		elif mode=='modified_filters' and value!='0': new_filters = new_filters+'&'+key+'='+value
		elif mode=='all': new_filters = new_filters+'&'+key+'='+value
	new_filters = new_filters.strip(' + ')
	new_filters = new_filters.strip('&')
	#new_filters = new_filters.replace('=0','=')
	#DIALOG_OK(filters,'RECONSTRUCT_FILTER 22')
	return new_filters



