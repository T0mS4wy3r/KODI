# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from LIBRARY import *

script_name='MENUS'

def MAIN(mode,url,text=''):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==260: results = MENU()
	elif mode==261: results = WEBSITES_MENU()
	elif mode==262: results = GLOBAL_SEARCH_MENU(text,True)
	elif mode==263: results = ANSWERS_MENU()
	elif mode==264: results = SERVICES_MENU()
	elif mode==265: results = LAST_VIDEOS_MENU(text)
	elif mode==266: results = DELETE_LAST_VIDEOS_MENU(text)
	else: results = False
	return results

def MENU():
	#addMenuItem('video','Testing - watched enabled','',179)
	#addMenuItem('live','Testing - watched disabled','',179)
	addMenuItem('folder','[COLOR FFC89008]  1.  [/COLOR]'+'مواقع هذا البرنامج','',261)
	addMenuItem('folder','[COLOR FFC89008]  2.  [/COLOR]'+'مواقع يوتيوب من يوتيوب','https://www.youtube.com/feed/guide_builder',144)
	addMenuItem('folder','[COLOR FFC89008]  3.  [/COLOR]'+'مواقع يوتيوب من البرنامج','',290)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]  4.  [/COLOR]'+'قائمة القنوات','',100)
	addMenuItem('folder','[COLOR FFC89008]  5.  [/COLOR]'+'قائمة الاقسام','',165,'','','SITES')
	addMenuItem('folder','[COLOR FFC89008]  6.  [/COLOR]'+'قائمة العشوائية','',160)
	addMenuItem('folder','[COLOR FFC89008]  7.  [/COLOR]'+'بحث بجميع المواقع','',262,'','','NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]  8.  [/COLOR]'+'الفيديوهات المحملة','',330)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]  9.  [/COLOR]'+'قائمة اشتراك IPTV','',230)
	addMenuItem('folder','[COLOR FFC89008]10.  [/COLOR]'+'IPTV قائمة أقسام الـ','',165,'','','IPTV')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]11.  [/COLOR]'+'قائمة المفضلة 1','',270,'','','','1')
	addMenuItem('folder','[COLOR FFC89008]12.  [/COLOR]'+'قائمة المفضلة 2','',270,'','','','2')
	addMenuItem('folder','[COLOR FFC89008]13.  [/COLOR]'+'قائمة المفضلة 3','',270,'','','','3')
	addMenuItem('folder','[COLOR FFC89008]14.  [/COLOR]'+'قائمة المفضلة 4','',270,'','','','4')
	addMenuItem('folder','[COLOR FFC89008]15.  [/COLOR]'+'قائمة المفضلة 5','',270,'','','','5')
	addMenuItem('folder','[COLOR FFC89008]16.  [/COLOR]'+'آخر 50 فيديو تم تشغيلها','',265,'','','video')
	addMenuItem('folder','[COLOR FFC89008]17.  [/COLOR]'+'آخر 50 قناة تم تشغيلها','',265,'','','live')
	addMenuItem('folder','[COLOR FFC89008]18.  [/COLOR]'+'آخر 50 مجلد تم فتحها','',265,'','','folder')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('link','[COLOR FFC89008]19.  [/COLOR]'+'تقرير عن آخر التغييرات','',199)
	addMenuItem('link','[COLOR FFC89008]20.  [/COLOR]'+'تقرير عن استخدام البرنامج','',176)
	addMenuItem('link','[COLOR FFC89008]21.  [/COLOR]البرنامج إصدار رقم ( '+addon_version+' )','',7)
	#addMenuItem('folder','[COLOR FFC89008]10.  [/COLOR]'+'ـ Services Menu  قائمة الخدمات','',172)
	#addMenuItem('folder','  4.  [COLOR FFC89008]ـ Services Menu  قائمة الخدمات[/COLOR]','',264)
	#addMenuItem('link','  5.  [COLOR FFC89008]البرنامج إصدار رقم ('+addon_version+')[/COLOR]','',7)
	addMenuItem('folder','[COLOR FFC89008]22.  [/COLOR]ـ Answers Menu  قائمة الاجوبة','',263)
	addMenuItem('folder','[COLOR FFC89008]23.  [/COLOR]ـ Services Menu  قائمة الخدمات','',264)
	addMenuItem('link','[COLOR FFC89008]24.  [/COLOR]ـ Contact Me  كيف تتصل بالمبرمج','',196)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return

