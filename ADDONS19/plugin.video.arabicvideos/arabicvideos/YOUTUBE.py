# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='YOUTUBE'
menu_name='_YUT_'
website0a = WEBSITES[script_name][0]

#headers = '' 
#headers = {'User-Agent':''}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}

def MAIN(mode,url,text,type):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if	 mode==140: results = MENU()
	elif mode==141: results = TITLES(url)
	elif mode==142: results = PLAYLIST_ITEMS(url)
	elif mode==143: results = PLAY(url,type)
	#elif mode==144: results = SETTINGS()
	#elif mode==144: results = TEST_YOUTUBE()
	elif mode==145: results = CHANNEL_MENU(url)
	elif mode==146: results = CHANNEL_ITEMS(url)
	elif mode==147: results = LIVE_ARABIC()
	elif mode==148: results = LIVE_ENGLISH()
	elif mode==149: results = SEARCH(text)
	else: results = False
	return results

def MENU():
	addMenuItem('folder',menu_name+'بحث في الموقع','',149)
	#addMenuItem('folder',menu_name+'TEST_YOUTUBE','',144)
	addMenuItem('folder',menu_name+'قنوات عربية','',147)
	addMenuItem('folder',menu_name+'قنوات أجنبية','',148)
	addMenuItem('folder',menu_name+'افلام عربية',website0a+'/results?search_query=فيلم',141)
	addMenuItem('folder',menu_name+'افلام اجنبية',website0a+'/results?search_query=movie',141)
	addMenuItem('folder',menu_name+'مسلسلات عربية',website0a+'/results?search_query=مسلسل&sp=EgIQAw==',141)
	addMenuItem('folder',menu_name+'مسلسلات اجنبية',website0a+'/results?search_query=series&sp=EgIQAw==',141)
	addMenuItem('folder',menu_name+'مسرحيات عربية',website0a+'/results?search_query=مسرحية',141)
	addMenuItem('folder',menu_name+'مسلسلات كارتون',website0a+'/results?search_query=كارتون&sp=EgIQAw==',141)
	addMenuItem('folder',menu_name+'خطبة المرجعية',website0a+'/results?search_query=قناة+كربلاء+الفضائية+خطبة+الجمعة&sp=CAISAhAB',141)
	addMenuItem('folder',menu_name+'قناة كربلاء الفضائية',website0a+'/user/karbalatvchannel',145)
	addMenuItem('folder',menu_name+'العراق خطبة المرجعية',website0a+'/playlist?list=PL4jUq6pnG36QjuXDhNnIlriuzroTFtmfr',142)
	addMenuItem('folder',menu_name+'العتبة الحسينية المقدسة',website0a+'/user/ImamHussaindotorg',145)
	addMenuItem('folder',menu_name+'شوف دراما الاولى',website0a+'/channel/UCgd_tWU4X7s10DKdgt-XDNQ',145)
	addMenuItem('folder',menu_name+'شوف دراما الثانية',website0a+'/channel/UC25ZB5ZMqLQwxFDV9FHvF8g',145)
	addMenuItem('folder',menu_name+'شوف دراما الثالثة',website0a+'/channel/UCQOz2_AhxeHUbNMYan-6ZQQ',145)
	addMenuItem('folder',menu_name+'شبكة وطن',website0a+'/user/WatanNetwork',145)
	#addMenuItem('folder',menu_name+'اعدادات اضافة يوتيوب','',144)
	#yes = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','هذا الاختيار سوف يخرجك من البرنامج','لأنه سوف يقوم بتشغيل برنامج يوتيوب')
	#if yes:
	#	url = 'plugin://plugin.video.youtube'
	#	xbmc.executebuiltin('Dialog.Close(busydialog)')
	#	xbmc.executebuiltin('ReplaceWindow(videos,'+url+')')
	#	#xbmc.executebuiltin('RunAddon(plugin.video.youtube)')
	return

def LIVE_ARABIC():
	TITLES(website0a+'/results?search_query=قناة+بث&sp=EgJAAQ==')
	return

def LIVE_ENGLISH():
	TITLES(website0a+'/results?search_query=tv&sp=EgJAAQ==')
	return

