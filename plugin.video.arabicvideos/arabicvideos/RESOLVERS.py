# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='RESOLVERS'
doNOTresolveMElist = [ 'mystream','vimple','vidbom' ]

def MAIN(mode,url,text):
	if mode==160: PLAY_LINK(url,text)
	return

def PLAY(linkLIST,script_name):
	serversLIST,urlLIST = SERVERS_cached(linkLIST,script_name)
	#xbmcgui.Dialog().ok('',str(urlLIST))
	if len(serversLIST)==0: result = 'unresolved'
	else:
		while True:
			if len(serversLIST)==1: selection = 0
			else: selection = xbmcgui.Dialog().select('اختر السيرفر المناسب', serversLIST)
			if selection == -1: result = 'canceled1'
			else:
				title = serversLIST[selection]
				#xbmcgui.Dialog().ok(str(urlLIST[selection]),str(urlLIST[selection]))
				if 'سيرفر عام مجهول' in title:
					import PROBLEMS
					PROBLEMS.MAIN(156)
					result = 'unresolved'
				else:
					url = urlLIST[selection]
					result = PLAY_LINK(url,script_name)
			if result in ['playing','canceled1'] or len(serversLIST)==1: break
			elif result in ['failed','timeout','tried']: break
			elif result not in ['canceled2','https']: xbmcgui.Dialog().ok('السيرفر لم يعمل','جرب سيرفر غيره')
	if result=='unresolved' and len(serversLIST)>0: xbmcgui.Dialog().ok('سيرفر هذا الفيديو لم يعمل','جرب فيديو غيره')
	elif result in ['failed','timeout']: xbmcgui.Dialog().ok('الفيديو لم يعمل',' ')
	"""
	elif result in ['Canceled1','Canceled2']:
		#xbmc.log('['+addon_id+']:  Test:  '+sys.argv[0]+sys.argv[2], level=xbmc.LOGNOTICE)
		xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem())
		play_item = xbmcgui.ListItem(path='plugin://plugin.video.arabicvideos/?mode=143&url=https://www.youtube.com/watch%3Fv%3Dgwb1pxVtw9Q')
		xbmc.Player().play('https://flv1.alarab.com/iphone/123447.mp4',play_item)
		#xbmcgui.Dialog().ok('تم الالغاء','')
	"""
	return result
	#if script_name=='HALACIMA': menu_name='HLA [/COLOR]'
	#elif script_name=='4HELAL': menu_name='[COLOR FFC89008]HEL [/COLOR]'
	#elif script_name=='AKOAM': menu_name='[COLOR FFC89008]AKM [/COLOR]'
	#elif script_name=='SHAHID4U': menu_name='[COLOR FFC89008]SHA '
	#size = len(urlLIST)
	#for i in range(0,size):
	#	title = serversLIST[i]
	#	link = urlLIST[i]
	#	addLink(menu_name+title,link,160,'','',script_name)
	#xbmcplugin.endOfDirectory(addon_handle)

def PLAY_LINK(url,script_name):
	url = url.strip(' ')
	videofiletype = re.findall('(.mp4|.m3u|.m3u8|.mpd|.mkv)(|\?.*?|/\?.*?|\|.*?)&&',url+'&&',re.DOTALL)
	if videofiletype: result = PLAY_VIDEO(url,script_name,'yes')
	else:
		titleLIST,linkLIST = RESOLVE_cached(url)
		#xbmcgui.Dialog().ok(url,str(linkLIST))
		if not linkLIST: result = 'unresolved'
		else:
			while True:
				if len(linkLIST)==1: selection = 0
				else: selection = xbmcgui.Dialog().select('اختر الملف المناسب:', titleLIST)
				if selection == -1: result = 'canceled2'
				else:
					videoURL = linkLIST[selection]
					if 'moshahda.' in videoURL and 'download_orig' in videoURL:
						videoURL1,videoURL2 = MOVIZLAND(videoURL)
						if videoURL2: videoURL = videoURL2[0]
						else: videoURL = ''
					if videoURL=='': result = 'unresolved'
					else: result = PLAY_VIDEO(videoURL,script_name,'yes')
				if result in ['playing','canceled2'] or len(linkLIST)==1: break
				elif result in ['failed','timeout','tried']: break
				else: xbmcgui.Dialog().ok('الملف لم يعمل','جرب ملف غيره')
			if 'youtube.mpd' in linkLIST[0]:
				#xbmcgui.Dialog().ok('click ok to take down the http server','')
				#html = openURL_cached(NO_CACHE,'http://localhost:64000/shutdown','','','','RESOLVERS-PLAY_LINK-1st')
				titleLIST[0].shutdown()
	return result
	#title = xbmc.getInfoLabel( "ListItem.Label" )
	#if 'سيرفر عام مجهول' in title:
	#	import PROBLEMS
	#	PROBLEMS.MAIN(156)
	#	return ''

def CHECK(url):
	result = 'unknown'
	if   '1fichier'		in url: result = 'known'
	elif '4helal'		in url: result = 'known'
	elif 'allmyvideos'	in url: result = 'known'
	elif 'allvid'		in url: result = 'known'
	elif 'bestcima'		in url: result = 'known'
	elif 'cloudy.ec'	in url: result = 'known'
	elif 'dailymotion'	in url: result = 'known'
	elif 'downace'		in url: result = 'known'
	#elif 'estream'		in url: result = 'known'
	elif 'filerio'		in url: result = 'known'
	elif 'firedrive'	in url: result = 'known'
	elif 'flashx'		in url: result = 'known'
	elif 'govid'		in url: result = 'known'
	elif 'hqq'			in url: result = 'known'
	elif 'media4up'		in url: result = 'known'
	#elif 'mystream'		in url: result = 'known'
	elif 'nitroflare'	in url: result = 'known'
	elif 'nowvideo'		in url: result = 'known'
	elif 'ok.ru'		in url: result = 'known'
	elif 'oload'		in url: result = 'known'
	elif 'openload'		in url: result = 'known'
	elif 'streamango'	in url: result = 'known'
	elif 'streamin'		in url: result = 'known'
	elif 'streammango'	in url: result = 'known'
	elif 'thevid.net'	in url: result = 'known'
	elif 'upload'		in url: result = 'known'
	elif 'uptobox'		in url: result = 'known'
	elif 'videobam'		in url: result = 'known'
	elif 'videorev'		in url: result = 'known'
	elif 'vidfast'		in url: result = 'known'
	elif 'vidgg'		in url: result = 'known'
	elif 'vidlox'		in url: result = 'known'
	elif 'vidzi'		in url: result = 'known'
	elif 'watchers'		in url: result = 'known'
	elif 'watchers.to'	in url: result = 'known'
	elif 'wintv.live'	in url: result = 'known'
	elif 'youwatch'		in url: result = 'known'
	elif 'vidto.me'		in url: result = 'known'
	elif 'archive'		in url: result = 'known'
	elif 'publicvideohost' in url: result = 'known'
	#elif 'vidbom'		in url: result = 'known'
	else:
		link = 'http://emadmahdi.pythonanywhere.com/check?url=' + url
		result = openURL_cached(SHORT_CACHE,link,'','','','RESOLVERS-CHECK-1st')
	return result

