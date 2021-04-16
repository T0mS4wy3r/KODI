# -*- coding: utf-8 -*-
from LIBRARY import *

"""
website0a = 'https://egy4best.com'
website0a = 'https://egy1.best'
website0a = 'https://egybest1.com'
website0a = 'https://egybest.vip'
website0a = 'https://ww.egy.best'
website0a = 'https://movies.egybest.site'
website0a = 'https://series.egybest.tv'
website0a = 'https://back.egybest.co'
website0a = 'https://ww.egybest.blog'
website0a = 'https://near.egybest.me'
website0a = 'https://tool.egybest.ltd'
"""

script_name = 'EGYBEST'
menu_name='_EGB_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,page,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==120: results = MENU(url)
	elif mode==121: results = TITLES(url,page)
	elif mode==122: results = SUBMENU(url)
	elif mode==123: results = PLAY(url)
	elif mode==124: results = FILTERS_MENU(url,'CATEGORIES___'+text)
	elif mode==125: results = FILTERS_MENU(url,'FILTERS___'+text)
	elif mode==126: results = FILTERS_SUBMENU(text)
	elif mode==128: results = GET_USERNAME_PASSWORD()
	elif mode==129: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',129,'','','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'فلتر محدد',website0a,126,'','','CATEGORIES___')
		addMenuItem('folder',menu_name+'فلتر كامل',website0a,126,'','','FILTERS___')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a,'','','','','EGYBEST-MENU-1st')
	html = response.content
	html_blocks = re.findall('class="i i-home"(.*?)class="i-folder">',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)</a>',block,re.DOTALL)
	for link,title in items:
		if '</i>' in title: title = title.split('</i>')[1]
		addMenuItem('folder',website+'___'+menu_name+title,link,122)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks = re.findall('class="ba(.*?)<script',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('pda bdb"><strong>(.*?)<.*?href="(.*?)"',html,re.DOTALL)
	for title,link in items:
		addMenuItem('folder',website+'___'+menu_name+title,link,121)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	items = re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for link,title in items:
		if not link.endswith('/'): addMenuItem('folder',website+'___'+menu_name+title,link,121)
	return html

def SUBMENU(url):
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'','','','','EGYBEST-SUBMENU-1st')
	html = response.content
	html_blocks = re.findall('class="rs_scroll"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)".*?</i>(.*?)</a>',block,re.DOTALL)
	for link,title in items:
		addMenuItem('folder',menu_name+title,link,121)
	return

def TITLES(url,page='1'):
	if page=='': page = '1'
	if '/explore/' in url or '?' in url: url2 = url + '&'
	else: url2 = url + '?'
	url2 = url2 + 'output_format=json&output_mode=movies_list&page='+page
	html = OPENURL_CACHED(REGULAR_CACHE,url2,'','','','EGYBEST-TITLES-1st')
	name = ''
	if '/season/' in url:
		name = re.findall('<h1>(.*?)<',html,re.DOTALL)
		if name: name = escapeUNICODE(name[0]).strip(' ') + ' - '
		else: name = xbmc.getInfoLabel( "ListItem.Label" ) + ' - '
	items = re.findall('n<a href=\\\\"(.*?)\\\\".*?src=\\\\"(.*?)\\\\".*?title\\\\">(.*?)<',html,re.DOTALL)
	for link,img,title in items:
		if '/series/' in url and '/season\/' not in link: continue
		if '/season/' in url and '/episode\/' not in link: continue
		title = name+escapeUNICODE(title).strip(' ')
		link = link.replace('\/','/')
		img = img.replace('\/','/')
		if 'http' not in img: img = 'http:'+img
		url2 = website0a+link
		if '/movie/' in url2 or '/episode/' in url2 or '/masrahiyat/' in url:
			addMenuItem('video',menu_name+title,url2.rstrip('/'),123,img)
		else: addMenuItem('folder',menu_name+title,url2,121,img)
	if len(items)>=12:
		pagingLIST = ['/movies/','/tv/','/explore/','/trending/','/masrahiyat/']
		page = int(page)
		if any(value in url for value in pagingLIST):
			for n in range(0,1100,100):
				if int(page/100)*100==n:
					for i in range(n,n+100,10):
						if int(page/10)*10==i:
							for j in range(i,i+10,1):
								if not page==j and j!=0:
									addMenuItem('folder',menu_name+'صفحة '+str(j),url,121,'',str(j))
						elif i!=0: addMenuItem('folder',menu_name+'صفحة '+str(i),url,121,'',str(i))
						else: addMenuItem('folder',menu_name+'صفحة '+str(1),url,121,'',str(1))
				elif n!=0: addMenuItem('folder',menu_name+'صفحة '+str(n),url,121,'',str(n))
				else: addMenuItem('folder',menu_name+'صفحة '+str(1),url,121)
	return

