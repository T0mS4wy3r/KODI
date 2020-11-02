# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from LIBRARY import *

script_name='SERVICES'

def MAIN(mode,text=''):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==  0: ARABIC_KEYBOARD(text)
	elif mode==  2: SEND_MESSAGE(text)
	elif mode==  3: DMCA()
	elif mode==  4: HTTPS_TEST(text)
	elif mode==  5: INPUTSTREAM_ADAPTIVE_SETTINGS()
	elif mode==  6: KODI_INTERFACE_SETTINGS()
	elif mode==  7: VERSIONS()
	elif mode==  9: DELETE_CACHE()
	elif mode==150: USING_FAVOURITES()
	elif mode==151: NO_ARABIC_FONTS()
	elif mode==152: HTTPS_FAILED()
	elif mode==153: LINKS_NOT_WORKING()
	elif mode==154: NO_FORIGN_LANGUAGE_VIDEOS()
	elif mode==155: SLOW_LINKS()
	elif mode==156: UNKNOWN_SERVERS()
	elif mode==157: PRIVATE_PUBLIC_SERVERS()
	elif mode==158: SLOW_VIDES()
	elif mode==159: CHECK_FOR_ADDONS_UPDATES()
	elif mode==170: DELETE_FAVOURITES_AND_LAST_MENUS()
	elif mode==171: SSL_WARNING()
	elif mode==172: INSTALL_REPOSITORY(True)
	elif mode==173: ENABLE_MPD()
	elif mode==174: ENABLE_RTMP()
	elif mode==175: TEST_ALL_WEBSITES()
	elif mode==176: ANALYTICS_REPORT()
	elif mode==177: RESOLVEURL_SETTINGS()
	elif mode==178: YOUTUBE_DL_SETTINGS()
	elif mode==179: TESTINGS()
	elif mode==190: WHAT_IS_CACHE()
	elif mode==191: WHAT_DOT_COMMA_MEANS()
	elif mode==192: SOLVE_TEMP_PROBLEM()
	elif mode==193: WHY_IGNORE_SSL_CERTIFICATE()
	elif mode==194: MPD_NOT_WORKING()
	elif mode==195: WEBSITES_BLOCKED()
	elif mode==196: CONTACT_ME()
	elif mode==197: KODI_SKIN()
	elif mode==198: KODI_REMOTE_CONTROL()
	elif mode==199: CHANGELOG()
	elif mode==340: SHOW_LOGFILE()
	elif mode==341: KODIEMAD_WEBSITE()
	elif mode==342: ALLOW_AUTO_PROXY()
	return

def ALLOW_AUTO_PROXY():
	settings = xbmcaddon.Addon(id=addon_id)
	status = settings.getSetting('proxy.status')
	if status=='ENABLED': staus = 'البروكسي الأوتوماتيكي يعمل'
	else: staus = 'البروكسي الأوتوماتيكي متوقف'
	yes = XBMCGUI_DIALOG_YESNO(staus,'البروكسي هو جهاز بالإنترنيت يعمل وسيط بين جهازك والإنترنيت . هو يستلم طلباتك ويقوم بسحبها بدلا منك ثم يبعثها لك . هل تريد تشغيل أم إيقاف البروكسي ؟','','','تشغيل','إيقاف')
	if yes: settings.setSetting('proxy.status','DISABLED')
	else: settings.setSetting('proxy.status','ENABLED')
	return

def ARABIC_KEYBOARD(text):
	if text!='':
		text = mixARABIC(text)
		text = text.decode('utf8').encode('utf8')
		window_id = 10103
		#xbmc.log('EMAD222::   window_id: ['+str(window_id)+']', level=xbmc.LOGNOTICE)
		window = xbmcgui.Window(window_id)
		window.getControl(311).setLabel(text)
		#xbmc.log('EMAD333::   text: ['+text+']', level=xbmc.LOGNOTICE)
		#dialog = xbmcgui.WindowXMLDialog('DialogKeyboard22.xml', xbmcaddon.Addon().getAddonInfo('path').decode('utf-8'),'Default','720p')
		#dialog.show()
		#dialog.getControl(99991).setPosition(0,0)
		#dialog.getControl(311).setLabel(text)
		#dialog.getControl(5).setText(logfileNEW)
		#width = xbmcgui.getScreenWidth()
		#height = xbmcgui.getScreenHeight()
		#resolution = (0.0+width)/height
		#dialog.getControl(5).setWidth(width-180)
		#dialog.getControl(5).setHeight(height-180)
		#dialog.doModal()
		#del dialog
	return

def CHECK_LOGLINE(line):
	if "extension '' is not currently supported" in line: return True
	if 'Checking for Malicious scripts' in line: return True
	#if 'Previous line repeats' in line: return True
	if 'PVR IPTV Simple Client' in line: return True
	if 'this hash function is broken' in line: return True
	if 'uses plain HTTP for add-on downloads' in line: return True
	if 'NOTICE: ADDON:' in line and line.endswith('installed\n'): return True
	return False

def SHOW_LOGFILE():
	new = XBMCGUI_DIALOG_YESNO('حدد السجل المطلوب للقراءة والفحص','السجل القديم هو الذي كان يستخدمه كودي قبل آخر إطفاء لبرنامج كودي . والسجل الجديد هو السجل الذي يستخدمه كودي الآن وهو السجل الأفضل والمطلوب قراءته وفحصه','','','السجل القديم','سجل الأخطاء')
	if new: logfilename = logfile
	else: logfilename = oldlogfile
	dataNEW,counts = [],0
	size = os.path.getsize(logfilename)
	f = open(logfilename,'rb')
	if size>150000: f.seek(-150000,os.SEEK_END)
	data = f.readlines()
	f.close()
	#XBMCGUI_DIALOG_OK(str(size),str(len(data)))
	limit = 74999999
	for line in reversed(data):  # reversed needed to get the last 100 lines in the log file
		line = line.replace('============================================================================================_','=========================')
		#line = '0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz'
		ignore = CHECK_LOGLINE(line)
		if not ignore:
			#LOG_THIS('NOTICE',line)
			line = line.replace('    ','')
			count = 1+len(line)/limit
			text = ''
			for i in range(count): text = text+line[i*limit+i:i*limit+i+limit+1]+' '
			line_start = re.findall('^\d+-\d+-\d+ \d+:\d+:\d+\.\d+ T:\d+',text)
			if not line_start: line_start = re.findall('^\d+:\d+:\d+\.\d+ T:\d+',text)
			if line_start: text = text.replace(line_start[0],'[COLOR FFC89008]'+line_start[0]+'[/COLOR]')
			dataNEW.append(text)
			counts += 1
			if counts==200: break
	dataNEW = reversed(dataNEW)   # reversed needed to get the last 100 lines in the log file
	logfileNEW = ''.join(dataNEW)
	logfileNEW = logfileNEW.replace('    ','')
	logfileNEW = logfileNEW.replace('ERROR:','[COLOR FFFF0000]ERROR:[/COLOR]')
	logfileNEW = logfileNEW.replace('=========================','[COLOR FFFFFF00]=========================[/COLOR]')
	#logfileNEW = logfileNEW.replace('\r','').replace('\n\n','\n').replace('\n\n','\n')
	#logfileNEW = logfileNEW.replace('\n','%').replace('\r','$')
	#testing = '00 11 22 33 44 55 66 77 88 99 00 11 22 33 44 55 66 77 88 99 00 11 22 33 44 55 66 77 88 99'
	#testing = '0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz'
	#XBMCGUI_DIALOG_TEXTVIEWER('آخر أسطر سجل الأخطاء والاستخدام',logfileNEW)
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN('آخر أسطر سجل الأخطاء والاستخدام',logfileNEW,'small','left')
	return