def RESOLVABLE(url):
	url2 = url.lower()
	result1,result2,result3 = '','',''
	if   any(value in url2 for value in doNOTresolveMElist): return ''
	elif 'go.akoam.net'	in url2 and 'name=' not in url2: result1 = 'akoam'
	elif 'go.akoam.net'	in url2 and 'name=' in url2: result3 = url2.split('name=')[1]
	elif 'shahid4u.net'	in url2 and 'name=' in url2: result3 = url2.split('name=')[1]
	elif 'e5tsar'		in url2 and 'name=' in url2: result3 = url2.split('name=')[1]
	elif '://moshahda.'	in url2: result1 = 'movizland'
	elif 'arabloads'	in url2: result1 = 'arabloads'
	elif 'archive'		in url2: result1 = 'archive'
	elif 'catch.is'	 	in url2: result1 = 'catch'
	#elif 'estream'	 	in url2: result1 = 'estream'
	elif 'filerio'		in url2: result1 = 'filerio'
	elif 'gounlimited'	in url2: result1 = 'gounlimited'
	elif 'govid'		in url2: result1 = 'govid'
	#elif 'intoupload' 	in url2: result1 = 'intoupload'
	elif 'liivideo' 	in url2: result1 = 'liivideo'
	elif 'mp4upload'	in url2: result1 = 'mp4upload'
	elif 'publicvideohost' in url2: result1 = 'publicvideohost'
	elif 'rapidvideo' 	in url2: result1 = 'rapidvideo'
	elif 'thevideo'		in url2: result1 = 'thevideo'
	elif 'top4top'		in url2: result1 = 'top4top'
	elif 'upbom' 		in url2: result1 = 'upbom'
	elif 'uppom' 		in url2: result1 = 'uppom'
	elif 'uptobox' 		in url2: result1 = 'uptobox'
	elif 'uptostream'	in url2: result1 = 'uptostream'
	elif 'uqload' 		in url2: result1 = 'uqload'
	elif 'vcstream' 	in url2: result1 = 'vcstream'
	#elif 'vev.io'	 	in url2: result1 = 'vev'
	elif 'vidbob'		in url2: result1 = 'vidbob'
	#elif 'playr.4helal'	in url2: result1 = 'helal'
	#elif 'vidbom'		in url2: result1 = 'vidbom'
	elif 'vidhd' 		in url2: result1 = 'vidhd'
	elif 'vidoza' 		in url2: result1 = 'vidoza'
	#elif 'vidshare' 	in url2: result1 = 'vidshare'
	elif 'watchvideo' 	in url2: result1 = 'watchvideo'
	elif 'wintv.live'	in url2: result1 = 'wintv.live'
	elif 'youtu'	 	in url2: result1 = 'youtube'
	elif 'zippyshare'	in url2: result1 = 'zippyshare'
	else:
		import urlresolver
		resolvable = urlresolver.HostedMediaFile(url).valid_url()
		if resolvable:
			result2 = url.split('//')[1].split('/')[0]
	#xbmcgui.Dialog().ok(str(url),result1)
	if result1 in ['akoam','helal','moshahda']: result = ' سيرفر خاص ' + result1
	elif result1=='movizland': result = ' سيرفرات خاصة ' + result1
	elif result1!='': result = ' سيرفر عام معروف ' + result1
	elif result2!='': result = 'سيرفر عام خارجي ' + result2
	elif result3!='':
		parts = result3.split('__')
		name = parts[0]
		if len(parts)==1:
			result = 'سيرفر عام ' + name
		else:
			type = parts[1]
			if type=='download': result = 'سيرفر تحميل عام ' + name
			elif type=='watch': result = 'سيرفر  مشاهدة عام ' + name
			else: result = 'سيرفر  مشاهدة وتحميل عام  ' + name
	else: result = ''
	return result

def RESOLVE_cached(url):
	server = url.split('/')[2]
	if 'youtu' in server or 'upto' in server:
		titleLIST,linkLIST = RESOLVE(url)
	else:
		#t1 = time.time()
		cacheperiod = SHORT_CACHE
		conn = sqlite3.connect(dbfile)
		c = conn.cursor()
		conn.text_factory = str
		c.execute('SELECT titleLIST,linkLIST FROM resolvecache WHERE url="'+url+'"')
		rows = c.fetchall()
		if rows:
			#message = 'found in cache'
			titleLIST,linkLIST = eval(rows[0][0]),eval(rows[0][1])
		else:
			#message = 'not found in cache'
			titleLIST,linkLIST = RESOLVE(url)
			t = (now,now+cacheperiod,url,str(titleLIST),str(linkLIST))
			c.execute("INSERT INTO resolvecache VALUES (?,?,?,?,?)",t)
			conn.commit()
		conn.close()
		#t2 = time.time()
		#xbmcgui.Dialog().notification(message,str(int(t2-t1))+' ms')
	return titleLIST,linkLIST

def RESOLVE(url):
	#url = 'https://govid.co/video/play/AAVENd'
	xbmc.log('['+addon_id+']:   Started resolving:   [ '+url+' ]', level=xbmc.LOGNOTICE)
	url2 = url.lower()
	titleLIST,linkLIST = [],[]
	if any(value in url2 for value in doNOTresolveMElist): titleLIST,linkLIST = [],[]
	elif 'shahid4u.net'	in url2 and 'name=' in url2: titleLIST,linkLIST = SHAHID4U(url)
	elif 'e5tsar'		in url2 and 'name=' in url2: titleLIST,linkLIST = E5TSAR(url)
	elif '://moshahda.'	in url2: titleLIST,linkLIST = MOVIZLAND(url)
	elif 'go.akoam.net'	in url2: titleLIST,linkLIST = AKOAM(url)
	elif 'arabloads'	in url2: titleLIST,linkLIST = ARABLOADS(url)
	elif 'archive'		in url2: titleLIST,linkLIST = ARCHIVE(url)
	elif 'catch.is'	 	in url2: titleLIST,linkLIST = CATCHIS(url)
	#elif 'estream'	 	in url2: titleLIST,linkLIST = ESTREAM(url)
	elif 'filerio'		in url2: titleLIST,linkLIST = FILERIO(url)
	elif 'gounlimited'	in url2: titleLIST,linkLIST = GOUNLIMITED(url)
	elif 'govid'		in url2: titleLIST,linkLIST = GOVID(url)
	#elif 'intoupload' 	in url2: titleLIST,linkLIST = INTOUPLOAD(url)
	elif 'liivideo' 	in url2: titleLIST,linkLIST = LIIVIDEO(url)
	elif 'mp4upload'	in url2: titleLIST,linkLIST = MP4UPLOAD(url)
	elif 'publicvideohost' in url2: titleLIST,linkLIST = PUBLICVIDEOHOST(url)
	elif 'rapidvideo' 	in url2: titleLIST,linkLIST = RAPIDVIDEO(url)
	elif 'thevideo'		in url2: titleLIST,linkLIST = THEVIDEO(url)
	elif 'top4top'		in url2: titleLIST,linkLIST = TOP4TOP(url)
	elif 'upbom' 		in url2: titleLIST,linkLIST = UPBOM(url)
	elif 'uppom' 		in url2: titleLIST,linkLIST = UPBOM(url)
	elif 'uptobox' 		in url2: titleLIST,linkLIST = UPTO(url)
	elif 'uptostream'	in url2: titleLIST,linkLIST = UPTO(url)
	elif 'uqload' 		in url2: titleLIST,linkLIST = UQLOAD(url)
	elif 'vcstream' 	in url2: titleLIST,linkLIST = VCSTREAM(url)
	#elif 'vev.io'	 	in url2: titleLIST,linkLIST = VEVIO(url)
	#elif 'playr.4helal'	in url2: titleLIST,linkLIST = HELAL(url)
	elif 'vidbob'		in url2: titleLIST,linkLIST = VIDBOB(url)
	#elif 'vidbom'		in url2: titleLIST,linkLIST = VIDBOM(url)
	elif 'vidhd' 		in url2: titleLIST,linkLIST = VIDHD(url)
	elif 'vidoza' 		in url2: titleLIST,linkLIST = VIDOZA(url)
	#elif 'vidshare' 	in url2: titleLIST,linkLIST = VIDSHARE(url)
	elif 'watchvideo' 	in url2: titleLIST,linkLIST = WATCHVIDEO(url)
	elif 'wintv.live'	in url2: titleLIST,linkLIST = WINTVLIVE(url)
	elif 'youtu' in url2 or 'y2u.be' in url2: titleLIST,linkLIST = YOUTUBE(url)
	elif 'zippyshare'	in url2: titleLIST,linkLIST = ZIPPYSHARE(url)
	else:
		import urlresolver
		resolvable = urlresolver.HostedMediaFile(url).valid_url()
		#xbmcgui.Dialog().ok(url,str(resolvable))
		if resolvable:
			titleLIST,linkLIST = URLRESOLVER(url)
	if len(linkLIST)==0: xbmc.log('['+addon_id+']:   Resolving Failed', level=xbmc.LOGNOTICE)
	else: xbmc.log('['+addon_id+']:   Resolving succeded:   [ '+str(linkLIST)+' ]', level=xbmc.LOGNOTICE)
	return titleLIST,linkLIST

