# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='PROGRAM'

def MAIN(mode,text=''):
	if mode in [0,1]: FIX_KEYBOARD(mode,text)
	elif mode==2: SEND_MESSAGE(text)
	elif mode==3: DMCA()
	elif mode==4: HTTPS_TEST()
	elif mode==5: CLOSED()
	elif mode==6: GLOBAL_SEARCH_MENU(text)
	elif mode==7: VERSION()
	elif mode==8: RANDOM()
	elif mode==9: DELETE_CACHE()
	elif mode==170: TV_CHANNELS_MENU()
	elif mode==171: SSL_WARNING()
	elif mode==172: TOOLS_MENU()
	elif mode==173: ENABLE_MPD()
	elif mode==174: ENABLE_RTMP()
	elif mode==175: TEST_ALL_WEBSITES()
	elif mode==179: TESTINGS()
	return

def TOOLS_MENU():
	addDir('[COLOR FFC89008]ـ Problems & Questions  قائمة مشاكل وأسئلة  .1 [/COLOR]','',150)
	#addLink('[COLOR FFC89008] 2.  [/COLOR]'+'فحص جميع مواقع البرنامج','',175,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 2.  [/COLOR]'+'فحص الاصدار الاخير والتحديثات','',7,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 3.  [/COLOR]'+'فحص تفعيل فيديوهات mpd ـ','',173,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 4.  [/COLOR]'+'فحص تفعيل فيديوهات rtmp ـ','',174,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 5.  [/COLOR]'+'فحص اتصال المواقع المشفرة','',4,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 6.  [/COLOR]'+'مسح كاش البرنامج','',9,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 7.  [/COLOR]'+'ارسال سجل الاخطاء للمبرمج','',2,'','','IsPlayable=no,problem=yes')
	addLink('[COLOR FFC89008] 8.  [/COLOR]'+'ابلاغ المبرمج بوجود مشكلة','',2,'','','IsPlayable=no,problem=yes')
	addLink('[COLOR FFC89008] 9.  [/COLOR]'+'ارسال رسالة الى المبرمج','',2,'','','IsPlayable=no,problem=no')
	addLink('[COLOR FFC89008]10. [/COLOR]'+'تحذير يخص شهادة التشفير','',171,'','','IsPlayable=no')
	addLink('[COLOR FFC89008]11. [/COLOR]'+'ـ DMCA  قانون الألفية للملكية الرقمية','',3,'','','IsPlayable=no')
	#addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	xbmcplugin.endOfDirectory(addon_handle)
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
	working = HTTPS(True)
	if not working:
		import PROBLEMS
		PROBLEMS.MAIN(152)
	return

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
		#xbmcgui.Dialog().ok(new1,new2)
	return