def PLAY(url):
	# cache does not work after 3 minutes
	response = OPENURL_REQUESTS_CACHED(NO_CACHE,'GET',url,'','','','','EGYBEST-PLAY-1st')
	html = response.content
	ratingLIST = re.findall('<td>التصنيف</td>.*?">(.*?)<',html,re.DOTALL)
	if ratingLIST and RATING_CHECK(script_name,url,ratingLIST): return
	"""
	html_blocks = re.findall('tbody(.*?)tbody',html,re.DOTALL)
	if not html_blocks:
		DIALOG_NOTIFICATION('خطأ من الموقع الاصلي','ملف الفيديو غير متوفر')
		return
	block = html_blocks[0]
	"""
	# watchlink https://egybest.net/watch/?v=YhhheGZiZGdXVrehQhhheGlEhehQhefSKKWxMddedkiZfhKbfKheQeheCKduehQheDlOdpIdeKfDXRDqTVZfhhehYQehedSKhehQhedKYDSnEVdhdZWGheQeheZvoYdSlZWehQDnYDnhDQDmCdDfQQeheKSNehQhesdSKGflpNohdpodZpKheQehedSchehQheDnlehfnhQrfhhfnhDhhehY&h=5de8bb072d336de05092297ec8b61643
	# embeded https://vidstream.top/embed/o2RbrN9bqf/?vclid=44711370a2655b3f2d23487cb74c05e5347648e8bb9571dfa7c5d5e4zlllsCGMDslElsMaYXobviuROhYfamfMOhlsEslsWQUlslElsMOcSbzMykqapaqlsEslsxMcGlslElsOGsabiZusOxySMgOpEaucSxiSVGEBOlOouQzsEslsxWdlslElsmmmlRPMMslnfpaqlsEslsCMcGlslElsOEOEEZlEMOuzslh
	titleLIST,linkLIST = [],[]
	watchlink = re.findall('class="auto-size" src="(.*?)"',html,re.DOTALL)
	if watchlink:
		server = SERVER(url)
		watchlink = server+watchlink[0]		#+'||MyProxyUrl=http://79.165.242.84:4145'
		response = OPENURL_REQUESTS_CACHED(NO_CACHE,'GET',watchlink,'','','','','EGYBEST-PLAY-2nd')
		html2 = response.content
		#WRITE_THIS(html2)
		if 'dostream' not in html2:
			result = VidStream(html2)
			#DIALOG_TEXTVIEWER_FULLSCREEN(str(result),str(html2))
			adlink,verifylink,verifydata = result
			verifylink = server+verifylink
			adlink = server+adlink
			cookies = response.cookies.get_dict()
			PSSID = cookies['PSSID']
			headers = {'Cookie':'PSSID='+PSSID}
			response = OPENURL_REQUESTS_CACHED(NO_CACHE,'GET',adlink,'',headers,'','','EGYBEST-PLAY-3rd')
			response = OPENURL_REQUESTS_CACHED(NO_CACHE,'POST',verifylink,verifydata,headers,'','','EGYBEST-PLAY-4th')
			response = OPENURL_REQUESTS_CACHED(NO_CACHE,'GET',watchlink,'',headers,'','','EGYBEST-PLAY-5th')
			html2 = response.content
		m3u8 = re.findall('source src="(.*?)"',html2,re.DOTALL)
		if m3u8:
			m3u8 = server+m3u8[0]
			titleLIST,linkLIST = EXTRACT_M3U8(m3u8,headers)
			z = zip(titleLIST,linkLIST)
			titleLIST,linkLIST = [],[]
			for title,link in z:
				quality = title.rsplit(' ',1)[-1]
				linkLIST.append(link+'?named=vidstream__watch__m3u8__'+quality)
	"""
	# need account user/pass
	# does not work in all countries
	# download+watch links
	# https://egybest.net/api?call=PEEEjcIqEjEvEjmTpjEYTEvRYEEYTEmEEjvjEjEGmEjEvEjhKapEhAccjcUCwYEndejvjEjxIajEvEjfIaIxIeMhvYEjvjEjwfsbcIpwejEvmTbmTEmvvNbmbmbmHjEjtaEjEvEjmTpbwfNbmTajvjEjpKPEjEvEjcmIndecYpKhxDEjvjEjcIxEjEvEjmYYTTTajEb&auth=09b5c2725761e149f671827c58c4256b
	html_blocks = re.findall('</thead> <tbody>(.*?)</span> </span>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('</td> <>(.*?)<.*?data-url="(.*?)".*?data-url="(.*?)"',block,re.DOTALL)
	for quality,link1,link2 in items:
		quality = quality.strip(' ').split(' ')[-1]
		url1 = website0a+link1 # + '&v=1'
		url2 = website0a+link2 # + '&v=1'
		#url = url+'?PHPSID='+PHPSID
		linkLIST.append(url1+'?named=vidstream__download__mp4__'+quality)
		linkLIST.append(url2+'?named=vidstream__watch__mp4__'+quality)
	"""
	#selection = DIALOG_SELECT('اختر الفيديو المناسب:', linkLIST)
	if len(linkLIST)==0: DIALOG_OK('رسالة من المبرمج','للأسف لم أجد ملفات الفيديو . الرجاء إرسال سجل الأخطاء إلى المبرمج')
	import RESOLVERS
	RESOLVERS.PLAY(linkLIST,script_name,'video')
	return
	"""
	#cookies = response.cookies.get_dict()
	#PHPSID = cookies['PHPSID']
	headers2 = headers
	#headers2['Cookie'] = 'PHPSID='+PHPSID
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url2,'',headers2,False,'','EGYBEST-PLAY-3rd')
	html2 = response.content
	items = re.findall('source src="(.*?)"',html2,re.DOTALL)
	if items:
		url3 = server+items[0]
		titleLIST,linkLIST = EXTRACT_M3U8(url3)
		z = zip(titleLIST,linkLIST)
		for title,link in z:
			if 'Res: ' in title: quality = title.split('Res: ')[1]
			elif 'BW: ' in title: quality = title.split('BW: ')[1].split('kbps')[0]
			else: quality = ''
			linkLIST.append(link+'?named=vidstream__watch__m3u8__'+quality)
	#else: linkLIST.append(url2+'?named=vidstream__watch__m3u8')
	#if not linkLIST:
	#	return
	url = website0a + '/api?call=' + watchitem[0]
	EGUDI, EGUSID, EGUSS = GET_PLAY_TOKENS()
	if EGUDI=='': return
	headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET', url, '', headers, False,'','EGYBEST-PLAY-2nd')
	html = response.content
	items = re.findall('#EXT-X-STREAM.*?RESOLUTION=(.*?),.*?\n(.*?)\n',html,re.DOTALL)
	if items:
		for qualtiy,url in reversed(items):
			qualityLIST.append ('m3u8   '+qualtiy)
			datacallLIST.append (url)
	#selection = DIALOG_SELECT('اختر الفيديو المناسب:', linkLIST)
	#if selection == -1 : return
	#url = linkLIST[selection]
	if 'http' not in url:
		link = linkLIST[selection]
		url = website0a + '/api?call=' + link
		headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET', url, '', headers, False,'','EGYBEST-PLAY-3rd')
		html = response.content
		items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		#link = items[0]
		#url = website0a + '/api?call=' + link
		#headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		#response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET', url, '', headers, False,'','EGYBEST-PLAY-4th')
		#html = response.content
		#xbmc.log(escapeUNICODE(html), level=xbmc.LOGNOTICE)
		#items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		url = items[0]
		#items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		#url = items[0]
	url = url.replace('\/','/')
	#result = PLAY_VIDEO(url,script_name,'video')
	"""

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	new_search = search.replace(' ','+')
	url = website0a + '/explore/?q=' + new_search
	TITLES(url)
	return