def CHANGELOG():
	with open(changelogfile,'r') as f: changelog = f.read()
	changelog = changelog.replace('\t','        ')
	versions = re.findall('(v\d.*?)[\n\r]',changelog)
	for line in versions:
		changelog = changelog.replace(line,'[COLOR FFFFFF00]'+line+'[/COLOR]')
	XBMCGUI_DIALOG_TEXTVIEWER('التغييرات الأخيرة في البرامج',changelog)
	return

def KODI_REMOTE_CONTROL():
	message1 = 'بعض الأزرار على الريموت كونترول توفر إمكانية تقديم وتأخير الفيديو وهذه الأزرار هي الأسهم والأرقام مع بعض وكالتالي'
	message2 = 'لتقديم الفيديو استخدم السهم اليمين ولتأخيره استخدم السهم اليسار . أما عدة اسهم متتالية فهذه تقوم بتحريك الفيديو بوقت اكبر من وقت السهم الواحد . أما السهم الأعلى والأسفل فهو يحرك الفيديو إلى الأمام أو إلى الوراء ولكن بقفزة كبيرة'
	message3 = 'أما الأرقام فهي تستخدم للتقديم والتأخير ولكن بمقدار عدد الثواني والدقائق . مثلا رقم 544 تعني 5 دقائق و 44 ثانية إلى الأمام أو إلى الوراء بحسب استخدامك للسهم اليمين أو سهم اليسار'
	message = message1+': '+message2+' . '+message3
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN('رسالة من المبرمج',message,'big','right')
	return

def SEND_EMAIL(subject,message,showDialogs=True,url='',source='',text=''):
	if '_PROBLEM_' in text: problem = True
	else: problem = False
	sendit,html = 1,''
	if showDialogs:
		sendit = XBMCGUI_DIALOG_YESNO('هل ترسل هذه الرسالة إلى المبرمج',message.replace('\\n','\n'),'','','كلا','نعم')
		if sendit==0: 
			XBMCGUI_DIALOG_OK('رسالة من المبرمج','تم إلغاء الإرسال بناء على طلبك')
			return ''
	if sendit==1:
		#addon_version = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
		kodiName = xbmc.getInfoLabel( "System.FriendlyName" )
		message = message+' \\n\\n==== ==== ==== \\nAddon Version: '+addon_version+' :\\nEmail Sender: '+dummyClientID(32)+' :\\nKodi Version: '+kodi_release+' :\\nKodi Name: '+kodiName
		#xbmc.sleep(4000)
		#playerTitle = xbmc.getInfoLabel( "Player.Title" )
		#playerPath = xbmc.getInfoLabel( "Player.Filenameandpath" )
		#if playerTitle != '': message += ' :\\nPlayer Title: '+playerTitle
		#if playerPath != '': message += ' :\\nPlayer Path: '+playerPath
		#XBMCGUI_DIALOG_OK(playerTitle,playerPath)
		if url != '': message += ' :\\nURL: ' + url
		if source != '': message += ' :\\nSource: ' + source
		message += ' :\\n'
		if showDialogs: XBMCGUI_DIALOG_NOTIFICATION('جاري ألإرسال','الرجاء الانتظار')
		logfileNEW = ''
		if problem:
			dataNEW,counts = [],0
			#logfile = 'S://DOWNLOADS/6ac26462c99fc35816f3532bb17608f4-5.8.1.log'
			size = os.path.getsize(logfile)
			f = open(logfile,'rb')
			if size>600000: f.seek(-600000,os.SEEK_END)
			data = f.readlines()
			for line in reversed(data):
				ignore = CHECK_LOGLINE(line)
				if not ignore:
					dataNEW.append(line)
					counts += 1
					if counts==1000: break
			dataNEW = reversed(dataNEW)
			logfileNEW = ''.join(dataNEW)
			#logfileNEW = ''.join(dataNEW[-1000:])
			#logfileNEW = logfileNEW[:102400]
			#logfileNEW = quote(logfileNEW)
			logfileNEW = base64.b64encode(logfileNEW)
		url = WEBSITES['PYTHON'][2]
		payload = { 'subject' : subject , 'message' : message , 'logfile' : logfileNEW }
		#logfileNEW = base64.b64decode(logfileNEW)
		#with open('S:\\00emad.log','w') as f: f.write(logfileNEW)
		response = openURL_requests_cached(NO_CACHE,'POST',url,payload,'','','','SERVICES-SEND_EMAIL-1st')
		html = response.content
		result = html[0:6]
		if showDialogs:
			if result == 'Error ':
				XBMCGUI_DIALOG_NOTIFICATION('للأسف','فشل في الإرسال')
				XBMCGUI_DIALOG_OK('رسالة من المبرمج','خطأ وفشل في إرسال الرسالة')
			else:
				XBMCGUI_DIALOG_NOTIFICATION('تم الإرسال','بنجاح')
				XBMCGUI_DIALOG_OK('Message sent','تم إرسال الرسالة بنجاح')
	return html

def NO_ARABIC_FONTS():
	message1 = '1.   If you can\'t see Arabic Letters then go to "Kodi Interface Settings" and change the font to "Arial"'
	message2 = '1.   إذا لم تستطع رؤية الأحرف العربية فغير الخط المستخدم إلى "Arial" من إعدادات واجهة كودي'
	XBMCGUI_DIALOG_OK('Arabic Problem',message1,message2)
	message1 = '2.   If you don\'t find "Arial" font in kodi skin then change skin in "Kodi Interface Settings"'
	message2 = '2.   إذا لم تجد الخط "Arial" فإدن عليك أن تذهب إلى إعدادات كودي وتغير واجهة كودي المستخدمة'
	XBMCGUI_DIALOG_OK('Font Problem',message1,message2)
	yes = XBMCGUI_DIALOG_YESNO('Font settings','Do you want to go to "Kodi Interface Settings" now?','هل تريد الذهاب إلى لوحة إعدادات واجهة كودي ألآن؟')
	if yes==1: xbmc.executebuiltin("ActivateWindow(InterfaceSettings)")
	return

