# -*- coding: utf-8 -*-
from LIBRARY import *
from urlresolver import HostedMediaFile as urlresolver_HostedMediaFile

script_name='RESOLVERS'
doNOTresolveMElist = [ 'mystream','vimple','vidbom' ]

def MAIN(mode,url,text):
	if mode==160: PLAY_LINK(url,text)
	return

def PLAY(linkLIST,script_name):
	serversLIST,urlLIST = SERVERS(linkLIST,script_name)
	if len(serversLIST)==0:
		xbmcgui.Dialog().ok('No video file found','لا يوجد ملف فيديو')
		return ''
	elif len(serversLIST)==1:
		selection = 0
	else:
		selection = xbmcgui.Dialog().select('اختر السيرفر المناسب:', serversLIST)
		if selection == -1 : return ''
	title = serversLIST[selection]
	videoURL = ''
	if 'مجهول' in title:
		from PROBLEMS import MAIN as PROBLEMS_MAIN
		PROBLEMS_MAIN(156)
	else:
		url = urlLIST[selection]
		#xbmcgui.Dialog().ok(url,'')
		videoURL = PLAY_LINK(url,title,script_name)
	#if script_name=='HALACIMA': menu_name='[COLOR FFC89008]HLA [/COLOR]'
	#elif script_name=='4HELAL': menu_name='[COLOR FFC89008]HEL [/COLOR]'
	#elif script_name=='AKOAM': menu_name='[COLOR FFC89008]AKM [/COLOR]'
	#elif script_name=='SHAHID4U': menu_name='[COLOR FFC89008]SHA [/COLOR]'
	#size = len(urlLIST)
	#for i in range(0,size):
	#	title = serversLIST[i]
	#	link = urlLIST[i]
	#	addLink(menu_name+title,link,160,'','',script_name)
	#xbmcplugin.endOfDirectory(addon_handle)
	return videoURL

def PLAY_LINK(url,title,script_name):
	#title = xbmc.getInfoLabel( "ListItem.Label" )
	if 'مجهول' in title:
		from PROBLEMS import MAIN as PROBLEMS_MAIN
		PROBLEMS_MAIN(156)
		return ''
	if '.mp4' in url or '.m3u' in url or '.mpd' in url:
		videoURL = url
	else:
		titleLIST,linkLIST = RESOLVE(url)
		#xbmcgui.Dialog().ok(url,str(linkLIST))
		if len(linkLIST)==0:
			xbmcgui.Dialog().ok('No video file found','لا يوجد ملف فيديو')
			return ''
		elif len(linkLIST)==1:
			videoURL = linkLIST[0]
		else:
			selection = xbmcgui.Dialog().select('اختر الملف المناسب:', titleLIST)
			if selection == -1 : return ''
			videoURL = linkLIST[selection]
	PLAY_VIDEO(videoURL,script_name,'yes')
	return videoURL

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
	elif 'mystream'		in url: result = 'known'
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
	elif 'vidbom'		in url: result = 'known'
	else:
		link = 'http://emadmahdi.pythonanywhere.com/check?url=' + url
		result = openURL(link,'','','','RESOLVERS-CHECK-1st')
	return result

