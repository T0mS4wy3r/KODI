# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='IPTV'
menu_name='_IPT_'

def MAIN(mode,url,text,type):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	#LOG_THIS('NOTICE','start')
	if   mode==230: results = MENU()
	elif mode==231: results = ADD_ACCOUNT()
	elif mode==232: results = CREATE_STREAMS(True)
	elif mode==233: results = GROUPS(url,text)
	elif mode==234: results = ITEMS(url,text)
	elif mode==235: results = PLAY(url,type)
	elif mode==236: results = CHECK_ACCOUNT(True)
	elif mode==237: results = DELETE_IPTV_FILES(True)
	elif mode==238: results = EPG_ITEMS(url,text)
	elif mode==239: results = SEARCH(text)
	elif mode==280: results = ADD_USERAGENT()
	elif mode==281: results = COUNTS()
	else: results = False
	#LOG_THIS('NOTICE','end')
	return results

def MENU():
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'بحث في ملفات IPTV','',239,'','','_REMEMBERRESULTS_')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة','LIVE_GROUPED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'أفلام مصنفة','VOD_MOVIES_GROUPED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'مسلسلات مصنفة','VOD_SERIES_GROUPED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مجهولة','VOD_UNKNOWN_GROUPED',233)
	#addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مجهولة','LIVE_UNKNOWN',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة ومرتبة','LIVE_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'أفلام مصنفة ومرتبة','VOD_MOVIES_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'مسلسلات مصنفة ومرتبة','VOD_SERIES_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مجهولة ومرتبة','VOD_UNKNOWN_GROUPED_SORTED',233)
	#addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مجهولة','LIVE_UNKNOWN_SORTED',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'القنوات الأصلية بدون تغيير','LIVE_ORIGINAL_GROUPED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'الفيديوهات الأصلية بدون تغيير','VOD_ORIGINAL_GROUPED',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة من أسمائها ومرتبة','LIVE_FROM_NAME_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مصنفة من أسمائها ومرتبة','VOD_FROM_NAME_SORTED',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة من أقسامها ومرتبة','LIVE_FROM_GROUP_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مصنفة من أقسامها ومرتبة','VOD_FROM_GROUP_SORTED',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'برامج القنوات (جدول فقط)','LIVE_EPG_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'أرشيف القنوات للأيام الماضية','LIVE_TIMESHIFT_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'أرشيف برامج القنوات للأيام الماضية','LIVE_ARCHIVED_GROUPED_SORTED',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'إضافة اشتراك IPTV','',231)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'فحص اشتراك IPTV','',236)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'عدد فيديوهات IPTV','',281)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'جلب ملفات IPTV','',232)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'مسح ملفات IPTV','',237)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'تغيير IPTV User-Agent','',280)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return

def CHECK_ACCOUNT(showDialog=True):
	ok,status = False,''
	settings = xbmcaddon.Addon(id=addon_id)
	useragent = settings.getSetting('iptv.useragent')
	iptvURL = settings.getSetting('iptv.url')
	headers = {'User-Agent':useragent}
	username = re.findall('username=(.*?)&',iptvURL+'&',re.DOTALL)
	password = re.findall('password=(.*?)&',iptvURL+'&',re.DOTALL)
	if username and password:
		username = username[0]
		password = password[0]
		url_parts = iptvURL.split('/')
		server = url_parts[0]+'//'+url_parts[2]
		settings.setSetting('iptv.username',username)
		settings.setSetting('iptv.password',password)
		settings.setSetting('iptv.server',server)
		url = server+'/player_api.php?username='+username+'&password='+password
		response = openURL_requests_cached(NO_CACHE,'GET',url,'',headers,False,'','IPTV-CHECK_ACCOUNT-1st')
		html = response.content
		if '___Error___' not in html:
			try:
				dict = EVAL(html)
				time_now = dict['server_info']['time_now']
				status = dict['user_info']['status']
				ok = True
			except: pass
			if ok:
				struct = time.strptime(time_now,'%Y-%m-%d %H:%M:%S')
				timestamp = int(time.mktime(struct))
				timediff = int(now-timestamp)
				# normalizing to the closest half hour with 15 minutes error range
				timediff = int((timediff+900)/1800)*1800
				settings.setSetting('iptv.timestamp',str(now))
				settings.setSetting('iptv.timediff',str(timediff))
				if showDialog:
					sep1 = '\r\n'
					struct = time.localtime(int(dict['user_info']['created_at']))
					created_at = time.strftime('%Y-%m-%d  %H:%M:%S',struct)
					struct = time.localtime(int(dict['user_info']['exp_date']))
					exp_date = time.strftime('%Y-%m-%d  %H:%M:%S',struct)
					max = dict['user_info']['max_connections']
					active = dict['user_info']['active_cons']
					is_trial = dict['user_info']['is_trial']
					parts = iptvURL.split('&',1)
					message = parts[0]+sep1+'&'+parts[1]+sep1
					message += sep1+'Status:  '+'[COLOR FFC89008]'+status+'[/COLOR]'
					message += sep1+'Trial:    '+'[COLOR FFC89008]'+str(is_trial=='1')+'[/COLOR]'
					message += sep1+'Created  At:  '+'[COLOR FFC89008]'+created_at+'[/COLOR]'
					message += sep1+'Expiry Date:  '+'[COLOR FFC89008]'+exp_date+'[/COLOR]'
					message += sep1+'Connections   ( Active / Maximum ) :  '+'[COLOR FFC89008]'+active+' / '+max+'[/COLOR]'
					message += sep1+'Allowed Outputs:   '+'[COLOR FFC89008]'+" , ".join(dict['user_info']['allowed_output_formats'])+'[/COLOR]'
					message += sep1+sep1+str(dict['server_info'])
					if status=='Active': XBMCGUI_DIALOG_TEXTVIEWER('الاشتراك يعمل بدون مشاكل',message)
					else: XBMCGUI_DIALOG_TEXTVIEWER('يبدو أن هناك مشكلة في الاشتراك',message)
	if ok and status=='Active':
		LOG_THIS('NOTICE','Checking IPTV URL   [ IPTV account is OK ]   [ '+iptvURL+' ]')
		result = True
	else:
		LOG_THIS('ERROR','Checking IPTV URL   [ Does not work ]   [ '+iptvURL+' ]')
		if iptvURL: XBMCGUI_DIALOG_OK('فحص اشتراك IPTV','رابط اشتراك IPTV الذي قمت انت بإضافته إلى البرنامج لا يعمل أو الرابط غير موجود في البرنامج . أذهب إلى قائمة اشتراك IPTV وقم بإعادة إدخال رابط IPTV جديد أو قم بإصلاح الرابط القديم')
		result = False
	return result

