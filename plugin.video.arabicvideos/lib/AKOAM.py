# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'https://akoam.net'
headers = { 'User-Agent' : '' }
script_name='AKOAM'
menu_name='[COLOR FFC89008]AKM [/COLOR]'
noEpisodesLIST = ['فيلم','كليب','العرض الاسبوعي','مسرحية','مسرحيه','اغنية','اعلان','لقاء']

def MAIN(mode,url,text):
	if mode==70: MENU()
	elif mode==71: CATEGORIES(url)
	elif mode==72: TITLES(url,text)
	elif mode==73: EPISODES(url)
	elif mode==74: PLAY(url)
	elif mode==79: SEARCH(text)
	return

def MENU():
	#from requests import request as requests_request
	#response = requests_request('GET', 'https://akoam.net', headers='', data='', allow_redirects=False)
	#website0a = response.headers['Location']
	#website0a = website0a.strip('/')
	#xbmcgui.Dialog().ok(website0a,'')
	addDir(menu_name+'بحث في الموقع','',79)
	addDir(menu_name+'المميزة',website0a,72,'','','featured')
	addDir(menu_name+'المزيد',website0a,72,'','','more')
	#addDir(menu_name+'الاخبار',website0a,72,'','','news')
	ignoreLIST = ['الكتب و الابحاث','الكورسات التعليمية','الألعاب','البرامج','الاجهزة اللوحية','الصور و الخلفيات']
	html = openURL(website0a,'',headers,'','AKOAM-MENU-1st')
	html_blocks = re.findall('big_parts_menu(.*?)main_partions',html,re.DOTALL)
	#if not html_blocks:
	#	xbmc.sleep(2000)
	#	html = openURL(website0a,'',headers,'','AKOAM-MENU-2nd')
	#	html_blocks = re.findall('big_parts_menu(.*?)main_partions',html,re.DOTALL)
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		if title not in ignoreLIST:
			addDir(menu_name+title,link,71)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def CATEGORIES(url):
	html = openURL(url,'',headers,'','AKOAM-CATEGORIES-1st')
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
	html = openURL(url,'',headers,'','AKOAM-TITLES-1st')
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
		items = re.findall('<li >.*?href=\'(.*?)\'>(.*?)<',block,re.DOTALL)
		for link,title in items:
			addDir(menu_name+'صفحة '+title,link,72)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def EPISODES(url):
	notvideosLIST = ['zip','rar','txt','pdf','htm','tar','iso','html']
	html = openURL(url,'',headers,'','AKOAM-EPISODES-1st')
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
	if not items:
		items = [ ('رابط التشغيل','') ]
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
	if len(titleLIST)>0:
		if any(value in name for value in noEpisodesLIST):
			if len(titleLIST)==1:
				selection = 0
			else:
				selection = xbmcgui.Dialog().select('اختر الفيديو المناسب:', titleLIST)
				if selection == -1: return
			PLAY(url+'?ep='+str(episodeLIST[selection]+1))
		else:
			for i in range(0,len(titleLIST)):
				#if ':' in titleLIST[i]: title = titleLIST[i].strip(':') + ' - ملف الفيديو غير موجود'
				#else: title = name + ' - ' + titleLIST[i]
				title = name + ' - ' + titleLIST[i]
				link = url + '?ep='+str(size-i)
				addLink(menu_name+title,link,74,img)
			xbmcplugin.endOfDirectory(addon_handle)
	else:
		addLink(menu_name+'الرابط ليس فيديو','',9999,img)
		#xbmcgui.Dialog().notification('خطأ خارجي','الرابط ليس فيديو')
		xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	import xbmcaddon
	settings = xbmcaddon.Addon(id=addon_id)
	previous_url = settings.getSetting('previous.url')
	if url==previous_url:
		linkLIST = settings.getSetting('previous.linkLIST')
		linkLIST = linkLIST[1:-1].replace('&apos;','').replace(' ','').replace("'",'')
		linkLIST = linkLIST.split(',')
		#xbmcgui.Dialog().ok(url,str(linkLIST))
	else:
		url2,episode = url.split('?ep=')
		html = openURL(url2,'',headers,'','AKOAM-PLAY-1st')
		html_blocks = re.findall('ad-300-250.*?ad-300-250(.*?)ako-feedback',html,re.DOTALL)
		html_block = html_blocks[0].replace('\'direct_link_box','"direct_link_box epsoide_box')
		html_block = html_block + 'direct_link_box'
		blocks = re.findall('epsoide_box(.*?)direct_link_box',html_block,re.DOTALL)
		episode = len(blocks)-int(episode)
		block = blocks[episode]
		linkLIST = []
		serversDICT = {'1423075862':'dailymotion','1477487601':'estream','1505328404':'streamango',
			'1423080015':'flashx','1458117295':'openload','1423079306':'vimple','1430052371':'ok.ru',
			'1477488213':'thevid','1558278006':'uqload'}
		items = re.findall('download_btn\' target=\'_blank\' href=\'(.*?)\'',block,re.DOTALL)
		for link in items:
			linkLIST.append(link)
		items = re.findall('background-image: url\((.*?)\).*?href=\'(.*?)\'',block,re.DOTALL)
		for serverIMG,link in items:
			serverIMG = serverIMG.split('/')[-1]
			serverIMG = serverIMG.split('.')[0]
			try: linkLIST.append(link+'?name='+serversDICT[serverIMG])
			except: linkLIST.append(link+'?name='+serverIMG)
		settings.setSetting('previous.url',url)
		settings.setSetting('previous.linkLIST',str(linkLIST))
	if len(linkLIST)==0:
		message = re.findall('sub-no-file.*?\n(.*?)\n',block,re.DOTALL)
		if message: xbmcgui.Dialog().ok('رسالة من الموقع الاصلي',message[0])
		else: xbmcgui.Dialog().ok('No video file found','لا يوجد ملف فيديو')
	else:
		from RESOLVERS import PLAY as RESOLVERS_PLAY
		RESOLVERS_PLAY(linkLIST,script_name)
	return ''

def SEARCH(search):
	#from requests import request as requests_request
	#response = requests_request('GET', 'https://akoam.net', headers='', data='', allow_redirects=False)
	#website0a = response.headers['Location']
	#website0a = website0a.strip('/')
	if search=='': search = KEYBOARD()
	if search == '': return
	new_search = search.replace(' ','%20')
	#xbmcgui.Dialog().ok(str(len(search)) , str(len(new_search)) )
	url = website0a + '/search/' + new_search
	TITLES(url,'search')
	return