def FILTERS_SUBMENU(text):
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a,'','','','','EGYBEST-FILTERS_SUBMENU-1st')
	html = response.content
	html_blocks = re.findall('class="i i-home"(.*?)class="i-folder">',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)</a>',block,re.DOTALL)
	for link,title in items:
		if 'trending' in link: continue
		if '</i>' in title: title = title.split('</i>')[1]
		if 'CATEGORIES' in text: addMenuItem('folder',menu_name+title,link,124,'','',text)
		elif 'FILTERS' in text: addMenuItem('folder',menu_name+title,link,125,'','',text)
	return

def FILTERS_MENU(url,filter):
	#url = url.strip('/')
	#headers2 = {'Referer':url,'User-Agent':''}
	#headers2 = ''
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
		filter_show = UNQUOTE(filter_show)
		clean_filter = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		url2 = url+'//getposts??'+clean_filter
		url4 = PREPARE_FILTER_FINAL_URL(url2)
		addMenuItem('folder',menu_name+'أظهار قائمة الفيديو التي تم اختيارها ',url4,121,'','','filters')
		addMenuItem('folder',menu_name+' [[   '+filter_show+'   ]]',url4,121,'','','filters')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'POST',url,'','','','','ARABSEED-FILTERS_MENU-1st')
	html = response.content
	html_blocks = re.findall('class="current_opt ">(.*?)<(.*?)class="dropdown"',html+'</ul></div></div>',re.DOTALL)
	dict = {}
	html_blocks1 = [('القسم','')]
	html_blocks = html_blocks1+html_blocks
	for name,block in html_blocks:
		name = name.replace(' ','')
		category2 = name
		#if 'interest' in category2: continue
		items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
		if name=='القسم':
			response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'','','','','EGYBEST-SUBMENU-1st')
			html = response.content
			html_blocks = re.findall('class="rs_scroll"(.*?)</div>',html,re.DOTALL)
			block = html_blocks[0]
			items1 = re.findall('href="(.*?)".*?</i>(.*?)</a>',block,re.DOTALL)
			items = items1+items
		if '==' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==all_categories_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES___'+new_filter)
				return
			else:
				url4 = PREPARE_FILTER_FINAL_URL(url2)
				if category2==all_categories_list[-1]: addMenuItem('folder',menu_name+'الجميع ',url4,121,'','','filters')
				else: addMenuItem('folder',menu_name+'الجميع ',url2,124,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&&'+category2+'==0'
			new_values = filter_values+'&&'+category2+'==0'
			new_filter = new_options+'___'+new_values
			addMenuItem('folder',menu_name+name+': الجميع',url2,125,'','',new_filter+'_FORGETRESULTS_')
		dict[category2] = {}
		for value,option in items:
			option = option.strip(' ')
			value = value.rsplit('/',1)[1]
			if 'الكل' in option: continue
			#if option in ignoreLIST: continue
			#if 'http' in option: continue
			#if 'n-a' in value: continue
			title1,title2 = option,option
			if name!='': title2 = name+': '+title1
			dict[category2][value] = title2
			new_options = filter_options+'&&'+category2+'=='+title1
			new_values = filter_values+'&&'+category2+'=='+value
			new_filter2 = new_options+'___'+new_values
			if type=='FILTERS':
				addMenuItem('folder',menu_name+title2,url,125,'','',new_filter2+'_FORGETRESULTS_')
			elif type=='CATEGORIES' and all_categories_list[-2]+'==' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'modified_filters')
				url3 = url+'//getposts??'+clean_filter
				url4 = PREPARE_FILTER_FINAL_URL(url3)
				addMenuItem('folder',menu_name+title2,url4,121,'','','filters')
			else: addMenuItem('folder',menu_name+title2,url,124,'','',new_filter2)
	return

