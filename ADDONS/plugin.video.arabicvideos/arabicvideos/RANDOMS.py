# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from LIBRARY import *

script_name='RANDOMS'

def MAIN(mode,url,text=''):
	if   mode==160: results = MAIN_MENU()
	elif mode==161: results = RANDOM_LIVETV()
	elif mode==162: results = RANDOM_CATEGORY(text,162)
	elif mode==163: results = RANDOM_CATEGORY(text,163)
	elif mode==164: results = SEARCH_RANDOM_VIDEOS(text)
	elif mode==165: results = CATEGORIES_MENU(text)
	elif mode==166: results = CATEGORIES_SUBMENU(url,text)
	else: results = False
	return results

def MAIN_MENU():
	addMenuItem('dir','[COLOR FFC89008]  1.  [/COLOR]'+'قسم عشوائي','',162,'','','VOD')
	addMenuItem('dir','[COLOR FFC89008]  2.  [/COLOR]'+'فيديوهات عشوائية','',163,'','','VOD')
	addMenuItem('dir','[COLOR FFC89008]  3.  [/COLOR]'+'فيديوهات بحث عشوائي','',164,'','','VOD')
	addMenuItem('dir','[COLOR FFC89008]  4.  [/COLOR]'+'فيديو عشوائي من قسم','',165,'','','RANDOM_VOD')
	addMenuItem('dir','[COLOR FFC89008]  5.  [/COLOR]'+'قنوات تلفزيون عشوائية','',161)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('dir','[COLOR FFC89008]  6.  [/COLOR]'+'قسم IPTV عشوائي','',162,'','','LIVE')
	addMenuItem('dir','[COLOR FFC89008]  7.  [/COLOR]'+'فيديو IPTV عشوائي','',163,'','','LIVE')
	addMenuItem('dir','[COLOR FFC89008]  8.  [/COLOR]'+'فيديو IPTV بحث عشوائي','',164,'','','LIVE')
	addMenuItem('dir','[COLOR FFC89008]  9.  [/COLOR]'+'فيديو IPTV عشوائي من قسم','',165,'','','RANDOM_LIVE')
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	return

def RANDOM_LIVETV():
	addMenuItem('dir','إعادة طلب قنوات عشوائية','',161)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('dir','[COLOR FFC89008] YUT   [/COLOR]'+'قنوات عربية من يوتيوب','',147)
	addMenuItem('dir','[COLOR FFC89008] YUT   [/COLOR]'+'قنوات أجنبية من يوتيوب','',148)
	addMenuItem('dir','[COLOR FFC89008] IFL    [/COLOR]'+'قناة آي فيلم من موقعهم','',28)
	addMenuItem('link','[COLOR FFC89008] MRF  [/COLOR]'+'قناة المعارف من موقعهم','',41,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008] KWT  [/COLOR]'+'قناة الكوثر من موقعهم','',135,'','','IsPlayable=no')
	import LIVETV
	LIVETV.ITEMS('0',False)
	LIVETV.ITEMS('1',False)
	LIVETV.ITEMS('2',False)
	#LIVETV.ITEMS('3',False)
	#LOG_THIS('NOTICE','EMAD   RANDOM_LIVETV'+str(contentsDICT))
	return

def SEARCH_RANDOM_VIDEOS(options):
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
	if 'VOD' in options:
		search_modes = [19,29,49,59,69,79,99,119,139,149,209,229,249,259]
		#search_modes = [39]	panet search does not work at panet website
	else:
		search_modes = [239]
		import IPTV
		if not IPTV.isIPTVFiles(True): return
	count,repeats = 0,0
	addMenuItem('dir','البحث عن : [  ]','',164,'','',options)
	addMenuItem('dir','إعادة البحث العشوائي','',164,'','',options)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	for i in range(0,20):
		text = random.sample(list2,1)[0]
		text = text+'::'
		mode = random.sample(search_modes,1)[0]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Video Search   mode:'+str(mode)+'  text:'+text)
		results = MAIN_DISPATCHER(mode,'',text,'')
		if len(menuItemsLIST)>3: break
	menuItemsLIST[0][1] = '[ [COLOR FFC89008]'+text[:-2]+'[/COLOR] البحث عن : [ '
	#GLOBAL_SEARCH_MENU(search,False)
	#xbmcgui.Dialog().ok(str(len(menuItemsLIST)),'MENUS')
	return

