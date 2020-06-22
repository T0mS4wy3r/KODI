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
	addMenuItem('folder','[COLOR FFC89008]  1.  [/COLOR]'+'قسم عشوائي','',162,'','','SITES')
	addMenuItem('folder','[COLOR FFC89008]  2.  [/COLOR]'+'فيديوهات عشوائية','',163,'','','SITES_RANDOM')
	addMenuItem('folder','[COLOR FFC89008]  3.  [/COLOR]'+'فيديوهات بحث عشوائي','',164,'','','SITES_RANDOM')
	addMenuItem('folder','[COLOR FFC89008]  4.  [/COLOR]'+'فيديوهات عشوائية من قسم','',165,'','','SITES_RANDOM')
	addMenuItem('folder','[COLOR FFC89008]  5.  [/COLOR]'+'قنوات تلفزيون عشوائية','',161,'','','LIVETV_RANDOM')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]  6.  [/COLOR]'+'قسم قنوات IPTV عشوائي','',162,'','','IPTV_LIVE')
	addMenuItem('folder','[COLOR FFC89008]  7.  [/COLOR]'+'قسم فيديو IPTV عشوائي','',162,'','','IPTV_VOD')
	addMenuItem('folder','[COLOR FFC89008]  8.  [/COLOR]'+'قنوات IPTV عشوائية','',163,'','','IPTV_LIVE_RANDOM')
	addMenuItem('folder','[COLOR FFC89008]  9.  [/COLOR]'+'فيديوهات IPTV عشوائية','',163,'','','IPTV_VOD_RANDOM')
	addMenuItem('folder','[COLOR FFC89008]10.  [/COLOR]'+'فيديوهات IPTV بحث عشوائي','',164,'','','IPTV_RANDOM')
	addMenuItem('folder','[COLOR FFC89008]11.  [/COLOR]'+'فيديوهات IPTV عشوائية من قسم','',165,'','','IPTV_RANDOM')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return

