# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'https://www.youtube.com'
script_name='YOUTUBE'
menu_name='_YUT_'

def MAIN(mode,url,text):
	result = ''
	if mode==140: MENU()
	elif mode==141: TITLES(url)
	elif mode==142: PLAYLIST_ITEMS(url)
	elif mode==143: result = PLAY(url)
	elif mode==144: SETTINGS()
	elif mode==145: CHANNEL_MENU(url)
	elif mode==146: CHANNEL_ITEMS(url)
	elif mode==149: SEARCH(text)
	"""
	import xbmcaddon
	settings = xbmcaddon.Addon(id=addon_id)
	previous_url = settings.getSetting('previous.url')
	previous_linkLIST = settings.getSetting('previous.linkLIST')
	yes = True
	if previous_linkLIST!='executed':
		yes = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','هذا الاختيار سوف يخرجك من البرنامج','لأنه سوف يقوم بتشغيل برنامج يوتيوب')
		if yes:
			settings.setSetting('previous.linkLIST','executed')
			xbmc.executebuiltin('Dialog.Close(busydialog)')
			if mode==140: MENU()
			elif mode==149: SEARCH(text)
	if mode==140: MENU()
	elif mode==149: SEARCH(text)
	if previous_url=='youtube' and previous_linkLIST=='executed':
		settings.setSetting('previous.url','')
		settings.setSetting('previous.linkLIST','')
	elif yes: settings.setSetting('previous.url','youtube')
	"""
	return result

def MENU():
	addDir(menu_name+'بحث في الموقع','',149)
	addDir(menu_name+'مسلسلات عربية','https://www.youtube.com/results?search_query=مسلسل&sp=EgIQAw%253D%253D',141)
	addDir(menu_name+'افلام عربية','https://www.youtube.com/results?search_query=فيلم',141)
	addDir(menu_name+'مسرحيات عربية','https://www.youtube.com/results?search_query=مسرحية',141)
	addDir(menu_name+'مسلسلات اجنبية','https://www.youtube.com/results?search_query=series&sp=EgIQAw%253D%253D',141)
	addDir(menu_name+'افلام اجنبية','https://www.youtube.com/results?search_query=movie',141)
	addDir(menu_name+'مسلسلات كارتون','https://www.youtube.com/results?search_query=كارتون&sp=EgIQAw%253D%253D',141)
	#addDir(menu_name+'اعدادات اضافة يوتيوب','',144)
	xbmcplugin.endOfDirectory(addon_handle)
	#yes = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','هذا الاختيار سوف يخرجك من البرنامج','لأنه سوف يقوم بتشغيل برنامج يوتيوب')
	#if yes:
	#	url = 'plugin://plugin.video.youtube'
	#	xbmc.executebuiltin('Dialog.Close(busydialog)')
	#	xbmc.executebuiltin('ReplaceWindow(videos,'+url+')')
	#	#xbmc.executebuiltin('RunAddon(plugin.video.youtube)')
	return

def PLAY(url):
	#url = url+'&'
	#items = re.findall('v=(.*?)&',url,re.DOTALL)
	#id = items[0]
	#xbmcgui.Dialog().ok(url,'')
	#link = 'plugin://plugin.video.youtube/play/?video_id='+id
	#PLAY_VIDEO(link,script_name)
	linkLIST = [url]
	from RESOLVERS import PLAY as RESOLVERS_PLAY
	result = RESOLVERS_PLAY(linkLIST,script_name)
	return result

