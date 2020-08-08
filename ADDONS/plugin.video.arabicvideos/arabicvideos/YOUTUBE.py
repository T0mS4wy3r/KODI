# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='YOUTUBE'
menu_name='_YUT_'
website0a = WEBSITES[script_name][0]

#headers = '' 
#headers = {'User-Agent':''}

def MAIN(mode,url,text,type,page):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if	 mode==140: results = MENU()
	elif mode==141: results = TITLES(url,page,text)
	elif mode==142: results = PLAYLIST_ITEMS(url)
	elif mode==143: results = PLAY(url,type)
	elif mode==144: results = TRENDING_MENU(url)
	#elif mode==144: results = SETTINGS()
	#elif mode==144: results = TEST_YOUTUBE()
	#elif mode==145: results = CHANNEL_MENU(url)
	elif mode==146: results = CHANNEL_ITEMS(url,page,text)
	elif mode==147: results = LIVE_ARABIC()
	elif mode==148: results = LIVE_ENGLISH()
	elif mode==149: results = SEARCH(text)
	else: results = False
	return results

def MENU():
	addMenuItem('folder',menu_name+'بحث: موقع يوتيوب','',149)
	addMenuItem('folder',menu_name+'الفيديوهات المقترحة',website0a,141)
	addMenuItem('folder',menu_name+'المحتوى الرائج',website0a+'/feed/trending',144)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#addMenuItem('folder',menu_name+'TEST_YOUTUBE','',144)
	addMenuItem('folder',menu_name+'بحث: قنوات عربية','',147)
	addMenuItem('folder',menu_name+'بحث: قنوات أجنبية','',148)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder',menu_name+'بحث: افلام عربية',website0a+'/results?search_query=فيلم',141)
	addMenuItem('folder',menu_name+'بحث: افلام اجنبية',website0a+'/results?search_query=movie',141)
	addMenuItem('folder',menu_name+'بحث: مسلسلات عربية',website0a+'/results?search_query=مسلسل&sp=EgIQAw==',141)
	addMenuItem('folder',menu_name+'بحث: مسلسلات اجنبية',website0a+'/results?search_query=series&sp=EgIQAw==',141)
	addMenuItem('folder',menu_name+'بحث: مسرحيات عربية',website0a+'/results?search_query=مسرحية',141)
	addMenuItem('folder',menu_name+'بحث: مسلسلات كارتون',website0a+'/results?search_query=كارتون&sp=EgIQAw==',141)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder',menu_name+'بحث: خطبة المرجعية',website0a+'/results?search_query=قناة+كربلاء+الفضائية+خطبة+الجمعة&sp=CAISAhAB',141)
	addMenuItem('folder',menu_name+'قناة كربلاء الفضائية',website0a+'/user/karbalatvchannel',146)
	addMenuItem('folder',menu_name+'العراق خطبة المرجعية',website0a+'/playlist?list=PL4jUq6pnG36QjuXDhNnIlriuzroTFtmfr',142)
	addMenuItem('folder',menu_name+'العتبة الحسينية المقدسة',website0a+'/user/ImamHussaindotorg',146)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder',menu_name+'شوف دراما الاولى',website0a+'/channel/UCgd_tWU4X7s10DKdgt-XDNQ',146)
	addMenuItem('folder',menu_name+'شوف دراما الثانية',website0a+'/channel/UC25ZB5ZMqLQwxFDV9FHvF8g',146)
	addMenuItem('folder',menu_name+'شوف دراما الثالثة',website0a+'/channel/UCQOz2_AhxeHUbNMYan-6ZQQ',146)
	addMenuItem('folder',menu_name+'شبكة وطن',website0a+'/user/WatanNetwork',146)
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

