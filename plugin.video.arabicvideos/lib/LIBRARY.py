# -*- coding: utf-8 -*-
import urllib2,xbmcplugin,xbmcgui,sys,xbmc,os,re,time,urllib

addon_handle = int(sys.argv[1])
addon_id = sys.argv[0].split('/')[2] 		# plugin.video.arabicvideos
addon_path = sys.argv[0]+sys.argv[2] 		# plugin://plugin.video.arabicvideos/?mode=12&url=http://test.com
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def addDir(name,url='',mode='',iconimage=icon,page='',text=''):
	if iconimage=='': iconimage=icon
	u = 'plugin://'+addon_id+'/?mode='+str(mode)
	if url!='': u = u + '&url=' + quote(url)
	if page!='': u = u + '&page=' + quote(page)
	if text!='': u = u + '&text=' + quote(text)
	listitem=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setInfo( type="Video", infoLabels={ "Title": name } )
	listitem.setProperty('fanart_image', fanart)
	#listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=listitem,isFolder=True)
	return

def addLink(name,url,mode,iconimage=icon,duration='',text=''):
	if 'IsPlayable=no' in text: IsPlayable='no'
	else: IsPlayable='yes'
	if iconimage=='': iconimage=icon
	#xbmcgui.Dialog().ok(duration,'')
	u = 'plugin://'+addon_id+'/?mode='+str(mode)
	if url!='': u = u + '&url=' + quote(url)
	if text!='': u = u + '&text=' + quote(text)
	listitem=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setProperty('fanart_image', fanart)
	listitem.setInfo('Video', {'mediatype': 'video'})
	if duration != '' :
		if len(duration)<=2 : duration = '00:' + duration
		if len(duration)<=5 : duration = '00:' + duration
		duration = sum(x * int(t) for x, t in zip([3600,60,1], duration.split(":"))) 	
		listitem.setInfo('Video', {'duration': duration})
	if IsPlayable=='yes': listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.setContent(addon_handle, 'videos')
	xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=listitem,isFolder=False)
	return

def openURL(url,data='',headers='',showDialogs='',source=''):
	if showDialogs=='': showDialogs='yes'
	if data=='' and headers=='': request = urllib2.Request(url)
	elif data=='' and headers!='': request = urllib2.Request(url,headers=headers)
	elif data!='' and headers=='': request = urllib2.Request(url,data=data)
	elif data!='' and headers!='': request = urllib2.Request(url,headers=headers,data=data)
	html,code,reason = '','200','OK'
	try:
		response = urllib2.urlopen(request,timeout=60)
		html = response.read()
		code = str(response.code)
		response.close
	except urllib2.HTTPError as error:
		code = str(error.code)
		reason = str(error.reason)
	except urllib2.URLError as error:
		code = str(error.reason[0])
		reason = str(error.reason[1])
	if code!='200':
		message,send,showDialogs = '','no','no'
		html = 'Error {}: {!r}'.format(code, reason)
		if 'google-analytics' in url: send = showDialogs
		if showDialogs=='yes':
			xbmcgui.Dialog().ok('خطأ في الاتصال',html)
			if code=='502' or code=='7':
				xbmcgui.Dialog().ok('Website is not available','لا يمكن الوصول الى الموقع والسبب قد يكون من جهازك او من الانترنيت الخاصة بك او من الموقع كونه مغلق للصيانة او التحديث لذا يرجى المحاولة لاحقا')
				send = 'no'
			elif code=='404':
				xbmcgui.Dialog().ok('File not found','الملف غير موجود والسبب غالبا هو من المصدر ومن الموقع الاصلي الذي يغذي هذا البرنامج')
			if send=='yes':
				yes = xbmcgui.Dialog().yesno('سؤال','هل تربد اضافة رسالة مع الخطأ لكي تشرح فيها كيف واين حصل الخطأ وترسل التفاصيل الى المبرمج ؟','','','كلا','نعم')
				if yes: message = ' \\n\\n' + KEYBOARD('Write a message   اكتب رسالة')
		if send=='yes': SEND_EMAIL('Error: From Arabic Videos',html+message,showDialogs,url,source)
	return html

#with open('S:\emad3.html', 'w') as file: file.write(block)