all_categories_list = ['القسم','اللغة','البلد','السنة']
all_filters_list = ['القسم','اللغة','البلد','السنة','النوع','التصنيف','الجودة']

def PREPARE_FILTER_FINAL_URL(url):
	#DIALOG_OK(url,'PREPARE_FILTER_FINAL_URL   IN')
	for key in all_filters_list:
		url = url.replace(key+'==','')
	url = url.replace('&&','-')
	url = url.replace('///getposts??','/')
	url = url.strip('/')
	#DIALOG_OK(url,'PREPARE_FILTER_FINAL_URL   OUT')
	return url

def RECONSTRUCT_FILTER(filters,mode):
	#DIALOG_OK(filters,'RECONSTRUCT_FILTER   IN   '+mode)
	# mode=='modified_values'		only non empty values
	# mode=='modified_filters'		only non empty filters
	# mode=='all'					all filters (includes empty filter)
	filters = filters.strip('FILTERS&&')
	filters = filters.strip('CATEGORIES&&')
	#filters = filters.strip('&&')
	filtersDICT,new_filters = {},''
	if '==' in filters:
		items = filters.split('&&')
		for item in items:
			key,value = item.split('==')
			filtersDICT[key] = value
	for key in all_filters_list:
		if key in filtersDICT.keys():
			value = filtersDICT[key]
		else: value = '0'
		if '%' not in value: value = QUOTE(value)
		if mode=='modified_values' and value!='0': new_filters = new_filters+' + '+value
		elif mode=='modified_filters' and value!='0': new_filters = new_filters+'&&'+key+'=='+value
		elif mode=='all': new_filters = new_filters+'&&'+key+'=='+value
	new_filters = new_filters.strip(' + ')
	new_filters = new_filters.strip('&&')
	#DIALOG_OK(new_filters,'RECONSTRUCT_FILTER   OUT   '+mode)
	return new_filters

