





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
	#XBMCGUI_DIALOG_OK(str(items),html)
	if items:
		link = items[0].rstrip('/')
		title,url = VEVIO(link)
		return title,url
	else: return ['Error: ESTREAM Resolver failed'],[]

def HELAL_PROBLEM(url):
	# https://playr.4helal.tv/4qlqt9d3813e
	headers = { 'User-Agent' : '' }
	#url = url.replace('http:','https:')
	html = openURL_cached(NO_CACHE,url,'',headers,'','RESOLVERS-VIDBOB-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	#XBMCGUI_DIALOG_OK(items[0].rstrip('/'),'')
	if items:
		url = items[0].replace('https:','http:')
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

def VIMPLE_PROBLEM(link):
	id = link.split('id=')[1]
	headers = { 'User-Agent' : '' }
	url = 'http://player.vimple.ru/iframe/' + id
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VIMPLE-1st')
	items = re.findall('true,"url":"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0].replace('\/','/')
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

def VIDSHARE_PROBLEM(url):
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VIDSHARE-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

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
	#XBMCGUI_DIALOG_OK(code,str(captcha))
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'id':id , 'op':op , 'code':code , 'rand':rand }
	data = urllib.urlencode(payload)
	progress = XBMCGUI_DIALOGPROGRESS()
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
	else: return ['Error: ESTREAM Resolver failed'],[]

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
	else: return ['Error: ESTREAM Resolver failed'],[]

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
	response = requests.request('GET', url, headers=headers, params=querystring)
	items = re.findall('video="" src="(.*?)"',response.content,re.DOTALL)
	#XBMCGUI_DIALOG_OK(str(response.content),str(len(response.content)))
	if items:
		url = items[0]
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

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
	else: return ['Error: ESTREAM Resolver failed'],[]
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





