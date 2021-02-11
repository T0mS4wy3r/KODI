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
	#elif mode==141: results = MAINPAGE(url)
	#elif mode==142: results = PLAYLIST_ITEMS(url,text)
	elif mode==143: results = PLAY(url,type)
	elif mode==144: results = ITEMS(url,page,text)
	elif mode==145: results = SEARCH_CHANNEL(url)
	elif mode==146: results = TRENDING_MENU(url)
	elif mode==147: results = LIVE_ARABIC()
	elif mode==148: results = LIVE_ENGLISH()
	elif mode==149: results = SEARCH(text)
	else: results = False
	return results

def MENU():
	#url = 'https://www.youtube.com/playlist?list=PLD3XcXKBUszlBtMSwFfZZVTLPKzzprxOS'
	#addMenuItem('folder',menu_name+'TEST YOUTUBE',url,144)
	#addMenuItem('folder',menu_name+'older playlist not listing newer plyalist','https://www.youtube.com/watch?v=XFpqeYzXZfk&list=RDQM63vHjP0heTs',144)
	#addMenuItem('folder',menu_name+'موقع فارغ',website0a+'/channel/UCtOvonj4GyopMTMBa23qUcw',144)
	addMenuItem('folder',menu_name+'بحث في الموقع','',149,'','','_REMEMBERRESULTS_')
	addMenuItem('folder',menu_name+'الصفحة الرئيسية',website0a,144)
	addMenuItem('folder',menu_name+'المحتوى الرائج',website0a+'/feed/trending',146)
	addMenuItem('folder',menu_name+'مواقع اختارها يوتيوب',website0a+'/feed/guide_builder',144)
	addMenuItem('folder','_YTC_'+'مواقع اختارها المبرمج','',290)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder',menu_name+'بحث: قنوات عربية','',147)
	addMenuItem('folder',menu_name+'بحث: قنوات أجنبية','',148)
	addMenuItem('folder',menu_name+'بحث: افلام عربية',website0a+'/results?search_query=فيلم',144)
	addMenuItem('folder',menu_name+'بحث: افلام اجنبية',website0a+'/results?search_query=movie',144)
	addMenuItem('folder',menu_name+'بحث: مسرحيات عربية',website0a+'/results?search_query=مسرحية',144)
	addMenuItem('folder',menu_name+'بحث: مسلسلات عربية',website0a+'/results?search_query=مسلسل&sp=EgIQAw==',144)
	addMenuItem('folder',menu_name+'بحث: مسلسلات اجنبية',website0a+'/results?search_query=series&sp=EgIQAw==',144)
	addMenuItem('folder',menu_name+'بحث: مسلسلات كارتون',website0a+'/results?search_query=كارتون&sp=EgIQAw==',144)
	addMenuItem('folder',menu_name+'بحث: خطبة المرجعية',website0a+'/results?search_query=قناة+كربلاء+الفضائية+خطبة+الجمعة&sp=CAISAhAB',144)
	addMenuItem('folder',menu_name+'العراق خطبة المرجعية',website0a+'/playlist?list=PL4jUq6pnG36QjuXDhNnIlriuzroTFtmfr',144)
	#addMenuItem('folder',menu_name+'اعدادات اضافة يوتيوب','',144)
	#yes = DIALOG_YESNO('هل تريد الاستمرار ؟','هذا الاختيار سوف يخرجك من البرنامج','لأنه سوف يقوم بتشغيل برنامج يوتيوب')
	#if yes:
	#	url = 'plugin://plugin.video.youtube'
	#	xbmc.executebuiltin('Dialog.Close(busydialog)')
	#	xbmc.executebuiltin('ReplaceWindow(videos,'+url+')')
	#	#xbmc.executebuiltin('RunAddon(plugin.video.youtube)')
	return

"""
def MAINPAGE(url):
	html,cc = GET_PAGE_DATA(url)
	if 'Refaat Al-Gammal' in html: DIALOG_OK(url,'yes')
	dd = cc['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['richGridRenderer']['header']['feedFilterChipBarRenderer']['contents']
	for i in rnage(len(dd)):
		item = dd[i]
		INSERT_ITEM_TO_MENU(item)
	ITEMS(url)
	return
"""