"""
def OLD_FILTERS_MENU(link):
	filter = link.split('/')[-1]
	if '/movies/' in link:
		if filter=='': filter = 'new'
		elif not any(value in filter for value in ['latest','top','popular']): filter = 'new-'+filter
	elif '/tv/' in link:
		if filter=='': filter = 'latest'
		elif not any(value in filter for value in ['new','top','popular']): filter = 'latest-'+filter
	filter = filter.replace('-',' + ')
	#DIALOG_OK(str(link), str(filter))
	if '/trending/' not in link:
		addMenuItem('folder',menu_name+'اظهار قائمة الفيديو التي تم اختيارها',link,121)
		addMenuItem('folder',menu_name+'[[   ' + filter + '   ]]',link,121)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = OPENURL_CACHED(LONG_CACHE,link,'',headers,'','EGYBEST-FILTERS_MENU-1st')
	html_blocks=re.findall('mainLoad(.*?)</div></div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items=re.findall('href="(.*?)".*?</i> (.*?)<',block,re.DOTALL)
		for url,title in items:
			#if '/movies/' in url and 'فلام' not in title: title = 'افلام ' + title
			#elif '/tv/' in url and 'مسلسل' not in title: title = 'مسلسلات ' + title
			if '/trending/' in url:
				title = 'الاكثر مشاهدة ' + title
				addMenuItem('folder',menu_name+title,url,121)
			else:
				link = link.replace('popular','')
				link = link.replace('top','')
				link = link.replace('latest','')
				link = link.replace('new','')
				newfilter = url.split('/')[-1]
				url = link + '-' + newfilter
				url = url.replace('/-','/')
				url = url.rstrip('-')
				url = url.replace('--','-')
				addMenuItem('folder',menu_name+title,url,125)
	html_blocks=re.findall('sub_nav(.*?)</div></div></div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			ignoreLIST = ['- الكل -','[R]']
			if any(value in title for value in ignoreLIST): continue
			#if '/movies/' in link: title = '_MOD_' + 'افلام ' + title
			#elif '/tv/' in link: title = '_MOD_' + 'مسلسلات ' + title
			addMenuItem('folder',menu_name+title,link,125)
	return

def GET_USERNAME_PASSWORD():
	text = 'هذا الموقع يحتاج اسم دخول وكلمة السر لكي تستطيع تشغيل ملفات الفيديو. للحصول عليهم قم بفتح حساب مجاني من الموقع الاصلي'
	DIALOG_OK('الموقع الاصلي  '+website0a,text)
	oldusername = settings.getSetting('egybest.user')
	oldpassword = settings.getSetting('egybest.pass')
	xbmc.executebuiltin('Addon.OpenSettings(%s)' %addon_id, True)
	newusername = settings.getSetting('egybest.user')
	newpassword = settings.getSetting('egybest.pass')
	if oldusername!=newusername or oldpassword!=newpassword:
		settings.setSetting('egybest.EGUDI','')
		settings.setSetting('egybest.EGUSID','')
		settings.setSetting('egybest.EGUSS','')
	return

def GET_PLAY_TOKENS():
	EGUDI = settings.getSetting('egybest.EGUDI')
	EGUSID = settings.getSetting('egybest.EGUSID')
	EGUSS = settings.getSetting('egybest.EGUSS')
	username = mixARABIC(settings.getSetting('egybest.user'))
	password = mixARABIC(settings.getSetting('egybest.pass'))
	#DIALOG_OK(username,password)
	if username=='' or password=='':
		settings.setSetting('egybest.EGUDI','')
		settings.setSetting('egybest.EGUSID','')
		settings.setSetting('egybest.EGUSS','')
		GET_USERNAME_PASSWORD()
		return ['','','']
	if EGUDI!='':
		headers = { 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET', website0a, '', headers, False,'','EGYBEST-GET_PLAY_TOKENS-1st')
		register = re.findall('ssl.egexa.com\/register',response.content,re.DOTALL)
		if register:
			settings.setSetting('egybest.EGUDI','')
			settings.setSetting('egybest.EGUSID','')
			settings.setSetting('egybest.EGUSS','')
		else:
			#DIALOG_OK('no new login needed, you were already logged in','')
			return [ EGUDI, EGUSID, EGUSS ]
	char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
	randomString = ''.join(random.sample(char_set*15, 15))
	url = "https://ssl.egexa.com/login/"
	#recaptcha = '03AOLTBLQDtmeIcT8L59DpznG0p1WCkhhumhekamXOdA1k9K6cSu_EYatvjH-RpkHnQh4TKhJl8RVvs_ipxjc6jIeAYRdbge_GrQdvT4wHWm_Lv6L23ZEgFOlxhavVhwhq2OeDGK-bonSSSIU4qiHOtRfbwW8JfHN-Izxb-TxM6OWZL2juHygljmFCjFX5E_tfY2XJvMqGSjhFa5xYwatX-cmpX7X0My9Q7mkpu86A-JmXtcotcXoN6WAmVwUYomLPPYxpfapJnfWX3Bw833YKD_BDWwvTXjfW_PeNUdJH7FwL9tn5_ghDqVe_lQkhp6ooXmVtjMAn9_M4'
	#recaptcha = ''
	payload = ""
	payload += "------WebKitFormBoundary"+randomString+"\nContent-Disposition: form-data; name=\"ajax\"\n\n1\n"
	payload += "------WebKitFormBoundary"+randomString+"\nContent-Disposition: form-data; name=\"do\"\n\nlogin\n"
	payload += "------WebKitFormBoundary"+randomString+"\nContent-Disposition: form-data; name=\"email\"\n\n"+username+"\n"
	payload += "------WebKitFormBoundary"+randomString+"\nContent-Disposition: form-data; name=\"password\"\n\n"+password+"\n"
	#payload += "------WebKitFormBoundary"+randomString+"\nContent-Disposition: form-data; name=\"g-recaptcha-response\"\n\n"+recaptcha+"\n"
	payload += "------WebKitFormBoundary"+randomString+"\nContent-Disposition: form-data; name=\"valForm\"\n\n\n"
	payload += "------WebKitFormBoundary"+randomString+"--"
	#xbmc.log(payload, level=xbmc.LOGNOTICE)
	headers = {
	'Content-Type': "multipart/form-data; boundary=----WebKitFormBoundary"+randomString,
	#'Cookie': "PSSID="+PSSID+"; JS_TIMEZONE_OFFSET=18000",
	'Referer': 'https://ssl.egexa.com/login/?domain='+website0a.split('//')[1]+'&url=ref'
	}
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST', url, payload, headers, False,'','EGYBEST-GET_PLAY_TOKENS-2nd')
	cookies = response.cookies.get_dict()
	#xbmc.log(response.content, level=xbmc.LOGNOTICE)
	if '"action":"captcha"' in response.content:
		DIALOG_OK('مشكلة جدا مزعجة تخص جهازك فقط','موقع ايجي بيست يرفض دخولك اليهم بإستخدام كودي ... حاول فصل الانترنيت واعادة ربطها لتحصل على عنوان IP جديد ... او اعد المحاولة بعد عدة ايام او عدة اسابيع')
		return ['','','']
	if len(cookies)<3:
		DIALOG_OK('مشكلة في تسجيل الدخول للموقع','حاول اصلاح اسم الدخول وكلمة السر لكي تتمكن من تشغيل الفيديو بصورة صحيحة')
		GET_USERNAME_PASSWORD()
		return ['','','']
	EGUDI = cookies['EGUDI']
	EGUSID = cookies['EGUSID']
	EGUSS = cookies['EGUSS']
	time.sleep(1)
	url = "https://ssl.egexa.com/finish/"
	headers = { 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET', url, '', headers, True,'','EGYBEST-GET_PLAY_TOKENS-3rd')
	cookies = response.cookies.get_dict()
	#DIALOG_OK(str(response.content),str(cookies))
	EGUDI = cookies['EGUDI']
	EGUSID = cookies['EGUSID']
	EGUSS = cookies['EGUSS']
	settings.setSetting('egybest.EGUDI',EGUDI)
	settings.setSetting('egybest.EGUSID',EGUSID)
	settings.setSetting('egybest.EGUSS',EGUSS)
	#DIALOG_OK('success, you just logged in now','')
	return [ EGUDI, EGUSID, EGUSS ]
"""