def PLAYLIST_ITEMS(url):
	# https://www.youtube.com/watch?v=nMaNCKJCLfE&list=PLbg43835F8ge08Sb_gl6dbdGZzD3hCnQL
	# https://www.youtube.com/playlist?list=PLbg43835F8ge08Sb_gl6dbdGZzD3hCnQL
	html,c = GET_PAGE_DATA(url)
	if c=='': PLAYLIST_ITEMS_OLD(url,html) ; return
	token = ''
	if '/watch?v=' in url:
		listID = re.findall('list=(.*?)&',url+'&',re.DOTALL)
		url = website0a+'/playlist?list='+listID[0]
		html,c = GET_PAGE_DATA(url)
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
		succeeded,title,link,img,count,duration,live,paid = ITEMS_RENDER(item)
		if not succeeded: continue
		addMenuItem('video',menu_name+title,link,143,img,duration)
	if token!='':
		url2 = website0a+'/browse_ajax?ctoken='+token#+'&continuation='+token+'&itct='+param
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,142)
	return

def TRENDING_MENU(url):
	html,c = GET_PAGE_DATA(url)
	d = c['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']
	e = d['contents']
	s = 0
	for i in range(len(e)):
		item = e[i]['itemSectionRenderer']['contents'][0]
		if item['shelfRenderer']['content'].keys()[0]=='horizontalListRenderer': continue
		succeeded,title,link,img,count,duration,live,paid = ITEMS_RENDER(item)
		if title=='':
			s += 1
			title = 'فيديوهات رائجة رقم '+str(s)
		#if not succeeded: continue
		addMenuItem('folder',menu_name+title,url,141,'',str(i))
	e = d['subMenu']['channelListSubMenuRenderer']['contents']
	for i in range(len(e)):
		item = e[i]
		ISERT_ITEM_TO_MENU(item)
	html,c = GET_PAGE_DATA(website0a,request='guide_data')
	d = c['items'][3]['guideSectionRenderer']['items']
	for i in range(len(d)):
		item = d[i]
		ISERT_ITEM_TO_MENU(item)
	return

