# -*- coding: utf-8 -*-
from LIBRARY import *

headers = { 'User-Agent' : '' }
script_name='AKOAM'
menu_name='_AKO_'
website0a = WEBSITES[script_name][0]
noEpisodesLIST = ['فيلم','كليب','العرض الاسبوعي','مسرحية','مسرحيه','اغنية','اعلان','لقاء']
#proxy = '||MyProxyUrl=https://159.203.87.130:3128'
proxy = '||MyProxyUrl='+PROXIES[6][1]
proxy = ''

def MAIN(mode,url,text):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==70: MENU()
	elif mode==71: CATEGORIES(url+proxy)
	elif mode==72: TITLES(url+proxy,text)
	elif mode==73: SECTIONS(url+proxy)
	elif mode==74: PLAY(url+proxy)
	elif mode==79: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',79)
	addDir(menu_name+'المميزة',website0a+proxy,72,'','','featured')
	addDir(menu_name+'المزيد',website0a+proxy,72,'','','more')
	#addDir(menu_name+'الاخبار',website0a+proxy,72,'','','news')
	ignoreLIST = ['الكتب و الابحاث','الكورسات التعليمية','الألعاب','البرامج','الاجهزة اللوحية','الصور و الخلفيات','المصارعة الحرة']
	html = openURL_cached(LONG_CACHE,website0a+proxy,'',headers,'','AKOAM-MENU-1st')
	html_blocks = re.findall('big_parts_menu(.*?)main_partions',html,re.DOTALL)
	#xbmcgui.Dialog().textviewer('',html)
	#if not html_blocks:
	#	xbmc.sleep(2000)
	#	html = openURL_cached(NO_CACHE,website0a+proxy,'',headers,'','AKOAM-MENU-2nd')
	#	html_blocks = re.findall('big_parts_menu(.*?)main_partions',html,re.DOTALL)
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title not in ignoreLIST:
				addDir(menu_name+title,link,71)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def CATEGORIES(url):
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','AKOAM-CATEGORIES-1st')
	html_blocks = re.findall('sect_parts(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			title = title.strip(' ')
			addDir(menu_name+title,link,72)
		addDir(menu_name+'جميع الفروع',url,72)
		xbmcplugin.endOfDirectory(addon_handle)
	else: TITLES(url,'')
	return

def TITLES(url,type):
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','AKOAM-TITLES-1st')
	items = []
	if type=='featured':
		html_blocks = re.findall('section_title featured_title(.*?)subjects-crousel',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)"><div class="subject_box.*?src="(.*?)".*?<h3.*?>(.*?)</h3>',block,re.DOTALL)
	elif type=='search':
		html_blocks = re.findall('akoam_result(.*?)<script',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?background-image: url\((.*?)\).*?<h1>(.*?)</h1>',block,re.DOTALL)
	elif type=='more':
		html_blocks = re.findall('section_title more_title(.*?)footer_bottom_services',html,re.DOTALL)
	#elif type=='news':
	#	html_blocks = re.findall('section_title news_title(.*?)news_more_choices',html,re.DOTALL)
	else:
		html_blocks = re.findall('navigation(.*?)<script',html,re.DOTALL)
	if not items and html_blocks:
		block = html_blocks[0]
		items = re.findall('div class="subject_box.*?href="(.*?)".*?src="(.*?)".*?<h3.*?>(.*?)</h3>',block,re.DOTALL)
	for link,img,title in items:
		title = title.strip(' ').replace('\t','').replace('\n','')
		title = unescapeHTML(title)
		if any(value in title for value in noEpisodesLIST):
			addLink(menu_name+title,link,73,img)
		else: 
			addDir(menu_name+title,link,73,img)
	html_blocks = re.findall('pagination(.*?)</div',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall("<li>.*?href='(.*?)'>(.*?)<",block,re.DOTALL)
		for link,title in items:
			addDir(menu_name+'صفحة '+title,link,72)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def SECTIONS(url):
	notvideosLIST = ['zip','rar','txt','pdf','htm','tar','iso','html']
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','AKOAM-SECTIONS-1st')
	if 'التصميم الجديد من هنا' in html or 'للموقع الجديد من هنا' in html:
		url3 = re.findall('<br />.*?<a href="(http.*?akwam.*?)"',html,re.DOTALL)
		url3 = unquote(url3[0])
		#xbmcgui.Dialog().ok(url3,'SECTIONS')
		import AKWAM
		if '/series/' in url3: AKWAM.EPISODES(url3)
		else: AKWAM.PLAY(url3)
		return
	rating = re.findall('محتوى الفيلم.*?>.*?(\w*?)\W*?<',html,re.DOTALL)
	#xbmcgui.Dialog().ok(rating[0],'')
	if rating:
		if rating[0] in BLOCKED_VIDEOS:
			LOG_THIS('ERROR',LOGGING(script_name)+'   Adult video   URL: [ '+url+' ]')
			xbmcgui.Dialog().notification('رسالة من المبرمج','الفيديو للكبار فقط وأنا منعته')
			return
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	#xbmcgui.Dialog().ok(url,html)
	items = re.findall('<br />\n<a href="(.*?)".*?<span style="color:.*?">(.*?)</span>',html,re.DOTALL)
	for link,title in items:
		title = unescapeHTML(title)
		addDir(menu_name+title,link,73)
	html_blocks = re.findall('class="sub_title".*?<h1.*?>(.*?)</h1>.*?class="main_img".*?src="(.*?)".*?ad-300-250(.*?)ako-feedback',html,re.DOTALL)
	if not html_blocks:
		xbmcgui.Dialog().notification('خطأ خارجي','لا يوجد ملف فيديو')
		return
	name,img,block = html_blocks[0]
	name = name.replace('\n','').replace('\t','').strip(' ')
	if 'sub_epsiode_title' in block:
		items = re.findall('sub_epsiode_title">(.*?)</h2>.*?sub_file_title.*?>(.*?)<',block,re.DOTALL)
	else:
		filenames = re.findall('sub_file_title\'>(.*?) - <i>',block,re.DOTALL)
		items = []
		for filename in filenames:
			items.append( ('رابط التشغيل',filename) )
	if not items: items = [ ('رابط التشغيل','') ]
	count = 0
	titleLIST,episodeLIST = [],[]
	size = len(items)
	for title,filename in items:
		filetype = ''
		if ' - ' in filename: filename = filename.split(' - ')[0]
		else: filename = 'dummy.zip'
		if '.' in filename: filetype = filename.split('.')[-1]
		#if any(value in filetype for value in notvideosLIST):
		#	if 'رابط التشغيل' not in title: title = title + ':'
		title = title.replace('\n','').strip(' ')
		titleLIST.append(title)
		episodeLIST.append(count)
		count += 1
	#xbmcgui.Dialog().ok(str(size),str(episodeLIST))
	if size>0:
		if any(value in name for value in noEpisodesLIST):
			if size==1:
				selection = 0
			else:
				#xbmcgui.Dialog().select('',titleLIST)
				selection = xbmcgui.Dialog().select('اختر الفيديو المناسب:', titleLIST)
				if selection == -1: return
			PLAY(url+'?section='+str(1+episodeLIST[size-selection-1]))
		else:
			for i in reversed(range(size)):
				#if ':' in titleLIST[i]: title = titleLIST[i].strip(':') + ' - ملف الفيديو غير موجود'
				#else: title = name + ' - ' + titleLIST[i]
				title = name + ' - ' + titleLIST[i]
				link = url + '?section='+str(size-i)
				addLink(menu_name+title,link,74,img)
			xbmcplugin.endOfDirectory(addon_handle)
	else:
		addLink(menu_name+'الرابط ليس فيديو','',9999,img)
		#xbmcgui.Dialog().notification('خطأ خارجي','الرابط ليس فيديو')
		xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	#xbmcgui.Dialog().ok(url,'')
	url2,episode = url.split('?section=')
	html = openURL_cached(REGULAR_CACHE,url2,'',headers,'','AKOAM-PLAY_AKOAM-1st')
	html_blocks = re.findall('ad-300-250.*?ad-300-250(.*?)ako-feedback',html,re.DOTALL)
	html_block = html_blocks[0].replace('\'direct_link_box','"direct_link_box epsoide_box')
	html_block = html_block + 'direct_link_box'
	blocks = re.findall('epsoide_box(.*?)direct_link_box',html_block,re.DOTALL)
	episode = len(blocks)-int(episode)
	block = blocks[episode]
	linkLIST = []
	serversDICT = {'1423075862':'dailymotion','1477487601':'estream','1505328404':'streamango',
		'1423080015':'flashx','1458117295':'openload','1423079306':'vimple','1430052371':'ok.ru',
		'1477488213':'thevid','1558278006':'uqload','1477487990':'vidtodo'}
	items = re.findall('download_btn\' target=\'_blank\' href=\'(.*?)\'',block,re.DOTALL)
	for link in items:
		linkLIST.append(link)
	items = re.findall('background-image: url\((.*?)\).*?href=\'(.*?)\'',block,re.DOTALL)
	for serverIMG,link in items:
		serverIMG = serverIMG.split('/')[-1]
		serverIMG = serverIMG.split('.')[0]
		if serverIMG in serversDICT:
			linkLIST.append(link+'?name='+serversDICT[serverIMG])
		else: linkLIST.append(link+'?name='+serverIMG)
	if len(linkLIST)==0:
		message = re.findall('sub-no-file.*?\n(.*?)\n',block,re.DOTALL)
		if message: xbmcgui.Dialog().ok('رسالة من الموقع الاصلي',message[0])
		else: xbmcgui.Dialog().ok('No video file found','لا يوجد ملف فيديو')
	else:
		#xbmcgui.Dialog().select('',linkLIST)
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name)
		return
	return

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search == '': return
	new_search = search.replace(' ','%20')
	#xbmcgui.Dialog().ok(str(len(search)) , str(len(new_search)) )
	url = website0a + '/search/' + new_search + proxy
	TITLES(url,'search')
	return



