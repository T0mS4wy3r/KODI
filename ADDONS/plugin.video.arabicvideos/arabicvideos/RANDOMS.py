# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from LIBRARY import *

script_name='RANDOMS'

def MAIN(mode,url,text=''):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
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
	addMenuItem('dir','[COLOR FFC89008]  1.  [/COLOR]'+'قسم عشوائي','',162,'','','WEBSITES')
	addMenuItem('dir','[COLOR FFC89008]  2.  [/COLOR]'+'فيديوهات عشوائية','',163,'','','WEBSITES')
	addMenuItem('dir','[COLOR FFC89008]  3.  [/COLOR]'+'فيديوهات بحث عشوائي','',164,'','','WEBSITES')
	addMenuItem('dir','[COLOR FFC89008]  4.  [/COLOR]'+'فيديو عشوائي من قسم','',165,'','','RANDOM_WEBSITES')
	addMenuItem('dir','[COLOR FFC89008]  5.  [/COLOR]'+'قنوات تلفزيون عشوائية','',161)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('dir','[COLOR FFC89008]  6.  [/COLOR]'+'قسم IPTV عشوائي','',162,'','','IPTV')
	addMenuItem('dir','[COLOR FFC89008]  7.  [/COLOR]'+'فيديو IPTV عشوائي','',163,'','','IPTV')
	addMenuItem('dir','[COLOR FFC89008]  8.  [/COLOR]'+'فيديو IPTV بحث عشوائي','',164,'','','IPTV')
	addMenuItem('dir','[COLOR FFC89008]  9.  [/COLOR]'+'فيديو IPTV عشوائي من قسم','',165,'','','RANDOM_IPTV')
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	return