#=================================================================================
# some of the below functions were added from:
# https://github.com/zombiB/zombi-addons/blob/master/plugin.video.matrix/resources/sites/egybest.py
#=================================================================================

def atob(elm):
    try:
        ret = base64.b64decode(elm)
    except:
        try:
            ret = base64.b64decode(elm+'=')
        except:
            try:
                ret = base64.b64decode(elm+'==')
            except:
                ret = 'ERR:base64 decode error'
    return ret

def a0d(main_tab,step2,a):
    a = a - step2
    if a<0:
        c = 'undefined'
    else:
        c = main_tab[a]
    return c

def x(main_tab,step2,a):
    return(a0d(main_tab,step2,a))

def parseInt(sin):
  m = re.search(r'^(\d+)[.,]?\d*?', str(sin))
  return int(m.groups()[-1]) if m and not callable(sin) else 0

def decal(tab,step,step2,decal_fnc):
    decal_fnc = decal_fnc.replace('var ','')    
    decal_fnc = decal_fnc.replace('x(','x(tab,step2,') 
    exec(decal_fnc)
    aa=0
    while True:
        aa=aa+1
        tab.append(tab[0])
        del tab[0]
        #print([i for i in tab[0:10]])
        exec(decal_fnc) 
        #print(str(aa)+':'+str(c))
        if ((c == step) or (aa>10000)): break