def CHANNEL_ITEMS(url,page_type,vistordetails):
	html,c = GET_PAGE_DATA(url,vistordetails)
	if c=='': CHANNEL_ITEMS_OLD(url,html) ; return
	not_entry_urls = ['/videos','/playlists','/channels','/featured','ss=','ctoken=','key=','shelf_id=']
	entry_page = any(value in url for value in not_entry_urls)
	if not entry_page:
		if '"title":"الفيديوهات"' in html: addMenuItem('folder',menu_name+'الفيديوهات',url+'/videos',146)
		if '"title":"قوائم التشغيل"' in html: addMenuItem('folder',menu_name+'قوائم التشغيل',url+'/playlists',146)
		if '"title":"القنوات"' in html: addMenuItem('folder',menu_name+'القنوات',url+'/channels',146)#,'','','UPDATE')
		if '"title":"Videos"' in html: addMenuItem('folder',menu_name+'الفيديوهات',url+'/videos',146)
		if '"title":"Playlists"' in html: addMenuItem('folder',menu_name+'قوائم التشغيل',url+'/playlists',146)
		if '"title":"Channels"' in html: addMenuItem('folder',menu_name+'القنوات',url+'/channels',146)#,'','','UPDATE')
	f,g = {},{}
	if 'key=' in url:
		try:
			f = c['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems']
			ff = f[0]
		except: return
	elif 'ctoken=' in url:
		ff = c[1]['response']['continuationContents']['sectionListContinuation']
		f = ff['contents']
	elif 'contents' in str(c):
		d = c['contents']['twoColumnBrowseResultsRenderer']['tabs']
		e = d[0]
		cond1 = '/videos' in url or '/playlists' in url or '/channels' in url
		cond2a = '"title":"الفيديوهات"' in html or '"title":"قوائم التشغيل"' in html or '"title":"القنوات"' in html
		cond2b = '"title":"Videos"' in html or '"title":"Playlists"' in html or '"title":"Channels"' in html
		if cond1 and (cond2a or cond2b):
			for i in range(len(d)):
				if 'tabRenderer' not in d[i].keys(): continue
				ee = d[i]['tabRenderer']
				try: gg = ee['content']['sectionListRenderer']['subMenu']['channelSubMenuRenderer']['contentTypeSubMenuItems'][0]
				except: gg = ee
				try: link = gg['endpoint']['commandMetadata']['webCommandMetadata']['url']
				except: continue
				if   '/videos'		in link	and '/videos'		in url: e = d[i] ; break
				elif '/playlists'	in link	and '/playlists'	in url: e = d[i] ; break
				elif '/channels'	in link	and '/channels'		in url: e = d[i] ; break
		ff = e['tabRenderer']['content']['sectionListRenderer']
		f = ff['contents']
		g = f[0]['itemSectionRenderer']['contents'][0]
	if 'shelf_id' in url:
		shelf_id = url.split('shelf_id=')[1]
		for i in range(len(f)):
			if 'shelf_id='+shelf_id in str(f[i]['itemSectionRenderer']['contents']):
				g = f[i]['itemSectionRenderer']['contents'][0]
				break
	found = False
	# videos shelf list
	if page_type=='1' or (not found and '/videos' in url and 'view=' not in url):
		try:
			f = e['tabRenderer']['content']['sectionListRenderer']['subMenu']
			g = f['channelSubMenuRenderer']['contentTypeSubMenuItems']
			ok = True
		except: ok = False
		if ok:
			for i in range(len(g)):
				try:
					item = g[i]
					title = item['title']
					if title=='All videos': continue
					link = item['endpoint']['commandMetadata']['webCommandMetadata']['url']
					link = website0a+link.replace('\u0026','&')
					addMenuItem('folder',menu_name+title,link,146)
					found = True
				except: pass
			if found: page_type = '1'
	# playlists contents
	if page_type=='2' or (not found and ('/videos' in url or '/playlists' in url or '/channels' in url)):
		try:
			h = g['gridRenderer']['items']
			for i in range(len(h)):
				item = h[i]
				ISERT_ITEM_TO_MENU(item)
				found = True
		except: pass
		if found: page_type = '2'
	# shelf list
	if page_type=='3' or (not found and ('/playlists' in url or '/channels' in url or '/videos' in url) and 'shelf_id=' not in url):
		for i in range(len(f)):
			try:
				item = f[i]['itemSectionRenderer']['contents'][0]
				if 'messageRenderer' in item.keys(): continue
				ISERT_ITEM_TO_MENU(item)
				found = True
			except: pass
		if found: page_type = '3'
	# newer shelf items
	if page_type=='4' or (not found and ('?ss=' in url or '?bp=' in url)):
		try:
			h = g['shelfRenderer']['content']['gridRenderer']['items']
			for i in range(len(h)):
				item = h[i]
				ISERT_ITEM_TO_MENU(item)
				found = True
		except: pass
		if found: page_type = '4'
	# items with section but without link
	if page_type=='5' or (not found and '?bp=' in url):
		for i in range(len(f)):
			if 'itemSectionRenderer' not in f[i].keys(): continue
			g = f[i]['itemSectionRenderer']['contents'][0]['shelfRenderer']
			if 'endpoint' in g.keys(): continue
			if 'horizontalMovieListRenderer' not in g['content'].keys(): continue
			h = g['content']['horizontalMovieListRenderer']['items']
			try: title = g['title']['simpleText']
			except: title = g['title']['runs'][0]['text']
			title = escapeUNICODE(title)
			title = '==  '+title+'  =='
			addMenuItem('link',menu_name+title,'',9999)
			for j in range(len(h)):
				item = h[j]
				ISERT_ITEM_TO_MENU(item)
				found = True
		if found: page_type = '5'
		if not found: CHANNEL_ITEMS(url,'','')
	# home page main categories
	if (page_type=='6' or not found) and 'shelf_id' not in url:
		settings = xbmcaddon.Addon(id=addon_id)
		for i in range(len(f)):
			#xbmcgui.Dialog().ok(str(i),str(len(f)))
			try:
				item = f[i]['itemSectionRenderer']['contents'][0]
				link = item['shelfRenderer']['endpoint']['commandMetadata']['webCommandMetadata']['url']
				if 'ctoken=' not in url or 'shelf_id' not in link:
					ISERT_ITEM_TO_MENU(item)
					pass
				else:
					shelf_id = '&shelf_id='+link.split('shelf_id=')[1]
					title = item['shelfRenderer']['title']['runs'][0]['text']
					link2 = url+shelf_id
					VISITOR_INFO1_LIVE = settings.getSetting('youtube.VISITOR_INFO1_LIVE')
					addMenuItem('folder',menu_name+title,link2,146,'',page_type,VISITOR_INFO1_LIVE)
				found = True
			except: pass
		if found: page_type = '6'
	# trending shelf items
	if page_type=='7' or not found:
		try:
			h = g['shelfRenderer']['content']['horizontalListRenderer']['items']
			ok = True
		except: ok = False
		if ok:
			for i in range(len(h)):
				try:
					item = h[i]
					ISERT_ITEM_TO_MENU(item)
					found = True
				except: pass
			if found: page_type = '7'
	settings = xbmcaddon.Addon(id=addon_id)
	if 'continuations' in ff.keys() and 'shelf_id' not in url:
		continuation = settings.getSetting('youtube.continuation')
		VISITOR_INFO1_LIVE = settings.getSetting('youtube.VISITOR_INFO1_LIVE')
		url2 = website0a+'/browse_ajax?ctoken='+continuation
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,146,'',page_type,VISITOR_INFO1_LIVE)
	elif '"token"' in html:
		key = settings.getSetting('youtube.key')
		visitorData = settings.getSetting('youtube.visitorData')
		url2 = website0a+'/youtubei/v1/browse?key='+key
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,146,'',page_type,visitorData)
	return