#file = open('/data/emad.html', 'w')
#file.write(html)
#file.close()

def quote(url):
	return urllib2.quote(url,':/')

def unquote(url):
	return urllib2.unquote(url)

#decode('utf8')
#decode('unicode_escape')
#decode('ascii')
#decode('windows-1256')

def unescapeHTML(string):
	if '&' in string and ';' in string:
		string = string.decode('utf8')
		import HTMLParser
		string = HTMLParser.HTMLParser().unescape(string)
		string = string.encode('utf8')
	return string

def escapeUNICODE(string):
	if '\u' in string:
		string = string.decode('unicode_escape')
		string = string.encode('utf8')
	return string

def mixARABIC(string):
	import unicodedata
	#if '\u' in string:
	#	string = string.decode('unicode_escape')
	#	unicode_strings=re.findall(r'\u[0-9A-F]',string)	
	#	for unicode in unicode_strings
	#		char = unichar(
	#		replace(    , char)
	string = string.decode('utf8')
	new_string = ''
	for letter in string:
		#xbmcgui.Dialog().ok(unicodedata.decomposition(letter),hex(ord(letter)))
		if ord(letter) < 256: unicode_letter = '\u00'+hex(ord(letter)).replace('0x','')
		elif ord(letter) < 4096: unicode_letter = '\u0'+hex(ord(letter)).replace('0x','')
		else: unicode_letter = '\u'+unicodedata.decomposition(letter).split(' ')[1]
		new_string += unicode_letter
	new_string = new_string.replace('\u06CC','\u0649')
	new_string = new_string.decode('unicode_escape')
	new_string = new_string.encode('utf-8')
	return new_string

def KEYBOARD(label='Search'):
	search =''
	keyboard = xbmc.Keyboard(search, label)
	keyboard.doModal()
	if keyboard.isConfirmed(): search = keyboard.getText()
	search = search.strip(' ')
	if len(search.decode('utf8'))<2:
		#xbmcgui.Dialog().ok('Wrong entry. Try again','خطأ في الادخال. أعد المحاولة')
		return ''
	new_search = mixARABIC(search)
	return new_search

