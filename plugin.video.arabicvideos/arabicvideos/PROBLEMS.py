# -*- coding: utf-8 -*-
from LIBRARY import *

def MAIN(mode):
	if mode==150:
		addDir('[COLOR FFC89008]1.  [/COLOR]'+'Can\'t see Arabic Text or Letters','',151)
		addDir('[COLOR FFC89008]2.  [/COLOR]'+'ما هو اخر اصدار لكودي وللبرنامج','',159)
		addDir('[COLOR FFC89008]3.  [/COLOR]'+'ما هو الكاش وكم مقداره في البرنامج','',190)
		addDir('[COLOR FFC89008]4. [/COLOR]'+'كيف تحل بنفسك مشكلة مؤقته','',192)
		addDir('[COLOR FFC89008]5.  [/COLOR]'+'المواقع المشفرة لا تعمل','',152)
		addDir('[COLOR FFC89008]6.  [/COLOR]'+'بعض الروابط لا تعمل','',153)
		addDir('[COLOR FFC89008]7.  [/COLOR]'+'بعض الروابط بطيئة','',155)
		addDir('[COLOR FFC89008]8.  [/COLOR]'+'بعض الفيدوهات بطيئة وتقطع','',158)
		addDir('[COLOR FFC89008]9.  [/COLOR]'+'لماذا يوجد سيرفرات مجهولة','',156)
		addDir('[COLOR FFC89008]10. [/COLOR]'+'ما هي السيرفرات العامة والخاصة','',157)
		addDir('[COLOR FFC89008]11. [/COLOR]'+'اين مواقع الافلام والمسلسلات الاجنبية','',154)
		addDir('[COLOR FFC89008]12. [/COLOR]'+'ما معنى هذه العلامات ,'+escapeUNICODE('\u02d1')+';','',191)
		xbmcplugin.endOfDirectory(addon_handle)

	elif mode==151:
		message1 = '1.   If you can\'t see Arabic Letters then go to "Kodi Interface Settings" and change the font to "Arial"'
		message2 = '2.   If you can\'t see "Arial" in kodi skin fonts then go to "Kodi Interface Settings" and change your skin to another skin that accepts "Arial" font'
		xbmcgui.Dialog().ok('Arabic Problem',message1)
		xbmcgui.Dialog().ok('Font Problem',message2)

	elif mode==152:
		message1 = 'بعض المواقع تحتاج ربط مشفر ... حاول اضافة شهادة التشفير (SSL Certificate) على كودي أو استخدم كودي اصدار  17.6  أو اصدار  18.2'
		xbmcgui.Dialog().ok('المواقع المشفرة',message1)
		#message2 = 'شهادة التشفير هي ملف يحتوي على شفرة خاصة او تواقيع خاصة لشركات معروفة وله تاريخ صلاحية ونفاذ والغرض منه هو تبادل المعلومات بطريقة مشفرة يصعب اختراقها وفهمها'
		#xbmcgui.Dialog().ok('شهادة التشفير - SSL Certificate',message2)
		import PROGRAM
		PROGRAM.KODI_VERSION()

	elif mode==153:
		yes = xbmcgui.Dialog().yesno('روابط لا تعمل','غالبا السبب هو من الموقع الاصلي المغذي للبرنامج وللتأكد تستطيع اخبار المبرمج بجميع التفاصيل فهل تريد اخبار المبرمج الان ؟')	
		if yes: 
			import PROGRAM
			PROGRAM.SEND_MESSAGE()

	elif mode==154:
		message = 'السبب هو ان هذا البرنامج مخصص فقط للغة العربية ولكن مع هذا وبالصدفة يوجد فيه مواقع فيها افلام ومسلسلات مترجمة او مدبلجة الى اللغة العربية والى لغات اخرى ولا يوجد سبب للتكرار'
		xbmcgui.Dialog().ok('مواقع اجنبية',message)

	elif mode==155:
		message = 'الروابط البطيئة لا علاقة لها بالبرنامج وغالبا السبب هو من الموقع الاصلي المغذي للبرنامج'
		xbmcgui.Dialog().ok('روابط بطيئة',message)

	elif mode==156:
		message = 'هي سيرفرات لا يستطيع البرنامج استخدامها بسبب كونها محمية من المصدر او بحاجة الى اشتراك رسمي او جديدة او لا يعرفها البرنامج'
		xbmcgui.Dialog().ok('سيرفرات سيئة او مجهولة',message)

	elif mode==157:
		message = 'السيرفرات العامة هي سيرفرات خارجية وغير جيدة لان الكثير منها ممنوع او محذوف او خطأ بسبب حقوق الطبع وحقوق الالفية الرقمية ولا توجد طريقة لفحصها او اصلاحها \n\n السيرفرات الخاصة هي سيرفرات يتحكم فيها الموقع الاصلي وهي جيدة نسبيا ولا توجد طريقة لفحصها او اصلاحها \n\n الرجاء قبل الابلاغ عن مشكلة وقبل مراسلة المبرمج افحص نفس الفيديو وافحص نفس السيرفر على الموقع الاصلي'
		xbmcgui.Dialog().textviewer('مواقع تستخدم سيرفرات عامة',message)

	elif mode==158:
		message1 = 'ابتعد عن ملفات الدقة العالية'
		message2 = 'ابتعد عن ملفات ال m3u8'
		message3 = 'ابتعد عن ملفات التحميل والداونلود download'
		message = message1 + '\n' + message2 + '\n' + message3
		xbmcgui.Dialog().ok('لتسريع عمل الفيديوهات',message)

	elif mode==159:
		import PROGRAM
		PROGRAM.VERSION()

	elif mode==190:
		message2 = 'الكاش هو مخزن مؤقت للمعلومات يستخدمه البرنامج لخزن صفحات الانترنيت وروابط الفيديوهات'
		message2 += ' ' + 'للوصول اليها بسرعة وبدون انترنيت والبرنامج يمسحها اوتوماتيكيا بعد انتهاء وقتها وايضا عند تحديث البرنامج والكاش في البرنامج هو ثلاثة انواع'
		message2 += '\n\n' + 'طويل المدى للصفحات التي لا تتغير ومدته ' + str(LONG_CACHE/60/60) + ' ساعة'
		message2 += '\n\n' + 'متوسط المدى للصفحات التي قد تتغير ومدته ' + str(REGULAR_CACHE/60/60) + ' ساعة'
		message2 += '\n\n' + 'قصير المدى للصفحات التي تتغير دائما ومدته ' + str(SHORT_CACHE/60/60) + ' ساعة'
		xbmcgui.Dialog().textviewer('ما هو الكاش المستخدم في البرنامج',message2)

	elif mode==191:
		message = 'الفاصلة تعني مجلد بنفس اسمه الاصلي والنقطة تعني ان الاسم الاصلي تم تعديله وفاصلة ونقطة تعنى مجلد وتم تعديل اسمه وبدون علامة تعني ملف بنفس اسمه الاصلي'
		xbmcgui.Dialog().ok('ما معنى هذه العلامات ,'+escapeUNICODE('\u02d1')+';',message)

	elif mode==192:
		message = 'اذا واجهتك مشكلة في الشبكة وتم حلها ... او انك تظن ان الموقع الاصلي كان فيه مشكلة مؤقته وتم حلها ... فاذن جرب مسح كاش البرنامج لكي يقوم البرنامج بطلب الصفحة الصحيحة وتخزينها بدلا من الصفحة القديمة'
		xbmcgui.Dialog().ok('كيف تحل مشكلة مؤقته',message)

	return
		

