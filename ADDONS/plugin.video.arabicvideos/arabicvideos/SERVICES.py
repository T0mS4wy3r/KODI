# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='SERVICES'

def MAIN(mode,text=''):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if mode in [0,1]: FIX_KEYBOARD(mode,text)
	elif mode==2: SEND_MESSAGE(text)
	elif mode==3: DMCA()
	elif mode==4: HTTPS_TEST()
	#elif mode==5: EGYBEST_ADBLOCKER()
	elif mode==6: GLOBAL_SEARCH_MENU(text)
	elif mode==7: VERSIONS()
	elif mode==8: RANDOM()
	elif mode==9: DELETE_CACHE()
	elif mode==170: TV_CHANNELS_MENU()
	elif mode==171: SSL_WARNING()
	elif mode==173: ENABLE_MPD()
	elif mode==174: ENABLE_RTMP()
	elif mode==175: TEST_ALL_WEBSITES()
	elif mode==176: ANALYTICS_REPORT()
	elif mode==179: TESTINGS()
	elif mode==150: MAIN_MENU()
	elif mode==151: NO_ARABIC_FONTS()
	elif mode==152: HTTPS_FAILED()
	elif mode==153: LINKS_NOT_WORKING()
	elif mode==154: NO_FORIGN_LANGUAGE_VIDEOS()
	elif mode==155: SLOW_LINKS()
	elif mode==156: UNKNOWN_SERVERS()
	elif mode==157: PRIVATE_PUBLIC_SERVERS()
	elif mode==158: SLOW_VIDES()
	elif mode==190: WHAT_IS_CACHE()
	elif mode==191: WHAT_DOT_COMMA_MEANS()
	elif mode==192: SOLVE_TEMP_PROBLEM()
	elif mode==193: WHY_IGNORE_SSL_CERTIFICATE()
	elif mode==194: MPD_NOT_WORKING()
	elif mode==195: WEBSITES_BLOCKED()
	elif mode==196: HOW_TO_CONTACT_US()
	elif mode==197: KODI_SKIN()
	return