def RESOLVABLE(url):
	url2 = url.lower()
	result1,result2,result3 = '','',''
	if   any(value in url2 for value in doNOTresolveMElist): return ''
	elif 'go.akoam.net'	in url2 and '?n' not in url2: result1 = 'akoam'
	elif 'go.akoam.net'	in url2 and '?n' in url2: result2 = url2.split('?name=')[1]
	elif 'shahid4u.net'	in url2 and '?n' in url2: result2 = url2.split('?name=')[1]
	elif 'e5tsar'		in url2 and '?n' in url2: result3 = url2.split('?name=')[1]
	elif '://moshahda.'	in url2: result1 = 'moshahda'
	elif 'arabloads'	in url2: result1 = 'arabloads'
	elif 'archive'		in url2: result1 = 'archive'
	elif 'catch.is'	 	in url2: result1 = 'catch'
	#elif 'estream'	 	in url2: result1 = 'estream'
	elif 'filerio'		in url2: result1 = 'filerio'
	elif 'gounlimited'	in url2: result1 = 'gounlimited'
	elif 'govid'		in url2: result1 = 'govid'
	elif 'intoupload' 	in url2: result1 = 'intoupload'
	elif 'liivideo' 	in url2: result1 = 'liivideo'
	elif 'mp4upload'	in url2: result1 = 'mp4upload'
	elif 'publicvideohost' in url2: result1 = 'publicvideohost'
	elif 'rapidvideo' 	in url2: result1 = 'rapidvideo'
	elif 'thevideo'		in url2: result1 = 'thevideo'
	elif 'top4top'		in url2: result1 = 'top4top'
	elif 'upbom' 		in url2: result1 = 'upbom'
	elif 'uptobox' 		in url2: result1 = 'uptobox'
	elif 'uptostream'	in url2: result1 = 'uptostream'
	elif 'uqload' 		in url2: result1 = 'uqload'
	elif 'vcstream' 	in url2: result1 = 'vcstream'
	elif 'vev.io'	 	in url2: result1 = 'vev'
	elif 'vidbob'		in url2: result1 = 'vidbob'
	elif 'playr.4helal'	in url2: result1 = 'helal'
	#elif 'vidbom'		in url2: result1 = 'vidbom'
	elif 'vidhd' 		in url2: result1 = 'vidhd'
	elif 'vidoza' 		in url2: result1 = 'vidoza'
	elif 'vidshare' 	in url2: result1 = 'vidshare'
	elif 'watchvideo' 	in url2: result1 = 'watchvideo'
	elif 'wintv.live'	in url2: result1 = 'wintv.live'
	elif 'youtu'	 	in url2: result1 = 'youtube'
	elif 'zippyshare'	in url2: result1 = 'zippyshare'
	else:
		resolvable = urlresolver_HostedMediaFile(url).valid_url()
		if resolvable:
			result2 = url.split('//')[1].split('/')[0]
	#xbmcgui.Dialog().ok(str(url),result1)
	if result1 in ['akoam','helal','moshahda']: result = ' سيرفر خاص ' + result1
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

def RESOLVE(url):
	url2 = url.lower()
	titleLIST,linkLIST = [],[]
	if any(value in url2 for value in doNOTresolveMElist): return ''
	elif 'go.akoam.net'	in url2: titleLIST,linkLIST = AKOAM(url)
	elif 'shahid4u.net'	in url2: titleLIST,linkLIST = SHAHID4U(url)
	elif '://moshahda.'	in url2: titleLIST,linkLIST = MOSHAHDA_ONLINE(url)
	elif 'e5tsar'		in url2: titleLIST,linkLIST = E5TSAR(url)
	elif 'arabloads'	in url2: titleLIST,linkLIST = ARABLOADS(url)
	elif 'archive'		in url2: titleLIST,linkLIST = ARCHIVE(url)
	elif 'catch.is'	 	in url2: titleLIST,linkLIST = CATCHIS(url)
	#elif 'estream'	 	in url2: titleLIST,linkLIST = ESTREAM(url)
	elif 'filerio'		in url2: titleLIST,linkLIST = FILERIO(url)
	elif 'gounlimited'	in url2: titleLIST,linkLIST = GOUNLIMITED(url)
	elif 'govid'		in url2: titleLIST,linkLIST = GOVID(url)
	elif 'intoupload' 	in url2: titleLIST,linkLIST = INTOUPLOAD(url)
	elif 'liivideo' 	in url2: titleLIST,linkLIST = LIIVIDEO(url)
	elif 'mp4upload'	in url2: titleLIST,linkLIST = MP4UPLOAD(url)
	elif 'publicvideohost' in url2: titleLIST,linkLIST = PUBLICVIDEOHOST(url)
	elif 'rapidvideo' 	in url2: titleLIST,linkLIST = RAPIDVIDEO(url)
	elif 'thevideo'		in url2: titleLIST,linkLIST = THEVIDEO(url)
	elif 'top4top'		in url2: titleLIST,linkLIST = TOP4TOP(url)
	elif 'upbom' 		in url2: titleLIST,linkLIST = UPBOM(url)
	elif 'uptobox' 		in url2: titleLIST,linkLIST = UPTO(url)
	elif 'uptostream'	in url2: titleLIST,linkLIST = UPTO(url)
	elif 'uqload' 		in url2: titleLIST,linkLIST = UQLOAD(url)
	elif 'vcstream' 	in url2: titleLIST,linkLIST = VCSTREAM(url)
	elif 'vev.io'	 	in url2: titleLIST,linkLIST = VEVIO(url)
	elif 'playr.4helal'	in url2: titleLIST,linkLIST = HELAL(url)
	elif 'vidbob'		in url2: titleLIST,linkLIST = VIDBOB(url)
	#elif 'vidbom'		in url2: titleLIST,linkLIST = VIDBOM(url)
	elif 'vidhd' 		in url2: titleLIST,linkLIST = VIDHD(url)
	elif 'vidoza' 		in url2: titleLIST,linkLIST = VIDOZA(url)
	elif 'vidshare' 	in url2: titleLIST,linkLIST = VIDSHARE(url)
	elif 'watchvideo' 	in url2: titleLIST,linkLIST = WATCHVIDEO(url)
	elif 'wintv.live'	in url2: titleLIST,linkLIST = WINTVLIVE(url)
	elif 'youtu'	 	in url2: titleLIST,linkLIST = YOUTUBE(url)
	elif 'zippyshare'	in url2: titleLIST,linkLIST = ZIPPYSHARE(url)
	else:
		resolvable = urlresolver_HostedMediaFile(url).valid_url()
		if resolvable:
			titleLIST,linkLIST = URLRESOLVER(url)
	return titleLIST,linkLIST