def MULTIPLE_TRY(render,in1,in2,in3='',in4='',in5=''):
	in_s = [in1,in2,in3,in4,in5]
	succeeded,out = False,''
	for i in range(5):
		if in_s[i]!='' and succeeded==False:
			try:
				out = eval(in_s[i])
				succeeded = True
				break
			except: pass
	return succeeded,out

def ITEMS_RENDER(item):
	succeeded,title,link,img,count,duration,live,paid = False,'','','','','','',''
	renderName = item.keys()[0]
	render = item[renderName]
	#LOG_THIS('NOTICE','=====================================')
	#LOG_THIS('NOTICE',str(item))
	#xbmcgui.Dialog().ok(render,'')
	in1 = "render['title']['simpleText']"
	in2 = "render['title']['runs'][0]['text']"
	in3 = "render['unplayableText']['simpleText']"
	in4 = "render['formattedTitle']['simpleText']"
	in5 = "render['title']"
	succeeded99,out99 = MULTIPLE_TRY(render,in1,in2,in3,in4,in5)
	if succeeded99: title = out99
	in1 = "render['viewPlaylistText']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']"
	in2 = "render['title']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']"
	in3 = "render['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']"
	in4 = "render['endpoint']['commandMetadata']['webCommandMetadata']['url']"
	succeeded99,out99 = MULTIPLE_TRY(render,in1,in2,in3,in4)
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
		if 'مباشر الآن' in badges: live = 'LIVE:  '
		if '\\xd9\\x85\\xd8\\xa8\\xd8\\xa7\\xd8\\xb4\\xd8\\xb1' in badges: live = 'LIVE:  '
		if 'شراء أو استئجار' in badges: paid = '$$:'
		if '\\xd8\\xb4\\xd8\\xb1\\xd8\\xa7\\xd8\\xa1' in badges: paid = '$$:'
		if '\\xd8\\xa7\\xd8\\xb3\\xd8\\xaa\\xd8\\xa6\\xd8\\xac\\xd8\\xa7\\xd8\\xb1' in badges: paid = '$$:'
		if 'LIVE NOW' in badges: live = 'LIVE:  '
		if 'Buy' in badges or 'Rent' in badges: paid = '$$:'
	if 'http' not in img: img = 'https:'+img
	link = escapeUNICODE(link)
	if link!='' and 'http' not in link: link = website0a+link
	#xbmcgui.Dialog().ok(link,website0a)
	title = escapeUNICODE(title)
	if paid!='': title = paid+'  '+title
	#title = title.replace('\n','')
	#title = unescapeHTML(title)
	count = count.replace(',','')
	count = re.findall('\d+',count)
	if count: count = count[0]
	else: count = ''
	return True,title,link,img,count,duration,live,paid