def VidStream(script):
	tmp = re.findall('function.+?{ var(.+?)=', script, re.S)
	if not tmp: return 'ERR:Varconst Not Found'
	varconst = tmp[0].strip()
	#print('Varconst     = %s' % varconst)
	tmp = re.findall('}\('+varconst+'?,(0x[0-9a-f]{1,10})\)\);', script)
	if not tmp: return 'ERR:Step1 Not Found'
	step = eval(tmp[0])
	#print('Step1        = 0x%s' % '{:02X}'.format(step).lower())
	tmp = re.findall('a=a-(0x[0-9a-f]{1,10});', script)
	if not tmp: return 'ERR:Step2 Not Found'
	step2 = eval(tmp[0])
	#print('Step2        = 0x%s' % '{:02X}'.format(step2).lower())    
	tmp = re.findall("try{(var.*?);", script)
	if not tmp: return 'ERR:decal_fnc Not Found'
	decal_fnc = tmp[0]
	#print('Decal func   = " %s..."' % decal_fnc[0:135])   
	tmp = re.findall("'data':{'(_[0-9a-zA-Z]{10,20})':'ok'", script)
	if not tmp: return 'ERR:PostKey Not Found'
	PostKey = tmp[0]
	#print('PostKey      = %s' % PostKey)
	tmp = re.findall("(var "+varconst+"=\[.*?\];)", script)
	if not tmp: return 'ERR:TabList Not Found'	
	TabList = tmp[0]
	TabList = TabList.replace('var ','')
	exec(TabList) in globals(), locals()
	main_tab = locals()[varconst]
	#print(varconst+'          = %.90s...'%str(main_tab))
	decal(main_tab,step,step2,decal_fnc)
	#print(varconst+'          = %.90s...'%str(main_tab))
	tmp = re.findall(";"+varconst[0:2]+".\(\);(var .*?)\$\('\*'\)", script, re.S)
	if not tmp: return 'ERR:List_Var Not Found'		
	List_Var = tmp[0]
	#print('List_Var     = %.90s...' % List_Var)
	tmp = re.findall("(_[a-zA-z0-9]{4,8})=\[\]" , List_Var)
	if not tmp: return 'ERR:3Vars Not Found'
	_3Vars = tmp
	#print('3Vars        = %s'%str(_3Vars))
	big_str_var = _3Vars[1]
	#print('big_str_var  = %s'%big_str_var)    
	List_Var = List_Var.replace(',',';').split(';')
	for elm in List_Var:
		elm = elm.strip()
		if 'ismob' in elm: elm=''
		if '=[]'   in elm: elm = elm.replace('=[]','={}')
		elm = re.sub("(a0.\()", "a0d(main_tab,step2,", elm)
		#if 'a0G('  in elm: elm = elm.replace('a0G(','a0G(main_tab,step2,') 
		if elm!='':
			#print('elm = %s' % elm)
			elm = elm.replace('!![]','True');
			elm = elm.replace('![]','False');
			elm = elm.replace('var ','');
			#print('elm = %s' % elm)
			try:
				exec(elm)
			except:
				print('elm = %s' % elm)
				print('v = "%s" exec problem!' % elm, sys.exc_info()[0])            
	bigString = ''
	for i in range(0,len(locals()[_3Vars[2]])):
		if locals()[_3Vars[2]][i] in locals()[_3Vars[1]]:
			bigString = bigString + locals()[_3Vars[1]][locals()[_3Vars[2]][i]]	
	#print('bigString    = %.90s...'%bigString) 
	tmp = re.findall('var b=\'/\'\+(.*?)(?:,|;)', script, re.S)
	if not tmp: return 'ERR:GetUrl Not Found'
	GetUrl = str(tmp[0])
	#print('GetUrl       = %s' % GetUrl)    
	tmp = re.findall('(_.*?)\[', GetUrl, re.S)
	if not tmp: return 'ERR:GetVar Not Found'
	GetVar = tmp[0]
	#print('GetVar       = %s' % GetVar)
	GetVal = locals()[GetVar][0]
	GetVal = atob(GetVal)
	#print('GetVal       = %s' % GetVal)
	tmp = re.findall('}var (f=.*?);', script, re.S)        
	if not tmp: return 'ERR:PostUrl Not Found'
	PostUrl = str(tmp[0])
	#print('PostUrl      = %s' % PostUrl)
	PostUrl = re.sub("(window\[.*?\])", "atob", PostUrl)        
	PostUrl = re.sub("([A-G]{1,2}\()", "a0d(main_tab,step2,", PostUrl)    
	exec(PostUrl)
	return(['/'+GetVal,f+bigString,{ PostKey : 'ok'}])