def LINKS_NOT_WORKING():
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','غالبا السبب هو من الموقع الأصلي المغذي للبرنامج وللتأكد قم بتشغيل الرابط الذي لا يعمل ثم قم بإرسال مشكلة إلى المبرمج من القائمة الرئيسية للبرنامج')
	return

def NO_FORIGN_LANGUAGE_VIDEOS():
	message = 'هذا البرنامج مخصص فقط للغة العربية ولكن هذا لا يمنع وجود مواقع فيها أفلام ومسلسلات مترجمة أو مدبلجة إلى اللغة العربية والى لغات اخرى ولا يوجد سبب للتكرار'
	XBMCGUI_DIALOG_OK('رسالة من المبرمج',message)
	return

def SLOW_LINKS():
	message = 'الروابط البطيئة لا علاقة لها بالبرنامج وغالبا السبب هو من الموقع الأصلي المغذي للبرنامج'
	XBMCGUI_DIALOG_OK('رسالة من المبرمج',message)
	return

def UNKNOWN_SERVERS():
	message = 'هي سيرفرات لا يستطيع البرنامج استخدامها بسبب كونها محمية من المصدر أو بحاجة إلى اشتراك رسمي أو جديدة أو لا يعرفها البرنامج'
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','سيرفرات سيئة أو مجهولة',message)
	return

def PRIVATE_PUBLIC_SERVERS():
	message = 'السيرفرات العامة هي سيرفرات خارجية وغير جيدة لان الكثير منها ممنوع أو محذوف أو خطأ بسبب حقوق الطبع وحقوق الألفية الرقمية ولا توجد طريقة لفحصها أو إصلاحها \n\n السيرفرات الخاصة هي سيرفرات يتحكم فيها الموقع الأصلي وهي جيدة نسبيا ولا توجد طريقة لفحصها أو إصلاحها \n\n الرجاء قبل الإبلاغ عن مشكلة وقبل مراسلة المبرمج افحص نفس الفيديو وافحص نفس السيرفر على الموقع الأصلي'
	XBMCGUI_DIALOG_TEXTVIEWER('رسالة من المبرمج',message)
	return

def SLOW_VIDES():
	message1 = 'ابتعد عن ملفات الدقة العالية'
	message2 = 'ابتعد عن ملفات أل m3u8'
	message3 = 'ابتعد عن ملفات التحميل والداونلود download'
	XBMCGUI_DIALOG_OK('رسالة من المبرمج',message1,message2,message3)
	return

def WHAT_IS_CACHE():
	message2 = 'الكاش هو مخزن مؤقت للمعلومات يستخدمه البرنامج لخزن صفحات الإنترنيت وروابط الفيديوهات'
	message2 += ' ' + 'للوصول إليها بسرعة وبدون إنترنيت والبرنامج يمسحها أوتوماتيكيا بعد انتهاء وقتها وأيضا عند تحديث البرنامج والكاش في البرنامج هو ثلاثة أنواع'
	message2 += '\n\n' + 'جدا طويل المدى للصفحات الثابتة ومدته ' + str(VERY_LONG_CACHE/60/60/24) + ' يوم'
	message2 += '\n' + 'طويل المدى للصفحات التي نادرا تتغير ومدته ' + str(LONG_CACHE/60/60/24) + ' يوم'
	message2 += '\n' + 'متوسط المدى للصفحات التي قد تتغير ومدته ' + str(REGULAR_CACHE/60/60) + ' ساعة'
	message2 += '\n' + 'قصير المدى للصفحات التي تتغير دائما ومدته ' + str(SHORT_CACHE/60/60) + ' ساعة'
	message2 += '\n' + 'جدا قصير المدى للصفحات التي تتغير كثيرا ومدته ' + str(VERY_SHORT_CACHE/60) + ' دقيقة'
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN('ما هو الكاش المستخدم في البرنامج',message2,'big','right')
	return

def WHAT_DOT_COMMA_MEANS():
	message = 'الفاصلة تعني مجلد بنفس اسمه الأصلي والنقطة تعني أن الاسم الأصلي تم تعديله وفاصلة ونقطة تعنى مجلد وتم تعديل اسمه وبدون علامة تعني ملف بنفس اسمه الأصلي'
	XBMCGUI_DIALOG_OK('رسالة من المبرمج',message)
	return

def SOLVE_TEMP_PROBLEM():
	message = 'إذا واجهتك مشكلة في الشبكة وتم حلها ... أو انك تظن أن الموقع الأصلي كان فيه مشكلة مؤقته وتم حلها ... فإذن جرب مسح كاش البرنامج لكي يقوم البرنامج بطلب الصفحة الصحيحة وتخزينها بدلا من الصفحة القديمة'
	XBMCGUI_DIALOG_OK('رسالة من المبرمج',message)
	return

def WHY_IGNORE_SSL_CERTIFICATE():
	message = 'الغرض من شهادة التشفير هو ضمان صحة وسرية المعلومات المتبادلة بين البرنامج والموقع المشفر وهذا الضمان غير مطلوب ولا حاجة له عند الاتصال او الربط مع مواقع الفيديوهات المشفرة'
	XBMCGUI_DIALOG_OK('رسالة من المبرمج',message)
	return

def MPD_NOT_WORKING():
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','يجب تفعيل إضافة اسمها inputstream.adaptive لكي يعمل هذا النوع من الفيديوهات')
	ENABLE_MPD()
	return