def WEBSITES_MENU():
	#addMenuItem('folder','  1.  [COLOR FFC89008]TV    [/COLOR]'+'قنوات تلفزيونية','',100)
	#addMenuItem('folder','  2.  [COLOR FFC89008]IPT   [/COLOR]'+'اشتراك IPTV مدفوع','',230)
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات خاصة - قليلة المشاكل[/COLOR]','',157)
	addMenuItem('folder','[COLOR FFC89008]PNT  [/COLOR]'+'موقع بانيت','',30)
	addMenuItem('folder','[COLOR FFC89008]YUT  [/COLOR]'+'موقع يوتيوب','',140)
	addMenuItem('folder','[COLOR FFC89008]KLA  [/COLOR]'+'موقع كل العرب','',10)
	addMenuItem('folder','[COLOR FFC89008]AKW [/COLOR]'+'موقع أكوام الجديد','',240)
	addMenuItem('folder','[COLOR FFC89008]SHF  [/COLOR]'+'موقع شوف ماكس','',50)
	addMenuItem('folder','[COLOR FFC89008]KRB  [/COLOR]'+'موقع قناة كربلاء','',320)
	addMenuItem('folder','[COLOR FFC89008]KWT  [/COLOR]'+'موقع قناة الكوثر','',130)
	addMenuItem('folder','[COLOR FFC89008]IFL    [/COLOR]'+'موقع قناة آي فيلم','',20)
	addMenuItem('folder','[COLOR FFC89008]MRF  [/COLOR]'+'موقع قناة المعارف','',40)
	addMenuItem('folder','[COLOR FFC89008]SHV  [/COLOR]'+'موقع صوت الشيعة','',310)
	addMenuItem('folder','[COLOR FFC89008]FTM  [/COLOR]'+'موقع المنبر الفاطمي','',60)
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات خاصة وعامة - كثيرة المشاكل[/COLOR]','',157)
	addMenuItem('folder','[COLOR FFC89008]CMN  [/COLOR]'+'موقع سيما ناو','',300)
	addMenuItem('folder','[COLOR FFC89008]ARS  [/COLOR]'+'موقع عرب سييد','',250)
	addMenuItem('folder','[COLOR FFC89008]AKO  [/COLOR]'+'موقع أكوام القديم','',70)
	addMenuItem('folder','[COLOR FFC89008]EGV  [/COLOR]'+'موقع إيجي بيست vip','',220)    # 220
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات عامة - كثيرة المشاكل[/COLOR]','',157)
	addMenuItem('folder','[COLOR FFC89008]ARL  [/COLOR]'+'موقع عرب ليونز','',200)
	addMenuItem('folder','[COLOR FFC89008]SHA  [/COLOR]'+'موقع شاهد فوريو','',110)
	addMenuItem('folder','[COLOR FFC89008]HEL  [/COLOR]'+'موقع هلال يوتيوب','',90)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#addMenuItem('folder','16.  [COLOR FFC89008]HLA  [/COLOR]'+'موقع هلا سيما','',88) # 80
	#addMenuItem('folder','17.  [COLOR FFC89008]SFW  [/COLOR]'+'موقع سيريس فور وتش','',218)  # 210
	#addMenuItem('folder','18.  [COLOR FFC89008]MVZ  [/COLOR]'+'موقع موفيزلاند اونلاين','',188) # 180
	#addMenuItem('folder','19.  [COLOR FFC89008]EGB  [/COLOR]'+'موقع ايجي بيست','',128) # 120
	return

def SERVICES_MENU():
	#addMenuItem('folder','[COLOR FFC89008]ـ Problems & Questions  قائمة مشاكل وأسئلة  .1 [/COLOR]','',264)
	#addMenuItem('link','[COLOR FFC89008]  2.  [/COLOR]'+'فحص جميع مواقع البرنامج','',175)
	addMenuItem('link','[COLOR FFC89008]  1.  [/COLOR]'+'No Arabic letters (or text)','',151)
	addMenuItem('link','[COLOR FFC89008]  2.  [/COLOR]'+'مسح كاش البرنامج','',9)
	addMenuItem('link','[COLOR FFC89008]  3.  [/COLOR]'+'تحديث جميع إضافات كودي','',159)
	addMenuItem('link','[COLOR FFC89008]  4.  [/COLOR]'+'تغيير مكان تحميل الفيديوهات','',332)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('link','[COLOR FFC89008]  5.  [/COLOR]'+'إرسال رسالة إلى المبرمج','',2,'','','')
	addMenuItem('link','[COLOR FFC89008]  6.  [/COLOR]'+'إبلاغ المبرمج بوجود مشكلة','',2,'','','PROBLEM')
	addMenuItem('link','[COLOR FFC89008]  7.  [/COLOR]'+'إرسال سجل الأخطاء والاستخدام','',2,'','','PROBLEM')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('link','[COLOR FFC89008]  8.  [/COLOR]'+'فحص وتفعيل مخزن عماد','',172)
	addMenuItem('link','[COLOR FFC89008]  9.  [/COLOR]'+'فحص وتفعيل فيديوهات mpd','',173)
	addMenuItem('link','[COLOR FFC89008]10.  [/COLOR]'+'فحص وتفعيل فيديوهات rtmp','',174)
	addMenuItem('link','[COLOR FFC89008]11.  [/COLOR]'+'فحص الإصدار الأخير والتحديثات','',7)
	addMenuItem('link','[COLOR FFC89008]12.  [/COLOR]'+'فحص اتصال المواقع المشفرة','',4)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('link','[COLOR FFC89008]13.  [/COLOR]'+'إعدادات واجهة كودي','',6)
	addMenuItem('link','[COLOR FFC89008]14.  [/COLOR]'+'إعدادات ResolveURL','',177)
	addMenuItem('link','[COLOR FFC89008]15.  [/COLOR]'+'إعدادات Youtube-DL','',178)
	addMenuItem('link','[COLOR FFC89008]16.  [/COLOR]'+'إعدادات Inputstream Adaptive','',5)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return

