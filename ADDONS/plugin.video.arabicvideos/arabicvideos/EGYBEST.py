# -*- coding: utf-8 -*-
from LIBRARY import *

#website0a = 'https://egy4best.com'
#website0a = 'https://egy1.best'
#website0a = 'https://egybest1.com'
#website0a = 'https://egybest.vip'

"""
https://ww.egy.best
https://movies.egybest.site
https://series.egybest.tv
https://back.egybest.co
https://ww.egybest.blog
"""

#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
#headers = {'User-Agent':''}
headers = {'User-Agent':None}
script_name = 'EGYBEST'
menu_name='_EGB_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,page,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==120: results = MENU(url)
	elif mode==121: results = FILTERS_MENU(url)
	elif mode==122: results = TITLES(url,page)
	elif mode==123: results = PLAY(url)
	elif mode==125: results = GET_USERNAME_PASSWORD()
	elif mode==126: results = WARNING()
	elif mode==128: results = TERMINATED_ADBLOCKER()
	elif mode==129: results = SEARCH(text)
	else: results = False
	return results

def TERMINATED_ADBLOCKER():
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','سيرفر ملفات الفيديو لهذا الموقع يستخدم مانع اعلانات والمبرمج لم يستطع تجاوزه لان كودي لا يفهم لغة البرمجة جافاسكربت ولهذا سيبقى الموقع مغلق الى ما شاء الله')
	return