def WEBSITES_BLOCKED():
	message  = 'مؤخرا قامت بعض شركات الأنترنيت الدولي بوضع عائق ضد البرامج مثل كودي لتسمح فقط لبعض مستخدمي المتصفح بالدخول لمواقع الفيديو'
	#message += '\n[COLOR FFC89008]وهذا العائق هو reCAPTCHA الخاص بشركة جوجل[/COLOR]\n'
	#message += 'والذي صنعته شركة جوجل خصيصا لمنع برامج مثل كودي من تصفح الأنترنيت'
	message += ' ونتيجة لهذا العائق فانه تقريبا جميع مستخدمي برنامج كودي لا يستطيعون الدخول لجميع مواقع البرنامج حتى مع استخدام'
	message += '\n[COLOR FFC89008]ـ  VPN  أو  Proxy  أو  DNS  أو أي حل بسيط آخر[/COLOR]\n'
	message += '\nلان هذا لن يحل المشكلة وإنما فقط سيقوم بإصلاح بعض المواقع وإعاقة مواقع اخرى كانت تعمل سابقا بدون مشاكل'
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN('رسالة من المبرمج',message,'big','right')
	message = 'المواقع التي تأثرت بالعائق عند بعض الناس هي:'
	message += '\n'+'[COLOR FFC89008]akoam  egybest  egybestvip  movizland  series4watch  shahid4u[/COLOR]'
	message += '\n\n'+'الدول التي تأثرت بالعائق عند بعض الناس هي:'
	message += '\n'+'[COLOR FFC89008]مصر  الكويت  أميركا  كندا  فرنسا  اليونان  بريطانيا الإمارات ألمانيا روسيا اليابان السعودية رومانيا هولندا[/COLOR]'
	message += '\n\n'+'المبرمج وجد طريقة لتجاوز العائق ولكنها تحتاج جهد كبير والمبرمج يظن المشكلة صغيرة ولا تستحق التعب فإذا لديك مشكلة بالدخول لبعض المواقع وأيضا لكي يتضح حجم المشكلة '
	message += '[COLOR FFC89008]ارسل رسالة مؤدبة إلى المبرمج واكتب فيها اسم بلدك وأسماء المواقع التي لا تستطيع دخولها[/COLOR]'
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN('رسالة من المبرمج',message,'big','right')
	#SEND_MESSAGE('IsProblem=False')
	#message = '\n\n'+'ولقد لاحظنا ايضا أن المواقع المعاقة تختلف باختلاف البلد وتختلف باختلاف شركة الانترنيت في ذلك البلد وهذا معناه انه حتى لو تم استخدام VPN أو Proxy أو أي وسيلة اخرى فان المواقع المعاقة سوف تختلف ولكنها لن تعمل جميعها'
	#message += 'لحل المشكلة قم بعملين:    الأول: أرسل سجل الأخطاء والاستخدام إلى المبرمج (من قائمة خدمات البرنامج) واكتب معه اسم بلدك واسم شركة الإنترنيت وأسماء المواقع التي لا تعمل عندك'
	#message += '\n\n'+'والثاني: جرب استخدام VPN وعند البعض قد تحتاج فقط تغيير DNS والأحسن أن يكون في بلد اخر علما ان استخدام Proxy قد يحل مشكلة بعض المواقع ولكن ليس في جميع الدول'
	#XBMCGUI_DIALOG_TEXTVIEWER('مشكلة عند بعض الناس',message)
	#yes = XBMCGUI_DIALOG_YESNO('فحص جميع مواقع البرنامج','هذا الفحص هو لمعرفة هل المشكلة من عندك ام من البرنامج. سيقوم البرنامج الآن بفحص مواقعه مرتين الأولى بوضعك الطبيعي والثانية باستخدام بروكسي مجاني انت تختاره من القائمة التي ستظهر لاحقا. هل تريد الاستمرار؟','','','كلا','نعم')
	#if yes==1:
	#TEST_ALL_WEBSITES()
	return

def CONTACT_ME():
	XBMCGUI_DIALOG_OK('ثلاث طرق للتواصل مع المبرمج','استخدم فيسبوك "الحاج عماد مهدي" أو أرسل رسالة أو مشكلة من قائمة خدمات البرنامج أو افتح نقاش بواحد من هذه الروابط','https://github.com/emadmahdi/KODI/issues')
	return

def DELETE_CACHE():
	#WHAT_IS_CACHE()
	yes = XBMCGUI_DIALOG_YESNO('هل تريد مسح جميع الكاش ؟','الكاش يعمل على تسريع عمل البرنامج ومسحه يسبب إعادة طلب جميع الصفحات من الأنترنيت عند الحاجة إليها والمسح ليس فيه أي ضرر وبالعكس فان المسح ممكن أن يحل بعض مشاكل البرنامج','','','كلا','نعم')
	if yes:
		CLEAN_KODI_CACHE_FOLDER()
		XBMCGUI_DIALOG_OK('تم مسح كاش البرنامج بالكامل','إذا كانت عندك مشكلة في احد المواقع فجرب الموقع الآن ... وأدا المشكلة مستمرة فإذن ارسل المشكلة إلى المبرمج')
	return yes

def HTTPS_TEST(showDialogs=True):
	if showDialogs=='': showDialogs = True
	#XBMCGUI_DIALOG_OK(str(showDialogs),str(showDialogs))
	html = openURL_cached(NO_CACHE,'https://example.com','','',False,'LIBRARY-HTTPS-1st')
	if '___Error___' in html:
		worked = False
		LOG_THIS('ERROR',LOGGING(script_name)+'   HTTPS Failed   Label:['+menu_label+']   Path:['+menu_path+']')
		if showDialogs: XBMCGUI_DIALOG_OK('رسالة من المبرمج','فحص الاتصال المشفر ... مشكلة ... الاتصال المشفر (الربط المشفر) لا يعمل عندك على كودي ... وعندك كودي غير قادر على استخدام المواقع المشفرة')
	else:
		worked = True
		if showDialogs: XBMCGUI_DIALOG_OK('رسالة من المبرمج','فحص الاتصال المشفر ... جيد جدا ... الاتصال المشفر (الربط المشفر) يعمل عندك والبرنامج قادر على استخدام المواقع المشفرة')
	if not worked and showDialogs: HTTPS_FAILED()
	return

def HTTPS_FAILED():
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','بعض المواقع تحتاج ربط مشفر وقد يكون جهازك غير قادر على الربط المشفر أو هناك مشكلة في شهادة التشفير الخاصة بكودي عندك علما انه تم فحص البرنامج على كودي الإصدارات \r\n 17.6  &  18.[0-7]')
	#message2 = 'شهادة التشفير هي ملف يحتوي على شفرة خاصة أو تواقيع خاصة لشركات معروفة وله تاريخ صلاحية ونفاذ والغرض منه هو تبادل المعلومات بطريقة مشفرة يصعب اختراقها وفهمها'
	#XBMCGUI_DIALOG_OK('شهادة التشفير - SSL Certificate',message2)
	LATEST_KODI()
	return

