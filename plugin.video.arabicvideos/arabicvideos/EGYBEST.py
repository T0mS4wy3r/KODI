# -*- coding: utf-8 -*-
from LIBRARY import *
import requests

website0a = 'https://egy1.best'
headers = { 'User-Agent' : '' }
script_name = 'EGYBEST'
menu_name='_EGB_'

def MAIN(mode,url,page,text):
	if   mode==120: MAIN_MENU()
	elif mode==121: FILTERS_MENU(url)
	elif mode==122: TITLES(url,page)
	elif mode==123: PLAY(url)
	elif mode==125: GET_USERNAME_PASSWORD()
	elif mode==129: SEARCH(text)
	return

def MAIN_MENU():
	addDir(menu_name+'اضغط هنا لاضافة اسم دخول وكلمة السر','',125)
	addDir(menu_name+'بحث في الموقع','',129)
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','EGYBEST-MAIN_MENU-1st')
	#xbmcgui.Dialog().ok(website0a, html)
	html_blocks=re.findall('id="menu"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('<a href="(https://egy1.best/.*?)".*?></i>(.*?)<',block,re.DOTALL)
	for url,title in reversed(items):
		if '/my/' not in url:
			addDir(menu_name+title,website0a+url,121)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def FILTERS_MENU(link):
	filter = link.split('/')[-1]
	if '/movies/' in link:
		if filter=='': filter = 'new'
		elif not any(value in filter for value in ['latest','top','popular']): filter = 'new-'+filter
	elif '/tv/' in link:
		if filter=='': filter = 'latest'
		elif not any(value in filter for value in ['new','top','popular']): filter = 'latest-'+filter
	filter = filter.replace('-',' + ')
	#xbmcgui.Dialog().ok(str(link), str(filter))
	if '/trending/' not in link:
		addDir(menu_name+'اظهار قائمة الفيديو التي تم اختيارها',link,122,'','1')
		addDir(menu_name+'[[   ' + filter + '   ]]',link,122,'','1')
		addDir(menu_name+'===========================',link,9999)
	html = openURL_cached(REGULAR_CACHE,link,'',headers,'','EGYBEST-FILTERS_MENU-1st')
	html_blocks=re.findall('mainLoad(.*?)</div></div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items=re.findall('href="(.*?)".*?</i> (.*?)<',block,re.DOTALL)
		for url,title in items:
			if '/movies/' in url and 'فلام' not in title: title = 'افلام ' + title
			elif '/tv/' in url and 'مسلسل' not in title: title = 'مسلسلات ' + title
			if '/trending/' in url:
				title = 'الاكثر مشاهدة ' + title
				addDir(menu_name+title,website0a+url,122,'','1')
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
	html_blocks=re.findall('sub_nav(.*?)</div></div></div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for url,title in items:
			ignoreLIST = ['- الكل -','[R]']
			if any(value in title for value in ignoreLIST): continue
			if '/movies/' in url: title = 'افلام ' + title
			elif '/tv/' in url: title = 'مسلسلات ' + title
			addDir(menu_name+title,website0a+url,121)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url,page):
	#xbmcgui.Dialog().ok(str(url), page)
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
		#xbmcgui.Dialog().ok(name, name)
	items = re.findall('n<a href=\\\\"(.*?)\\\\".*?src=\\\\"(.*?)\\\\".*?title\\\\">(.*?)<',html,re.DOTALL)
	for link,img,title in items:
		if '/series/' in url and '/season\/' not in link: continue
		if '/season/' in url and '/episode\/' not in link: continue
		title = name + escapeUNICODE(title).strip(' ')
		title = title.replace('\n','')
		link = link.replace('\/','/')
		img = img.replace('\/','/')
		if 'http' not in img: img = 'http:' + img
		#xbmcgui.Dialog().notification(img,'')
		url2 = website0a + link
		if '/movie/' in url2 or '/episode/' in url2:
			addLink(menu_name+title,url2.rstrip('/'),123,img)
			found = True
		else:
			addDir(menu_name+title,url2,122,img,'1')
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
									addDir(menu_name+'صفحة '+str(j),url,122,'',str(j))
						elif i!=0: addDir(menu_name+'صفحة '+str(i),url,122,'',str(i))
						else: addDir(menu_name+'صفحة '+str(1),url,122,'',str(1))
				elif n!=0: addDir(menu_name+'صفحة '+str(n),url,122,'',str(n))
				else: addDir(menu_name+'صفحة '+str(1),url,122,'','1')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	#xbmcgui.Dialog().ok(url, url[-45:])
	headers = { 'User-Agent' : '' }
	html = openURL_cached(LONG_CACHE,url,'',headers,'','EGYBEST-PLAY-1st')
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
	response = requests.request('GET', url, headers=headers, allow_redirects=False)
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
		response = requests.request('GET', url, headers=headers, allow_redirects=False)
		html = response.text
		#xbmcgui.Dialog().ok(url,html)
		#xbmc.log(html, level=xbmc.LOGNOTICE)
		items = re.findall('"url":"(.*?)"',html,re.DOTALL)
		#datacall = items[0]

		#url = website0a + '/api?call=' + datacall
		#headers = { 'User-Agent':'Googlebot/2.1 (+http)', 'Referer':website0a, 'Cookie':'EGUDI='+EGUDI+'; EGUSID='+EGUSID+'; EGUSS='+EGUSS }
		#response = requests.request('GET', url, headers=headers, allow_redirects=False)
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

def GET_USERNAME_PASSWORD():
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

def GET_PLAY_TOKENS():
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
		response = requests.request('GET', website0a, headers=headers, allow_redirects=False)
		register = re.findall('ssl.egexa.com\/register',response.text,re.DOTALL)
		if register:
			settings.setSetting('egybest.EGUDI','')
			settings.setSetting('egybest.EGUSID','')
			settings.setSetting('egybest.EGUSS','')
		else:
			#xbmcgui.Dialog().ok('no new login needed, you were already logged in','')
			return [ EGUDI, EGUSID, EGUSS ]

	import random
	import string
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
	response = requests.request('POST', url, data=payload, headers=headers, allow_redirects=False)
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
	response = requests.request('GET', url, headers=headers, allow_redirects=True)
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

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search == '': return
	new_search = search.replace(' ','+')
	url = website0a + '/explore/?q=' + new_search
	TITLES(url,'1')
	return