def LIVE_ARABIC():
	ITEMS(website0a+'/results?search_query=قناة+بث&sp=EgJAAQ==')
	return

def LIVE_ENGLISH():
	ITEMS(website0a+'/results?search_query=tv&sp=EgJAAQ==')
	return

def PLAY(url,type):
	#url = url+'&'
	#items = re.findall('v=(.*?)&',url,re.DOTALL)
	#id = items[0]
	#DIALOG_OK(url,'')
	#link = 'plugin://plugin.video.youtube/play/?video_id='+id
	#PLAY_VIDEO(link,script_name,'video')
	linkLIST = [url]
	import RESOLVERS
	result = RESOLVERS.PLAY(linkLIST,script_name,type)
	if 'RETURN_TO_YOUTUBE' in result:
		link = website0a+result.split('::')[1]
		#DIALOG_OK(link,result)
		new_path = sys.argv[0]+'?type=folder&mode=144&url='+link
		xbmc.executebuiltin("Container.Update("+new_path+")")
		#threads = CustomThread(False,False)
		#threads.start_new_thread('1',xbmc.executebuiltin,"Container.Update("+new_path+")")
		#DIALOG_OK(link,str(len(KodiMenuList)))
		#LOG_THIS('NOTICE','EMAD EMAD 9999: '+new_path)
	return

def TRENDING_MENU(url):
	html,cc = GET_PAGE_DATA(url)
	dd = cc['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']
	ee = dd['contents']
	s = 0
	for i in range(len(ee)):
		item = ee[i]['itemSectionRenderer']['contents'][0]
		if item['shelfRenderer']['content'].keys()[0]=='horizontalListRenderer': continue
		succeeded,title,link,img,count,duration,live,paid = RENDER(item)
		if title=='':
			s += 1
			title = 'فيديوهات رائجة '+str(s)
		addMenuItem('folder',menu_name+title,url,144,'',str(i))
	ee = dd['subMenu']['channelListSubMenuRenderer']['contents']
	for i in range(len(ee)):
		item = ee[i]
		INSERT_ITEM_TO_MENU(item)
	#DIALOG_OK(str(url2),str(dd))
	#LOG_THIS('NOTICE','EMAD ==== '+dd)
	key = re.findall('"innertubeApiKey":"(.*?)"',html,re.DOTALL)
	url2 = 'https://www.youtube.com/youtubei/v1/guide?key='+key[0]
	html,cc = GET_PAGE_DATA(url2)
	for j in range(3,4):
		dd = cc['items'][j]['guideSectionRenderer']['items']
		for i in range(len(dd)):
			item = dd[i]
			if 'YouTube Premium' in str(item): continue
			INSERT_ITEM_TO_MENU(item)
	return

