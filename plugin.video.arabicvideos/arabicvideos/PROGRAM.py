# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='PROGRAM'

def MAIN(mode,text=''):
	if mode in [0,1]: FIX_KEYBOARD(mode,text)
	elif mode==2: SEND_MESSAGE(text)
	elif mode==3: DMCA()
	elif mode==4: HTTPS_TEST()
	elif mode==5: CLOSED()
	elif mode==6: GLOBAL_SEARCH(text)
	elif mode==7: VERSION()
	elif mode==8: RANDOM()
	elif mode==9: DELETE_CACHE()
	elif mode==170: TV_CHANNELS()
	elif mode==179: TESTINGS()
	
	return

def DELETE_CACHE():
	import PROBLEMS
	PROBLEMS.MAIN(190)
	yes = xbmcgui.Dialog().yesno('هل متأكد وتريد مسح جميع الكاش ؟','الكاش مهم لتسريع عمل البرنامج ومسحه يسبب اعادة طلب جميع الصفحات من الانترنيت عند الحاجة اليها. وهذا قد يحل مشاكل بعض المواقع','','','كلا','نعم')
	if yes==1: 
		DELETE_DATABASE_FILES()
		xbmcgui.Dialog().ok('تم مسح كاش البرنامج بالكامل','اذا كانت عندك مشكلة في احد المواقع فجرب الموقع الان ... واذا المشكلة مستمرة فاذن ارسل المشكلة الى المبرمج')
	return ''

def HTTPS_TEST():
	worked = HTTPS(True)
	if not worked:
		import PROBLEMS
		PROBLEMS.MAIN(152)

def FIX_KEYBOARD(mode,text):
	keyboard=text
	if keyboard=='': return
	if mode==1:
		try:
			window_id = xbmcgui.getCurrentWindowDialogId()
			window = xbmcgui.Window(window_id)
			keyboard = mixARABIC(keyboard)
			window.getControl(311).setLabel(keyboard)
		except: pass
	elif mode==0:
		ttype='X'
		check=isinstance(keyboard, unicode)
		if check==True: ttype='U'
		new1=str(type(keyboard))+' '+keyboard+' '+ttype+' '
		for i in range(0,len(keyboard),1):
			new1 += hex(ord(keyboard[i])).replace('0x','')+' '
		keyboard = mixARABIC(keyboard)
		ttype='X'
		check=isinstance(keyboard, unicode)
		if check==True: ttype='U'
		new2=str(type(keyboard))+' '+keyboard+' '+ttype+' '
		for i in range(0,len(keyboard),1):
			new2 += hex(ord(keyboard[i])).replace('0x','')+' '
		xbmcgui.Dialog().ok(new1,new2)
	return