def SERVERS_cached(linkLIST,script_name=''):
	#t1 = time.time()
	cacheperiod = LONG_CACHE
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	c.execute('SELECT serversLIST,urlLIST FROM serverscache WHERE linkLIST="'+str(linkLIST)+'"')
	rows = c.fetchall()
	if rows:
		#message = 'found in cache'
		serversLIST,urlLIST = eval(rows[0][0]),eval(rows[0][1])
	else:
		#message = 'not found in cache'
		serversLIST,urlLIST = SERVERS(linkLIST)
		t = (now,now+cacheperiod,str(linkLIST),str(serversLIST),str(urlLIST))
		c.execute("INSERT INTO serverscache VALUES (?,?,?,?,?)",t)
		conn.commit()
	conn.close()
	#t2 = time.time()
	#xbmcgui.Dialog().notification(message,str(int(t2-t1))+' ms')
	return serversLIST,urlLIST

def SERVERS(linkLIST,script_name=''):
	serversLIST,urlLIST,unknownLIST,serversDICT = [],[],[],[]
	message = '\\n'
	linkLIST = list(set(linkLIST))
	#selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', NEWlinkLIST)
	#if selection == -1 : return ''
	for link in linkLIST:
		if link=='': continue
		link = link.rstrip('/')
		#xbmc.log('['+addon_id+']:  '+link, level=xbmc.LOGNOTICE)
		serverNAME = RESOLVABLE(link)
		if serverNAME=='':
			if 'name=' in link:
				serverNAME = 'سيرفر عام ' + link.split('name=')[1].lower().split('__')[0]
				serversDICT.append( [serverNAME,link] )
			else:
				serverNAME = 'سيرفر عام مجهول ' + link.split('//')[1].split('/')[0].lower()
				serversDICT.append( [serverNAME,link] )
		else:
			serversDICT.append( [serverNAME,link] )		
	sortedDICT = sorted(serversDICT, reverse=False, key=lambda key: key[0])
	for i in range(0,len(sortedDICT)):
		serversLIST.append(sortedDICT[i][0])
		urlLIST.append(sortedDICT[i][1])
	#lines = len(unknownLIST)
	#if lines>0:
	#	for link in unknownLIST:
	#		message += link + '\\n'
	#	subject = 'Unknown Resolvers = ' + str(lines)
	#	result = SEND_EMAIL(subject,message,'no','','FROM-RESOLVERS-'+script_name)
	return serversLIST,urlLIST

def	URLRESOLVER(url):
	try:
		import urlresolver
		link = urlresolver.HostedMediaFile(url).resolve()
		return [link],[link]
	except: return [],[]