def GROUPS(TYPE,GROUP,website=''):
	if website=='': show = True
	else: show = False
	if not isIPTVFiles(show): return
	results = READ_FROM_SQL3('IPTV_GROUPS',[TYPE,GROUP,website])
	if results: menuItemsLIST[:] = menuItemsLIST+results ; return
	else: previous_menuItemsLIST = menuItemsLIST[:] ; menuItemsLIST[:] = []
	streams = READ_FROM_SQL3('IPTV_STREAMS',TYPE)
	groups,unique,logos = [],[],[]
	for dict in streams:
		groups.append(dict['group'])
		logos.append(dict['img'])
	z = zip(groups,logos)
	z = sorted(z, reverse=False, key=lambda key: key[0])
	if '__IPTVSeries__' in GROUP: MAINGROUP,SUBGROUP = GROUP.split('__IPTVSeries__')
	else: MAINGROUP,SUBGROUP = GROUP,''
	#XBMCGUI_DIALOG_OK(TYPE,GROUP)
	menu_name2 = menu_name
	if len(z)>0:
		for group,img in z:
			if website!='':
				if '__IPTVSeries__' in group: menu_name2 = 'SERIES'
				elif '!!__UNKNOWN__!!' in group: menu_name2 = 'UNKNOWN'
				elif 'LIVE' in TYPE: menu_name2 = 'LIVE'
				else: menu_name2 = 'VIDEOS'
				menu_name2 = ',[COLOR FFC89008]'+menu_name2+': [/COLOR]'
			if '__IPTVSeries__' in group: maingroup,subgroup = group.split('__IPTVSeries__')
			else: maingroup,subgroup = group,''
			if GROUP=='':
				if maingroup in unique: continue
				unique.append(maingroup)
				if 'RANDOM' in website: addMenuItem('folder',menu_name2+maingroup,TYPE,167,img,'',group)
				elif '__IPTVSeries__' in group: addMenuItem('folder',menu_name2+maingroup,TYPE,233,'','',group)
				else: addMenuItem('folder',menu_name2+maingroup,TYPE,234,'','',group)
			elif '__IPTVSeries__' in group and maingroup==MAINGROUP:
				if subgroup in unique: continue
				unique.append(subgroup)
				if '!!__UNKNOWN__!!' in subgroup: img = ''
				if 'RANDOM' in website: addMenuItem('folder',menu_name2+subgroup,TYPE,167,img,'',group)
				else: addMenuItem('folder',menu_name2+subgroup,TYPE,234,img,'',group)
	else:
		addMenuItem('link',menu_name2+'هذه الخدمة غير موجودة في اشتراكك','',9999)
		addMenuItem('link',menu_name2+'أو رابط IPTV الذي أنت أضفته غير صحيح','',9999)
	WRITE_TO_SQL3('IPTV_GROUPS',[TYPE,GROUP,website],menuItemsLIST,PERMANENT_CACHE)
	menuItemsLIST[:] = previous_menuItemsLIST+menuItemsLIST
	return

def ITEMS(TYPE,GROUP):
	#XBMCGUI_DIALOG_OK(TYPE,GROUP)
	if not isIPTVFiles(True): return
	#LOG_THIS('NOTICE','before DATABASE')
	results = READ_FROM_SQL3('IPTV_ITEMS',[TYPE,GROUP])
	if results: menuItemsLIST[:] = menuItemsLIST+results ; return
	else: previous_menuItemsLIST = menuItemsLIST[:] ; menuItemsLIST[:] = []
	streams = READ_FROM_SQL3('IPTV_STREAMS',TYPE)
	#XBMCGUI_DIALOG_OK(TYPE+'___:'+GROUP,str(len(streams)))
	if '__IPTVSeries__' in GROUP: MAINGROUP,SUBGROUP = GROUP.split('__IPTVSeries__')
	else: MAINGROUP,SUBGROUP = GROUP,''
	#XBMCGUI_DIALOG_OK(MAINGROUP,SUBGROUP)
	for dict in streams:
		#if 'EG - ' in dict['title']: LOG_THIS('NOTICE','111111'+str(dict))
		group = dict['group']
		if '__IPTVSeries__' in group: maingroup,subgroup = group.split('__IPTVSeries__')
		else: maingroup,subgroup = group,''
		cond1 = ('GROUPED' in TYPE or TYPE=='ALL') and group==GROUP
		cond2 = ('GROUPED' not in TYPE and TYPE!='ALL') and maingroup==MAINGROUP
		if cond1 or cond2:
			#if 'EG - ' in dict['title']: LOG_THIS('NOTICE','222222'+str(dict))
			title = dict['title']
			url = dict['url']
			img = dict['img']
			if   'ARCHIVED' in TYPE: addMenuItem('folder',menu_name+title,url,238,img,'','archive')
			elif 'EPG' in TYPE: addMenuItem('folder',menu_name+title,url,238,img,'','full_epg')
			elif 'TIMESHIFT' in TYPE: addMenuItem('folder',menu_name+title,url,238,img,'','timeshift')
			elif 'LIVE' in TYPE: addMenuItem('live',menu_name+title,url,235,img)
			else: addMenuItem('video',menu_name+title,url,235,img)
	#XBMCGUI_DIALOG_OK('OUT',str(menuItemsLIST))
	WRITE_TO_SQL3('IPTV_ITEMS',[TYPE,GROUP],menuItemsLIST,PERMANENT_CACHE)
	menuItemsLIST[:] = previous_menuItemsLIST+menuItemsLIST
	return