def SEND_MESSAGE(text=''):
	if 'problem=yes' in text: problem='yes'
	else:
		problem='no'
		yes = xbmcgui.Dialog().yesno('هل لديك مشكلة تريد ابلاغ المبرمج عنها ؟','','','','كلا','نعم')
		if yes==1: problem='yes'
	if problem=='yes':
		yes = xbmcgui.Dialog().yesno('هل جربت مسح كاش البرنامج ولم تحل المشكلة ؟','في بعض الاحيان تكون المشكلة بسبب صفحة مخزنة في كاش البرنامج وعند مسح الكاش تعود الصفحة للعمل بصورة طبيعية','','','كلا','نعم')
		if yes==0: 
			DELETE_DATABASE_FILES()
			xbmcgui.Dialog().ok('تم مسح كاش البرنامج بالكامل','اذا كانت عندك مشكلة في احد المواقع فجرب الموقع الان ... واذا المشكلة مستمرة فاذن ارسل المشكلة الى المبرمج')
			return ''
		logs = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','سيقوم البرنامج بارسال ال 300 سطر الاخيرة من سجل الاخطاء الى المبرمج لكي يستطيع المبرمج معرفة المشكلة واصلاحها','','','كلا','نعم')
		if logs==0:
			xbmcgui.Dialog().ok('تم الغاء الارسال','للأسف بدون سجل الاخطاء المبرمج لا يستطيع معرفة المشكلة ولا حلها لان المبرمج لا يعلم الغيب')
			return ''
		logs2 = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','هل قمت قبل قليل بتشغيل الفيديو او الرابط الذي اعطاك المشكلة لكي يتم تسجيل هذه المشكلة في سجل الاخطاء قبل ارساله للمبرمج','','','كلا','نعم')
		if logs2==0:
			xbmcgui.Dialog().ok('تم الغاء الارسال','للأسف بدون تسجيل المشكلة في سجل الاخطاء فان المبرمج لا يستطيع معرفة المشكلة ولا حلها لان المبرمج لا يعلم الغيب')
			return ''
		"""
		else:
			text += 'logs=yes'
			yes = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','قبل ارسال سجل الاخطاء الى المبرمج عليك ان تقوم بتشغيل الفيديو او الرابط الذي يعطيك المشكلة لكي يتم تسجيل المشكلة في سجل الاخطاء. هل تريد الارسال الان ؟','','','كلا','نعم')
			if yes==0:
				xbmcgui.Dialog().ok('تم الغاء الارسال','')
				return ''
		xbmcgui.Dialog().ok('المبرمج لا يعلم الغيب','اذا كانت لديك مشكلة فالرجاء قراءة قسم المشاكل والاسئلة واذا لم تجد الحل هناك فحاول كتابة جميع تفاصيل المشكلة لان المبرمج لا يعلم الغيب')
		"""
	xbmcgui.Dialog().ok('email address عنوان الايميل','اذا كنت تحتاج جواب من المبرمج فيجب عليك اضافة عنوان بريدك الالكتروني الى الرسالة')
	search = KEYBOARD('Write a message   اكتب رسالة')
	if search == '':
		xbmcgui.Dialog().ok('تم الغاء الارسال','تم الغاء الارسال لانك لم تكتب اي شيء')
		return ''
	message = search
	subject = 'Message: From Arabic Videos'
	text = 'problem='+problem
	result = SEND_EMAIL(subject,message,'yes','','EMAIL-FROM-USERS',text)
	#	url = 'my API and/or SMTP server'
	#	payload = '{"api_key":"MY API KEY","to":["me@email.com"],"sender":"me@email.com","subject":"From Arabic Videos","text_body":"'+message+'"}'
	#	#auth=("api", "my personal api key"),
	#	import requests
	#	response = requests.request('POST',url, data=payload, headers='', auth='')
	#	response = requests.post(url, data=payload, headers='', auth='')
	#	if response.status_code == 200:
	#		xbmcgui.Dialog().ok('تم الارسال بنجاح','')
	#	else:
	#		xbmcgui.Dialog().ok('خطأ في الارسال','Error {}: {!r}'.format(response.status_code, response.content))
	#	FROMemailAddress = 'me@email.com'
	#	TOemailAddress = 'me@email.com'
	#	header = ''
	#	#header += 'From: ' + FROMemailAddress
	#	#header += '\nTo: ' + emailAddress
	#	#header += '\nCc: ' + emailAddress
	#	header += '\nSubject: من كودي الفيديو العربي'
	#	server = smtplib.SMTP('smtp-server',25)
	#	#server.starttls()
	#	server.login('username','password')
	#	response = server.sendmail(FROMemailAddress,TOemailAddress, header + '\n' + message)
	#	server.quit()
	#	xbmcgui.Dialog().ok('Response',str(response))
	return ''