def MENU(website=''):
	#addMenuItem('folder',menu_name+'تحذير','',126)
	#addMenuItem('folder',menu_name+'اضغط هنا لاضافة اسم دخول وكلمة السر','',125)
	addMenuItem('folder',menu_name+'بحث في الموقع','',129,'','','_REMEMBERRESULTS_')
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','EGYBEST-MENU-1st')
	#XBMCGUI_DIALOG_OK(website0a, html)
	#addMenuItem('folder',website+'___'+menu_name+'الأكثر مشاهدة',website0a+'/trending/',121)
	#addMenuItem('folder',website+'___'+menu_name+'الأفلام',website0a+'/movies/',121)
	#addMenuItem('folder',website+'___'+menu_name+'المسلسلات',website0a+'/tv/',121)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks=re.findall('class="ba(.*?)<script',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('pda bdb"><strong>(.*?)<.*?href="(.*?)"',html,re.DOTALL)
	ignoreLIST = ['تابع ايجي بست']
	for title,link in items:
		if title not in ignoreLIST: addMenuItem('folder',website+'___'+menu_name+title,link,122,'','1')
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for link,title in items:
		#if title not in ignoreLIST: addMenuItem('folder',website+'___'+menu_name+title,link,122,'','1')
		if not link.endswith('/'): addMenuItem('folder',website+'___'+menu_name+title,link,122,'','1')
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def FILTERS_MENU(link):
	filter = link.split('/')[-1]
	if '/movies/' in link:
		if filter=='': filter = 'new'
		elif not any(value in filter for value in ['latest','top','popular']): filter = 'new-'+filter
	elif '/tv/' in link:
		if filter=='': filter = 'latest'
		elif not any(value in filter for value in ['new','top','popular']): filter = 'latest-'+filter
	filter = filter.replace('-',' + ')
	#XBMCGUI_DIALOG_OK(str(link), str(filter))
	if '/trending/' not in link:
		addMenuItem('folder',menu_name+'اظهار قائمة الفيديو التي تم اختيارها',link,122,'','1')
		addMenuItem('folder',menu_name+'[[   ' + filter + '   ]]',link,122,'','1')
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = openURL_cached(LONG_CACHE,link,'',headers,'','EGYBEST-FILTERS_MENU-1st')
	html_blocks=re.findall('mainLoad(.*?)</div></div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items=re.findall('href="(.*?)".*?</i> (.*?)<',block,re.DOTALL)
		for url,title in items:
			if '/movies/' in url and 'فلام' not in title: title = 'افلام ' + title
			elif '/tv/' in url and 'مسلسل' not in title: title = 'مسلسلات ' + title
			if '/trending/' in url:
				title = 'الاكثر مشاهدة ' + title
				addMenuItem('folder',menu_name+title,url,122,'','1')
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
				addMenuItem('folder',menu_name+title,url,121)
	html_blocks=re.findall('sub_nav(.*?)</div></div></div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for url,title in items:
			ignoreLIST = ['- الكل -','[R]']
			if any(value in title for value in ignoreLIST): continue
			if '/movies/' in url: title = '_MOD_' + 'افلام ' + title
			elif '/tv/' in url: title = '_MOD_' + 'مسلسلات ' + title
			addMenuItem('folder',menu_name+title,url,121)
	return

def TITLES(url,page):
	#XBMCGUI_DIALOG_OK(str(url), page)
	if '/explore/' in url or '?' in url: url2 = url + '&'
	else: url2 = url + '?'
	url2 = url2 + 'output_format=json&output_mode=movies_list&page='+page
	html = openURL_cached(REGULAR_CACHE,url2,'',headers,'','EGYBEST-TITLES-1st')
	name = ''
	found = False
	if '/season/' in url:
		name = re.findall('<h1>(.*?)<',html,re.DOTALL)
		if name: name = escapeUNICODE(name[0]).strip(' ') + ' - '
		else: name = xbmc.getInfoLabel( "ListItem.Label" ) + ' - '
		#XBMCGUI_DIALOG_OK(name, name)
	items = re.findall('n<a href=\\\\"(.*?)\\\\".*?src=\\\\"(.*?)\\\\".*?title\\\\">(.*?)<',html,re.DOTALL)
	for link,img,title in items:
		if '/series/' in url and '/season\/' not in link: continue
		if '/season/' in url and '/episode\/' not in link: continue
		title = name+escapeUNICODE(title).strip(' ')
		link = link.replace('\/','/')
		img = img.replace('\/','/')
		if 'http' not in img: img = 'http:'+img
		#XBMCGUI_DIALOG_NOTIFICATION(img,'')
		url2 = website0a+link
		if '/movie/' in url2 or '/episode/' in url2:
			addMenuItem('video',menu_name+title,url2.rstrip('/'),123,img)
			found = True
		else:
			addMenuItem('folder',menu_name+title,url2,122,img,'1')
			found = True
	if found:
		pagingLIST = ['/movies/','/tv/','/explore/','/trending/']
		page = int(page)
		if any(value in url for value in pagingLIST):
			for n in range(0,1000,100):
				if int(page/100)*100==n:
					for i in range(n,n+100,10):
						if int(page/10)*10==i:
							for j in range(i,i+10,1):
								if not page==j and j!=0:
									addMenuItem('folder',menu_name+'صفحة '+str(j),url,122,'',str(j))
						elif i!=0: addMenuItem('folder',menu_name+'صفحة '+str(i),url,122,'',str(i))
						else: addMenuItem('folder',menu_name+'صفحة '+str(1),url,122,'',str(1))
				elif n!=0: addMenuItem('folder',menu_name+'صفحة '+str(n),url,122,'',str(n))
				else: addMenuItem('folder',menu_name+'صفحة '+str(1),url,122,'','1')
	return

def PLAY(url):
	global headers
	#XBMCGUI_DIALOG_OK(url, url[-45:])
	html = openURL_cached(LONG_CACHE,url,'',headers,'','EGYBEST-PLAY-1st')
	ratingLIST = re.findall('<td>التصنيف</td>.*?">(.*?)<',html,re.DOTALL)
	if RATING_CHECK(script_name,url,ratingLIST): return
	"""
	html_blocks = re.findall('tbody(.*?)tbody',html,re.DOTALL)
	if not html_blocks:
		XBMCGUI_DIALOG_NOTIFICATION('خطأ من الموقع الاصلي','ملف الفيديو غير متوفر')
		return
	block = html_blocks[0]
	"""
	titleLIST,linkLIST = [],[]
	watchitem = re.findall('class="auto-size" src="(.*?)"',html,re.DOTALL)
	#XBMCGUI_DIALOG_OK(url2, str(html2))
	# https://vidstream.top/embed/o2RbrN9bqf/?vclid=44711370a2655b3f2d23487cb74c05e5347648e8bb9571dfa7c5d5e4zlllsCGMDslElsMaYXobviuROhYfamfMOhlsEslsWQUlslElsMOcSbzMykqapaqlsEslsxMcGlslElsOGsabiZusOxySMgOpEaucSxiSVGEBOlOouQzsEslsxWdlslElsmmmlRPMMslnfpaqlsEslsCMcGlslElsOEOEEZlEMOuzslh
	if watchitem:
		url2 = website0a+watchitem[0]#+'||MyProxyUrl=http://79.165.242.84:4145'
		server = SERVER(url2)
		#XBMCGUI_DIALOG_OK(server,'')
		response = openURL_requests_cached(SHORT_CACHE,'GET',url2,'','',True,'','EGYBEST-PLAY-2nd')
		#html2 = response.content
		#cookies = response.cookies.get_dict()
		#PHPSID = cookies['PHPSID']
		#XBMCGUI_DIALOG_OK(server, str(PHPSID))
		headers2 = headers
		#headers2['Cookie'] = 'PHPSID='+PHPSID
		response = openURL_requests_cached(SHORT_CACHE,'GET',url2,'',headers2,False,'','EGYBEST-PLAY-3rd')
		html2 = response.content
		#xbmc.log(html2, level=xbmc.LOGNOTICE)
		#XBMCGUI_DIALOG_OK(url2, str(html2.count('404')))
		items = re.findall('source src="(.*?)"',html2,re.DOTALL)
		#XBMCGUI_DIALOG_OK(url2, str(html2))
		#XBMCGUI_DIALOG_OK(url2, str(items))
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
	items = re.findall('</td> <td>(.*?)<.*?data-url="(.*?)".*?data-url="(.*?)"',html,re.DOTALL)
	for quality,link1,link2 in items:
		quality = quality.strip(' ').split(' ')[-1]
		url1 = website0a+link1 # + '&v=1'
		url2 = website0a+link2 # + '&v=1'
		#url = url+'?PHPSID='+PHPSID
		linkLIST.append(url1+'?named=vidstream__download__mp4__'+quality)
		linkLIST.append(url2+'?named=vidstream__watch__mp4__'+quality)
	#if not linkLIST:
	#	WARNING()
	#	return
	"""
	url = website0a + '/api?call=' + watchitem[0]
	EGUDI, EGUSID, EGUSS = GET_PLAY_TOKENS()
	if EGUDI=='': return
	headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
	response = openURL_requests_cached(SHORT_CACHE,'GET', url, '', headers, False,'','EGYBEST-PLAY-2nd')
	html = response.content
	#XBMCGUI_DIALOG_OK(url,html)
	items = re.findall('#EXT-X-STREAM.*?RESOLUTION=(.*?),.*?\n(.*?)\n',html,re.DOTALL)
	if items:
		for qualtiy,url in reversed(items):
			qualityLIST.append ('m3u8   '+qualtiy)
			datacallLIST.append (url)
	"""
	#selection = XBMCGUI_DIALOG_SELECT('اختر الفيديو المناسب:', linkLIST)
	#if selection == -1 : return
	#url = linkLIST[selection]
	"""
	if 'http' not in url:
		link = linkLIST[selection]
		url = website0a + '/api?call=' + link
		headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		response = openURL_requests_cached(SHORT_CACHE,'GET', url, '', headers, False,'','EGYBEST-PLAY-3rd')
		html = response.content
		#XBMCGUI_DIALOG_OK(url,html)
		#xbmc.log(html, level=xbmc.LOGNOTICE)
		items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		#link = items[0]

		#url = website0a + '/api?call=' + link
		#headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		#response = openURL_requests_cached(SHORT_CACHE,'GET', url, '', headers, False,'','EGYBEST-PLAY-4th')
		#html = response.content
		#xbmc.log(escapeUNICODE(html), level=xbmc.LOGNOTICE)
		#items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		url = items[0]

		#XBMCGUI_DIALOG_OK(url,html)
		#xbmc.log(html, level=xbmc.LOGNOTICE)
		#items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		#url = items[0]
	url = url.replace('\/','/')
	#xbmc.log(url, level=xbmc.LOGNOTICE)
	#XBMCGUI_DIALOG_OK(url,url[-45:])
	"""
	#WARNING() ; return
	#result = PLAY_VIDEO(url,script_name,'video')
	#if result!='playing': WARNING()
	#XBMCGUI_DIALOG_OK(url,'')
	import RESOLVERS
	RESOLVERS.PLAY(linkLIST,script_name,'video')
	return

def GET_USERNAME_PASSWORD():
	text = 'هذا الموقع يحتاج اسم دخول وكلمة السر لكي تستطيع تشغيل ملفات الفيديو. للحصول عليهم قم بفتح حساب مجاني من الموقع الاصلي'
	XBMCGUI_DIALOG_OK('الموقع الاصلي  '+website0a,text)
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

def GET_PLAY_TOKENS():
	settings = xbmcaddon.Addon(id=addon_id)
	EGUDI = settings.getSetting('egybest.EGUDI')
	EGUSID = settings.getSetting('egybest.EGUSID')
	EGUSS = settings.getSetting('egybest.EGUSS')
	username = mixARABIC(settings.getSetting('egybest.user'))
	password = mixARABIC(settings.getSetting('egybest.pass'))
	#XBMCGUI_DIALOG_OK(username,password)
	if username=='' or password=='':
		settings.setSetting('egybest.EGUDI','')
		settings.setSetting('egybest.EGUSID','')
		settings.setSetting('egybest.EGUSS','')
		GET_USERNAME_PASSWORD()
		return ['','','']

	if EGUDI!='':
		headers = { 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		response = openURL_requests_cached(SHORT_CACHE,'GET', website0a, '', headers, False,'','EGYBEST-GET_PLAY_TOKENS-1st')
		register = re.findall('ssl.egexa.com\/register',response.content,re.DOTALL)
		if register:
			settings.setSetting('egybest.EGUDI','')
			settings.setSetting('egybest.EGUSID','')
			settings.setSetting('egybest.EGUSS','')
		else:
			#XBMCGUI_DIALOG_OK('no new login needed, you were already logged in','')
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
	response = openURL_requests_cached(SHORT_CACHE,'POST', url, payload, headers, False,'','EGYBEST-GET_PLAY_TOKENS-2nd')
	cookies = response.cookies.get_dict()
	#xbmc.log(response.content, level=xbmc.LOGNOTICE)

	if '"action":"captcha"' in response.content:
		XBMCGUI_DIALOG_OK('مشكلة جدا مزعجة تخص جهازك فقط','موقع ايجي بيست يرفض دخولك اليهم بإستخدام كودي ... حاول فصل الانترنيت واعادة ربطها لتحصل على عنوان IP جديد ... او اعد المحاولة بعد عدة ايام او عدة اسابيع')
		return ['','','']

	if len(cookies)<3:
		XBMCGUI_DIALOG_OK('مشكلة في تسجيل الدخول للموقع','حاول اصلاح اسم الدخول وكلمة السر لكي تتمكن من تشغيل الفيديو بصورة صحيحة')
		GET_USERNAME_PASSWORD()
		return ['','','']

	EGUDI = cookies['EGUDI']
	EGUSID = cookies['EGUSID']
	EGUSS = cookies['EGUSS']
	time.sleep(1)
	url = "https://ssl.egexa.com/finish/"
	headers = { 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
	response = openURL_requests_cached(SHORT_CACHE,'GET', url, '', headers, True,'','EGYBEST-GET_PLAY_TOKENS-3rd')
	cookies = response.cookies.get_dict()
	#XBMCGUI_DIALOG_OK(str(response.content),str(cookies))
	EGUDI = cookies['EGUDI']
	EGUSID = cookies['EGUSID']
	EGUSS = cookies['EGUSS']
	settings.setSetting('egybest.EGUDI',EGUDI)
	settings.setSetting('egybest.EGUSID',EGUSID)
	settings.setSetting('egybest.EGUSS',EGUSS)
	#XBMCGUI_DIALOG_OK('success, you just logged in now','')
	return [ EGUDI, EGUSID, EGUSS ]

def WARNING():
	XBMCGUI_DIALOG_OK('https://egy.best','هذا الموقع هو موقع ايجي بيست الاصلي وهو قيد الانشاء ولهذا تقريبا جميع الفيدوهات لا تعمل')
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	new_search = search.replace(' ','+')
	url = website0a + '/explore/?q=' + new_search
	TITLES(url,'1')
	return




