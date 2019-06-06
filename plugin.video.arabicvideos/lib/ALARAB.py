# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'https://vod.alarab.com'


website0b = 'https://vod.alarab.com/view-1/افلام-عربية'
website0c = 'http://tv.alarab.com'
website0d = 'http://tv1.alarab.com'
website0e = 'http://vod.alarab.com/index.php'

script_name = 'ALARAB'
headers = { 'User-Agent' : '' }
menu_name='_KLA_'

def MAIN(mode,url,text):
	if mode==10: MENU()
	elif mode==11: TITLES(url)
	elif mode==12: PLAY(url)
	elif mode==13: EPISODES(url)
	elif mode==14: LATEST()
	elif mode==15: RAMADAN_MENU()
	elif mode==16: RAMADAN()
	elif mode==19: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',19)
	addDir(menu_name+'اخر الاضافات','',14)
	addDir(menu_name+'مسلسلات رمضان','',15)
	html = openURL(website0a,'',headers,'','ALARAB-MENU-1st')
	html_blocks=re.findall('id="navbar"(.*?)</div>',html,re.DOTALL)
	block=html_blocks[0]
	#xbmcgui.Dialog().ok(str(len(html)), str(len(block)) )
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for link,title in items:
		link = website0a+link
		addDir(menu_name+title,link,11)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def RAMADAN_MENU():
	addDir(menu_name+'مسلسلات رمضان 2019','',16)
	addDir(menu_name+'مسلسلات رمضان 2018',website0a+'/ramadan2018/مصرية',11)
	addDir(menu_name+'مسلسلات رمضان 2017',website0a+'/ramadan2017/مصرية',11)
	addDir(menu_name+'مسلسلات رمضان 2016',website0a+'/ramadan2016/مصرية',11)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def LATEST():
	html = openURL(website0a,'',headers,'','ALARAB-LATEST-1st')
	#xbmcgui.Dialog().ok('',html)
	html_blocks=re.findall('heading-top(.*?)div class=',html,re.DOTALL)
	block = html_blocks[1]+html_blocks[2]
	items=re.findall('href="(.*?)".*?src="(.*?)" alt="(.*?)"',block,re.DOTALL)
	for link,img,title in items:
		url = website0a + link
		if 'series' in url: addDir(menu_name+title,url,11,img)
		else: addLink(menu_name+title,url,12,img)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url):
	html = openURL(url,'',headers,'','ALARAB-ITEMS-1st')
	html_blocks = re.findall('video-category(.*?)right_content',html,re.DOTALL)
	block = html_blocks[0]
	found = False
	items = re.findall('src="(http.*?)".*?<h5><a href="(.*?)">(.*?)<',block,re.DOTALL)
	if not items:
		items = re.findall('src="(http.*?)".*?<h2>#<a href="(.*?)">(.*?)<',block,re.DOTALL)		
	allTitles,itemsNEW = [],[]
	for img,link,title in items:
		sequence = re.findall('(\d+)',title,re.DOTALL)
		if sequence: sequence = int(sequence[0])
		else: sequence = ''
		itemsNEW.append([img,link,title,sequence])
	itemsNEW = sorted(itemsNEW, reverse=True, key=lambda key: key[3])
	for img,link,title,sequence in itemsNEW:
		link = website0a + link
		#xbmcgui.Dialog().ok(url,title)
		title = title.replace('مشاهدة مسلسل','مسلسل')
		title = title.replace('مشاهدة المسلسل','المسلسل')
		title = title.replace('مباشرة كواليتي','')
		title = title.replace('عالية على العرب','')
		title = title.replace('مشاهدة مباشرة','')
		title = title.replace('اون لاين','')
		title = title.replace('اونلاين','')
		title = title.replace('بجودة عالية','')
		title = title.replace('جودة عالية','')
		title = title.replace('بدون تحميل','')
		title = title.replace('على العرب','')
		title = title.replace('مباشرة','')
		title = title.strip(' ').replace('  ',' ').replace('  ',' ')
		title2 = title
		if '/q/' in url and ('الحلقة' in title or 'الحلقه' in title):
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode: title2 = episode[0]
			#if 'مسلسل' not in title2: title2 = 'مسلسل '+title2
			title2 = '_MOD_'+title2
		if title2 not in allTitles:
			allTitles.append(title2)
			#xbmc.log(title2, level=xbmc.LOGNOTICE)
			if '/q/' in url and ('الحلقة' in title or 'الحلقه' in title):
				addDir(menu_name+title2,link,13,img)
				found = True
			elif 'series' in link:
				addDir(menu_name+title,link,11,img)
				found = True
			else:
				#if 'مسلسل' not in title and 'الحلقة' in title: title = 'مسلسل '+title
				addLink(menu_name+title,link,12,img)
				found = True
	if found:
		items = re.findall('tsc_3d_button red.*?href="(.*?)" title="(.*?)"',block,re.DOTALL)
		for link,page in items:
			url = website0a + link
			addDir(menu_name+page,url,11)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def EPISODES(url):
	html = openURL(url,'',headers,'','SHAHID4U-ITEMS-1st')
	series = re.findall('href="(/series.*?)"',html,re.DOTALL)
	url2 = website0a+series[0]
	TITLES(url2)
	return

