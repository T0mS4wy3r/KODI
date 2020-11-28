# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from LIBRARY import *

script_name='DOWNLOAD'

def MAIN(mode,url,context):
	#DIALOG_OK(url,context)
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if context=='6_REMOVE': results = DELETE_FILE(url)
	elif mode==330: results = LIST_FILES()
	elif mode==331: results = PLAY(url)
	elif mode==332: results = CHANGE_FOLDER()
	elif mode==333: results = TO_ADD()
	else: results = False
	return results

def DELETE_FILE(filenamepath):
	try: os.remove(filenamepath.decode('utf8'))
	except: os.remove(filenamepath)
	return

def PLAY(url):
	result = PLAY_VIDEO(url,script_name,'video')
	#xbmc.Player().play(url)
	#DIALOG_OK(url,result)
	return

def TO_ADD():
	message = 'أذهب الى رابط الفيديو او الصوت في الموقع المطلوب ثم أضغط على زر القائمة اليمين ثم أختار "تحميل ملفات فيديو" ثم اختار دقة الصورة واختار نوع ملف الصورة وبعدها سوف يبدأ التحميل'
	DIALOG_OK('طريقة تحميل الملفات',message)
	return

def LIST_FILES():
	addMenuItem('link','[COLOR FFC89008]طريقة تحميل ملفات الفيديو[/COLOR]','',333)
	downloadpath = GET_DOWNLOAD_FOLDER()
	mtime = os.stat(downloadpath).st_mtime
	files = []
	for filename in os.listdir(unicode(downloadpath,'utf8')):
		if not filename.startswith('file_'): continue
		filepath = os.path.join(downloadpath,filename)
		mtime = os.path.getmtime(filepath)
		#ctime = os.path.getctime(filepath)
		#mtime = os.stat(filepath).ct_mtime
		#filename = filename.decode('utf8').encode('utf8')
		files.append([filename,mtime])
	files = sorted(files,reverse=True,key=lambda key: key[1])
	for filename,mtime in files:
		#DIALOG_OK(filename,filename)
		filename = filename.decode('utf8').encode('utf8')
		filepath = os.path.join(downloadpath,filename)
		addMenuItem('video',filename,filepath,331)
	return

def GET_DOWNLOAD_FOLDER():
	settings = xbmcaddon.Addon(id=addon_id)
	downloadpath = settings.getSetting('download.path')
	if downloadpath!='': return downloadpath
	settings.setSetting('download.path',addoncachefolder)
	return addoncachefolder

def CHANGE_FOLDER():
	downloadpath = GET_DOWNLOAD_FOLDER()
	change = DIALOG_YESNO(downloadpath,'هذا هو مكان تخزين ملفات الفيديو التي تحملها انت باستخدام هذا البرنامج . هل تريد تغيير المكان ؟','','','كلا','نعم')
	if change:
		newpath = DIALOG_BROWSESINGLE(3,'مكان تحميل ملفات الفيديو','local','',False,True,downloadpath)
		yes = DIALOG_YESNO(newpath,'هذا هو المكان الجديد لتخزين ملفات الفيديو التي تحملها انت باستخدام هذا البرنامج . هل تريد استخدامه بدلا من المكان القديم ؟','','','كلا','نعم')
		if yes:
			settings = xbmcaddon.Addon(id=addon_id)
			settings.setSetting('download.path',newpath)
			DIALOG_OK('رسالة من المبرمج','تم تغيير مكان تخزين الملفات المحملة')
	#if not change or not yes: DIALOG_OK('رسالة من المبرمج','تم الغاء العملية')
	return