def PLAY_VIDEO(url3,website='',showWatched='yes'):
	class PlayerCalss(xbmc.Player):
		def __init__( self, *args, **kwargs ):
			self.status = ''
		def onPlayBackStopped(self):
			self.status='Failed'
		def onPlayBackStarted(self):
			self.status='Playing'
			time.sleep(1)
		def onPlayBackError(self):
			self.status='Failed'
		def onPlayBackEnded(self):
			self.status='Failed'
	myplayer = PlayerCalss()
	if len(url3)==2:
		url,subtitle = url3
		urlmessage = 'Url:['+url+']  Subtitle:['+subtitle+']'
	else:
		url,subtitle = url3,''
		urlmessage = 'Url:['+url+']'
	xbmc.log('['+addon_id+']:  Started playing video:  '+urlmessage, level=xbmc.LOGNOTICE)
	if 'https' in url:
		html = openURL('https://www.google.com','','','','LIBRARY-1st')
		if 'html' not in html:
			xbmcgui.Dialog().ok('الاتصال مشفر','مشكلة ... هذا الفيديو يحتاج الى اتصال مشفر (ربط مشفر) ولكن للأسف الاتصال المشفر لا يعمل على جهازك')
			from PROBLEMS import MAIN as PROBLEMS_MAIN
			PROBLEMS_MAIN(152)
			return
	play_item = xbmcgui.ListItem(path=url)
	if showWatched=='yes':
		#title = xbmc.getInfoLabel('ListItem.Title')
		#label = xbmc.getInfoLabel('ListItem.Label')
		#xbmcgui.Dialog().ok(url,label)
		#play_item.setInfo( "video", { "Title": label } )
		#play_item.setPath(url)
		#play_item.setInfo('Video', {'duration': 3600})
		if '.mpd' in url:
			#play_item.setContentLookup(False)
			#play_item.setMimeType('application/xml+dash')
			play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
			play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
			#emad   play_item.setMimeType('application/dash+xml')
			#emad   play_item.setContentLookup(True)
		if subtitle!='':
			play_item.setSubtitles([subtitle])
			#xbmc.log('['+addon_id+']:  Added subtitle to video: ['+subtitle+']', level=xbmc.LOGNOTICE)
		xbmcplugin.setResolvedUrl(addon_handle, True, play_item)
		#xbmc.Player().play(url,play_item)
	else:
		label = xbmc.getInfoLabel('ListItem.Label')
		play_item.setInfo( "video", { "Title": label } )
		myplayer.play(url,play_item)
	#logfilename = xbmc.translatePath('special://logpath')+'kodi.log'
	timeout,step,result = 60,2,'Tried'
	#progress = xbmcgui.DialogProgress()
	#progress.create('جاري محاولة تشغيل الفيديو المطلوب')
	for i in range(0,timeout,step):
		xbmc.sleep(step*1000)
		#progress.update(i*100/timeout,'باقي '+str(timeout-i)+' ثانية')
		result = myplayer.status
		if result=='Playing':
			xbmc.log('['+addon_id+']:  Success: Video is playing successfully:  '+urlmessage, level=xbmc.LOGNOTICE)
			xbmcgui.Dialog().notification('','')
			break
		elif result=='Failed':
			xbmc.log('['+addon_id+']:  Failure: Video failed playing:  '+urlmessage, level=xbmc.LOGNOTICE)
			break
		xbmcgui.Dialog().notification(myplayer.status +' جاري محاولة تشغيل الفيديو المطلوب','باقي '+str(timeout-i)+' ثانية')
		"""
		elif progress.iscanceled():
			myplayer.stop()
			result = 'Canceled0'
			xbmc.log('['+addon_id+']:  Canceled: Video was canceled successfully:  '+urlmessage, level=xbmc.LOGNOTICE)
			break
		"""
	else:
		myplayer.stop()
		result = 'Timeout'
		xbmc.log('['+addon_id+']:  Timeout: Unknown playing issue:  '+urlmessage, level=xbmc.LOGNOTICE)
		"""
		playing = str(myplayer.isPlaying())
		logfile = file(logfilename, 'rb')
		logfile.seek(-4000, os.SEEK_END)
		logfile = logfile.read()
		logfile2 = logfile.split('['+addon_id+']:  Started playing video:')
		if len(logfile2)==1: continue
		else: logfile2 = logfile2[-1]
		if 'CloseFile' in logfile2 or 'Attempt to use invalid handle' in logfile2:
			result = 'Failed'
			xbmc.log('['+addon_id+']:  Failure: Video failed playing:  '+urlmessage, level=xbmc.LOGNOTICE)
			#break
		elif 'Opening stream' in logfile2:
			result = 'Playing'
			xbmc.log('['+addon_id+']:  Success: Video is playing successfully:  '+urlmessage, level=xbmc.LOGNOTICE)
			#break
		"""
	if result!='Playing': xbmcgui.Dialog().notification('انتهت عملية التشغيل','بالفشل')
	#progress.close()
	#if i==timeout-step:
	#	myplayer.stop()
	#	result = 'Timeout'
	#	xbmc.log('['+addon_id+']:  Timeout: Unknown playing issue:  '+urlmessage, level=xbmc.LOGNOTICE)
	addonVersion = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
	import random
	randomNumber = str(random.randrange(111111111111,999999999999))
	url2 = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addonVersion+'&av='+addonVersion+'&an=ARABIC_VIDEOS&ea='+website+'&z='+randomNumber
	openURL(url2,'','','no','LIBRARY-PLAY_VIDEO-1st')
	return result