def EPG_ITEMS(url,function):
	settings = xbmcaddon.Addon(id=addon_id)
	useragent = settings.getSetting('iptv.useragent')
	headers = {'User-Agent':useragent}
	if not isIPTVFiles(True): return
	timestamp = settings.getSetting('iptv.timestamp')
	if timestamp=='' or now-int(timestamp)>24*HOUR:
		ok = CHECK_ACCOUNT(False)
		if not ok: return
	timediff = int(settings.getSetting('iptv.timediff'))
	server = settings.getSetting('iptv.server')
	username = settings.getSetting('iptv.username')
	password = settings.getSetting('iptv.password')
	url_parts = url.split('/')
	stream_id = url_parts[-1].replace('.ts','').replace('.m3u8','')
	#XBMCGUI_DIALOG_OK(str(timediff),str(timestamp))
	if function=='short_epg': url_action = 'get_short_epg'
	else: url_action = 'get_simple_data_table'
	epg_url = server+'/player_api.php?username='+username+'&password='+password+'&action='+url_action+'&stream_id='+stream_id
	html = openURL_cached(NO_CACHE,epg_url,'',headers,'','IPTV-EPG_ITEMS-2nd')
	archive_files = EVAL(html)
	#XBMCGUI_DIALOG_OK('',str(archive_files))
	#with open('S:\\00iptv.txt','w') as f: f.write(html)
	all_epg = archive_files['epg_listings']
	epg_items = []
	if function in ['archive','timeshift']:
		for dict in all_epg:
			if dict['has_archive']==1:
				epg_items.append(dict)
				if function in ['timeshift']: break
		if not epg_items: return
		addMenuItem('link',menu_name+'[COLOR FFC89008]الملفات الأولي بهذه القائمة قد لا تعمل[/COLOR]','',9999)
		if function in ['timeshift']:
			length_hours = 2
			length_secs = length_hours*HOUR
			epg_items = []
			initial_timestamp = int(int(dict['start_timestamp'])/length_secs)*length_secs
			finish_timestamp = now+length_secs
			videos_count = int((finish_timestamp-initial_timestamp)/HOUR)
			for count in range(videos_count):
				if count>=6:
					if count%length_hours!=0: continue
					duration = length_secs
				else: duration = length_secs/2
				start_timestamp = initial_timestamp+count*HOUR
				dict = {}
				dict['title'] = ''
				struct = time.localtime(start_timestamp-timediff-HOUR)
				dict['start'] = time.strftime('%Y-%m-%d:%H:%M:%S',struct)
				dict['start_timestamp'] = str(start_timestamp)
				dict['stop_timestamp'] = str(start_timestamp+duration)
				epg_items.append(dict)
	elif function in ['short_epg','full_epg']: epg_items = all_epg
	if function=='full_epg' and len(epg_items)>0: addMenuItem('link',menu_name+'[COLOR FFC89008]هذه قائمة برامج القنوات (جدول فقط)ـ[/COLOR]','',9999)
	#english = ['Sat', 'Sun', 'Mon', 'Tue', 'Wed' , 'Thu', 'Fri']
	#arabic = ['سبت', 'أحد', 'أثنين', 'ثلاثاء', 'أربعاء', 'خميس', 'جمعة']
	epg_list = []
	img = xbmc.getInfoLabel('ListItem.Icon')
	for dict in epg_items:
		title = base64.b64decode(dict['title'])
		start_timestamp = int(dict['start_timestamp'])
		stop_timestamp = int(dict['stop_timestamp'])
		duration_minutes = str(int((stop_timestamp-start_timestamp+59)/60))
		start_string = dict['start'].replace(' ',':')
		#struct = time.gmtime(start_timestamp-timediff+time.altzone-3600)
		#start_string = time.strftime('%Y-%m-%d:%H:%M:%S',struct)
		struct = time.localtime(start_timestamp-HOUR)
		time_string = time.strftime('%H:%M',struct)
		english_dayname = time.strftime('%a',struct)
		#dayname_index = english.index(english_dayname)
		#arabic_dayname = arabic[dayname_index]
		#title = 'ـ '+title+'  ('+duration_minutes+'دق) '+time_string+' '+arabic_dayname
		if function=='short_epg': title = '[COLOR FFFFFF00]'+time_string+' ـ '+title+'[/COLOR]'
		elif function=='timeshift': title = english_dayname+' '+time_string+' ('+duration_minutes+'min)'
		else: title = english_dayname+' '+time_string+' ('+duration_minutes+'min)   '+title+' ـ'
		if function in ['archive','full_epg','timeshift']:
			timeshift_url = server+'/timeshift/'+username+'/'+password+'/'+duration_minutes+'/'+start_string+'/'+stream_id+'.m3u8'
			if function=='full_epg': addMenuItem('link',menu_name+title,timeshift_url,9999,img)
			else: addMenuItem('video',menu_name+title,timeshift_url,235,img)
		epg_list.append(title)
	if function=='short_epg': selection = XBMCGUI_DIALOG_CONTEXTMENU(epg_list)
	return epg_list

