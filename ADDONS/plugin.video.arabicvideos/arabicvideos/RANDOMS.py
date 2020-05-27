# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from LIBRARY import *

script_name='RANDOMS'

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
	addMenuItem('folder','[COLOR FFC89008]10.  [/COLOR]'+'فيديوهات IPTV بحث عشوائي','',164,'','','IPTV')
	addMenuItem('folder','[COLOR FFC89008]11.  [/COLOR]'+'فيديوهات IPTV عشوائية من قسم','',165,'','','IPTV_RANDOM')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return

def RANDOM_LIVETV(options):
	addMenuItem('folder','إعادة طلب قنوات عشوائية','',161,'','','LIVETV_RANDOM')
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
	if 'RANDOM' in options and len(menuItemsLIST)>random_size:
		menuItemsLIST[:] = random.sample(menuItemsLIST,random_size)
	menuItemsLIST[:] = previous+menuItemsLIST
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
	if 'SITES' in options:
		search_modes = [19,29,49,59,69,79,99,119,139,149,209,229,249,259]
		#search_modes = [39]	panet search does not work at panet website
	else:
		search_modes = [239]
		import IPTV
		if not IPTV.isIPTVFiles(True): return
	count,repeats = 0,0
	addMenuItem('folder','البحث عن : [  ]','',164,'','',options)
	addMenuItem('folder','إعادة البحث العشوائي','',164,'','',options)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	for i in range(0,20):
		text = random.sample(list2,1)[0]
		text = text+'::'
		mode = random.sample(search_modes,1)[0]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Video Search   mode:'+str(mode)+'  text:'+text)
		results = MAIN_DISPATCHER('','','',mode,'','',text)
		if len(menuItemsLIST)>3: break
	menuItemsLIST[0][1] = '[ [COLOR FFC89008]'+text[:-2]+'[/COLOR] البحث عن : [ '
	if len(menuItemsLIST)>(random_size+3): menuItemsLIST[:] = menuItemsLIST[:3]+random.sample(menuItemsLIST[3:],random_size)
	#GLOBAL_SEARCH_MENU(search,False)
	#xbmcgui.Dialog().ok(str(len(menuItemsLIST)),'MENUS')
	return

def IMPORT_SITES_HELPER(html,title,failed):
	if '__Error__' in html:
		failed += 1
		dummy,code,reason = html.split(':',2)
		messageARABIC,messageENGLISH = EXPLAIN_ERRORS(code,reason,False)
		xbmcgui.Dialog().ok(title,messageARABIC,messageENGLISH)
	return failed