def EPISODES_OLD(url):
	html = openURL(url,'',headers,'','SHAHID4U-ITEMS-1st')
	html_blocks = re.findall('banner-right(.*?)classic-channel',html,re.DOTALL)
	xbmcgui.Dialog().ok(url,'step 2')
	block = html_blocks[0]
	items = re.findall('src="(.*?)".*?href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	xbmcgui.Dialog().ok(url,'step 3')
	items = sorted(items, reverse=True, key=lambda key: key[1])
	#name = xbmc.getInfoLabel('ListItem.Label')
	xbmcgui.Dialog().ok(url,'step 4')
	allTitles = []
	for img,link,title in items:
		if title not in allTitles:
			link = website0a+unquote(link)
			title = title.strip(' ')
			addLink(menu_name+'مسلسل '+title,link,12,img)
			allTitles.append(title)
	xbmcgui.Dialog().ok(url,'step 5')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	items_url,items_name = [],[]
	if '/viewVedio/' in url:
		id = re.findall('.com/viewVedio/([0-9]+)/',url,re.DOTALL)[0]
	else:
		id = re.findall('.com/v([0-9]+)-',url,re.DOTALL)[0]
	url2 = 'https://alarabplayers.alarab.com/?vid='+id
	html = openURL(url,'',headers,'','ALARAB-PLAY-1st')
	html += openURL(url2,'',headers,'','ALARAB-PLAY-2nd')
	html_blocks = re.findall('playerInstance.setup(.*?)primary',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		try: block += html_blocks[1]
		except: pass
		items = re.findall('file: "(.*?mp4)".*?label: "(.*?)"',block,re.DOTALL)
		#xbmcgui.Dialog().ok(url,str(items))
		for file,label in reversed(items):
			items_url.append(file)
			items_name.append(label)
		items = re.findall('file:".*?youtu.*?=(.*?)"',block,re.DOTALL)
		for youtubeID in items:
			#url = 'plugin://plugin.video.youtube/play/?video_id='+youtubeID
			items_url.append(url)
			items_name.append('ملف اليوتيوب')
	else:
		videodeliveryID = re.findall('stream src="(.*?)"',html,re.DOTALL)
		if videodeliveryID:
			url = 'https://videodelivery.net/'+videodeliveryID[0]+'/manifest/video.mpd'
			items_url.append(url)
			items_name.append('ملف mpd')
	#items = re.findall('resp-container.*?src="(.*?)".*?</div>',html,re.DOTALL)
	#if items:
	#	url = items[0]
	#	items_url.append(url)
	#	items_name.append('ملف التشغيل')
	#xbmcgui.Dialog().ok('',str(items_url))
	#url = website0a + '/download.php?file='+id
	#html = openURL(url,'',headers,'','ALARAB-PLAY-3rd')
	#items = re.findall('</h2>.*?href="(.*?mp4)"',html,re.DOTALL)
	#if items:
	#	items_url.append(items[0])
	#	items_name.append('ملف التحميل')
	if len(items_url)==0:
		xbmcgui.Dialog().ok('No video file found','لا يوجد ملف فيديو')
		return
	elif len(items_url)==1:
		selection = 0
		url = items_url[selection]
	else:
		new_items_url,new_items_name = [],[]
		for i in range(0,len(items_url),+1):
			if items_url[i] not in new_items_url:
				new_items_url.append(items_url[i])
				new_items_name.append(items_name[i])
		selection = xbmcgui.Dialog().select('اختر الملف المناسب:', new_items_name)
		if selection == -1 : return
		url = new_items_url[selection]
	#xbmcgui.Dialog().ok(url,'')
	#PLAY_VIDEO(url,script_name)
	from RESOLVERS import PLAY_LINK as RESOLVERS_PLAY_LINK
	RESOLVERS_PLAY_LINK(url,script_name)
	return ''

def RAMADAN():
	html = openURL(website0a,'',headers,'','ALARAB-RAMADAN-1st')
	html_blocks=re.findall('id="content_sec"(.*?)id="left_content"',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	year = re.findall('/ramadan([0-9]+)/',str(items),re.DOTALL)
	year = year[0]
	for link,title in items:
		url = website0a + link
		title = title.strip(' ') + ' ' + year
		addDir(menu_name+title,url,11)
	xbmcplugin.endOfDirectory(addon_handle)
	return ''

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search == '': return ''
	new_search = search.replace(' ','%20')
	url = website0a + "/q/" + new_search
	#xbmcgui.Dialog().ok('',url)
	TITLES(url)
	return ''