def MOVIZLAND(link):
	# http://moshahda.online/hj4ihfwvu3rl.html?name=Main
	# http://moshahda.online/dl?op=download_orig&id=hj4ihfwvu3rl&mode=o&hash=62516-107-159-1560654817-4fa63debbd8f3714289ad753ebf598ae
	headers = { 'User-Agent' : '' }
	if 'op=download_orig' in link:
		html = openURL_cached(SHORT_CACHE,link,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-1st')
		#xbmc.log(html, level=xbmc.LOGNOTICE)
		#xbmcgui.Dialog().ok(link,html)
		items = re.findall('direct link.*?href="(.*?)"',html,re.DOTALL)
		if items:
			url = items[0]
			return [url],[url]
		else:
			message = re.findall('class="err">(.*?)<',html,re.DOTALL)
			if message: xbmcgui.Dialog().ok('رسالة من الموقع الاصلي',message[0])
			return [],[]
	else:
		parts = link.split('?')
		url = parts[0]
		name2 = parts[1].replace('name=','').lower()
		# watch links
		html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-2nd')
		html_blocks = re.findall('Form method="POST" action=\'(.*?)\'(.*?)div',html,re.DOTALL)
		if not html_blocks: return [],[]
		link2 = html_blocks[0][0]
		block = html_blocks[0][1]
		if '.rar' in block or '.zip' in block: return [],[]
		items = re.findall('name="(.*?)".*?value="(.*?)"',block,re.DOTALL)
		payload = {}
		for name,value in items:
			payload[name] = value
		data = urllib.urlencode(payload)
		html = openURL_cached(SHORT_CACHE,link2,data,'','','RESOLVERS-MOSHAHDA_ONLINE-3rd')
		html_blocks = re.findall('Download Video.*?get\(\'(.*?)\'.*?sources:(.*?)image:',html,re.DOTALL)
		if not html_blocks: return [],[]
		download = html_blocks[0][0]
		block = html_blocks[0][1]
		items = re.findall('file:"(.*?)"(,label:".*?"|)',block,re.DOTALL)
		titleLIST,linkLIST = [],[]
		resolutionLIST = []
		for link,title in items:
			if '.m3u8' in link:
				html = openURL_cached(SHORT_CACHE,link,'','','','RESOLVERS-MOSHAHDA_ONLINE-4th')
				items2 = re.findall('RESOLUTION=(.*?),.*?\n(.*?)\n',html,re.DOTALL)
				if items2:
					for resolution,link in items2:
						resolutionLIST.append(resolution)
						title = ' سيرفر خاص '+'m3u8 '+name2+' '+resolution.split('x')[1]
						titleLIST.append(title)
						linkLIST.append(link)
				else:
					title = ' سيرفر خاص '+'m3u8 '+name2
					titleLIST.append(title)
					linkLIST.append(link)
			else:
				title = title.replace(',label:"','')
				title = title.strip('"')
				#xbmcgui.Dialog().ok(title,str(resolutionLIST))
				title = ' سيرفر  خاص '+' mp4 '+name2+' '+title
				titleLIST.append(title)
				linkLIST.append(link)
		# download links
		link = 'http://moshahda.online' + download
		html = openURL_cached(SHORT_CACHE,link,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-5th')
		items = re.findall("download_video\('(.*?)','(.*?)','(.*?)'.*?<td>(.*?),",html,re.DOTALL)
		for id,mode,hash,resolution in items:
			title = ' سيرفر تحميل خاص '+' mp4 '+name2+' '+resolution.split('x')[1]
			link = 'http://moshahda.online/dl?op=download_orig&id='+id+'&mode='+mode+'&hash='+hash
			resolutionLIST.append(resolution)
			titleLIST.append(title)
			linkLIST.append(link)
		resolutionLIST = set(resolutionLIST)
		titleLISTnew,sortingDICT = [],[]
		for title in titleLIST:
			#xbmcgui.Dialog().ok(title,'')
			res = re.findall(" (\d*x|\d*)&&",title+'&&',re.DOTALL)
			for resolution in resolutionLIST:
				if res[0] in resolution:
					title = title.replace(res[0],resolution.split('x')[1])
			titleLISTnew.append(title)
		#xbmc.log(items[0][0], level=xbmc.LOGNOTICE)
		for i in range(len(linkLIST)):
			items = re.findall("&&(.*?)(\d*)&&",'&&'+titleLISTnew[i]+'&&',re.DOTALL)
			sortingDICT.append( [titleLISTnew[i],linkLIST[i],items[0][0],items[0][1]] )
		sortingDICT = sorted(sortingDICT, key=lambda x: x[3], reverse=True)
		sortingDICT = sorted(sortingDICT, key=lambda x: x[2], reverse=False)
		titleLIST,linkLIST = [],[]
		for i in range(len(sortingDICT)):
			titleLIST.append(sortingDICT[i][0])
			linkLIST.append(sortingDICT[i][1])
		return titleLIST,linkLIST

def E5TSAR(url):
	# http://e5tsar.com/717254
	parts = url.split('?')
	url2 = parts[0]
	headers = { 'User-Agent' : '' }
	html = openURL_cached(REGULAR_CACHE,url2,'',headers,'','RESOLVERS-E5TSAR-1st')
	items = re.findall('Please wait.*?href=\'(.*?)\'',html,re.DOTALL)
	url = items[0]
	titleLIST,linkLIST = RESOLVE_cached(url)
	#xbmcgui.Dialog().ok(items[0],html)
	return titleLIST,linkLIST

def SHAHID4U(link):
	# https://tv.shahid4u.net/?postid=126981&serverid=5&name=Streamango
	parts = re.findall('postid=(.*?)&serverid=(.*?)&name=',link,re.DOTALL|re.IGNORECASE)
	#xbmcgui.Dialog().ok(link,str(parts))
	postid = parts[0][0]
	serverid = parts[0][1]
	url = 'https://on.shahid4u.net/ajaxCenter?_action=getserver&_post_id='+postid+'&serverid='+serverid
	headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','RESOLVERS-SHAHID4U-1st')
	url2 = html
	#xbmcgui.Dialog().ok(url2,'')
	titleLIST,linkLIST = RESOLVE_cached(url2)
	#try: url3 = url2[0]
	#except: url3 = ''
	#xbmcgui.Dialog().ok(str(url3),str(html))
	return titleLIST,linkLIST

def AKOAM(link):
	# http://go.akoam.net/5cf68c23e6e79
	import requests
	response = requests.request('GET', link, data='', headers='')
	html = response.text
	cookies = response.cookies.get_dict()
	cookie = cookies['golink']
	cookie = unquote(escapeUNICODE(cookie))
	items = re.findall('route":"(.*?)"',cookie,re.DOTALL)
	url = items[0].replace('\/','/')
	url = escapeUNICODE(url)
	if 'catch.is' in url:
		id = url.split('%2F')[-1]
		url = 'http://catch.is/'+id
		titleLIST,linkLIST = CATCHIS(url)
	else:
		response = requests.request('GET', 'https://akoam.net/', headers='', data='', allow_redirects=False)
		relocateURL = response.headers['Location']
		url = url.replace('https://akoam.net/',relocateURL)
		headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' , 'Referer':url }
		response = requests.request('POST', url, headers=headers, data='', allow_redirects=False)
		html = response.text
		items = re.findall('direct_link":"(.*?)"',html,re.DOTALL|re.IGNORECASE)
		if not items:
			items = re.findall('<iframe.*?src="(.*?)"',html,re.DOTALL|re.IGNORECASE)
			if not items:
				items = re.findall('<embed.*?src="(.*?)"',html,re.DOTALL|re.IGNORECASE)
		url2 = items[0].replace('\/','/')
		url2 = url2.rstrip('/')
		if 'http' not in url2: url2 = 'http:' + url2
		if 'name=' in link: titleLIST,linkLIST = RESOLVE_cached(url2)
		else: titleLIST,linkLIST = ['ملف التحميل'],[url2]
		"""
		splits = url.split('/')
		server = '/'.join(splits[0:3])
		hash_data = url.split('/')[4]
		watch_title = url.split('/')[-1]
		url3 = server + '/watching/'+hash_data+'/'+watch_title
		response = requests.request('GET', url3, headers='', data='', allow_redirects=False)
		html = response.text
		url3 = re.findall('file: "(.*?)"',html,re.DOTALL|re.IGNORECASE)[0]
		titles2,urls2 = ['ملف المشاهدة المباشرة'],[url3]
		titleLIST,linkLIST = titleLIST+titles2,linkLIST+urls2
		"""
	return titleLIST,linkLIST

def RAPIDVIDEO(url):
	# https://www.rapidvideo.com/e/FZSQ3R0XHZ
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-RAPIDVIDEO-1st')
	#xbmcgui.Dialog().ok(url,html)
	items = re.findall('<source src="(.*?)".*?label="(.*?)"',html,re.DOTALL)
	titles,urls = [],[]
	for link,label in items:
		titles.append(label)
		urls.append(link)
	return titles,urls

def UQLOAD(url):
	# https://uqload.com/embed-iaj1zudyf89v.html
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-UQLOAD-1st')
	items = re.findall('sources: \["(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,items[0])
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VCSTREAM(url):
	# https://vcstream.to/embed/5c83f14297d62
	url = url.strip('/')
	id = url.split('/')[-1]
	url = 'https://vcstream.to/player?fid=' + id
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VCSTREAM-1st')
	html = html.replace('\\','')
	#xbmcgui.Dialog().ok(url,html)
	items = re.findall('file":"(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0],items[0])
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VIDOZA(url):
	# https://vidoza.net/embed-pkqq5ljvckb7.html
	url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-VIDOZA-1st')
	items = re.findall('src: "(.*?)".*?label:"(.*?)", res:"(.*?)"',html,re.DOTALL)
	titles,urls = [],[]
	for link,label,res in items:
		titles.append(label+' '+res)
		urls.append(link)
	return titles,urls

def WATCHVIDEO(url):
	# https://watchvideo.us/embed-rpvwb9ns8i73.html
	url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-WATCHVIDEO-1st')
	items = re.findall("download_video\('(.*?)','(.*?)','(.*?)'\)\">(.*?)</a>.*?<td>(.*?),.*?</td>",html,re.DOTALL)
	items = set(items)
	titles,urls = [],[]
	for id,mode,hash,label,res in items:
		url = 'https://watchvideo.us/dl?op=download_orig&id='+id+'&mode='+mode+'&hash='+hash
		html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-WATCHVIDEO-2nd')
		items = re.findall('direct link.*?href="(.*?)"',html,re.DOTALL)
		for link in items:
			titles.append(label+' '+res)
			urls.append(link)
	return titles,urls

def UPBOM(url):
	# http://upbom.live/hm9opje7okqm/TGQSDA001.The.Vanishing.2018.1080p.WEB-DL.Cima4U.mp4.html
	url = url.replace('upbom.live','uppom.live')
	url = url.strip('/')
	id = url.split('/')[-2]
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'id' : id  , 'op' : 'download2' , 'method_free':'Free+Download+%3E%3E' }
	data = urllib.urlencode(payload)
	html = openURL_cached(SHORT_CACHE,url,data,headers,'','RESOLVERS-UPBOM-1st')
	#xbmcgui.Dialog().ok(url,html)
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	items = re.findall('direct_link.*?href="(.*?)"',html,re.DOTALL)
	if items:
		url2 = items[0]
		return [url2],[url2]
	else: return [],[]

def LIIVIDEO(url):
	# https://www.liivideo.com/012ocyw9li6g.html
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-LIIVIDEO-1st')
	items = re.findall('sources:.*?"(.*?)","(.*?)"',html,re.DOTALL)
	titles,urls = [],[]
	if items:
		titles.append('mp4')
		urls.append(items[0][1])
		titles.append('m3u8')
		urls.append(items[0][0])
	return titles,urls

def UPTO(url):
	#xbmcgui.Dialog().ok(url,'')
	titleLIST = ['uptostream','uptobox (delay 30sec)','both']
	selection = xbmcgui.Dialog().select('اختر السيرفر:', titleLIST)
	if selection == -1:
		titleLIST,linkLIST = [],[]
	else:
		if selection==0:
			url2 = url.replace('://uptobox.','://uptostream.')
			titleLIST,linkLIST = UPTOSTREAM(url2)
		elif selection==1:
			url2 = url.replace('://uptostream','://uptobox.')
			titleLIST,linkLIST = UPTOBOX(url2)
		else:
			url2 = url.replace('://uptobox.','://uptostream.')
			titleLIST2,linkLIST2 = UPTOSTREAM(url2)
			url2 = url.replace('://uptostream.','://uptobox.')
			titleLIST3,linkLIST3 = UPTOBOX(url2)
			titleLIST = titleLIST2 + titleLIST3
			linkLIST = linkLIST2 + linkLIST3
	return titleLIST,linkLIST

def UPTOSTREAM(url):
	#xbmcgui.Dialog().ok(url,'')
	headers = { 'User-Agent' : '' }
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','RESOLVERS-UPTOSTREAM-1st')
	items = re.findall('src":"(.*?)".*?label":"(.*?)"',html,re.DOTALL)
	titleLIST,linkLIST = [],[]
	if items:
		for link,title in items:
			link = link.replace('\/','/')
			titleLIST.append(title)
			linkLIST.append(link)
	return titleLIST,linkLIST

def UPTOBOX(url):
	#xbmcgui.Dialog().ok(url,'')
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-UPTOBOX-1st')
	titleLIST,linkLIST = [],[]
	if 'waitingToken' in html:
		token = re.findall('waitingToken\' value=\'(.*?)\'',html,re.DOTALL)
		token = token[0]
		headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'waitingToken' : token }
		data = urllib.urlencode(payload)
		progress = xbmcgui.DialogProgress()
		progress.create('Waiting 35 seconds ...')
		for i in range(0,35):
			progress.update(i*100/35,str(35-i)+' seconds left')
			xbmc.sleep(1000)
			if progress.iscanceled(): break
		progress.close()
		html = openURL_cached(SHORT_CACHE,url,data,headers,'','RESOLVERS-UPTOBOX-2nd')
	items = re.findall('class=\'file-title\'>(.*?)<.*?comparison-table.*?href="(.*?)"',html,re.DOTALL)
	if items:
		title,url = items[0]
		titleLIST,linkLIST = [title],[url]
	return titleLIST,linkLIST
	#xbmcgui.Dialog().ok(str(html),html)
	#file = open('S:\emad3.html', 'w')
	#file.write(token)
	#file.write('\n\n\n')
	#file.write(html)
	#file.close()

def YOUTUBE(url):
	#subtitles example		url = 'https://www.youtube.com/watch?v=eDlZ5vANQUg'
	#mpddash example		url = 'https://www.youtube.com/watch?v=XvmSNAyeyFI'
	#signature example		url = 'https://www.youtube.com/watch?v=e_S9VvJM1PI'
	#signature example	deleted		url = 'https://www.youtube.com/watch?v=-ckLRhgN9r0'
	#url = 'https://youtu.be/eDlZ5vANQUg'
	#url = 'http://y2u.be/eDlZ5vANQUg'
	#url = 'https://www.youtube.com/embed/eDlZ5vANQUg'
	#youtube unofficial details   https://tyrrrz.me/Blog/Reverse-engineering-YouTube
	"""
	youtubeID = url.split('/watch?v=')[-1]
	#xbmcgui.Dialog().ok(url,youtubeID)
	#id = url.split('/')[-1]
	#youtubeID = id.split('?')[0]
	url = 'plugin://plugin.video.youtube/play/?video_id='+youtubeID
	return [url],[url]
	"""
	id = url.split('/')[-1]
	id = id.replace('watch?v=','')
	if 'embed' in url: url = 'https://www.youtube.com/watch?v='+id
	#html = openURL_cached(NO_CACHE,'http://localhost:64000/shutdown','','','','RESOLVERS-YOUTUBE-1st')
	block2,block3,format_block,jshtml = '','','',''
	subtitleURL,dashURL,finalURL = '','',''
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-YOUTUBE-2nd')
	#xbmc.log('===========================================',level=xbmc.LOGNOTICE)
	#xbmc.log(html,level=xbmc.LOGNOTICE)
	html = html.replace('\\','')
	html_blocks = re.findall('playerCaptionsTracklistRenderer(.*?)defaultAudioTrackIndex',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0].replace('u0026','&')
		items = re.findall('{"languageCode":"(.*?)".*?simpleText":"(.*?)"',block,re.DOTALL)
		titleLIST,linkLIST = ['بدون اضافة الترجمة الاضافية'],['']
		for lang,title in items:
			titleLIST.append(title)
			linkLIST.append(lang)
		selection = xbmcgui.Dialog().select('اختر الترجمة المناسبة:', titleLIST)
		if selection not in [0,-1]:
			subtitleURL = re.findall('baseUrl":"(.*?)"',block,re.DOTALL)
			subtitleURL = subtitleURL[0]+'&fmt=vtt&type=track&tlang='+linkLIST[selection]
	titleLIST,linkLIST = [],[]
	html_blocks = re.findall('dashManifestUrl":"(.*?)"',html,re.DOTALL)
	if html_blocks:
		if '/signature/' in html_blocks[0]: dashURL = html_blocks[0]
		else: dashURL = html_blocks[0].replace('/s/','/signature/')
	html_blocks = re.findall('url_encoded_fmt_stream_map":"(.*?)"',html,re.DOTALL)
	if html_blocks: block2 = html_blocks[0]
	html_blocks = re.findall('adaptive_fmts":"(.*?)"',html,re.DOTALL)
	if html_blocks: block3 = html_blocks[0]
	html_blocks = re.findall('fmt_list":"(.*?)"',html,re.DOTALL)
	if html_blocks: format_block = html_blocks[0]
	#xbmc.log('fmt_list='+format_block,level=xbmc.LOGNOTICE)
	#xbmc.log(block2,level=xbmc.LOGNOTICE)
	#xbmc.log(block3,level=xbmc.LOGNOTICE)
	if 'sp=sig' in block2 or 'sp=sig' in block3:
		html_blocks = re.findall('src="(/yts/jsbin/player_.*?)"',html,re.DOTALL)
		if html_blocks:
			jsfile = 'https://www.youtube.com'+html_blocks[0]
			jshtml = openURL_cached(REGULAR_CACHE,jsfile,'','','','RESOLVERS-YOUTUBE-3rd')
			import youtube_signature.cipher
			import youtube_signature.json_script_engine
			cypher = youtube_signature.cipher.Cipher()
			cypher._object_cache = {}
			json_script = cypher._load_javascript(jshtml)
			json_script_cached = str(json_script)
	#xbmc.log(jsfile,level=xbmc.LOGNOTICE)
	streams,streams2 = [],[]
	for block in [block2,block3]:
		if block=='': continue
		lines = block.split(',')
		for line in lines:
			#xbmc.log('===========================================',level=xbmc.LOGNOTICE)
			#xbmc.log(line,level=xbmc.LOGNOTICE)
			"""
			line = line.replace('"','_').replace('=','":"').replace('u0026','","')
			dict = eval('{"'+line+'"}')
			for key,value in dict.items():
				dict[key] = unquote(value.replace('_','"'))
				#xbmc.log(key+'='+dict[key],level=xbmc.LOGNOTICE)
			"""
			line = unquote(line)
			dict = {}
			items = line.split('u0026')
			for item in items:
				key,value = item.split('=',1)
				dict[key] = value
				#xbmc.log(key+'='+value,level=xbmc.LOGNOTICE)
			#xbmc.log('url='+dict['url'],level=xbmc.LOGNOTICE)
			if 'signature=' in dict['url'] or dict['url'].count('sig=')>1:
				streams.append(dict)
				#pass
			elif jshtml!='' and 's' in dict and 'sp' in dict:
				json_script = eval(json_script_cached)
				json_script_engine = youtube_signature.json_script_engine.JsonScriptEngine(json_script)
				signature = json_script_engine.execute(dict['s'])
				if signature!=dict['s']:
					dict['url'] = dict['url'] + '&'+dict['sp']+'=' + signature
					streams.append(dict)
				#xbmc.log('json_script='+str(json_script2),level=xbmc.LOGNOTICE)
			#xbmc.log('['+addon_id+']:  dict:['+str(dict)+']', level=xbmc.LOGNOTICE)
			#xbmc.log('url='+dict['url'], level=xbmc.LOGNOTICE)
	#xbmc.log('['+addon_id+']:  streams:['+str(streams)+']', level=xbmc.LOGNOTICE)
	for dict in streams:
		filetype,codec,quality2,type2,codecs,bitrate = 'unknown','unknown','unknown','Unknown','',0
		try:
			type = dict['type']
			#xbmc.log('['+addon_id+']:  Type:['+type+']', level=xbmc.LOGNOTICE)
			type = type.replace('+','')
			items = re.findall('/(.*?);.*?"(.*?)"',type,re.DOTALL)
			filetype,codecs = items[0]
			codecs2 = codecs.split(',')
			codec = ''
			for item in codecs2: codec += item.split('.')[0]+','
			codec = codec.strip(',')
			if ',' in type:
				type2 = 'A+V'
				bitrate = 0
				quality2 = dict['quality']
				format = re.findall(','+dict['itag']+'/(.*?),',','+format_block+',',re.DOTALL)
				if format:
					dict['size'] = format[0]
					quality2 = dict['size'].split('x')[1]
			elif 'video' in type:
				type2 = 'Video'
				bitrate = int(dict['bitrate'])
				#quality2 = str(bitrate/1000)+'kbps  '+dict['quality_label']+'  '+dict['size']+'  '+dict['fps']+'fps'
				quality2 = dict['size'].split('x')[1]+'  '+str(bitrate/1000)+'kbps  '+dict['fps']+'fps'
			elif 'audio' in type:
				type2 = 'Audio'
				bitrate = int(dict['bitrate'])
				quality2 = str(bitrate/1000)+'kbps  '+str(int(dict['audio_sample_rate'])/1000)+'khz  '+dict['audio_channels']+'ch'
		except: pass
		title = type2+':  '+filetype+'  '+quality2+'  ('+codec+','+dict['itag']+')'
		dict['title'] = title
		dict['type2'] = type2
		dict['filetype'] = filetype
		dict['codecs'] = codecs
		dict['bitrate'] = bitrate
		dict['duration'] = round(0.5+float(dict['url'].split('dur=',1)[1].split('&',1)[0]))
		streams2.append(dict)
	#xbmc.log('['+addon_id+']:  streams2:['+str(streams2)+']', level=xbmc.LOGNOTICE)
	videoTitleLIST,audioTitleLIST,muxedTitleLIST,mpdaudioTitleLIST,mpdvideoTitleLIST,allTitleLIST = [],[],[],[],[],[]
	videoDictLIST,audioDictLIST,muxedDictLIST,mpdaudioDictLIST,mpdvideoDictLIST,allvideoDictLIST,allaudioDictLIST = [],[],[],[],[],[],[]
	streams2 = sorted(streams2, reverse=False, key=lambda key: key['filetype'])
	for dict in streams2:
		if dict['type2']=='Video':
			videoTitleLIST.append(dict['title'])
			videoDictLIST.append(dict)
		elif dict['type2']=='Audio':
			audioTitleLIST.append(dict['title'])
			audioDictLIST.append(dict)
		else:
			muxedTitleLIST.append(dict['title'].replace('A+V:  ',''))
			muxedDictLIST.append(dict)
		if dict['type2']=='Video' and dict['init']!='0-0' and 'avc' in dict['codecs']:
			mpdvideoTitleLIST.append(dict['title'])
			mpdvideoDictLIST.append(dict)
		elif dict['type2']=='Audio' and dict['init']!='0-0' and 'mp4a' in dict['codecs']:
			mpdaudioTitleLIST.append(dict['title'])
			mpdaudioDictLIST.append(dict)
	for dict in muxedDictLIST:
		dict['title'] = dict['title'].replace('A+V:  ','')
		allTitleLIST.append(dict['title'])
		allvideoDictLIST.append(dict)
		allaudioDictLIST.append({})
	#highest,highestAudioDICT = 0,{}
	#for dict in mpdaudioDictLIST:
	#	if dict['bitrate']>highest: highest,highestAudioDICT = dict['bitrate'],dict
	#audiodict = highestAudioDICT
	for audiodict in mpdaudioDictLIST:
		audioBitrate = int(audiodict['bitrate']/1000)
		for videodict in mpdvideoDictLIST:
			videoBitrate = int(videodict['bitrate']/1000)
			title = videodict['title'].replace('Video:  '+videodict['filetype'],'mpd')+'('+audiodict['title'].split('(',1)[1]
			title = title.replace(str(videoBitrate)+'kbps',str(videoBitrate+audioBitrate)+'kbps')
			allTitleLIST.append(title)
			allvideoDictLIST.append(videodict)
			allaudioDictLIST.append(audiodict)
	if dashURL!='': allTitleLIST = allTitleLIST + ['mpd  دقة اوتوماتيكية']
	selectMenu,choiceMenu = [],[]
	if allTitleLIST: selectMenu.append('صورة وصوت جميع المتوفر') ; choiceMenu.append('all')
	if muxedTitleLIST: selectMenu.append('صورة وصوت محدودة الدقة') ; choiceMenu.append('muxed')
	if mpdvideoTitleLIST: selectMenu.append('mpd انت تختار دقة الصورة ودقة الصوت') ; choiceMenu.append('mpd')
	if videoTitleLIST: selectMenu.append('صورة فقط بدون صوت') ; choiceMenu.append('video')
	if audioTitleLIST: selectMenu.append('صوت فقط بدون صورة') ; choiceMenu.append('audio')
	need_mpd_server = False
	while True:
		selection = xbmcgui.Dialog().select('اختر النوع المناسب:', selectMenu)
		if selection==-1: break
		choice = choiceMenu[selection]
		if choice in ['audio','video','muxed']:
			if choice=='muxed': titleLIST,dictLIST = muxedTitleLIST,muxedDictLIST
			elif choice=='video': titleLIST,dictLIST = videoTitleLIST,videoDictLIST
			elif choice=='audio': titleLIST,dictLIST = audioTitleLIST,audioDictLIST
			selection = xbmcgui.Dialog().select('اختر الملف المناسب:', titleLIST)
			if selection!=-1:
				finalURL = dictLIST[selection]['url']
				break
		elif choice=='mpd':
			selection = xbmcgui.Dialog().select('اختر دقة الصورة المناسبة:', mpdvideoTitleLIST)
			if selection!=-1:
				videoDICT = videoDictLIST[selection]
				selection = xbmcgui.Dialog().select('اختر دقة الصوت المناسبة:', mpdaudioTitleLIST)
				if selection!=-1:
					audioDICT = audioDictLIST[selection]
					need_mpd_server = True
					break
		else:
			selection = xbmcgui.Dialog().select('اختر الملف المناسب:', allTitleLIST)
			if selection!=-1:
				if dashURL!='' and selection==len(allTitleLIST)-1:
					finalURL = dashURL
				else:
					videoDICT = allvideoDictLIST[selection]
					if 'mpd' in allTitleLIST[selection]:
						audioDICT = allaudioDictLIST[selection]
						need_mpd_server = True
					else: finalURL = videoDICT['url']
				break
	httpd = 'YOUTUBE'
	if need_mpd_server:
		#xbmc.log(videoDICT['url'],level=xbmc.LOGNOTICE)
		#xbmc.log(audioDICT['url'],level=xbmc.LOGNOTICE)
		videoDuration = int(videoDICT['duration'])
		audioDuration = int(audioDICT['duration'])
		duration = str(videoDuration) if videoDuration>audioDuration else str(audioDuration)
		mpd = '<?xml version="1.0" encoding="UTF-8"?>\n'
		mpd += '<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:mpeg:dash:schema:mpd:2011" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="urn:mpeg:dash:schema:mpd:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd" minBufferTime="PT1.5S" mediaPresentationDuration="PT'+duration+'S" type="static" profiles="urn:mpeg:dash:profile:isoff-main:2011">\n'
		mpd += '<Period>\n'
		mpd += '<AdaptationSet id="0" mimeType="video/'+videoDICT['filetype']+'" subsegmentAlignment="true">\n'# subsegmentStartsWithSAP="1" bitstreamSwitching="true" default="true">\n'
		mpd += '<Role schemeIdUri="urn:mpeg:DASH:role:2011" value="main"/>\n'
		mpd += '<Representation id="'+videoDICT['itag']+'" codecs="'+videoDICT['codecs']+'" startWithSAP="1" bandwidth="'+str(videoDICT['bitrate'])+'" width="'+videoDICT['size'].split('x')[0]+'" height="'+videoDICT['size'].split('x')[1]+'" frameRate="'+videoDICT['fps']+'">\n'
		mpd += '<BaseURL>'+videoDICT['url'].replace('&','&amp;')+'</BaseURL>\n'
		mpd += '<SegmentBase indexRange="'+videoDICT['index']+'">\n'# indexRangeExact="true">\n'
		mpd += '<Initialization range="'+videoDICT['init']+'" />\n'
		mpd += '</SegmentBase>\n'
		mpd += '</Representation>\n'
		mpd += '</AdaptationSet>\n'
		mpd += '<AdaptationSet id="1" mimeType="audio/'+audioDICT['filetype']+'" subsegmentAlignment="true">\n'# subsegmentStartsWithSAP="1" bitstreamSwitching="true" default="true">\n'
		mpd += '<Role schemeIdUri="urn:mpeg:DASH:role:2011" value="main"/>\n'
		mpd += '<Representation id="'+audioDICT['itag']+'" codecs="'+audioDICT['codecs']+'" bandwidth="130475">\n'
		mpd += '<AudioChannelConfiguration schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011" value="'+audioDICT['audio_channels']+'"/>\n'
		mpd += '<BaseURL>'+audioDICT['url'].replace('&','&amp;')+'</BaseURL>\n'
		mpd += '<SegmentBase indexRange="'+audioDICT['index']+'">\n'# indexRangeExact="true">\n'
		mpd += '<Initialization range="'+audioDICT['init']+'" />\n'
		mpd += '</SegmentBase>\n'
		mpd += '</Representation>\n'
		mpd += '</AdaptationSet>\n'
		mpd += '</Period>\n'
		mpd += '</MPD>\n'
		#xbmc.log(mpd,level=xbmc.LOGNOTICE)
		"""
		mpdfolder = os.path.join(xbmc.translatePath('special://temp'),addon_id)
		if not os.path.exists(mpdfolder):
			#xbmcgui.Dialog().ok('folder does not exsit','')
			import xbmcvfs
			xbmcvfs.mkdir(mpdfolder)
		mpdfile = os.path.join(mpdfolder,id+'.mpd')
		#xbmcgui.Dialog().ok(mpdfile,mpd)
		#with open(mpdfile,'w') as file: file.write(mpd)
		#mpdfile = 'http://localhost:64000/'+id+'.mpd'
		"""
		import BaseHTTPServer#,httplib
		class HTTP_SERVER(BaseHTTPServer.HTTPServer):
			#mpd = 'mpd = used when not using __init__'
			def __init__(self,port='64000',mpd='mpd = from __init__'):
				BaseHTTPServer.HTTPServer.__init__(self,("",port), HTTP_HANDLER)
				self.port = port
				self.mpd = mpd
				#print('server is up now listening on port: '+str(port))
			def serve(self):
				#print('serving requests started')
				self.keeprunning = True
				#counter = 0
				while self.keeprunning:
					#counter += 1
					#print('running a single handle_request() now: '+str(counter)+'')
					#settimeout does not work due to error message if it kill an http request
					#self.socket.settimeout(1)
					self.handle_request()
				#print('serving requests stopped\n')
			def stop(self):
				self.keeprunning = False
				self.socket.close()
				#self.send_http()
			def shutdown(self):
				self.stop()
				self.server_close()
				#print('server is down now\n')
			def start(self):
				#thread.start_new_thread(self.serve, ())
				self.threads = CustomThread()
				self.threads.start_new_thread('1',self.serve)
			def load(self,mpd):
				self.mpd = mpd
			#def send_http(self):
			#	conn = httplib.HTTPConnection("localhost:%d" % self.port)
			#	conn.request("HEAD", "/")
			#	conn.getresponse()
		class HTTP_HANDLER(BaseHTTPServer.BaseHTTPRequestHandler):
			def do_GET(self):
				#print('doing GET  '+self.path)
				self.send_response(200)
				self.send_header('Content-type', 'text/plain')
				self.end_headers()
				#self.wfile.write(self.path+'\n')
				self.wfile.write(self.server.mpd)
				if self.path=='/shutdown': self.server.shutdown()
			def do_HEAD(s):
				#print('doing HEAD  '+self.path)
				s.send_response(200)
				s.end_headers()
		httpd = HTTP_SERVER(64000,mpd)
		#httpd.load(mpd)
		httpd.start()
		finalURL = 'http://localhost:64000/youtube.mpd'
	titleLIST,linkLIST = [],[]
	if finalURL!='':
		if subtitleURL!='': finalURL = [finalURL,subtitleURL]
		titleLIST,linkLIST = [httpd],[finalURL]
	return titleLIST,linkLIST

def VIDBOB(url):
	# https://vidbob.com/v6rnlgmrwgqu
	headers = { 'User-Agent' : '' }
	#url = url.replace('http:','https:')
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VIDBOB-1st')
	items = re.findall('file:"(.*?)"(,label:"(.*?)"|)\}',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0].rstrip('/'),'')
	linkLIST,titleLIST = [],[]
	for link,dummy,label in reversed(items):
		link = link.replace('https:','http:')
		if '.m3u8' in link:
			html = openURL_cached(SHORT_CACHE,link,'','','','RESOLVERS-VIDBOB-2nd')
			items2 = re.findall('RESOLUTION=(.*?),.*?\n(.*?)\n',html,re.DOTALL)
			if items2:
				for resolution,link2 in items2:
					title = 'سيرفر خاص'+'   m3u8   '+resolution.split('x')[1]
					titleLIST.append(title)
					linkLIST.append(link2)
			else:
				title = 'سيرفر خاص'+'   m3u8'
				titleLIST.append(title)
				linkLIST.append(link)
		else:
			title = 'سيرفر خاص'+'   '+label
			linkLIST.append(link)
			titleLIST.append(title)
	return titleLIST,linkLIST

def	FILERIO(url):
	# https://filerio.in/pbcqob1217la
	#xbmc.log(url, level=xbmc.LOGNOTICE)
	id = url.split('/')[-1]
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'id':id , 'op':'download2' }
	data = urllib.urlencode(payload)
	html = openURL_cached(SHORT_CACHE,url,data,headers,'','RESOLVERS-FILERIO-2nd')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	items = re.findall('direct_link.*?href="(.*?)"',html,re.DOTALL)
	if items: return [items[0]],[items[0]]
	else: return [],[]

