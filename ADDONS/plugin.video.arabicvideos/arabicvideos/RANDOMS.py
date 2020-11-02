# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from LIBRARY import *

script_name='RANDOMS'
menu_name='_LST_'

random_size = 5

def MAIN(mode,url,text=''):
	if   mode==160: results = MENU()
	elif mode==161: results = RANDOM_LIVETV(text)
	elif mode==162: results = RANDOM_CATEGORY(text,162)
	elif mode==163: results = RANDOM_CATEGORY(text,163)
	elif mode==164: results = SEARCH_RANDOM_VIDEOS(text)
	elif mode==165: results = CATEGORIES_MENU(text)
	elif mode==166: results = RANDOM_VOD_ITEMS(url,text)
	elif mode==167: results = RANDOM_IPTV_ITEMS(url,text)
	else: results = False
	return results

def MENU():
	addMenuItem('folder','[COLOR FFC89008]  1.  [/COLOR]'+'قنوات تلفزيون عشوائية','',161,'','','_LIVETV__RANDOM__REMEMBERRESULTS_')
	addMenuItem('folder','[COLOR FFC89008]  2.  [/COLOR]'+'قسم عشوائي','',162,'','','_SITES__REMEMBERRESULTS_')
	addMenuItem('folder','[COLOR FFC89008]  3.  [/COLOR]'+'فيديوهات عشوائية','',163,'','','_SITES__RANDOM__REMEMBERRESULTS_')
	addMenuItem('folder','[COLOR FFC89008]  4.  [/COLOR]'+'فيديوهات بحث عشوائي','',164,'','','_SITES__RANDOM__REMEMBERRESULTS_')
	addMenuItem('folder','[COLOR FFC89008]  5.  [/COLOR]'+'فيديوهات عشوائية من قسم','',165,'','','_SITES__RANDOM__REMEMBERRESULTS_')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]  6.  [/COLOR]'+'قنوات IPTV عشوائية','',163,'','','_IPTV__LIVE__RANDOM__REMEMBERRESULTS_')
	addMenuItem('folder','[COLOR FFC89008]  7.  [/COLOR]'+'قسم قنوات IPTV عشوائي','',162,'','','_IPTV__LIVE__REMEMBERRESULTS_')
	addMenuItem('folder','[COLOR FFC89008]  8.  [/COLOR]'+'قسم فيديو IPTV عشوائي','',162,'','','_IPTV__VOD__REMEMBERRESULTS_')
	addMenuItem('folder','[COLOR FFC89008]  9.  [/COLOR]'+'فيديوهات IPTV عشوائية','',163,'','','_IPTV__VOD__RANDOM__REMEMBERRESULTS_')
	addMenuItem('folder','[COLOR FFC89008]10.  [/COLOR]'+'فيديوهات IPTV بحث عشوائي','',164,'','','_IPTV__RANDOM__REMEMBERRESULTS_')
	addMenuItem('folder','[COLOR FFC89008]11.  [/COLOR]'+'فيديوهات IPTV عشوائية من قسم','',165,'','','_IPTV__RANDOM__REMEMBERRESULTS_')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return

