# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='YTB_CHANNELS'
menu_name='_YTC_'

def MAIN(mode,url,page,text):
	if   mode==290: results = MENU(url)
	elif mode==291: results = ITEMS(text,page)
	elif mode==292: results = MODIFY()
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('link',menu_name+'[COLOR FFC89008]إضافة وحذف مواقع من هذه القائمة[/COLOR]','',292)
		#addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	#XBMCGUI_DIALOG_OK(website,str(YTB_CHANNELS))
	for seq in range(len(YTB_CHANNELS)):
		name = YTB_CHANNELS[seq][0]
		if website!='': name = name.replace('مواقع','')
		addMenuItem('folder',website+'___'+menu_name+name,'',291,'',website,str(seq))
	return

def ITEMS(seq,website=''):
	#XBMCGUI_DIALOG_OK(website,str(seq))
	if website=='':
		addMenuItem('link',menu_name+'[COLOR FFC89008]إضافة وحذف مواقع من هذه القائمة[/COLOR]','',292)
		#addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	seq = int(seq)
	del YTB_CHANNELS[seq][0]
	for title,url in YTB_CHANNELS[seq]:
		addMenuItem('folder',menu_name+title,url,144)
	return

def MODIFY():
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','هذه القائمة اختيرت عشوائيا والمبرمج لا يعرف أصحابها . للمساهمة في تغييرها . قم بمراسلة المبرمج من قائمة خدمات البرنامج . وأعلم أن للمبرمج كامل الحرية في قبول طلبك أو رفضه')
	send = XBMCGUI_DIALOG_YESNO('رسالة من المبرمج','لإضافة أو حذف موقع أو قسم . قم بكتابة أسم ورابط الموقع أو القسم الذي تريد إضافته أو حذفه علما أن المواقع ذات الأسماء الشخصية أو ذات الفيديوهات القليلة مرفوضة . هل تريد الآن أن ترسل رسالة إلى المبرمج ؟!','','','كلا','نعم')
	if send:
		import SERVICES
		SERVICES.SEND_MESSAGE()
	return