def PLAY(url,type):
	settings = xbmcaddon.Addon(id=addon_id)
	useragent = settings.getSetting('iptv.useragent')
	if useragent!='': url = url+'|User-Agent='+useragent
	"""
	if type=='live':
		xbmc.Player().play(url)
		randomNumber = str(random.randrange(111111111111,999999999999))
		url2 = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addon_version+'&av='+addon_version+'&an=ARABIC_VIDEOS&ea='+script_name+'&z='+randomNumber
		html = openURL_requests('GET',url2,'','',True,False,'IPTV-PLAY-1st')
		ADD_TO_LAST_VIDEO_FILES()
	else:
	"""
	PLAY_VIDEO(url,script_name,type)
	return

def ADD_USERAGENT():
	settings = xbmcaddon.Addon(id=addon_id)
	XBMCGUI_DIALOG_OK('رسالة من المبرمج','تحذير مهم وهام جدا . يرجى عدم تغييره إذا كنت لا تعرف ما هو .  وعدم تغييره إلا عند الضرورة القصوى . الحاجة لهذا التغيير هي فقط إذا طلبت منك شركة IPTV أن تعمل هذا التغيير . وفقط عندما تستخدم خدمة IPTV تحتاج User-Agent خاص')
	useragent = settings.getSetting('iptv.useragent')
	answer = XBMCGUI_DIALOG_YESNO(useragent,'هذا هو IPTV User-Agent المسجل في البرنامج . هل تريد تعديله أم تريد مسحه . للعلم عند المسح سوف يعود إلى الأصلي الذي يناسب جميع شركات IPTV ؟!','','','مسح القديم','تعديل القديم')
	if answer:
		useragent = KEYBOARD('أكتب IPTV User-Agent جديد',useragent)
		if useragent=='': return
	else: useragent = ''
	answer = XBMCGUI_DIALOG_YESNO(useragent,'هل تريد استخدام هذا IPTV User-Agent بدلا من  القديم ؟','','','كلا','نعم')
	if not answer:
		XBMCGUI_DIALOG_OK('رسالة من المبرمج','تم الإلغاء')
		return
	settings.setSetting('iptv.useragent',useragent)
	XBMCGUI_DIALOG_OK(useragent,'تم تغيير IPTV User-Agent إلى هذا الجديد')
	CREATE_STREAMS(True)
	return

def ADD_ACCOUNT():
	settings = xbmcaddon.Addon(id=addon_id)
	answer = XBMCGUI_DIALOG_YESNO('رسالة من المبرمج','البرنامج يحتاج اشتراك IPTV من نوع رابط التحميل m3u من أي شركة IPTV والأفضل أن يحتوي الرابط في نهايته على هذه الكلمات\n\r&type=m3u_plus\n\rهل تريد تغيير الرابط الآن ؟','','','كلا','نعم')
	if not answer: return
	iptvURL = settings.getSetting('iptv.url')
	if iptvURL!='':
		answer = XBMCGUI_DIALOG_YESNO(iptvURL,'هذا هو رابط IPTV المسجل في البرنامج ... هل تريد تعديله أم تريد كتابة رابط جديد ؟!','','','كتابة جديد','تعديل القديم')
		if not answer: iptvURL = ''
	iptvURL = KEYBOARD('اكتب رابط IPTV كاملا',iptvURL)
	if iptvURL=='': return
	else:
		answer = XBMCGUI_DIALOG_YESNO(iptvURL,'هل تريد استخدام هذا الرابط بدلا من الرابط القديم ؟','','','كلا','نعم')
		if not answer:
			XBMCGUI_DIALOG_OK('رسالة من المبرمج','تم الإلغاء')
			return
	settings.setSetting('iptv.url',iptvURL)
	settings.setSetting('iptv.timestamp','')
	settings.setSetting('iptv.timediff','')
	settings.setSetting('iptv.username','')
	settings.setSetting('iptv.password','')
	settings.setSetting('iptv.server','')
	XBMCGUI_DIALOG_OK(iptvURL,'تم تغير رابط اشتراك IPTV إلى هذا الرابط الجديد')
	CREATE_STREAMS(True)
	return

def SEARCH(search=''):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if showdialogs:
		#XBMCGUI_DIALOG_OK('','')
		if not isIPTVFiles(True): return
		if search=='': search = KEYBOARD()
		if search=='': return
		searchTitle = ['الكل','قنوات','أفلام','مسلسلات','أخرى']
		typeList = ['ALL','LIVE_GROUPED_SORTED','VOD_MOVIES_GROUPED_SORTED','VOD_SERIES_GROUPED_SORTED','VOD_UNKNOWN_GROUPED_SORTED']
		selection = XBMCGUI_DIALOG_SELECT('أختر البحث المناسب', searchTitle)
		if selection == -1: return
		TYPE = typeList[selection]
	else:
		if not isIPTVFiles(False): return
		TYPE = 'ALL'
	streams = READ_FROM_SQL3('IPTV_STREAMS',TYPE)
	searchLower = search.lower()
	uniqueLIST = []
	for dict in streams:
		title = dict['title']
		group = dict['group']
		img = dict['img']
		if '__IPTVSeries__' in group: maingroup,subgroup = group.split('__IPTVSeries__')
		else: maingroup,subgroup = group,''
		if subgroup!='': title2 = maingroup+' || '+subgroup
		else: title2 = maingroup
		if searchLower in group.lower():
			if searchLower in maingroup.lower() and maingroup not in uniqueLIST:
				uniqueLIST.append(maingroup)
				if searchLower in maingroup.lower(): addMenuItem('folder',menu_name+maingroup,TYPE,234,img,'',group)
			if searchLower in subgroup.lower() and subgroup not in uniqueLIST:
				uniqueLIST.append(subgroup)
				if searchLower in subgroup.lower(): addMenuItem('folder',menu_name+subgroup,TYPE,234,img,'',group)
		elif searchLower in title.lower():
			url = dict['url']
			title2 = title2+' || '+title
			if '!!__UNKNOWN__!!' in group: title2 = '!!__UNKNOWN__!!'
			videofiletype = re.findall('(\.avi|\.mp4|\.mkv|\.flv|\.mp3)(|\?.*?|/\?.*?|\|.*?)&&',url.lower()+'&&',re.DOTALL|re.IGNORECASE)
			if videofiletype:
				addMenuItem('video',menu_name+title,url,235,img)
			else: addMenuItem('live',menu_name+title,url,235,img)
	menuItemsLIST[:] = sorted(menuItemsLIST, reverse=False, key=lambda key: key[1])
	return