def RANDOM_LIVETV():
	addMenuItem('dir','إعادة طلب قنوات عشوائية','',161)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('dir','[COLOR FFC89008] YUT   [/COLOR]'+'قنوات عربية من يوتيوب','',147)
	addMenuItem('dir','[COLOR FFC89008] YUT   [/COLOR]'+'قنوات أجنبية من يوتيوب','',148)
	addMenuItem('dir','[COLOR FFC89008] IFL    [/COLOR]'+'قناة آي فيلم من موقعهم','',28)
	addMenuItem('link','[COLOR FFC89008] MRF  [/COLOR]'+'قناة المعارف من موقعهم','',41)
	addMenuItem('link','[COLOR FFC89008] KWT  [/COLOR]'+'قناة الكوثر من موقعهم','',135)
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
	payload = { 'quantity' : '80' }
	data = urllib.urlencode(payload)
	#xbmcgui.Dialog().ok('',str(data))
	html = openURL_cached(SHORT_CACHE,url,data,headers,'','RANDOMS-SEARCH_RANDOM_VIDEOS-1st')
	html_blocks = re.findall('list-unstyled(.*?)clearfix',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('<span>(.*?)</span>.*?<span>(.*?)</span>',block,re.DOTALL)
	arbLIST,engLIST = [],[]
	for arbWORD, engWORD in items:
		if len(arbWORD)<=4 or len(engWORD)<=2: continue
		bad = False
		for i in [' ','"','`',',','.',':',';',"'",'-']:
			if i in arbWORD or i in engWORD:
				bad = True
				break
		if bad: continue
		arbLIST.append(arbWORD.lower())
		engLIST.append(engWORD.lower())
	list = ['كلمات عشوائية عربية','كلمات عشوائية إنكليزية']
	list2 = arbLIST+engLIST
	#selection = xbmcgui.Dialog().select('اختر كلمة للبحث عنها:', list2)
	"""
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
	if 'WEBSITES' in options:
		search_modes = [19,29,39,49,59,69,79,99,119,139,149,209,229,249,259]
		#search_modes = [39]
	else:
		search_modes = [239]
		import IPTV
		if not IPTV.isIPTVFiles(True): return
	count,repeats = 0,0
	addMenuItem('dir','كلمة البحث : [  ]','',164,'','',options)
	addMenuItem('dir','إعادة البحث عن فيديوهات عشوائية','',164,'','',options)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	while count==0 and repeats<20:
		text = random.sample(list2,1)[0]
		text = text+'::'
		mode = random.sample(search_modes,1)[0]
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Random Video Search   mode:'+str(mode)+'  text:'+text)
		results = MAIN_DISPATCHER(mode,'',text,'')
		#xbmcgui.Dialog().ok(str(repeats),str(results))
		count = len(menuItemsLIST)-2
		repeats = repeats+1
	if repeats<=20: menuItemsLIST[0][1] = 'كلمة البحث الحالية : [ '+text[:-2]+' ]'
	#GLOBAL_SEARCH_MENU(search,False)
	#xbmcgui.Dialog().ok(str(len(menuItemsLIST)),'MENUS')
	return

def IMPORT_WEBSITES():
	#LOG_THIS('NOTICE','START TIMING')
	try: import AKOAM		;	AKOAM.MENU('AKOAM')
	except: pass
	try: import AKWAM		;	AKWAM.MENU('AKWAM')
	except: pass
	try: import PANET		;	PANET.MENU('PANET')
	except: pass
	try: import HELAL		;	HELAL.MENU('HELAL')
	except: pass
	try: import IFILM		;	IFILM.MENU('IFILM')
	except: pass
	try: import ALARAB		;	ALARAB.MENU('ALARAB')
	except: pass
	try: import ALMAAREF	;	ALMAAREF.MENU('ALMAAREF')
	except: pass
	try: import ALFATIMI	;	ALFATIMI.MENU('ALFATIMI')
	except: pass
	try: import SHOOFMAX	;	SHOOFMAX.MENU('SHOOFMAX')
	except: pass
	try: import SHAHID4U	;	SHAHID4U.MENU('SHAHID4U')
	except: pass
	try: import ARABSEED	;	ARABSEED.MENU('ARABSEED')
	except: pass
	try: import EGYBESTVIP	;	EGYBESTVIP.MENU('EGYBESTVIP')
	except: pass
	try: import ARABLIONZ	;	ARABLIONZ.MENU('ARABLIONZ')
	except: pass
	try: import ALKAWTHAR	;	ALKAWTHAR.MENU('ALKAWTHAR')
	except: pass
	#import EGYBEST		;	EGYBEST.MENU('EGYBEST')
	#import HALACIMA	;	HALACIMA.MENU('HALACIMA')
	#import MOVIZLAND	;	MOVIZLAND.MENU('MOVIZLAND')
	#import SERIES4WATCH;	SERIES4WATCH.MENU('SERIES4WATCH')
	#LOG_THIS('NOTICE','END TIMING')
	return

def IMPORT_IPTV():
	import IPTV
	if not IPTV.isIPTVFiles(True): return
	try: IPTV.GROUPS('VOD_MOVIES','','MOVIES')
	except: pass
	try: IPTV.GROUPS('VOD_SERIES','','SERIES')
	except: pass
	try: IPTV.GROUPS('LIVE_GROUPED','','TV')
	except: pass
	return

def CATEGORIES_MENU(options):
	if 'WEBSITES' in options: IMPORT_WEBSITES()
	else: IMPORT_IPTV()
	for nameonly in sorted(contentsDICT.keys()):
		addMenuItem('dir',nameonly,nameonly,166,'','',options)
	return

def CATEGORIES_SUBMENU(nameonly,options):
	if 'WEBSITES' in options: IMPORT_WEBSITES()
	elif 'IPTV' in options: IMPORT_IPTV()
	if 'RANDOM' in options:
		addMenuItem('dir','القسم الحالي : [ '+nameonly+' ]',nameonly,166,'','',options)
		addMenuItem('dir','إعادة طلب فيديوهات عشوائية',nameonly,166,'','',options)
		addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	for website in contentsDICT[nameonly].keys():
		name,url,mode,iconimage,page,text = contentsDICT[nameonly][website]
		if   website=='AKOAM'		: name = 'موقع أكوام القديم'
		elif website=='AKWAM'		: name = 'موقع أكوام الجديد'
		elif website=='PANET'		: name = 'موقع بانيت'
		elif website=='IFILM'		: name = 'موقع قناة اي فيلم'
		elif website=='HELAL'		: name = 'موقع هلال يوتيوب'
		elif website=='ALARAB'		: name = 'موقع كل العرب'
		elif website=='ALFATIMI'	: name = 'موقع المنبر الفاطمي'
		elif website=='ALMAAREF'	: name = 'موقع قناة المعارف'
		elif website=='SHOOFMAX'	: name = 'موقع شوف ماكس'
		elif website=='SHAHID4U'	: name = 'موقع شاهد فوريو'
		elif website=='ARABSEED'	: name = 'موقع عرب سييد'
		elif website=='ALKAWTHAR'	: name = 'موقع قناة الكوثر'
		elif website=='ARABLIONZ'	: name = 'موقع عرب ليونز'
		elif website=='EGYBESTVIP'	: name = 'موقع ايجي بيست vip'
		elif website=='IPTV'		: name = 'IPTV'
		if 'RANDOM' in options: MAIN_DISPATCHER(mode,url,text,page)
		else:
			if len(contentsDICT[nameonly])==1: MAIN_DISPATCHER(mode,url,text,page)
			else: addMenuItem('dir',name,url,mode,iconimage,page,text)
	#LOG_THIS('NOTICE',str(contentsDICT[nameonly]))
	#xbmcgui.Dialog().ok(str(contentsDICT[nameonly].keys()),str(contentsDICT[nameonly]))
	return

def RANDOM_CATEGORY(options,mode):
	if 'WEBSITES' in options: IMPORT_WEBSITES()
	elif 'IPTV' in options: IMPORT_IPTV()
	for name in contentsDICT.keys():
		if 'مصنف' in name or 'مفلتر' in name: del contentsDICT[name]
	list1 = contentsDICT.keys()
	if len(list1)>0:
		nameonly = random.sample(list1,1)[0]
		list2 = contentsDICT[nameonly].keys()
		if len(list2)>0:
			addMenuItem('dir','القسم الحالي : [ '+nameonly+' ]','',mode,'','',options)
			addMenuItem('dir','إعادة طلب قسم جديد','',mode,'','',options)
			addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
			website = random.sample(list2,1)[0]
			name,url,mode2,iconimage,page,text = contentsDICT[nameonly][website]
			results = MAIN_DISPATCHER(mode2,url,text,page)
	return