def IMPORT_VOD():
	if contentsDICT:
		results = READ_FROM_SQL3('IMPORT_SECTIONS','VOD')
		if results: contentsDICT[:] = contentsDICT+results ; return
		elif contentsDICT: previous_contentsDICT = contentsDICT[:] ; contentsDICT[:] = []
	else: previous_contentsDICT = []
	message = 'للأسف لديك مشكلة في هذا الموقع . ورسالة الخطأ كان فيها تفاصيل المشكلة . أذا المشكلة ليست حجب فجرب إرسال هذه المشكلة إلى المبرمج من قائمة خدمات البرنامج'
	#LOG_THIS('NOTICE','START TIMING')
	failed = 0
	if failed<=5:
		try: import AKOAM ; AKOAM.MENU('AKOAM')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع أكوام القديم',message)
	if failed<=5:
		try: import AKWAM ; AKWAM.MENU('AKWAM')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع أكوام الجديد',message)
	if failed<=5:
		try: import ALARAB ; ALARAB.MENU('ALARAB')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع كل العرب',message)
	if failed<=5:
		try: import ALFATIMI ; ALFATIMI.MENU('ALFATIMI')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع المنبر الفاطمي',message)
	if failed<=5:
		try: import ALKAWTHAR ; ALKAWTHAR.MENU('ALKAWTHAR')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع قناة الكوثر',message)
	if failed<=5:
		try: import ALMAAREF ; ALMAAREF.MENU('ALMAAREF')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع قناة المعارف',message)
	if failed<=5:
		try: import ARABLIONZ ; ARABLIONZ.MENU('ARABLIONZ')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع عرب ليونز',message)
	if failed<=5:
		try: import ARABSEED ; ARABSEED.MENU('ARABSEED')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع عرب سييد',message)
	if failed<=5:
		try: import EGYBESTVIP ; EGYBESTVIP.MENU('EGYBESTVIP')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع ايجي بيست vip',message)
	if failed<=5:
		try: import HELAL ; HELAL.MENU('HELAL')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع هلال يوتيوب',message)
	if failed<=5:
		try: import IFILM ; IFILM.MENU('IFILM_ARABIC')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع قناة اي فيلم العربي',message)
	if failed<=5:
		try: import IFILM ; IFILM.MENU('IFILM_ENGLISH')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع قناة اي فيلم انكليزي',message)
	if failed<=5:
		try: import PANET ; PANET.MENU('PANET')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع بانيت',message)
	if failed<=5:
		try: import SHAHID4U ; SHAHID4U.MENU('SHAHID4U')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع شاهد فوريو',message)
	if failed<=5:
		try: import SHOOFMAX ; SHOOFMAX.MENU('SHOOFMAX')
		except: failed += 1 ; xbmcgui.Dialog().ok('موقع شوف ماكس',message)
	#import EGYBEST			;	EGYBEST.MENU('EGYBEST')
	#import HALACIMA		;	HALACIMA.MENU('HALACIMA')
	#import MOVIZLAND		;	MOVIZLAND.MENU('MOVIZLAND')
	#import SERIES4WATCH	;	SERIES4WATCH.MENU('SERIES4WATCH')
	if failed>5: xbmcgui.Dialog().ok('عندك مشكلة','لديك مشكلة غريبة وغير طبيعية في اكثر من 5 مواقع من مواقع البرنامج ... ومشكلة مثل هذه تسبب عطل هذه الوظيفة وسببها قد يكون عدم وجود إنترنيت في جهازك')
	else: WRITE_TO_SQL3('IMPORT_SECTIONS','VOD',contentsDICT,LONG_CACHE)
	if previous_contentsDICT: contentsDICT[:] = previous_contentsDICT+contentsDICT
	return

def IMPORT_IPTV(options):
	#results = READ_FROM_SQL3('IMPORT_SECTIONS','LIVE')
	#if results:
	#	menuItemsLIST[:] = results
	#	return
	message = 'للأسف لديك مشكلة في هذا الموقع . ورسالة الخطأ كان فيها تفاصيل المشكلة . أذا المشكلة ليست حجب فجرب إرسال هذه المشكلة إلى المبرمج من قائمة خدمات البرنامج'
	import IPTV
	if IPTV.isIPTVFiles(True):
		#xbmcgui.Dialog().ok('11111',str(len(menuItemsLIST)))
		#if 'RANDOM' in options: mode = 238
		#else: mode = 234
		try: IPTV.GROUPS('LIVE_GROUPED','','TV_'+options)
		except: xbmcgui.Dialog().ok('موقع IPTV للقنوات',message)
		try: IPTV.GROUPS('VOD_MOVIES','','MOVIES_'+options)
		except: xbmcgui.Dialog().ok('موقع IPTV للافلام',message)
		try: IPTV.GROUPS('VOD_SERIES','','SERIES_'+options)
		except: xbmcgui.Dialog().ok('موقع IPTV للمسلسلات',message)
		#xbmcgui.Dialog().ok('33333',str(len(menuItemsLIST)))
		#WRITE_TO_SQL3('IMPORT_SECTIONS','LIVE',menuItemsLIST,UNLIMITED_CACHE)
	return