def GOUNLIMITED(url):
	# https://gounlimited.to/embed-wqsi313vbpua.html
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	html_blocks = re.findall('function\(p,a,c,k,e,d\)(.*?)split',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall(",'(.*?)'",block,re.DOTALL)
		items = items[-1].split('|')
		link = items[12]+'://'+items[84]+'.'+items[11]+'.'+items[10]+'/'+items[83]+'/v.mp4'
		return [link],[link]
	else: return [],[]
	#link = 'https://shuwaikh.gounlimited.to/'+id+'/v.mp4'
	#link = 'https://fs67.gounlimited.to/'+id+'/v.mp4'

def VIDHD(url):
	# https://vidhd.net/562ghl3hr1cw.html
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-LIIVIDEO-1st')
	items = re.findall('file:"(.*?)",label:"(.*?)"',html,re.DOTALL)
	titleLIST,linkLIST = [],[]
	for link,label in items:
		titleLIST.append(label)
		linkLIST.append(link)
	html_blocks = re.findall('function\(p,a,c,k,e,d\)(.*?)split',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall(",'(.*?)'",block,re.DOTALL)
		items = items[-1].split('|')
		server = items[7]+'://'+items[19]+'.'+items[6]+'.'+items[4]
		html_blocks = re.findall('\|image(\|.*?\|)sources\|',block,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('\|(\w+)\|(\w+)',block,re.DOTALL)
			for label,id in items:
				link = server+'/'+id+'/v.mp4'
				titleLIST.append(label)
				linkLIST.append(link)
	return titleLIST,linkLIST
	#link = https://s2.vidhd.net/kmxsuzrepjumwmesrluuynfphmbrrpofmbwknihn4l6rdua3pwajpcxqvboq/v.mp4

def GOVID(url):
	# https://govid.co/video/play/AAVENd
	headers = { 'User-Agent' : '' }
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','RESOLVERS-GOVID-1st')
	items = re.findall('source src="(.*?)"',html,re.DOTALL)
	titleLIST,linkLIST = [],[]
	if items:
		link = items[0]
		if '.m3u8' in link:
			server = '/'.join(link.split('/')[0:3])
			html = openURL_cached(REGULAR_CACHE,link,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-4th')
			items2 = re.findall('RESOLUTION=(.*?),.*?\n(.*?)\n',html,re.DOTALL)
			if items2:
				for resolution,link in items2:
					link = server+link
					title = 'سيرفر خاص'+'   m3u8   '+resolution.split('x')[1]
					titleLIST.append(title)
					linkLIST.append(link)
			else:
				title = 'سيرفر خاص'+'   m3u8'
				titleLIST.append(title)
				linkLIST.append(link)
		else:
			title = 'سيرفر خاص'
			titleLIST.append(title)
			linkLIST.append(link)
	return titleLIST,linkLIST
	# https://s1m.govid.co/stream/229.m3u8









#####################################################
#    NOT YET VERIFIED
#    16-06-2019
#####################################################

def CATCHIS(url):
	id = url.split('/')[-1]
	payload = { 'op' : 'download2' , 'id' : id }
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	data = urllib.urlencode(payload)
	html = openURL_cached(SHORT_CACHE,url,data,headers,'','RESOLVERS-CATCH-1st')
	items = re.findall('direct_link.*?href="(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def ARABLOADS(url):
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-ARABLOADS-1st')
	items = re.findall('color="red">(.*?)<',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def TOP4TOP(url):
	return [url],[url]

def ZIPPYSHARE(url):
	#xbmcgui.Dialog().ok(url,'')
	server = url.split('/')
	basename = '/'.join(server[0:3])
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-ZIPPYSHARE-1st')
	items = re.findall('dlbutton\'\).href = "(.*?)" \+ \((.*?) \% (.*?) \+ (.*?) \% (.*?)\) \+ "(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,str(var))
	if items:
		var1,var2,var3,var4,var5,var6 = items[0]
		var = int(var2) % int(var3) + int(var4) % int(var5)
		url = basename + var1 + str(var) + var6
		return [url],[url]
	else: return [],[]

def THEVIDEO(url):
	url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-THEVIDEO-1st')
	items = re.findall('direct link" value="(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(str(items),html)
	if items:
		link = items[0].rstrip('/')
		title,url = VEVIO(link)
		return title,url
	else: return [],[]

def MP4UPLOAD(url):
	url = url.replace('embed-','')
	url = url.replace('.html','')
	id = url.split('/')[-1]
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { "id":id , "op":"download2" }
	import requests
	request = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False)
	url = request.headers['Location']
	if url!='':
		return [url],[url]
	else: return [],[]

def WINTVLIVE(url):
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-WINTVLIVE-1st')
	items = re.findall('mp4: \[\'(.*?)\'',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def ARCHIVE(url):
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-ARCHIVE-1st')
	items = re.findall('source src="(.*?)"',html,re.DOTALL)
	#logging.warning('https://archive.org' + items[0])
	if items:
		url = url = 'https://archive.org' + items[0]
		return [url],[url]
	else: return [],[]

def PUBLICVIDEOHOST(url):
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-PUBLICVIDEOHOST-1st')
	items = re.findall('file: "(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(str(items),html)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def ESTREAM(url):
	#url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-ESTREAM-1st')
	items = re.findall('video preload.*?src=.*?src="(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0],items[0])
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]








#####################################################
#         FAILED
#	NOT WORKING ANYMORE
#####################################################
"""
def HELAL_PROBLEM(url):
	# https://playr.4helal.tv/4qlqt9d3813e
	headers = { 'User-Agent' : '' }
	#url = url.replace('http:','https:')
	html = openURL_cached(NO_CACHE,url,'',headers,'','RESOLVERS-VIDBOB-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0].rstrip('/'),'')
	if items:
		url = items[0].replace('https:','http:')
		return [url],[url]
	else: return [],[]

def VIMPLE_PROBLEM(link):
	id = link.split('id=')[1]
	headers = { 'User-Agent' : '' }
	url = 'http://player.vimple.ru/iframe/' + id
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VIMPLE-1st')
	items = re.findall('true,"url":"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0].replace('\/','/')
		return [url],[url]
	else: return [],[]

def VIDSHARE_PROBLEM(url):
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VIDSHARE-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def INTOUPLOAD_PROBLEM(url):
	# https://intoupload.net/w2j4lomvzopd
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-INTOUPLOAD-1st')
	html_blocks = re.findall('POST.*?(.*?)clearfix',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('op" value="(.*?)".*?id" value="(.*?)".*?rand" value="(.*?)".*?left:(.*?)px;.*?&#(.*?);.*?left:(.*?)px;.*?&#(.*?);.*?left:(.*?)px;.*?&#(.*?);.*?left:(.*?)px;.*?&#(.*?);',block,re.DOTALL)
	op,id,rand,pos1,num1,pos2,num2,pos3,num3,pos4,num4 = items
	captcha = { int(pos1):chr(int(num1)) , int(pos2):chr(int(num2)) , int(pos3):chr(int(num3)) , int(pos4):chr(int(num4)) }
	code = ''
	for char in sorted(captcha):
		code += captcha[char]
	#xbmcgui.Dialog().ok(code,str(captcha))
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'id':id , 'op':op , 'code':code , 'rand':rand }
	data = urllib.urlencode(payload)
	progress = xbmcgui.DialogProgress()
	progress.create('Waiting 15 seconds ...')
	for i in range(0,15):
		progress.update(i*100/15,str(15-i))
		xbmc.sleep(1000)
		if progress.iscanceled(): return
	progress.close()
	html = openURL_cached(SHORT_CACHE,url,data,headers,'','RESOLVERS-INTOUPLOAD-2nd')
	items = re.findall('target_type.*?href="(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VIDBOM_PROBLEM(url):
	# https://www.vidbom.com/embed-05ycj7325jae.html
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-VIDBOM-1st')
	xbmc.sleep(1500)
	items = re.findall('file: "(.*?)"',html,re.DOTALL)
	slidesURL = items[0].rstrip('/')
	html2 = openURL_cached(SHORT_CACHE,slidesURL,'','','','RESOLVERS-VIDBOM-2nd')
	xbmc.sleep(1500)
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def GOUNLIMITED_OLD(url):
	url = url.replace('embed-','')
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	items = re.findall('data(.*?)hide.*?embed(.*?)hash',html,re.DOTALL)
	id = items[0][0].replace('|','')
	hash = items[0][1].split('|')
	newhash = ''
	for i in reversed(hash):
		newhash += i + '-'
	newhash = newhash.strip('-')
	#url = 'https://gounlimited.to/dl?op=view&file_code='+id+'&hash='+newhash+'&embed=&adb=1'
	#html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	url = "https://gounlimited.to/dl"
	querystring = { "op":"view","file_code":"o1yo2xwdmk0l","hash":newhash,"embed":"","adb":"1" }
	headers = {
		'accept': "*/*",
		'dnt': "1",
		'x-requested-with': "XMLHttpRequest",
		'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
		'referer': "https://gounlimited.to/o1yo2xwdmk0l.html",
		'accept-encoding': "gzip, deflate, br",
		'accept-language': "en-US,en;q=0.9,ar;q=0.8"
		}
	import requests
	html = requests.request('GET', url, headers=headers, params=querystring)
	items = re.findall('video="" src="(.*?)"',html.text,re.DOTALL)
	#xbmcgui.Dialog().ok(str(html.content),str(len(html.content)))
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VEVIO_PROBLEM(url):
	# https://vev.io/qnoxd4yqyy30
	id = url.split('/')[-1]
	url = 'https://vev.io/api/serve/video/' + id
	headers = { 'User-Agent' : '' }
	titleLIST,linkLIST = [],[]
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VEVIO-1st')
	html_blocks = re.findall('qualities":\{(.*?)\}',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('"(.*?)":"(.*?)"',block,re.DOTALL)
		for label,link in items:
			titleLIST.append(label)
			linkLIST.append(link)
	return titleLIST,linkLIST



"""



