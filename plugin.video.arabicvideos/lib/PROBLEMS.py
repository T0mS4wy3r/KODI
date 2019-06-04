# -*- coding: utf-8 -*-
from LIBRARY import *

def MAIN(mode):
	if mode==150:
		addDir('Problem:   Can\'t see Arabic Text or Letters','',151)
		addDir('المواقع المشفرة لا تعمل   :مشكلة','',152)
		addDir('بعض الروابط لا تعمل   :مشكلة','',153)
		addDir('لا توجد مواقع مخصصة للافلام والمسلسلات الاجنبية   :مشكلة','',154)
		addDir('بعض الروابط بطيئة   :مشكلة','',155)
		addDir('لماذا يوجد سيرفرات مجهولة او سيئة   :مشكلة','',156)
		addDir('ما هي السيرفرات العامة والخاصة   :مشكلة','',157)
		addDir('بعض الفيدوهات بطيئة   :مشكلة','',158)
		xbmcplugin.endOfDirectory(addon_handle)

	elif mode==151:
		message1 = '1.   If you can\'t see Arabic Letters then go to "Kodi Interface Settings" and change the font to "Arial"'
		message2 = '2.   If you can\'t see "Arial" in kodi skin fonts then go to "Kodi Interface Settings" and change your skin to another skin that accepts "Arial" font'
		xbmcgui.Dialog().ok('Arabic Problem',message1)
		xbmcgui.Dialog().ok('Font Problem',message2)

	elif mode==152:
		message1 = 'بعض المواقع تحتاج ربط مشفر ... حاول اضافة شهادة التشفير (SSL Certificate) على كودي أو استخدم كودي اصدار 17.6'
		xbmcgui.Dialog().ok('المواقع المشفرة',message1)
		message2 = 'شهادة التشفير هي ملف يحتوي على شفرة خاصة او تواقيع خاصة لشركات معروفة وله تاريخ صلاحية ونفاذ والغرض منه هو تبادل المعلومات بطريقة مشفرة يصعب اختراقها وفهمها'
		xbmcgui.Dialog().ok('شهادة التشفير - SSL Certificate',message2)

	elif mode==153:
		yes = xbmcgui.Dialog().yesno('روابط لا تعمل','غالبا السبب هو من الموقع الاصلي المغذي للبرنامج وللتأكد تستطيع اخبار المبرمج بجميع التفاصيل فهل تريد اخبار المبرمج الان ؟')	
		if yes: 
			from PROGRAM import MAIN as PROGRAM_MAIN
			PROGRAM_MAIN(2)

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

	return
		