YTB_CHANNELS = [


['مواقع افلام'
,('Aflam'								,'https://www.youtube.com/c/Aflam')
,('مصر اونلاين افلام - Masr Online Aflam'	,'https://www.youtube.com/channel/UCPWO-qQdxskpq2awKqQHmew')
,('افلام عربى - Aflam 3raby'				,'https://www.youtube.com/channel/UC4JTDDLe7CMaQ7ZbtcfMxvA')
,('افلام رعب واكشن'						,'https://www.youtube.com/channel/UC0K6YUd5AqAj5KTut4nSj0A')
,('افلام محترمة'							,'https://www.youtube.com/c/mim21889aflammo7trama')
,('alyelbasl'							,'https://www.youtube.com/user/alyelbasl')
,('افلام رعب'							,'https://www.youtube.com/channel/UCjTzLhZLUUqWlU_JIx52c6g')
,('أفلام زمان - Aflam Zaman'				,'https://www.youtube.com/channel/UCozlTUSFGUiRKvrFeCEgVOw')
,('أفلام زمان Aflam Zaman'				,'https://www.youtube.com/channel/UCoYwO1pckaNTqm4eLR0M1xQ')
,('افلام الغرب'							,'https://www.youtube.com/channel/UCH1AcZHgW0nch9CBETZd7dw')
,('MDM Aflam - إم دي إم أفلام'			,'https://www.youtube.com/channel/UCONjV3OIpCXtBG27TldgGYQ')
,('MDM Classic - إم دي إم كلاسيك'		,'https://www.youtube.com/channel/UC_2Uh65J98i2Hl2BguGpiaQ')
,('سناب ميديا افلام - Snap Media Movies'	,'https://www.youtube.com/channel/UCK27DSJGcNnbomvnTmto39Q')
]



,['مواقع للأطفال'
,('افلام كرتون كيدو'						,'https://www.youtube.com/channel/UCEof7Z2iOP48t9a0HYoek7A')
,('كارتون الزمن الجميل Cartoon Zaman'	,'https://www.youtube.com/channel/UC-1wxEg-_tPAd5OA_2aa86A')
,('ماشا و الدب'							,'https://www.youtube.com/channel/UCpm9UA5N0Y9Kv1FJNtnNlJA')
,('Fanar Production - فنر برودكشن'		,'https://www.youtube.com/Shaabia')
,('مسلسلات وأفلام كرتون بالعربية'			,'https://www.youtube.com/user/arabickidschannel')
,('كنز دراما الأطفال'					,'https://www.youtube.com/channel/UCb3zTnPA1QwdHPGwbo-9bag')
,('الأيادي الصغيرة كتاب تلوين - Arabic'	,'https://www.youtube.com/channel/UCFGT9nAZTvuiS_51cTK2Kog')
,('Arabian Fairy Tales'					,'https://www.youtube.com/c/ArabianFairyTales')
,('الشاحنة الخارقة - مدينة السيارات'	,'https://www.youtube.com/channel/UCMrkbPKagiOY5tGvIk5-1_w')
,('تعلم الرسم و التلوين تلفزيون اللأطفال - Arabic'		,'https://www.youtube.com/channel/UCFBZOFHWS6KzfUhPAEy1gAQ')
,('قصص الاطفال باللغة العربية - Arabian Fairy Tales'		,'https://www.youtube.com/channel/UCWlrq6k6eaDHUcyroV4aw3Q')
,('الأطفال السعداء أغاني الأطفال Arabic Kids Songs'		,'https://www.youtube.com/c/الأطفالالسعداءنغماتروضةالأطفال')
,('Arabic Fairy Tales for Kids - قصص اطفال'				,'https://www.youtube.com/c/smartkidstvarabicArabicFairyTales')
]



,['مواقع برامج وثائقية'
,('Nat Geo Abu Dhabi'					,'https://www.youtube.com/c/natgeoabudhabime')
,('DW Documentary وثائقية دي دبليو'		,'https://www.youtube.com/c/dwdocarabia')
,('جرائم الارهاب في العراق'				,'https://www.youtube.com/user/PhotosterrorismIraq')
,('متع عقلك | حقائق'					,'https://www.youtube.com/channel/UCQ0imqAHB4pJWvIih3xTH5A')
,('متع عقلك | شخصيات'					,'https://www.youtube.com/channel/UCjYuzWEBTpM4llxH0mLNLGw')
,('Al Jazeera Documentary الجزيرة الوثائقية'			,'https://www.youtube.com/user/aljazeeradoc')
]



,['مواقع مسرحيات'
,('MDM Masrahiyat - إم دي إم مسرحيات'	,'https://www.youtube.com/channel/UCQyNn_GQ_UCwHoAoQwOG0Pg')
,('كنز المسرحيات والدراما'				,'https://www.youtube.com/channel/UCKn4VQbbX6UlhEtLCLVgsRQ')
]



,['مواقع مسلسلات'
,('WatanNetwork - شبكة وطن'				,'https://www.youtube.com/user/WatanNetwork')
,('Sham Drama شام دراما'				,'https://www.youtube.com/channel/UC24ILr30tJeVf9H5dCMHV4g')
,('MBC DRAMA'							,'https://www.youtube.com/c/MBCDrama')
,('Roya Drama'							,'https://www.youtube.com/user/RoyaDrama')
,('Alhayah Series TV'					,'https://www.youtube.com/c/AlHayahSeriesTV')
,('Shoof Drama | شوف دراما'				,'https://www.youtube.com/channel/UCgd_tWU4X7s10DKdgt-XDNQ')
,('شوف دراما الثانية • Shoof Drama 2'	,'https://www.youtube.com/channel/UC25ZB5ZMqLQwxFDV9FHvF8g')
,('شوف دراما الثالثة - Shoof Drama 3'	,'https://www.youtube.com/channel/UCQOz2_AhxeHUbNMYan-6ZQQ')
,('كنز التلفزيون TV Kanaz'				,'https://www.youtube.com/channel/UCPCvJob5Fraqn2Mc5UNdLAA')
,('مسلسلات عربى'							,'https://www.youtube.com/channel/UC5F1StguaaE1cTYWniTdBXg')
,('مسلسلات لاتنية و تركية'				,'https://www.youtube.com/channel/UCFZnmr3kXPe_qh6X0prImBw')
,('مسلسلات تركية Arabic Series'			,'https://www.youtube.com/channel/UC9v0-V3lhqArm0Ysy52OTTw')
]



,['مواقع قنوات فضائية اسلامية'
,('قناة كربلاء الفضائية'					,'https://www.youtube.com/user/karbalatvchannel')
,('قناة الحجة الفضائية'					,'https://www.youtube.com/c/قناةالحجةالفضائية')
,('Imam Hussein TV 2'					,'https://www.youtube.com/c/imamhussein2tv')
,('imam hussein tv4'					,'https://www.youtube.com/c/imamhusseintv4')
,('قناة القران الكريم الفضائية'			,'https://www.youtube.com/channel/UCqAbG6ft9Px-wNrCs0lBIHw')
,('FADAK TV'							,'https://www.youtube.com/c/fadaktv')
,('ALKafeelMedia'						,'https://www.youtube.com/c/ALKafeelMedia')
,('قناة الجوادين'						,'https://www.youtube.com/c/AljawadainTV')
,('IMAM ALI TV فضائية العتبة العلوية المقدسة'			,'https://www.youtube.com/c/IMAMALISHRINETV')
,('قناة الامام الحسين عليه السلام الفضائية للمقتطفات'		,'https://www.youtube.com/channel/UCmQ5UbWQl51mjIg3JbUmUcA')
]



,['مواقع قنوات فضائية عامة'
,('قناة دجلة الفضائية'					,'https://www.youtube.com/c/DijlahTv')
,('قناة نبأ الفضائية'					,'https://www.youtube.com/c/NabaaTV')
,('AlHayah TV Network'					,'https://www.youtube.com/c/AlHayah1TV')
,('Alsharqiya Tube'						,'https://www.youtube.com/c/AlsharqiyaTube')
,('MBC BOLLYWOOD'						,'https://www.youtube.com/c/mbcbollywood')
,('MBC Action'							,'https://www.youtube.com/c/MBCAction')
,('MBC MAX'								,'https://www.youtube.com/c/mbcmax')
,('MBC مصر'								,'https://www.youtube.com/c/MBCMASRtv')
,('MBC MASR 2'							,'https://www.youtube.com/c/MBCMASR2tv')
,('MBC IRAQ'							,'https://www.youtube.com/channel/UCOSY1uNYaW53aQgLE8YcozQ')
,('MBC1'								,'https://www.youtube.com/c/MBC1')
,('MBC2'								,'https://www.youtube.com/channel/UCC22GST1xmjAYNs8D_n6Vyw')
,('MBC3'								,'https://www.youtube.com/channel/UC12YWO1LML5RFbf7dPvfJWA')
,('MBC4'								,'https://www.youtube.com/c/MBC4')
,('MBC5'								,'https://www.youtube.com/channel/UCVad7F4_ZuILXyBsBj-WEnQ')
,('Arab news broadcasting'				,'https://www.youtube.com/c/AnbIraq')
,('DW عربية'							,'https://www.youtube.com/c/dwarabic')
,('Roya Comedy'							,'https://www.youtube.com/c/RoyaComedy')
,('Roya TV'								,'https://www.youtube.com/c/royatv')
,('SharqiyaTube'						,'https://www.youtube.com/user/SharqiyaTube')
,('mtvlebanon'							,'https://www.youtube.com/user/mtvlebanon')
,('تلفزيون أورينت Orient TV'			,'https://www.youtube.com/c/OrientNews')
,('سكاي نيوز عربية'						,'https://www.youtube.com/c/SkyNewsArabia')
,('قناة آسيا - Asia TV'					,'https://www.youtube.com/user/Asiasatonline')
]



,['مواقع قنوات فضائية اخبارية'
,('Fadak News Net'						,'https://www.youtube.com/c/FadakNewsNetwork')
,('BBC News عربي'						,'https://www.youtube.com/c/bbcarabic')
,('RT Arabic'							,'https://www.youtube.com/user/RTarabic')
,('MTVLebanonNews'						,'https://www.youtube.com/user/MTVLebanonNews')
]



,['مواقع القرآن الكريم'
,('موقع الشيخ عبد الباسط عبد الصمد'		,'https://www.youtube.com/user/ABD0LBASIT60HIZB')
,('القرآن باصوات شيعية'					,'https://www.youtube.com/user/ShiaTelawa')
,('قناة الشيخ كشك'						,'https://www.youtube.com/c/kichk1933')
,('دار القرآن الكريم'					,'https://www.youtube.com/c/daralquran1')
,('صوت السماء الشيخ عبد الباسط عبد الصمد رحمه الله'		,'https://www.youtube.com/channel/UCNSvXqML7vSjEJZ8Yk9Ub8A')
,('مركز القرآن الكريم في العتبة العلوية المقدسة'		,'https://www.youtube.com/c/quranimamali')
]



,['مواقع العتبات المقدسة'
,('العتبة العباسية المقدسة'				,'https://www.youtube.com/user/alkafeelnet')
,('العتبة الحسينية المقدسة'				,'https://www.youtube.com/c/العتبةالحسينيةالمقدسة')
,('Imam Ali Holy Shrine'				,'https://www.youtube.com/c/ImamAliNet')
,('Imam Ali العتبة العلوية المقدسة'		,'https://www.youtube.com/channel/UCwrw_LVjq6k5q7Q_M2ChtVg')
,('العتبة العسكرية المقدسة /Al-Aaskari Holy Shrine'		,'https://www.youtube.com/channel/UCVHMwTQ7lsfqCzTzCVsW69A')
]



,['مواقع محاضرات اسلامية'
,('العلامة الشيخ عبدالحميد المهاجر'		,'https://www.youtube.com/c/Al-muhajir')
,('الشيخ محمد الأسدي'					,'https://www.youtube.com/c/الشيخمحمدالأسدي')
,('صوتيات تراث المنبر الأحسائي'			,'https://www.youtube.com/user/alradodali')
,('اتحاد خدام المهدي عليه السلام'		,'https://www.youtube.com/c/ddrricky')
,('طريق السلام'							,'https://www.youtube.com/channel/UCMNtOiJtS9TyAQBE445Rt_w')
,('يوتيوب رافضي'						,'https://www.youtube.com/channel/UCxYg8GbfJqKOobXDV4deKxw')
,('قصص مضيئة Luminous stories'			,'https://www.youtube.com/c/Luminousstories')
,('قناة الشيخ أحمد ديدات'				,'https://www.youtube.com/c/Come2heavenar')
,('موقع تراث الشيعة - أبوأحمد السليمان'	,'https://www.youtube.com/channel/UCepM6-Ps02B5JSNUPZa8vKQ')
,('أدوية القلب والروح'					,'https://www.youtube.com/channel/UC56S39mFs0xhkxj53uaWd5w')
]



,['مواقع فقه اسلامي'
,('شبكة فقه الشيعة'						,'https://www.youtube.com/c/faqahalshia')
,('إرشادات فقهية'						,'https://www.youtube.com/channel/UCe-6xsNGzeRsAxAWb8DD9dw')
,('قسم الشؤون الدينية - العتبة العلوية المقدسة'			,'https://www.youtube.com/channel/UCCN7aqmU3riapaOUZIOEYnw')
]



,['مواقع نواعي ورواديد'
,('أسفار الغدير'						,'https://www.youtube.com/c/Alghadeer313')
,('Basim Karbalaei / باسم الكربلائي'		,'https://www.youtube.com/c/BasimKarbalaei')
,('جواهر الشيعة'						,'https://www.youtube.com/c/جواهرالشيعة')
,('جروب ميديا - Ahlaa Group'			,'https://www.youtube.com/channel/UCqdzqjOEMEC1WwwMuYkfJQA')
,('صدى الخليج للانتاج والتوزيع الفني'	,'https://www.youtube.com/channel/UCHlHdqvnFavr79iMasmcmtg')
,('قناة الشموسي للقصائد الحسينية القديمة'				,'https://www.youtube.com/channel/UCXFx82kAyIQ29OP76ueXbBg')
]



,['مواقع إسلاميه منوعة'
,('Hussein Media حسين ميديا'			,'https://www.youtube.com/channel/UCOq26pLeUkO-x32IXCPUgzg')
,('مدينة الحكمة'						,'https://www.youtube.com/c/Hekm01')
,('AlmustafaChannel1'					,'https://www.youtube.com/user/AlmustafaChannel1')
,('Shia4media ناصر الحجة'				,'https://www.youtube.com/user/shia4media')
,('مركز الاشعاع الاسلامي'					,'https://www.youtube.com/c/Islam4u')
,('شبكة الرصد الشيعية'					,'https://www.youtube.com/channel/UCchyPwzTX3xV-ZaT4SrRTiw')
,('مؤسسة علوم نهج البلاغة'				,'https://www.youtube.com/c/مؤسسةعلومنهجالبلاغة')
,('حقيبة المؤمن'						,'https://www.youtube.com/c/HaqybatElmomen')
,('قناة القائم'							,'https://www.youtube.com/user/MrMuh25')
,('شبكة صوت الشيعة - Shia Voice'		,'https://www.youtube.com/channel/UCNNV5nxxla7jwuyGtp6pIVA')
,('شيعة العالم 1'						,'https://www.youtube.com/channel/UCkZpr2hhOEZhwlVNnVDQGIQ')
,('im shia أنا شيعي'					,'https://www.youtube.com/channel/UCyxj5ipESwweiR5z7iFKrOw')
,('قناة المنتقم عليه السلام'				,'https://www.youtube.com/channel/UCPeWl8zkFVQjiP9pPv8fTUg')
,('الشيعة Al-Shiaa'						,'https://www.youtube.com/channel/UCaYxqB74OwKlhGciwU-MS7Q')
,('الحسن المجتبى عليه السلام'			,'https://www.youtube.com/channel/UCxTzs6wTdd60JFZ4lcNtATg')
,('العلم النافع hd'						,'https://www.youtube.com/channel/UC1GTIPYpXDfqKya2ENvmEoA')
,('اسلاميات hd'							,'https://www.youtube.com/c/Uslameyat1')
,('التاريخ الأسلامى'						,'https://www.youtube.com/c/التاريخالأسلامى1')
,('الرحال علوم ودين'					,'https://www.youtube.com/c/AlRehal')
,('الدروس الحوزوية العتبة العلوية المقدسة'				,'https://www.youtube.com/user/imamalinj')
]



,['مواقع نقاش أديان ومذاهب وعقائد'
,('قناة الحقيقة'						,'https://www.youtube.com/c/قناةالحقيقة')
,('للباحثين عن الحقيقة من السنة والشيعة'				,'https://www.youtube.com/user/BaseemIRAQ14')
,('المستبصرون يتحدثون اليكم بالصوت والصورة'				,'https://www.youtube.com/user/Mustabsroon')
]



,['مواقع اغاني وموسيقى'
,('Moseeqa TV موسيقي تي في'				,'https://www.youtube.com/moseeqaTV')
,('Rotana '								,'https://www.youtube.com/c/rotanaaudio')
,('Music Al Haneen | ميوزك الحنين'		,'https://www.youtube.com/c/MusicAlHaneen')
,('انا اصدق الموسيقى'					,'https://www.youtube.com/c/Ibelieveinmusic')
,('هاوي موسيقى'							,'https://www.youtube.com/c/هاويموسيقى')
,('Music Nabeel nl'						,'https://www.youtube.com/c/MusicNabeelnl')
,('موسيقي ترانيم مسيحية'				,'https://www.youtube.com/channel/UCkMS7t_ruumx2ZDOrtsdkMg')
,('Umm Kulthum - ام كلثوم'				,'https://www.youtube.com/omkalthoum')
,('A7la aghani أحلى أغاني'				,'https://www.youtube.com/channel/UCfL2d97ppuqo-n9QwHQVM2Q')
,('أغاني زمان'							,'https://www.youtube.com/channel/UCIA6Zo87X5W1TQLMb2eS_zw')
,('TransTube أغاني مترجمة'				,'https://www.youtube.com/channel/UCjNd6Fo2VCjoaQAb0hKqUnA')
,('مصر اونلاين ميوزيك - Masr Online Music'				,'https://www.youtube.com/user/NaghamTone')
]



,['مواقع حقائق وغرائب'
,('M.A TUBE'							,'https://www.youtube.com/c/MATUBENET95')
,('هل تعلم؟'							,'https://www.youtube.com/channel/UCa7lQu3RM6p88h4KOfTpqWA')
,('هل تعلم؟ الرياضية'					,'https://www.youtube.com/channel/UC6I9kmGVlehae4PyqYjp4PA')
,('هل تعلم؟ علوم وتكنولوجيا'			,'https://www.youtube.com/user/Generalculture1')
,('هل تعلم؟ حصريات'						,'https://www.youtube.com/channel/UCNFMnrQNbiiI9Ktto9-n5IA')
,('أسرار'								,'https://www.youtube.com/c/أسرار1')
,('أسرار كونية'							,'https://www.youtube.com/channel/UCEF6H8IqHSxQJMYpXdOMFgQ')
,('Events and Facts'					,'https://www.youtube.com/channel/UCjqeNyFuOhAmyfpQQOdkwOQ')
,('وثائقية أحداث وحقائق روايات'			,'https://www.youtube.com/channel/UC8UMer6lHgbnj6XCNQIL-Pw')
,('AROUND WORLD !?'						,'https://www.youtube.com/c/5أغرب1')
,('غذي ذهنك | حقائق و أسرار'			,'https://www.youtube.com/channel/UCBAywmMs9FOVVbVYerdVBfw')
,('غذي ذهنك | غموض'						,'https://www.youtube.com/channel/UCSbean8UDq1L2vSeL3whLTw')
,('قرية العجائب'						,'https://www.youtube.com/c/VillageofWonders')
,('هل تعلم ! Did you know'				,'https://www.youtube.com/channel/UC3QLsqW5lI_QJXz5I_sj4dQ')
,('اليوم - Today'						,'https://www.youtube.com/channel/UCI89nC3uvqhFhYmkxbnys6w')
]



,['مواقع منوعات'
,('متع عقلك'							,'https://www.youtube.com/c/Mata33a2lak')
,('مصر اونلاين Masr Online'				,'https://www.youtube.com/c/MasrOnlineTV')
,('Arabs Got Talent'					,'https://www.youtube.com/c/ArabsGotTalent')
,('MBCTrending'							,'https://www.youtube.com/c/MBCTrending')
,('MBC GROUP'							,'https://www.youtube.com/user/mbc')
,('Shahid'								,'https://www.youtube.com/c/ShahidVOD')
,('AlHayah Network'						,'https://www.youtube.com/c/AlhayahNetwork')
,('صندوق المفاجأت'						,'https://www.youtube.com/channel/UCSHjNkzZWwZUggI5aC0YvHw')
,('أوديوهات'							,'https://www.youtube.com/channel/UCMyAMbDuTCUkG8YXwokux-g')
,('AJ+ عربي'							,'https://www.youtube.com/c/ajplusarabi')
,('قناة المجلة'							,'https://www.youtube.com/c/AlmajlaTV')
,('مجلة سيدتي'							,'https://www.youtube.com/c/Sayidaty')
,('3anakib'								,'https://www.youtube.com/user/3anakib')
,('Nafham Life Skills - نفهم مهارات الحياة'				,'https://www.youtube.com/channel/UCRYrSHVkWJAto3fXZDw-ZTg')
]



,['مواقع الدعاء'
,('قناة أدعية الشيعة'					,'https://www.youtube.com/user/ShiaDu3aa')
,('أدعية دينية مختارة'					,'https://www.youtube.com/channel/UC-c0v8cwyiDZJRXQrZ3ZVOg')
,('ادعية وسور قرأنية'					,'https://www.youtube.com/c/أدعيهوسورقرأنيه')
,('HABOUBOUSSA لطميات و اناشيد و ادعية'	,'https://www.youtube.com/channel/UC7czLILZtkEZMbdCVLdM21g')
,('ترتيل القران الكريم وبعض ادعية كتاب مفاتيح الجنان'	,'https://www.youtube.com/channel/UCRwD2UFCYFXFmt8eii6X93w')
,('دعاء الرزق ـ آيات الرزق ـ أدعية الرزق ـ جلب الرزق'	,'https://www.youtube.com/channel/UCFPeDyvCV5irgvvDEuf7IwA')
]



,['مواقع اخبار'
,('Roya News'							,'https://www.youtube.com/c/RoyaNews')
,('Erem News إرم نيوز'					,'https://www.youtube.com/channel/UCpvT09HPVoyBd4i1rHU2tVg')
,('شيعة ويفز أخبار شيعة العالم - shiawaves arabic'		,'https://www.youtube.com/channel/UCoMyr9K-PSAgf8jOVmVeKKg')
]



,['مواقع طبخ'
,('Creativethink الطبخ العربي'			,'https://www.youtube.com/c/creativethinkchannel')
,('بكل سهوله So Easy'					,'https://www.youtube.com/channel/UCU1-76h3slAix7pu3_1eoow')
,('قناة بيتي و مطبخي'					,'https://www.youtube.com/channel/UCyu4Nhb7vkKdb8_Y3ouVO_g')
]



,['مواقع علوم'
,('Egychology - ايجيكولوجي'				,'https://www.youtube.com/c/Egychology')
]



,['مواقع طبية'
,('Espitalia - الاسبتالية'				,'https://www.youtube.com/c/Espitalia')
,('فِكر تاني'							,'https://www.youtube.com/c/fekrtany')
,('تعلم الأدوية اونلاين'					,'https://www.youtube.com/channel/UCuOyd1rCi3c6VRxIL8Yjfzw')
,('أدوية صيدلية لشفاء'					,'https://www.youtube.com/channel/UCuhvHTz3ulj7VGxu0ND8hqA')
,('احذروا الادوية المزيفة والمزورة'		,'https://www.youtube.com/channel/UCFjIdHR6X-yhgYcVqLQtsZA')
,('بنك الادويه'							,'https://www.youtube.com/channel/UCvt-p3pK4U-CgHxzzeWgbEw')
]



,['مواقع رياضة'
,('Roya Sports'							,'https://www.youtube.com/c/RoyaSports')
,('متع عقلك | رياضة'					,'https://www.youtube.com/channel/UC-0XDwL94TrD3ZUJX1ZQ5xw')
,('MBC PRO SPORTS'						,'https://www.youtube.com/c/mbcprosports')
,('MED SPORT'							,'https://www.youtube.com/c/MEDTUBETV')
,('هاي سبورت'							,'https://www.youtube.com/channel/UCznXHSPIbc0P7paQQz0kBxg')
,('Saba7o Korah - صباحو كورة'			,'https://www.youtube.com/c/Saba7oKorah')
,('سيلفي سبورت'							,'https://www.youtube.com/channel/UCrMd6lrIFEniqb_J1_p_Q7g')
]



,['مواقع دروس مدرسية'
,('Nafham - نفهم'						,'https://www.youtube.com/c/nafham')
,('أكاديمية التحرير'					,'https://www.youtube.com/user/tahriracademy')
,('متمكن التاريخ و الجغرافيا'			,'https://www.youtube.com/channel/UCyJGa2QCOVb5Vc4Qc1L67TQ')
,('قناة المستقبل'						,'https://www.youtube.com/c/OstazEnglish')
,('مصر التعليمية'						,'https://www.youtube.com/c/EgyptianEducationalChannel')
,('العتبة العلوية المقدسة - شركة فيض القسيم'			,'https://www.youtube.com/c/faydalqasim')
]



,['مواقع تعلم اللغات'
,('zAmericanEnglish'					,'https://www.youtube.com/c/ZAmericanEnglish')
,('Learn English with Ehab'				,'https://www.youtube.com/c/LearnEnglishwithEhab')
,('the French language'					,'https://www.youtube.com/c/lalanguefrancaisefacile')
,('The english language'				,'https://www.youtube.com/channel/UCpTdIcP9VWqgg-GJDp98STA')
,('learn spanish with asmae'			,'https://www.youtube.com/channel/UCkIebF1pf2iRSX3e1JtQYvQ')
,('Learn English with Asmae'			,'https://www.youtube.com/c/learnenglishwithasmae')
,('معهد تعلم اللغات'					,'https://www.youtube.com/c/MubaraksvSes')
,('تعلم الانجليزية بالعربية للمبتدئين'	,'https://www.youtube.com/channel/UCqZNmd4z-FCeWhM8eNzX0Ug')
,('تعلم اللغة الفرنسية Learn French'	,'https://www.youtube.com/channel/UCfuoybNkY7Gl-q_4LfNny8w')
,('تعلم اللغة الفرنسية بالعربي للمبتدئين'				,'https://www.youtube.com/channel/UCe5p_yffntJCeq2TRY4mbeQ')
,('تعلم اللغة الانجليزية learn english 350'				,'https://www.youtube.com/c/learnenglish350')
]



,['مواقع تعليمية عامة'
,('دروس أونلاين'							,'https://www.youtube.com/c/DroosOnline4u')
,('رؤية جغرافية'						,'https://www.youtube.com/c/رويةجغرافيةللبشمهندساحمديوسف')
]



,['مواقع الادب العربي'
,('الأدب العربي'							,'https://www.youtube.com/c/الأدبالعربي1')
]



,['مواقع نقد سينمائي'
,('Film Gamed'							,'https://www.youtube.com/c/FilmGamed')
,('CINEMATOLOGY Official'				,'https://www.youtube.com/c/CINEMATOLOGYOfficial')
]



,['مواقع نسائية'
,('موسوعة حواء اليوم'					,'https://www.youtube.com/channel/UCaH-RT90-_ua_3qTPpX77gg')
]



,['مواقع تكنولوجيا'
,('قرية تكنولوجيا المستقبل'				,'https://www.youtube.com/c/قريةتكنولوجياالمستقبل')
,('غذي ذهنك | تكنولوجيا'				,'https://www.youtube.com/channel/UCz57Zzi_IdEP97QWwNUR3IA')
,('تكنولوجيا بدون تعقيد'				,'https://www.youtube.com/channel/UCx6WTRDyXUOjfmQPn73ginw')
,('كل يوم تكنولوجيا'					,'https://www.youtube.com/channel/UCpxjS5ED8KHf99YYL-mQC3w')
,('Total Tech | التكنولوجيا الشاملة'	,'https://www.youtube.com/c/Totltech')
,('تكنولوجيا الديكور'					,'https://www.youtube.com/c/تكنولوجياالديكور')
]



,['مواقع أزياء'
,('Fashion & Beauty'					,'https://www.youtube.com/c/FashionBeautyGîrl')
,('ازياء'								,'https://www.youtube.com/user/Azyyaacom')
]



,['مواقع سياحة'
,('السياحة المذهلة'						,'https://www.youtube.com/c/السياحةالمذهلة')
,('الوليد للسياحة'						,'https://www.youtube.com/c/الوليدللسياحة')
,('Syrian Tourism'						,'https://www.youtube.com/c/SyrianTourism')
,('عطلات افضل الفيديوهات السياحية'		,'https://www.youtube.com/c/otlaat')
,('Memphis Tours TV'					,'https://www.youtube.com/user/freedaysegypt')
,('سرب للسياحة والسفر'					,'https://www.youtube.com/c/ssiirb')
,('السياحي - نتشرف بمتابعتكم وتفاعلكم'	,'https://www.youtube.com/c/assiyahi')
,('seyahaa سياحة'						,'https://www.youtube.com/channel/UCSvPuZu_yt7XjlGC3prol1g')
,('سياحة عالمية'						,'https://www.youtube.com/channel/UCWRHPMxUrVmLUAogqS3kCXQ')
,('The u tube tourist ثقافة السفر'		,'https://www.youtube.com/user/sarmadsayah')
]



,['مواقع برمجة كومبيوتر'
,('عالم البرمجة'						,'https://www.youtube.com/c/barmij4Maroc')
,('قناة تكويد لتعليم البرمجة'			,'https://www.youtube.com/channel/UCp8ejsYduufGjYiWP-bE3RQ')
,('learning and programming'			,'https://www.youtube.com/channel/UC_zVQgEEwOJf1hC7FFnf8Ww')
]



,['مواقع خياطة'
,('تعلمي الخياطة من الصفر'				,'https://www.youtube.com/channel/UC7vGqVcGPyxzPMsjrcrq0rg')
,('تفصيل وخياطة للازياء التقليدية'		,'https://www.youtube.com/c/تفصيلوخياطةللازياءالتقليدية')
,('عشاق الخياطة والتفصيل'				,'https://www.youtube.com/c/عشاقالخياطةوالتفصيل')
,('خياطة وموضة'							,'https://www.youtube.com/c/خياطةوموضة')
,('عالم تفصيل فى خياطة creative woman'	,'https://www.youtube.com/channel/UCviRR8_ByPAE-i19S8ZxJ6A')
,('أفكار و ابداعات خياطة'				,'https://www.youtube.com/channel/UC7eAoDwZL3I4h4uVbSDqPgA')
,('خياطة و تطريز ماريمار للسيدات'		,'https://www.youtube.com/channel/UC2K3YiEZ82svrqPjRIbd7CQ')
,('عالم الصناعة التقليدية و العصرية'	,'https://www.youtube.com/channel/UC2RkiLoyZVLu62hKZwjsMZg')
]



,['مواقع سيارات'
,('2500 NMR'							,'https://www.youtube.com/c/nmr2500')
,('فلوقات السيارات Car VLOGS'			,'https://www.youtube.com/channel/UCRqOhcUXS2PMmCjarM9vFZQ')
,('كبسولة سيارات'						,'https://www.youtube.com/channel/UCwtz6Wrr1JLswHobP3lHw-Q')
,('Cars Time'							,'https://www.youtube.com/user/TheA7b8')
]



,['مواقع العاب كومبيوتر'
,('Awesome Cars Games'					,'https://www.youtube.com/c/AwesomeCarGames')
,('zeidgh games'						,'https://www.youtube.com/c/zeidghgames')
,('العاب كمبيوتر مجانية'				,'https://www.youtube.com/channel/UChE3_q4e_QF3ZuXb4B0a2Og')
,('تحميل العاب MediaFire'				,'https://www.youtube.com/channel/UCVRk447Gb-0RzE47eVYmD1g')
]



,['مواقع صيانة وتصليح'
,('صيانة الرحال تعلم تصليح جهازك بنفسك'	,'https://www.youtube.com/channel/UC2sj1GGS7IRI2Qo3wt3srtg')
,('قناة الصيانة المنزلية'				,'https://www.youtube.com/c/قناةالصيانةالمنزلية')
,('صيانة بلاحدود'						,'https://www.youtube.com/c/صيانةبلاحدود')
,('صيانــة سيارتــك'					,'https://www.youtube.com/user/mjmjmj90')
,('صيانة السيارات الألمانية'				,'https://www.youtube.com/c/صيانةالسياراتالألمانية')
,('تعلم صيانة الاجهزه المنزليه'			,'https://www.youtube.com/c/تعلمصيانةالاجهزهالمنزليه')
,('صيانة التلفزيون هواري'				,'https://www.youtube.com/channel/UCyVVaXntCDJgEHSzOCVJr-A')
,('الشمس لاصلاح وصيانة الأجهزه المنزليه'	,'https://www.youtube.com/c/الشمسلاصلاحوصيانةالأجهزهالمنزليه')
,('دورات صيانة التكييف المركزي واسبليت وشباك'			,'https://www.youtube.com/channel/UCReMav9GTJ4t5Qw1tFfRTEA')
,('Education and maintenance of electricity'			,'https://www.youtube.com/c/تعليموصيانةالكهرباء')
,('قناة كل ما هو مفيد كهرباء إلكترونيات صيانة'			,'https://www.youtube.com/c/قناةكلماهومفيدكهرباءإلكترونياتصيانة')
]



,['مواقع حيوانات'
,('animals - حيوانات'					,'https://www.youtube.com/channel/UCrgNKCytJ9OeIazm92BRRjQ')
,('animal vlog'							,'https://www.youtube.com/channel/UCB1BAkuqKMe6MBj99-g8vVg')
,('حيوانات اليفة Pets'					,'https://www.youtube.com/channel/UC8GI2xW-7fuKRGh03Aiz3gg')
,('cute animals حيوانات ظرفية'			,'https://www.youtube.com/channel/UCNg8YMzdoV6ZTSJKVTc6_kQ')
,('حيوان TV'							,'https://www.youtube.com/channel/UCKthzj8tsqat0hCZpRl1ucg')
]



,['مواقع فكاهية مضحكة'
,('Mr Bean Arabic مستر بين'				,'https://www.youtube.com/user/MrBeanArabic')
,('كرتون مستر بين Mr. Bean كل الحلقات'	,'https://www.youtube.com/channel/UCbbRXMrzvGLnrt3grDzA8-g')
,('مقاطع مضحكة قصيرة'					,'https://www.youtube.com/channel/UCHx_sDjjN8hwBkMTPqAXPVg')
,('مقاطع مضحكة من الزمن الجميل'			,'https://www.youtube.com/channel/UCu2eTiTH8zlLgvyuwz0DNVQ')
,('ضحك مووووت'							,'https://www.youtube.com/c/comedyyyyyyyyyyy')
,('Mr Bean Arabic version مستر بين بالعربي'				,'https://www.youtube.com/channel/UCplQlDzJh2zErUFAwv-2mGA')
]



,['مواقع الغاز'
,('الغاز'								,'https://www.youtube.com/channel/UChgB7q5nPv1yxtlqnURjx_Q')
,('الغاز'								,'https://www.youtube.com/c/الغازالغاز')
,('7 دقائق - ألغاز'						,'https://www.youtube.com/c/7دقائقألغاز')
,('الغاز للأذكياء'						,'https://www.youtube.com/channel/UCmDjj2g1VUx13LXHp_JgX0w')
,('ألغاز في 7 ثواني'					,'https://www.youtube.com/c/إفتحمخك')
,('ألغاز السيما cimaQuiz'				,'https://www.youtube.com/channel/UCuvFur8XkkHnCgqXfEOyr6g')
,('ألغاز و حلول 2'						,'https://www.youtube.com/c/ألغازوحلول2')
,('ألغاز وحلول'							,'https://www.youtube.com/channel/UCSGU6C1sTAvCHqylLmNZ_uw')
,('متع عقلك | ألغاز'					,'https://www.youtube.com/channel/UC1jpn0fbnFfsUmEe0MXKOMQ')
]



,['مواقع كتب'
,('ملخصات كتب'							,'https://www.youtube.com/c/ملخصاتكتب')
,('خير جليس'							,'https://www.youtube.com/c/KhairJaleesBook')
,('كتب و روايات صوتية و مسموعة'			,'https://www.youtube.com/channel/UCnElAj7Lkf34UWb7fifybHQ')
,('كتب وسينما'							,'https://www.youtube.com/channel/UChawn8UTtWyY6ubZ7tGF5_g')
,('كتب مسموعة livre audio'				,'https://www.youtube.com/channel/UCPaGszYpjqqxwREv6vwDzkA')
,('كتب تاريخية نادرة'					,'https://www.youtube.com/channel/UCN4XAG6V3DfQs9YGgoXSbeQ')
,('مذكرات مسموعة تاريخية'				,'https://www.youtube.com/channel/UCP8WeaG7ReEW3NHyhOsjasw')
,('الكتب المسموعة'						,'https://www.youtube.com/c/AudioBookss')
,('كتب مسموعة لكل الاعمار'				,'https://www.youtube.com/channel/UCSb6RvOaYAgty6rAzETfeCQ')
,('كتب مسموعة لكل الاعمار ٢'				,'https://www.youtube.com/channel/UC879QRyFj3ESPupeoHSCG0Q')
,('كتب صوتية audio books'				,'https://www.youtube.com/channel/UC_D5m5dCOyhaGw_zKMDhluQ')
,('رواية مسموعة'						,'https://www.youtube.com/channel/UC9A0LLcqXaSsdDi-4mMRrwA')
,('قصص وروايات'							,'https://www.youtube.com/channel/UCp-iAluITUSeM3M69cWkUNg')
,('قصص سمعية'							,'https://www.youtube.com/channel/UC36sKUX6roAWB0T7Q2R2g9g')
,('كتب مسموعة'							,'https://www.youtube.com/channel/UCcC96vsC6phmZEsHrezlcYQ')
]



,['مواقع تخسيس ورشاقة'
,('مجلة تمارين تخسيس'					,'https://www.youtube.com/channel/UCPYw3VGjz72_37id9OPqn-Q')
,('عالم التخسيس'						,'https://www.youtube.com/channel/UCPbkRpGcXYdEinzN-SRhYbA')
,('مجلة الدايت'							,'https://www.youtube.com/channel/UCpJOLSb78snBUe6B7OEakOA')
,('حلم التخسيس'							,'https://www.youtube.com/channel/UC0GFAI_BV_VuL5rGOxhDgrg')
,('تجربتى تخسيس و توفير'				,'https://www.youtube.com/c/تخسيسوتوفير')
,('عالم أسرار التخسيس'					,'https://www.youtube.com/channel/UCijMWwI-LMskVUixEbwGnQQ')
,('قناة تعليمية - تخسيس - رشاقة - المرأة'				,'https://www.youtube.com/channel/UCc3ivwJpLVlUd8qoNVwcIjg')
]



,['مواقع أشعار أدبية'
,('خواطر شعر'							,'https://www.youtube.com/channel/UCe16ZjwiQGLplR5cMbTUFoQ')
,('شعر شعبي ليبي'						,'https://www.youtube.com/c/you777sef1')
,('مستر شعر'							,'https://www.youtube.com/channel/UCXtmqA0b_lVMtOfGelmfc1g')
,('شعر المجهول'							,'https://www.youtube.com/channel/UCa5pAIPGpNJbyGbrzhnEXBg')
]



,['مواقع تسريحات شعر'
,('Lilialady777 تسريحة شعر'				,'https://www.youtube.com/channel/UCijMWwI-LMskVUixEbwGnQQ')
,('تسريح جميله ١'						,'https://www.youtube.com/channel/UCf6tR3VuTQlWmQ7R0KYduQA')
,('تسريحات بنات'						,'https://www.youtube.com/c/تسريحاتبنات')
,('تسريحات شعر مذهله'					,'https://www.youtube.com/channel/UCaz-ewGld-FRB0ipBT3VQIA')
]



,['مواقع مكياج'
,('تتوريال مكياج'							,'https://www.youtube.com/channel/UCI-764QdRlHQxDk275ykj5w')
,('Renad تعليم مكياج'					,'https://www.youtube.com/channel/UCJWiQkPVcTNidlT3hD8mmvA')
,('تعليم مكياج'							,'https://www.youtube.com/channel/UCxLa319B8JBmafobNA08vMw')
,('عالم مكياج وجمال'					,'https://www.youtube.com/channel/UCxd4NYCTIqVpzSlkpmOqpEA')
,('مكياج حواء'							,'https://www.youtube.com/channel/UCVU9ZZrLC-1bRG1FLEUvqpg')
,('مكياج خبيرة تجميل_ Makeup artist'	,'https://www.youtube.com/channel/UCv1E3AI0tHxVVXpH-5doBEg')
,('عالم رسم الحنه - ساره أبو المعاطي'	,'https://www.youtube.com/c/سارهأبوالمعاطي')
]



,['مواقع زراعة'
,('زراعة بلكونة'						,'https://www.youtube.com/c/زراعةبلكونة')
,('World of Agriculture'				,'https://www.youtube.com/c/zera3atty99')
,('زراعة الاسطح'							,'https://www.youtube.com/c/زراعةالاسطح')
,('الزراعة المنزلية'					,'https://www.youtube.com/channel/UCYImI0nx4k0ArX3kybB_PQQ')
,('How To Plant كيفية زراعة وتجذير النباتات'			,'https://www.youtube.com/channel/UCGnjDpDAo5zVm4qKTdb06qg')
]



,['مواقع صناعة'
,('تكنولوجيا عالم الصناعة الحديثة'		,'https://www.youtube.com/channel/UCg5wb97dazk1WOYFROhZpeA')
,('ملك الصناعة'							,'https://www.youtube.com/c/ملكالصناعة')
,('الصناعة اليدوية - Handmade Diy'		,'https://www.youtube.com/channel/UCJU_Fx7lIlKTEGguK-gZj3w')
,('صناعة الاجبان والالبان'				,'https://www.youtube.com/c/صناعةالاجبانوالالبان')
,('الصناعة التقليدية'					,'https://www.youtube.com/channel/UClIbKsoR8UlhlwzfDEas9Bw')
]



,['مواقع تجارة'
,('قناة التجارة العالمية GBC Arabic'	,'https://www.youtube.com/c/GBCtvarabic')
,('مشاريع تجارية مربحة'					,'https://www.youtube.com/channel/UCWXoLHm32U-ArbZDe0Cmjxw')
,('الفوركس العربي'						,'https://www.youtube.com/c/ForexarabyOfficial')
]



,['مواقع رسم'
,('رسم وإبداع'							,'https://www.youtube.com/c/رسموإبداع')
,('رسم X رسم'							,'https://www.youtube.com/channel/UCICu_9Wu5KU5BYnRfmVu5vg')
,('أرسم'								,'https://www.youtube.com/channel/UCiQf-LeinzBD4ajuH0EB3LQ')
,('متعة الرسم'							,'https://www.youtube.com/user/massiouimohamed')
,('رسم و تلوين للأطفال'					,'https://www.youtube.com/channel/UC5_dms8wrv2fvDEEje78FvA')
]




,['مواقع خط'
,('تعليم الخط العربى'					,'https://www.youtube.com/channel/UCBcHXptiGN4u0wwKN8jhN3Q')
,('learn arabic calligraphy'			,'https://www.youtube.com/channel/UCRu_uRw9H2GTJgOZlD2PZgw')
,('مهارات الخط'							,'https://www.youtube.com/channel/UCFvW1gh2XsjVOmkj-ILVjhg')
,('بيت الخط العربي'						,'https://www.youtube.com/c/بيتالخطالعربي')
]



,['مواقع صباغة'
,('تعليم الخط العربى'					,'https://www.youtube.com/channel/UCBcHXptiGN4u0wwKN8jhN3Q')
,('learn arabic calligraphy'			,'https://www.youtube.com/channel/UCRu_uRw9H2GTJgOZlD2PZgw')
,('مهارات الخط'							,'https://www.youtube.com/channel/UCFvW1gh2XsjVOmkj-ILVjhg')
,('بيت الخط العربي'						,'https://www.youtube.com/c/بيتالخطالعربي')
]



,['مواقع صباغة ودهان'
,('دهان سيارات تدهين سيارات'			,'https://www.youtube.com/channel/UCy4MqmVqIRdmowB18THu3Aw')
,('ادهن بيتك بنفسك paint your house by yourself'		,'https://www.youtube.com/channel/UCkV9S-O71RntMFLmkvJIjgA')
]





]