def CLEAN_NAME(title):
	title = title.replace('  ',' ').replace('  ',' ').replace('  ',' ')
	title = title.replace('||','|').replace('___',':').replace('--','-')
	title = title.replace('[[','[').replace(']]',']')
	title = title.replace('((','(').replace('))',')')
	title = title.replace('<<','<').replace('>>','>')
	#title = title.strip(' ').strip('|').strip('-').strip(':').strip('(').strip('[')
	return title

def SPLIT_NAME(title):
	if title=='!!__UNKNOWN__!!': return title
	lowest,lang = 9999,''
	first = title[0:2]
	separators = [' ',':','-','|',']',')','#','.',',','$',"'",'!','@','%','&','*','^']
	if   first[0]=='(': separators = [')']
	elif first[0]=='[': separators = [']']
	elif first[0]=='<': separators = ['>']
	for i in separators:
		position = title[2:].find(i)
		#position = title[1:].replace(' ','').find(i)
		if position>=0 and position<=lowest:
			lowest = position
			sep = i
	if lowest==9999: lang = '!!__UNKNOWN__!!'
	if lang=='': lang = first+title[2:].split(sep,1)[0]+sep.strip(' ')
	return lang

def CREATE_STREAMS(showDialogs=True):
	settings = xbmcaddon.Addon(id=addon_id)
	useragent = settings.getSetting('iptv.useragent')
	iptvURL = settings.getSetting('iptv.url')
	headers = {'User-Agent':useragent}
	ok = CHECK_ACCOUNT(False)
	if not ok:
		XBMCGUI_DIALOG_OK('رسالة من المبرمج','فشل بسحب ملفات IPTV . أحتمال رابط IPTV غير صحيح أو انت لم تستخدم سابقا خدمة IPTV الموجودة بالبرنامج . هذه الخدمة تحتاج اشتراك مدفوع وصحيح ويجب أن تضيفه بنفسك للبرنامج باستخدام قائمة IPTV الموجودة بهذا البرنامج')
		if iptvURL=='': LOG_THIS('ERROR',LOGGING(script_name)+'   No IPTV URL found to download IPTV files')
		else: LOG_THIS('ERROR',LOGGING(script_name)+'   Failed to download IPTV files')
		return
	#XBMCGUI_DIALOG_NOTIFICATION('IPTV','جلب ملفات جديدة')
	#BUSY_DIALOG('start')
	#LOG_THIS('NOTICE','EMAD 111')
	if showDialogs:
		yes = XBMCGUI_DIALOG_YESNO('رسالة من المبرمج','هل تريد أن تجلب الآن ملفات IPTV جديدة ؟','','','كلا','نعم')
		if not yes:
			#BUSY_DIALOG('stop')
			return
	pDialog = XBMCGUI_DIALOGPROGRESS()
	pDialog.create('جلب ملفات IPTV جديدة','جلب الملف الرئيسي (الملف قد يكون كبير وقد يحتاج بعض الوقت)')
	m3u_text = ''
	MegaByte = 1024*1024
	chunksize = 1*MegaByte
	import requests
	response = requests.get(iptvURL,headers=headers,stream=True)
	filesize = int(response.headers['Content-Length'])
	filesize_MB = int(1+filesize/MegaByte)
	chunksCount = int(filesize/chunksize)
	i = 0
	t1 = time.time()
	for chunk in response.iter_content(chunk_size=chunksize):
		i = i+1
		#if i==2: break
		if pDialog.iscanceled():
			response.close()
			return
		t2 = time.time()
		timeElapsed = t2-t1
		chunkTime = timeElapsed/i
		timeTotal = chunkTime*(chunksCount+1)
		timeRemaining = timeTotal-timeElapsed
		pDialog.update(0+int(35*i/chunksCount),'جلب الملف الرئيسي:- الجزء رقم',str(i*chunksize/MegaByte)+'/'+str(filesize_MB)+' MB    وقت متبقي: '+time.strftime("%H:%M:%S",time.gmtime(timeRemaining))+' ـ')
		m3u_text = m3u_text+chunk
	with open(fulliptvfile,'wb') as f: f.write(m3u_text)
	#m3u_filename = 'iptv_'+str(int(now))+'_.m3u'
	#iptvfile = os.path.join(addoncachefolder,m3u_filename)
	#return
	#XBMCGUI_DIALOG_OK(iptvURL,m3u_text)
	"""
	response.close()
	chunks_count = filesize/MegaByte
	def get_chunk(start):
		headers = {'Range':'bytes=%s-%s'%(start,start+MegaByte)}
		response = requests.get(iptvURL,headers=headers)
		chunk = response.content
		return chunk
	chunk = get_chunk(0)
	XBMCGUI_DIALOG_OK('',str(len(chunk)))
	mythread = CustomThread()
	for i in chunks_count:
		mythread.start_new_thread(i,get_chunk,i*MegaByte)
	count = 0
	while count<=chunks_count:
		time.sleep(1000)
		count = len(mythread.finishedLIST)
		if pDialog.iscanceled(): return
		pDialog.update(0+int(35*count/chunks_count),'جلب الملف الرئيسي:- الجزء رقم',str(count)+'/'+str(chunks_count)+' MB')
	#mythread.wait_finishing_all_threads()
	for id in chunks_count:
		chunk = mythread.resultsDICT[id]
		m3u_text = m3u_text+chunk
	"""
	if pDialog.iscanceled(): return
	pDialog.update(35,'جلب الملفات الثانوية:- الملف رقم','1/3')
	m3u_text = m3u_text.replace('"tvg-','" tvg-')
	m3u_text = m3u_text.replace('َ','').replace('ً','').replace('ُ','').replace('ٌ','')
	m3u_text = m3u_text.replace('ّ','').replace('ِ','').replace('ٍ','').replace('ْ','')
	m3u_text = m3u_text.replace('group-title=','group=')
	m3u_text = m3u_text.replace('tvg-','')
	#m3u_text = m3u_text.replace('group="AR | ISLAMIC"','group=""')
	username = settings.getSetting('iptv.username')
	password = settings.getSetting('iptv.password')
	server = settings.getSetting('iptv.server')
	live_archived_channels,live_epg_channels = [],[]
	url = server+'/player_api.php?username='+username+'&password='+password+'&action=get_series_categories'
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','IPTV-CREATE_STREAMS-2nd')
	if pDialog.iscanceled(): return
	pDialog.update(40,'جلب الملفات الثانوية:- الملف رقم','2/3')
	series_groups = re.findall('category_name":"(.*?)"',html,re.DOTALL)
	#XBMCGUI_DIALOG_OK('','')
	for group in series_groups:
		group = group.replace('\/','/').decode('unicode_escape').encode('utf8')
		m3u_text = m3u_text.replace('group="'+group+'"','group="__IPTVSeries__'+group+'"')
	url = server+'/player_api.php?username='+username+'&password='+password+'&action=get_vod_categories'
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','IPTV-CREATE_STREAMS-3rd')
	pDialog.update(45,'جلب الملفات الثانوية:- الملف رقم','3/3')
	vod_groups = re.findall('category_name":"(.*?)"',html,re.DOTALL)
	for group in vod_groups:
		group = group.replace('\/','/').decode('unicode_escape').encode('utf8')
		m3u_text = m3u_text.replace('group="'+group+'"','group="__MOVIES__'+group+'"')
	url = server+'/player_api.php?username='+username+'&password='+password+'&action=get_live_streams'
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','IPTV-CREATE_STREAMS-4th')
	live_archived = re.findall('"name":"(.*?)".*?"tv_archive":(.*?),',html,re.DOTALL)
	for name,archived in live_archived:
		if archived=='1': live_archived_channels.append(name)
	live_epg = re.findall('"name":"(.*?)".*?"epg_channel_id":(.*?),',html,re.DOTALL)
	for name,epg in live_epg:
		if epg!='null': live_epg_channels.append(name)
	lines = re.findall('INF(.*?)#EXT',m3u_text+'#EXT',re.DOTALL)
	streams_not_sorted = []
	length = len(lines)
	i = 0
	for line in lines:
		group,title,type = '','',''
		dict = {}
		i = i+1
		if pDialog.iscanceled(): return
		pDialog.update(50+int(25*i/length),'قراءة الملفات الجديدة:- الفيديو رقم',str(i)+'/'+str(length))
		line = line.replace('\r','').replace('\n','')
		if 'http' not in line: continue
		line,url = line.rsplit('http',1)
		url = 'http'+url
		try:
			line,title = line.rsplit('",',1)
			line = line+'"'
		except:
			#XBMCGUI_DIALOG_OK('FAILED','FAILED')
			try: line,title = line.rsplit('1,',1)
			except: title = ''
		dict['url'] = url
		params = re.findall(' (.*?)="(.*?)"',line,re.DOTALL)
		for key,value in params:
			key = key.replace('"','').strip(' ')
			dict[key] = value.strip(' ')
		dict['org_title'] = title
		if title=='':
			if 'name' in dict.keys() and dict['name']!='': title = dict['name']
			else: title = '!!__UNKNOWN__!!'
		dict['title'] = title.strip(' ').replace('  ',' ').replace('  ',' ')
		if 'logo' in dict.keys():
			dict['img'] = dict['logo']
			del dict['logo']
		else: dict['img'] = ''
		if 'group' in dict.keys() and dict['group']!='': group = dict['group']
		else: group = '!!__UNKNOWN__!!'
		dict['org_group'] = group
		videofiletype = re.findall('(\.avi|\.mp4|\.mkv|\.flv|\.mp3)(|\?.*?|/\?.*?|\|.*?)&&',url.lower()+'&&',re.DOTALL|re.IGNORECASE)
		if videofiletype or '__IPTVSeries__' in group or '__MOVIES__' in group:
			type = 'VOD'
			if '__IPTVSeries__' in group: type = type+'_SERIES'
			elif '__MOVIES__' in group: type = type+'_MOVIES'
			else: type = type+'_UNKNOWN'
			group = group.replace('__IPTVSeries__','').replace('__MOVIES__','')
		else:
			type = 'LIVE'
			if group=='': type = type+'_UNKNOWN'
			if title in live_epg_channels: type = type+'_EPG'
			if title in live_archived_channels: type = type+'_ARCHIVED'
		#LOG_THIS('NOTICE','EMAD 2222  .  '+str(i*2)+'  .  '+group)
		dict['type'] = type
		group = group.strip(' ').replace('  ',' ').replace('  ',' ').upper()
		if type=='LIVE_UNKNOWN': group = '!!__UNKNOWN__!!'
		elif type=='VOD_UNKNOWN': group = '!!__UNKNOWN__!!'
		elif type=='VOD_SERIES':
			series_title = re.findall('(.*?) [Ss]\d+ +[Ee]\d+',dict['title'],re.DOTALL)
			if series_title: group = group+'__IPTVSeries__'+series_title[0]
			else: group = group+'__IPTVSeries__'+'!!__UNKNOWN__!!'
		dict['group'] = group
		if 'id' in dict.keys(): del dict['id']
		if 'ID' in dict.keys(): del dict['ID']
		if 'name' in dict.keys(): del dict['name']
		title = dict['title']
		if '\u' in title.lower(): title = title.decode('unicode_escape')
		title = CLEAN_NAME(title)
		try: country = SPLIT_NAME(title)
		except: country = '!!__UNKNOWN__!!'
		try: language = SPLIT_NAME(group)
		except: language = '!!__UNKNOWN__!!'
		dict['title'] = title.upper()
		dict['country'] = country.upper()
		dict['language'] = language.upper()
		#if 'AL - ' in dict['title']: dict['title'] = dict['title'].replace('AL - ','AL ')
		#if 'EL - ' in dict['title']: dict['title'] = dict['title'].replace('EL - ','EL ')
		streams_not_sorted.append(dict)
	if pDialog.iscanceled(): return
	pDialog.update(75,'تصنيف الملفات الغير مرتبة',' ')
	#LOG_THIS('NOTICE','EMAD 444')
	#with open('S:\\0iptvemad.m3u','w') as f: f.write(str(streams_not_sorted).replace("},","}\n,"))
	streams_sorted = sorted(streams_not_sorted, reverse=False, key=lambda key: key['title'].lower())
	grouped_streams = {}
	types = ['ALL','DUMMY','VOD_UNKNOWN_GROUPED','LIVE_UNKNOWN_SORTED','LIVE_UNKNOWN','VOD_UNKNOWN_GROUPED_SORTED',
			'LIVE_ARCHIVED_GROUPED_SORTED','LIVE_EPG_GROUPED_SORTED','LIVE_TIMESHIFT_GROUPED_SORTED',
			'LIVE_ORIGINAL_GROUPED','LIVE_FROM_NAME_SORTED','LIVE_GROUPED_SORTED','LIVE_GROUPED','LIVE_FROM_GROUP_SORTED',
			'VOD_MOVIES_GROUPED_SORTED','VOD_MOVIES_GROUPED','VOD_SERIES_GROUPED','VOD_SERIES_GROUPED_SORTED',
			'VOD_ORIGINAL_GROUPED','VOD_FROM_NAME_SORTED','VOD_FROM_GROUP_SORTED']
	for type in types: grouped_streams[type] = []
	#LOG_THIS('NOTICE','EMAD 555 CREATE STREAMS START creating 1st STREAMS dictionary')
	for dict in streams_sorted:
		type = dict['type']
		dict2 = {'group':dict['group'],'title':dict['title'],'url':dict['url'],'img':dict['img']}
		dict3 = {'group':dict['country'],'title':dict['title'],'url':dict['url'],'img':dict['img']}
		dict4 = {'group':dict['language'],'title':dict['title'],'url':dict['url'],'img':dict['img']}
		grouped_streams['ALL'].append(dict)
		#grouped_streams[type].append(dict2)
		if 'LIVE' in type:
			if 'EPG'		in type: grouped_streams['LIVE_EPG_GROUPED_SORTED'].append(dict2)
			if 'ARCHIVED'	in type: grouped_streams['LIVE_ARCHIVED_GROUPED_SORTED'].append(dict2)
			if 'UNKNOWN'	in type: grouped_streams['LIVE_UNKNOWN_SORTED'].append(dict2)
			grouped_streams['LIVE_GROUPED_SORTED'].append(dict2)
			grouped_streams['LIVE_FROM_NAME_SORTED'].append(dict3)
			grouped_streams['LIVE_FROM_GROUP_SORTED'].append(dict4)
		elif 'VOD' in type:
			if 'MOVIES'		in type: grouped_streams['VOD_MOVIES_GROUPED_SORTED'].append(dict2)
			if 'SERIES'		in type: grouped_streams['VOD_SERIES_GROUPED_SORTED'].append(dict2)
			if 'UNKNOWN'	in type: grouped_streams['VOD_UNKNOWN_GROUPED_SORTED'].append(dict2)
			grouped_streams['VOD_FROM_NAME_SORTED'].append(dict3)
			grouped_streams['VOD_FROM_GROUP_SORTED'].append(dict4)
	if pDialog.iscanceled(): return
	pDialog.update(80,'تصنيف الملفات المرتبة')
	grouped_streams['LIVE_TIMESHIFT_GROUPED_SORTED'] = grouped_streams['LIVE_ARCHIVED_GROUPED_SORTED']
	for dict in streams_not_sorted:
		type = dict['type']
		dict2 = {'group':dict['group'],'title':dict['title'],'url':dict['url'],'img':dict['img']}
		#if 'EG - ' in dict['title']: LOG_THIS('NOTICE','___:'+type+'___:  ___:'+str(dict2))
		if 'LIVE' in type:
			grouped_streams['LIVE_GROUPED'].append(dict2)
			grouped_streams['LIVE_ORIGINAL_GROUPED'].append(dict2)
			if 'UNKNOWN' in type: grouped_streams['LIVE_UNKNOWN'].append(dict2)
		elif 'VOD' in type:
			grouped_streams['VOD_ORIGINAL_GROUPED'].append(dict2)
			if 'MOVIES' in type: grouped_streams['VOD_MOVIES_GROUPED'].append(dict2)
			if 'SERIES' in type: grouped_streams['VOD_SERIES_GROUPED'].append(dict2)
			if 'UNKNOWN' in type: grouped_streams['VOD_UNKNOWN_GROUPED'].append(dict2)
	grouped_streams['DUMMY'].append('')
	DELETE_IPTV_FILES(False)
	length = len(types)
	i = 0
	t1 = time.time()
	chunksCount = len(types)
	for TYPE in types:
		i = i+1
		if pDialog.iscanceled(): return
		t2 = time.time()
		timeElapsed = t2-t1
		chunkTime = timeElapsed/i
		timeTotal = chunkTime*(chunksCount+1)
		timeRemaining = timeTotal-timeElapsed
		pDialog.update(85+int(15*i/length),'تخزين الملفات:- الملف رقم','وقت متبقي: '+time.strftime("%H:%M:%S",time.gmtime(timeRemaining))+'      '+str(i)+'/'+str(length))
		WRITE_TO_SQL3('IPTV_STREAMS',TYPE,grouped_streams[TYPE],PERMANENT_CACHE)
	#streams = READ_FROM_SQL3('IPTV_STREAMS','LIVE_GROUPED')
	#for dict in streams:
	#	if 'EG - ' in dict['title']: LOG_THIS('NOTICE','======'+str(dict))
	with open(dummyiptvfile,'w') as f: f.write('')
	pDialog.close()
	#BUSY_DIALOG('stop')
	countsMessage = COUNTS(False)
	XBMCGUI_DIALOG_OK('تم جلب ملفات IPTV جديدة',countsMessage)
	return

