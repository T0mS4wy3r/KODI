# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='RESOLVERS'
doNOTresolveMElist = [ 'mystream','vimple','vidbom','gounlimited' ]

def PLAY(linkLIST,script_name,text=''):
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
					result = PLAY_LINK(url,script_name,text)
			if result in ['playing','canceled1'] or len(serversLIST)==1: break
			elif result in ['failed','timeout','tried']: break
			elif result not in ['canceled2','https']: xbmcgui.Dialog().ok('السيرفر لم يعمل','جرب سيرفر غيره')
	if result=='unresolved' and len(serversLIST)>0: xbmcgui.Dialog().ok('سيرفر هذا الفيديو لم يعمل','جرب فيديو غيره')
	elif result in ['failed','timeout']: xbmcgui.Dialog().ok('الفيديو لم يعمل',' ')
	"""
	elif result in ['Canceled1','Canceled2']:
		#xbmc.log('[ '+addon_id+' ]:   Test:   '+sys.argv[0]+sys.argv[2], level=xbmc.LOGNOTICE)
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

def PLAY_LINK(url,script_name,text=''):
	url = url.strip(' ').strip('&').strip('?').strip('/')
	titleLIST,linkLIST = RESOLVE(url)
	if 'IsPlayable=no' in text: IsPlayable = 'no'
	else: IsPlayable='yes'
	if linkLIST:
		while True:
			if len(linkLIST)==1: selection = 0
			else: selection = xbmcgui.Dialog().select('اختر الملف المناسب:', titleLIST)
			if selection == -1: result = 'canceled2'
			else:
				videoURL = linkLIST[selection]
				#xbmcgui.Dialog().ok('',str(videoURL))
				if 'moshahda.' in videoURL and 'download_orig' in videoURL:
					videoURL1,videoURL2 = MOVIZLAND(videoURL)
					if videoURL2: videoURL = videoURL2[0]
					else: videoURL = ''
				if videoURL=='': result = 'unresolved'
				else: result = PLAY_VIDEO(videoURL,script_name,IsPlayable)
			if result in ['playing','canceled2'] or len(linkLIST)==1: break
			elif result in ['failed','timeout','tried']: break
			else: xbmcgui.Dialog().ok('الملف لم يعمل','جرب ملف غيره')
		"""
		if 'youtube.mpd' in linkLIST[0]:
			#xbmcgui.Dialog().ok('click ok to shutdown the http server','')
			#html = openURL_cached(NO_CACHE,'http://localhost:64000/shutdown','','','','RESOLVERS-PLAY_LINK-1st')
			titleLIST[0].shutdown()
		"""
	else:
		result = 'unresolved'
		videofiletype = re.findall('(.ts|.mp4|.m3u|.m3u8|.mpd|.mkv|.flv|.mp3)(|\?.*?|/\?.*?|\|.*?)&&',url+'&&',re.DOTALL)
		if videofiletype: result = PLAY_VIDEO(url,script_name,IsPlayable)
	return result
	#title = xbmc.getInfoLabel( "ListItem.Label" )
	#if 'سيرفر عام مجهول' in title:
	#	import PROBLEMS
	#	PROBLEMS.MAIN(156)
	#	return ''

"""
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
"""

def RESOLVABLE(url):
	url2 = url.lower().split('name=',1)[0].strip('?').strip('/').strip('&')
	#xbmcgui.Dialog().ok(url,url2)
	server = url2.split('/')[2].lower()
	private,known,external,named = '','','',''
	# private	: سيرفر خاص
	# known		: سيرفر عام معروف
	# external	: سيرفر عام خارجي
	# named		: سيرفر عام محدد
	if   any(value in server for value in doNOTresolveMElist): pass
	elif 'akoam'		in server and 'name=' not in url: private = 'akoam'
	elif 'moshahda'		in server:	private = 'Movizland '+url.split('name=')[1].lower()
	elif 'name=' 		in url:		named = url.split('name=')[1].lower()
	elif 'arabloads'	in server:	known = 'arabloads'
	elif 'archive'		in server:	known = 'archive'
	elif 'catch.is'	 	in server:	known = 'catch'
	elif 'filerio'		in server:	known = 'filerio'
	#elif 'estream'	 	in server:	known = 'estream'
	#elif 'gounlimited'	in server:	known = 'gounlimited'
	#elif 'intoupload' 	in server:	known = 'intoupload'
	#elif 'thevideo'	in server:	known = 'thevideo'
	elif 'govid'		in server:	known = 'govid'
	elif 'liivideo' 	in server:	known = 'liivideo'
	elif 'mp4upload'	in server:	known = 'mp4upload'
	elif 'publicvideohost' in server:	known = 'publicvideohost'
	elif 'rapidvideo' 	in server:	known = 'rapidvideo'
	elif 'top4top'		in server:	known = 'top4top'
	elif 'upbom' 		in server:	known = 'upbom'
	elif 'uppom' 		in server:	known = 'uppom'
	elif 'uptobox' 		in server:	known = 'uptobox'
	elif 'uptostream'	in server:	known = 'uptostream'
	elif 'uqload' 		in server:	known = 'uqload'
	elif 'vcstream' 	in server:	known = 'vcstream'
	elif 'vidbob'		in server:	known = 'vidbob'
	#elif 'vev.io'	 	in server:	known = 'vev'
	#elif 'playr.4helal'in server:	private = 'helal'
	#elif 'vidbom'		in server:	known = 'vidbom'
	#elif 'vidhd' 		in server:	known = 'vidhd'
	#elif 'vidshare' 	in server:	known = 'vidshare'
	elif 'vidoza' 		in server:	known = 'vidoza'
	elif 'watchvideo' 	in server:	known = 'watchvideo'
	elif 'wintv.live'	in server:	known = 'wintv.live'
	elif 'youtu'	 	in server:	private = 'youtube'
	elif 'zippyshare'	in server:	known = 'zippyshare'
	else:
		import urlresolver
		resolvable = urlresolver.HostedMediaFile(url2).valid_url()
		if resolvable: external = url2.split('//')[1].split('/')[0]
	if private!='': result = ' سيرفر خاص ' + private	
	elif known!='': result = ' سيرفر عام معروف ' + known
	elif external!='': result = 'سيرفر عام خارجي ' + external
	elif named!='':
		if '__' not in named: result = 'سيرفر عام محدد ' + named
		else:
			parts = named.split('__')
			name,type = parts
			if type=='download': result = 'سيرفر تحميل عام ' + name
			elif type=='watch': result = 'سيرفر  مشاهدة عام ' + name
			else: result = 'سيرفر  مشاهدة وتحميل عام  ' + name
	else: result = 'سيرفر مجهول ' + server
	return result

"""
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
			t = (now+cacheperiod,url,str(titleLIST),str(linkLIST))
			c.execute("INSERT INTO resolvecache VALUES (?,?,?,?)",t)
			conn.commit()
		conn.close()
		#t2 = time.time()
		#xbmcgui.Dialog().notification(message,str(int(t2-t1))+' ms')
	return titleLIST,linkLIST