def MAIN_MENU():
	#addDir('[COLOR FFC89008]ـ Problems & Questions  قائمة مشاكل وأسئلة  .1 [/COLOR]','',150)
	#addLink('[COLOR FFC89008] 2.  [/COLOR]'+'فحص جميع مواقع البرنامج','',175,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 1.  [/COLOR]'+'Can\'t see Arabic Text or Letters','',151)
	addLink('[COLOR FFC89008] 2.  [/COLOR]'+'ـ DMCA  قانون الألفية للملكية الرقمية','',3,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 3.  [/COLOR]'+'فحص الاصدار الاخير والتحديثات','',7,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 4.  [/COLOR]'+'فحص تفعيل فيديوهات mpd ـ','',173,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 5.  [/COLOR]'+'فحص تفعيل فيديوهات rtmp ـ','',174,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 6.  [/COLOR]'+'فحص اتصال المواقع المشفرة','',4,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 7.  [/COLOR]'+'مسح كاش البرنامج','',9,'','','IsPlayable=no')
	addLink('[COLOR FFC89008] 8.  [/COLOR]'+'ارسال سجل الاخطاء والاستخدام للمبرمج','',2,'','','IsPlayable=no,problem=yes')
	addLink('[COLOR FFC89008] 9.  [/COLOR]'+'ابلاغ المبرمج بوجود مشكلة','',2,'','','IsPlayable=no,problem=yes')
	addLink('[COLOR FFC89008]10.  [/COLOR]'+'ارسال رسالة الى المبرمج','',2,'','','IsPlayable=no,problem=no')
	addLink('[COLOR FFC89008]11.  [/COLOR]'+'تحذير يخص شهادة التشفير','',171,'','','IsPlayable=no')
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addLink('[COLOR FFC89008]12.  [/COLOR]'+'ما هي افضل واجهة للبرنامج','',197)
	addLink('[COLOR FFC89008]13.  [/COLOR]'+'لماذا بعض المواقع لا تعمل','',195)
	addLink('[COLOR FFC89008]14.  [/COLOR]'+'كيف تحل مشكلة ححب بعض المواقع','',195)
	addLink('[COLOR FFC89008]15.  [/COLOR]'+'بعض الفيدوهات بطيئة وتقطع','',158)
	addLink('[COLOR FFC89008]16.  [/COLOR]'+'كيف تحل بنفسك مشكلة مؤقته','',192)
	addLink('[COLOR FFC89008]17.  [/COLOR]'+'بعض الروابط لا تعمل','',153)
	addLink('[COLOR FFC89008]18.  [/COLOR]'+'بعض الروابط بطيئة','',155)
	addLink('[COLOR FFC89008]19.  [/COLOR]'+'لماذا يوجد سيرفرات مجهولة','',156)
	addLink('[COLOR FFC89008]20.  [/COLOR]'+'ما هي السيرفرات العامة والخاصة','',157)
	addLink('[COLOR FFC89008]21. [/COLOR]'+'ما معنى هذه العلامات بالبرنامج ,'+escapeUNICODE('\u02d1')+';','',191)
	addLink('[COLOR FFC89008]22. [/COLOR]'+'ما هو اخر اصدار لكودي وللبرنامج','',7)
	addLink('[COLOR FFC89008]23. [/COLOR]'+'ما هو الكاش وكم مقداره بالبرنامج','',190)
	addLink('[COLOR FFC89008]24. [/COLOR]'+'الفيديوهات نوع mpd لا تعمل','',194)
	addLink('[COLOR FFC89008]25. [/COLOR]'+'المواقع المشفرة لا تعمل','',152)
	addLink('[COLOR FFC89008]26. [/COLOR]'+'لماذا لا نفحص شهادة التشفير','',193)
	addLink('[COLOR FFC89008]27. [/COLOR]'+'اين مواقع الافلام والمسلسلات الاجنبية','',154)
	xbmcplugin.endOfDirectory(addon_handle)

def NO_ARABIC_FONTS():
	message1 = '1.   If you can\'t see Arabic Letters then go to "Kodi Interface Settings" and change the font to "Arial"'
	message2 = '1.   اذا لم تستطع رؤية الاحرف العربية فغير الخط المستخدم الى "Arial" من اعدادات واجهة كودي'
	xbmcgui.Dialog().ok('Arabic Problem',message1,message2)
	message1 = '2.   If you don\'t find "Arial" font in kodi skin then change skin in "Kodi Interface Settings"'
	message2 = '2.   اذا لم تجد الخط "Arial" فاذن عليك ان تذهب الى اعدادات كودي وتغير واجهة كودي المستخدمة'
	xbmcgui.Dialog().ok('Font Problem',message1,message2)
	yes = xbmcgui.Dialog().yesno('Font settings','Do you want to go to "Kodi Interface Settings" now?','هل تريد الذهاب الى لوحة اعدادت واجهة كودي الان؟')
	if yes==1: xbmc.executebuiltin("ActivateWindow(InterfaceSettings)")

def HTTPS_FAILED():
	message1 = 'بعض المواقع تحتاج ربط مشفر وقد يكون جهازك غير قادر على الربط المشفر او هناك مشكلة في شهادة التشفير الخاصة بكودي عندك علما انه تم فحص البرنامج على كودي الاصدارات'
	message2 = '17.6  &  18.[0-3]'
	xbmcgui.Dialog().ok('المواقع المشفرة',message1,message2)
	#message2 = 'شهادة التشفير هي ملف يحتوي على شفرة خاصة او تواقيع خاصة لشركات معروفة وله تاريخ صلاحية ونفاذ والغرض منه هو تبادل المعلومات بطريقة مشفرة يصعب اختراقها وفهمها'
	#xbmcgui.Dialog().ok('شهادة التشفير - SSL Certificate',message2)
	LATEST_KODI()

def LINKS_NOT_WORKING():
	xbmcgui.Dialog().ok('روابط لا تعمل','غالبا السبب هو من الموقع الاصلي المغذي للبرنامج وللتأكد قم بتشغيل الرابط الذي لا يعمل ثم قم بارسال مشكلة الى المبرمج من القائمة الرئيسية للبرنامج')

def NO_FORIGN_LANGUAGE_VIDEOS():
	message = 'هذا البرنامج مخصص فقط للغة العربية ولكن هذا لا يمنع وجود مواقع فيها افلام ومسلسلات مترجمة او مدبلجة الى اللغة العربية والى لغات اخرى ولا يوجد سبب للتكرار'
	xbmcgui.Dialog().ok('مواقع اجنبية',message)

def SLOW_LINKS():
	message = 'الروابط البطيئة لا علاقة لها بالبرنامج وغالبا السبب هو من الموقع الاصلي المغذي للبرنامج'
	xbmcgui.Dialog().ok('روابط بطيئة',message)

def UNKNOWN_SERVERS():
	message = 'هي سيرفرات لا يستطيع البرنامج استخدامها بسبب كونها محمية من المصدر او بحاجة الى اشتراك رسمي او جديدة او لا يعرفها البرنامج'
	xbmcgui.Dialog().ok('سيرفرات سيئة او مجهولة',message)

def PRIVATE_PUBLIC_SERVERS():
	message = 'السيرفرات العامة هي سيرفرات خارجية وغير جيدة لان الكثير منها ممنوع او محذوف او خطأ بسبب حقوق الطبع وحقوق الالفية الرقمية ولا توجد طريقة لفحصها او اصلاحها \n\n السيرفرات الخاصة هي سيرفرات يتحكم فيها الموقع الاصلي وهي جيدة نسبيا ولا توجد طريقة لفحصها او اصلاحها \n\n الرجاء قبل الابلاغ عن مشكلة وقبل مراسلة المبرمج افحص نفس الفيديو وافحص نفس السيرفر على الموقع الاصلي'
	xbmcgui.Dialog().textviewer('مواقع تستخدم سيرفرات عامة',message)

def SLOW_VIDES():
	message1 = 'ابتعد عن ملفات الدقة العالية'
	message2 = 'ابتعد عن ملفات ال m3u8'
	message3 = 'ابتعد عن ملفات التحميل والداونلود download'
	xbmcgui.Dialog().ok('لتسريع عمل الفيديوهات',message1,message2,message3)

def WHAT_IS_CACHE():
	message2 = 'الكاش هو مخزن مؤقت للمعلومات يستخدمه البرنامج لخزن صفحات الانترنيت وروابط الفيديوهات'
	message2 += ' ' + 'للوصول اليها بسرعة وبدون انترنيت والبرنامج يمسحها اوتوماتيكيا بعد انتهاء وقتها وايضا عند تحديث البرنامج والكاش في البرنامج هو ثلاثة انواع'
	message2 += '\n\n' + 'طويل المدى للصفحات التي لا تتغير ومدته ' + str(LONG_CACHE/60/60) + ' ساعة'
	message2 += '\n\n' + 'متوسط المدى للصفحات التي قد تتغير ومدته ' + str(REGULAR_CACHE/60/60) + ' ساعة'
	message2 += '\n\n' + 'قصير المدى للصفحات التي تتغير دائما ومدته ' + str(SHORT_CACHE/60/60) + ' ساعة'
	xbmcgui.Dialog().textviewer('ما هو الكاش المستخدم في البرنامج',message2)

def WHAT_DOT_COMMA_MEANS():
	message = 'الفاصلة تعني مجلد بنفس اسمه الاصلي والنقطة تعني ان الاسم الاصلي تم تعديله وفاصلة ونقطة تعنى مجلد وتم تعديل اسمه وبدون علامة تعني ملف بنفس اسمه الاصلي'
	xbmcgui.Dialog().ok('ما معنى هذه العلامات ,'+escapeUNICODE('\u02d1')+';',message)

def SOLVE_TEMP_PROBLEM():
	message = 'اذا واجهتك مشكلة في الشبكة وتم حلها ... او انك تظن ان الموقع الاصلي كان فيه مشكلة مؤقته وتم حلها ... فاذن جرب مسح كاش البرنامج لكي يقوم البرنامج بطلب الصفحة الصحيحة وتخزينها بدلا من الصفحة القديمة'
	xbmcgui.Dialog().ok('كيف تحل مشكلة مؤقته',message)

def WHY_IGNORE_SSL_CERTIFICATE():
	message = 'الغرض من شهادة التشفير هو ضمان صحة وسرية المعلومات المتبادلة بين البرنامج والموقع المشفر وهذا الضمان غير مطلوب ولا حاجة له عند الاتصال او الربط مع مواقع الفيديوهات المشفرة'
	xbmcgui.Dialog().ok('لماذا لا نفحص شهادة التشفير',message)

def MPD_NOT_WORKING():
	message1 = 'يجب تفعيل اضافة اسمها inputstream.adaptive لكي يعمل هذا النوع من الفيدوهات'
	message2 = 'InputStream Adaptive'
	message3 = 'وبعدها سوف تعمل هذه الفيدوهات'
	xbmcgui.Dialog().ok('الفيديوهات نوع mpd لا تعمل',message1)
	ENABLE_MPD()

def WEBSITES_BLOCKED():
	message  = 'مؤخرا قامت بعض شركات الانترنيت الدولي بوضع عائق ضد البرامج مثل كودي لتسمح فقط لبعض مستخدمي المتصفح بالدخول لمواقع الفيديو'
	#message += '\n[COLOR FFC89008]وهذا العائق هو reCAPTCHA الخاص بشركة جوجل[/COLOR]\n'
	#message += 'والذي صنعته شركة جوجل خصيصا لمنع برامج مثل كودي من تصفح الانترنيت'
	message += '\n\nونتيجة لهذا العائق فانه تقريبا جميع مستخدمي برنامج كودي لا يستطيعون الدخول لجميع مواقع البرنامج حتى مع استخدام'
	message += '\n[COLOR FFC89008]ـ  VPN  أو  Proxy  أو  DNS  أو أي حل بسيط اخر[/COLOR]\n'
	message += '\nلان هذا لن يحل المشكلة وانما فقط سيقوم باصلاح بعض المواقع واعاقة مواقع اخرى كانت تعمل سابقا بدون مشاكل'
	xbmcgui.Dialog().textviewer('عائق ضد كودي والبرامج الاخرى عدا المتصفح',message)
	message = 'المواقع التي تأثرت بالعائق عند بعض الناس هي:'
	message += '\n'+'[COLOR FFC89008]akoam  egybest  egy4best  movizland  series4watch  shahid4u[/COLOR]'
	message += '\n\n'+'الدول التي تأثرت بالعائق عند بعض الناس هي:'
	message += '\n'+'[COLOR FFC89008]مصر  الكويت  اميركا  كندا  فرنسا  اليونان  بريطانيا الامارات المانيا روسيا اليابان السعودية رومانيا هولندا[/COLOR]'
	message += '\n\n'+'المبرمج وجد طريقة لتجاوز العائق ولكنها تحتاج جهد كبير والمبرمج يظن المشكلة صغيرة ولا تستحق التعب فاذا لديك مشكلة بالدخول لبعض المواقع وايضا لكي يتضح حجم المشكلة '
	message += '[COLOR FFC89008]ارسل رسالة مؤدبة الى المبرمج واكتب فيها اسم بلدك واسماء المواقع التي لا تستطيع دخولها[/COLOR]'
	xbmcgui.Dialog().textviewer('المواقع والدول التي تأثرت بالعائق',message)
	#SEND_MESSAGE('IsPlayable=no,problem=no')
	#message = '\n\n'+'ولقد لاحظنا ايضا ان المواقع المعاقة تختلف باختلاف البلد وتختلف باختلاف شركة الانترنيت في ذلك البلد وهذا معناه انه حتى لو تم استخدام VPN او Proxy او اي وسيلة اخرى فان المواقع المعاقة سوف تختلف ولكنها لن تعمل جميعها'
	#message += 'لحل المشكلة قم بعملين:    الأول: أرسل سجل الاخطاء والاستخدام الى المبرمج (من قائمة خدمات البرنامج) واكتب معه اسم بلدك واسم شركة الانترنيت واسماء المواقع التي لا تعمل عندك'
	#message += '\n\n'+'والثاني: جرب استخدام VPN وعند البعض قد تحتاج فقط تغيير DNS والاحسن ان يكون في بلد اخر علما ان استخدام Proxy قد يحل مشكلة بعض المواقع ولكن ليس في جميع الدول'
	#xbmcgui.Dialog().textviewer('مشكلة عند بعض الناس',message)
	#yes = xbmcgui.Dialog().yesno('فحص جميع مواقع البرنامج','هذا الفحص هو لمعرفة هل المشكلة من عندك ام من البرنامج. سيقوم البرنامج الان بفحص مواقعه مرتين الاولى بوضعك الطبيعي والثانية باستخدام بروكسي مجاني انت تختاره من القائمة التي ستظهر لاحقا. هل تريد الاستمرار؟','','','كلا','نعم')
	#if yes==1:
	#TEST_ALL_WEBSITES()

def HOW_TO_CONTACT_US():
	xbmcgui.Dialog().ok('هناك طريقتين للتواصل مع المبرمج','الاولى عن طريق ارسال رسالة او مشكلة من قائمة الخدمات ... والافضل الطريقة الثانية وهي فتح موضوع للنقاش عن طريق هذا الرابط','https://github.com/emadmahdi/KODI/issues')

def DELETE_CACHE():
	MAIN(190)
	yes = xbmcgui.Dialog().yesno('هل متأكد وتريد مسح جميع الكاش ؟','الكاش مهم لتسريع عمل البرنامج ومسحه يسبب اعادة طلب جميع الصفحات من الانترنيت عند الحاجة اليها. وهذا قد يحل مشاكل بعض المواقع','','','كلا','نعم')
	if yes==1: 
		DELETE_DATABASE_FILES()
		xbmcgui.Dialog().ok('تم مسح كاش البرنامج بالكامل','اذا كانت عندك مشكلة في احد المواقع فجرب الموقع الان ... واذا المشكلة مستمرة فاذن ارسل المشكلة الى المبرمج')
	return ''

def HTTPS_TEST():
	working = HTTPS(True)
	if not working:
		MAIN(152)
	return

def FIX_KEYBOARD(mode,text):
	import xbmc,unicodedata,email.charset
	import xbmcgui
	#import simplejson as json
	#from LIBRARY import *
	#xbmcgui.Dialog().ok(str(mode),text)
	keyboard = text
	if keyboard=='': return
	if mode==1:
		try:
			window_id = xbmcgui.getCurrentWindowDialogId()
			window = xbmcgui.Window(window_id)
			keyboard = mixARABIC(keyboard)
			window.getControl(311).setLabel(keyboard)
		except:
			traceback.print_exc(file=sys.stderr)
			pass
	elif mode==0:
		ttype = 'X'
		check = isinstance(keyboard, unicode)
		if check==True: ttype = 'U'
		new1 = str(type(keyboard))+' '+keyboard+' '+ttype+' '
		for i in range(0,len(keyboard),1):
			new1 += hex(ord(keyboard[i])).replace('0x','')+' '
		keyboard = mixARABIC(keyboard)
		ttype = 'X'
		check = isinstance(keyboard, unicode)
		if check==True: ttype='U'
		new2 = str(type(keyboard))+' '+keyboard+' '+ttype+' '
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
		logs = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','سيقوم البرنامج بارسال سجل الاخطاء والاستخدام الى المبرمج لكي يستطيع المبرمج معرفة المشكلة واصلاحها','','','كلا','نعم')
		if logs==0:
			xbmcgui.Dialog().ok('تم الغاء الارسال','للأسف بدون سجل الاخطاء والاستخدام المبرمج لا يستطيع معرفة المشكلة ولا حلها لان المبرمج لا يعلم الغيب')
			return ''
		logs2 = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','هل قمت قبل قليل بتشغيل الفيديو او الرابط الذي اعطاك المشكلة لكي يتم تسجيل هذه المشكلة في سجل الاخطاء والاستخدام قبل ارساله للمبرمج','','','كلا','نعم')
		if logs2==0:
			xbmcgui.Dialog().ok('تم الغاء الارسال','للأسف بدون تسجيل المشكلة في سجل الاخطاء والاستخدام فان المبرمج لا يستطيع معرفة المشكلة ولا حلها لان المبرمج لا يعلم الغيب')
			return ''
		"""
		else:
			text += 'logs=yes'
			yes = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','قبل ارسال سجل الاخطاء والاستخدام الى المبرمج عليك ان تقوم بتشغيل الفيديو او الرابط الذي يعطيك المشكلة لكي يتم تسجيل المشكلة في سجل الاخطاء والاستخدام. هل تريد الارسال الان ؟','','','كلا','نعم')
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
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Searching: [ '+search+' ]')
	search = search.lower()
	addLink('[COLOR FFC89008]مواقع سيرفرات خاصة - قليلة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('1.  [COLOR FFC89008]YUT  [/COLOR]'+search+' - خدمة IPTV','',239,'','',search)
	addDir('2.  [COLOR FFC89008]YUT  [/COLOR]'+search+' - موقع يوتيوب','',149,'','',search)
	addDir('3.  [COLOR FFC89008]SHF  [/COLOR]'+search+' - موقع شوف ماكس','',59,'','',search)
	addDir('4.  [COLOR FFC89008]KLA  [/COLOR]'+search+' - موقع كل العرب','',19,'','',search)
	addDir('5.  [COLOR FFC89008]PNT  [/COLOR]'+search+' - موقع بانيت','',39,'','',search)
	addDir('6.  [COLOR FFC89008]IFL    [/COLOR]'+search+' - موقع قناة اي فيلم','',29,'','',search)
	addDir('7.  [COLOR FFC89008]KWT  [/COLOR]'+search+' - موقع قناة الكوثر','',139,'','',search)
	addDir('8.  [COLOR FFC89008]MRF  [/COLOR]'+search+' - موقع قناة المعارف','',49,'','',search)
	addDir('9.  [COLOR FFC89008]FTM  [/COLOR]'+search+' - موقع المنبر الفاطمي','',69,'','',search)
	#addDir('[COLOR FFC89008]=========================[/COLOR]','',9999)
	addLink('[COLOR FFC89008]مواقع سيرفرات خاصة وعامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('10. [COLOR FFC89008]AKM  [/COLOR]'+search+' - موقع اكوام','',79,'','',search)
	addDir('11. [COLOR FFC89008]EG4  [/COLOR]'+search+' - موقع ايجي فور بيست','',229,'','',search)
	#addDir('[COLOR FFC89008]=========================[/COLOR]','',9999)
	addLink('[COLOR FFC89008]مواقع سيرفرات عامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('12. [COLOR FFC89008]HEL  [/COLOR]'+search+' - موقع هلال يوتيوب','',99,'','',search)
	addDir('13. [COLOR FFC89008]SHA  [/COLOR]'+search+' - موقع شاهد فوريو','',119,'','',search)
	addDir('14. [COLOR FFC89008]ARL  [/COLOR]'+search+' - موقع عرب ليونز','',209,'','',search)
	#addDir('[COLOR FFC89008]=========================[/COLOR]','',9999)
	#addDir('15. [COLOR FFC89008]HLA  [/COLOR]'+search+' - موقع هلا سيما','',88,'','',search) # 89
	#addDir('16. [COLOR FFC89008]SFW  [/COLOR]'+search+' - موقع سيريس فور وتش','',218,'','',search) # 219
	#addDir('17. [COLOR FFC89008]MVZ  [/COLOR]'+search+' - موقع موفيز لاند','',188,'','',search)# 189
	#addDir('18. [COLOR FFC89008]EGB  [/COLOR]'+search+' - موقع ايجي بيست','',128,'','',search)# 129
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TV_CHANNELS_MENU():
	addDir('1.  [COLOR FFC89008]IPT   [/COLOR]'+'للمشتركين بخدمة IPTV','',230)
	addDir('2.  [COLOR FFC89008]TV0  [/COLOR]'+'قنوات من مواقعها الاصلية','',100)
	addDir('3.  [COLOR FFC89008]YUT  [/COLOR]'+'قنوات عربية من يوتيوب','',147)
	addDir('4.  [COLOR FFC89008]YUT  [/COLOR]'+'قنوات اجنبية من يوتيوب','',148)
	addDir('5.  [COLOR FFC89008]IFL    [/COLOR]'+'قناة اي فيلم من موقعهم','',28)
	#addDir('5.  [COLOR FFC89008]MRF  [/COLOR]'+'من موقع قناة المعارف','',41)
	#addDir('6.  [COLOR FFC89008]KWT  [/COLOR]'+'من موقع قناة الكوثر','',135)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addDir('6.  [COLOR FFC89008]TV1  [/COLOR]'+'قنوات تلفزونية عامة','',101)
	addDir('7.  [COLOR FFC89008]TV2  [/COLOR]'+'قنوات تلفزونية خاصة','',102)
	addDir('8.  [COLOR FFC89008]TV3  [/COLOR]'+'قنوات تلفزونية للفحص','',103)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def VERSIONS():
	xbmcgui.Dialog().notification('جاري جمع المعلومات','الرجاء الانتظار')
	#xbmc.log('BBBB: 1111:', level=xbmc.LOGNOTICE)
	threads22 = CustomThread()
	#xbmc.log('BBBB: 2222:', level=xbmc.LOGNOTICE)
	threads22.start_new_thread('22',LATEST_KODI)
	#xbmc.log('BBBB: 3333:', level=xbmc.LOGNOTICE)
	#xbmcgui.Dialog().notification('thread submitted','')
	#	url = 'http://raw.githack.com/emadmahdi/KODI/master/addons.xml'
	#   url = 'https://github.com/emadmahdi/KODI/raw/master/addons.xml'
	url = 'https://raw.githubusercontent.com/emadmahdi/KODI/master/ADDONS/addons.xml'
	html = openURL_PROXY(url,'','','','SERVICES-VERSIONS-1st')
	latest_ADDON_VER = re.findall('plugin.video.arabicvideos" name="Arabic Videos" version="(.*?)"',html,re.DOTALL)[0]
	current_ADDON_VER = addon_version
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
	#LATEST_KODI()
	#threads22.wait_finishing_all_threads()
	return

def RANDOM():
	headers = { 'User-Agent' : '' }
	url = 'https://www.bestrandoms.com/random-arabic-words'
	payload = { 'quantity' : '5' }
	data = urllib.urlencode(payload)
	#xbmcgui.Dialog().ok('',str(data))
	html = openURL_PROXY(url,data,headers,'','SERVICES-RANDOM-1st')
	#html = openURL_cached(NO_CACHE,url,data,headers,'','SERVICES-RANDOM-1st')
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

def SSL_WARNING():
	xbmcgui.Dialog().ok('تحذير مهم','البرنامج لا يفحص شهادة التشفير عند الاتصال بالمواقع المشفرة ولهذا في حال وجود شهادة غير صحيحة او منتهية الصلاحية او مزيفة فان هذا لن يوقف الربط المشفر ولن يوقف عمل البرنامج')
	MAIN(193)
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
	current_KODI_VER = xbmc.getInfoLabel( "System.BuildVersion" ).split(' ')[0]
	#xbmc.log('ZZZZ: 4444:', level=xbmc.LOGNOTICE)
	message4a = 'اصدار كودي الاخير المتوفر الان هو :   ' + latest_KODI_VER
	message4b = 'اصدار كودي الذي انت تستخدمه هو :   ' + current_KODI_VER
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
		xbmcgui.Dialog().ok('نتيجة فحص مواقع البرنامج','مشكلتك ظهرت مع بروكسي وبدون بروكسي وسببها اما من الموقع الاصلي أو البرنامج أو البروكسي الذي انت اخترته. جرب اعادة الفحص باختيار بروكسي مختلف وارسل سجل الاخطاء والاستخدام للمبرمج (من قائمة خدمات البرنامج)')		
	elif direct!='problem':
		xbmcgui.Dialog().ok('نتيجة فحص مواقع البرنامج','جميع المواقع تعمل عندك بدون مشكلة وهذا معناه ان جهازك لا يحتاج اي تعديلات. فاذا كانت لديك مشكلة في البرنامج فقم بارسال سجل الاخطاء والاستخدام الى المبرمج (من قائمة خدمات البرنامج)')
	return

def ANALYTICS_REPORT():
	payload,usageDICT,message1,message2,message3,message4 = {'a':'a'},{},'','','',''
	data = urllib.urlencode(payload)
	html = openURL_cached(SHORT_CACHE,WEBSITES['LIVETV'][1],data,'','','SERVICES-ANALYTICS_REPORT-1st')
	#xbmcgui.Dialog().ok('',html)
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
		countries = countries[:43].strip(' ').strip(' .')
		message4 += '\n[COLOR FFC89008]'+site+' : [/COLOR]'+countries
	for site in sorted(WEBSITES.keys()):
		if site not in siteLIST:
			message3 += '  '+site
			message4 += '\n[COLOR FFC89008]'+site+' : [/COLOR]'+'لا يوجد'
	message1 = message1.strip(' ')
	message2 = message2.strip(' ')
	message3 = message3.strip(' ')
	message4 = message4.strip('\n')
	LOG_THIS('NOTICE',LOGGING(script_name)+'   HighUsage: [ '+message1+' ]')
	LOG_THIS('NOTICE',LOGGING(script_name)+'   LowUsage: [ '+message2+' ]')
	LOG_THIS('NOTICE',LOGGING(script_name)+'   NoUsage: [ '+message3+' ]')
	message6 = message1+'  '+message2
	message5  = 'مواقع شغل منها البرنامج مؤخراً فيديوهات بدون مشاكل'+'\n'
	message5 += 'وهذا معناه اذا لديك مشكلة فهي ليست من البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message6+'[/COLOR]'+'\n\n'
	message5 += 'مواقع لم يشغل البرنامج منها مؤخراً أي فيديوهات'+'\n'
	message5 += 'وهذا معناه احتمال كبير وجود مشكلة في البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message3+'[/COLOR]'+'\n\n'
	"""
	message5  = 'مواقع شغل منها البرنامج مؤخراً فيديوهات كثيرة'+'\n'
	message5 += 'وهذا معناه اذا لديك مشكلة فهي ليست من البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message1+'[/COLOR]'+'\n\n'
	message5 += 'مواقع شغل منها البرنامج مؤخراً فيديوهات قليلة\n'
	message5 += 'وهذا معناه اذا لديك مشكلة فهي ليست من البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message2+'[/COLOR]'+'\n\n'
	"""
	xbmcgui.Dialog().textviewer('مواقع اشتغلت مؤخراً في جميع دول العالم',message5)
	xbmcgui.Dialog().textviewer('اعلى الدول التي استخدمت مؤخراً البرنامج',message4)

def KODI_SKIN():
	xbmcgui.Dialog().textviewer('واجهة كودي Kodi Skin','هذا البرنامج يعمل افضل بأستخدام واجهة كودي التي اسمها\nkodi skin "[COLOR FFC89008]metropolisEMAD[/COLOR]"\n\nوهي موجودة في نفس موقع البرنامج\n[COLOR FFC89008]https://github.com/emadmahdi/KODI [/COLOR]\n\nهذه الرسالة وغيرها كثير موجودة في قائمة خدمات البرنامج')
	return

def TESTINGS():
	url = 'http://egybest.vip/ee.mp4'
	PLAY_VIDEO(url)
	return
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