def SEND_MESSAGE(text=''):
	if '_PROBLEM_' in text: problem = True
	else:
		problem = False
		yes = XBMCGUI_DIALOG_YESNO('','هل تريد أن ترسل رسالة أم تريد أن ترسل مشكلة ؟','','','إرسال رسالة','إرسال مشكلة')
		if yes==1: problem = True
	if problem:
		#yes = DELETE_CACHE()
		#if yes==1: return ''
		logs = XBMCGUI_DIALOG_YESNO('إرسال سجل الأخطاء والاستخدام','هل تريد إرسال سجل الأخطاء والاستخدام إلى المبرمج لكي يستطيع المبرمج معرفة المشكلة وإصلاحها','','','كلا','نعم')
		if logs==0:
			XBMCGUI_DIALOG_OK('تم إلغاء الإرسال','للأسف بدون سجل الأخطاء والاستخدام المبرمج لا يستطيع معرفة المشكلة ولا حلها لان المبرمج لا يعلم الغيب')
			return ''
		logs2 = XBMCGUI_DIALOG_YESNO('وضع المشكلة في السجل','قبل إرسال السجل عليك أن تقوم بتكرار الفعل الذي أعطاك المشكلة لكي يتم تسجيل هذه المشكلة في سجل الأخطاء والاستخدام قبل إرسال السجل للمبرمج . هل قمت قبل قليل بهذا العمل ؟','','','كلا','نعم')
		if logs2==0:
			XBMCGUI_DIALOG_OK('تم إلغاء الإرسال','للأسف بدون تسجيل المشكلة في سجل الأخطاء والاستخدام فان المبرمج لا يستطيع معرفة المشكلة ولا حلها لان المبرمج لا يعلم الغيب')
			return ''
		"""
		else:
			text += 'logs=yes'
			yes = XBMCGUI_DIALOG_YESNO('هل تريد الاستمرار ؟','قبل ارسال سجل الاخطاء والاستخدام إلى المبرمج عليك ان تقوم بتشغيل الفيديو او الرابط الذي يعطيك المشكلة لكي يتم تسجيل المشكلة في سجل الاخطاء والاستخدام. هل تريد الارسال الان ؟','','','كلا','نعم')
			if yes==0:
				XBMCGUI_DIALOG_OK('','تم الغاء الارسال')
				return ''
		XBMCGUI_DIALOG_OK('المبرمج لا يعلم الغيب','اذا كانت لديك مشكلة فالرجاء قراءة قسم المشاكل والاسئلة واذا لم تجد الحل هناك فحاول كتابة جميع تفاصيل المشكلة لان المبرمج لا يعلم الغيب')
		"""
	XBMCGUI_DIALOG_OK('كتابة وشرح الموضوع للمبرمج','في الشاشة القادمة حاول أن تكتب رسالة إلى المبرمج واشرح فيها المشكلة أو الموضوع وإذا أردت جواب من المبرمج فإذن أكتب عنوان بريدك ألإلكتروني الايميل وتذكر ولا تنسى أن المبرمج لا يعلم الغيب')
	search = KEYBOARD('Write a message   اكتب رسالة')
	if search=='': return ''
	message = search
	subject = 'Message: From Arabic Videos'
	if problem: text = '_PROBLEM_'
	result = SEND_EMAIL(subject,message,True,'','EMAIL-FROM-USERS',text)
	#	url = 'my API and/or SMTP server'
	#	payload = '{"api_key":"MY API KEY","to":["me@email.com"],"sender":"me@email.com","subject":"From Arabic Videos","text_body":"'+message+'"}'
	#	#auth=("api", "my personal api key"),
	#	import requests
	#	response = requests.request('POST',url, data=payload, headers='', auth='')
	#	response = requests.post(url, data=payload, headers='', auth='')
	#	if response.status_code == 200:
	#		XBMCGUI_DIALOG_OK('','تم الإرسال بنجاح')
	#	else:
	#		XBMCGUI_DIALOG_OK('خطأ في الإرسال','Error {}: {!r}'.format(response.status_code, response.content))
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
	#	XBMCGUI_DIALOG_OK('Response',str(response))
	return ''

def DMCA():
	text = 'هذا البرنامج لا يوجد له أي سيرفر يستضيف أي محتويات. البرنامج يستخدم روابط وتضمين لمحتويات مرفوعة على سيرفرات خارجية. البرنامج غير مسؤول عن أي محتويات تم تحميلها على سيرفرات ومواقع خارجية "مواقع طرف ثالث". جميع الأسماء والماركات والصور والمنشورات هي خاصة باصحابها. البرنامج لا ينتهك حقوق الطبع والنشر وقانون الألفية للملكية الرقمية DMCA إذا كان لديك شكوى خاصة بالروابط والتضامين الخارجية فالرجاء التواصل مع إدارة هذه السيرفرات والمواقع الخارجية. هذا البرنامج هو ببساطة متصفح لمواقع الويب'
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN('حقوق الطبع والنشر وقانون الألفية للملكية الرقمية',text,'big','right')
	text = 'This program does not host any content on any server. It only uses links to embedded content that was uploaded to popular online video hosting sites. All trademarks, videos, trade names, service marks, copyrighted work, logos referenced herein belong to their respective owners / companies. The program is not responsible for what other people upload to 3rd party sites. We urge all copyright owners, to recognize that the links contained within this program are located somewhere else on the web or video embedded are from other various sites. If you have any legal issues please contact appropriate media file owners / hosters. This program is simply a web browser.'
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN('Digital Millennium Copyright Act (DMCA)',text,'big','left')
	return

def VERSIONS():
	#BUSY_DIALOG('start')
	#url = 'http://raw.githack.com/emadmahdi/KODI/master/addons.xml'
	#url = 'https://gitee.com/emadmahdi/KODI/raw/master/addons.xml'
	#XBMCGUI_DIALOG_NOTIFICATION('جاري جمع المعلومات','الرجاء الانتظار')
	latest_REPO_VER,latest_ADDON_VER = LATEST_EMAD_VERSIONS()
	current_ADDON_VER = addon_version
	current_REPO_VER = xbmc.getInfoLabel('System.AddonVersion(repository.emad)')
	if latest_ADDON_VER>current_ADDON_VER or latest_REPO_VER>current_REPO_VER:
		need_update = True
		message1 = 'الرجاء تحديث إضافات كودي لحل المشاكل'
		message3 = '\n\n' + 'انت بحاجة لتحديث هذا البرنامج أو تحديث مخزن عماد'
	else:
		need_update = False
		message1 = 'لا توجد تحديثات للبرنامج أو المخزن حاليا'
		message3 = '\n\n' + 'الرجاء إبلاغ المبرمج عن المشكلة التي تواجهك'
	if current_REPO_VER=='': current_REPO_VER='لا يوجد'
	else: current_REPO_VER = ' ' + current_REPO_VER
	message2  = 'الإصدار الأخير للبرنامج المتوفر الآن هو :   ' + latest_ADDON_VER
	message2 += '\n' + 'الإصدار الذي انت تستخدمه للبرنامج هو :   ' + current_ADDON_VER
	message2 += '\n' + 'ألإصدار الأخير لمخزن عماد المتوفر الآن هو :   ' + latest_REPO_VER
	message2 += '\n' + 'ألإصدار الذي انت تستخدمه لمخزن عماد هو :  ' + current_REPO_VER
	message3 += '\n\n' + 'لكي يعمل عندك التحديث الأوتوماتيكي ... يجب أن يكون لديك في كودي مخزن عماد EMAD Repository'
	message3 += '\n\n' + 'الموقع الرسمي الجديد للبرنامج وفيه ملف تثبيت تطبيق كودي عماد تجده في الرابط'
	message3 += '\n' + '[COLOR FFFFFF00]http://tiny.cc/kodiemad[/COLOR]'
	message3 += '\n\n' + 'ملفات التثبيت القديمة وملفات البرمجة تجدها في هذه الروابط'
	message3 += '\n' + '[COLOR FFFFFF00]https://github.com/emadmahdi/KODI[/COLOR]'
	#message3 += '\n' + '[COLOR FFFFFF00]https://gitee.com/emadmahdi/KODI[/COLOR]'
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN(message1,message2+message3,'big','right')
	#threads22 = CustomThread()
	#threads22.start_new_thread('22',LATEST_KODI)
	#XBMCGUI_DIALOG_NOTIFICATION('thread submitted','')
	#time.sleep(5)
	LATEST_KODI()
	#BUSY_DIALOG('stop')
	if need_update:
		INSTALL_REPOSITORY(False)
		CHECK_FOR_ADDONS_UPDATES()
	#time.sleep(5)
	#LATEST_KODI()
	#threads22.wait_finishing_all_threads()
	return

