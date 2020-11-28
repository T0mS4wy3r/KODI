# -*- coding: utf-8 -*-
from LIBRARY import *

headers = { 'User-Agent' : '' }
script_name='AKOAMCAM'
menu_name='_AKC_'
website0a = WEBSITES[script_name][0]
#noEpisodesLIST = ['فيلم','كليب','العرض الاسبوعي','مسرحية','مسرحيه','اغنية','اعلان','لقاء']
#proxy = '||MyProxyUrl=https://159.203.87.130:3128'
#proxy = '||MyProxyUrl='+PROXIES[6][1]

#ignoreLIST = ['برامج','ألعاب','المصارعة الحرة','الأجهزة اللوحية','الكورسات التعليمية','برامج التصميم','العاب قتال','العاب الكمبيوتر PC','البرامج']
ignoreLIST = ['مصارعة']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==350: results = MENU(url)
	elif mode==351: results = TITLES(url,text)
	elif mode==352: results = EPISODES(url)
	elif mode==353: results = PLAY(url)
	elif mode==354: results = FILTERS_MENU(url,'FILTERS___'+text)
	elif mode==355: results = FILTERS_MENU(url,'CATEGORIES___'+text)
	elif mode==356: results = FILTERS_DEFINED(url)
	elif mode==357: results = FILTERS_FULL(url)
	elif mode==359: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	addMenuItem('folder',menu_name+'بحث في الموقع','',359,'','','_REMEMBERRESULTS_')
	if website=='': addMenuItem('folder',website+'___'+menu_name+'فلتر محدد',website0a,356)
	if website=='': addMenuItem('folder',website+'___'+menu_name+'فلتر كامل',website0a,357)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#addMenuItem('folder',website+'___'+menu_name+'المزيد',website0a,352,'','','more')
	#addMenuItem('folder',website+'___'+menu_name+'الاخبار',website0a,352,'','','news')
	html = OPENURL_CACHED(REGULAR_CACHE,website0a,'',headers,'','AKOAMCAM-MENU-1st')
	url2 = re.findall('recently-container.*?href="(.*?)"',html,re.DOTALL)
	if url2: url2 = url2[0]
	else: url2 = website0a
	addMenuItem('folder',website+'___'+menu_name+'اضيف حديثا',url2,351)
	url2 = re.findall('@id":"(.*?)"',html,re.DOTALL)
	if url2: url2 = url2[0]
	else: url2 = website0a
	addMenuItem('folder',website+'___'+menu_name+'المميزة',url2,351,'','','featured')
	html_blocks = re.findall('main-categories-list(.*?)main-categories-list',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?class="font.*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title not in ignoreLIST: addMenuItem('folder',menu_name+title,link,351)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks = re.findall('class="categories-box(.*?)<footer',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?">(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = unescapeHTML(link)
			if title not in ignoreLIST: addMenuItem('folder',menu_name+title,link,351)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def FILTERS_DEFINED(website=''):
	html = OPENURL_CACHED(LONG_CACHE,website0a,'',headers,'','AKOAMCAM-MENU-1st')
	html_blocks = re.findall('class="menu(.*?)<nav',html,re.DOTALL)
	#DIALOG_OK(link,html_blocks][0])
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?text">(.*?)<',block,re.DOTALL)
		for link,title in items:
			#DIALOG_OK(link,title)
			if title not in ignoreLIST:
				title = title+' مصنفة'
				addMenuItem('folder',menu_name+title,link,355)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def FILTERS_FULL(website=''):
	html = OPENURL_CACHED(LONG_CACHE,website0a,'',headers,'','AKOAMCAM-MENU-1st')
	html_blocks = re.findall('class="menu(.*?)<nav',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?text">(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title not in ignoreLIST:
				title = title+' مفلترة'
				addMenuItem('folder',menu_name+title,link,354)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def TITLES(url,type=''):
	#DIALOG_OK(url,type)
	html = OPENURL_CACHED(NO_CACHE,url,'',headers,True,'AKOAMCAM-TITLES-1st')
	if type=='featured': html_blocks = re.findall('swiper-container(.*?)swiper-button-prev',html,re.DOTALL)
	else: html_blocks = re.findall('class="container"(.*?)main-footer',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('xlink:href="(.*?)".*?href="(.*?)".*?text-white">(.*?)<',block,re.DOTALL)
		#DIALOG_OK(str(len(block)),url)
		allTitles = []
		for img,link,title in items:
			title = unescapeHTML(title)
			if 'الحلقة' in title or 'الحلقه' in title:
				episode = re.findall('(.*?) (الحلقة|الحلقه) \d+',title,re.DOTALL)
				if episode:
					title = '_MOD_' + episode[0][0]
					if title not in allTitles:
						addMenuItem('folder',menu_name+title,link,352,img)
						allTitles.append(title)
			elif 'مسلسل' in title:
				addMenuItem('folder',menu_name+title,link,352,img)
			else: addMenuItem('video',menu_name+title,link,353,img)
			#if '/series/' in link or '/shows/' in link:
			#	addMenuItem('folder',menu_name+title,link,352,img)
			#elif '/programs/' not in link and '/games/' not in link:
	html_blocks = re.findall('pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href=["\'](.*?)["\'].*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			#if '&lsaquo;' in title: title = 'صفحة سابقة'
			#if '&rsaquo;' in title: title = 'صفحة لاحقة'
			#if '&laquo' in title: title = 'الصفحة التالية'
			#if 'صفحة' not in title: title = 'صفحة '+title
			link = unescapeHTML(link)
			title = unescapeHTML(title)
			addMenuItem('folder',menu_name+title,link,351)
	return

def SEARCH(search):
	# https://akwam.net/search?q=%D8%A8%D8%AD%D8%AB
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	new_search = search.replace(' ','+')
	url = website0a + '/?s='+new_search
	#DIALOG_OK(url,'SEARCH_AKOAM')
	results = TITLES(url)
	return

def EPISODES(url):
	#DIALOG_OK(url,'EPISODES_AKWAM')
	html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,True,'AKOAMCAM-EPISODES-1st')
	#if '-episodes' not in html:
	#	img = xbmc.getInfoLabel('ListItem.Icon')
	#	addMenuItem('video',menu_name+'رابط التشغيل',url,353,img)
	#else:
	html_blocks = re.findall('text-white">الحلقات(.*?)<header',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		episodes = re.findall('href="(http.*?)".*?src="(.*?)".*?alt="(.*?)"',block,re.DOTALL)
		for link,img,title in episodes:
			if 'الحلقة' in title or 'الحلقه' in title: addMenuItem('video',menu_name+title,link,353,img)
			#else: addMenuItem('folder',menu_name+title,link,352,img)
	else:
		img = xbmc.getInfoLabel('ListItem.Icon')
		if html.count('<title>')>1: title = re.findall('<title>(.*?)<',html,re.DOTALL)[1]
		else: title = 'رابط التشغيل'
		addMenuItem('video',menu_name+title,url,353,img)
	return

def PLAY(url):
	linkLIST,titleLIST = [],[]
	responce = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'','','','','AKOAMCAM-PLAY-1st')
	html = responce.content
	postid = re.findall('post_id=(.*?)"',html,re.DOTALL)
	if postid:
		postid = postid[0]
		headers = {'User-Agent':'','Content-Type':'application/x-www-form-urlencoded'}
		data = {'post_id':postid}
		url2 = website0a+'/wp-content/themes/aflam8kkk/Inc/Ajax/Single/Watch.php'
		responce2 = OPENURL_REQUESTS_CACHED(LONG_CACHE,'POST',url2,data,headers,'','','AKOAMCAM-PLAY-1st')
		html2 = responce2.content
		items = re.findall('data-server="(.*?)".*?class="text">(.*?)<',html2,re.DOTALL)
		for serverid,name in items:
			#data = {'post_id':postid,'server':serverid}
			link = 'https://w.akoam.cam/wp-content/themes/aflam8kkk/Inc/Ajax/Single/Server.php'
			link = link+'?postid='+postid+'&serverid='+serverid+'?named='+name+'__watch'
			linkLIST.append(link)
			titleLIST.append(name)
		url2 = website0a+'/wp-content/themes/aflam8kkk/Inc/Ajax/Single/Download.php'
		responce2 = OPENURL_REQUESTS_CACHED(LONG_CACHE,'POST',url2,data,headers,'','','AKOAMCAM-PLAY-1st')
		html2 = responce2.content
		items = re.findall('href="(.*?)".*?class="text">(.*?)<',html2,re.DOTALL)
		for link,title in items:
			#DIALOG_OK(link,title)
			link = link.strip(' ')
			link = link+'?named='+title+'__download'
			linkLIST.append(link)
			titleLIST.append(title)
	#DIALOG_SELECT('',linkLIST)
	if len(linkLIST)==0:
		DIALOG_OK('رسالة من المبرمج','الرابط ليس فيه فيديو')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name,'video')
	return

def FILTERS_MENU(url,filter):
	filter = filter.replace('_FORGETRESULTS_','')
	#DIALOG_OK(filter,url)
	menu_list = ['cat','genre','release-year','quality','orderby']
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
		addMenuItem('folder',menu_name+'أظهار قائمة الفيديو التي تم اختيارها',url2,351,'','1')
		addMenuItem('folder',menu_name+' [[   '+filter_show+'   ]]',url2,351,'','1')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = OPENURL_CACHED(LONG_CACHE,url,'',headers,True,'AKOAMCAM-FILTERS_MENU-1st')
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
				if category2==menu_list[-1]: addMenuItem('folder',menu_name+'الجميع',url2,351,'','1')
				else: addMenuItem('folder',menu_name+'الجميع',url2,355,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&'+category2+'=0'
			new_values = filter_values+'&'+category2+'=0'
			new_filter = new_options+'___'+new_values
			addMenuItem('folder',menu_name+'الجميع : '+name,url2,354,'','',new_filter+'_FORGETRESULTS_')
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
			if type=='FILTERS': addMenuItem('folder',menu_name+title,url,354,'','',new_filter2+'_FORGETRESULTS_')
			elif type=='CATEGORIES' and menu_list[-2]+'=' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'all')
				url3 = url+'?'+clean_filter
				addMenuItem('folder',menu_name+title,url3,351,'','1')
			else: addMenuItem('folder',menu_name+title,url,355,'','',new_filter2)
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
	url_filter_list = ['cat','genre','release-year','quality','orderby']
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