def CATEGORIES_MENU(options):
	options = options.replace('DELETE_DELETE_','DELETE_')
	addMenuItem('dir','تحديث هذه القائمة','',165,'','','DELETE_'+options)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	if 'VOD' in options:
		if 'DELETE' in options: DELETE_FROM_SQL3('IMPORT_SECTIONS','VOD')
		IMPORT_VOD()
		for nameonly in sorted(contentsDICT.keys()):
			addMenuItem('dir',nameonly,nameonly,166,'','',options)
	elif 'LIVE' in options:
		if 'DELETE' in options:
			import IPTV
			IPTV.CREATE_STREAMS()
			options = options.replace('DELETE_','')
		IMPORT_IPTV(options)
	return

def CATEGORIES_SUBMENU(nameonly,options):
	if 'VOD' in options: IMPORT_VOD()
	elif 'LIVE' in options: IMPORT_IPTV(options)
	if contentsDICT=={}: return
	if 'RANDOM' in options:
		addMenuItem('dir','[ [COLOR FFC89008]'+nameonly+'[/COLOR] القسم : [ ',nameonly,166,'','',options)
		addMenuItem('dir','إعادة الطلب العشوائي من نفس القسم',nameonly,166,'','',options)
		addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	for website in sorted(contentsDICT[nameonly].keys()):
		type,name,url,mode2,image,page,text = contentsDICT[nameonly][website]
		if 'RANDOM' in options: MAIN_DISPATCHER(mode2,url,text,page)
		else:
			if len(contentsDICT[nameonly])==1: MAIN_DISPATCHER(mode2,url,text,page)
			else: addMenuItem('dir',website,url,mode2,image,page,text)
	#LOG_THIS('NOTICE',str(contentsDICT[nameonly]))
	#xbmcgui.Dialog().ok(str(contentsDICT[nameonly].keys()),str(contentsDICT[nameonly]))
	return

def RANDOM_CATEGORY(options,mode):
	#xbmcgui.Dialog().ok('',options)
	if 'VOD' in options:
		IMPORT_VOD()
		if contentsDICT=={}: return
		list1 = contentsDICT.keys()
		nameonly = random.sample(list1,1)[0]
		list2 = contentsDICT[nameonly].keys()
		website = random.sample(list2,1)[0]
		type,name,url,mode2,image,page,text = contentsDICT[nameonly][website]
		name = name.replace('[COLOR FFC89008]','').replace('[/COLOR]','').replace('_MOD_','')
		if name.count('_')>1: name = name.split('_',2)[2]
		if name=='': name = '....'
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   website: '+website+'   name: '+name+'   url: '+url+'   mode: '+str(mode2))
		addMenuItem('dir','[ [COLOR FFC89008]'+name+'[/COLOR] القسم : [ ','',mode,'','',options)
		addMenuItem('dir','إعادة طلب قسم عشوائي','',mode,'','',options)
		addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
		MAIN_DISPATCHER(mode2,url,text,page)
	elif 'LIVE' in options:
		addMenuItem('dir','[ [COLOR FFC89008]  [/COLOR] القسم : [ ','',mode,'','',options)
		addMenuItem('dir','إعادة طلب قسم عشوائي','',mode,'','',options)
		addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
		IMPORT_IPTV(options)
	for i in range(0,10):
		if str(menuItemsLIST[3:]).count('link')>0: break
		menuItemsLIST2 = []
		for type,name,url,mode2,image,page,text in menuItemsLIST[3:]:
			if 'صفحة' in name: continue
			menuItemsLIST2.append([type,name,url,mode2,image,page,text])
		if len(menuItemsLIST2)>0:
			menuItem = random.sample(menuItemsLIST2,1)[0]
			type,name,url,mode2,image,page,text = menuItem
			del menuItemsLIST[3:]
			name = name.replace('[COLOR FFC89008]','').replace('[/COLOR]','').replace('_MOD_','')
			if name.count('_')>1: name = name.split('_',2)[2]
			if name=='': name = '....'
			menuItemsLIST[0][1] = '[ [COLOR FFC89008]'+name+'[/COLOR] القسم : [ '
			LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   name: '+name+'   url: '+url+'   mode: '+str(mode2))
			MAIN_DISPATCHER(mode2,url,text,page)
	return