def ITEMS(url,index='',visitor=''):
	#DIALOG_OK(url,index)
	global settings
	html,cc = GET_PAGE_DATA(url,visitor)
	ownerNAME,ff = '',''
	#if 'owner' in html.lower(): DIALOG_OK('owner exist','in html')
	owner = re.findall('"ownerName".*?":"(.*?)".*?"url":"(.*?)"',html,re.DOTALL)
	if not owner: owner = re.findall('"videoOwner".*?"text":"(.*?)".*?"url":"(.*?)"',html,re.DOTALL)
	if not owner: owner = re.findall('"channelMetadataRenderer":\{"title":"(.*?)".*?"ownerUrls":\["(.*?)"',html,re.DOTALL)
	if owner:
		ownerNAME = '[COLOR FFC89008]'+owner[0][0]+'[/COLOR]'
		link = owner[0][1]
		if 'http' not in link: link = website0a+link
		#if '/playlists' in url and '/channel/' not in url and '/c/' not in url and '/user/' not in url:
		if 'list=' in url: addMenuItem('folder',menu_name+ownerNAME,link,144)
	#if cc=='': CHANNEL_ITEMS_OLD(url,html) ; return
	not_entry_urls = ['/search','/videos','/channels','/playlists','/featured','ss=','ctoken=','key=','bp=','shelf_id=']
	channels_entry_page = not any(value in url for value in not_entry_urls)
	if channels_entry_page:
		if '"title":"بحث"' in html: addMenuItem('folder',menu_name+'بحث في هذا الموقع',url,145,'','','_REMEMBERRESULTS_')
		if '"title":"قوائم التشغيل"' in html: addMenuItem('folder',menu_name+' - قوائم'+ownerNAME,url+'/playlists',144)
		if '"title":"الفيديوهات"' in html: addMenuItem('folder',menu_name+' - فيديوهات'+ownerNAME,url+'/videos',144)
		if '"title":"القنوات"' in html: addMenuItem('folder',menu_name+' - قنوات'+ownerNAME,url+'/channels',144)
		if '"title":"Search"' in html: addMenuItem('folder',menu_name+'بحث في هذا الموقع',url,145,'','','_REMEMBERRESULTS_')
		if '"title":"Playlists"' in html: addMenuItem('folder',menu_name+' - قوائم'+ownerNAME,url+'/playlists',144)
		if '"title":"Videos"' in html: addMenuItem('folder',menu_name+' - فيديوهات'+ownerNAME,url+'/videos',144)
		if '"title":"Channels"' in html: addMenuItem('folder',menu_name+' - قنوات'+ownerNAME,url+'/channels',144)
	if 'search_query' in url:
		dd = cc['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
		biggest = 0
		for i in range(len(dd)):
			if 'itemSectionRenderer' in dd[i].keys():
				fff = dd[i]['itemSectionRenderer']
				length = len(str(fff))
				if length>biggest:
					biggest = length
					ff = fff
		if biggest==0: return
	elif '&list=' in url or '/search?key=' in url or '/browse?key=' in url or 'ctoken=' in url or '/search' in url or url==website0a:
		trial = []
		trial.append("cc['onResponseReceivedCommands'][0]['appendContinuationItemsAction']['continuationItems'][0]['itemSectionRenderer']")
		trial.append("cc['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems']")
		trial.append("cc[1]['response']['continuationContents']['sectionListContinuation']")
		trial.append("cc[1]['response']['continuationContents']['gridContinuation']['items']")  # required for channels items
		trial.append("cc[1]['response']['continuationContents']['playlistVideoListContinuation']")
		trial.append("cc['contents']['twoColumnBrowseResultsRenderer']['tabs'][-1]['expandableTabRenderer']['content']['sectionListRenderer']")
		trial.append("cc['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['richGridRenderer']")
		trial.append("cc['contents']['twoColumnWatchNextResults']['playlist']['playlist']")
		succeeded99,ff = TRY_MULITPLE(cc,cc,trial)
		#DIALOG_OK('0000 index= '+index,'found in '+succeeded99)
	if ff=='':
		try:
			dd = cc['contents']['twoColumnBrowseResultsRenderer']['tabs']
			cond1 = '/videos' in url or '/playlists' in url or '/channels' in url
			cond2a = '"title":"الفيديوهات"' in html or '"title":"قوائم التشغيل"' in html or '"title":"القنوات"' in html
			cond2b = '"title":"Videos"' in html or '"title":"Playlists"' in html or '"title":"Channels"' in html
			if cond1 and (cond2a or cond2b):
				for i in range(len(dd)):
					if 'tabRenderer' not in dd[i].keys(): continue
					ee = dd[i]['tabRenderer']
					try: gg = ee['content']['sectionListRenderer']['subMenu']['channelSubMenuRenderer']['contentTypeSubMenuItems'][0]
					except: gg = ee
					try: link = gg['endpoint']['commandMetadata']['webCommandMetadata']['url']
					except: continue
					if   '/videos'		in link	and '/videos'		in url: ee = dd[i] ; break
					elif '/playlists'	in link	and '/playlists'	in url: ee = dd[i] ; break
					elif '/channels'	in link	and '/channels'		in url: ee = dd[i] ; break
					else: ee = dd[0]
			else: ee = dd[0]
			ff = ee['tabRenderer']['content']['sectionListRenderer']
		except: pass
	if ff=='': return
	#DIALOG_OK(url,'index='+index)
	trial = []
	trial.append("ff['contents'][int(index)]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items']")
	trial.append("ff['contents'][int(index)]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['horizontalMovieListRenderer']['items']")
	trial.append("ff['contents'][int(index)]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['horizontalListRenderer']['items']")
	trial.append("ff['contents'][int(index)]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['gridRenderer']['items']")
	trial.append("ff['contents'][int(index)]['itemSectionRenderer']['contents'][0]['shelfRenderer']['cards']")
	trial.append("ff['contents'][int(index)]['itemSectionRenderer']['contents'][0]['horizontalCardListRenderer']['cards']")
	trial.append("ff['contents'][int(index)]['richSectionRenderer']['content']")
	if 'view=' not in url: trial.append("ff['subMenu']['channelSubMenuRenderer']['contentTypeSubMenuItems']")  # required for channels submenu
	trial.append("ff['contents'][0]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items']")
	trial.append("ff['contents'][0]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['gridRenderer']['items']")
	trial.append("ff['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']")
	trial.append("ff['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']")  # required for channels items
	trial.append("ff['contents']")
	trial.append("ff")  # required for channels items
	str1 = ARABIC_HEX(u'كل قوائم التشغيل')
	str2 = ARABIC_HEX(u'كل الفيديوهات')
	str3 = ARABIC_HEX(u'كل القنوات')
	list1 = [str1,str2,str3,'All playlists','All videos','All channels']
	succeeded88,gg = TRY_MULITPLE(ff,index,trial)
	#DIALOG_OK('1111 index= '+index+'   found in '+succeeded88,str(len(gg)))
	#DIALOG_TEXTVIEWER('',str(gg))
	#DIALOG_OK('',str(len(gg)))
	if 'list' in str(type(gg)) and any(value in str(gg[0]) for value in list1): del gg[0]
	for index2 in range(len(gg)):
		trial = []
		trial.append("gg[index2]['itemSectionRenderer']['contents'][0]['horizontalCardListRenderer']['header']")  # shuld be 1st		#1
		trial.append("gg[index2]['itemSectionRenderer']['header']")  # should be 2nd		required for trending gaming		#2
		trial.append("gg[index2]['horizontalCardListRenderer']['header']")  # should be 3rd		required for trending movies	#3
		trial.append("gg[index2]['itemSectionRenderer']['contents'][0]")		#4
		trial.append("gg[index2]['richSectionRenderer']['content']")		#7
		trial.append("gg[index2]['richItemRenderer']['content']")		#6
		trial.append("gg[index2]['gameCardRenderer']['game']")		#5
		trial.append("gg[index2]")  # required for channels submenu & items		#8
		succeeded99,item = TRY_MULITPLE(gg,index2,trial)
		#DIALOG_OK('2222 index= '+index,'found in '+succeeded99)
		#if succeeded99 not in ['2','4','5']: INSERT_ITEM_TO_MENU(item)		# 2,4,7
		#else: INSERT_ITEM_TO_MENU(item,url,str(index2),visitor)
		INSERT_ITEM_TO_MENU(item,url,str(index2),visitor)
		if succeeded99=='4':
			try:
				hh = item['shelfRenderer']['content']['horizontalMovieListRenderer']['items']
				for index3 in range(len(hh)):
					item2 = hh[index3]
					INSERT_ITEM_TO_MENU(item2)
			except: pass
	submenu = False
	if 'view=' not in url and succeeded88=='8': submenu = True
	if '&list=' not in url and '"continuations"' in html and not submenu and 'shelf_id' not in url:	# and (index!='' or 'ctoken=' in url or 'list=' in url or 'search?query=' in url or 'view=' in url):
		continuation = settings.getSetting('youtube.continuation')
		VISITOR_INFO1_LIVE = settings.getSetting('youtube.VISITOR_INFO1_LIVE')
		url2 = website0a+'/browse_ajax?ctoken='+continuation
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,144,'','',VISITOR_INFO1_LIVE)
	elif '"token"' in html and 'bp=' not in url:
		key = settings.getSetting('youtube.key')
		visitorData = settings.getSetting('youtube.visitorData')
		if 'search_query' in url or 'search?key=' in url: url2 = website0a+'/youtubei/v1/search?key='+key
		else: url2 = website0a+'/youtubei/v1/browse?key='+key
		addMenuItem('folder',menu_name+'صفحة اخرى',url2,144,'','',visitorData)
	#DIALOG_OK('YOUTUBE.ITEMS() size',str(len(menuItemsLIST)))
	return