"""
url = 'https://tool.egybest.ltd/movie/laugh-killer-laugh-2015'
url = 'https://tool.egybest.ltd/movie/all-hallows-eve-2-2015/?ref=similar'
url = 'https://tool.egybest.ltd/movie/adverse-2020/?ref=movies-p1'
response = OPENURL_REQUESTS_CACHED(NO_CACHE,'GET',url,'','','','','TEST1')
html = response.content
link = re.findall('class="auto-size" src="(.*?)"',html,re.DOTALL)
link = 'https://tool.egybest.ltd'+link[0]
#link = 'https://tool.egybest.ltd/watch/?v=YhhheGZiZGdXVrehQhhheGlEhehQhefSKKWxMddedkiZfhKbfKheQeheCKduehQheDlOdpIdeKfDXRDqTVZfhhehYQehedSKhehQhedKYDSnEVdhdZWGheQeheZvoYdSlZWehQDnYDnhDQDmCdDfQQeheKSNehQhesdSKGflpNohdpodZpKheQehedSchehQheDnlehfnhQrfhhfnhDhhehY&h=5de8bb072d336de05092297ec8b61643'
response = OPENURL_REQUESTS_CACHED(NO_CACHE,'GET',link,'','','','','TEST2')
html = response.content
try:
	result = VidStream(html)
	ln1,ln2,prm = result
	LOG_THIS('','EMAD EMAD:   '+str(ln1))
	LOG_THIS('','EMAD EMAD:   '+str(ln2))
	LOG_THIS('','EMAD EMAD:   '+str(prm))
except:
	LOG_THIS('','EMAD EMAD:   '+str(result))
"""