def DMCA():
	text = 'نفي: البرنامج لا يوجد له اي سيرفر يستضيف اي محتويات. البرنامج يستخدم روابط وتضمين لمحتويات مرفوعة على سيرفرات خارجية. البرنامج غير مسؤول عن اي محتويات تم تحميلها على سيرفرات ومواقع خارجية "مواقع طرف 3". جميع الاسماء والماركات والصور والمنشورات هي خاصة باصحابها. البرنامج لا ينتهك حقوق الطبع والنشر وقانون الألفية للملكية الرقمية DMCA اذا كان لديك شكوى خاصة بالروابط والتضامين الخارجية فالرجاء التواصل مع ادارة هذه السيرفرات والمواقع الخارجية'
	xbmcgui.Dialog().textviewer('حقوق الطبع والنشر وقانون الألفية للملكية الرقمية',text)
	text = 'Disclaimer: The program does not host any content on any server. The program just use linking to or embedding content that was uploaded to popular Online Video hosting sites. All trademarks, Videos, trade names, service marks, copyrighted work, logos referenced herein belong to their respective owners/companies. The program is not responsible for what other people upload to 3rd party sites. We urge all copyright owners, to recognize that the links contained within this site are located somewhere else on the web or video embedded are from other various site. If you have any legal issues please contact appropriate media file owners/hosters.'
	xbmcgui.Dialog().textviewer('Digital Millennium Copyright Act (DMCA)',text)
	return