def TRY_MULITPLE(var1,var2,try_list):
	#DIALOG_TEXTVIEWER('multi try',str(counter))
	cc,cc = var1,var2
	gg,index2 = var1,var2
	ff,index = var1,var2
	item,render = var1,var2
	count = len(try_list)
	for counter in range(count):
		try:
			out = eval(try_list[counter])
			return str(counter+1),out
		except: pass
	return '',''

def RENDER(item):
	try: renderName = item.keys()[0]
	except: return False,'','','','','','',''
	succeeded,title,link,img,count,duration,live,paid = False,'','','','','','',''
	render = item[renderName]
	#LOG_THIS('NOTICE',str(item))
	#DIALOG_OK('badges','exist')
	trial = []
	trial.append("render['unplayableText']['simpleText']")
	trial.append("render['formattedTitle']['simpleText']")
	trial.append("render['title']['simpleText']")
	trial.append("render['title']['runs'][0]['text']")
	trial.append("render['text']['simpleText']")
	trial.append("render['text']['runs'][0]['text']")
	trial.append("render['title']")
	trial.append("item['title']")  # required for channels submenus
	succeeded99,title = TRY_MULITPLE(item,render,trial)
	trial = []
	trial.append("render['title']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']")
	trial.append("render['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']")
	trial.append("render['endpoint']['commandMetadata']['webCommandMetadata']['url']")
	trial.append("item['endpoint']['commandMetadata']['webCommandMetadata']['url']") # required for channels submenu
	succeeded99,link = TRY_MULITPLE(item,render,trial)
	#DIALOG_OK('render link:  '+link,'found in '+succeeded99)
	trial = []
	trial.append("render['thumbnail']['thumbnails'][0]['url']")
	trial.append("render['thumbnails'][0]['thumbnails'][0]['url']")
	succeeded99,img = TRY_MULITPLE(item,render,trial)
	trial = []
	trial.append("render['videoCount']")
	trial.append("render['videoCountText']['runs'][0]['text']")
	trial.append("render['thumbnailOverlays'][0]['thumbnailOverlayBottomPanelRenderer']['text']['runs'][0]['text']")
	succeeded99,count = TRY_MULITPLE(item,render,trial)
	trial = []
	trial.append("render['lengthText']['simpleText']")
	trial.append("render['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText']")
	trial.append("render['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['runs'][0]['text']")
	succeeded99,duration = TRY_MULITPLE(item,render,trial)
	if 'LIVE' in duration: duration,live = '','LIVE:  '
	if 'مباشر' in duration: duration,live = '','LIVE:  '
	if 'badges' in render.keys():
		badges = str(render['badges'])
		if 'Free with Ads' in badges: paid = '$:'
		if 'LIVE NOW' in badges: live = 'LIVE:  '
		if 'Buy' in badges or 'Rent' in badges: paid = '$$:'
		if ARABIC_HEX(u'مباشر') in badges: live = 'LIVE:  '
		if ARABIC_HEX(u'شراء') in badges: paid = '$$:'
		if ARABIC_HEX(u'استئجار') in badges: paid = '$$:'
		if ARABIC_HEX(u'إعلانات') in badges: paid = '$:'
	if 'http' not in img and img!='': img = 'https:'+img
	link = escapeUNICODE(link)
	if link!='' and 'http' not in link: link = website0a+link
	title = escapeUNICODE(title)
	if paid!='': title = paid+'  '+title
	#title = unescapeHTML(title)
	duration = duration.replace(',','')
	count = count.replace(',','')
	count = re.findall('\d+',count)
	if count: count = count[0]
	else: count = ''
	return True,title,link,img,count,duration,live,paid

