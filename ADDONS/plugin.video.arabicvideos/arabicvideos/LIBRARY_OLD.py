


def openURL_OLD(url,data='',headers='',showDialogs=True,source=''):
	#url = url + '||MyProxyUrl=http://188.166.59.17:8118'
	proxies,timeout = {},40
	url2,proxyurl,dnsurl,sslurl = EXTRACT_URL(url)
	#DIALOG_OK(url2,'')
	#url2 = quote(url2)
	html,code,reason,finalURL = None,None,None,url2
	if dnsurl!=None:
		import socket
		original_create_connection = socket.create_connection
		def patched_create_connection(address,*args,**kwargs):
			host,port = address
			ip = DNS_RESOLVER(host,dnsurl)
			if ip: host = ip[0]
			address = (host,port)
			return original_create_connection(address,*args,**kwargs)
		socket.create_connection = patched_create_connection
	if proxyurl!=None:
		if headers=='': headers = { 'User-Agent' : '' }
		elif 'User-Agent' not in headers: headers['User-Agent'] = ''
		if proxyurl=='': proxyname,proxyurl = RANDOM_HTTPS_PROXY()
		proxies = {"http":proxyurl,"https":proxyurl}
		MyProxyHandler = urllib2.ProxyHandler(proxies)
		opener = urllib2.build_opener(MyProxyHandler)
		urllib2.install_opener(opener)
	"""
	if   proxyurl==None and dnsurl==None: opener = urllib2.build_opener()
	elif proxyurl!=None and dnsurl==None: opener = urllib2.build_opener(MyProxyHandler)
	elif proxyurl==None and dnsurl!=None: opener = urllib2.build_opener(MyHTTPSHandler,MyHTTPHandler)
	elif proxyurl!=None and dnsurl!=None: opener = urllib2.build_opener(MyProxyHandler,MyHTTPSHandler,MyHTTPHandler)
	#old_opener = urllib2._opener
	urllib2.install_opener(opener)
	"""
	if   headers=='': headers = {}
	if   data=='': request = urllib2.Request(url2,headers=headers)
	elif data!='': request = urllib2.Request(url2,headers=headers,data=data)
	"""
	if   data=='' and headers=='': request = urllib2.Request(url2)
	elif data=='' and headers!='': request = urllib2.Request(url2,headers=headers)
	elif data!='' and headers=='': request = urllib2.Request(url2,data=data)
	elif data!='' and headers!='': request = urllib2.Request(url2,headers=headers,data=data)
	"""
	try:
		if proxyurl!=None or dnsurl!=None or sslurl!=None:
			# if testing proxies then timeout=10
			if url2=='https://www.google.com': timeout = 10
			response = urllib2.urlopen(request,timeout=timeout)
		else:
			#ctx = ssl.create_default_context()
			#ctx.check_hostname = False
			#ctx.verify_mode = ssl.CERT_NONE
			#ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
			ctx = ssl._create_unverified_context()
			response = urllib2.urlopen(request,timeout=timeout,context=ctx)
		#urllib2.install_opener(old_opener)
		code = response.code
		reason = response.msg
		html = response.read()
		#final_url = response.url
		response.close
		# error code
		#		code = response.code
		#		code = response.getcode()
		# final url after all redirects
		#		finalURL = response.geturl()
		#		finalURL = response.url
		# headers & cookies
		#		headers = response.headers
		#		headers = response.info()
	except Exception as e:
		#xbmc.log(str(dir(e)), level=xbmc.LOGNOTICE)
		#xbmc.log(str(url), level=xbmc.LOGNOTICE)
		#xbmc.log(str(data), level=xbmc.LOGNOTICE)
		#xbmc.log(str(headers), level=xbmc.LOGNOTICE)
		#DIALOG_OK(url,'')
		#final_url = response.url
		if 'google-analytics' not in url2:
			traceback.print_exc(file=sys.stderr)
		if 'timeout' in str(type(e)).lower():
			code = -1
			reason = e.message
		elif 'httperror' in str(type(e)).lower():
			code = e.code
			reason = e.reason
		# 'socket' errors must come before 'urlerror' errors
		elif hasattr(e,'reason') and 'socket' in str(type(e.reason)).lower():
			code = e.reason.errno
			reason = e.reason.strerror
		elif 'urlerror' in str(type(e)).lower():
			code = e.errno
			reason = e.reason
		if code==None:
			code = -1
		if reason==None:
			reason = 'Unknown error ( Raised by: '
			try: reason += e.__class__.__module__
			except: reason += 'UnknownModule'
			try: reason += '.'+e.__class__.__name__
			except: reason += '.UnknownClass'
			reason += ' )'
		if html==None:
			if hasattr(e,'read'): html = e.read()
			else: html = '___Error___:'+str(code)+':'+str(reason)
	htmlLower = html.lower()
	condition1 = (code!=200 and int(code/100)*100!=300)
	condition2 = ('cloudflare' in htmlLower and 'ray id: ' in htmlLower)
	condition3 = ('___Error___' in htmlLower)
	condition4 = ('5 sec' in htmlLower)
	if condition1 or condition2 or condition3 or condition4:
		if condition2:
			reason2 = 'Blocked by Cloudflare'
			if 'recaptcha' in htmlLower: reason2 += ' Using Google reCAPTCHA'
			reason = reason2+' ( '+reason+' )'
		elif condition4:
			reason4 = 'Blocked by 5 seconds browser check'
			reason = reason4+' ( '+reason+' )'
		html = '___Error___:'+str(code)+':'+reason
		message,send,showDialogs = '','no',False
		"""
		if 'google-analytics' in url2: send = showDialogs
		if showDialogs=='yes':
			DIALOG_OK('خطأ في الاتصال',html)
			if code==502 or code==7:
				DIALOG_OK('Website is not available','لا يمكن الوصول الى الموقع والسبب قد يكون من جهازك او من الانترنيت الخاصة بك او من الموقع كونه مغلق للصيانة او التحديث لذا يرجى المحاولة لاحقا')
				send = 'no'
			elif code==404:
				DIALOG_OK('File not found','الملف غير موجود والسبب غالبا هو من المصدر ومن الموقع الاصلي الذي يغذي هذا البرنامج')
			if send=='yes':
				yes = DIALOG_YESNO('سؤال','هل تربد اضافة رسالة مع الخطأ لكي تشرح فيها كيف واين حصل الخطأ وترسل التفاصيل الى المبرمج ؟','','','كلا','نعم')
				if yes: message = ' \\n\\n' + KEYBOARD('Write a message   اكتب رسالة')
		if send=='yes': SEND_EMAIL('Error: From Arabic Videos',html+message,showDialogs,url,source)
		"""
		#if 'google-analytics' not in url:
		#if code==502:
		#	LOG_THIS('ERROR',LOGGING(script_name)+'   URL Quote Error   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]   Final URL: [ '+final_url+' ]')
		#	html = OPENURL(final_url,data,headers,showDialogs,source)
		#	return html
		if code in [7,11001,10054] and dnsurl==None:
			LOG_THIS('ERROR',LOGGING(script_name)+'   DNS Failed   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
			url = url+'||MyDNSUrl='
			html = OPENURL(url,data,headers,showDialogs,source)
			return html
		if code==8 and sslurl==None:
			LOG_THIS('ERROR',LOGGING(script_name)+'   SSL Failed   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
			url = url+'||MySSLUrl='
			html = OPENURL(url,data,headers,showDialogs,source)
			return html
		else:
			LOG_THIS('ERROR',LOGGING(script_name)+'   Failed Opening URL   Code: [ '+str(code)+' ]   Reason :[ '+reason+' ]   Source: [ '+source+' ]'+'   URL: [ '+url+' ]')
		EXIT_IF_SOURCE(source,code,reason)
	#DIALOG_OK('',html)
	return html

def openURL_WEBPROXIES(url,data='',headers='',showDialogs=True,source=''):
	html = openURL_WEBPROXYTO(url,data,headers,showDialogs,'LIBRARY-openURL_WEBPROXIES-1st')
	if '___Error___' in html:
		html = openURL_KPROXYCOM(url,data,headers,showDialogs,'LIBRARY-openURL_WEBPROXIES-2nd')
		if '___Error___' in html:
			reason = 'Web Proxy failed'
			code = -1
			LOG_THIS('ERROR',LOGGING(script_name)+'   Failed opening url   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]'+'   URL: [ '+url+' ]')
			EXIT_IF_SOURCE(source,code,reason)
	return html

def openURL_PROXY(url,data='',headers='',showDialogs=True,source=''):
	#html = '___Error___'
	if source=='SERVICES-TEST_ALL_WEBSITES-2nd': html = '___Error___'
	else: html = OPENURL_CACHED(NO_CACHE,url,data,headers,showDialogs,'LIBRARY-openURL_PROXY-1st')
	if '___Error___' in html:
		html = openURL_HTTPSPROXIES(url,data,headers,showDialogs,'LIBRARY-openURL_PROXY-2nd')
		if '___Error___' in html:
			html = openURL_WEBPROXIES(url,data,headers,showDialogs,'LIBRARY-openURL_PROXY-3rd')
			if '___Error___' in html:
				reason = 'Proxy failed'
				code = -1
				LOG_THIS('ERROR',LOGGING(script_name)+'   Failed opening url   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]'+'   URL: [ '+url+' ]')
				EXIT_IF_SOURCE(source,code,reason)
	return html

def openURL_HTTPSPROXIES(url,data='',headers='',showDialogs=True,source=''):
	url2,proxyurl,dnsurl,sslurl = EXTRACT_URL(url)
	if proxyurl==None: url = url+'||MyProxyUrl='
	html = OPENURL_CACHED(NO_CACHE,url,data,headers,showDialogs,'LIBRARY-openURL_HTTPSPROXIES-1st')
	if '___Error___' in html: code = int(html.split(':')[1])
	else: code = 200
	if code!=200 and int(code/100)*100!=300:
		source = 'LIBRARY-openURL_WEBPROXYTO-2nd'
		reason = 'HTTPS proxy failed'
		code = -1
		LOG_THIS('ERROR',LOGGING(script_name)+'   Failed opening url   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
		html = '___Error___:'+str(code)+':'+reason
	return html

def openURL_WEBPROXYTO(url,data='',headers='',showDialogs=True,source=''):
	# Proxy + DNS
	# http://webproxy.to		http://69.64.52.22
	# cookie will expire after 30 miuntes (only if not used within these 30 minutes)
	response = OPENURL_REQUESTS_CACHED(VERY_SHORT_CACHE,'GET', 'http://webproxy.to','','',False,False,'LIBRARY-openURL_WEBPROXYTO-1st')
	html2 = response.content
	cookies = response.cookies.get_dict()
	s = cookies['s']
	cookies2 = 's=' + s
	headers2 = { 'Cookie' : cookies2 }
	if headers=='': headers3 = {}
	else: headers3 = headers
	if 'Cookie' in headers3: headers3['Cookie'] += ';' + cookies2
	else: headers3['Cookie'] = cookies2
	html = OPENURL_CACHED(NO_CACHE,'http://webproxy.to/browse.php?u='+quote(url)+'&b=128',data,headers3,showDialogs,'LIBRARY-openURL_WEBPROXYTO-2nd')
	html = unquote(html).replace('/browse.php?u='+url,'').replace('/browse.php?u=','').replace('&amp;b=128','')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	if '<!-- CONTENT START -->'.lower() in html.lower() or '___Error___' in html:
		source = 'LIBRARY-openURL_WEBPROXYTO-4th'
		reason = 'WEBPROXYTO proxy failed'
		code = -1
		LOG_THIS('ERROR',LOGGING(script_name)+'   Failed opening url   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]   URL: [ '+url+' ]')
		html = '___Error___:'+str(code)+':'+reason
	return html

def openURL_KPROXYCOM(url,data='',headers='',showDialogs=True,source=''):
	# Proxy + DNS
	# http://kproxy.com			http://37.187.147.158
	# cookie does not expire (tested for 3 days)
	# servers will expire after 20 miuntes (even if used within these 20 minutes)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET', 'http://kproxy.com','','',False,False,'LIBRARY-openURL_KPROXYCOM-1st')
	html2 = response.content
	cookies = response.cookies.get_dict()
	KP_DAT2 = cookies['KP_DAT2__']
	cookies2 = 'KP_DAT2__=' + KP_DAT2
	headers2 = { 'Cookie' : cookies2 }
	#payload = { 'page' : quote(url) }
	#data2 = urllib.urlencode(payload)
	html2 = OPENURL_CACHED(VERY_SHORT_CACHE,'http://kproxy.com/doproxy.jsp?page='+quote(url),'',headers2,False,'LIBRARY-openURL_KPROXYCOM-2nd')
	proxyURL = re.findall('url=(.*?)"',html2,re.DOTALL)
	if proxyURL:
		proxyURL = proxyURL[0]
		if headers=='': headers3 = {}
		else: headers3 = headers
		if 'Cookie' in headers3: headers3['Cookie'] += ';' + cookies2
		else: headers3['Cookie'] = cookies2
		html = OPENURL_CACHED(NO_CACHE,proxyURL,data,headers3,showDialogs,'LIBRARY-openURL_KPROXYCOM-3rd')
	else:	#if not proxyURL:# or 'kproxy.com'.lower() not in html.lower():
		source = 'LIBRARY-openURL_KPROXYCOM-4th'
		reason = 'KPROXYCOM proxy failed'
		code = -1
		LOG_THIS('ERROR',LOGGING(script_name)+'   Failed opening url   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   Source: [ '+source+' ]'+'   URL: [ '+url+' ]')
		html = '___Error___:'+str(code)+':'+reason
	return html

def OPENURL_REQUESTS_CACHED_OLD(cacheperiod,method,url,data='',headers='',allow_redirects=True,showDialogs=True,source=''):
	if cacheperiod==0: return OPENURL_REQUESTS(method,url,data,headers,allow_redirects,showDialogs,source)
	url2,proxyurl,dnsurl,sslurl = EXTRACT_URL(url)
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	t = (url2,str(data),str(headers),str(allow_redirects),source)
	c.execute('SELECT response FROM responsecache WHERE url=? AND data=? AND headers=? AND allow_redirects=? AND source=?', t)
	rows = c.fetchall()
	conn.close()
	if rows:
		#message = 'found in cache'
		compressed = rows[0][0]
		text = zlib.decompress(compressed)
		response = cPickle.loads(text)
	else:
		#message = 'not found in cache'
		response = OPENURL_REQUESTS(method,url2,data,headers,allow_redirects,showDialogs,source)
		html = response.content
		if '___Error___' not in html:
			conn = sqlite3.connect(dbfile)
			c = conn.cursor()
			conn.text_factory = str
			text = cPickle.dumps(response)
			compressed = zlib.compress(text)
			t = (now+cacheperiod,url2,str(data),str(headers),str(allow_redirects),source,sqlite3.Binary(compressed))
			c.execute("INSERT INTO responsecache VALUES (?,?,?,?,?,?,?)",t)
			conn.commit()
			conn.close()
	#DIALOG_NOTIFICATION(message,'')
	return response

def OPENURL_CACHED_OLD(cacheperiod,url,data='',headers='',showDialogs=True,source=''):
	#url = url+'||MyProxyUrl=http://41.33.212.68:4145'
	#cacheperiod = 0
	#t1 = time.time()
	#DIALOG_OK(unquote(url),source+'     cache(hours)='+str(cacheperiod/60/60))
	#nowTEXT = time.ctime(now)
	#xbmc.log(LOGGING(script_name)+'   opening url   Source:['+source+']   URL: [ '+url+' ]', level=xbmc.LOGNOTICE)
	#xbmc.log('WWWW: 1111:', level=xbmc.LOGNOTICE)
	if cacheperiod==0: return OPENURL(url,data,headers,showDialogs,source)
	#xbmc.log('WWWW: 2222:', level=xbmc.LOGNOTICE)
	url2,proxyurl,dnsurl,sslurl = EXTRACT_URL(url)
	#xbmc.log('WWWW: 3333:', level=xbmc.LOGNOTICE)
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	#conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
	t = (url2,str(data),str(headers),source)
	c.execute('SELECT html FROM htmlcache WHERE url=? AND data=? AND headers=? AND source=?', t)
	rows = c.fetchall()
	#html = repr(rows[0][0])
	conn.close()
	#xbmc.log('WWWW: 4444:', level=xbmc.LOGNOTICE)
	if rows:
		#message = 'found in cache'
		html = rows[0][0]
		#html = base64.b64decode(html)
		#xbmc.log('WWWW: 9999:', level=xbmc.LOGNOTICE)
		html = zlib.decompress(html)
		#xbmc.log('WWWW: 5555:', level=xbmc.LOGNOTICE)
	else:
		#message = 'not found in cache'
		#xbmc.log('WWWW: AAAA:', level=xbmc.LOGNOTICE)
		html = OPENURL(url2,data,headers,showDialogs,source)
		#xbmc.log('WWWW: 6666:', level=xbmc.LOGNOTICE)
		if '___Error___' not in html:
			#xbmc.log('WWWW: BBBB:', level=xbmc.LOGNOTICE)
			conn = sqlite3.connect(dbfile)
			c = conn.cursor()
			conn.text_factory = str
			#html2 = base64.b64encode(html)
			#xbmc.log('WWWW: CCCC:', level=xbmc.LOGNOTICE)
			compressed = zlib.compress(html)
			t = (now+cacheperiod,url2,str(data),str(headers),source,sqlite3.Binary(compressed))
			c.execute("INSERT INTO htmlcache VALUES (?,?,?,?,?,?)",t)
			#xbmc.log('WWWW: DDDD:', level=xbmc.LOGNOTICE)
			conn.commit()
			conn.close()
		#xbmc.log('WWWW: 7777:', level=xbmc.LOGNOTICE)
	#t2 = time.time()
	#DIALOG_NOTIFICATION(message,str(int(t2-t1))+' ms')
	#xbmc.log('WWWW: 8888:', level=xbmc.LOGNOTICE)
	return html


def TEST_HTTPS_PROXIES():
	headers = { 'User-Agent' : '' }
	testedLIST,timingLIST = [],[]
	threads = CustomThread(True)
	for id in PROXIES:
		proxyname,proxyurl = PROXIES[id]
		url = 'https://www.google.com||MyProxyUrl='+proxyurl
		threads.start_new_thread('proxy_'+str(id),OPENURL_CACHED,NO_CACHE,url,'',headers,'','LIBRARY-CHECK_HTTPS_PROXIES-1st')
	threads.wait_finishing_all_threads()
	resultsDICT,finishedLIST =	threads.resultsDICT,threads.finishedLIST
	elpasedtimeDICT = threads.elpasedtimeDICT
	for id in finishedLIST:
		html = resultsDICT[id]
		if '___Error___' not in html:
			timingLIST.append(elpasedtimeDICT[id])
			id = int(id.replace('proxy_',''))
			testedLIST.append(id)
	for id in PROXIES:
		html = resultsDICT['proxy_'+str(id)]
		if '___Error___' in html:
			name,url = PROXIES[id]
			if html.count(':')>=2:
				dummy,code,reason = html.split(':')
			LOG_THIS('ERROR',LOGGING(script_name)+'   Failed testing proxy   Name: [ '+name+' ]   id: [ '+str(id)+' ]   Code: [ '+str(code)+' ]   Reason: [ '+reason+' ]   URL: [ '+url+' ]')
	if testedLIST:
		z = zip(testedLIST,timingLIST)
		z = sorted(z, reverse=False, key=lambda key: key[1])
		testedLIST,timingLIST = zip(*z)
	return testedLIST,timingLIST

def RANDOM_HTTPS_PROXY(number=None):
	if number==None: number = random.randrange(0,len(PROXIES)) # (0,6) means 6 servers
	proxyname,proxyurl = PROXIES[number] # 6 means 7th server
	return proxyname,proxyurl

# Proxies were taken from http://free-proxy.cz
PROXIES = {
		 0:('فرنسا 1'			,'http://51.79.26.40:80')		# HTTPS France	4564kB/s 100% 4ms
		,1:('فرنسا 2'			,'http://51.79.26.40:8080')		# HTTPS France	5291kB/s 100% 9ms
		,2:('كندا كيبيك'		,'http://198.50.147.158:3128')	# HTTPS Canada	3725kB/s 100% 13ms
		,3:('اليونان 2'			,'http://178.128.229.122:80')	# HTTPS Greece	3078kB/s 100% 37ms
		,4:('اميركا نيوجيرسي'	,'http://198.211.102.155:8080')	# HTTPS USA		4675kB/s 100% 46ms
		,5:('اميركا ماسشيوستس'	,'http://140.82.63.13:8080')	# HTTPS USA		5879kB/s 100% 57ms
		,6:('اميركا نيويورك'	,'http://159.203.87.130:3128')	# HTTPS USA		6057kB/s 100% 118ms
		,7:('اميركا مشيغان'		,'http://155.138.141.68:8080')	# HTTPS USA		4445kB/s 100% 132ms
		,8:('كندا اونتاريو'		,'http://149.248.59.104:8080')	# HTTPS Canada	3447kB/s 100% 175ms
		,9:('اميركا كاليفورنيا'	,'http://159.203.204.101:8888')	# HTTPS USA		1514kB/s 100% 352ms
		,10:('المانيا'			,'http://5.9.142.124:3128')		# HTTPS Germany	1121kB/s 100% 385ms
		,11:('اوربا'			,'http://35.204.241.76:3128')	# HTTPS Europe	1271kB/s 100% 484ms
		,12:('بريطانيا'			,'http://45.77.90.217:8080')	# HTTPS UK		1183kB/s 100% 501ms
		,13:('روسيا'			,'http://195.182.135.237:3128')	# HTTPS Russia	819kB/s  100% 653ms
		,14:('اليونان 1'		,'http://178.128.229.122:8080')	# HTTPS Greece	4383kB/s 100% 657ms
		,15:('اليابان'			,'http://45.32.33.87:3128')		# HTTPS Japan	664kB/s 100% 963ms
		,16:('تشيلي'			,'http://186.103.175.158:3128')	# HTTPS Chile	595kB/s 100% 700ms
		,17:('فرنسا 3'			,'http://51.77.215.51:3128')	# HTTPS France	902kB/s 100% 775ms
		,18:('الأرجنتين'			,'http://190.217.81.6:8080')	# HTTPS Argentina 812kB/s 100% 634ms
		,19:('هونج كونج'		,'http://47.52.29.184:3128')	# HTTPS Hong Kong 476kB/s 100% 1143ms
		,20:('اميركا كولورادو'	,'http://167.86.89.108:3128')	# HTTPS Colorado  938kB/s 100% 659ms
		,21:('الصين'			,'http://49.51.155.45:8081')	# HTTPS China			  92.2% 473ms
		,22:('مصر'				,'http://41.33.212.68:4145')	# HTTPS
		#,23:('تركيا'			,'http://45.230.215.46:8080')	# HTTPS China	368kB/s 100% 1300ms
		}


# open file using one line example
"""
with open('S:\\emad3.html', 'w') as f: f.write(emad)
with open('S:\\test2.m3u8', 'r') as f: emad = f.read()
"""


# open file using manu line example
"""
#file = open('/data/emad.html', 'w')
#file.write(html)
#file.close()
"""


# encode & decode examples
"""
decode('utf8')
decode('unicode_escape')
decode('ascii')
decode('windows-1256')
"""


# timing using time.time()
"""
t1 = time.time()
t2 = time.time()
DIALOG_OK(str(t2-t1), '')
"""


# timing using timeit.timeit()
"""
timeit.timeit('import LIBRARY',number=1)
"""


# logfile open, read, and close
"""
playing = str(myplayer.isPlaying())
logfile = file(logfilename, 'rb')
logfile.seek(-4000, os.SEEK_END)
logfile = logfile.read()
logfile2 = logfile.split(LOGGING(script_name)+'   Started playing video:')
if len(logfile2)==1: continue
else: logfile2 = logfile2[-1]
if 'CloseFile' in logfile2 or 'Attempt to use invalid handle' in logfile2:
	result = 'failed'
	xbmc.log(LOGGING(script_name)+'      Failure: Video failed playing  '+urlmessage, level=xbmc.LOGNOTICE)
	#break
elif 'Opening stream' in logfile2:
	result = 'playing'
	xbmc.log(LOGGING(script_name)+'      Success: Video is playing successfully  '+urlmessage, level=xbmc.LOGNOTICE)
	#break
"""


# to change the numbers name to digits
"""
lowLIST = [  ['']  ]
lowLIST.append(['الاولى','الأولى','الحادية','الحاديه','الواحدة','الواحده','الحادي','الواحد'])
lowLIST.append(['الثانية','الثانيه'])
lowLIST.append(['الثالثة','الثالثه'])
lowLIST.append(['الرابعة','الرابعه'])
lowLIST.append(['الخامسة','الخامسه'])
lowLIST.append(['السادسة','السادسه'])
lowLIST.append(['السابعة','السابعه'])
lowLIST.append(['الثامنة','الثامنه'])
lowLIST.append(['التاسعة','التاسعه'])
lowLIST.append(['العاشرة','العاشره'])
lowLIST.append(['العشرون','العشرين'])
lowLIST.append(['الثلاثون','الثلاثين'])
lowLIST.append(['الاربعون','الاربعين'])
lowLIST.append(['الخمسون','الخمسين'])
highLIST = [  ['']  ]
highLIST.append(['عشرة','عشر'])
highLIST.append(['و العشرون','و العشرين','والعشرون','والعشرين'])
highLIST.append(['و العشرون','و العشرين','والعشرون','والعشرين'])
highLIST.append(['و الثلاثون','و الثلاثين','والثلاثون','والثلاثين'])
highLIST.append(['و الاربعون','و الاربعين','والاربعون','والاربعين'])
cleanLIST = ['و الاخيرة','و الاخيره','والاخيرة','والاخيره','الاخيرة','الاخيره','كاملة','كامله']

def CLEAN_EPSIODE_NAME(title):
	#return title
	title2 = title.strip(' ').replace('  ',' ').replace('  ',' ')
	title2 = title2.replace('ـ','')
	episode = re.findall('(الحلقة|الحلقه) (\d+)',title2,re.DOTALL)
	if episode:
		for word in cleanLIST:
			title2 = title2.replace(word,'')
		number = int(episode[0][1])
		high,low = int(number/10),int(number%10)
		episode2 = []
		if low==0: high,low = 0,high+9
		for highTEXT in highLIST[high]:
			if highTEXT!='': highTEXT=' '+highTEXT
			for lowTEXT in lowLIST[low]:
				findTEXT = episode[0][0]+' '+episode[0][1]+' '+lowTEXT+highTEXT
				episode2 = re.findall(findTEXT,title2,re.DOTALL)
				if episode2: break
			if episode2: break
		if episode2: title2 = title2.replace(episode2[0],'')
		else: title2 = title2.replace(episode[0][0]+' '+episode[0][1],'')
		title2 = title2.strip(' ').replace('  ',' ').replace('  ',' ')
	#DIALOG_OK(title,title2)
	return title2
"""


# threading.Thread example
"""
items = re.findall('getVideoPlayer\(\'(.*?)\'',block,re.DOTALL)
for server in items:
	payload = { 'Ajax' : '1' , 'art' : artID , 'server' : server }
	data = urllib.urlencode(payload)
	#dataLIST.append(data)
	t = threading.Thread(target=linkFUNC,args=(data,linkLIST))
	t.start()
	threads.append(t)
for i in threads:
	i.join()
"""


# concurrent.futures threading example
"""
count = len(dataLIST)
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
	responcesDICT = dict( (executor.submit(openURL, url2, dataLIST[i], headers,'','HALACIMA-PLAY-3rd'), i) for i in range(count) )
for response in concurrent.futures.as_completed(responcesDICT):
	html = response.result()
	html = html.replace('SRC=','src=')
	links = re.findall('src=\'(.*?)\'',html,re.DOTALL)
	#if 'http' not in link: link = 'http:' + link
	linkLIST.append(links[0])
"""


"""
class MyHTTPConnection(httplib.HTTPConnection):
	def connect(self):
		ip = DNS_RESOLVER(self.host)
		if ip: self.host = ip[0]
		else: xbmc.log(LOGGING(script_name)+'      Error: MyHTTPConnection failed getting ip   URL:['+self.host+']', level=xbmc.LOGERROR)
		self.sock = socket.create_connection((self.host,self.port))

class MyHTTPSConnection(httplib.HTTPSConnection):
	def connect(self):
		ip = DNS_RESOLVER(self.host)
		if ip: self.host = ip[0]
		else: xbmc.log(LOGGING(script_name)+'      Error: MyHTTPSConnection failed getting ip   URL:['+self.host+']', level=xbmc.LOGERROR)
		self.sock = socket.create_connection((self.host,self.port), self.timeout)
		self.sock = ssl.wrap_socket(self.sock, self.key_file, self.cert_file)

class MyHTTPHandler(urllib2.HTTPHandler):
	def http_open(self,req):
		return self.do_open(MyHTTPConnection,req)

class MyHTTPSHandler(urllib2.HTTPSHandler):
	def https_open(self,req):
		return self.do_open(MyHTTPSConnection,req)
"""


#url = 'http://example.com/name.mp4'
#OPENURL_REQUESTS('GET',url)
#import RESOLVERS ; RESOLVERS.URLRESOLVER(url)
#PLAY_VIDEO(url)
#traceback.print_exc(file=sys.stderr)




def FREE_GATE_WEBPROXY(url):
	website:	http://dongtaiwang.com/home_en.php
	GET:		http://dongtaiwang.com/loc/redirect.php?pm=y&URL=https%3A%2F%2Femadmahdi.pythonanywhere.com
	Referer:	http://dongtaiwang.com
	return html