def ANSWERS_MENU():
	addMenuItem('link','[COLOR FFC89008]  1.  [/COLOR]'+'No Arabic letters (or text)','',151)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('link','[COLOR FFC89008]  2.  [/COLOR]'+'بعض الروابط بطيئة','',155)
	addMenuItem('link','[COLOR FFC89008]  3.  [/COLOR]'+'بعض الروابط لا تعمل','',153)
	addMenuItem('link','[COLOR FFC89008]  4.  [/COLOR]'+'كيفية استخدام المفضلة','',150)
	addMenuItem('link','[COLOR FFC89008]  5.  [/COLOR]'+'المواقع المشفرة لا تعمل','',152)
	addMenuItem('link','[COLOR FFC89008]  6.  [/COLOR]'+'كيفية مسح محتويات قائمة','',170)
	addMenuItem('link','[COLOR FFC89008]  7.  [/COLOR]'+'لماذا بعض المواقع لا تعمل','',195)
	addMenuItem('link','[COLOR FFC89008]  8.  [/COLOR]'+'تحذير يخص شهادة التشفير','',171)
	addMenuItem('link','[COLOR FFC89008]  9.  [/COLOR]'+'ما هي افضل واجهة للبرنامج','',197)
	addMenuItem('link','[COLOR FFC89008]10.  [/COLOR]'+'لماذا يوجد سيرفرات مجهولة','',156)
	addMenuItem('link','[COLOR FFC89008]11.  [/COLOR]'+'الفيديوهات نوع mpd لا تعمل','',194)
	addMenuItem('link','[COLOR FFC89008]12.  [/COLOR]'+'لماذا لا نفحص شهادة التشفير','',193)
	addMenuItem('link','[COLOR FFC89008]13.  [/COLOR]'+'بعض الفيديوهات بطيئة وتقطع','',158)
	addMenuItem('link','[COLOR FFC89008]14.  [/COLOR]'+'كيف تحل بنفسك مشكلة مؤقته','',192)
	addMenuItem('link','[COLOR FFC89008]15.  [/COLOR]'+'كيف تستخدم الريموت مع كودي','',198)
	addMenuItem('link','[COLOR FFC89008]16.  [/COLOR]'+'كيف تتصل وتتواصل مع المبرمج','',196)
	addMenuItem('link','[COLOR FFC89008]17.  [/COLOR]'+'ما هو آخر إصدار لكودي وللبرنامج','',7)
	addMenuItem('link','[COLOR FFC89008]18.  [/COLOR]'+'ما هي السيرفرات العامة والخاصة','',157)
	addMenuItem('link','[COLOR FFC89008]19.  [/COLOR]'+'ما معنى هذه العلامات بالبرنامج ,'+escapeUNICODE('\u02d1')+';','',191)
	addMenuItem('link','[COLOR FFC89008]20.  [/COLOR]'+'ما هو الكاش وكم مقداره بالبرنامج','',190)
	addMenuItem('link','[COLOR FFC89008]21.  [/COLOR]'+'كيف تحل مشكلة حجب بعض المواقع','',195)
	addMenuItem('link','[COLOR FFC89008]22.  [/COLOR]'+'DMCA  قانون الألفية للملكية الرقمية','',3)
	addMenuItem('link','[COLOR FFC89008]23.  [/COLOR]'+'أين مواقع الأفلام والمسلسلات الأجنبية','',154)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return