def INSERT_ITEM_TO_MENU(item,url='',index='',visitor=''):
	succeeded,title,link,img,count,duration,live,paid = RENDER(item)
	#DIALOG_TEXTVIEWER('',str(item))
	#DIALOG_OK(link,url)
	#DIALOG_OK(index,visitor)
	#if '/feed/guide_builder' in url and index=='0':
	#	addMenuItem('folder',menu_name+title,url,144)
	#	return
	if not succeeded: return
	elif 'continuationItemRenderer' in str(item): return	# continuation not items
	elif 'searchPyvRenderer' in str(item): return			# ads not items
	elif link=='' and 'search_query' in url: return			# separator horizontal list not items
	elif title!='' and link=='' and ('search_query' in url or 'horizontalMovieListRenderer' in str(item) or url==website0a):
		title = '=== '+title+' ==='
		addMenuItem('link',menu_name+title,'',9999)
	elif title!='' and 'messageRenderer' in str(item):
		addMenuItem('link',menu_name+title,'',9999)
	elif '/feed/trending' in link and 'bp=' not in link: return #addMenuItem('folder',menu_name+title,link,146)
	elif title=='': return
	elif live!='': addMenuItem('live',menu_name+live+title,link,143,img)
	elif 'list=' in link and 'index=' not in link and 't=0' not in link:
		listID = re.findall('list=(.*?)&',link+'&',re.DOTALL)
		link = website0a+'/playlist?list='+listID[0]
		addMenuItem('folder',menu_name+'LIST'+count+':  '+title,link,144,img)
	elif 'watch?v=' in link:
		if 'list=' in link and 'index=' not in link:
			addMenuItem('folder',menu_name+'LIST'+count+':  '+title,link,144,img)
		else: addMenuItem('video',menu_name+title,link,143,img,duration)
	else:
		type = ''
		if link=='': link = url
		#if 'ss=' in link: link = url
		#elif 'shelf_id=' in link: link = url		# not needed it will stop opening channels submenu
		elif not any(value in link for value in ['/videos','/playlists','/channels','/featured','ss=','bp=']):
			if '/channel/'	in link or '/c/' in link: type = 'CHNL'+count+':  '
			if '/user/' in link: type = 'USER'+count+':  '
			index,visitor = '',''
		addMenuItem('folder',menu_name+type+title,link,144,img,index,visitor)
	return

