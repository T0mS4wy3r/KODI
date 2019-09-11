# -*- coding: utf-8 -*-
from LIBRARY import *

#website0a = 'https://egy.best'
#website0a = 'https://egy1.best'
#website0a = 'https://egybest1.com'
#website0a = 'https://egybest.vip'

headers = { 'User-Agent' : '' }
script_name = 'EGY4BEST'
menu_name='_EG4_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,page,text):
	xbmc.log(LOGGING(script_name)+'Mode:['+str(mode)+']   Label:['+menulabel+']   Path:['+menupath+']', level=xbmc.LOGNOTICE)
	if   mode==220: MAIN_MENU()
	elif mode==221: FILTERS_MENU(url)
	elif mode==222: TITLES(url,page)
	elif mode==223: PLAY(url)
	elif mode==225: GET_USERNAME_PASSWORD()
	elif mode==226: WARNING()
	elif mode==229: SEARCH(text)
	return

def MAIN_MENU():
	#addDir(menu_name+'اضغط هنا لاضافة اسم دخول وكلمة السر','',125)
	#addDir(menu_name+'تحذير','',226)
	addDir(menu_name+'بحث في الموقع','',229)
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','EGY4BEST-MAIN_MENU-1st')
	#xbmcgui.Dialog().ok(website0a, html)
	html_blocks=re.findall('id="menu"(.*?)mainLoad',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".*?i>(.*?)\n',block,re.DOTALL)
	for url,title in items:
		if url!=website0a: addDir(menu_name+title,url,221)
	html_blocks=re.findall('class="ba mgb(.*?)class="tam pdb',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for link,title in items:
		addDir(menu_name+title,link,222,'','1')
	xbmcplugin.endOfDirectory(addon_handle)
	return
	"""
	# egybest1.com
	html_blocks=re.findall('id="menu"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	#items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	items=re.findall('<a href="(.*?)".*?[1/][i"]>(.*?)</a',block,re.DOTALL)
	for link,title in items:
		if 'torrent' not in link: addDir(menu_name+title,link,222)
	html_blocks=re.findall('class="card(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		if 'torrent' not in link: addDir(menu_name+title,link,222)
	"""

def FILTERS_MENU(url):
	html = openURL_cached(LONG_CACHE,url,'',headers,'','EGY4BEST-FILTERS_MENU-1st')
	#xbmcgui.Dialog().ok(website0a, html)
	html_blocks=re.findall('class="sub_nav(.*?)id="movies',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".+?>(.*?)<',block,re.DOTALL)
	for link,title in items:
		if link=='#': name = title
		else:
			title = title + '  :  ' + 'فلتر ' + name
			addDir(menu_name+title,link,222,'','1')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url,page):
	#xbmcgui.Dialog().ok(str(url), str(page))
	if '/search' in url or '?' in url: url2 = url + '&'
	else: url2 = url + '?'
	#url2 = url2 + 'output_format=json&output_mode=movies_list&page='+page
	url2 = url2 + 'page=' + page
	html = openURL_cached(REGULAR_CACHE,url2,'',headers,'','EGY4BEST-TITLES-1st')
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
		html_blocks=re.findall('id="movies(.*?)class="footer',html,re.DOTALL)
		block = html_blocks[-1]
	items = re.findall('<a href="(.*?)".*?src="(.*?)".*?title">(.*?)<',block,re.DOTALL)
	for link,img,title in items:
		"""
		if '/series' in url and '/season' not in link: continue
		if '/season' in url and '/episode' not in link: continue
		#xbmcgui.Dialog().ok(title, str(link))
		title = name + escapeUNICODE(title).strip(' ')
		"""
		title = unescapeHTML(title)
		"""
		title = title.replace('\n','')
		link = link.replace('\/','/')
		img = img.replace('\/','/')
		if 'http' not in img: img = 'http:' + img
		#xbmcgui.Dialog().notification(img,'')
		url2 = website0a + link
		"""
		if '/movie/' in link or '/episode' in link:
			addLink(menu_name+title,link.rstrip('/'),123,img)
		else:
			addDir(menu_name+title,link,122,img,'1')
	count = len(items)
	if (count==16 and '/movies' in url) \
		or (count==16 and '/trending' in url) \
		or (count==19 and '/tv' in url):
		pagingLIST = ['/movies','/tv','/search','/trending']
		page = int(page)
		if any(value in url for value in pagingLIST):
			for n in range(0,1000,100):
				if int(page/100)*100==n:
					for i in range(n,n+100,10):
						if int(page/10)*10==i:
							for j in range(i,i+10,1):
								if not page==j and j!=0:
									addDir(menu_name+'صفحة '+str(j),url,122,'',str(j))
						elif i!=0: addDir(menu_name+'صفحة '+str(i),url,122,'',str(i))
						else: addDir(menu_name+'صفحة '+str(1),url,122,'',str(1))
				elif n!=0: addDir(menu_name+'صفحة '+str(n),url,122,'',str(n))
				else: addDir(menu_name+'صفحة '+str(1),url,122,'','1')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	headers = { 'User-Agent' : '' }
	html = openURL_cached(LONG_CACHE,url,'',headers,'','EGY4BEST-PLAY-1st')
	rating = re.findall('<td>التصنيف</td>.*?">(.*?)<',html,re.DOTALL)
	if rating[0] in ['R','TVMA','TV-MA','PG-18','NC-17']:
		xbmcgui.Dialog().notification('قم بتشغيل فيديو غيره','هذا الفيديو للكبار فقط ولا يعمل هنا')
		return
	html_blocks = re.findall('tbody(.*?)tbody',html,re.DOTALL)
	if not html_blocks:
		xbmcgui.Dialog().notification('خطأ من الموقع الاصلي','ملف الفيديو غير متوفر')
		return
	block = html_blocks[0]
	showUrl = re.findall('id="video".*?src="(.*?)"',block,re.DOTALL)
	html = openURL_cached(LONG_CACHE,showUrl,'',headers,'','EGY4BEST-PLAY-2nd')
	items = re.findall('source src="(.*?)" title="(.*?)"',html,re.DOTALL)
	#titleLIST,linkLIST = zip(*items)
	titleLIST,linkLIST = [],[]
	for link,title in items:
		linkLIST = linkLIST.append(link)
		titleLIST = titleLIST.append(title)
	selection = xbmcgui.Dialog().select('اختر الفيديو المناسب:', titleLIST)
	if selection == -1 : return
	url = linkLIST[selection]
	PLAY_VIDEO(url,script_name,'yes')
	return
	"""
	import RESOLVERS
	result = RESOLVERS.PLAY(linkLIST,script_name)
	if result!='playing': WARNING()
	"""

def WARNING():
	xbmcgui.Dialog().ok('https://egy4best.com','هذا الموقع هو البديل الجديد لموقع ايجي بيست السابق وهو قيد الانشاء ولهذا الكثير من الفيدوهات لا تعمل')
	return

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search == '': return
	new_search = search.replace(' ','+')
	url = website0a + '/search?q=' + new_search
	TITLES(url,'1')
	return

"""
def FILTERS_MENU_OLD(link):
	filter = link.split('/')[-1]
	if '/movies' in link:
		if filter=='': filter = 'new'
		elif not any(value in filter for value in ['latest','top','popular']): filter = 'new-'+filter
	elif '/tv' in link:
		if filter=='': filter = 'latest'
		elif not any(value in filter for value in ['new','top','popular']): filter = 'latest-'+filter
	filter = filter.replace('-',' + ')
	#xbmcgui.Dialog().ok(str(link), str(filter))
	if '/trending' not in link:
		addDir(menu_name+'اظهار قائمة الفيديو التي تم اختيارها',link,122,'','1')
		addDir(menu_name+'[[   ' + filter + '   ]]',link,122,'','1')
		addDir(menu_name+'===========================',link,9999)
	html = openURL_cached(LONG_CACHE,link,'',headers,'','EGY4BEST-FILTERS_MENU-1st')
	html_blocks=re.findall('mainLoad(.*?)</div>\n</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items=re.findall('href="(.*?)".*?</i> (.*?)<',block,re.DOTALL)
		for url,title in items:
			if '/movies' in url and 'فلام' not in title: title = 'افلام ' + title
			elif '/tv' in url and 'مسلسل' not in title: title = 'مسلسلات ' + title
			if '/trending' in url:
				title = 'الاكثر مشاهدة ' + title
				addDir(menu_name+title,url,122,'','1')
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
				addDir(menu_name+title,url,121)
	html_blocks=re.findall('sub_nav(.*?)</div>\n</div>\n</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for url,title in items:
			ignoreLIST = ['- الكل -','[R]']
			if any(value in title for value in ignoreLIST): continue
			if '/movies' in url: title = '_MOD_' + 'افلام ' + title
			elif '/tv' in url: title = '_MOD_' + 'مسلسلات ' + title
			addDir(menu_name+title,url,121)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY_OLD(url):
	#xbmcgui.Dialog().ok(url, url[-45:])
	headers = { 'User-Agent' : '' }
	html = openURL_cached(LONG_CACHE,url,'',headers,'','EGY4BEST-PLAY-1st')
	rating = re.findall('<td>التصنيف</td>.*?">(.*?)<',html,re.DOTALL)
	if rating[0] in ['R','TVMA','TV-MA','PG-18','PG-16']:
		xbmcgui.Dialog().notification('قم بتشغيل فيديو غيره','هذا الفيديو للكبار فقط ولا يعمل هنا')
		return
	html_blocks = re.findall('tbody(.*?)tbody',html,re.DOTALL)
	if not html_blocks:
		xbmcgui.Dialog().notification('خطأ من الموقع الاصلي','ملف الفيديو غير متوفر')
		return
	block = html_blocks[0]
	items = re.findall('</td> <td>(.*?)<.*?data-call="(.*?)"',block,re.DOTALL)
	qualityLIST = []
	datacallLIST = []
	if len(items)>0:
		for qualtiy,datacall in items:
			qualityLIST.append ('mp4   '+qualtiy)
			datacallLIST.append (datacall)
	watchitem = re.findall('x-mpegURL" src="/api/\?call=(.*?)"',html,re.DOTALL)
	url = website0a + '/api?call=' + watchitem[0]
	EGUDI, EGUSID, EGUSS = GET_PLAY_TOKENS()
	if EGUDI=='': return
	headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
	response = openURL_requests_cached(SHORT_CACHE,'GET', url, '', headers, False,'','EGY4BEST-PLAY-2nd')
	html = response.text
	#xbmcgui.Dialog().ok(url,html)
	items = re.findall('#EXT-X-STREAM.*?RESOLUTION=(.*?),.*?\n(.*?)\n',html,re.DOTALL)
	if len(items)>0:
		for qualtiy,url in reversed(items):
			qualityLIST.append ('m3u8   '+qualtiy)
			datacallLIST.append (url)
	selection = xbmcgui.Dialog().select('اختر الفيديو المناسب:', qualityLIST)
	if selection == -1 : return
	url = datacallLIST[selection]
	if 'http' not in url:
		datacall = datacallLIST[selection]
		url = website0a + '/api?call=' + datacall
		headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		response = openURL_requests_cached(SHORT_CACHE,'GET', url, '', headers, False,'','EGY4BEST-PLAY-3rd')
		html = response.text
		#xbmcgui.Dialog().ok(url,html)
		#xbmc.log(html, level=xbmc.LOGNOTICE)
		items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		#datacall = items[0]

		#url = website0a + '/api?call=' + datacall
		#headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		#response = requests_request('GET', url, headers=headers, allow_redirects=False)
		#html = response.text
		#xbmc.log(escapeUNICODE(html), level=xbmc.LOGNOTICE)
		#items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		url = items[0]

		#xbmcgui.Dialog().ok(url,html)
		#xbmc.log(html, level=xbmc.LOGNOTICE)
		#items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		#url = items[0]
	url = url.replace('\/','/')
	#xbmc.log(url, level=xbmc.LOGNOTICE)
	#xbmcgui.Dialog().ok(url,url[-45:])
	PLAY_VIDEO(url,script_name,'yes')
	return

def GET_USERNAME_PASSWORD_OLD():
	text = 'هذا الموقع يحتاج اسم دخول وكلمة السر لكي تستطيع تشغيل ملفات الفيديو. للحصول عليهم قم بفتح حساب مجاني من الموقع الاصلي'
	xbmcgui.Dialog().ok('الموقع الاصلي  '+website0a,text)
	settings = xbmcaddon.Addon(id=addon_id)
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

def GET_PLAY_TOKENS_OLD():
	settings = xbmcaddon.Addon(id=addon_id)
	EGUDI = settings.getSetting('egybest.EGUDI')
	EGUSID = settings.getSetting('egybest.EGUSID')
	EGUSS = settings.getSetting('egybest.EGUSS')
	username = mixARABIC(settings.getSetting('egybest.user'))
	password = mixARABIC(settings.getSetting('egybest.pass'))
	#xbmcgui.Dialog().ok(username,password)
	if username=='' or password=='':
		settings.setSetting('egybest.EGUDI','')
		settings.setSetting('egybest.EGUSID','')
		settings.setSetting('egybest.EGUSS','')
		GET_USERNAME_PASSWORD()
		return ['','','']

	if EGUDI!='':
		headers = { 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		response = openURL_requests_cached(SHORT_CACHE,'GET', website0a, '', headers, False,'','EGY4BEST-GET_PLAY_TOKENS-1st')
		register = re.findall('ssl.egexa.com\/register',response.text,re.DOTALL)
		if register:
			settings.setSetting('egybest.EGUDI','')
			settings.setSetting('egybest.EGUSID','')
			settings.setSetting('egybest.EGUSS','')
		else:
			#xbmcgui.Dialog().ok('no new login needed, you were already logged in','')
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
	response = openURL_requests_cached(SHORT_CACHE,'POST', url, payload, headers, False,'','EGY4BEST-GET_PLAY_TOKENS-2nd')
	cookies = response.cookies.get_dict()
	#xbmc.log(response.text, level=xbmc.LOGNOTICE)

	if '"action":"captcha"' in response.text:
		xbmcgui.Dialog().ok('مشكلة جدا مزعجة تخص جهازك فقط','موقع ايجي بيست يرفض دخولك اليهم بإستخدام كودي ... حاول فصل الانترنيت واعادة ربطها لتحصل على عنوان IP جديد ... او اعد المحاولة بعد عدة ايام او عدة اسابيع')
		return ['','','']

	if len(cookies)<3:
		xbmcgui.Dialog().ok('مشكلة في تسجيل الدخول للموقع','حاول اصلاح اسم الدخول وكلمة السر لكي تتمكن من تشغيل الفيديو بصورة صحيحة')
		GET_USERNAME_PASSWORD()
		return ['','','']

	EGUDI = cookies['EGUDI']
	EGUSID = cookies['EGUSID']
	EGUSS = cookies['EGUSS']
	xbmc.sleep(1000)
	url = "https://ssl.egexa.com/finish/"
	headers = { 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
	response = openURL_requests_cached(SHORT_CACHE,'GET', url, '', headers, True,'','EGY4BEST-GET_PLAY_TOKENS-3rd')
	cookies = response.cookies.get_dict()
	#xbmcgui.Dialog().ok(str(response.text),str(cookies))
	EGUDI = cookies['EGUDI']
	EGUSID = cookies['EGUSID']
	EGUSS = cookies['EGUSS']
	settings.setSetting('egybest.EGUDI',EGUDI)
	settings.setSetting('egybest.EGUSID',EGUSID)
	settings.setSetting('egybest.EGUSS',EGUSS)
	#xbmcgui.Dialog().ok('success, you just logged in now','')
	return [ EGUDI, EGUSID, EGUSS ]
"""