def SEND_EMAIL(subject,message,showDialogs='yes',url='',source='',text=''):
	if 'logs=yes' in text: logs='yes'
	else: logs='no'
	sendit=1
	html = ''
	if showDialogs=='yes':
		sendit = xbmcgui.Dialog().yesno('هل ترسل هذه الرسالة الى المبرمج',message.replace('\\n','\n'),'','','كلا','نعم')
	if sendit==1:
		addonVersion = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
		kodiVersion = xbmc.getInfoLabel( "System.BuildVersion" )	
		kodiName = xbmc.getInfoLabel( "System.FriendlyName" )
		message = message+' \\n\\n==== ==== ==== \\nAddon Version: '+addonVersion+' :\\nEmail Sender: '+dummyClientID(32)+' :\\nKodi Version: '+kodiVersion+' :\\nKodi Name: '+kodiName
		#xbmc.sleep(4000)
		#playerTitle = xbmc.getInfoLabel( "Player.Title" )
		#playerPath = xbmc.getInfoLabel( "Player.Filenameandpath" )
		#if playerTitle != '': message += ' :\\nPlayer Title: '+playerTitle
		#if playerPath != '': message += ' :\\nPlayer Path: '+playerPath
		#xbmcgui.Dialog().ok(playerTitle,playerPath)
		if url != '': message += ' :\\nURL: ' + url
		if source != '': message += ' :\\nSource: ' + source
		message += ' :\\n'
		logfileNEW = ''
		if logs:
			logfile = xbmc.translatePath('special://logpath')+'kodi.log'
			logfile=file(logfile, 'rb')
			logfile.seek(-15000, os.SEEK_END)
			logfile = logfile.read().splitlines()
			#xbmcgui.Dialog().ok(logfile,str(len(logfile)))
			logfileNEW = '\n'.join(logfile[-100:])
			from base64 import b64encode as base64_b64encode
			logfileNEW = base64_b64encode(logfileNEW)
		url = 'http://emadmahdi.pythonanywhere.com/sendemail'
		payload = { 'subject' : quote(subject) , 'message' : quote(message) , 'logfile' : logfileNEW }
		data = urllib.urlencode(payload)
		html = openURL(url,data,'','','LIBRARY-SEND_EMAIL-1st')
		result = html[0:6]
		if showDialogs=='yes':
			if result == 'Error ':
				xbmcgui.Dialog().ok('Failed sending the message','خطأ وفشل في ارسال الرسالة')
			else:
				xbmcgui.Dialog().ok('Message sent','تم ارسال الرسالة بنجاح')
	return html

def dummyClientID(length):
	#from uuid import getnode as uuid_getnode
	#macfull = hex(uuid_getnode())		# e1f2ace4a35e
	#mac = '-'.join(mac_num[i:i+2].upper() for i in range(0,11,2))		# E1:F2:AC:E4:A3:5E
	import platform
	hostname = platform.node()			# empc12/localhosting
	os_type = platform.system()			# Windows/Linux
	os_version = platform.release()		# 10.0/3.14.22
	os_bits = platform.machine()		# AMD64/aarch64
	#processor = platform.processor()	# Intel64 Family 9 Model 68 Stepping 16, GenuineIntel/''
	import xbmcaddon
	settings = xbmcaddon.Addon(id=addon_id)
	savednode = settings.getSetting('node')
	if savednode=='':
		from uuid import getnode as uuid_getnode
		node = str(uuid_getnode())		# 326509845772831
		settings.setSetting('node',node)
	else:
		node = savednode
	hashComponents = node+':'+hostname+':'+os_type+':'+os_version+':'+os_bits
	from hashlib import md5 as hashlib_md5
	md5full = hashlib_md5(hashComponents).hexdigest()
	md5 = md5full[0:length]
	#xbmcgui.Dialog().ok(node,md5)
	return md5
	#import xbmcaddon
	#settings = xbmcaddon.Addon(id=addon_id)
	#settings.setSetting('user.hash','')
	#settings.setSetting('user.hash2','')
	#settings.setSetting('user.hash3','')
	#settings.setSetting('user.hash4','')
	#else: file = 'saverealhash4'
	#url = 'http://emadmahdi.pythonanywhere.com/saveinput'
	#input = md5full + '  ::  Found at:' + str(i) + '  ::  ' + hashComponents
	#	#payload = { 'file' : file , 'input' : input }
	#	#data = urllib.urlencode(payload)
	#	#html = openURL(url,data,'','','LIBRARY-DUMMYCLIENTID-1st')
	#import requests
	#headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
	#payload = "file="+file+"&input="+input
	#response = requests.request("POST", url, data=payload, headers=headers)
	#	#html = response.text
	#	#xbmcgui.Dialog().ok(html,html)
	#url = 'http://emadmahdi.pythonanywhere.com/saveinput'
	#payload = { 'file' : 'savehash' , 'input' : md5full + '  ::  ' + hashComponents }
	#data = urllib.urlencode(payload)
	#return ''

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
	#xbmcgui.Dialog().ok(title,title2)
	return title2
"""