def GET_PAGE_DATA(url,visitor='',request=''):
	#if '__' in visitor: visitor = ''
	#if 'ss=' in url: url = url.split('ss=')[0]
	if request=='': request = 'ytInitialData'
	global settings
	useragent = RANDOM_USERAGENT()
	headers2 = {'User-Agent':useragent,'Cookie':'PREF=hl=ar'}
	#headers2 = headers.copy()
	if 'guide?key=' in url:
		clientversion = settings.getSetting('youtube.clientversion')
		data = {}
		data['context'] = {"client":{"hl":"ar","clientName":"WEB","clientVersion":clientversion}}
		data = str(data)
		response = OPENURL_REQUESTS_CACHED(VERY_SHORT_CACHE,'POST',url,data,headers2,True,True,'YOUTUBE-GET_PAGE_DATA-1st')
		#DIALOG_OK(url,str(data))
		html = response.content
	elif 'key=' in url and visitor!='':
		settings.setSetting('youtube.visitorData',visitor)
		clientversion = settings.getSetting('youtube.clientversion')
		token = settings.getSetting('youtube.token')
		data = {'continuation':token}
		data['context'] = {"client":{"visitorData":visitor,"clientName":"WEB","clientVersion":clientversion}}
		data = str(data)
		response = OPENURL_REQUESTS_CACHED(VERY_SHORT_CACHE,'POST',url,data,headers2,True,True,'YOUTUBE-GET_PAGE_DATA-1st')
		#DIALOG_OK(url,str(data))
		html = response.content
	elif 'ctoken=' in url and visitor!='':
		clientversion = settings.getSetting('youtube.clientversion')
		headers2.update({'X-YouTube-Client-Name':'1','X-YouTube-Client-Version':clientversion})
		headers2.update({'Cookie':'VISITOR_INFO1_LIVE='+visitor})
		response = OPENURL_REQUESTS_CACHED(VERY_SHORT_CACHE,'GET',url,'',headers2,'','','YOUTUBE-GET_PAGE_DATA-2nd')
		html = response.content
	else:
		response = OPENURL_REQUESTS_CACHED(VERY_SHORT_CACHE,'GET',url,'',headers2,'','','YOUTUBE-GET_PAGE_DATA-3rd')
		html = response.content
	visitorData = re.findall('"visitorData".*?"(.*?)"',html,re.DOTALL|re.I)
	if visitorData: settings.setSetting('youtube.visitorData',visitorData[0])
	key = re.findall('"innertubeApiKey".*?"(.*?)"',html,re.DOTALL|re.I)
	if key: settings.setSetting('youtube.key',key[0])
	continuation = re.findall('"continuation".*?"(.*?)"',html,re.DOTALL|re.I)
	if continuation: settings.setSetting('youtube.continuation',continuation[0])
	clientversion = re.findall('"cver".*?"value".*?"(.*?)"',html,re.DOTALL|re.I)
	if clientversion: settings.setSetting('youtube.clientversion',clientversion[0])
	token = re.findall('"token".*?"(.*?)"',html,re.DOTALL|re.I)
	if token: settings.setSetting('youtube.token',token[0])
	cookies = response.cookies.get_dict()
	if 'VISITOR_INFO1_LIVE' in cookies.keys():
		settings.setSetting('youtube.VISITOR_INFO1_LIVE',cookies['VISITOR_INFO1_LIVE'])
	if request=='ytInitialData' and 'ytInitialData' in html:
		#DIALOG_OK(url,html)
		aa = re.findall('window\["ytInitialData"\] = ({.*?});',html,re.DOTALL)
		if not aa: aa = re.findall('var ytInitialData = ({.*?});',html,re.DOTALL)
		bb = EVAL(aa[0])
	elif request=='ytInitialGuideData' and 'ytInitialGuideData' in html:
		aa = re.findall('var ytInitialGuideData = ({.*?});',html,re.DOTALL)
		bb = EVAL(aa[0])
	elif '</script>' not in html: bb = EVAL(html)
	else: bb = ''
	#with open('S:\\00emad.json','w') as f: f.write(str(bb))
	#with open('S:\\00emad.json','r') as f: aa = f.read() ; bb = eval(aa)
	#with open('S:\\00emad.html','w') as f: f.write(html)
	#with open('S:\\00emad.dat','w') as f: f.write(str(aa))
	return html,bb