def IMPORT_SITES():
	global contentsDICT
	results = READ_FROM_SQL3('IMPORT_SECTIONS','SITES')
	if results: contentsDICT = results ; return
	#LOG_THIS('NOTICE','START TIMING')
	failed = 0
	if failed<=5:
		import AKOAM ; html = AKOAM.MENU('AKOAM')
		failed = IMPORT_SITES_HELPER(html,'موقع أكوام القديم AKOAM',failed)
	if failed<=5:
		import AKWAM ; html = AKWAM.MENU('AKWAM')
		failed = IMPORT_SITES_HELPER(html,'موقع أكوام الجديد AKWAM',failed)
	if failed<=5:
		import ALARAB ; html = ALARAB.MENU('ALARAB')
		failed = IMPORT_SITES_HELPER(html,'موقع كل العرب ALARAB',failed)
	if failed<=5:
		import ALFATIMI ; html = ALFATIMI.MENU('ALFATIMI')
		failed = IMPORT_SITES_HELPER(html,'موقع المنبر الفاطمي ALFATIMI',failed)
	if failed<=5:
		import ALKAWTHAR ; html = ALKAWTHAR.MENU('ALKAWTHAR')
		failed = IMPORT_SITES_HELPER(html,'موقع قناة الكوثر ALKAWTHAR',failed)
	if failed<=5:
		import ALMAAREF ; html = ALMAAREF.MENU('ALMAAREF')
		failed = IMPORT_SITES_HELPER(html,'موقع قناة المعارف ALMAAREF',failed)
	if failed<=5:
		import ARABLIONZ ; html = ARABLIONZ.MENU('ARABLIONZ')
		failed = IMPORT_SITES_HELPER(html,'موقع عرب ليونز ARABLIONZ',failed)
	if failed<=5:
		import ARABSEED ; html = ARABSEED.MENU('ARABSEED')
		failed = IMPORT_SITES_HELPER(html,'موقع عرب سييد ARABSEED',failed)
	if failed<=5:
		import EGYBESTVIP ; html = EGYBESTVIP.MENU('EGYBESTVIP')
		failed = IMPORT_SITES_HELPER(html,'vip موقع ايجي بيست EGYBESTVIP',failed)
	if failed<=5:
		import HELAL ; html = HELAL.MENU('HELAL')
		failed = IMPORT_SITES_HELPER(html,'موقع هلال يوتيوب HELALCIMA',failed)
	if failed<=5:
		import IFILM ; html = IFILM.MENU('IFILM_ARABIC')
		failed = IMPORT_SITES_HELPER(html,'موقع قناة اي فيلم العربي IFILM_ARABIC',failed)
	if failed<=5:
		import IFILM ; html = IFILM.MENU('IFILM_ENGLISH')
		failed = IMPORT_SITES_HELPER(html,'موقع قناة اي فيلم انكليزي IFILM_ENGLISH',failed)
	if failed<=5:
		import SHAHID4U ; html = SHAHID4U.MENU('SHAHID4U')
		failed = IMPORT_SITES_HELPER(html,'موقع شاهد فوريو SHAHID4U',failed)
	if failed<=5:
		import PANET ; html = PANET.MENU('PANET')
		failed = IMPORT_SITES_HELPER(html,'موقع بانيت PANET',failed)
	if failed<=5:
		import SHOOFMAX ; html = SHOOFMAX.MENU('SHOOFMAX')
		failed = IMPORT_SITES_HELPER(html,'موقع شوف ماكس SHOOFMAX',failed)
	#import EGYBEST			;	EGYBEST.MENU('EGYBEST')
	#import HALACIMA		;	HALACIMA.MENU('HALACIMA')
	#import MOVIZLAND		;	MOVIZLAND.MENU('MOVIZLAND')
	#import SERIES4WATCH	;	SERIES4WATCH.MENU('SERIES4WATCH')
	if failed>5: xbmcgui.Dialog().ok('عندك مشكلة','لديك مشكلة غريبة وغير طبيعية في اكثر من 5 مواقع من مواقع البرنامج ... ومشكلة مثل هذه تسبب عطل هذه الوظيفة وسببها قد يكون عدم وجود إنترنيت في جهازك')
	else:
		"""
		for key1 in contentsDICT.keys():
			for key2 in contentsDICT[key1].keys():
				name = contentsDICT[key1][key2][1]
				name2 = name.replace('VOD_','').replace('_MOD_','')
				if name2.count('_')>1: name2 = name2.split('_',2)[2]
				if name2=='': name2 = '....'
				contentsDICT[key1][key2][1] = name2
		"""
		WRITE_TO_SQL3('IMPORT_SECTIONS','SITES',contentsDICT,LONG_CACHE)
	return

def IMPORT_IPTV(options):
	message = 'للأسف لديك مشكلة في هذا الموقع . ورسالة الخطأ كان فيها تفاصيل المشكلة . أذا المشكلة ليست حجب فجرب إرسال هذه المشكلة إلى المبرمج من قائمة خدمات البرنامج'
	import IPTV
	if IPTV.isIPTVFiles(True):
		if 'IPTV' in options and 'LIVE' not in options:
			try: IPTV.GROUPS('VOD_MOVIES','',options+'_MOVIES')
			except: xbmcgui.Dialog().ok('موقع IPTV للافلام',message)
			try: IPTV.GROUPS('VOD_SERIES','',options+'_SERIES')
			except: xbmcgui.Dialog().ok('موقع IPTV للمسلسلات',message)
		if 'IPTV' in options and 'VOD' not in options:
			try: IPTV.GROUPS('LIVE_ORIGINAL','',options+'_TV')
			except: xbmcgui.Dialog().ok('موقع IPTV للقنوات',message)
		for item in menuItemsLIST:
			item[1] = item[1].replace('IPTV_','').replace('_MOD_','')
			if item[1].count('_')>1: item[1] = item[1].split('_',2)[2]
			if item[1]=='': item[1] = '....'
	else: EXIT_PROGRAM('RANDOMS-IMPORT_IPTV-1st')
	return

def CATEGORIES_MENU(options):
	#xbmcgui.Dialog().ok('',options)
	options = options.replace('DELETE_DELETE_','DELETE_')
	addMenuItem('folder','تحديث هذه القائمة','',165,'','','DELETE_'+options)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	if 'SITES' in options:
		if 'DELETE' in options: DELETE_FROM_SQL3('IMPORT_SECTIONS','SITES')
		IMPORT_SITES()
		for nameonly in sorted(contentsDICT.keys()):
			addMenuItem('folder',nameonly,nameonly,166,'','',options)
	elif 'IPTV' in options:
		if 'DELETE' in options:
			import IPTV
			IPTV.CREATE_STREAMS()
			options = options.replace('DELETE_','')
		IMPORT_IPTV(options)
	return

