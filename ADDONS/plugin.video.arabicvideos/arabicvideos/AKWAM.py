# -*- coding: utf-8 -*-
from LIBRARY import *

headers = { 'User-Agent' : '' }
script_name='AKWAM'
menu_name='_AKW_'
website0a = WEBSITES[script_name][0]
#noEpisodesLIST = ['فيلم','كليب','العرض الاسبوعي','مسرحية','مسرحيه','اغنية','اعلان','لقاء']
#notvideosLIST = ['zip','rar','txt','pdf','htm','tar','iso','html']
#ignoreLIST = ['الكتب و الابحاث','الكورسات التعليمية','الألعاب','البرامج','الاجهزة اللوحية','الصور و الخلفيات']
#proxy = '||MyProxyUrl=https://159.203.87.130:3128'
#proxy = '||MyProxyUrl='+PROXIES[6][1]
proxy = ''

def MAIN(mode,url,text):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==240: MENU()
	elif mode==241: TITLES(url+proxy,text)
	elif mode==242: EPISODES(url+proxy)
	elif mode==243: PLAY(url+proxy)
	elif mode==249: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',249)
	addDir(menu_name+'المميزة',website0a+proxy,241,'','','featured')
	#addDir(menu_name+'المزيد',website0a+proxy,242,'','','more')
	#addDir(menu_name+'الاخبار',website0a+proxy,242,'','','news')
	html = openURL_cached(LONG_CACHE,website0a+proxy,'',headers,'','AKWAM-MENU-1st')
	html_blocks = re.findall('class="menu(.*?)<nav',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?text">(.*?)<',block,re.DOTALL)
		ignoreLIST = ['ألعاب','برامج','منوعات']
		for link,title in items:
			if title not in ignoreLIST:
				addDir(menu_name+title,link,241)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url,type=''):
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','AKWAM-TITLES-1st')
	if type=='featured':
		html_blocks = re.findall('swiper-container(.*?)swiper-button-prev',html,re.DOTALL)
	else:
		html_blocks = re.findall('class="widget"(.*?)</div>.. *?</div>.. *?</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('src="(.*?)".*?href="(.*?)".*?text-white">(.*?)<',block,re.DOTALL)
		for img,link,title in items:
			if '/series/' in link or '/shows/' in link:
				addDir(menu_name+title,link,242,img)
			else: addLink(menu_name+title,link,243,img)
	html_blocks = re.findall('pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title=='&lsaquo;': title = 'سابقة'
			if title=='&rsaquo;': title = 'لاحقة'
			#title = unescapeHTML(title)
			addDir(menu_name+'صفحة '+title,link,241)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def SEARCH(search):
	# https://akwam.net/search?q=%D8%A8%D8%AD%D8%AB
	if search=='': search = KEYBOARD()
	if search == '': return
	new_search = search.replace(' ','%20')
	#xbmcgui.Dialog().ok(str(len(search)) , str(len(new_search)) )
	url = website0a + '/search?q=' + new_search + proxy
	TITLES(url)
	return

def EPISODES(url):
	#xbmcgui.Dialog().ok(url,'EPISODES_AKWAM')
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','AKWAM-EPISODES-1st')
	if '-episodes' not in html:
		img = xbmc.getInfoLabel('ListItem.Icon')
		addLink(menu_name+'رابط التشغيل',url,243,img)
	else:
		html_blocks = re.findall('-episodes">(.*?)col-lg-8',html,re.DOTALL)
		block = html_blocks[0]
		episodes = re.findall('href="(.*?)".*?>(.*?)<.*?src="(.*?)"',block,re.DOTALL)
		for link,title,img in episodes:
			if 'الحلقات' in title: continue
			addLink(menu_name+title,link,243,img)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	#xbmcgui.Dialog().ok(url,'PLAY')
	html = openURL_cached(LONG_CACHE,url,'','','','AKWAM-PLAY-1st')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	#with open('S:\\emad.html', 'w') as f: f.write(html)
	rating = re.findall('class="badge.*?>.*?(\w*).*?<',html,re.DOTALL)
	#xbmcgui.Dialog().ok(rating[0],'')
	if rating:
		if rating[0] in BLOCKED_VIDEOS:
			LOG_THIS('ERROR',LOGGING(script_name)+'   Adult video   URL: [ '+url+' ]')
			xbmcgui.Dialog().notification('قم بتشغيل فيديو غيره','هذا الفيديو للكبار فقط ولا يعمل هنا')
			return
	buttons = re.findall('li><a href="#(.*?)".*?>(.*?)<',html,re.DOTALL)
	buttonLIST,qualityLIST = zip(*buttons)
	if not buttonLIST: return
	linkLIST,titleLIST = [],[]
	for i in range(len(buttonLIST)):
		button = buttonLIST[i]
		quality = qualityLIST[i]
		#xbmcgui.Dialog().ok(quality,button)
		html_blocks = re.findall('tab-content" id="'+button+'"(.*?)</a>.. *?</div>.. *?</div>',html,re.DOTALL)
		block = html_blocks[0]
		links = re.findall('href="(.*?)".*?icon-(.*?)"',block,re.DOTALL)
		for link,icon in links:
			if 'torrent' in icon: continue
			elif 'download' in icon: type = 'تحميل'
			elif 'play' in icon: type = 'مشاهدة'
			else: type = 'غير معروف'
			title = quality+' ملف '+type
			titleLIST.append(title)
			linkLIST.append(link)
	#selection = xbmcgui.Dialog().select('',linkLIST)
	selection = xbmcgui.Dialog().select('',titleLIST)
	if selection==-1: return
	link = linkLIST[selection]
	title = titleLIST[selection]
	html2 = openURL_cached(LONG_CACHE,link,'',headers,'','AKWAM-PLAY-2nd')
	url2 = re.findall('class="content.*?href="(.*?)"',html2,re.DOTALL)
	url2 = unquote(url2[0])
	url3 = ''
	if 'تحميل' in title:
		html3 = openURL_cached(REGULAR_CACHE,url2,'',headers,'','AKWAM-PLAY-3rd')
		url3 = re.findall('btn-loader.*?href="(.*?)"',html3,re.DOTALL)
		url3 = unquote(url3[0])
	if 'مشاهدة' in title:
		html4 = openURL_cached(REGULAR_CACHE,url2,'',headers,'','AKWAM-PLAY-4th')
		links = re.findall('source\n *?src="(.*?)".*?size="(.*?)"',html4,re.DOTALL)
		for link,size in links:
			if size in title:
				url3 = link
				break
		if url3=='':
			linkLIST,titleLIST = [],[]
			for link,size in links:
				titleLIST.append(size)
				linkLIST.append(link)
			selection = xbmcgui.Dialog().select('',titleLIST)
			if selection==-1: return
			url3 = linkLIST[selection]
	if url3=='': xbmcgui.Dialog().ok('','لا يوجد ملف تشغيل لهذا الفيديو')
	else: PLAY_VIDEO(url3,script_name,'yes')
	return