def SEARCH_CHANNEL(url):
	search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','+')
	url2 = url+'/search?query='+search
	ITEMS(url2)
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','+')
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
	if showdialogs:
		selection_sort = DIALOG_SELECT('اختر الترتيب المناسب:', fileterLIST_sort)
		if selection_sort == -1: return
		link_sort = linkLIST_sort[selection_sort]
	else: link_sort = ''
	url2 = website0a+'/results?search_query='+search
	html,c = GET_PAGE_DATA(url2+link_sort)
	if c!='':
		d = c['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['subMenu']['searchSubMenuRenderer']['groups']
		for groupID in range(len(d)):
			group = d[groupID]['searchFilterGroupRenderer']['filters']
			for filterID in range(len(group)):
				render = group[filterID]['searchFilterRenderer']
				if 'navigationEndpoint' in render.keys():
					link = render['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
					link = link.replace('\u0026','&')
					title = render['tooltip']
					title = title.replace('البحث عن ','')
					if 'إزالة الفلتر' in title: continue
					if 'قائمة تشغيل' in title: title = 'جيد للمسلسلات '+title
					if 'ترتيب حسب' in title: continue
					title = title.replace('Search for ','')
					if 'Remove' in title: continue
					if 'Playlist' in title: title = 'جيد للمسلسلات '+title
					if 'Sort by' in title: continue
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
	if showdialogs:
		selection_search = DIALOG_SELECT('اختر الفلتر المناسب:',fileterLIST_search)
		if selection_search == -1: return
		link_search = linkLIST_search[selection_search]
		if link_search!='': url3 = website0a+link_search
		elif link_sort!='': url3 = url2+link_sort
		else: url3 = url2
		#DIALOG_OK(url3,'')
	else: url3 = url2
	ITEMS(url3)
	return