def SERVERS(linkLIST,script_name=''):
	serversLIST,urlLIST,unknownLIST,serversDICT = [],[],[],[]
	message = '\\n'
	linkLIST = list(set(linkLIST))
	#selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', NEWlinkLIST)
	#if selection == -1 : return ''
	for link in linkLIST:
		if link=='': continue
		link = link.rstrip('/')
		if '://moshahda.' in link:
			titleLIST,linkLIST = MOSHAHDA_ONLINE(link)
			for i in range(0,len(linkLIST)):
				serversDICT.append( [titleLIST[i],linkLIST[i]] )
		else:
			serverNAME = RESOLVABLE(link)
			#xbmcgui.Dialog().ok(link,serverNAME)
			if serverNAME=='':
				if '?' in link and ('akoam' in link or 'shahid4u' in link or 'e5tsar' in link):
					serverNAME = 'سيرفر عام مجهول ' + link.split('name=')[1].lower().split('__')[0]
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
		link = urlresolver_HostedMediaFile(url).resolve()
		return [link],[link]
	except: return [],[]

def MOSHAHDA_ONLINE(link):
	headers = { 'User-Agent' : '' }
	if 'op=download_orig' in link:
		html = openURL(link,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-1st')
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
		html = openURL(url,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-2nd')
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
		html = openURL(link2,data,'','','RESOLVERS-MOSHAHDA_ONLINE-3rd')
		html_blocks = re.findall('Download Video.*?get\(\'(.*?)\'.*?sources:(.*?)image:',html,re.DOTALL)
		if not html_blocks: return [],[]
		download = html_blocks[0][0]
		block = html_blocks[0][1]
		items = re.findall('file:"(.*?)"(,label:".*?"|)',block,re.DOTALL)
		titleLIST,linkLIST = [],[]
		for link,title in items:
			if '.m3u8' in link:
				html = openURL(link,'','','','RESOLVERS-MOSHAHDA_ONLINE-4th')
				items2 = re.findall('RESOLUTION=(.*?x).*?\n(.*?)\n',html,re.DOTALL)
				if items:
					for title,link in items2:
						title = ' سيرفر خاص ' + 'm3u8: ' + name2 + ' ' + title
						titleLIST.append(title)
						linkLIST.append(link)
				else:
					title = ' سيرفر خاص ' + 'm3u8: ' + name2
					titleLIST.append(title)
					linkLIST.append(link)
			else:
				title = title.replace(',label:"','')
				title = title.strip('"')
				title = ' سيرفر  خاص ' + ' mp4: ' + name2 + ' ' + title
				titleLIST.append(title)
				linkLIST.append(link)
		# download links
		link = 'http://moshahda.online' + download
		html = openURL(link,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-5th')
		items = re.findall("download_video\('(.*?)','(.*?)','(.*?)'.*?<td>(.*?)x",html,re.DOTALL)
		for id,mode,hash,title in items:
			title = ' سيرفر تحميل خاص ' + ' mp4: ' + name2 + title+'x'
			link = 'http://moshahda.online/dl?op=download_orig&id='+id+'&mode='+mode+'&hash='+hash
			titleLIST.append(title)
			linkLIST.append(link)
		return titleLIST,linkLIST

def E5TSAR(url):
	parts = url.split('?')
	url2 = parts[0]
	headers = { 'User-Agent' : '' }
	html = openURL(url2,'',headers,'','RESOLVERS-E5TSAR-1st')
	items = re.findall('Please wait.*?href=\'(.*?)\'',html,re.DOTALL)
	url = items[0]
	titleLIST,linkLIST = RESOLVE(url)
	#xbmcgui.Dialog().ok(items[0],html)
	return titleLIST,linkLIST

def SHAHID4U(link):
	parts = re.findall('postid=(.*?)&serverid=(.*?)&name=',link,re.DOTALL|re.IGNORECASE)
	#xbmcgui.Dialog().ok(link,str(parts))
	postid = parts[0][0]
	serverid = parts[0][1]
	url = 'https://on.shahid4u.net/ajaxCenter?_action=getserver&_post_id='+postid+'&serverid='+serverid
	headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
	html = openURL(url,'',headers,'','RESOLVERS-SHAHID4U-1st')
	url2 = html
	titleLIST,linkLIST = RESOLVE(url2)
	#try: url3 = url2[0]
	#except: url3 = ''
	#xbmcgui.Dialog().ok(str(url3),str(html))
	return titleLIST,linkLIST

def AKOAM(link):
	from requests import request as requests_request
	response = requests_request('GET', link, data='', headers='')
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
		titles,urls = CATCHIS(url)
	else:
		response = requests_request('GET', 'https://akoam.net/', headers='', data='', allow_redirects=False)
		relocateURL = response.headers['Location']
		url = url.replace('https://akoam.net/',relocateURL)
		headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' , 'Referer':url }
		response = requests_request('POST', url, headers=headers, data='', allow_redirects=False)
		html = response.text
		items = re.findall('direct_link":"(.*?)"',html,re.DOTALL|re.IGNORECASE)
		if not items:
			items = re.findall('<iframe.*?src="(.*?)"',html,re.DOTALL|re.IGNORECASE)
			if not items:
				items = re.findall('<embed.*?src="(.*?)"',html,re.DOTALL|re.IGNORECASE)
		url2 = items[0].replace('\/','/')
		url2 = url2.rstrip('/')
		if 'http' not in url2: url2 = 'http:' + url2
		if '?name=' in link:
			titles,urls = RESOLVE(url2)
		else: 
			titles,urls = ['ملف التحميل'],[url2]
			"""
			splits = url.split('/')
			server = '/'.join(splits[0:3])
			hash_data = url.split('/')[4]
			watch_title = url.split('/')[-1]
			url3 = server + '/watching/'+hash_data+'/'+watch_title
			response = requests_request('GET', url3, headers='', data='', allow_redirects=False)
			html = response.text
			url3 = re.findall('file: "(.*?)"',html,re.DOTALL|re.IGNORECASE)[0]
			titles2,urls2 = ['ملف المشاهدة المباشرة'],[url3]
			titles,urls = titles+titles2,urls+urls2
			"""
	if urls: return titles,urls
	else: return [],[]

def RAPIDVIDEO(url):
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','RESOLVERS-RAPIDVIDEO-1st')
	#xbmcgui.Dialog().ok(url,html)
	items = re.findall('poster=.*?src="(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VIDSHARE(url):
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','RESOLVERS-VIDSHARE-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def UQLOAD(url):
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','RESOLVERS-UQLOAD-1st')
	items = re.findall('sources: \["(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,items[0])
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VCSTREAM(url):
	id = url.split('/')[-2]
	url = 'https://vcstream.to/player?fid=' + id
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','RESOLVERS-VCSTREAM-1st')
	html = html.replace('\\','')
	items = re.findall('file":"(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0],items[0])
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VIDOZA(url):
	url = url.replace('embed-','')
	html = openURL(url,'','','','RESOLVERS-VIDOZA-1st')
	items = re.findall('source src="(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(str(items),html)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def WATCHVIDEO(url):
	url = url.replace('embed-','')
	html = openURL(url,'','','','RESOLVERS-WATCHVIDEO-1st')
	items = re.findall("Download start.*?download_video\('(.*?)','(.*?)','(.*?)'",html,re.DOTALL)
	for id,mode,hash in items:
		url = 'https://watchvideo.us/dl?op=download_orig&id='+id+'&mode='+mode+'&hash='+hash
		html = openURL(url,'','','','RESOLVERS-WATCHVIDEO-2nd')
	items = re.findall('direct link.*?href="(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def UPBOM(url):
	id = url.split('/')[-2]
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'id' : id , 'op' : 'download2' }
	data = urllib.urlencode(payload)
	html = openURL(url,data,headers,'','RESOLVERS-UPBOM-1st')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	items = re.findall('direct_link.*?href="(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def LIIVIDEO(url):
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','RESOLVERS-LIIVIDEO-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VIDHD(url):
	html = openURL(url,'','','','RESOLVERS-LIIVIDEO-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def INTOUPLOAD(url):
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','RESOLVERS-INTOUPLOAD-1st')
	html_blocks = re.findall('POST.*?(.*?)clearfix',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('op" value="(.*?)".*?id" value="(.*?)".*?rand" value="(.*?)".*?left:(.*?)px;.*?&#(.*?);.*?left:(.*?)px;.*?&#(.*?);.*?left:(.*?)px;.*?&#(.*?);.*?left:(.*?)px;.*?&#(.*?);',block,re.DOTALL)
	for op,id,rand,pos1,num1,pos2,num2,pos3,num3,pos4,num4 in items:
		a=1
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
	html = openURL(url,data,headers,'','RESOLVERS-INTOUPLOAD-2nd')
	items = re.findall('target_type.*?href="(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def ESTREAM(url):
	#url = url.replace('embed-','')
	html = openURL(url,'','','','RESOLVERS-ESTREAM-1st')
	items = re.findall('video preload.*?src=.*?src="(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0],items[0])
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VEVIO(url):
	id = url.split('/')[-1]
	url = 'https://vev.io/api/serve/video/' + id
	headers = { 'User-Agent' : '' }
	data = '{}'
	html = openURL(url,data,headers,'','RESOLVERS-VEVIO-1st')
	items = re.findall('":"(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,str(items))
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def YOUTUBE(url):
	id = url.split('/')[-1]
	youtubeID = id.split('?')[0]
	url = 'plugin://plugin.video.youtube/play/?video_id='+youtubeID
	return [url],[url]

def CATCHIS(url):
	id = url.split('/')[-1]
	payload = { 'op' : 'download2' , 'id' : id }
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	data = urllib.urlencode(payload)
	html = openURL(url,data,headers,'','RESOLVERS-CATCH-1st')
	items = re.findall('direct_link.*?href="(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VIDBOM_PROBLEM(url):
	html = openURL(url,'','','','RESOLVERS-VIDBOM-1st')
	xbmc.sleep(1500)
	items = re.findall('file: "(.*?)"',html,re.DOTALL)
	slidesURL = items[0].rstrip('/')
	html2 = openURL(slidesURL,'','','','RESOLVERS-VIDBOM-2nd')
	xbmc.sleep(1500)
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def HELAL(url):
	headers = { 'User-Agent' : '' }
	#url = url.replace('http:','https:')
	html = openURL(url,'',headers,'','RESOLVERS-VIDBOB-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0].rstrip('/'),'')
	if items:
		url = items[0].replace('https:','http:')
		return [url],[url]
	else: return [],[]

def VIDBOB(url):
	headers = { 'User-Agent' : '' }
	#url = url.replace('http:','https:')
	html = openURL(url,'',headers,'','RESOLVERS-VIDBOB-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0].rstrip('/'),'')
	if items:
		url = items[0].replace('https:','http:')
		return [url],[url]
	else: return [],[]

def ARABLOADS(url):
	html = openURL(url,'','','','RESOLVERS-ARABLOADS-1st')
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
	html = openURL(url,'','','','RESOLVERS-ZIPPYSHARE-1st')
	items = re.findall('dlbutton\'\).href = "(.*?)" \+ \((.*?) \% (.*?) \+ (.*?) \% (.*?)\) \+ "(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,str(var))
	if items:
		var1,var2,var3,var4,var5,var6 = items[0]
		var = int(var2) % int(var3) + int(var4) % int(var5)
		url = basename + var1 + str(var) + var6
		return [url],[url]
	else: return [],[]

def GOUNLIMITED_PROBLEM(url):
	url = url.replace('embed-','')
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	items = re.findall('data(.*?)hide.*?embed(.*?)hash',html,re.DOTALL)
	id = items[0][0].replace('|','')
	hash = items[0][1].split('|')
	newhash = ''
	for i in reversed(hash):
		newhash += i + '-'
	newhash = newhash.strip('-')
	#url = 'https://gounlimited.to/dl?op=view&file_code='+id+'&hash='+newhash+'&embed=&adb=1'
	#html = openURL(url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	from requests import request as requests_request
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
	html = requests_request('GET', url, headers=headers, params=querystring)
	items = re.findall('video="" src="(.*?)"',html.text,re.DOTALL)
	#xbmcgui.Dialog().ok(str(html.content),str(len(html.content)))
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def GOUNLIMITED(url):
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	items = re.findall('preload\|mp4\|(.*?)\|sources\|Player',html,re.DOTALL)
	if items:
		url = 'https://shuwaikh.gounlimited.to/'+items[0]+'/v.mp4'
		return [url],[url]
	else: return [],[]

def UPTO(url):
	#xbmcgui.Dialog().ok(url,'')
	titleLIST = ['uptostream','uptobox (delay 30sec)','both']
	selection = xbmcgui.Dialog().select('اختر السيرفر:', titleLIST)
	if selection == -1 : return ''
	elif selection==0:
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
	html = openURL(url,'',headers,'','RESOLVERS-UPTOSTREAM-1st')
	items = re.findall('src":"(.*?)".*?label":"(.*?)"',html,re.DOTALL)
	if items:
		titleLIST,linkLIST = [],[]
		for link,title in items:
			link = link.replace('\/','/')
			titleLIST.append(title)
			linkLIST.append(link)
		return titleLIST,linkLIST
	else: return [],[]

def UPTOBOX(url):
	#xbmcgui.Dialog().ok(url,'')
	headers = { 'User-Agent' : '' }
	html = openURL(url,'',headers,'','RESOLVERS-UPTOBOX-1st')
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
			progress.update(i*100/35,str(35-i))
			xbmc.sleep(1000)
			if progress.iscanceled(): return
		progress.close()
		html = openURL(url,data,headers,'','RESOLVERS-UPTOBOX-2nd')
	items = re.findall('class=\'file-title\'>(.*?)<.*?comparison-table.*?href="(.*?)"',html,re.DOTALL)
	if items:
		title = items[0][0]
		url = items[0][1]
		return [title],[url]
	else: return [],[]
	#xbmcgui.Dialog().ok(str(html),html)
	#file = open('S:\emad3.html', 'w')
	#file.write(token)
	#file.write('\n\n\n')
	#file.write(html)
	#file.close()

def THEVIDEO(url):
	url = url.replace('embed-','')
	html = openURL(url,'','','','RESOLVERS-THEVIDEO-1st')
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
	from requests import request as requests_request
	request = requests_request('POST', url, headers=headers, data=payload, allow_redirects=False)
	url = request.headers['Location']
	if url!='':
		return [url],[url]
	else: return [],[]

def WINTVLIVE(url):
	html = openURL(url,'','','','RESOLVERS-WINTVLIVE-1st')
	items = re.findall('mp4: \[\'(.*?)\'',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def	FILERIO(url):
	#xbmc.log(url, level=xbmc.LOGNOTICE)
	id = url.split('/')[-1]
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'id':id , 'op':'download2' }
	data = urllib.urlencode(payload)
	html = openURL(url,data,headers,'','RESOLVERS-FILERIO-2nd')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	items = re.findall('direct_link.*?href="(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def GOVID(url):
	html = openURL(url,'','','','RESOLVERS-GOVID-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]

def VIMPLE_PROBLEM(link):
	id = link.split('id=')[1]
	headers = { 'User-Agent' : '' }
	url = 'http://player.vimple.ru/iframe/' + id
	html = openURL(url,'',headers,'','RESOLVERS-VIMPLE-1st')
	items = re.findall('true,"url":"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0].replace('\/','/')
		return [url],[url]
	else: return [],[]

def ARCHIVE(url):
	html = openURL(url,'','','','RESOLVERS-ARCHIVE-1st')
	items = re.findall('source src="(.*?)"',html,re.DOTALL)
	#logging.warning('https://archive.org' + items[0])
	if items:
		url = url = 'https://archive.org' + items[0]
		return [url],[url]
	else: return [],[]

def PUBLICVIDEOHOST(url):
	html = openURL(url,'','','','RESOLVERS-PUBLICVIDEOHOST-1st')
	items = re.findall('file: "(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(str(items),html)
	if items:
		url = items[0]
		return [url],[url]
	else: return [],[]