def RANDOM_LIVETV(options):
	addMenuItem('folder','إعادة طلب قنوات عشوائية','',161,'','','_FORGETRESULTS__REMEMBERRESULTS__LIVETV__RANDOM_')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	previous = menuItemsLIST[:]
	menuItemsLIST[:] = []
	#addMenuItem('folder','[COLOR FFC89008] YUT   [/COLOR]'+'قنوات عربية من يوتيوب','',147)
	#addMenuItem('folder','[COLOR FFC89008] YUT   [/COLOR]'+'قنوات أجنبية من يوتيوب','',148)
	#addMenuItem('folder','[COLOR FFC89008] IFL    [/COLOR]'+'قناة آي فيلم من موقعهم','',28)
	#addMenuItem('live','[COLOR FFC89008] MRF  [/COLOR]'+'قناة المعارف من موقعهم','',41)
	#addMenuItem('live','[COLOR FFC89008] KWT  [/COLOR]'+'قناة الكوثر من موقعهم','',135)
	import LIVETV
	LIVETV.ITEMS('0',False)
	LIVETV.ITEMS('1',False)
	LIVETV.ITEMS('2',False)
	#LIVETV.ITEMS('3',False)
	if '_RANDOM_' in options:
		menuItemsLIST[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
		if len(menuItemsLIST)>random_size: menuItemsLIST[:] = random.sample(menuItemsLIST,random_size)
	menuItemsLIST[:] = previous+menuItemsLIST
	#LOG_THIS('NOTICE','EMAD   RANDOM_LIVETV'+str(contentsDICT))
	return

def SEARCH_RANDOM_VIDEOS(options):
	options = options.replace('_FORGETRESULTS_','').replace('_REMEMBERRESULTS_','')
	headers = { 'User-Agent' : '' }
	url = 'https://www.bestrandoms.com/random-arabic-words'
	payload = { 'quantity' : '50' }
	data = urllib.urlencode(payload)
	#XBMCGUI_DIALOG_OK('',str(data))
	response = openURL_requests_cached(VERY_SHORT_CACHE,'GET',url,data,headers,'','','RANDOMS-SEARCH_RANDOM_VIDEOS-1st')
	html = response.content
	html_blocks = re.findall('class="content"(.*?)class="clearfix"',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('<span>(.*?)</span>.*?<span>(.*?)</span>',block,re.DOTALL)
	arbLIST,engLIST = zip(*items)
	list2 = []
	splitters = [' ','"','`',',','.',':',';',"'",'-']
	bothLIST = engLIST+arbLIST
	for word in bothLIST:
		if word in engLIST: minimumChars = 2
		if word in arbLIST: minimumChars = 4
		list3 = [i in word for i in splitters]
		if any(list3):
			index = list3.index(True)
			splitter = splitters[index]
			word3 = ''
			if word.count(splitter)>1: word1,word2,word3 = word.split(splitter,2)
			else: word1,word2 = word.split(splitter,1)
			if len(word1)>minimumChars: list2.append(word1.lower())
			if len(word2)>minimumChars: list2.append(word2.lower())
			if len(word3)>minimumChars: list2.append(word3.lower())
		elif len(word)>minimumChars: list2.append(word.lower())
	for i in range(9): random.shuffle(list2)
	#LOG_THIS('NOTICE',str(list2))
	#selection = XBMCGUI_DIALOG_SELECT(str(len(list2)),list2)
	"""
	list = ['كلمات عشوائية عربية','كلمات عشوائية إنكليزية']
	#selection = XBMCGUI_DIALOG_SELECT('اختر كلمة للبحث عنها:', list2)
	list1 = []
	counts = len(list2)
	for i in range(counts*5): random.shuffle(list2)
	for i in range(length): list1.append('كلمة عشوائية رقم '+str(i))
	while True:
		#selection = XBMCGUI_DIALOG_SELECT('اختر اللغة:', list)
		#if selection == -1: return
		#elif selection==0: list2 = arbLIST
		#else: list2 = engLIST
		selection = XBMCGUI_DIALOG_SELECT('اختر كلمة للبحث عنها:', list1)
		if selection != -1: break
		elif selection == -1: return
	search = list2[selection]
	"""
	if '_SITES_' in options:
		search_modes = [19,29,39,49,59,69,79,99,119,139,149,209,229,249,259,309]
	elif '_IPTV_' in options:
		search_modes = [239]
		import IPTV
		if not IPTV.isIPTVFiles(True): return
	count,repeats = 0,0
	addMenuItem('folder','البحث عن : [  ]','',164,'','','_FORGETRESULTS__REMEMBERRESULTS_'+options)
	addMenuItem('folder','إعادة البحث العشوائي','',164,'','','_FORGETRESULTS__REMEMBERRESULTS_'+options)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	previuosLIST = menuItemsLIST[:]
	menuItemsLIST[:] = []
	for i in range(0,20):
		text = random.sample(list2,1)[0]
		#text = text+'___'
		mode = random.sample(search_modes,1)[0]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Video Search   mode:'+str(mode)+'  text:'+text)
		results = MAIN_DISPATCHER('','','',mode,'','',text+'_NODIALOGS_','')
		if len(menuItemsLIST)>0: break
	#text = text.replace('_','')
	previuosLIST[0][1] = '[ [COLOR FFC89008]'+text[:-2]+'[/COLOR] البحث عن : [ '
	menuItemsLIST[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
	if len(menuItemsLIST)>random_size: menuItemsLIST[:] = random.sample(menuItemsLIST,random_size)
	menuItemsLIST[:] = previuosLIST+menuItemsLIST
	#GLOBAL_SEARCH_MENU(search,False)
	#XBMCGUI_DIALOG_OK(str(len(menuItemsLIST)),'MENUS')
	return

def IMPORT_SITES():
	global contentsDICT
	results = READ_FROM_SQL3('IMPORT_SECTIONS','SITES')
	if results: contentsDICT = results ; return
	previousMenu = menuItemsLIST[:]
	#LOG_THIS('NOTICE','START TIMING')
	#XBMCGUI_DIALOG_OK('','start')
	failed = 0
	if failed<=5:
		try: 
			import AKOAM ; html = AKOAM.MENU('AKOAM')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import AKWAM ; html = AKWAM.MENU('AKWAM')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import HELAL ; html = HELAL.MENU('HELAL')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import PANET ; html = PANET.MENU('PANET')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import ALARAB ; html = ALARAB.MENU('ALARAB')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import IFILM ; html = IFILM.MENU('IFILM_ARABIC')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import IFILM ; html = IFILM.MENU('IFILM_ENGLISH')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import ALFATIMI ; html = ALFATIMI.MENU('ALFATIMI')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import ALMAAREF ; html = ALMAAREF.MENU('ALMAAREF')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import ARABSEED ; html = ARABSEED.MENU('ARABSEED')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import SHOOFMAX ; html = SHOOFMAX.MENU('SHOOFMAX')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import SHAHID4U ; html = SHAHID4U.MENU('SHAHID4U')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import ALKAWTHAR ; html = ALKAWTHAR.MENU('ALKAWTHAR')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import ARABLIONZ ; html = ARABLIONZ.MENU('ARABLIONZ')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import EGYBESTVIP ; html = EGYBESTVIP.MENU('EGYBESTVIP')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import CIMANOW ; html = CIMANOW.MENU('CIMANOW')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import SHIAVOICE ; html = SHIAVOICE.MENU('SHIAVOICE')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import KARBALATV ; html = KARBALATV.MENU('KARBALATV')
			if '__Error__' in html: failed += 1
		except: failed += 1
	if failed<=5:
		try:
			import YTB_CHANNELS ; html = YTB_CHANNELS.MENU('YTB_CHANNELS')
			if '__Error__' in html: failed += 1
		except: failed += 1
	#import EGYBEST			;	EGYBEST.MENU('EGYBEST')
	#import HALACIMA		;	HALACIMA.MENU('HALACIMA')
	#import MOVIZLAND		;	MOVIZLAND.MENU('MOVIZLAND')
	#import SERIES4WATCH	;	SERIES4WATCH.MENU('SERIES4WATCH')
	#import YOUTUBE			;	YOUTUBE.MENU('YOUTUBE')
	menuItemsLIST[:] = previousMenu
	if failed>5: XBMCGUI_DIALOG_OK('رسالة من المبرمج','لديك مشكلة في اكثر من 5 مواقع من مواقع البرنامج ... وسببها قد يكون عدم وجود إنترنيت في جهازك')
	else: WRITE_TO_SQL3('IMPORT_SECTIONS','SITES',contentsDICT,PERMANENT_CACHE)
	return

def IMPORT_IPTV(options):
	message = 'للأسف لديك مشكلة في هذا الموقع . ورسالة الخطأ كان فيها تفاصيل المشكلة . أذا المشكلة ليست حجب فجرب إرسال هذه المشكلة إلى المبرمج من قائمة خدمات البرنامج'
	import IPTV
	if IPTV.isIPTVFiles(True):
		#XBMCGUI_DIALOG_OK('',options)
		if '_IPTV_' in options and '_LIVE_' not in options:
			try: IPTV.GROUPS('VOD_ORIGINAL_GROUPED','',options+'_FORGETRESULTS__REMEMBERRESULTS_')
			except: XBMCGUI_DIALOG_OK('موقع IPTV للفيديوهات',message)
		if '_IPTV_' in options and '_VOD_' not in options:
			try: IPTV.GROUPS('LIVE_ORIGINAL_GROUPED','',options+'_FORGETRESULTS__REMEMBERRESULTS_')
			except: XBMCGUI_DIALOG_OK('موقع IPTV للقنوات',message)
	else: EXIT_PROGRAM('RANDOMS-IMPORT_IPTV-1st')
	return

def CATEGORIES_MENU(options):
	#XBMCGUI_DIALOG_OK('',options)
	clean_options = options.replace('_CREATENEW_','').replace('_FORGETRESULTS_','').replace('_REMEMBERRESULTS_','')
	addMenuItem('folder','تحديث هذه القائمة','',165,'','','_CREATENEW__FORGETRESULTS_'+clean_options)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	if '_SITES_' in options:
		if '_CREATENEW_' in options: DELETE_FROM_SQL3('IMPORT_SECTIONS','SITES')
		IMPORT_SITES()
		#XBMCGUI_DIALOG_OK('',str(len(menuItemsLIST)))
		for nameonly in sorted(contentsDICT.keys()):
			addMenuItem('folder',menu_name+nameonly,nameonly,166,'','',clean_options)
	elif '_IPTV_' in options:
		if '_CREATENEW_' in options:
			import IPTV
			IPTV.CREATE_STREAMS()
		IMPORT_IPTV(clean_options)
	return

def RANDOM_VOD_ITEMS(nameonly,options):
	options = options.replace('_FORGETRESULTS_','').replace('_REMEMBERRESULTS_','')
	#XBMCGUI_DIALOG_OK(nameonly,options)
	IMPORT_SITES()
	if contentsDICT=={}: return
	if '_RANDOM_' in options:
		addMenuItem('folder','[ [COLOR FFC89008]'+nameonly+'[/COLOR] القسم : [ ',nameonly,166,'','','_FORGETRESULTS__REMEMBERRESULTS_'+options)
		addMenuItem('folder','إعادة الطلب العشوائي من نفس القسم',nameonly,166,'','','_FORGETRESULTS__REMEMBERRESULTS_'+options)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	for website in sorted(contentsDICT[nameonly].keys()):
		type,name,url,mode2,image,page,text,favourite = contentsDICT[nameonly][website]
		if '_RANDOM_' in options or len(contentsDICT[nameonly])==1:
			MAIN_DISPATCHER(type,'',url,mode2,'',page,text,'')
			menuItemsLIST[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
			previousLIST,newLIST = menuItemsLIST[:3],menuItemsLIST[3:]
			for i in range(9): random.shuffle(newLIST)
			if '_RANDOM_' in options: menuItemsLIST[:] = previousLIST+newLIST[:random_size]
			else: menuItemsLIST[:] = previousLIST+newLIST
		elif '_SITES_' in options: addMenuItem('folder',website,url,mode2,image,page,text,favourite)
	#LOG_THIS('NOTICE',str(contentsDICT[nameonly]))
	#XBMCGUI_DIALOG_OK(str(contentsDICT[nameonly].keys()),str(contentsDICT[nameonly]))
	return

def RANDOM_CATEGORY(options,mode):
	options = options.replace('_FORGETRESULTS_','').replace('_REMEMBERRESULTS_','')
	#XBMCGUI_DIALOG_OK(options,str(mode))
	name,menuItemsLIST2 = '',[]
	addMenuItem('folder','[ [COLOR FFC89008]'+name+'[/COLOR] القسم : [ ','',mode,'','','_FORGETRESULTS__REMEMBERRESULTS_'+options)
	addMenuItem('folder','إعادة طلب قسم عشوائي','',mode,'','','_FORGETRESULTS__REMEMBERRESULTS_'+options)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	previousLIST = menuItemsLIST[:]
	menuItemsLIST[:] = []
	if '_SITES_' in options:
		IMPORT_SITES()
		if contentsDICT=={}: return
		list1 = contentsDICT.keys()
		nameonly = random.sample(list1,1)[0]
		list2 = contentsDICT[nameonly].keys()
		website = random.sample(list2,1)[0]
		type,name,url,mode2,image,page,text,favourite = contentsDICT[nameonly][website]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   website: '+website+'   name: '+name+'   url: '+url+'   mode: '+str(mode2))
	elif '_IPTV_' in options:
		IMPORT_IPTV(options)
		type,name,url,mode2,image,page,text,favourite = random.sample(menuItemsLIST,1)[0]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   name: '+name+'   url: '+url+'   mode: '+str(mode2))
	series_category_name = name
	series_names_list = []
	for i in range(0,10):
		if i>0: LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   name: '+name+'   url: '+url+'   mode: '+str(mode2))
		menuItemsLIST[:] = []
		#XBMCGUI_DIALOG_OK(name,'')
		if mode2==234 and '__IPTVSeries__' in text: mode2 = 233		
		if mode2==144: mode2 = 291		
		html = MAIN_DISPATCHER(type,name,url,mode2,image,page,text,favourite)
		#if '___Error___' in html: RANDOM_CATEGORY(options,mode)
		if '_IPTV_' in options and mode2==167: del menuItemsLIST[:3]
		menuItemsLIST2[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
		if series_names_list and ARABIC_HEX(u'حلقة') in str(menuItemsLIST2) or ARABIC_HEX(u'حلقه') in str(menuItemsLIST2):
			name = series_category_name
			menuItemsLIST2[:] = series_names_list
			break
		series_category_name = name
		series_names_list = menuItemsLIST2[:]
		if str(menuItemsLIST2).count('video')>0: break
		if str(menuItemsLIST2).count('live')>0: break
		if mode2==233: break	# iptv series names instead of episodes name
		if mode2==291: break	# youtube channels names instead of youtube channels contents
		if menuItemsLIST2: type,name,url,mode2,image,page,text,favourite = random.sample(menuItemsLIST2,1)[0]
	if name=='': name = '....'
	elif name.count('_')>1: name = name.split('_',2)[2]
	name = name.replace('UNKNOWN: ','')#.replace(',MOVIES: ','').replace(',SERIES: ','').replace(',LIVE: ','')
	previousLIST[0][1] = '[ [COLOR FFC89008]'+name+'[/COLOR] القسم : [ '
	for i in range(9): random.shuffle(menuItemsLIST2)
	if '_RANDOM_' in options: menuItemsLIST[:] = previousLIST+menuItemsLIST2[:random_size]
	else: menuItemsLIST[:] = previousLIST+menuItemsLIST2
	return

def RANDOM_IPTV_ITEMS(TYPE,GROUP):
	GROUP = GROUP.replace('_FORGETRESULTS_','').replace('_REMEMBERRESULTS_','')
	#XBMCGUI_DIALOG_OK(TYPE,GROUP)
	GROUP2 = GROUP
	if '__IPTVSeries__' in GROUP:
		GROUP2 = GROUP.split('__IPTVSeries__')[0]
		type = ',SERIES: '
	elif 'VOD' in TYPE: type = ',VIDEOS: '
	elif 'LIVE' in TYPE: type = ',LIVE: '
	addMenuItem('folder','[ [COLOR FFC89008]'+type+GROUP2+'[/COLOR] القسم : [ ',TYPE,167,'','','_FORGETRESULTS__REMEMBERRESULTS_'+GROUP)
	addMenuItem('folder','إعادة الطلب العشوائي من نفس القسم',TYPE,167,'','','_FORGETRESULTS__REMEMBERRESULTS_'+GROUP)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	import IPTV
	if '__IPTVSeries__' in GROUP: IPTV.GROUPS(TYPE,GROUP,'')
	else: IPTV.ITEMS(TYPE,GROUP)
	menuItemsLIST[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
	if len(menuItemsLIST)>(random_size+3): menuItemsLIST[:] = menuItemsLIST[:3]+random.sample(menuItemsLIST[3:],random_size)
	#LOG_THIS('NOTICE',str(contentsDICT[nameonly]))
	#XBMCGUI_DIALOG_OK(str(contentsDICT[nameonly].keys()),str(contentsDICT[nameonly]))
	return

def CLEAN_RANDOM_LIST(menuItemsLIST):
	menuItemsLIST2 = []
	for type,name,url,mode,image,page,text,favourite in menuItemsLIST:
		if 'صفحة' in name or 'صفحه' in name or 'page' in name.lower(): continue
		menuItemsLIST2.append([type,name,url,mode,image,page,text,favourite])
	return menuItemsLIST2