def GLOBAL_SEARCH(search=''):
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.lower()
	addDir('1.  [COLOR FFC89008]YUT  [/COLOR]'+search+' - موقع يوتيوب مشفر','',149,'','',search)
	addDir('2.  [COLOR FFC89008]SHF  [/COLOR]'+search+' - موقع شوف ماكس مشفر','',59,'','',search)
	addDir('3.  [COLOR FFC89008]KLA  [/COLOR]'+search+' - موقع كل العرب مشفر','',19,'','',search)
	addDir('4.  [COLOR FFC89008]PNT  [/COLOR]'+search+' - موقع بانيت','',39,'','',search)
	addDir('5.  [COLOR FFC89008]IFL    [/COLOR]'+search+' - موقع قناة اي فيلم','',29,'','',search)
	addDir('6.  [COLOR FFC89008]KWT  [/COLOR]'+search+' - موقع قناة الكوثر','',139,'','',search)
	addDir('7.  [COLOR FFC89008]MRF  [/COLOR]'+search+' - موقع قناة المعارف','',49,'','',search)
	addDir('8.  [COLOR FFC89008]FTM  [/COLOR]'+search+' - موقع المنبر الفاطمي','',69,'','',search)
	addDir('9.  [COLOR FFC89008]EGB  [/COLOR]'+search+' - موقع ايجي بيست مشفر','',5,'','',search)  # 129
	addDir('[COLOR FFC89008]=========================[/COLOR]','',9999)
	addDir('10.  [COLOR FFC89008]MVZ  [/COLOR]'+search+' - موقع موفيز لاند مشفر','',189,'','',search)
	addDir('11.  [COLOR FFC89008]AKM  [/COLOR]'+search+' - موقع اكوام مشفر','',79,'','',search)
	addDir('[COLOR FFC89008]=========================[/COLOR]','',9999)
	addDir('12.  [COLOR FFC89008]HEL  [/COLOR]'+search+' - موقع هلال يوتيوب مشفر','',99,'','',search)
	addDir('13.  [COLOR FFC89008]SHA  [/COLOR]'+search+' - موقع شاهد فوريو مشفر','',119,'','',search)
	addDir('14.  [COLOR FFC89008]HLA  [/COLOR]'+search+' - موقع هلا سيما مشفر','',89,'','',search)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TV_CHANNELS():
	addDir('1.  [COLOR FFC89008]TV0   [/COLOR]'+'قنوات من مواقعها الاصلية','',100)
	addDir('2.  [COLOR FFC89008]YUT  [/COLOR]'+'قنوات عربية من يوتيوب','',147)
	addDir('3.  [COLOR FFC89008]YUT  [/COLOR]'+'قنوات اجنبية من يوتيوب','',148)
	addDir('4.  [COLOR FFC89008]IFL    [/COLOR]'+'من موقع قناة اي فيلم','',28)
	#addDir('5.  [COLOR FFC89008]MRF  [/COLOR]'+'من موقع قناة المعارف','',41)
	#addDir('6.  [COLOR FFC89008]KWT  [/COLOR]'+'من موقع قناة الكوثر','',135)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addDir('5.  [COLOR FFC89008]TV1   [/COLOR]'+'قنوات تلفزونية خاصة','',101)
	addDir('6.  [COLOR FFC89008]TV2   [/COLOR]'+'قنوات تلفزونية للفحص','',102)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def VERSION():
	#   http://www.kproxy.com
	#   http://hideme.be
	#   http://www.apirequest.io
	#	url = 'http://raw.githack.com/emadmahdi/KODI/master/addons.xml'
	#   url = 'https://github.com/emadmahdi/KODI/raw/master/addons.xml'
	#xbmcgui.Dialog().notification('جاري طلب الارقام','','',2000)
	def dummyFunc():
		url = 'https://raw.githubusercontent.com/emadmahdi/KODI/master/addons.xml'
		html = openURL_KPROXY(url,'','','','PROGRAM-VERSION-1st')
		latest_ADDON_VER = re.findall('plugin.video.arabicvideos" name="Arabic Videos" version="(.*?)"',html,re.DOTALL)[0]
		current_ADDON_VER = xbmc.getInfoLabel('System.AddonVersion(plugin.video.arabicvideos)')
		latest_REPO_VER = re.findall('name="EMAD Repository" version="(.*?)"',html,re.DOTALL)[0]
		current_REPO_VER = xbmc.getInfoLabel('System.AddonVersion(repository.emad)')
		if latest_ADDON_VER > current_ADDON_VER:
			message1 =  'الرجاء تحديث البرنامج لحل المشاكل'
			message3 =  '\n\n' + 'جرب اغلاق كودي وتشغيله وانتظر التحديث الاوتوماتيكي'
		else:
			message1 = 'لا توجد اي تحديثات للبرنامج حاليا'
			message3 =  '\n\n' + 'الرجاء ابلاغ المبرمج عن اي مشكلة تواجهك'
		if current_REPO_VER=='': current_REPO_VER='لا يوجد'
		else: current_REPO_VER = ' ' + current_REPO_VER
		message2 = 'الاصدار الاخير للبرنامج المتوفر الان هو :   ' + latest_ADDON_VER
		message2 +=  '\n' + 'الاصدار الذي انت تستخدمه للبرنامج هو :   ' + current_ADDON_VER
		message2 += '\n' + 'الاصدار الاخير لمخزن عماد المتوفر الان هو :   ' + latest_REPO_VER
		message2 +=  '\n' + 'الاصدار الذي انت تستخدمه لمخزن عماد هو :  ' + current_REPO_VER
		message3 +=  '\n\n' + 'لكي يعمل التحديث الاوتوماتيكي يجب ان يكون لديك في كودي مخزن عماد EMAD Repository'
		message3 +=  '\n\n' + 'ملفات التنصيب مع التعليمات متوفرة على هذا الرابط'
		message3 +=  '\n' + 'https://github.com/emadmahdi/KODI'
		xbmcgui.Dialog().textviewer(message1,message2+message3)
	threads = CustomThread()
	threads.start_new_thread('1',dummyFunc)
	KODI_VERSION()
	threads.wait_finishing_all_threads()
	return ''