def CHANNEL_MENU(url):
	addMenuItem('folder',menu_name+'فيديوهات',url+'/videos',146)
	addMenuItem('folder',menu_name+'قوائم',url+'/playlists',146)
	addMenuItem('folder',menu_name+'قنوات',url+'/channels',146)#,'','','UPDATE')
	return

def PLAY(url,type):
	#url = url+'&'
	#items = re.findall('v=(.*?)&',url,re.DOTALL)
	#id = items[0]
	#xbmcgui.Dialog().ok(url,'')
	#link = 'plugin://plugin.video.youtube/play/?video_id='+id
	#PLAY_VIDEO(link,script_name,'video')
	linkLIST = [url]
	import RESOLVERS
	RESOLVERS.PLAY(linkLIST,script_name,type)
	return

def PLAYLIST_ITEMS_NEW(url):
	# https://www.youtube.com/watch?v=nMaNCKJCLfE&list=PLbg43835F8ge08Sb_gl6dbdGZzD3hCnQL
	# https://www.youtube.com/playlist?list=PLbg43835F8ge08Sb_gl6dbdGZzD3hCnQL
	if '/watch?v=' in url:
		listID = re.findall('list=(.*?)&',url+'&',re.DOTALL)
		url = website0a+'/playlist?list='+listID[0]
	html,c = GET_PAGE_DATA(url)
	token = ''
	if 'ctoken' in url:
		f = c[1]['response']['continuationContents']['playlistVideoListContinuation']
		if 'continuations' in f.keys(): token = f['continuations'][0]['nextContinuationData']['continuation']
	else:
		d = c['contents']
		if '/watch?v=' in url: f = d['twoColumnWatchNextResults']['playlist']['playlist']
		else:
			e = d['twoColumnBrowseResultsRenderer']['tabs'][0]
			f = e['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']
			if 'continuations' in f.keys(): token = f['continuations'][0]['nextContinuationData']['continuation']
	g = f['contents']
	for i in range(len(g)):
		item = g[i]
		#if item.keys()[0]=='shelfRenderer': continue
		succeeded,title,link,img,count,duration,live = ITEMS_RENDER(item)
		if not succeeded: continue
		addMenuItem('video',menu_name+title,link,143,img,duration)
	if token!='':
		#param = f['continuations'][0]['nextContinuationData']['clickTrackingParams']#.replace('=','%253D')
		#https://www.youtube.com/browse_ajax?ctoken=4qmFsgI0EhhVQ040NWFkeDVlUUN4MXZNNnBfTGZyNEEaGEVnWjJhV1JsYjNNZ0FEZ0JlZ0V5dUFFQQ%253D%253D&continuation=4qmFsgI0EhhVQ040NWFkeDVlUUN4MXZNNnBfTGZyNEEaGEVnWjJhV1JsYjNNZ0FEZ0JlZ0V5dUFFQQ%253D%253D&itct=CCgQybcCIhMI-_nWhMmR6gIVI9BgCh3bTQ9z
		url2 = website0a+'/browse_ajax?ctoken='+token#+'&continuation='+token+'&itct='+param
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,142)
	return

def PLAYLIST_ITEMS(url):
	# https://www.youtube.com/playlist?list=PLRXjtfMCvJBUzMQksXgR2IB2_AndVBmfm
	# https://www.youtube.com/watch?v=l5TBLKr3WYY&list=PLRXjtfMCvJBUzMQksXgR2IB2_AndVBmfm&index=18
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','YOUTUBE-PLAYLIST_ITEMS-1st')
	if 'footer-container' not in html:
		PLAYLIST_ITEMS_NEW(url)
		return
	if '/watch?v=' in url:
		PLAYLIST_ITEMS_PLAYER(url)
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

def PLAYLIST_ITEMS_PLAYER(url):
	# https://www.youtube.com/watch?v=l5TBLKr3WYY&list=PLRXjtfMCvJBUzMQksXgR2IB2_AndVBmfm&index=18
	#xbmcgui.Dialog().ok(url,'')
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','YOUTUBE-PLAYLIST_ITEMS_PLAYER-1st')
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