def COUNTS(show=True):
	#XBMCGUI_DIALOG_OK('COUNTS','0000')
	if not isIPTVFiles(show): return ''
	BUSY_DIALOG('start')
	unknownLIVECount = len(READ_FROM_SQL3('IPTV_STREAMS','LIVE_UNKNOWN'))
	knownLIVECount = len(READ_FROM_SQL3('IPTV_STREAMS','LIVE_GROUPED'))
	liveCount = unknownLIVECount+knownLIVECount
	moviesCount = len(READ_FROM_SQL3('IPTV_STREAMS','VOD_MOVIES_GROUPED'))
	unknownVODCount = len(READ_FROM_SQL3('IPTV_STREAMS','VOD_UNKNOWN_GROUPED'))
	episodes = READ_FROM_SQL3('IPTV_STREAMS','VOD_SERIES_GROUPED')
	episodesCount = len(episodes)
	uniqeSeriesLIST = []
	for dict in episodes:
		group = dict['group']
		if '__IPTVSeries__' in group:
			seriesName = group.split('__IPTVSeries__')[1]
			if seriesName not in uniqeSeriesLIST: uniqeSeriesLIST.append(seriesName)
	seriesCount = len(uniqeSeriesLIST)
	total = liveCount+moviesCount+episodesCount+unknownVODCount
	countsMessage = 'قنوات: '+str(liveCount)+'     أفلام: '+str(moviesCount)+'\r\n     مسلسلات: '+str(seriesCount)+'     حلقات: '+str(episodesCount)+'\r\n     فيدوهات مجهولة: '+str(unknownVODCount)+'     المجموع: '+str(total)
	if show: XBMCGUI_DIALOG_OK('رسالة من المبرمج',countsMessage)
	BUSY_DIALOG('stop')	
	logMssage = countsMessage.replace('     ','  .  ').replace('\r\n','')
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Counts of IPTV videos   '+logMssage)
	return countsMessage