def SSL_WARNING():
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','البرنامج لا يفحص شهادة التشفير عند الاتصال بالمواقع المشفرة ولهذا في حال وجود شهادة غير صحيحة أو منتهية الصلاحية أو مزيفة فان هذا لن يوقف الربط المشفر ولن يوقف عمل البرنامج')
	WHY_IGNORE_SSL_CERTIFICATE()
	return

def LATEST_KODI():
	#	https://kodi.tv/download/849
	#   https://play.google.com/store/apps/details?id=org.xbmc.kodi
	#	http://mirror.math.princeton.edu/pub/xbmc/releases/windows/win64
	#	http://mirrors.mit.edu/kodi/releases/windows/win64'
	url = 'http://mirrors.kodi.tv/releases/windows/win64/'
	#xbmc.log('ZZZZ: 1111:', level=xbmc.LOGNOTICE)
	html = openURL_cached(REGULAR_CACHE,url,'','','','SERVICES-LATEST_KODI-1st')
	#html = openURL_requests(url,'','','','SERVICES-LATEST_KODI-1st')
	#xbmc.log('ZZZZ: 2222:', level=xbmc.LOGNOTICE)
	latest_KODI_VER = re.findall('title="kodi-(.*?)-',html,re.DOTALL)[0]
	#xbmc.log('ZZZZ: 3333:', level=xbmc.LOGNOTICE)
	current_KODI_VER = str(kodi_version)
	#xbmc.log('ZZZZ: 4444:', level=xbmc.LOGNOTICE)
	message4a = 'إصدار كودي الأخير المتوفر الآن هو :   ' + latest_KODI_VER
	message4b = 'إصدار كودي الذي انت تستخدمه هو :   ' + current_KODI_VER
	XBMCGUI_DIALOG_OK('رسالة من المبرمج',message4a+'\n\r'+message4b)
	return

def TEST_ALL_WEBSITES():
	#XBMCGUI_DIALOG_NOTIFICATION('جاري فحص','جميع المواقع')
	websites_keys = WEBSITES.keys()
	headers = { 'User-Agent' : '' }
	def test_all(type,proxy_url=''):
		def dummyFunc(site,type,proxy_url):
			if type=='proxy': url = WEBSITES[site][0]+'||MyProxyUrl='+proxy_url
			else: url = WEBSITES[site][0]
			if type=='direct': html = openURL_cached(NO_CACHE,url,'',headers,'','SERVICES-TEST_ALL_WEBSITES-1st')
			elif type=='proxy': html = openURL_HTTPSPROXIES(url,'',headers,'','SERVICES-TEST_ALL_WEBSITES-2nd')
			#if 'https' in url: html = '___Error___'
			#else: html = ''
			return html
		threads = CustomThread(True)
		for site in websites_keys:
			threads.start_new_thread(type+'_'+site,dummyFunc,site,type,proxy_url)
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
		selection = XBMCGUI_DIALOG_SELECT(str(len(proxies_name))+' اختر بروكسي (الأسرع فوق)', proxies_name)
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
	message += '\n\n'+'== [COLOR FFC89008]فحص باستخدام شبكة الإنترنيت الخاصة بك[/COLOR] =='
	message += '\n'+messageDIRECT.strip(' ')
	if proxyname!='': message += '\n\n'+'== [COLOR FFC89008]فحص باستخدام بروكسي موجود في '+proxyname+'[/COLOR] =='
	else: message += '\n\n'+'== [COLOR FFC89008]فحص باستخدام بروكسي ببلد وإنترنيت مختلفة[/COLOR] =='
	message += '\n'+messagePROXY.strip(' ')
	XBMCGUI_DIALOG_TEXTVIEWER('فحص جميع مواقع البرنامج',message)
	direct,proxy = '',''
	if '___Error___' in str(DIRECTdict_result): direct = 'problem'
	if '___Error___' in str(PROXYdict_result): proxy = 'problem'
	if direct=='problem' and proxy!='problem':
		XBMCGUI_DIALOG_OK('رسالة من المبرمج','المشكلة التي عندك في بعض المواقع قد اختفت باستخدام بروكسي وهذا معناه ان المشكلة من طرفك وليست من البرنامج. حاول حل مشكلتك إما باستخدام DNS أو Proxy أو VPN')
	elif direct=='problem' and proxy=='problem':
		XBMCGUI_DIALOG_OK('رسالة من المبرمج','مشكلتك ظهرت مع بروكسي وبدون بروكسي وسببها إما من الموقع الأصلي أو البرنامج أو البروكسي الذي انت اخترته. جرب إعادة الفحص باختيار بروكسي مختلف وارسل سجل الأخطاء والاستخدام للمبرمج (من قائمة خدمات البرنامج)')		
	elif direct!='problem':
		XBMCGUI_DIALOG_OK('رسالة من المبرمج','جميع المواقع تعمل عندك بدون مشكلة وهذا معناه إن جهازك لا يحتاج أي تعديلات. فإذا كانت لديك مشكلة في البرنامج فقم بإرسال سجل الأخطاء والاستخدام إلى المبرمج (من قائمة خدمات البرنامج)')
	return