def SHELF_MENU(f):
	for i in range(len(f)):
		item = f[i]['itemSectionRenderer']['contents'][0]
		succeeded,title,link,img,count,duration,live = ITEMS_RENDER(item)
		#xbmcgui.Dialog().ok(link,title)
		if not succeeded: continue
		addMenuItem('folder',menu_name+title,link,146)
	return

def CHANNEL_ITEMS_NEW(url):
	#xbmcgui.Dialog().ok(url,'starting CHANNEL_ITEMS_NEW')
	html,c = GET_PAGE_DATA(url)
	#LOG_THIS('NOTICE','==================================================')
	#LOG_THIS('NOTICE',str(c))
	#LOG_THIS('NOTICE',str(c.keys()))
	token = ''
	if 'ctoken' in url:
		g = c[1]['response']['continuationContents']['gridContinuation']
		if 'continuations' in g.keys(): token = g['continuations'][0]['nextContinuationData']['continuation']
	else:
		d = c['contents']
		if   '/videos?' 	in url+'?': e = d['twoColumnBrowseResultsRenderer']['tabs'][1]
		elif '/playlists?' 	in url+'?': e = d['twoColumnBrowseResultsRenderer']['tabs'][2]
		elif '/channels?' 	in url+'?': e = d['twoColumnBrowseResultsRenderer']['tabs'][4]
		f = e['tabRenderer']['content']['sectionListRenderer']['contents']
		try: g = f[0]['itemSectionRenderer']['contents'][0]['gridRenderer']
		except:
			SHELF_MENU(f)
			return
		if 'continuations' in g.keys(): token = g['continuations'][0]['nextContinuationData']['continuation']
	h = g['items']
	for i in range(len(h)):
		item = h[i]
		succeeded,title,link,img,count,duration,live = ITEMS_RENDER(item)
		if not succeeded: continue
		#title = title.replace('\n','')
		#link = website0a+link
		#title = unescapeHTML(title)
		if 'list=' in link: addMenuItem('folder',menu_name+'LIST'+count+':  '+title,link,142,img)
		elif '/channel/' in link: addMenuItem('folder',menu_name+'CHNL:  '+title,link,145,img,'','UPDATE')
		elif live!='': addMenuItem('live',menu_name+live+title,link,143,img)
		else: addMenuItem('video',menu_name+title,link,143,img,duration)
	if token!='':
		#param = f['continuations'][0]['nextContinuationData']['clickTrackingParams']#.replace('=','%253D')
		#https://www.youtube.com/browse_ajax?ctoken=4qmFsgI0EhhVQ040NWFkeDVlUUN4MXZNNnBfTGZyNEEaGEVnWjJhV1JsYjNNZ0FEZ0JlZ0V5dUFFQQ%253D%253D&continuation=4qmFsgI0EhhVQ040NWFkeDVlUUN4MXZNNnBfTGZyNEEaGEVnWjJhV1JsYjNNZ0FEZ0JlZ0V5dUFFQQ%253D%253D&itct=CCgQybcCIhMI-_nWhMmR6gIVI9BgCh3bTQ9z
		url2 = website0a+'/browse_ajax?ctoken='+token#+'&continuation='+token+'&itct='+param
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,146)
	return