def DOWNLOAD_VIDEO(url,videofiletype):
	DIALOG_NOTIFICATION('يرجى الانتظار','جاري فحص ملف التحميل',sound=False)
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Preparing to download the video file   URL: [ '+url+' ]')
	#DIALOG_OK(url,videofiletype)
	if videofiletype=='':
		if 'mp4' in url.lower(): videofiletype = '.mp4'
		elif 'm3u8' in url.lower(): videofiletype = '.m3u8'
	if videofiletype not in ['.ts','.mkv','.mp4','.mp3','.flv','.m3u8','avi']:
		DIALOG_OK('تنزيل ملف الفيديو','الملف من نوع '+videofiletype+' والبرنامج حاليا غير جاهز لتحميل هذا النوع من الملفات')
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Video type/extension is not supported   URL: [ '+url+' ]')
		return
	#DIALOG_OK('free space',str(freediskspace_MB))
	settings = xbmcaddon.Addon(id=addon_id)
	filename = menu_label.replace('  ',' ').replace(' ','_')
	filename = 'file_'+str(int(now))[-4:]+'_'+filename+videofiletype
	downloadpath = GET_DOWNLOAD_FOLDER()
	windowsfilename = windows_filename(filename).decode('utf8')
	windowsfilenamepath = os.path.join(downloadpath,windowsfilename)
	filenamepath = os.path.join(downloadpath,filename)
	#DIALOG_OK(downloadpath,filename)
	url = url.replace('verifypeer=false','')
	if 'User-Agent=' in url:
		url2,useragent = url.rsplit('User-Agent=',1)
		useragent = useragent.replace('|','').replace('&','')
	else: url2,useragent = url,None
	if 'Referer=' in url2: url2,referer = url2.rsplit('Referer=',1)
	else: url2,referer = url2,''
	url2 = url2.strip('|').strip('&').strip('|').strip('&')
	referer = referer.replace('|','').replace('&','')
	headers = {'User-Agent':useragent}
	if referer!='':	headers['Referer'] = referer
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Downloading video file   URL: [ '+url2+' ]   Headers: [ '+str(headers)+' ]   File: [ '+filenamepath+' ]')
	#DIALOG_OK(url2,str(headers))
	#DIALOG_OK(xbmc.getInfoLabel('System.UsedSpace'),xbmc.getInfoLabel('System.TotalSpace'))
	#DIALOG_OK(xbmc.getInfoLabel('System.UsedSpacePercent'),xbmc.getInfoLabel('System.FreeSpacePercent'))
	MegaByte = 1024*1024
	freediskspace =	xbmc.getInfoLabel('System.FreeSpace')
	freediskspace_MB = int(re.findall('\d+',freediskspace)[0])
	if freediskspace_MB==0:
		try:
			st = os.statvfs(downloadpath)
			freediskspace_MB = st.f_frsize*st.f_bavail/MegaByte
			#DIALOG_OK(osname,str(freediskspace_MB))
			#string = str(st.f_bavail)+','+str(st.f_frsize)+','+str(st.f_blocks)
			#string += ','+str(st.f_bfree)+','+str(st.f_bsize)+','+str(st.f_ffree)
			#DIALOG_OK(str(freeuserspace),str(dir(st)))
		except: pass
		if freediskspace_MB==0:
			DIALOG_TEXTVIEWER('مساحة التخزين مجهولة','للأسف البرنامج غير قادر أن يحدد مقدار مساحة التخزين الفارغة في جهازك وعليه فان تحميل الفيديوهات لن يعمل عندك إلى أن يقوم مبرمجي برنامج كودي بحل هذه المشكلة لان تحميل الفيديوهات قد يسبب امتلاء جهازك بالملفات وهذا فيه خطورة على عمل جهازك بصورة صحيحة ولهذا السبب قام المبرمج مؤقتا بمنع البرنامج من تحميل الفيديوهات')
			LOG_THIS('NOTICE',LOGGING(script_name)+'   Unable to determine the disk free space')
			return
	import requests
	headers['Accept-Encoding'] = ''
	if videofiletype=='.m3u8':
		windowsfilenamepath = windowsfilenamepath.rsplit('.m3u8')[0]+'.mp4'
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url2,'',headers,'','','DOWNLOAD-DOWNLOAD_VIDEO-1st')
		m3u8 = response.content
		linkLIST = []
		links = re.findall('\#EXTINF:.*?[\n\r](.*?)[\n\r]',m3u8+'\n\r',re.DOTALL)
		if not links:
			LOG_THIS('NOTICE',LOGGING(script_name)+'   The m3u8 file did not have the required links   URL: [ '+url2+' ]')
			return
		try: file = open(windowsfilenamepath,'wb')
		except: file = open(windowsfilenamepath.encode('utf8'),'wb')
		response = requests.get(links[0])
		chunk = response.content
		response.close()
		file.write(chunk)
		chunksize = len(chunk)
		chunksCount = len(links)
		filesize = chunksize*chunksCount
	else:
		chunksize = 1*MegaByte
		response = requests.request('GET',url2,headers=headers,verify=False,stream=True)
		try: filesize = int(response.headers['Content-Length'])
		except: filesize = 0
		chunksCount = int(filesize/chunksize)
		if filesize>102400:
			try: file = open(windowsfilenamepath,'wb')
			except: file = open(windowsfilenamepath.encode('utf8'),'wb')
	filesize_MB = int(1+filesize/MegaByte)
	if filesize<=102400:
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Video file is too small and/or something wrong   URL: [ '+url2+' ]   Video file size: [ '+str(filesize_MB)+' MB ]   Available size: [ '+str(freediskspace_MB)+' MB ]   File: [ '+filenamepath+' ]')
		DIALOG_OK('رسالة من المبرمج','فشل في معرفة حجم ملف الفيديو ولهذا لا يمكن للبرنامج تحميل هذا الملف')
		if videofiletype=='.m3u8': file.close()
		return
	freeafterdownload_MB = freediskspace_MB-filesize_MB
	if freeafterdownload_MB<500:
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Not enough disk space to download the video file   URL: [ '+url2+' ]   Video file size: [ '+str(filesize_MB)+' MB ]   Available size: [ '+str(freediskspace_MB)+' MB ]   File: [ '+filenamepath+' ]')
		DIALOG_OK('لا يوجد مساحة كافية للتحميل','الملف المطلوب تحميله حجمه '+str(filesize_MB)+' ميغابايت وجهازك فيه مساحة فارغة '+str(freediskspace_MB)+' ميغابايت وللمحافظة على عمل جهازك بدون مشاكل يجب ابقاء 500 ميغابايت فارغة دائما وهذا معناه جهازك لا توجد فيه مساحة كافية لتحميل ملف الفيديو المطلوب')
		file.close()
		return
	yes = DIALOG_YESNO('هل تريد تحميل الملف ؟','الملف المطلوب حجمه تقريبا '+str(filesize_MB)+' ميغابايت وجهازك فيه مساحة فارغة تقريبا '+str(freediskspace_MB)+' ميغابايت وهذا الملف قد يحتاج بعض الوقت للتحميل من الأنترنيت إلى جهازك . هل انت متأكد وتريد الاستمرار بتحميل ملف الفيديو ؟','','','كلا','نعم')
	if not yes:
		DIALOG_OK('','تم إلغاء عملية تحميل ملف الفيديو')
		file.close()
		LOG_THIS('NOTICE',LOGGING(script_name)+'   User refused to start the download of the video file   URL: [ '+url2+' ]   File: [ '+filenamepath+' ]')
		return
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Download started successfully')
	pDialog = DIALOG_PROGRESS()
	pDialog.create(windowsfilenamepath,'السطر فوق هو مكان تخزين ملف الفيديو')
	Finished = True
	t1 = time.time()
	if videofiletype=='.m3u8': # m3u8 and multi chunks video files
		for i in range(1,chunksCount):
			link = links[i]
			if 'http' not in link: link = url2.rsplit('/',1)[0]+'/'+link
			response = requests.get(link)
			chunk = response.content
			response.close()
			file.write(chunk)
			t2 = time.time()
			timeElapsed = t2-t1
			chunkTime = timeElapsed/i
			timeTotal = chunkTime*(chunksCount+1)
			timeRemaining = timeTotal-timeElapsed
			pDialog.update(int(100*i/(chunksCount+1)),'السطر فوق هو مكان تخزين ملف الفيديو','جلب ملف الفيديو:- الجزء رقم',str(i*chunksize/MegaByte)+'/'+str(filesize_MB)+' MB    وقت متبقي: '+time.strftime("%H:%M:%S",time.gmtime(timeRemaining))+' ـ')
			if pDialog.iscanceled():
				Finished = False
				break
	else: # mp4 and other single file videos
		i = 0
		for chunk in response.iter_content(chunk_size=chunksize):
			file.write(chunk)
			#file = file+chunk
			i = i+1
			t2 = time.time()
			timeElapsed = t2-t1
			chunkTime = timeElapsed/i
			timeTotal = chunkTime*(chunksCount+1)
			timeRemaining = timeTotal-timeElapsed
			pDialog.update(int(100*i/(chunksCount+1)),'السطر فوق هو مكان تخزين ملف الفيديو','جلب ملف الفيديو:- الجزء رقم',str(i*chunksize/MegaByte)+'/'+str(filesize_MB)+' MB    وقت متبقي: '+time.strftime("%H:%M:%S",time.gmtime(timeRemaining))+' ـ')
			if pDialog.iscanceled():
				Finished = False
				break
		response.close()
		#with open(filename,'w') as f: f.write(file)
	file.close()
	pDialog.close()
	if not Finished:
		LOG_THIS('NOTICE',LOGGING(script_name)+'   User cancelled/interrupted the download process   URL: [ '+url2+' ]   File: [ '+filenamepath+' ]')
		DIALOG_OK('','تم إلغاء عملية تحميل ملف الفيديو')
		return
	else:
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Video file downloaded successfully   URL: [ '+url2+' ]   File: [ '+filenamepath+' ]')
		DIALOG_OK('','تم تحميل ملف الفيديو بنجاح')
		return