def RANDOM_VOD_ITEMS(nameonly,options):
	#xbmcgui.Dialog().ok(nameonly,options)
	IMPORT_SITES()
	if contentsDICT=={}: return
	if 'RANDOM' in options:
		addMenuItem('folder','[ [COLOR FFC89008]'+nameonly+'[/COLOR] القسم : [ ',nameonly,166,'','',options)
		addMenuItem('folder','إعادة الطلب العشوائي من نفس القسم',nameonly,166,'','',options)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	for website in sorted(contentsDICT[nameonly].keys()):
		type,name,url,mode2,image,page,text = contentsDICT[nameonly][website]
		if 'RANDOM' in options or len(contentsDICT[nameonly])==1:
			MAIN_DISPATCHER(type,'',url,mode2,'',page,text)
			previousLIST,newLIST,newLIST2 = menuItemsLIST[:3],menuItemsLIST[3:],[]
			for item in newLIST:
				if 'صفحة' in item[1] or 'صفحه' in item[1] or 'page' in item[1].lower(): continue
				newLIST2.append(item)
			for i in range(0,5): random.shuffle(newLIST2)
			if 'RANDOM' in options: menuItemsLIST[:] = previousLIST+newLIST2[:random_size]
			else: menuItemsLIST[:] = previousLIST+newLIST2
		elif 'SITES' in options: addMenuItem('folder',website,url,mode2,image,page,text)
	#LOG_THIS('NOTICE',str(contentsDICT[nameonly]))
	#xbmcgui.Dialog().ok(str(contentsDICT[nameonly].keys()),str(contentsDICT[nameonly]))
	return

def RANDOM_CATEGORY(options,mode):
	#xbmcgui.Dialog().ok(options,str(mode))
	name,menuItemsLIST2 = '',[]
	addMenuItem('folder','[ [COLOR FFC89008]'+name+'[/COLOR] القسم : [ ','',mode,'','',options)
	addMenuItem('folder','إعادة طلب قسم عشوائي','',mode,'','',options)
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
		type,name,url,mode2,image,page,text = contentsDICT[nameonly][website]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   website: '+website+'   name: '+name+'   url: '+url+'   mode: '+str(mode2))
	elif 'IPTV' in options:
		IMPORT_IPTV(options)
		type,name,url,mode2,image,page,text = random.sample(menuItemsLIST,1)[0]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   name: '+name+'   url: '+url+'   mode: '+str(mode2))
	for i in range(0,10):
		if i>0: LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Category   name: '+name+'   url: '+url+'   mode: '+str(mode2))
		menuItemsLIST[:] = []
		MAIN_DISPATCHER(type,name,url,mode2,image,page,text)
		if 'IPTV' in options and mode2==167: del menuItemsLIST[:3]
		menuItemsLIST2 = []
		for type,name2,url,mode2,image,page,text in menuItemsLIST:
			if 'صفحة' in name2 or 'صفحه' in name2 or 'page' in name2.lower(): continue
			menuItemsLIST2.append([type,name2,url,mode2,image,page,text])
		if str(menuItemsLIST2).count('video')>0: break
		if str(menuItemsLIST2).count('live')>0: break
		if menuItemsLIST2: type,name,url,mode2,image,page,text = random.sample(menuItemsLIST2,1)[0]
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
	#xbmcgui.Dialog().ok(TYPE,GROUP)
	if TYPE=='VOD_SERIES': GROUP = GROUP.split('__')[0]
	addMenuItem('folder','[ [COLOR FFC89008]'+GROUP+'[/COLOR] القسم : [ ',TYPE,167,'','',GROUP)
	addMenuItem('folder','إعادة الطلب العشوائي من نفس القسم',TYPE,167,'','',GROUP)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	import IPTV
	if TYPE=='VOD_SERIES': IPTV.GROUPS(TYPE,GROUP,'')
	else: IPTV.ITEMS(TYPE,GROUP)
	if len(menuItemsLIST)>(random_size+3): menuItemsLIST[:] = menuItemsLIST[:3]+random.sample(menuItemsLIST[3:],random_size)
	#LOG_THIS('NOTICE',str(contentsDICT[nameonly]))
	#xbmcgui.Dialog().ok(str(contentsDICT[nameonly].keys()),str(contentsDICT[nameonly]))
	return