def CHANNEL_ITEMS(url):
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','YOUTUBE-CHANNEL_ITEMS-1st')
	if 'footer-container' not in html:
		CHANNEL_ITEMS_NEW(url)
		return
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
			elif '/channel/' in link: addMenuItem('folder',menu_name+'CHNL:  '+title,link,145,img)
			elif live!='': addMenuItem('live',menu_name+live+title,link,143,img)
			else: addMenuItem('video',menu_name+title,link,143,img,duration)
		html_blocks = re.findall('items-load-more-button(.*?)load-more-loading',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('href="(.*?)"',block,re.DOTALL)
			for link in items:
				addMenuItem('folder',menu_name+'صفحة اخرى',website0a+link,146)
	return

def MULTIPLE_TRY(render,in1,in2,in3=''):
	succeeded = True
	try: out = eval(in1)
	except:
		try: out = eval(in2)
		except:
			if in3=='':
				succeeded = False
				out = ''
			else:
				try: out = eval(in3)
				except:
					succeeded = False
					out = ''
	return succeeded,out

def ITEMS_RENDER(item):
	render,badges = '',''
	succeeded,title,link,img,count,duration,live = False,'','','','','',''
	#LOG_THIS('NOTICE','=====================================')
	#LOG_THIS('NOTICE',str(item))
	#xbmcgui.Dialog().ok(render,'')
	#validRenders = ['showRenderer','shelfRenderer','videoRenderer','playlistRenderer','channelRenderer',
	#				'gridVideoRenderer','gridPlaylistRenderer','gridChannelRenderer',
	#				'playlistVideoRenderer','playlistPanelVideoRenderer']
	renderName = item.keys()[0]
	#if 'Renderer' in renderName: render = item[renderName]
	#if renderName in validRenders: render = item[renderName]
	#else: return succeeded,title,link,img,count,duration,live
	render = item[renderName]
	in1 = "render['title']['simpleText']"
	in2 = "render['title']['runs'][0]['text']"
	in3 = "render['unplayableText']['simpleText']"
	succeeded99,out99 = MULTIPLE_TRY(render,in1,in2,in3)
	if succeeded99: title = out99
	else: return succeeded,title,link,img,count,duration,live
	in1 = "render['viewPlaylistText']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']"
	in2 = "render['title']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']"
	in3 = "render['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']"
	succeeded99,out99 = MULTIPLE_TRY(render,in1,in2,in3)
	if succeeded99: link = out99
	in1 = "render['thumbnail']['thumbnails'][0]['url']"
	in2 = "render['thumbnails'][0]['thumbnails'][0]['url']"
	in3 = "render['thumbnailRenderer']['showCustomThumbnailRenderer']['thumbnail']['thumbnails'][0]['url']"
	succeeded99,out99 = MULTIPLE_TRY(render,in1,in2,in3)
	if succeeded99: img = out99
	in1 = "render['videoCount']"
	in2 = "render['videoCountText']['runs'][0]['text']"
	in3 = "render['thumbnailOverlays'][0]['thumbnailOverlayBottomPanelRenderer']['text']['runs'][0]['text']"
	succeeded99,out99 = MULTIPLE_TRY(render,in1,in2,in3)
	if succeeded99: count = out99
	in1 = "render['lengthText']['simpleText']"
	in2 = "render['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText']"
	succeeded99,out99 = MULTIPLE_TRY(render,in1,in2)
	if succeeded99: duration = out99
	if 'badges' in render.keys():
		badges = str(render['badges'])
		if 'LIVE NOW' in badges: live = 'LIVE:  '
	if 'http' not in img: img = 'https:'+img
	link = escapeUNICODE(link)
	count = count.strip(' videos').replace(',','')
	if 'http' not in link: link = website0a+link
	#xbmcgui.Dialog().ok(link,website0a)
	return True,title,link,img,count,duration,live

def GET_PAGE_DATA(url):
	headers2 = headers.copy()
	if 'ctoken' in url: headers2.update({'X-YouTube-Client-Name':'1','X-YouTube-Client-Version':'2.20200618.01.01'})
	html = openURL_cached(SHORT_CACHE,url,'',headers2,'','YOUTUBE-GET_PAGE_DATA-1st')
	a,c = '',''
	if 'ytInitialData' in html:
		a = re.findall('window\["ytInitialData"\] = ({.*?});',html,re.DOTALL)
		a = a[0]
	elif '</script>' not in html: a = html
	if a!='':
		b = a.replace('true','True').replace('false','False')
		c = eval(b)
	return html,c

def TITLES_NEW(url):
	#xbmcgui.Dialog().ok(url,'starting TITLES_NEW')
	html,c = GET_PAGE_DATA(url)
	#with open('S:\\00emad00.html', 'w') as f: f.write(html)
	if 'ctoken' in url: d = c[1]['response']['continuationContents']['itemSectionContinuation']
	else: d = c['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][-1]['itemSectionRenderer']
	e = d['contents']
	#xbmcgui.Dialog().ok(str(len(e)),str(e[0].keys()))
	for i in range(len(e)):
		item = e[i]
		if item.keys()[0]=='shelfRenderer': continue
		succeeded,title,link,img,count,duration,live = ITEMS_RENDER(item)
		if not succeeded: continue
		if 'list=' in link: addMenuItem('folder',menu_name+'LIST'+count+':  '+title,link,142,img)
		elif '/channel/' in link: addMenuItem('folder',menu_name+'CHNL'+count+':  '+title,link,145,img)
		elif '/user/' in link: addMenuItem('folder',menu_name+'USER'+count+':  '+title,link,145,img)
		elif live!='': addMenuItem('live',menu_name+live+title,link,143,img)
		else: addMenuItem('video',menu_name+title,link,143,img,duration)
	if 'continuations' in d.keys():
		token = d['continuations'][0]['nextContinuationData']['continuation']#.replace('=','%253D')
		#param = d['continuations'][0]['nextContinuationData']['clickTrackingParams']#.replace('=','%253D')
		url2 = url+'&pbj=1&ctoken='+token#+'&continuation='+token+'&itct='+param
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,141)
	return

def TITLES(url):
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','YOUTUBE-TITLES-1st')
	if 'footer-container' not in html:
		TITLES_NEW(url)
		return
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
		elif '/channel/' in link: addMenuItem('folder',menu_name+'CHNL'+count+':  '+title,link,145,img)
		elif '/user/' in link: addMenuItem('folder',menu_name+'USER'+count+':  '+title,link,145,img)
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

def SEARCH(search):
	if '::' in search:
		search = search.split('::')[0]
		category = False
	else: category = True
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','%20')
	url2 = website0a + '/results?search_query='+search
	fileterLIST = ['بدون فلتر وبدون ترتيب']
	linkLIST = [url2]
	#url2 = 'plugin://plugin.video.youtube/kodion/search/query/?q='+search
	#xbmc.executebuiltin('Dialog.Close(busydialog)')
	#xbmc.executebuiltin('ActivateWindow(videos,'+url2+',return)')
	html,c = GET_PAGE_DATA(url2)
	if 'footer-container' not in html:
		d = c['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['subMenu']['searchSubMenuRenderer']['groups']
		for groupID in range(len(d)):
			group = d[groupID]['searchFilterGroupRenderer']['filters']
			for filterID in range(len(group)):
				#LOG_THIS('NOTICE','=========================================')
				#LOG_THIS('NOTICE',str(groupID))
				#LOG_THIS('NOTICE',str(filterID))
				render = group[filterID]['searchFilterRenderer']
				if 'navigationEndpoint' in render.keys():
					link = render['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
					title = render['tooltip']
					if 'Remove' in title: continue
					title = title.replace('Search for','Search for:  ')
					title = title.replace('Sort by','Sort by:  ')
					if 'Playlist' in title: title = 'جيد للمسلسلات '+title
					fileterLIST.append(escapeUNICODE(title))
					linkLIST.append(website0a+link)
	else:
		html_blocks = re.findall('filter-dropdown(.*?)class="item-section',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?title="(.*?)"',block,re.DOTALL)
		for link,title in items:
			if 'Remove' in title: continue
			title = title.replace('Search for','Search for:  ')
			title = title.replace('Sort by','Sort by:  ')
			if 'Playlist' in title: title = 'جيد للمسلسلات '+title
			fileterLIST.append(unescapeHTML(title))
			linkLIST.append(website0a+link)
	fileterLIST.append(unescapeHTML('Sort by:  relevance'))
	linkLIST.append(url2)
	if category:
		selection = xbmcgui.Dialog().select('اختر الفلتر او الترتيب المناسب:', fileterLIST)
		if selection == -1: return
		url3 = linkLIST[selection]
	else: url3 = linkLIST[0]
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
	with open('S:\\youtube_new_PAGE_RESULTS.txt', 'w') as f: f.write(html2)
	TITLES_NEW(url2)
	return
"""

"""
def SETTINGS():
	text1 = 'هذا الموقع يستخدم اضافة يوتيوب ولا يعمل بدونه'
	text2 = 'لعرض فيدوهات يوتيوب تحتاج ان تتأكد ان تضبيطات واعدادت يوتويب صحيحة'
	xbmcgui.Dialog().ok(text1,text2)
	xbmc.executebuiltin('Addon.OpenSettings(plugin.video.youtube)', True)
	return
"""