def RANDOM():
	headers = { 'User-Agent' : '' }
	url = 'https://www.bestrandoms.com/random-arabic-words'
	payload = { 'quantity' : '5' }
	data = urllib.urlencode(payload)
	#xbmcgui.Dialog().ok('',str(data))
	html = openURL_KPROXY(url,data,headers,'','PROGRAM-RANDOM-1st')
	html_blocks = re.findall('list-unstyled(.*?)clearfix',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('<span>(.*?)</span>.*?<span>(.*?)</span>',block,re.DOTALL)
	arbLIST,engLIST = [],[]
	for arbWORD, engWORD in items:
		arbLIST.append(arbWORD.lower())
		engLIST.append(engWORD.lower())
	list = ['كلمات عشوائية عربية','كلمات عشوائية انكليزية']
	while True:
		#selection = xbmcgui.Dialog().select('اختر اللغة:', list)
		#if selection == -1: return
		#elif selection==0: list2 = arbLIST
		#else: list2 = engLIST
		list2 = arbLIST + engLIST
		selection = xbmcgui.Dialog().select('اختر كلمة للبحث عنها:', list2)
		if selection != -1: break
		elif selection == -1: return
	search = list2[selection]
	GLOBAL_SEARCH(search)
	return

def CLOSED():
	xbmcgui.Dialog().ok('الموقع الاصلي للأسف مغلق','')
	return

def KODI_VERSION():
	#	https://kodi.tv/download/849
	#   https://play.google.com/store/apps/details?id=org.xbmc.kodi
	#	http://mirror.math.princeton.edu/pub/xbmc/releases/windows/win64
	#	http://mirrors.mit.edu/kodi/releases/windows/win64'
	url = 'http://mirrors.kodi.tv/releases/windows/win64/'
	html = openURL_cached(NO_CACHE,url,'','','','PROGRAM-KODI_VERSION-1st')
	latest_KODI_VER = re.findall('href="kodi-(.*?)-',html,re.DOTALL)[0]
	current_KODI_VER = xbmc.getInfoLabel( "System.BuildVersion" ).split(' ')[0]
	message4 = 'الاصدار الاخير لكودي المتوفر الان هو :   ' + latest_KODI_VER
	message4 +=  '\n' + 'الاصدار الذي انت تستخدمه لكودي هو :   ' + current_KODI_VER
	xbmcgui.Dialog().ok('كودي',message4)

def TESTINGS():
	url = 'https://intoupload.net/w2j4lomvzopd'
	import urlresolver
	try:
		#resolvable = urlresolver.HostedMediaFile(url).valid_url()
		link = urlresolver.HostedMediaFile(url).resolve()
		xbmcgui.Dialog().ok(str(link),url)
	except: xbmcgui.Dialog().ok('urlresolver: fail',url)
	import RESOLVERS
	titles,urls = RESOLVERS.RESOLVE(url)
	selection = xbmcgui.Dialog().select('TITLES :', titles)
	selection = xbmcgui.Dialog().select('URLS :', urls)
	#url = ''
	#PLAY_VIDEO(url)
	#settings = xbmcaddon.Addon(id=addon_id)
	#settings.setSetting('test1','hello test1')
	#var = settings.getSetting('test2')
	#xbmc.log('EMAD11 ' + str(var) + ' 11EMAD',level=xbmc.LOGNOTICE)
	#import subprocess
	#var = subprocess.check_output('wmic csproduct get UUID')
	#xbmc.log('EMAD11 ' + str(var) + ' 11EMAD',level=xbmc.LOGNOTICE)
	#import os
	#var = os.popen("wmic diskdrive get serialnumber").read()
	#xbmc.log('EMAD11 ' + str(var) + ' 11EMAD',level=xbmc.LOGNOTICE)

	#var = dummyClientID(32)
	#xbmcgui.Dialog().ok(var,'')
	#xbmc.log('EMAD11' + html + '11EMAD',level=xbmc.LOGNOTICE)
	url = ''
	urllist = [
		''
		]
	#play_item = xbmcgui.ListItem(path=url, thumbnailImage='')
	#play_item.setInfo(type="Video", infoLabels={"Title":''})
	# Pass the item to the Kodi player.
	#xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	# directly play the item.
	#xbmc.Player().play(url, play_item) 

	#import RESOLVERS
	#url = RESOLVERS.PLAY(urllist,script_name,'no')
	#PLAY_VIDEO(url,script_name,'yes')
	return
