# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='SHAHID4U'
headers = { 'User-Agent' : '' }
menu_name='_SHA_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,text):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if mode==110: MENU()
	elif mode==111: TITLES(url)
	elif mode==112: PLAY(url)
	elif mode==113: EPISODES(url)
	elif mode==114: FILTERS_MENU(url,'FILTERS::'+text)
	elif mode==115: FILTERS_MENU(url,'CATEGORIES::'+text)
	elif mode==119: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',119)
	addDir(menu_name+'فلتر محدد',website0a,115)
	addDir(menu_name+'فلتر كامل',website0a,114)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	#addDir(menu_name+'فلتر','',114,website0a)
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','SHAHID4U-MENU-1st')
	html_blocks = re.findall('categories-tabs(.*?)advanced-search',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('data-get="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	for link,title in items:
		url = website0a+'/getposts?type=one&data='+link
		addDir(menu_name+title,url,111)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	html_blocks = re.findall('navigation-menu(.*?)div',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(\/.*?)">(.*?)<',block,re.DOTALL)
	ignoreLIST = ['مسلسلات انمي','الرئيسية','عروض مصارعة']
	#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
	for link,title in items:
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
		#	if any(value in title for value in keepLIST):
			addDir(menu_name+title,website0a+link,111)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url):
	#xbmcgui.Dialog().ok(url,url)
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','SHAHID4U-TITLES-1st')
	if 'getposts' in url: block = html
	else:
		html_blocks = re.findall('page-content(.*?)tags-cloud',html,re.DOTALL)
		block = html_blocks[0]
	items = re.findall('class="box.*?src="(.*?)".*?href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	allTitles = []
	itemLIST = ['مشاهدة','فيلم','اغنية','كليب','اعلان','هداف','مباراة','عرض','مهرجان','البوم']
	for img,link,title in items:
		if '/series/' in link: continue
		link = unquote(link).strip('/')
		title = unescapeHTML(title)
		title = title.strip(' ')
		if '/film/' in link or any(value in title for value in itemLIST):
			addLink(menu_name+title,link,112,img)
		elif '/episode/' in link and 'الحلقة' in title:
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = '_MOD_' + episode[0]
				if title not in allTitles:
					addDir(menu_name+title,link,113,img)
					allTitles.append(title)
		else: addDir(menu_name+title,link,113,img)
	html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<a href=["\'](http.*?)["\'].*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = unescapeHTML(link)
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			if title!='': addDir(menu_name+'صفحة '+title,link,111)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def EPISODES(url):
	episodesCount,items,itemsNEW = -1,[],[]
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','SHAHID4U-EPISODES-1st')
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
			if '/season/' in link: addDir(menu_name+title,link,113)
	else:
		for link,title,sequence in items:
			if '/season/' not in link: addLink(menu_name+title,link,112)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	linkLIST = []
	parts = url.split('/')
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','SHAHID4U-PLAY-1st')
	id = re.findall('postId:"(.*?)"',html,re.DOTALL)
	if not id: id = re.findall('post_id=(.*?)"',html,re.DOTALL)
	id = id[0]
	if '/post/' in url and 'seed' in url: url = website0a+'/watch/'+id
	if '/watch/' in html:
		url2 = url.replace(parts[3],'watch')
		html2 = openURL_cached(REGULAR_CACHE,url2,'',headers,'','SHAHID4U-PLAY-2nd')
		items1 = re.findall('data-embedd="(.*?)".*?alt="(.*?)"',html2,re.DOTALL)
		items2 = re.findall('data-embedd=".*?(http.*?)("|&quot;)',html2,re.DOTALL)
		items3 = re.findall('src=&quot;(.*?)&quot;.*?>(.*?)<',html2,re.DOTALL|re.IGNORECASE)
		items4 = re.findall('data-embedd="(.*?)".*?server_image">\n(.*?)\n',html2,re.DOTALL)
		items = items1+items2+items3+items4
		for server,title in items:
			if '.png' in server: continue
			if '.jpg' in server: continue
			if server.isdigit():
				link = website0a+'/?postid='+id+'&serverid='+server+'?name='+title+'__watch'
			else: 
				if 'http' not in server: server = 'http:'+server
				link = server+'?name=__watch'
			linkLIST.append(link)
		#xbmcgui.Dialog().ok('watch 1',	str(len(items)))
	if '/download/' in html:
		headers2 = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
		url2 = website0a + '/ajaxCenter?_action=getdownloadlinks&postId='+id
		html2 = openURL_cached(REGULAR_CACHE,url2,'',headers2,'','SHAHID4U-PLAY-4th')
		if 'download-btns' in html2:
			items3 = re.findall('href="(.*?)"',html2,re.DOTALL)
			for url3 in items3:
				if '/page/' in url3:
					resolution4 = ''
					html4 = openURL_cached(REGULAR_CACHE,url3,'',headers,'','SHAHID4U-PLAY-5th')
					items4 = re.findall('<strong>(.*?)</strong>(.*?)-----',html4,re.DOTALL)
					for server4,temp4 in items4:
						if '<strong>' in temp4:
							resolution4 = server4
							server4 = re.findall('<strong>(.*?)</strong>',temp4,re.DOTALL)
							server4 = server4[0]
						items5 = re.findall('href="(.*?)"',temp4,re.DOTALL)
						for link5 in items5:
							link5 = link5+'?name='+server4+'__download____'+resolution4
							linkLIST.append(link5)
				elif 'http' in url3:
					url3 = url3+'?name=__download'
					linkLIST.append(url3)
			#xbmcgui.Dialog().ok('download 1',	str(len(linkLIST))	)
		elif 'slow-motion' in html2:
			if '</table>' in html2:
				blocks_upper = re.findall('class=(.*?)</table>',html2,re.DOTALL)
				blocks_lower = re.findall('</table>(.*?)</div>',html2,re.DOTALL)
			else:
				blocks_upper = []
				blocks_lower = re.findall('class=(.*?)</div>',html2,re.DOTALL)
			for block in blocks_upper:
				items = re.findall('slow-motion">(.*?)<',block,re.DOTALL)
				if not items: resolution = ''
				else: resolution = items[-1]
				items = re.findall('<td>(.*?)</td>.*?href="(.*?)"',block,re.DOTALL)
				for server,link in items:
					link = link+'?name='+server+'__download____'+resolution
					linkLIST.append(link)
			for block in blocks_lower:
				items = re.findall('slow-motion">(.*?)<',block,re.DOTALL)
				if not items: resolution = ''
				else: resolution = items[-1]
				items = re.findall('href="(.*?)".*?name">(.*?)<',block,re.DOTALL)
				for link,server in items:
					link = link.strip(' ')
					link = link+'?name='+server+'__download____'+resolution
					linkLIST.append(link)
	#xbmcgui.Dialog().ok('both: watch & download',	str(len(linkLIST))	)
	#selection = xbmcgui.Dialog().select('أختر البحث المناسب', linkLIST)
	if len(linkLIST)==0: xbmcgui.Dialog().ok('','الرابط ليس فيه فيديو')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name)
	return

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','+')
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','SHAHID4U-SEARCH-1st')
	html_blocks = re.findall('chevron-select(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('value="(.*?)".*?>(.*?)<',block,re.DOTALL)
		categoryLIST,filterLIST = [],[]
		for category,title in items:
			if title in ['عروض مصارعة']: continue
			categoryLIST.append(category)
			filterLIST.append(title)
		selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', filterLIST)
		if selection == -1 : return
		category = categoryLIST[selection]
	else: category = ''
	url = website0a + '/search?s='+search+'&category='+category
	TITLES(url)
	return

def FILTERS_MENU(url,filter):
	#xbmcgui.Dialog().ok(filter,url)
	menu_list = ['category','genre','release-year']
	if '?' in url: url = url.split('/getposts?')[0]
	type,filter = filter.split('::',1)
	if filter=='': filter_options,filter_values = '',''
	else: filter_options,filter_values = filter.split('::')
	if type=='CATEGORIES':
		if menu_list[0]+'=' not in filter_options: category = menu_list[0]
		for i in range(len(menu_list[0:-1])):
			if menu_list[i]+'=' in filter_options: category = menu_list[i+1]
		new_options = filter_options+'&'+category+'=0'
		new_values = filter_values+'&'+category+'=0'
		new_filter = new_options.strip('&')+'::'+new_values.strip('&')
		clean_filter = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		url2 = url+'/getposts?'+clean_filter
	elif type=='FILTERS':
		filter_show = RECONSTRUCT_FILTER(filter_options,'modified_values')
		filter_show = unquote(filter_show)
		if filter_values!='': filter_values = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		if filter_values=='': url2 = url
		else: url2 = url+'/getposts?'+filter_values
		addDir(menu_name+'أظهار قائمة الفيديو التي تم اختيارها ',url2,111)
		addDir(menu_name+' [[   '+filter_show+'   ]]',url2,111)
		addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	html = openURL_cached(LONG_CACHE,url,'',headers,'','SHAHID4U-FILTERS_MENU-1st')
	html_blocks = re.findall('<form class(.*?)</form>',html,re.DOTALL)
	block = html_blocks[0]
	select_blocks = re.findall('select.*?<a.*?>(.*?)</a>.*?data-tax="(.*?)"(.*?)</ul>',block,re.DOTALL)
	#xbmcgui.Dialog().ok('',str(select_blocks))
	dict = {}
	ignoreLIST = ['عروض مصارعة','الكل']
	for name,category2,block in select_blocks:
		name = name.replace('--','')
		items = re.findall('data-cat="(.*?)".*?checkmark-bold">(.*?)<',block,re.DOTALL)
		if '=' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==menu_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES::'+new_filter)
				return
			else:
				if category2==menu_list[-1]: addDir(menu_name+'الجميع ',url2,111)
				else: addDir(menu_name+'الجميع ',url2,115,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&'+category2+'=0'
			new_values = filter_values+'&'+category2+'=0'
			new_filter = new_options+'::'+new_values
			addDir(menu_name+'الجميع :'+name,url2,114,'','',new_filter)
		dict[category2] = {}
		for value,option in items:
			if option in ignoreLIST: continue
			#if 'value' not in value: value = option
			#else: value = re.findall('"(.*?)"',value,re.DOTALL)[0]
			dict[category2][value] = option
			new_options = filter_options+'&'+category2+'='+option
			new_values = filter_values+'&'+category2+'='+value
			new_filter2 = new_options+'::'+new_values
			title = option+' :'#+dict[category2]['0']
			title = option+' :'+name
			if type=='FILTERS': addDir(menu_name+title,url,114,'','',new_filter2)
			elif type=='CATEGORIES' and menu_list[-2]+'=' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'modified_filters')
				url3 = url+'/getposts?'+clean_filter
				addDir(menu_name+title,url3,111)
			else: addDir(menu_name+title,url,115,'','',new_filter2)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def RECONSTRUCT_FILTER(filters,mode):
	#xbmcgui.Dialog().ok(filters,'RECONSTRUCT_FILTER 11')
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
	url_filter_list = ['quality','release-year','genre','category']
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
	#xbmcgui.Dialog().ok(filters,'RECONSTRUCT_FILTER 22')
	return new_filters