def TITLES(url,index='0',vistordetails=''):
	html,c = GET_PAGE_DATA(url,vistordetails)
	if c=='': TITLES_OLD(url,html) ; return
	if index=='': index = '0'
	#xbmcgui.Dialog().ok(url,index)
	#LOG_THIS('NOTICE',url)
	#LOG_THIS('NOTICE',html)
	#token = ''
	if 'search_query' in url:
		d = c['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
		for i in range(len(d)):
			try: e = d[i]['itemSectionRenderer']['contents'] ; break
			except: pass
	elif '/search?key=' in url: 
		e = c['onResponseReceivedCommands'][0]['appendContinuationItemsAction']['continuationItems'][0]['itemSectionRenderer']['contents']
	elif '/browse?key=' in url:
		e = c['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems']
	elif '/trending' in url:
		d = c['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][int(index)]['itemSectionRenderer']
		e = d['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items']
	elif '"text":"Recommended"' in html:
		e = c['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['richGridRenderer']['contents']
	elif '"text":"الفيديوهات المقترحة"' in html:
		e = c['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['richGridRenderer']['contents']
	else: e = []
	"""
	elif 'ctoken' in url:
		d = c[1]['response']['continuationContents']['itemSectionContinuation']
		e = d['contents']
		try: token = d['continuations'][0]['nextContinuationData']['continuation']#.replace('=','%253D')
		except: pass
	"""
	for i in range(len(e)):
		try: item = e[i]['richItemRenderer']['content']
		except: item = e[i]
		#if item.keys()[0]=='shelfRenderer': continue
		ISERT_ITEM_TO_MENU(item)
	settings = xbmcaddon.Addon(id=addon_id)
	key = settings.getSetting('youtube.key')
	visitorData = settings.getSetting('youtube.visitorData')
	url2 = ''
	if 'search_query' in url or '/search?key=' in url: url2 = website0a+'/youtubei/v1/search?key='+key
	elif url==website0a or '/browse?key=' in url: url2 = website0a+'/youtubei/v1/browse?key='+key
	if url2!='': addMenuItem('folder',menu_name+'صفحة اخرى',url2,141,'',index,visitorData)
	"""
	if token!='':
		#param = d['continuations'][0]['nextContinuationData']['clickTrackingParams']#.replace('=','%253D')
		if '?' in url: url2 = url+'&pbj=1&ctoken='+token#+'&continuation='+token+'&itct='+param
		else: url2 = url+'?pbj=1&ctoken='+token#+'&continuation='+token+'&itct='+param
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,141)
	"""
	return

def ISERT_ITEM_TO_MENU(item):
	#xbmcgui.Dialog().ok(str(''),str(item))
	succeeded,title,link,img,count,duration,live,paid = ITEMS_RENDER(item)
	#if link==website0a or title=='' or '/gaming' in link: return
	if link=='' and title=='': return
	if   '/trending'	in link: addMenuItem('folder',menu_name+title,link,141,img)
	elif 'list='		in link: addMenuItem('folder',menu_name+'LIST'+count+':  '+title,link,142,img)
	elif '/channel/'	in link or '/c/' in link or '/user/' in link:
		if any(value in link for value in ['/videos','/playlists','/channels','/featured','ss=']):
			addMenuItem('folder',menu_name+title,link,146,img)
		else:
			type = ''
			if '/channel/' in link or '/c/' in link: type = 'CHNL'+count+':  '
			elif '/user/' in link: type = 'USER'+count+':  '
			addMenuItem('folder',menu_name+type+title,link,146,img)
	elif live!='': addMenuItem('live',menu_name+live+title,link,143,img)
	elif 'watch?v=' in link: addMenuItem('video',menu_name+title,link,143,img,duration)
	else: addMenuItem('folder',menu_name+title,link,146)
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

def RANDOM_USERAGENT():
	# https://github.com/lobstrio/shadow-useragent/blob/master/shadow_useragent/core.py
	url = 'http://51.158.74.109/useragents/?format=json'
	response = openURL_requests_cached(VERY_LONG_CACHE,'GET',url,'','','',False,'YOUTUBE-RANDOM_USERAGENT-1st')
	html = response.content
	if '___Error___' in html:
		useragentfile = xbmc.translatePath(os.path.join('special://home/addons/'+addon_id,'arabicvideos','useragents.txt'))
		with open(useragentfile,'r') as f: text = f.read()
		a = re.findall('(Mozilla.*?)\n',text,re.DOTALL)
		b = random.sample(a,1)
		#xbmcgui.Dialog().ok(str(b),str(a))
		useragent = b[0]
	else:
		a = EVAL(html)
		b = random.sample(a,1)
		#xbmcgui.Dialog().ok(str(b),str(a))
		useragent = b[0]['useragent']
	return useragent

def GET_PAGE_DATA(url,vistordetails='',request='initial_data'):
	useragent = RANDOM_USERAGENT()
	headers2 = {'User-Agent':useragent,'Cookie':'PREF=hl=ar'}
	#headers2 = headers.copy()
	settings = xbmcaddon.Addon(id=addon_id)
	if 'key=' in url:
		clientversion = settings.getSetting('youtube.clientversion')
		token = settings.getSetting('youtube.token')
		data = {'continuation':token}
		data['context'] = {"client":{"visitorData":vistordetails,"clientName":"WEB","clientVersion":clientversion}}
		data = str(data)
		response = openURL_requests_cached(VERY_SHORT_CACHE,'POST',url,data,headers2,True,True,'YOUTUBE-GET_PAGE_DATA-1st')
		#xbmcgui.Dialog().ok(url,str(data))
		html = response.content
	elif 'ctoken=' in url:
		clientversion = settings.getSetting('youtube.clientversion')
		headers2.update({'X-YouTube-Client-Name':'1','X-YouTube-Client-Version':clientversion})
		headers2.update({'Cookie':'VISITOR_INFO1_LIVE='+vistordetails})
		response = openURL_requests_cached(VERY_SHORT_CACHE,'GET',url,'',headers2,'','','YOUTUBE-GET_PAGE_DATA-2nd')
		html = response.content
	else:
		response = openURL_requests_cached(VERY_SHORT_CACHE,'GET',url,'',headers2,'','','YOUTUBE-GET_PAGE_DATA-3rd')
		html = response.content
	continuation = re.findall('"continuation".*?"(.*?)"',html,re.DOTALL|re.I)
	if continuation: settings.setSetting('youtube.continuation',continuation[0])
	clientversion = re.findall('"cver".*?"value".*?"(.*?)"',html,re.DOTALL|re.I)
	if clientversion: settings.setSetting('youtube.clientversion',clientversion[0])
	key = re.findall('"innertubeApiKey".*?"(.*?)"',html,re.DOTALL|re.I)
	if key: settings.setSetting('youtube.key',key[0])
	token = re.findall('"token".*?"(.*?)"',html,re.DOTALL|re.I)
	if token: settings.setSetting('youtube.token',token[0])
	visitorData = re.findall('"visitorData".*?"(.*?)"',html,re.DOTALL|re.I)
	if visitorData: settings.setSetting('youtube.visitorData',visitorData[0])
	cookies = response.cookies.get_dict()
	if 'VISITOR_INFO1_LIVE' in cookies.keys(): settings.setSetting('youtube.VISITOR_INFO1_LIVE',cookies['VISITOR_INFO1_LIVE'])
	if request=='initial_data' and 'ytInitialData' in html:
		#xbmcgui.Dialog().ok(url,html)
		a = re.findall('window\["ytInitialData"\] = ({.*?});',html,re.DOTALL)
		b = EVAL(a[0])
	elif request=='guide_data' and 'ytInitialGuideData' in html:
		a = re.findall('var ytInitialGuideData = ({.*?});',html,re.DOTALL)
		b = EVAL(a[0])
	elif '</script>' not in html: b = EVAL(html)
	else: b = ''
	#with open('S:\\00emad.html','w') as f: f.write(html)
	#with open('S:\\00emad.json','w') as f: f.write(str(b))
	#with open('S:\\00emad.json','r') as f: a = f.read() ; b = eval(a)
	return html,b

def SEARCH(search):
	if '::' in search:
		search = search.split('::')[0]
		category = False
	else: category = True
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','%20')
	fileterLIST_search = ['بدون فلتر']
	fileterLIST_sort = []
	linkLIST_search = ['']
	linkLIST_sort = ['']
	#fileterLIST_sort.append('Sort by:  relevance')
	#linkLIST_sort.append('')
	#url2 = 'plugin://plugin.video.youtube/kodion/search/query/?q='+search
	#xbmc.executebuiltin('Dialog.Close(busydialog)')
	#xbmc.executebuiltin('ActivateWindow(videos,'+url2+',return)')
	fileterLIST_sort = ['بدون ترتيب','ترتيب حسب مدى الصلة','ترتيب حسب تاريخ التحميل','ترتيب حسب عدد المشاهدات','ترتيب حسب التقييم']
	linkLIST_sort = ['','&sp=CAA%253D','&sp=CAI%253D','&sp=CAM%253D','&sp=CAE%253D']
	selection_sort = xbmcgui.Dialog().select('اختر الترتيب المناسب:', fileterLIST_sort)
	if selection_sort == -1: return
	link_sort = linkLIST_sort[selection_sort]
	url2 = website0a+'/results?search_query='+search
	html,c = GET_PAGE_DATA(url2+link_sort)
	if c!='':
		d = c['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['subMenu']['searchSubMenuRenderer']['groups']
		for groupID in range(len(d)-1):
			group = d[groupID]['searchFilterGroupRenderer']['filters']
			for filterID in range(len(group)):
				render = group[filterID]['searchFilterRenderer']
				if 'navigationEndpoint' in render.keys():
					link = render['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
					link = link.replace('\u0026','&')
					title = render['tooltip']
					if 'إزالة الفلتر' in title: continue
					if 'Remove' in title: continue
					if 'Playlist' in title: title = 'جيد للمسلسلات '+title
					if 'قائمة تشغيل' in title: title = 'جيد للمسلسلات '+title
					fileterLIST_search.append(escapeUNICODE(title))
					linkLIST_search.append(link)
	"""
	else:
		html_blocks = re.findall('filter-dropdown(.*?)class="item-section',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?title="(.*?)"',block,re.DOTALL)
		for link,title in items:
			if 'Remove' in title: continue
			title = title.replace('Search for','Search for:  ')
			title = title.replace('Sort by','Sort by:  ')
			if 'Playlist' in title: title = 'جيد للمسلسلات '+title
			link = link.replace('\u0026','&')
			if 'Search for:  ' in title:
				fileterLIST_search.append(escapeUNICODE(title))
				linkLIST_search.append(link)
			if 'Sort by:  ' in title:
				fileterLIST_sort.append(escapeUNICODE(title))
				linkLIST_sort.append(link)
	"""
	if category:
		selection_search = xbmcgui.Dialog().select('اختر الفلتر المناسب:', fileterLIST_search)
		if selection_search == -1: return
		link_search = linkLIST_search[selection_search]
		if link_search!='': url3 = website0a+link_search
		elif link_sort!='': url3 = url2+link_sort
		else: url3 = url2
		#xbmcgui.Dialog().ok(url3,'')
	else: url3 = url2
	TITLES(url3)
	return