def ANALYTICS_REPORT():
	#BUSY_DIALOG('start')
	payload,usageDICT,message1,message2,message3,message4 = {'a':'a'},{},'','','',''
	#data = urllib.urlencode(payload)
	response = openURL_requests_cached(SHORT_CACHE,'POST',WEBSITES['PYTHON'][1],payload,'','','','SERVICES-ANALYTICS_REPORT-1st')
	html = response.content
	#XBMCGUI_DIALOG_OK('',html)
	resultsLIST = eval(html)
	siteLIST,countLIST,countryLIST = zip(*resultsLIST)
	siteLIST,countLIST,countryLIST = list(siteLIST),list(countLIST),list(countryLIST)
	for i in range(len(siteLIST)):
		site = siteLIST[i].encode('utf8')
		usage = countLIST[i]
		if   usage=='highusage': message1 += '  '+site
		elif usage=='lowusage': message2 += '  '+site
		countries = countryLIST[i].encode('utf8')
		#countries = countries.replace('___',' . ')
		countries = countries.strip(' ').strip(' .')
		countries = countries.replace('___','  ')
		countries = countries.replace('United States','USA')
		countries = countries.replace('United Kingdom','UK')
		countries = countries.replace('United Arab Emirates','UAE')
		countries = countries.replace('Saudi Arabia','KSA')
		countries = countries.replace('Western Sahara','W.Sahara')
		countries = countries[:9999].strip(' ').strip(' .')
		message4 += '\n[COLOR FFFFFF00]'+site+' : [/COLOR]'+countries
	for site in sorted(WEBSITES.keys()):
		if site not in siteLIST:
			message3 += '  '+site
			message4 += '\n[COLOR FFFFFF00]'+site+' : [/COLOR]'+'لا يوجد'
	message1 = message1.strip(' ')
	message2 = message2.strip(' ')
	message3 = message3.strip(' ')
	message4 = message4.strip('\n')
	message6 = message1+'  '+message2
	message7  = '\nHighUsage: [ '+message1+' ]'
	message7 += '\nLowUsage : [ '+message2+' ]'
	message7 += '\nNoUsage  : [ '+message3+' ]'
	LOG_THIS('NOTICE',LOGGING(script_name)+message7)
	message5  = 'مواقع شغل منها البرنامج مؤخراً فيديوهات بدون مشاكل وهذا معناه إذا لديك مشكلة فهي ليست من البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message6+'[/COLOR]'+'\n\n'
	message5 += 'مواقع لم يشغل البرنامج منها مؤخراً أي فيديوهات وهذا معناه احتمال كبير وجود مشكلة في البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message3+'[/COLOR]'+'\n\n'
	"""
	message5  = 'مواقع شغل منها البرنامج مؤخراً فيديوهات كثيرة'+'\n'
	message5 += 'وهذا معناه إذا لديك مشكلة فهي ليست من البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message1+'[/COLOR]'+'\n\n'
	message5 += 'مواقع شغل منها البرنامج مؤخراً فيديوهات قليلة\n'
	message5 += 'وهذا معناه إذا لديك مشكلة فهي ليست من البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message2+'[/COLOR]'+'\n\n'
	"""
	#BUSY_DIALOG('stop')
	XBMCGUI_DIALOG_TEXTVIEWER('مواقع اشتغلت مؤخراً في جميع دول العالم',message5)
	XBMCGUI_DIALOG_TEXTVIEWER('أعلى الدول التي استخدمت مؤخراً البرنامج',message4)
	return

def KODI_SKIN():
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN('رسالة من المبرمج','هذا البرنامج يعمل افضل باستخدام واجهة كودي (Kodi Skin) التي اسمها\n"[COLOR FFFFFF00]metropolisEMAD[/COLOR]"\n\n\n وممكن تثبيتها إما باستخدام مخزن عماد EMAD Repository أو ممكن تحميلها من موقع البرنامج\n\n[COLOR FFFFFF00]http://tiny.cc/kodiemad\nأو\nhttps://github.com/emadmahdi/KODI[/COLOR]\n\n\n هذه الرسالة وغيرها كثير موجودة في قائمة خدمات البرنامج والمزيد أيضا موجود في قائمة أجوبة البرنامج','big','center')
	return

def KODIEMAD_WEBSITE():
	message = '\n'+'تم بحمد الله عمل تطبيق خاص لبرنامج كودي مدمج معه برنامج عماد'+'\n'+'التحميل من الموقع الرسمي لتطبيق كودي عماد'+'\n\n'+'[COLOR FFFFFF00]http://tiny.cc/kodiemad[/COLOR]'
	message += '\n\n\n\n'
	message += 'اما الملفات القديمة وملفات البرمجة فهي موجودة وباقية في الموقع القديم'+'\n\n'+'[COLOR FFFFFF00]https://github.com/emadmahdi/KODI[/COLOR]'
	XBMCGUI_DIALOG_TEXTVIEWER_FULLSCREEN('رسالة مهمة من برنامج عماد للفيديوهات العربية',message,'big','center')
	return

def RESOLVEURL_SETTINGS():
	xbmc.executebuiltin('Addon.OpenSettings(script.module.resolveurl)', True)
	return

def KODI_INTERFACE_SETTINGS():
	xbmc.executebuiltin("ActivateWindow(InterfaceSettings)")
	return


def YOUTUBE_DL_SETTINGS():
	xbmc.executebuiltin('Addon.OpenSettings(script.module.youtube.dl)', True)
	return

def INPUTSTREAM_ADAPTIVE_SETTINGS():
	xbmc.executebuiltin('Addon.OpenSettings(inputstream.adaptive)', True)
	return

def CHECK_FOR_ADDONS_UPDATES():
	yes = XBMCGUI_DIALOG_YESNO('رسالة من المبرمج','كودي يقوم بعملية تحديث جميع الإضافات أوتوماتيكيا كل 24 ساعة ولكن ممكن إجراءها الآن . هل تريد تحديث جميع إضافات كودي الآن ؟','','','كلا','نعم')
	if yes==1:
		xbmc.executebuiltin('UpdateAddonRepos')
		XBMCGUI_DIALOG_OK('رسالة من المبرمج','تم إرسال طلب إلى كودي لكي يقوم بتحديث جميع إضافات كودي . بما فيها تحديث هذا البرنامج وتحديث مخزن عماد . يرجى إعطاء كودي 5 دقائق لكي ينهي عملية التحديثات')
	return

def LATEST_EMAD_VERSIONS():
	REPO_VER2,ADDON_VER2,REPO_VER3,ADDON_VER3 = '','','',''
	url = 'https://raw.githubusercontent.com/emadmahdi/KODI/master/ADDONS/addons.xml'
	#url = 'https://gitee.com/emadmahdi/KODI/raw/master/ADDONS/addons.xml'
	html = openURL_cached(NO_CACHE,url,'','','','SERVICES-LATEST_EMAD_VERSIONS-1st')
	REPO_VER2 = re.findall('name="EMAD Repository" version="(.*?)"',html,re.DOTALL)
	if REPO_VER2: REPO_VER2 = REPO_VER2[0]
	ADDON_VER2 = re.findall('"plugin.video.arabicvideos" name="EMAD Arabic Videos" version="(.*?)"',html,re.DOTALL)
	if ADDON_VER2: ADDON_VER2 = ADDON_VER2[0]
	latest_REPO_VER = REPO_VER2
	latest_ADDON_VER = ADDON_VER2
	"""
	url = 'http://emadmahdi.pythonanywhere.com/KODI/addons.xml'
	html = openURL_cached(NO_CACHE,url,'','','','SERVICES-LATEST_EMAD_VERSIONS-2nd')
	REPO_VER3 = re.findall('name="EMAD Repository" version="(.*?)"',html,re.DOTALL)
	if REPO_VER3: REPO_VER3 = REPO_VER3[0]
	ADDON_VER3 = re.findall('"plugin.video.arabicvideos" name="EMAD Arabic Videos" version="(.*?)"',html,re.DOTALL)
	if ADDON_VER3: ADDON_VER3 = ADDON_VER3[0]
	if REPO_VER2>REPO_VER3: latest_REPO_VER = REPO_VER2
	else: latest_REPO_VER = REPO_VER3
	if ADDON_VER2>ADDON_VER3: latest_ADDON_VER = ADDON_VER2
	else: latest_ADDON_VER = ADDON_VER3
	if kodi_version>18.999:
		url = 'https://raw.githubusercontent.com/emadmahdi/KODI/master/ADDONS19/addons19.xml'
		html = openURL_cached(NO_CACHE,url,'','','','SERVICES-LATEST_EMAD_VERSIONS-3rd')
		latest_ADDON_VER = re.findall('"plugin.video.arabicvideos" name="EMAD Arabic Videos" version="(.*?)"',html,re.DOTALL)[0]
	"""
	return latest_REPO_VER,latest_ADDON_VER