def RANDOM_LIVETV(options):
	addMenuItem('folder','إعادة طلب قنوات عشوائية','',161,'','','UPDATE_LIVETV_RANDOM')
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
	if 'RANDOM' in options:
		menuItemsLIST[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
		if len(menuItemsLIST)>random_size: menuItemsLIST[:] = random.sample(menuItemsLIST,random_size)
	menuItemsLIST[:] = previous+menuItemsLIST
	#LOG_THIS('NOTICE','EMAD   RANDOM_LIVETV'+str(contentsDICT))
	return

def SEARCH_RANDOM_VIDEOS(options):
	options = options.replace('UPDATE_','')
	headers = { 'User-Agent' : '' }
	url = 'https://www.bestrandoms.com/random-arabic-words'
	payload = { 'quantity' : '50' }
	data = urllib.urlencode(payload)
	#xbmcgui.Dialog().ok('',str(data))
	html = openURL_cached(30*MINUTE,url,data,headers,'','RANDOMS-SEARCH_RANDOM_VIDEOS-1st')
	html_blocks = re.findall('list-unstyled(.*?)clearfix',html,re.DOTALL)
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
	for i in range(0,5): random.shuffle(list2)
	#LOG_THIS('NOTICE',str(list2))
	#selection = xbmcgui.Dialog().select(str(len(list2)),list2)
	"""
	list = ['كلمات عشوائية عربية','كلمات عشوائية إنكليزية']
	#selection = xbmcgui.Dialog().select('اختر كلمة للبحث عنها:', list2)
	list1 = []
	counts = len(list2)
	for i in range(counts*5): random.shuffle(list2)
	for i in range(length): list1.append('كلمة عشوائية رقم '+str(i))
	while True:
		#selection = xbmcgui.Dialog().select('اختر اللغة:', list)
		#if selection == -1: return
		#elif selection==0: list2 = arbLIST
		#else: list2 = engLIST
		selection = xbmcgui.Dialog().select('اختر كلمة للبحث عنها:', list1)
		if selection != -1: break
		elif selection == -1: return
	search = list2[selection]
	"""
	if 'SITES' in options:
		search_modes = [19,29,49,59,69,79,99,119,139,149,209,229,249,259]
		#search_modes = [39]	panet search does not work at panet website
	elif 'IPTV' in options:
		search_modes = [239]
		import IPTV
		if not IPTV.isIPTVFiles(True): return
	count,repeats = 0,0
	addMenuItem('folder','البحث عن : [  ]','',164,'','','UPDATE_'+options)
	addMenuItem('folder','إعادة البحث العشوائي','',164,'','','UPDATE_'+options)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	previuosLIST = menuItemsLIST[:]
	menuItemsLIST[:] = []
	for i in range(0,20):
		text = random.sample(list2,1)[0]
		text = text+'::'
		mode = random.sample(search_modes,1)[0]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Video Search   mode:'+str(mode)+'  text:'+text)
		results = MAIN_DISPATCHER('','','',mode,'','',text,'')
		if len(menuItemsLIST)>0: break
	previuosLIST[0][1] = '[ [COLOR FFC89008]'+text[:-2]+'[/COLOR] البحث عن : [ '
	menuItemsLIST[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
	if len(menuItemsLIST)>random_size: menuItemsLIST[:] = random.sample(menuItemsLIST,random_size)
	menuItemsLIST[:] = previuosLIST+menuItemsLIST
	#GLOBAL_SEARCH_MENU(search,False)
	#xbmcgui.Dialog().ok(str(len(menuItemsLIST)),'MENUS')
	return

def IMPORT_SITES():
	global contentsDICT
	results = READ_FROM_SQL3('IMPORT_SECTIONS','SITES')
	if results: contentsDICT = results ; return
	previousMenu = menuItemsLIST[:]
	#LOG_THIS('NOTICE','START TIMING')
	#xbmcgui.Dialog().ok('','start')
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
	#import EGYBEST			;	EGYBEST.MENU('EGYBEST')
	#import HALACIMA		;	HALACIMA.MENU('HALACIMA')
	#import MOVIZLAND		;	MOVIZLAND.MENU('MOVIZLAND')
	#import SERIES4WATCH	;	SERIES4WATCH.MENU('SERIES4WATCH')
	menuItemsLIST[:] = previousMenu
	if failed>5: xbmcgui.Dialog().ok('مشكلة غريبة جدا','لديك مشكلة في اكثر من 5 مواقع من مواقع البرنامج ... وسببها قد يكون عدم وجود إنترنيت في جهازك')
	else: WRITE_TO_SQL3('IMPORT_SECTIONS','SITES',contentsDICT,LONG_CACHE)
	return

def IMPORT_IPTV(options):
	#xbmcgui.Dialog().ok('',options)
	message = 'للأسف لديك مشكلة في هذا الموقع . ورسالة الخطأ كان فيها تفاصيل المشكلة . أذا المشكلة ليست حجب فجرب إرسال هذه المشكلة إلى المبرمج من قائمة خدمات البرنامج'
	import IPTV
	if IPTV.isIPTVFiles(True):
		if 'IPTV' in options and 'LIVE' not in options:
			try: IPTV.GROUPS('VOD_MOVIES_GROUPED','',options+'_MOVIES')
			except: xbmcgui.Dialog().ok('موقع IPTV للافلام',message)
			try: IPTV.GROUPS('VOD_SERIES_GROUPED','',options+'_SERIES')
			except: xbmcgui.Dialog().ok('موقع IPTV للمسلسلات',message)
		if 'IPTV' in options and 'VOD' not in options:
			try: IPTV.GROUPS('LIVE_GROUPED','',options+'_TV')
			except: xbmcgui.Dialog().ok('موقع IPTV للقنوات',message)
		for item in menuItemsLIST:
			item[1] = item[1].replace('IPTV_','').replace('_MOD_','').replace('UPDATE_','')
			if item[1].count('_')>1: item[1] = item[1].split('_',2)[2]
			if item[1]=='': item[1] = '....'
	else: EXIT_PROGRAM('RANDOMS-IMPORT_IPTV-1st')
	return

def CATEGORIES_MENU(options):
	#xbmcgui.Dialog().ok('',options)
	clean_options = options.replace('UPDATE_','').replace('DELETE_','')
	addMenuItem('folder','تحديث هذه القائمة','',165,'','','UPDATE_DELETE_'+clean_options)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	if 'SITES' in options:
		if 'DELETE' in options: DELETE_FROM_SQL3('IMPORT_SECTIONS','SITES')
		IMPORT_SITES()
		for nameonly in sorted(contentsDICT.keys()):
			addMenuItem('folder',menu_name+nameonly,nameonly,166,'','',clean_options)
	elif 'IPTV' in options:
		if 'DELETE' in options:
			import IPTV
			IPTV.CREATE_STREAMS()
		IMPORT_IPTV(clean_options)
	return

def RANDOM_VOD_ITEMS(nameonly,options):
	options = options.replace('UPDATE_','')
	#xbmcgui.Dialog().ok(nameonly,options)
	IMPORT_SITES()
	if contentsDICT=={}: return
	if 'RANDOM' in options:
		addMenuItem('folder','[ [COLOR FFC89008]'+nameonly+'[/COLOR] القسم : [ ',nameonly,166,'','','UPDATE_'+options)
		addMenuItem('folder','إعادة الطلب العشوائي من نفس القسم',nameonly,166,'','','UPDATE_'+options)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	for website in sorted(contentsDICT[nameonly].keys()):
		type,name,url,mode2,image,page,text,favourite = contentsDICT[nameonly][website]
		if 'RANDOM' in options or len(contentsDICT[nameonly])==1:
			MAIN_DISPATCHER(type,'',url,mode2,'',page,text,'')
			menuItemsLIST[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
			previousLIST,newLIST = menuItemsLIST[:3],menuItemsLIST[3:]
			for i in range(0,5): random.shuffle(newLIST)
			if 'RANDOM' in options: menuItemsLIST[:] = previousLIST+newLIST[:random_size]
			else: menuItemsLIST[:] = previousLIST+newLIST
		elif 'SITES' in options: addMenuItem('folder',website,url,mode2,image,page,text,favourite)
	#LOG_THIS('NOTICE',str(contentsDICT[nameonly]))
	#xbmcgui.Dialog().ok(str(contentsDICT[nameonly].keys()),str(contentsDICT[nameonly]))
	return

def RANDOM_CATEGORY(options,mode):
	options = options.replace('UPDATE_','')
	#xbmcgui.Dialog().ok(options,str(mode))
	name,menuItemsLIST2 = '',[]
	addMenuItem('folder','[ [COLOR FFC89008]'+name+'[/COLOR] القسم : [ ','',mode,'','','UPDATE_'+options)
	addMenuItem('folder','إعادة طلب قسم عشوائي','',mode,'','','UPDATE_'+options)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	previousLIST = menuItemsLIST[:]
	menuItemsLIST[:] = []
	if 'SITES' in options:
		IMPORT_SITES()
		if contentsDICT=={}: return
		list1 = contentsDICT.keys()
		nameonly = random.sample(list1,1)[0]
		list2 = contentsDICT[nameonly].keys()
		website = random.sample(list2,1)[0]
		type,name,url,mode2,image,page,text,favourite = contentsDICT[nameonly][website]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   website: '+website+'   name: '+name+'   url: '+url+'   mode: '+str(mode2))
	elif 'IPTV' in options:
		IMPORT_IPTV(options)
		type,name,url,mode2,image,page,text,favourite = random.sample(menuItemsLIST,1)[0]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   name: '+name+'   url: '+url+'   mode: '+str(mode2))
	for i in range(0,10):
		#xbmcgui.Dialog().ok(str(mode2),name)
		if i>0: LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   name: '+name+'   url: '+url+'   mode: '+str(mode2))
		menuItemsLIST[:] = []
		html = MAIN_DISPATCHER(type,name,url,mode2,image,page,text,favourite)
		#if '___Error___' in html: RANDOM_CATEGORY(options,mode)
		if 'IPTV' in options and mode2==167: del menuItemsLIST[:3]
		menuItemsLIST2[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
		if str(menuItemsLIST2).count('video')>0: break
		if str(menuItemsLIST2).count('live')>0: break
		if menuItemsLIST2: type,name,url,mode2,image,page,text,favourite = random.sample(menuItemsLIST2,1)[0]
	#name = name.replace('[COLOR FFC89008]','').replace('[/COLOR]','')
	name = name.replace('IPTV_','').replace('VOD_','').replace('_MOD_','')
	if name.count('_')>1: name = name.split('_',2)[2]
	if name=='': name = '....'
	previousLIST[0][1] = '[ [COLOR FFC89008]'+name+'[/COLOR] القسم : [ '
	for i in range(0,5): random.shuffle(menuItemsLIST2)
	if 'RANDOM' in options: menuItemsLIST[:] = previousLIST+menuItemsLIST2[:random_size]
	else: menuItemsLIST[:] = previousLIST+menuItemsLIST2
	return

def RANDOM_IPTV_ITEMS(TYPE,GROUP):
	GROUP = GROUP.replace('UPDATE_','')
	#xbmcgui.Dialog().ok(TYPE,GROUP)
	if '____' in GROUP: GROUP2 = GROUP.split('____')[0]
	else: GROUP2 = GROUP
	addMenuItem('folder','[ [COLOR FFC89008]'+GROUP2+'[/COLOR] القسم : [ ',TYPE,167,'','','UPDATE_'+GROUP)
	addMenuItem('folder','إعادة الطلب العشوائي من نفس القسم',TYPE,167,'','','UPDATE_'+GROUP)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	import IPTV
	if 'VOD_SERIES' in TYPE: IPTV.GROUPS(TYPE,GROUP,'')
	else: IPTV.ITEMS(TYPE,GROUP)
	menuItemsLIST[:] = CLEAN_RANDOM_LIST(menuItemsLIST)
	if len(menuItemsLIST)>(random_size+3): menuItemsLIST[:] = menuItemsLIST[:3]+random.sample(menuItemsLIST[3:],random_size)
	#LOG_THIS('NOTICE',str(contentsDICT[nameonly]))
	#xbmcgui.Dialog().ok(str(contentsDICT[nameonly].keys()),str(contentsDICT[nameonly]))
	return

def CLEAN_RANDOM_LIST(menuItemsLIST):
	menuItemsLIST2 = []
	for type,name,url,mode,image,page,text,favourite in menuItemsLIST:
		if 'صفحة' in name or 'صفحه' in name or 'page' in name.lower(): continue
		menuItemsLIST2.append([type,name,url,mode,image,page,text,favourite])
	return menuItemsLIST2