def DELETE_IPTV_FILES(show=True):
	if show:
		yes = XBMCGUI_DIALOG_YESNO('مسح ملفات IPTV','تستطيع في أي وقت الدخول إلى قائمة IPTV وجلب ملفات IPTV جديدة .. هل تريد الآن مسح الملفات القديمة المخزنة في البرنامج ؟!','','','كلا','نعم')
		if not yes: return
	else: yes = False
	if isIPTVFiles(False):
		os.remove(dummyiptvfile)
		if show: os.remove(fulliptvfile)
	DELETE_FROM_SQL3('IPTV_ITEMS')
	DELETE_FROM_SQL3('IPTV_GROUPS')
	DELETE_FROM_SQL3('IPTV_STREAMS')
	#DELETE_FROM_SQL3('IMPORT_SECTIONS','LIVE')
	#CLEAN_KODI_CACHE_FOLDER()
	if show: XBMCGUI_DIALOG_OK('رسالة من المبرمج','تم مسح جميع ملفات IPTV')
	return yes

def isIPTVFiles(showDialogs=True):
	list = str(os.listdir(addoncachefolder))
	filename = dummyiptvfile.split('/')[-1].split('\\')[-1]
	if filename in list: return True
	#streams = READ_FROM_SQL3('IPTV_STREAMS','DUMMY')
	#if streams: return True
	if showDialogs: XBMCGUI_DIALOG_OK('رسالة من المبرمج','انت بحاجة إلى الذهاب إلى قائمة IPTV ثم . أولا اضغط على "إضافة اشتراك IPTV المدفوع" (من أي شركة IPTV) . ثم ثانيا اضغط على جلب ملفات IPTV')
	return False

"""
def SAVE_STREAMS_TO_DISK(grouped_streams,types):
	global settings
	filesLIST = []
	filesLIST.append('iptv_'+str(int(now))+'_.m3u')
	filename = 'iptv_'+str(int(now))+'__TYPE__.streams'
	settings.setSetting('iptv.file',filename)
	for TYPE in types:
		new_streams = str(grouped_streams[TYPE])
		new_streams = new_streams.replace('},','},\n')
		new_filename = filename.replace('__TYPE__','_'+TYPE+'_')
		iptvFile = os.path.join(addoncachefolder,new_filename)
		file = open(iptvFile, 'wb')
		file.write(new_streams)
		file.close()
		filesLIST.append(new_filename)
	XBMCGUI_DIALOG_OK('IPTV','تم جلب ملفات IPTV جديدة')
	return

def GET_STREAMS_FROM_DISK(TYPE):
	global settings
	filename = settings.getSetting('iptv.file')
	filename = filename.replace('__TYPE__','_'+TYPE+'_')
	iptvFile = os.path.join(addoncachefolder,filename)
	f = open(iptvFile,'rb')
	streams_text = f.read()
	streams = EVAL(streams_text)
	return streams
"""