def INSTALL_REPOSITORY(showDialogs=True):
	if showDialogs=='': showDialogs = True
	latest_repo_version,latest_ADDON_VER = LATEST_EMAD_VERSIONS()
	repo_addon = 'repository.emad'
	installed_repo_version = xbmc.getInfoLabel('System.AddonVersion('+repo_addon+')')
	#installed_repo_version = '4.2.99999'
	is_installed = (installed_repo_version!='')
	is_old_version = (latest_repo_version>installed_repo_version)
	is_enabled = (xbmc.getCondVisibility('System.HasAddon('+repo_addon+')')==1)
	#XBMCGUI_DIALOG_OK(str(is_enabled),str(is_old_version))
	if is_installed and is_enabled and not is_old_version:
		if showDialogs: XBMCGUI_DIALOG_OK('رسالة من المبرمج','فحص مخزن عماد EMAD Repository\n\r هذا المخزن موجود عندك ومفعل وجاهز للاستخدام \n\r v'+installed_repo_version)
	elif is_installed and not is_enabled and not is_old_version:
		if showDialogs: yes = XBMCGUI_DIALOG_YESNO('رسالة من المبرمج','مخزن عماد EMAD Repository\n\r موجود عندك ولكن غير مفعل . هل تريد إصلاح المشكلة الآن ؟','','','كلا','نعم')
		else: yes = True
		if yes:
			result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"'+repo_addon+'","enabled":true}}')
			if 'OK' in result: XBMCGUI_DIALOG_OK('رسالة من المبرمج','تم تفعيل\n\r مخزن عماد EMAD Repository')
	else:
		if showDialogs: yes = XBMCGUI_DIALOG_YESNO('رسالة من المبرمج','مخزن عماد EMAD Repository\n\r فيه مشكلة عندك ... أما قديم أو غير مفعل أو غير موجود عندك ... هل تريد إصلاح المشكلة الآن ؟','','','كلا','نعم')
		else: yes = True
		if yes:
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"'+repo_addon+'","enabled":true}}')
			repo_zipfile = repo_addon+'-'+latest_repo_version+'.zip'
			zipfile_url = 'https://raw.githubusercontent.com/emadmahdi/KODI/master/ADDONS/'+repo_addon+'/'+repo_zipfile
			#zipfile_url = 'https://gitee.com/emadmahdi/KODI/raw/master/ADDONS/'+repo_addon+'/'+repo_zipfile
			zipfile_html = openURL_cached(LONG_CACHE,zipfile_url,'','','','SERVICES-INSTALL_REPOSITORY-2nd')
			addons_folder = os.path.join(xbmc.translatePath('special://home'),'addons')
			import zipfile,StringIO
			stream = StringIO.StringIO(zipfile_html)
			zf = zipfile.ZipFile(stream)
			zf.extractall(addons_folder)
			xbmc.sleep(1000)
			xbmc.executebuiltin('UpdateLocalAddons')
			xbmc.sleep(1000)
			result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"'+repo_addon+'","enabled":true}}')
			if 'OK' in result: XBMCGUI_DIALOG_OK('رسالة من المبرمج','تم تنصيب وتفعيل\n\r مخزن عماد EMAD Repository\r\n الإصدار رقم v'+latest_repo_version)
	return

def DELETE_FAVOURITES_AND_LAST_MENUS():
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','لمسح محتويات قائمة . اذهب إلى القائمة التي تريد مسحها ولا تدخل إليها ولكن باستخدام "الماوس" أو "الريموت" اضغط على الزر جهة اليمين وأما باستخدام "الكيبورد" فاضغط على حرف "C" أو على زر "القائمة" الذي في جهة اليمين')
	return

def USING_FAVOURITES():
	XBMCGUI_DIALOG_TEXTVIEWER('رسالة من المبرمج','للتعامل مع المفضلة . اذهب إلى الرابط الذي تريد إضافته أو مسحه من  قائمة المفضلة ولكن لا تضغط عليه ولا تشغله . وباستخدام "الماوس" أو "الريموت" اضغط على الزر جهة اليمين . وأما باستخدام "الكيبورد" فاضغط على حرف "C" أو على زر "القائمة" الذي في جهة اليمين . ونفس الكلام والطريقة عند التعامل مع محتويات قوائم المفضلة')
	return







"""
def TESTINGS():

	urls = [ 'http://www.youtube.com/watch?v=BaW_jenozKc' ]

	# from __future__ import unicode_literals

	success = 0
	xbmc.log('======= STARTING ==================================',level=xbmc.LOGNOTICE)
	import youtube_dl
	#import resolveurl
	#import urlresolver
	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
	for url in urls:
		t1 = time.time()
		try:
			with ydl:
				result = ydl.extract_info(url,download=False) # We just want to extract the info
			#result = urlresolver.HostedMediaFile(url).resolve()
			#result = resolveurl.HostedMediaFile(url).resolve()
			if not result: raise
			success += 1
			message = '      Succeeded_input:  '+url+'   '+str(result)
			xbmc.log('      Succeeded_output:  '+str(result['formats'][0]['url']),level=xbmc.LOGNOTICE)
			xbmc.log('      Succeeded_output:  '+str(result['formats'][0]['format']),level=xbmc.LOGNOTICE)
		except:
			message = '      Failed:  '+url
		t2 = time.time()
		t0 = str(t2-t1)[0:4]
		xbmc.log(t0+message,level=xbmc.LOGNOTICE)
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','Done','Succeeded:  '+str(success))
	xbmc.log('======= FINISHED =================================',level=xbmc.LOGNOTICE)
	return


	if 'entries' in result:
		# Can be a playlist or a list of videos
		video = result['entries'][0]
	else:
		# Just a video
		video = result
	video_url = video['url']
	XBMCGUI_DIALOG_OK(video_url,video)
	return


	#PLAY_VIDEO(url)
	#return

	#url = ''
	import resolveurl
	try:
		#resolvable = urlresolver.HostedMediaFile(url).valid_url()
		link = resolveurl.HostedMediaFile(url).resolve()
		XBMCGUI_DIALOG_OK(str(link),url)
	except: XBMCGUI_DIALOG_OK('Resolver: failed',url)
	return

	import RESOLVERS
	titles,urls = RESOLVERS.RESOLVE(url)
	selection = XBMCGUI_DIALOG_SELECT('TITLES :', titles)
	selection = XBMCGUI_DIALOG_SELECT('URLS :', urls)
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
	#XBMCGUI_DIALOG_OK(var,'')
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
	#url = RESOLVERS.PLAY(urllist,script_name,'live')
	#PLAY_VIDEO(url,script_name,'yes')
	return
"""