def PLAYLIST_ITEMS(url):
	if 'browse_ajax' in url:
		html = openURL(url,'','','','YOUTUBE-PLAYLIST_ITEMS-1st')
		html = CLEAN_AJAX(html)
		html_blocks = [html]
	else:
		id = url.split('list=')[1]
		url2 = website0a+'/playlist?list='+id
		html = openURL(url2,'','','','YOUTUBE-PLAYLIST_ITEMS-2nd')
		html_blocks = re.findall('class="pl-video-table(.*?)footer-container',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,url)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('data-title="(.*?)".*?href="(.*?)".*?data-thumb="(.*?)"',block,re.DOTALL)
		for title,link,img in items:
			title = title.replace('\n','')
			title = unescapeHTML(title)
			link = website0a+link
			addLink(menu_name+title,link,143,img)
		html_blocks = re.findall('items-load-more-button(.*?)load-more-loading',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('href="(.*?)"',block,re.DOTALL)
			for link in items:
				addDir(menu_name+'صفحة اخرى',website0a+link,142)
		xbmcplugin.endOfDirectory(addon_handle)
	else: PLAYLIST_ITEMS_PLAYER(url)
	return

def PLAYLIST_ITEMS_PLAYER(url):
	#xbmcgui.Dialog().ok(url,'')
	html = openURL(url,'','','','YOUTUBE-PLAYLIST_ITEMS_PLAYER-1st')
	html_blocks = re.findall('playlist-videos-container(.*?)watch7-container',html,re.DOTALL)
	block = html_blocks[0]
	items1 = re.findall('data-video-title="(.*?)".*?href="(.*?)"',block,re.DOTALL)
	items2 = re.findall('data-thumbnail-url="(.*?)"',block,re.DOTALL)
	#xbmcgui.Dialog().ok(str(len(items1)),str(len(items2)))
	i = 0
	for title,link in items1:
		title = title.replace('\n','')
		title = unescapeHTML(title)
		img = items2[i]
		link = website0a+link
		addLink(menu_name+title,link,143,img)
		i = i+1
	xbmcplugin.endOfDirectory(addon_handle)
	return

def CHANNEL_MENU(url):
	addDir(menu_name+'Videos',url+'/videos',146)
	addDir(menu_name+'Playlists',url+'/playlists',146)
	addDir(menu_name+'Channels',url+'/channels',146)
	xbmcplugin.endOfDirectory(addon_handle)

def CHANNEL_ITEMS(url):
	#xbmcgui.Dialog().ok(url,'')
	html = openURL(url,'','','','YOUTUBE-CHANNEL_ITEMS-1st')
	if 'browse_ajax' in url:
		html = CLEAN_AJAX(html)
		html_blocks = [html]
	else:
		html_blocks = re.findall('branded-page-v2-subnav-container(.*?)footer-container',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('yt-lockup-thumbnail.*?href="(.*?)".*?src="(.*?)"(.*?)sessionlink.*?title="(.*?)"',block,re.DOTALL)
		for link,img,count,title in items:
			if 'video-count-label' in count:
				count = ' '+re.findall('video-count-label.*?(\d+).*?</',count,re.DOTALL)[0]
			else: count=''
			title = title.replace('\n','')
			link = website0a+link
			title = unescapeHTML(title)
			if 'list=' in link:
				addDir(menu_name+'LIST'+count+':  '+title,link,142,img)
			elif '/channel/' in link:
				addDir(menu_name+'CHNL:  '+title,link,145,img)
			else:
				addLink(menu_name+title,link,143,img)
		html_blocks = re.findall('items-load-more-button(.*?)load-more-loading',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('href="(.*?)"',block,re.DOTALL)
			for link in items:
				addDir(menu_name+'صفحة اخرى',website0a+link,146)
		xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url):
	html = openURL(url,'','','','YOUTUBE-TITLES-1st')
	html_blocks = re.findall('(yt-lockup-tile.*?)footer-container',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('yt-lockup-tile.*?(src|thumb)="(.*?)"(.*?)href="(.*?)".*?title="(.*?)"(.*?)</div></div></div>(.*?)</li>',block,re.DOTALL)
	#xbmcgui.Dialog().ok(str(block.count('yt-lockup-tile')),str(len(items)))
	#with open('S:\emad3.html', 'w') as f: f.write(block)
	for dummy,img,count,link,title,count2,paid in items:
		if 'Watch later' in title: continue
		if 'adurl=' in link:
			#title = 'AD:  '+title
			#link = re.findall('adurl=(.*?)&amp;',link+'&amp;',re.DOTALL)
			#link = unquote(link[0])
			continue
		img2 = re.findall('thumb="(.*?)"',count,re.DOTALL)
		if img2: img = img2[0]
		counts = ''
		if 'video-count-label' in count:
			count = re.findall('video-count-label.*?(\d+).*?</',count,re.DOTALL)
			if count: counts = ' ' + count[0]
		else:
			count2 = re.findall('<li>(\d+) video',count2,re.DOTALL)
			if count2: counts = ' ' + count2[0]
		if 'http' not in img: img = 'https:'+img
		if 'http' not in link: link = website0a+link
		if '\n' in paid: title = '$$:  '+title
		title = title.replace('\n','')
		title = unescapeHTML(title)
		if 'list=' in link: addDir(menu_name+'LIST'+counts+':  '+title,link,142,img)
		elif '/channel/' in link: addDir(menu_name+'CHNL'+counts+':  '+title,link,145,img)
		elif '/user/' in link: addDir(menu_name+'USER'+counts+':  '+title,link,145,img)
		else: addLink(menu_name+title,link,143,img)
	html_blocks = re.findall('search-pager(.*?)footer-container',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?button-content">(.*?)<',block,re.DOTALL)
		for link,title in items:
			addDir(menu_name+'صفحة '+title,website0a+link,141)
	xbmcplugin.endOfDirectory(addon_handle)

def SETTINGS():
	text1 = 'هذا الموقع يستخدم اضافة يوتيوب ولا يعمل بدونه'
	text2 = 'لعرض فيدوهات يوتيوب تحتاج ان تتأكد ان تضبيطات واعدادت يوتويب صحيحة'
	xbmcgui.Dialog().ok(text1,text2)
	xbmc.executebuiltin('Addon.OpenSettings(plugin.video.youtube)', True)
	return

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','%20')
	url2 = website0a + '/results?search_query='+search
	#url2 = 'plugin://plugin.video.youtube/kodion/search/query/?q='+search
	#xbmc.executebuiltin('Dialog.Close(busydialog)')
	#xbmc.executebuiltin('ActivateWindow(videos,'+url2+',return)')
	html = openURL(url2,'','','','YOUTUBE-SEARCH-1st')
	html_blocks = re.findall('filter-dropdown(.*?)class="item-section',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)".*?title="(.*?)"',block,re.DOTALL)
	fileterLIST = ['بدون فلتر وبدون ترتيب']
	linkLIST = [url2]
	for link,title in items:
		if 'Remove' in title: continue
		title = title.replace('Search for','Search for:  ')
		title = title.replace('Sort by','Sort by:  ')
		if 'Playlist' in title: title = 'جيد للمسلسلات '+title
		fileterLIST.append(unescapeHTML(title))
		linkLIST.append(website0a+link)
	fileterLIST.append(unescapeHTML('Sort by:   relevance'))
	linkLIST.append(url2)
	selection = xbmcgui.Dialog().select('اختر الفلتر او الترتيب المناسب:', fileterLIST)
	if selection == -1: return
	url3 = linkLIST[selection]
	TITLES(url3)
	return

def CLEAN_AJAX(text):
	text = text.replace('\\u003c','<')
	text = text.replace('\\u003e','>')
	text = text.replace('\\u0026','&')
	text = text.replace('\\"','"')
	text = text.replace('\\/','/')
	text = text.replace('\\n','\n')
	#text = text.encode('utf8')
	#text = text.decode('unicode_escape')
	#text = escapeUNICODE(text)
	#file = open('s:\emad.txt', 'w')
	#file.write(text)
	#file.close()
	return text