"""

def RESOLVE(url):
	#url = 'https://gounlimited.to/embed-wqsi313vbpua.html'
	xbmc.log('[ '+addon_id+' ]:   Started resolving   URL:[ '+url+' ]', level=xbmc.LOGNOTICE)
	url2 = url.split('name=',1)[0].strip('?').strip('/').strip('&')
	server = url2.lower().split('/')[2]
	#if 'gounlimited' in server: url2 = url2.replace('https:','http:')
	#xbmcgui.Dialog().ok(url2,'')
	titleLIST,linkLIST = [],[]
	if any(value in server for value in doNOTresolveMElist): titleLIST,linkLIST = [],[]
	elif 'moshahda'		in server: titleLIST,linkLIST = MOVIZLAND(url)
	elif 'akoam'		in server: titleLIST,linkLIST = AKOAM(url)
	elif 'shahid4u'		in server: titleLIST,linkLIST = SHAHID4U(url2)
	elif 'arblionz'		in server: titleLIST,linkLIST = ARABLIONZ(url2)
	elif 'e5tsar'		in server: titleLIST,linkLIST = E5TSAR(url2)
	elif 'arabloads'	in server: titleLIST,linkLIST = ARABLOADS(url2)
	elif 'archive'		in server: titleLIST,linkLIST = ARCHIVE(url2)
	elif 'catch.is'	 	in server: titleLIST,linkLIST = CATCHIS(url2)
	#elif 'estream'	 	in server: titleLIST,linkLIST = ESTREAM(url2)
	#elif 'gounlimited'	in server: titleLIST,linkLIST = GOUNLIMITED(url2)
	#elif 'intoupload' 	in server: titleLIST,linkLIST = INTOUPLOAD(url2)
	#elif 'thevideo'	in server: titleLIST,linkLIST = THEVIDEO(url2)
	elif 'filerio'		in server: titleLIST,linkLIST = FILERIO(url2)
	elif 'govid'		in server: titleLIST,linkLIST = GOVID(url2)
	elif 'liivideo' 	in server: titleLIST,linkLIST = LIIVIDEO(url2)
	elif 'mp4upload'	in server: titleLIST,linkLIST = MP4UPLOAD(url2)
	elif 'publicvideohost' in server: titleLIST,linkLIST = PUBLICVIDEOHOST(url2)
	elif 'rapidvideo' 	in server: titleLIST,linkLIST = RAPIDVIDEO(url2)
	elif 'top4top'		in server: titleLIST,linkLIST = TOP4TOP(url2)
	elif 'upbom' 		in server: titleLIST,linkLIST = UPBOM(url2)
	elif 'uppom' 		in server: titleLIST,linkLIST = UPBOM(url2)
	elif 'uptobox' 		in server: titleLIST,linkLIST = UPTO(url2)
	elif 'uptostream'	in server: titleLIST,linkLIST = UPTO(url2)
	elif 'uqload' 		in server: titleLIST,linkLIST = UQLOAD(url2)
	elif 'vcstream' 	in server: titleLIST,linkLIST = VCSTREAM(url2)
	elif 'vidbob'		in server: titleLIST,linkLIST = VIDBOB(url2)
	#elif 'vev.io'	 	in server: titleLIST,linkLIST = VEVIO(url2)
	#elif 'playr.4helal'	in server: titleLIST,linkLIST = HELAL(url2)
	#elif 'vidbom'		in server: titleLIST,linkLIST = VIDBOM(url2)
	#elif 'vidhd' 		in server: titleLIST,linkLIST = VIDHD(url2)
	#elif 'vidshare' 	in server: titleLIST,linkLIST = VIDSHARE(url2)
	elif 'vidoza' 		in server: titleLIST,linkLIST = VIDOZA(url2)
	elif 'watchvideo' 	in server: titleLIST,linkLIST = WATCHVIDEO(url2)
	elif 'wintv.live'	in server: titleLIST,linkLIST = WINTVLIVE(url2)
	elif 'youtu'		in server: titleLIST,linkLIST = YOUTUBE(url2)
	elif 'y2u.be'		in server: titleLIST,linkLIST = YOUTUBE(url2)
	elif 'zippyshare'	in server: titleLIST,linkLIST = ZIPPYSHARE(url2)
	else: titleLIST,linkLIST = URLRESOLVER(url2)
	if len(linkLIST)==0: xbmc.log('[ '+addon_id+' ]:   Resolving Failed   URL:[ '+url+' ]', level=xbmc.LOGNOTICE)
	else: xbmc.log('['+addon_id+']:   Resolving succeded   URL:[ '+str(linkLIST)+' ]', level=xbmc.LOGNOTICE)
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
		t = (now+cacheperiod,str(linkLIST),str(serversLIST),str(urlLIST))
		c.execute("INSERT INTO serverscache VALUES (?,?,?,?)",t)
		conn.commit()
	conn.close()
	#t2 = time.time()
	#xbmcgui.Dialog().notification(message,str(int(t2-t1))+' ms')
	return serversLIST,urlLIST

def SERVERS(linkLIST,script_name=''):
	serversLIST,urlLIST,unknownLIST,serversDICT = [],[],[],[]
	linkLIST = list(set(linkLIST))
	#selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', NEWlinkLIST)
	#if selection == -1 : return ''
	for link in linkLIST:
		if link=='': continue
		serverNAME = RESOLVABLE(link)
		serversDICT.append( [serverNAME,link] )
	sortedDICT = sorted(serversDICT, reverse=False, key=lambda key: key[0])
	for server,link in sortedDICT:
		serversLIST.append(server)
		urlLIST.append(link)
	#lines = len(unknownLIST)
	#if lines>0:
	#	message = '\\n'
	#	for link in unknownLIST:
	#		message += link + '\\n'
	#	subject = 'Unknown Resolvers = ' + str(lines)
	#	result = SEND_EMAIL(subject,message,'no','','FROM-RESOLVERS-'+script_name)
	return serversLIST,urlLIST

def	URLRESOLVER(url):
	import urlresolver
	# urlresolver might fail either with an error or returns value False
	try: link = urlresolver.HostedMediaFile(url).resolve()
	except: link = False
	if link==False: return [],[]
	return [link],[link]

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
		#xbmcgui.Dialog().ok(link,'')
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
		titleLISTtemp,titleLIST,linkLISTtemp,linkLIST,resolutionLIST = [],[],[],[],[]
		for link,title in items:
			if '.m3u8' in link:
				titleLISTtemp,linkLISTtemp = M3U8_EXTRACTOR(link)
				linkLIST = linkLIST + linkLISTtemp
				if titleLISTtemp[0]=='-1': titleLIST.append(' سيرفر خاص '+'m3u8 '+name2)
				else:
					for title in titleLISTtemp:
						titleLIST.append(' سيرفر خاص '+'m3u8 '+name2+' '+title)
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
	html = openURL_cached(SHORT_CACHE,url2,'',headers,'','RESOLVERS-E5TSAR-1st')
	items = re.findall('Please wait.*?href=\'(.*?)\'',html,re.DOTALL)
	url = items[0]
	titleLIST,linkLIST = RESOLVE(url)
	#xbmcgui.Dialog().ok(items[0],html)
	return titleLIST,linkLIST

def ARABLIONZ(link):
	# http://arablionz/?postid=159485&serverid=0
	parts = re.findall('postid=(.*?)&serverid=(.*?)&&',link+'&&',re.DOTALL|re.IGNORECASE)
	postid,serverid = parts[0]
	url = 'https://arblionz.tv/ajaxCenter?_action=getserver&_post_id='+postid+'&serverid='+serverid
	headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
	url2 = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-ARABLIONZ-1st')
	titleLIST,linkLIST = RESOLVE(url2)
	return titleLIST,linkLIST

def SHAHID4U(link):
	# http://shahid4u/?postid=126981&serverid=5
	parts = re.findall('postid=(.*?)&serverid=(.*?)&&',link+'&&',re.DOTALL|re.IGNORECASE)
	postid,serverid = parts[0]
	url = 'https://on.shahid4u.net/ajaxCenter?_action=getserver&_post_id='+postid+'&serverid='+serverid
	headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
	url2 = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-SHAHID4U-1st')
	titleLIST,linkLIST = RESOLVE(url2)
	return titleLIST,linkLIST

def AKOAM(link):
	# http://go.akoam.net/5cf68c23e6e79
	response = openURL_requests_cached(LONG_CACHE,'GET', link, '', '', True,'','RESOLVERS-AKOAM-1st')
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
		response = openURL_requests_cached(REGULAR_CACHE,'GET', 'https://akoam.net/', '', '', False,'','RESOLVERS-AKOAM-2nd')
		relocateURL = response.headers['Location']
		url = url.replace('https://akoam.net/',relocateURL)
		headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' , 'Referer':url }
		response = openURL_requests_cached(SHORT_CACHE,'POST', url, '', headers, False,'','RESOLVERS-AKOAM-3rd')
		html = response.text
		#xbmc.log(html, level=xbmc.LOGNOTICE)
		#xbmcgui.Dialog().ok(url,html)
		items = re.findall('direct_link":"(.*?)"',html,re.DOTALL|re.IGNORECASE)
		if not items:
			items = re.findall('<iframe.*?src="(.*?)"',html,re.DOTALL|re.IGNORECASE)
			if not items:
				items = re.findall('<embed.*?src="(.*?)"',html,re.DOTALL|re.IGNORECASE)
		if items:
			url2 = items[0].replace('\/','/')
			url2 = url2.rstrip('/')
			if 'http' not in url2: url2 = 'http:' + url2
			#xbmcgui.Dialog().ok(link,url2)
			if 'name=' in link: titleLIST,linkLIST = RESOLVE(url2)
			else: titleLIST,linkLIST = ['ملف التحميل'],[url2]
			"""
			splits = url.split('/')
			server = '/'.join(splits[0:3])
			hash_data = url.split('/')[4]
			watch_title = url.split('/')[-1]
			url3 = server + '/watching/'+hash_data+'/'+watch_title
			response = openURL_requests_cached(SHORT_CACHE,'GET', url3, '', '', False,'','RESOLVERS-AKOAM-4th')
			html = response.text
			url3 = re.findall('file: "(.*?)"',html,re.DOTALL|re.IGNORECASE)[0]
			titles2,urls2 = ['ملف المشاهدة المباشرة'],[url3]
			titleLIST,linkLIST = titleLIST+titles2,linkLIST+urls2
			"""
		else: return [],[]
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
	if '/embed/' in url: id = url.split('/')[4]
	else: id = url.split('/')[-1]
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
	titleLIST,linkLIST = [],[]
	for link,label,res in items:
		titleLIST.append(label+' '+res)
		linkLIST.append(link)
	return titleLIST,linkLIST

def WATCHVIDEO(url):
	# https://watchvideo.us/embed-rpvwb9ns8i73.html
	url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-WATCHVIDEO-1st')
	items = re.findall("download_video\('(.*?)','(.*?)','(.*?)'\)\">(.*?)</a>.*?<td>(.*?),.*?</td>",html,re.DOTALL)
	items = set(items)
	titleLIST,linkLIST = [],[]
	for id,mode,hash,label,res in items:
		url = 'https://watchvideo.us/dl?op=download_orig&id='+id+'&mode='+mode+'&hash='+hash
		html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-WATCHVIDEO-2nd')
		items = re.findall('direct link.*?href="(.*?)"',html,re.DOTALL)
		for link in items:
			titleLIST.append(label+' '+res)
			linkLIST.append(link)
	return titleLIST,linkLIST

def UPBOM(url):
	# http://upbom.live/hm9opje7okqm/TGQSDA001.The.Vanishing.2018.1080p.WEB-DL.Cima4U.mp4.html
	url = url.replace('upbom.live','uppom.live')
	url = url.split('/')
	id = url[3]
	url = '/'.join(url[0:4])
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
	titleLIST,linkLIST = [],[]
	if items:
		titleLIST.append('mp4')
		linkLIST.append(items[0][1])
		titleLIST.append('m3u8')
		linkLIST.append(items[0][0])
	return titleLIST,linkLIST

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
	#hls ts example			url = 'https://www.youtube.com/watch?v=Gf2-NStSsNw'
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
	subtitleURL,dashURL,hlsURL,finalURL = '','','',''
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
	html_blocks = re.findall('hlsManifestUrl":"(.*?)"',html,re.DOTALL)
	if html_blocks:
		hlsURL = html_blocks[0]
		#html2 = openURL_cached(SHORT_CACHE,hlsURL,'','','','RESOLVERS-YOUTUBE-3rd')
		#items = re.findall('X-MEDIA:URI="(.*?)",TYPE=SUBTITLES,GROUP-ID="vtt',html2,re.DOTALL)
		#if items: subtitleURL = items[0]#+'&fmt=vtt&type=track&tlang='
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
			#xbmcgui.Dialog().ok('',jshtml)
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
			#xbmc.log('[ '+addon_id+' ]:   dict:[ '+str(dict)+' ]', level=xbmc.LOGNOTICE)
			#xbmc.log('url='+dict['url'], level=xbmc.LOGNOTICE)
	#xbmc.log('[ '+addon_id+' ]:   streams:[ '+str(streams)+' ]', level=xbmc.LOGNOTICE)
	for dict in streams:
		filetype,codec,quality2,type2,codecs,bitrate = 'unknown','unknown','unknown','Unknown','',0
		try:
			type = dict['type']
			#xbmc.log('[ '+addon_id+' ]:   Type:[ '+type+' ]', level=xbmc.LOGNOTICE)
			type = type.replace('+','')
			items = re.findall('(.*?)/(.*?);.*?"(.*?)"',type,re.DOTALL)
			type2,filetype,codecs = items[0]
			codecs2 = codecs.split(',')
			codec = ''
			for item in codecs2: codec += item.split('.')[0]+','
			codec = codec.strip(',')
			if type2=='text': continue
			elif ',' in type:
				type2 = 'A+V'
				bitrate = 0
				quality2 = dict['quality']
				format = re.findall(','+dict['itag']+'/(.*?),',','+format_block+',',re.DOTALL)
				if format:
					dict['size'] = format[0]
					quality2 = dict['size'].split('x')[1]
			elif type2=='video':
				type2 = 'Video'
				bitrate = int(dict['bitrate'])
				#quality2 = str(bitrate/1024)+'kbps  '+dict['quality_label']+'  '+dict['size']+'  '+dict['fps']+'fps'
				quality2 = dict['size'].split('x')[1]+'  '+str(bitrate/1024)+'kbps  '+dict['fps']+'fps'
			elif type2=='audio':
				type2 = 'Audio'
				bitrate = int(dict['bitrate'])
				quality2 = str(bitrate/1024)+'kbps  '+str(int(dict['audio_sample_rate'])/1000)+'khz  '+dict['audio_channels']+'ch'
		except: pass
		title = type2+':  '+filetype+'  '+quality2+'  ('+codec+','+dict['itag']+')'
		dict['title'] = title
		dict['type2'] = type2
		dict['filetype'] = filetype
		dict['codecs'] = codecs
		dict['bitrate'] = bitrate
		dict['quality'] = quality2.split(' ')[0].split('kbps')[0]
		if filetype=='mp4': dict['sort'] = 1
		else: dict['sort'] = 4
		if 'dur=' in dict['url']:
			dict['duration'] = round(0.5+float(dict['url'].split('dur=',1)[1].split('&',1)[0]))
		streams2.append(dict)
	#xbmc.log('[ '+addon_id+' ]:   streams2:[ '+str(streams2)+' ]', level=xbmc.LOGNOTICE)
	videoTitleLIST,audioTitleLIST,muxedTitleLIST,mpdaudioTitleLIST,mpdvideoTitleLIST,allTitleLIST = [],[],[],[],[],[]
	videoDictLIST,audioDictLIST,muxedDictLIST,mpdaudioDictLIST,mpdvideoDictLIST,allvideoDictLIST,allaudioDictLIST = [],[],[],[],[],[],[]
	HighestDictTitle,HighestDictVideo,HighestDictAudio = [],[],[]
	if dashURL!='':
		dict = {}
		dict['type2'] = 'A+V'
		dict['filetype'] = 'mpd'
		dict['title'] = dict['type2']+':  '+dict['filetype']+'  '+'دقة اوتوماتيكية'
		dict['url'] = dashURL
		dict['quality'] = '0' # for single dashURL any number will produce same sort order
		dict['sort'] = 7
		streams2.append(dict)
	if hlsURL!='':
		titleLISTtemp,linkLISTtemp = M3U8_EXTRACTOR(hlsURL)
		zippedLIST = zip(titleLISTtemp,linkLISTtemp)
		for title,link in zippedLIST:
			dict = {}
			dict['type2'] = 'A+V'
			dict['filetype'] = 'm3u8'
			dict['quality'] = title
			dict['url'] = link
			if title=='-1': dict['title'] = dict['type2']+':  '+dict['filetype']+'  '+'دقة اوتوماتيكية'
			else: dict['title'] = dict['type2']+':  '+dict['filetype']+'  '+dict['quality']
			dict['sort'] = 9
			streams2.append(dict)
	streams2 = sorted(streams2, reverse=True, key=lambda key: int(key['quality']))
	streams2 = sorted(streams2, reverse=False, key=lambda key: key['sort'])
	if not streams2: return [],[]
	first = ''
	for dict in streams2:
		if dict['type2']=='A+V':
			dict['title'] = dict['title'].replace('A+V:  ','')
			allTitleLIST.append(dict['title'])
			allvideoDictLIST.append(dict)
			allaudioDictLIST.append({})
			if first!=dict['filetype'] and 'دقة اوتوماتيكية' not in dict['title']:
				first = dict['filetype']
				HighestDictTitle.append(dict['title'])
				HighestDictVideo.append(dict)
				HighestDictAudio.append({})
		if dict['type2']=='Video':
			videoTitleLIST.append(dict['title'])
			videoDictLIST.append(dict)
		elif dict['type2']=='Audio':
			audioTitleLIST.append(dict['title'])
			audioDictLIST.append(dict)
		elif dict['filetype']!='mpd':
			muxedTitleLIST.append(dict['title'].replace('A+V:  ',''))
			muxedDictLIST.append(dict)
		if dict['type2']=='Video' and dict['init']!='0-0' and 'avc' in dict['codecs']:
			mpdvideoTitleLIST.append(dict['title'])
			mpdvideoDictLIST.append(dict)
		elif dict['type2']=='Audio' and dict['init']!='0-0' and 'mp4a' in dict['codecs']:
			mpdaudioTitleLIST.append(dict['title'])
			mpdaudioDictLIST.append(dict)
	#highest,highestAudioDICT = 0,{}
	#for dict in mpdaudioDictLIST:
	#	if dict['bitrate']>highest: highest,highestAudioDICT = dict['bitrate'],dict
	#audiodict = highestAudioDICT
	for audiodict in mpdaudioDictLIST:
		audioBitrate = int(audiodict['bitrate']/1024)
		for videodict in mpdvideoDictLIST:
			videoBitrate = int(videodict['bitrate']/1024)
			title = videodict['title'].replace('Video:  '+videodict['filetype'],'mpd')+'('+audiodict['title'].split('(',1)[1]
			title = title.replace(str(videoBitrate)+'kbps',str(videoBitrate+audioBitrate)+'kbps')
			allTitleLIST.append(title)
			allvideoDictLIST.append(videodict)
			allaudioDictLIST.append(audiodict)
			if first!=videodict['filetype']:
				first = videodict['filetype']
				HighestDictTitle.append(title)
				HighestDictVideo.append(videodict)
				HighestDictAudio.append(audiodict)				
	selectMenu,choiceMenu = [],[]
	if HighestDictTitle:
		z = zip(HighestDictTitle,HighestDictVideo,HighestDictAudio)
		#z = set(z)
		z = sorted(z, reverse=True, key=lambda key: int(key[0].split('  ')[1]))
		HighestDictTitle,HighestDictVideo,HighestDictAudio = zip(*z)
		#HighestDictTitle,HighestDictVideo,HighestDictAudio = list(HighestDictTitle),list(HighestDictVideo),list(HighestDictAudio)
		for title in HighestDictTitle:
			selectMenu.append(title) ; choiceMenu.append('highest')
	if dashURL!='': selectMenu.append('mpd صورة وصوت دقة اوتوماتيك') ; choiceMenu.append('dash')
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
		if choice=='dash':
			finalURL = dashURL
			break
		elif choice in ['audio','video','muxed']:
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
		elif choice=='all':
			selection = xbmcgui.Dialog().select('اختر الملف المناسب:', allTitleLIST)
			if selection!=-1:
				videoDICT = allvideoDictLIST[selection]
				if 'mpd' in allTitleLIST[selection] and videoDICT['url']!=dashURL:
					audioDICT = allaudioDictLIST[selection]
					need_mpd_server = True
				else: finalURL = videoDICT['url']
				break
		elif choice=='highest':
			videoDICT = HighestDictVideo[selection]
			if 'mpd' in HighestDictTitle[selection]:
				audioDICT = HighestDictAudio[selection]
				need_mpd_server = True
			else: finalURL = videoDICT['url']
			break
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
		import BaseHTTPServer
		class HTTP_SERVER(BaseHTTPServer.HTTPServer):
			#mpd = 'mpd = used when not using __init__'
			def __init__(self,port='64000',mpd='mpd = from __init__'):
				BaseHTTPServer.HTTPServer.__init__(self,('localhost',port), HTTP_HANDLER)
				self.port = port
				self.mpd = mpd
				#print('server is up now listening on port: '+str(port))
			def start(self):
				self.threads = CustomThread()
				self.threads.start_new_thread(1,False,self.serve)
			def serve(self):
				#print('serving requests started')
				self.keeprunning = True
				#counter = 0
				while self.keeprunning:
					#counter += 1
					#print('running a single handle_request() now: '+str(counter)+'')
					#settimeout does not work due to error message if it kills an http request
					#self.socket.settimeout(10) # default is 60 seconds (it will serve one request within 60 seconds)
					self.handle_request()
				#print('serving requests stopped\n')
			def stop(self):
				self.keeprunning = False
				self.send_dummy_http()	# needed to force self.handle_request() to serve its last request
			def shutdown(self):
				self.stop()
				self.socket.close()
				self.server_close()
				time.sleep(1)
				#print('server is down now\n')
			def load(self,mpd):
				self.mpd = mpd
			def send_dummy_http(self):
				conn = httplib.HTTPConnection('localhost:'+str(self.port))
				conn.request("HEAD", "/")
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
	else: httpd = ''
	titleLIST,linkLIST = [],[]
	if finalURL!='': linkLIST = [ [finalURL,subtitleURL,httpd] ]
	return titleLIST,linkLIST

def VIDBOB(url):
	# https://vidbob.com/v6rnlgmrwgqu
	headers = { 'User-Agent' : '' }
	#url = url.replace('http:','https:')
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VIDBOB-1st')
	items = re.findall('file:"(.*?)"(,label:"(.*?)"|)\}',html,re.DOTALL)
	items = set(items)
	items = sorted(items, reverse=True, key=lambda key: key[2])
	titleLISTtemp,titleLIST,linkLISTtemp,linkLIST = [],[],[],[]
	for link,dummy,label in items:
		link = link.replace('https:','http:')
		if '.m3u8' in link:
			titleLISTtemp,linkLISTtemp = M3U8_EXTRACTOR(link)
			linkLIST = linkLIST + linkLISTtemp
			if titleLISTtemp[0]=='-1': titleLIST.append('سيرفر خاص'+'   m3u8')
			else:
				for title in titleLISTtemp:
					titleLIST.append('سيرفر خاص'+'   m3u8   '+title)
		else:
			title = 'سيرفر خاص'+'   mp4   '+label
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

def GOVID(url):
	# https://govid.co/video/play/AAVENd
	headers = { 'User-Agent' : '' }
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','RESOLVERS-GOVID-1st')
	items = re.findall('source src="(.*?)"',html,re.DOTALL)
	titleLISTtemp,titleLIST,linkLIST = [],[],[],[]
	if items:
		link = items[0]
		if '.m3u8' in link:
			titleLISTtemp,linkLIST = M3U8_EXTRACTOR(link)
			if titleLISTtemp[0]=='-1': titleLIST.append('سيرفر خاص'+'   m3u8')
			else:
				for title in titleLISTtemp:
					titleLIST.append('سيرفر خاص'+'   m3u8   '+title)
		else:
			title = 'سيرفر خاص'+'   mp4'
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

def MP4UPLOAD(url):
	url = url.replace('embed-','')
	url = url.replace('.html','')
	id = url.split('/')[-1]
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { "id":id , "op":"download2" }
	request = openURL_requests_cached(SHORT_CACHE,'POST', url, payload, headers, False,'','RESOLVERS-MP4UPLOAD-1st')
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
def THEVIDEO_PROBLEM(url):
	# https://thevideo.me/embed-xldtqj5deiyj-780x439.html
	url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-THEVIDEO-1st')
	items = re.findall('direct link" value="(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(str(items),html)
	if items:
		link = items[0].rstrip('/')
		title,url = VEVIO(link)
		return title,url
	else: return [],[]

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

def GOUNLIMITED_PROBLEM(url):
	# https://gounlimited.to/embed-wqsi313vbpua.html
	# http://gounlimited.to/embed-bhczqclxokgq.html
	url = url.replace('https:','http:')
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	html_blocks = re.findall('function\(p,a,c,k,e,d\)(.*?)split',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall(",'(.*?)'",block,re.DOTALL)
		items = items[-1].split('|')
		link = items[12]+'://'+items[85]+'.'+items[11]+'.'+items[10]+'/'+items[84]+'/v.mp4'
		return [link],[link]
	else: return [],[]
	#link = 'https://shuwaikh.gounlimited.to/'+id+'/v.mp4'
	#link = 'https://fs67.gounlimited.to/'+id+'/v.mp4'

def VIDHD_PROBLEM(url):
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




"""