def SEND_MESSAGE(text=''):
	if 'problem=yes' in text: problem='yes'
	else:
		problem='no'
		yes = xbmcgui.Dialog().yesno('','هل لديك مشكلة تريد ابلاغ المبرمج عنها ؟','','','كلا','نعم')
		if yes==1: problem='yes'
	if problem=='yes':
		yes = xbmcgui.Dialog().yesno('هل جربت مسح كاش البرنامج ولم تحل المشكلة ؟','في بعض الاحيان تكون المشكلة بسبب صفحة مخزنة في كاش البرنامج وعند مسح الكاش تعود الصفحة للعمل بصورة طبيعية','','','كلا','نعم')
		if yes==0: 
			DELETE_DATABASE_FILES()
			xbmcgui.Dialog().ok('تم مسح كاش البرنامج بالكامل','اذا كانت عندك مشكلة في احد المواقع فجرب الموقع الان ... واذا المشكلة مستمرة فاذن ارسل المشكلة الى المبرمج')
			return ''
		logs = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','سيقوم البرنامج بارسال ال 400 سطر الاخيرة من سجل الاخطاء الى المبرمج لكي يستطيع المبرمج معرفة المشكلة واصلاحها','','','كلا','نعم')
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
				xbmcgui.Dialog().ok('','تم الغاء الارسال')
				return ''
		xbmcgui.Dialog().ok('المبرمج لا يعلم الغيب','اذا كانت لديك مشكلة فالرجاء قراءة قسم المشاكل والاسئلة واذا لم تجد الحل هناك فحاول كتابة جميع تفاصيل المشكلة لان المبرمج لا يعلم الغيب')
		"""
	xbmcgui.Dialog().ok('ملاحظة مهمة','اكتب الان رسالة الى المبرمج واذا كنت تحتاج جواب من المبرمج فلا تنسى اضافة عنوان بريدك الالكتروني الى الرسالة')
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
	#		xbmcgui.Dialog().ok('','تم الارسال بنجاح')
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

def GLOBAL_SEARCH_MENU(search=''):
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.lower()
	addLink('[COLOR FFC89008]مواقع سيرفرات خاصة - قليلة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('1.  [COLOR FFC89008]YUT  [/COLOR]'+search+' - موقع يوتيوب','',149,'','',search)
	addDir('2.  [COLOR FFC89008]SHF  [/COLOR]'+search+' - موقع شوف ماكس','',59,'','',search)
	addDir('3.  [COLOR FFC89008]KLA  [/COLOR]'+search+' - موقع كل العرب','',19,'','',search)
	addDir('4.  [COLOR FFC89008]PNT  [/COLOR]'+search+' - موقع بانيت','',39,'','',search)
	addDir('5.  [COLOR FFC89008]IFL    [/COLOR]'+search+' - موقع قناة اي فيلم','',29,'','',search)
	addDir('6.  [COLOR FFC89008]KWT  [/COLOR]'+search+' - موقع قناة الكوثر','',139,'','',search)
	addDir('7.  [COLOR FFC89008]MRF  [/COLOR]'+search+' - موقع قناة المعارف','',49,'','',search)
	addDir('8.  [COLOR FFC89008]FTM  [/COLOR]'+search+' - موقع المنبر الفاطمي','',69,'','',search)
	#addDir('[COLOR FFC89008]=========================[/COLOR]','',9999)
	addLink('[COLOR FFC89008]مواقع سيرفرات خاصة وعامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('9.   [COLOR FFC89008]MVZ  [/COLOR]'+search+' - موقع موفيز لاند','',189,'','',search)
	addDir('10. [COLOR FFC89008]AKM  [/COLOR]'+search+' - موقع اكوام','',79,'','',search)
	addDir('11. [COLOR FFC89008]EGB  [/COLOR]'+search+' - موقع ايجي بيست','',129,'','',search)
	addDir('12. [COLOR FFC89008]EG4  [/COLOR]'+search+' - موقع ايجي فور بيست','',229,'','',search)
	#addDir('[COLOR FFC89008]=========================[/COLOR]','',9999)
	addLink('[COLOR FFC89008]مواقع سيرفرات عامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('13. [COLOR FFC89008]HEL  [/COLOR]'+search+' - موقع هلال يوتيوب','',99,'','',search)
	addDir('14. [COLOR FFC89008]HLA  [/COLOR]'+search+' - موقع هلا سيما','',89,'','',search)
	addDir('15. [COLOR FFC89008]SHA  [/COLOR]'+search+' - موقع شاهد فوريو','',119,'','',search)
	addDir('16. [COLOR FFC89008]ARL  [/COLOR]'+search+' - موقع عرب ليونز','',209,'','',search)
	addDir('17. [COLOR FFC89008]SFW [/COLOR]'+search+' - موقع سيريس فور وتش','',219,'','',search)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TV_CHANNELS_MENU():
	addDir('1.  [COLOR FFC89008]TV0  [/COLOR]'+'قنوات من مواقعها الاصلية','',100)
	addDir('2.  [COLOR FFC89008]YUT  [/COLOR]'+'قنوات عربية من يوتيوب','',147)
	addDir('3.  [COLOR FFC89008]YUT  [/COLOR]'+'قنوات اجنبية من يوتيوب','',148)
	addDir('4.  [COLOR FFC89008]IFL    [/COLOR]'+'من موقع قناة اي فيلم','',28)
	#addDir('5.  [COLOR FFC89008]MRF  [/COLOR]'+'من موقع قناة المعارف','',41)
	#addDir('6.  [COLOR FFC89008]KWT  [/COLOR]'+'من موقع قناة الكوثر','',135)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addDir('5.  [COLOR FFC89008]TV1  [/COLOR]'+'قنوات تلفزونية خاصة','',101)
	addDir('6.  [COLOR FFC89008]TV2  [/COLOR]'+'قنوات تلفزونية للفحص','',102)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def VERSION():
	xbmcgui.Dialog().notification('جاري جمع المعلومات','الرجاء الانتظار')
	threads = CustomThread()
	threads.start_new_thread(1,False,KODI_VERSION)
	#	url = 'http://raw.githack.com/emadmahdi/KODI/master/addons.xml'
	#   url = 'https://github.com/emadmahdi/KODI/raw/master/addons.xml'
	url = 'https://raw.githubusercontent.com/emadmahdi/KODI/master/addons.xml'
	html = openURL_PROXY(url,'','','','PROGRAM-VERSION-1st')
	latest_ADDON_VER = re.findall('plugin.video.arabicvideos" name="Arabic Videos" version="(.*?)"',html,re.DOTALL)[0]
	current_ADDON_VER = xbmc.getInfoLabel('System.AddonVersion(plugin.video.arabicvideos)')
	latest_REPO_VER = re.findall('name="EMAD Repository" version="(.*?)"',html,re.DOTALL)[0]
	current_REPO_VER = xbmc.getInfoLabel('System.AddonVersion(repository.emad)')
	if latest_ADDON_VER > current_ADDON_VER:
		message1 = 'الرجاء تحديث البرنامج لحل المشاكل'
		message3 = '\n\n' + 'جرب اغلاق كودي وتشغيله وانتظر التحديث الاوتوماتيكي'
	else:
		message1 = 'لا توجد اي تحديثات للبرنامج حاليا'
		message3 = '\n\n' + 'الرجاء ابلاغ المبرمج عن اي مشكلة تواجهك'
	if current_REPO_VER=='': current_REPO_VER='لا يوجد'
	else: current_REPO_VER = ' ' + current_REPO_VER
	message2  = 'الاصدار الاخير للبرنامج المتوفر الان هو :   ' + latest_ADDON_VER
	message2 += '\n' + 'الاصدار الذي انت تستخدمه للبرنامج هو :   ' + current_ADDON_VER
	message2 += '\n' + 'الاصدار الاخير لمخزن عماد المتوفر الان هو :   ' + latest_REPO_VER
	message2 += '\n' + 'الاصدار الذي انت تستخدمه لمخزن عماد هو :  ' + current_REPO_VER
	message3 += '\n\n' + 'لكي يعمل التحديث الاوتوماتيكي يجب ان يكون لديك في كودي مخزن عماد EMAD Repository'
	message3 += '\n\n' + 'ملفات التنصيب مع التعليمات متوفرة على هذا الرابط'
	message3 += '\n' + 'https://github.com/emadmahdi/KODI'
	xbmcgui.Dialog().textviewer(message1,message2+message3)
	threads.wait_finishing_all_threads()
	return ''

def RANDOM():
	headers = { 'User-Agent' : '' }
	url = 'https://www.bestrandoms.com/random-arabic-words'
	payload = { 'quantity' : '5' }
	data = urllib.urlencode(payload)
	#xbmcgui.Dialog().ok('',str(data))
	html = openURL_PROXY(url,data,headers,'','PROGRAM-RANDOM-1st')
	#html = openURL_cached(NO_CACHE,url,data,headers,'','PROGRAM-RANDOM-1st')
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
	GLOBAL_SEARCH_MENU(search)
	return

def CLOSED():
	xbmcgui.Dialog().ok('','المبرمج يحتاج بعض الوقت لاصلاح هذا الموقع')
	return

def SSL_WARNING():
	xbmcgui.Dialog().ok('تحذير مهم','البرنامج لا يفحص شهادة التشفير عند الاتصال بالمواقع المشفرة ولهذا في حال وجود شهادة غير صحيحة او منتهية الصلاحية او مزيفة فان هذا لن يوقف الربط المشفر ولن يوقف عمل البرنامج')
	import PROBLEMS
	PROBLEMS.MAIN(193)
	return

def KODI_VERSION():
	#	https://kodi.tv/download/849
	#   https://play.google.com/store/apps/details?id=org.xbmc.kodi
	#	http://mirror.math.princeton.edu/pub/xbmc/releases/windows/win64
	#	http://mirrors.mit.edu/kodi/releases/windows/win64'
	url = 'http://mirrors.kodi.tv/releases/windows/win64/'
	html = openURL_cached(REGULAR_CACHE,url,'','','','PROGRAM-KODI_VERSION-1st')
	latest_KODI_VER = re.findall('title="kodi-(.*?)-',html,re.DOTALL)[0]
	current_KODI_VER = xbmc.getInfoLabel( "System.BuildVersion" ).split(' ')[0]
	message4a = 'الاصدار الاخير لكودي المتوفر الان هو :   ' + latest_KODI_VER
	message4b = 'الاصدار الذي انت تستخدمه لكودي هو :   ' + current_KODI_VER
	xbmcgui.Dialog().ok('كودي',message4a,message4b)
	return

def TEST_ALL_WEBSITES():
	#xbmcgui.Dialog().notification('جاري فحص','جميع المواقع')
	websites_keys = WEBSITES.keys()
	headers = { 'User-Agent' : '' }
	def test_all(type,proxy_url=''):
		def dummyFunc(site,type,proxy_url):
			if type=='proxy': url = WEBSITES[site][0]+'||MyProxyUrl='+proxy_url
			else: url = WEBSITES[site][0]
			if type=='direct': html = openURL_cached(NO_CACHE,url,'',headers,'','PROGRAM-TEST_ALL_WEBSITES-1st')
			elif type=='proxy': html = openURL_HTTPSPROXIES(url,'',headers,'','PROGRAM-TEST_ALL_WEBSITES-2nd')
			#if 'https' in url: html = '___Error___'
			#else: html = ''
			return html
		threads = CustomThread()
		for site in websites_keys:
			threads.start_new_thread(type+'_'+site,True,dummyFunc,site,type,proxy_url)
		threads.wait_finishing_all_threads()
		return threads.resultsDICT
	DIRECTdict_result = test_all('direct')
	type,messageDIRECT,proxyname,PROXYdict_result = 'direct','','',''
	for site in sorted(websites_keys):
		result = DIRECTdict_result[type+'_'+site]
		if '___Error___' not in result: messageDIRECT += site.lower()+'  '
		else: messageDIRECT += '[COLOR FFC89008]'+site.lower()+'[/COLOR]  '
	if '___Error___' in str(DIRECTdict_result):
		testedLIST,timingLIST = TEST_HTTPS_PROXIES()
		proxies_name,proxies_url = [],[]
		i = 0
		for id in testedLIST:
			proxies_name.append(PROXIES[id][0]+'   '+str(int(1000*timingLIST[i]))+'ms')
			proxies_url.append(PROXIES[id][1])
			i += 1
		selection = xbmcgui.Dialog().select(str(len(proxies_name))+' اختر بروكسي (الأسرع فوق)', proxies_name)
		if selection == -1: return
		else: 
			proxyname = proxies_name[selection].split('   ')[0]
			proxyurl = proxies_url[selection]
		type,messagePROXY = 'proxy',''
		PROXYdict_result = test_all('proxy',proxyurl)
		for site in sorted(websites_keys):
			result = PROXYdict_result[type+'_'+site]
			if '___Error___' not in result: messagePROXY += site.lower()+'  '
			else: messagePROXY += '[COLOR FFC89008]'+site.lower()+'[/COLOR]  '
	else: messagePROXY = 'جميع المواقع تعمل عندك والبرنامج لا يحتاج بروكسي'
	message  = '== المواقع البيضاء تعمل والحمراء لا تعمل =='
	message += '\n\n'+'== [COLOR FFC89008]فحص باستخدام شبكة الانترنيت الخاصة بك[/COLOR] =='
	message += '\n'+messageDIRECT.strip(' ')
	if proxyname!='': message += '\n\n'+'== [COLOR FFC89008]فحص باستخدام بروكسي موجود في '+proxyname+'[/COLOR] =='
	else: message += '\n\n'+'== [COLOR FFC89008]فحص باستخدام بروكسي ببلد وانترنيت مختلفة[/COLOR] =='
	message += '\n'+messagePROXY.strip(' ')
	xbmcgui.Dialog().textviewer('فحص جميع مواقع البرنامج',message)
	direct,proxy = '',''
	if '___Error___' in str(DIRECTdict_result): direct = 'problem'
	if '___Error___' in str(PROXYdict_result): proxy = 'problem'
	if direct=='problem' and proxy!='problem':
		xbmcgui.Dialog().ok('نتيجة فحص مواقع البرنامج','المشكلة التي عندك في بعض المواقع قد اختفت باستخدام بروكسي وهذا معناه ان المشكلة من طرفك وليست من البرنامج. حاول حل مشكلتك اما باستخدام DNS أو Proxy أو VPN')
	elif direct=='problem' and proxy=='problem':
		xbmcgui.Dialog().ok('نتيجة فحص مواقع البرنامج','مشكلتك ظهرت مع بروكسي وبدون بروكسي وسببها اما من الموقع الاصلي أو البرنامج أو البروكسي الذي انت اخترته. جرب اعادة الفحص باختيار بروكسي مختلف وارسل سجل الاخطاء للمبرمج (من قائمة خدمات البرنامج)')		
	elif direct!='problem':
		xbmcgui.Dialog().ok('نتيجة فحص مواقع البرنامج','جميع المواقع تعمل عندك بدون مشكلة وهذا معناه ان جهازك لا يحتاج اي تعديلات. فاذا كانت لديك مشكلة في البرنامج فقم بارسال سجل الاخطاء الى المبرمج (من قائمة خدمات البرنامج)')
	return

def TESTINGS():
	url = 'https://intoupload.net/w2j4lomvzopd'
	import urlresolver
	try:
		#resolvable = urlresolver.HostedMediaFile(url).valid_url()
		link = urlresolver.HostedMediaFile(url).resolve()
		#xbmcgui.Dialog().ok(str(link),url)
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
