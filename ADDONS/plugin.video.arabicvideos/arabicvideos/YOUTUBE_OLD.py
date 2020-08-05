"""
def TEST_YOUTUBE():
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36'}
	url = 'https://www.youtube.com/results?search_query=قناة+بث&sp=EgJAAQ=='
	import requests
	response = requests.request('GET',url=url,headers=headers)
	html = response.content
	a = re.findall('window\["ytInitialData"\] = ({.*?});',html,re.DOTALL)
	b = a[0].replace('true','True').replace('false','False')
	c = eval(b)
	d = c['contents']
	e = d['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']
	token = e['continuations'][0]['nextContinuationData']['continuation'].replace('=','%253D')
	url2 = url+'&pbj=1&ctoken='+token
	headers2 = headers.copy()
	headers2.update({'X-YouTube-Client-Name':'1','X-YouTube-Client-Version':'2.20200618.01.01'})
	response = requests.request('GET',url=url2,headers=headers2)
	html2 = response.content
	#with open('S:\\youtube_new_PAGE_RESULTS.txt', 'w') as f: f.write(html2)
	TITLES(url2)
	return

def CHANNEL_MENU(url):
	html,c = GET_PAGE_DATA(url)
	if 'ctoken=' not in url:
		if '"title":"Videos"' in html: addMenuItem('folder',menu_name+'فيديوهات',url+'/videos',146)
		if '"title":"Playlists"' in html: addMenuItem('folder',menu_name+'قوائم',url+'/playlists',146)
		if '"title":"Channels"' in html: addMenuItem('folder',menu_name+'قنوات',url+'/channels',146)#,'','','UPDATE')
		d = c['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']
	else: d = c[1]['response']['continuationContents']['sectionListContinuation']
	e = d['contents']
	for i in range(len(e)):
		try:
			item = e[i]['itemSectionRenderer']['contents'][0]
			ISERT_ITEM_TO_MENU(item)
		except: pass
	if 'continuations' in d.keys():
		token = d['continuations'][0]['nextContinuationData']['continuation']
		url2 = website0a+'/browse_ajax?ctoken='+token
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,146)
	return

def SETTINGS():
	text1 = 'هذا الموقع يستخدم اضافة يوتيوب ولا يعمل بدونه'
	text2 = 'لعرض فيدوهات يوتيوب تحتاج ان تتأكد ان تضبيطات واعدادت يوتويب صحيحة'
	#xbmcgui.Dialog().ok(text1,text2)
	xbmc.executebuiltin('Addon.OpenSettings(plugin.video.youtube)', True)
	return

def PLAYLIST_ITEMS_OLD(url,html):
	# https://www.youtube.com/playlist?list=PLRXjtfMCvJBUzMQksXgR2IB2_AndVBmfm
	# https://www.youtube.com/watch?v=l5TBLKr3WYY&list=PLRXjtfMCvJBUzMQksXgR2IB2_AndVBmfm&index=18
	if '/watch?v=' in url:
		PLAYLIST_ITEMS_PLAYER_OLD(url)
		return
	html_blocks = []
	if 'browse_ajax' in url:
		#html = openURL_cached(REGULAR_CACHE,url,'',headers,'','YOUTUBE-PLAYLIST_ITEMS-1st')
		html = CLEAN_AJAX(html)
		html_blocks = [html]
	elif 'list=' in url and 'index=' not in url:
		id = url.split('list=')[1].split('&')[0]
		url2 = website0a+'/playlist?list='+id
		html = openURL_cached(REGULAR_CACHE,url2,'',headers,'','YOUTUBE-PLAYLIST_ITEMS-2nd')
		html_blocks = re.findall('class="pl-video-table(.*?)footer-container',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url2,id)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('data-title="(.*?)".*?href="(.*?)".*?data-thumb="(.*?)".*?video-time(.*?)</div></td></tr>',block,re.DOTALL)
		for title,link,img,duration in items:
			if 'timestamp' in duration: duration = re.findall('timestamp.*?><.*?>(.*?)<',duration,re.DOTALL)[0]
			else: duration=''
			if '.' in duration: duration = duration.replace('.',':')
			title = title.replace('\n','')
			title = unescapeHTML(title)
			link = website0a+link
			addMenuItem('video',menu_name+title,link,143,img,duration)
		html_blocks = re.findall('items-load-more-button(.*?)load-more-loading',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('href="(.*?)"',block,re.DOTALL)
			for link in items:
				addMenuItem('folder',menu_name+'صفحة اخرى',website0a+link,142)
	return

def PLAYLIST_ITEMS_PLAYER_OLD(url):
	# https://www.youtube.com/watch?v=l5TBLKr3WYY&list=PLRXjtfMCvJBUzMQksXgR2IB2_AndVBmfm&index=18
	html,c = GET_PAGE_DATA(url)
	html_blocks = re.findall('playlist-videos-container(.*?)watch7-container',html,re.DOTALL)
	block = html_blocks[0]
	items1 = re.findall('data-video-title="(.*?)".*?href="(.*?)"',block,re.DOTALL)
	items2 = re.findall('data-thumbnail-url="(.*?)"',block,re.DOTALL)
	i = 0
	for title,link in items1:
		title = title.replace('\n','')
		title = unescapeHTML(title)
		img = items2[i]
		link = website0a+link
		addMenuItem('video',menu_name+title,link,143,img)
		i = i+1
	addMenuItem('folder',menu_name+'صفحة اخرى',link,142)
	return

def CHANNEL_ITEMS_OLD(url,html):
	#xbmcgui.Dialog().ok(url,str(c))
	if 'browse_ajax' in url:
		html = CLEAN_AJAX(html)
		html_blocks = [html]
	else: html_blocks = re.findall('branded-page-v2-subnav-container(.*?)footer-container',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('yt-lockup-thumbnail.*?href="(.*?)".*?src="(.*?)"(.*?)sessionlink.*?title="(.*?)"(.*?)container',block,re.DOTALL)
		for link,img,count,title,live in items:
			if '>Live now<' in live: live = 'LIVE:  '
			else: live = ''
			if 'video-time' in count: duration = re.findall('video-time.*?><.*?>(.*?)<',count,re.DOTALL)[0]
			else: duration=''
			if '.' in duration: duration = duration.replace('.',':')
			if 'video-count-label' in count: count = ' '+re.findall('video-count-label.*?(\d+).*?</',count,re.DOTALL)[0]
			else: count=''
			title = title.replace('\n','')
			link = website0a+link
			title = unescapeHTML(title)
			if 'list=' in link: addMenuItem('folder',menu_name+'LIST'+count+':  '+title,link,142,img)
			elif '/channel/' in link: addMenuItem('folder',menu_name+'CHNL:  '+title,link,146,img)
			elif live!='': addMenuItem('live',menu_name+live+title,link,143,img)
			else: addMenuItem('video',menu_name+title,link,143,img,duration)
		html_blocks = re.findall('items-load-more-button(.*?)load-more-loading',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('href="(.*?)"',block,re.DOTALL)
			for link in items:
				addMenuItem('folder',menu_name+'صفحة اخرى',website0a+link,146)
	return

def TITLES_OLD(url,html):
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
		count = ''
		if '\n' in paid: title = '$$:  '+title
		if 'video-time' in count: duration = re.findall('video-time.*?>(.*?)<',count,re.DOTALL)[0]
		else: duration = ''
		if '.' in duration: duration = duration.replace('.',':')
		if '>Live now<' in count2: live = 'LIVE:  '
		else: live = ''
		if 'video-count-label' in count:
			count = re.findall('video-count-label.*?(\d+).*?</',count,re.DOTALL)
			if count: count = ' ' + count[0]
		else:
			count2 = re.findall('<li>(\d+) video',count2,re.DOTALL)
			if count2: count = ' ' + count2[0]
		if 'http' not in img: img = 'https:'+img
		if 'http' not in link: link = website0a+link
		title = title.replace('\n','')
		title = unescapeHTML(title)
		if 'list=' in link: addMenuItem('folder',menu_name+'LIST'+count+':  '+title,link,142,img)
		elif '/channel/' in link: addMenuItem('folder',menu_name+'CHNL'+count+':  '+title,link,146,img)
		elif '/user/' in link: addMenuItem('folder',menu_name+'USER'+count+':  '+title,link,146,img)
		elif live!='': addMenuItem('live',menu_name+live+title,link,143,img)
		else: addMenuItem('video',menu_name+title,link,143,img,duration)
	html_blocks = re.findall('search-pager(.*?)footer-container',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		#with open('S:\\0emad.html', 'w') as f: f.write(block)
		items = re.findall('href="(.*?)".*?button-content">(.*?)<',block,re.DOTALL)
		for link,title in items:
			addMenuItem('folder',menu_name+'صفحة '+title,website0a+link,141)
	return
"""


