# -*- coding: utf-8 -*-


import sys,urllib2,re,xbmcaddon,os,xbmc,platform,uuid,hashlib,random,xbmcgui,time


try:
	args = {'mode':'','text':''}
	line = sys.argv[2]
	if '?' in line:
		params = line[1:].split('&')
		for param in params:
			key,value = param.split('=',1)
			args[key] = value
	mode = args['mode']
	if mode.isdigit(): mode = int(mode)
	text = urllib2.unquote(args['text'])
except: mode,text = '',''


def ADDON_ID_VERSION():
	addonfolder = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
	addonfile = os.path.join(addonfolder,'addon.xml')
	with open(addonfile,'r') as f: xmlfile = f.read()
	version = re.findall('id=[\"\'](.*?)[\"\'].*?version=[\"\'](.*?)[\"\']',xmlfile,re.DOTALL|re.IGNORECASE)
	id,ver = version[0]
	return id,ver


def dummyClientID(length):
	#addon_id,addon_version = ADDON_ID_VERSION()
	hostname = platform.node()			# empc12/localhosting
	os_type = platform.system()			# Windows/Linux
	os_version = platform.release()		# 10.0/3.14.22
	os_bits = platform.machine()		# AMD64/aarch64
	#settings = xbmcaddon.Addon(id=addon_id)
	#savednode = settings.getSetting('node')
	savednode = ''
	if savednode=='':
		node = str(uuid.getnode())		# 326509845772831
		#settings.setSetting('node',node)
	else: node = savednode
	hashComponents = node+':'+hostname+':'+os_type+':'+os_version+':'+os_bits
	md5full = hashlib.md5(hashComponents).hexdigest()
	md5 = md5full[0:length]
	return md5


def SEND_ANALYTICS_EVENT():
	addon_id,addon_version = ADDON_ID_VERSION()
	website = 'INSTALL'
	kodi_release = xbmc.getInfoLabel("System.BuildVersion")
	kodi_version = re.findall('&&(.*?)[ -]','&&'+kodi_release,re.DOTALL)
	kodi_version = str(float(kodi_version[0]))
	randomNumber = str(random.randrange(111111111111,999999999999))
	try:
		headers = {'User-Agent':''}
		url = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addon_version+'&av='+addon_version+'&an=ARABIC_VIDEOS&ea='+website+'&el='+kodi_version+'&z='+randomNumber
		request = urllib2.Request(url=url,headers=headers)
		response = urllib2.urlopen(request)
		xbmc.log('skin.installEMAD ========= Sent analytics',level=xbmc.LOGNOTICE)	
		#html = response.read()
	except: pass
	return


def BUSY_DIALOG(job):
	# dialog = 'busydialog'				# KODI 17.9 and earlier
	dialog = 'busydialognocancel'		# KODI 18 and later
	if job=='start': xbmc.executebuiltin('ActivateWindow('+dialog+')')
	elif job=='stop': xbmc.executebuiltin('Dialog.Close('+dialog+')')
	return


if mode==1:
	SEND_ANALYTICS_EVENT()
	sys.exit()


xbmc.log('skin.installEMAD ========= Starting installation', level=xbmc.LOGNOTICE)


BUSY_DIALOG('start')


xbmc.executebuiltin('UpdateAddonRepos')
time.sleep(10)


ARABIC_TEXT = 'سوف تبدأ الآن عملية تثبيت برنامج عماد للفيديوهات العربية ومعه جلد عماد متروبولس باستخدام برنامج كودي ... البداية هي تحديث جميع إضافات كودي وعند نهاية هذه التحديثات سوف تختفي هذه الشاشة ويظهر بدلا منها قائمة البرامج ... حجم التحميل المتوقع هو تقريبا 170 ميجابايت وهذه تحتاج وقت تقريبا 10 دقائق لتحميل الملفات من الأنترنيت وتثبيتها في كودي ... إذا كانت الأنترنيت عندك بطيئة أو جهازك بطيء فأنت تحتاج أكثر من 10 دقائق ... أهمل رسائل الخطأ في هذه الشاشة ... في حال حدوث مشكلة قم بمسح كل شيء وابدأ من جديد'
ENGLISH_TEXT = 'Will start now the install of EMAD Arabic videos and EMAD metropolis skin using KODI app . This will update all KODI addons and switch the screen to the program menu . The download size expected is 170 MegaByte and this will need 10 minutes to download the files and install them on KODI . If your internet is slow or your device is slow then you will need more time . Ignore error messages in this screen . If you get problems then delete everything and start again'
window = xbmcgui.Window(10000)
window.getControl(9001).setLabel(ARABIC_TEXT)
yes = xbmcgui.Dialog().yesno('Do you want the above big message in English ?','هل تريد الرسالة الكبيرة أعلاه باللغة الانجليزية ؟','','','No : كلا','Yes : نعم')
if yes:
	window.getControl(9001).setLabel('')
	window.getControl(9002).setLabel(ENGLISH_TEXT)
yes = xbmcgui.Dialog().yesno('Do you want to start downloading now ?','هل تريد أن تبدأ التحميل الآن ؟','','','No : كلا','Yes : نعم')
if not yes:
	xbmc.executebuiltin('Quit()')
	xbmc.log('skin.installEMAD ========= User requested to quit installation', level=xbmc.LOGNOTICE)
	sys.exit()
time.sleep(10)


xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":"1","params":{"setting":"screensaver.mode","value":""}}')
time.sleep(5)
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"service.xbmc.versioncheck","enabled":false}}')
time.sleep(5)


#time.sleep(5)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":"1","setting.level":{"default":"expert"}}')
#time.sleep(5)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":"1","params":{"setting":"locale.country","value":"Australia (12h)"}}')
#time.sleep(5)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"videoplayer.errorinaspect","value":"20"}}')


xbmc.executebuiltin('InstallAddon(resource.language.ar_sa)')
time.sleep(1)
xbmc.executebuiltin('SendClick(11)')
time.sleep(5)
while xbmc.getCondVisibility('Window.IsActive(progressdialog)'): time.sleep(1)
time.sleep(5)


xbmc.executebuiltin('InstallAddon(plugin.video.arabicvideos)')
time.sleep(1)
xbmc.executebuiltin('SendClick(11)')
time.sleep(5)
while xbmc.getCondVisibility('Window.IsActive(progressdialog)'): time.sleep(1)
time.sleep(5)


xbmc.executebuiltin('InstallAddon(skin.metropolisEMAD)')
time.sleep(1)
xbmc.executebuiltin('SendClick(11)')
time.sleep(5)
while xbmc.getCondVisibility('Window.IsActive(progressdialog)'): time.sleep(1)
time.sleep(5)


xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.metropolisEMAD"}}')
time.sleep(1)
xbmc.executebuiltin('SendClick(11)')
time.sleep(5)


xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"skin.installEMAD","enabled":false}}')
time.sleep(5)


BUSY_DIALOG('stop')
xbmc.log('skin.installEMAD ========= Finished installation', level=xbmc.LOGNOTICE)


#xbmc.executebuiltin('UpdateLocalAddons')
#time.sleep(10)