def GLOBAL_SEARCH_MENU(search='',show=True):
	search = search.replace('NOUPDATE','')
	if search=='': search = KEYBOARD()
	if search=='': return
	LOG_THIS('NOTICE',LOGGING(script_name)+'   .  Global Search For: [ '+search+' ]')
	search = search.lower()
	if show: search2 = search
	else: search2 = 'كلمة عشوائية'
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات خاصة - قليلة المشاكل[/COLOR]','',157)
	addMenuItem('folder','[COLOR FFC89008]IPT    [/COLOR]'+search2+' - خدمة IPTV','',239,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]PNT   [/COLOR]'+search2+' - موقع بانيت','',39,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]YUT   [/COLOR]'+search2+' - موقع يوتيوب','',149,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]KLA   [/COLOR]'+search2+' - موقع كل العرب','',19,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]AKW [/COLOR]'+search2+' - موقع أكوام الجديد','',249,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]SHF   [/COLOR]'+search2+' - موقع شوف ماكس','',59,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]KRB  [/COLOR]'+search2+' - موقع قناة كربلاء','',329,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]KWT  [/COLOR]'+search2+' - موقع قناة الكوثر','',139,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]IFL    [/COLOR]'+search2+' - موقع قناة آي فيلم','',29,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]MRF  [/COLOR]'+search2+' - موقع قناة المعارف','',49,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]SHV  [/COLOR]'+search2+' - موقع صوت الشيعة','',319,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]FTM   [/COLOR]'+search2+' - موقع المنبر الفاطمي','',69,'','',search+'NOUPDATE')
	#addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات خاصة وعامة - كثيرة المشاكل[/COLOR]','',157)
	addMenuItem('folder','[COLOR FFC89008]CMN  [/COLOR]'+search2+' - موقع سيما ناو','',309,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]ARS  [/COLOR]'+search2+' - موقع عرب سييد','',259,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]AKO  [/COLOR]'+search2+' - موقع أكوام القديم','',79,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]EGV  [/COLOR]'+search2+' - موقع إيجي بيست vip','',229,'','',search+'NOUPDATE')
	#addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات عامة - كثيرة المشاكل[/COLOR]','',157)
	addMenuItem('folder','[COLOR FFC89008]ARL  [/COLOR]'+search2+' - موقع عرب ليونز','',209,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]SHA  [/COLOR]'+search2+' - موقع شاهد فوريو','',119,'','',search+'NOUPDATE')
	addMenuItem('folder','[COLOR FFC89008]HEL  [/COLOR]'+search2+' - موقع هلال يوتيوب','',99,'','',search+'NOUPDATE')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#addMenuItem('folder','16. [COLOR FFC89008]HLA  [/COLOR]'+search+' - موقع هلا سيما','',88,'','',search) # 89
	#addMenuItem('folder','17. [COLOR FFC89008]SFW  [/COLOR]'+search+' - موقع سيريس فور وتش','',218,'','',search) # 219
	#addMenuItem('folder','18. [COLOR FFC89008]MVZ  [/COLOR]'+search+' - موقع موفيز لاند','',188,'','',search)# 189
	#addMenuItem('folder','19. [COLOR FFC89008]EGB  [/COLOR]'+search+' - موقع ايجي بيست','',128,'','',search)# 129
	return

def LAST_VIDEOS_MENU(type,lengthonly=False):
	#addMenuItem('folder','مسح هذه القائمة','',266,'','',type)
	#addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	videoLIST = []
	if os.path.exists(lastvideosfile):
		with open(lastvideosfile,'r') as f: listFILE = f.read()
		listFILE = eval(listFILE)
		if type in listFILE.keys():
			videoLIST = listFILE[type]
			if not lengthonly:
				try:
					for type2,name,url,mode2,image,page,text in videoLIST:
						addMenuItem(type2,name,url,mode2,image,page,text)
				except:
					xbmcgui.Dialog().ok('رسالة من المبرمج','هناك مشكلة في ملف آخر الفيديوهات','لكي تتخلص من المشكلة اضغط على','"مسح هذه القائمة"')
	return len(videoLIST)

def DELETE_LAST_VIDEOS_MENU(type):
	answer = xbmcgui.Dialog().yesno('رسالة من المبرمج','هل تريد فعلا مسح جميع محتويات قائمة آخر 50 '+TRANSLATE(type)+' ؟!','','','كلا','نعم')
	if answer:
		if os.path.exists(lastvideosfile):
			with open(lastvideosfile,'r') as f: listFILE = f.read()
			listFILE = eval(listFILE)
			if type in listFILE.keys():
				del listFILE[type]
				listFILE = str(listFILE)
				with open(lastvideosfile,'w') as f: f.write(listFILE)
				xbmcgui.Dialog().ok('رسالة من المبرمج','تم مسح جميع محتويات قائمة آخر 50 '+TRANSLATE(type))
	LAST_VIDEOS_MENU(type)
	return



