# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='IPTV'
menu_name='_IPT_'

settings = xbmcaddon.Addon(id=addon_id)
useragent = settings.getSetting('iptv.useragent')
headers = {'User-Agent':useragent}

def MAIN(mode,url,text,type):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	#LOG_THIS('NOTICE','start')
	if   mode==230: results = MENU()
	elif mode==231: results = ADD_ACCOUNT()
	elif mode==232: results = CREATE_STREAMS()
	elif mode==233: results = GROUPS(url,text)
	elif mode==234: results = ITEMS(url,text)
	elif mode==235: results = PLAY(url,type)
	elif mode==236: results = PLAY(url,type)
	elif mode==237: results = DELETE_IPTV_FILES(True)
	elif mode==238: results = EPG_ITEMS(url,text)
	elif mode==239: results = SEARCH(text)
	elif mode==280: results = ADD_USERAGENT()
	else: results = False
	#LOG_THIS('NOTICE','end')
	return results

def MENU():
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'بحث في ملفات IPTV','',239)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'برامج القنوات (جدول فقط)','LIVE_EPG_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'أرشيف القنوات للأيام الماضية','LIVE_TIMESHIFT_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'أرشيف برامج القنوات للأيام الماضية','LIVE_ARCHIVED_GROUPED_SORTED',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة','LIVE_GROUPED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'أفلام مصنفة','VOD_MOVIES_GROUPED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'مسلسلات مصنفة','VOD_SERIES_GROUPED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مجهولة','VOD_UNKNOWN_GROUPED',233)
	#addMenuItem('folder',menu_name+'قنوات مجهولة','LIVE_UNKNOWN',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة ومرتبة','LIVE_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'أفلام مصنفة ومرتبة','VOD_MOVIES_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'مسلسلات مصنفة ومرتبة','VOD_SERIES_GROUPED_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مجهولة ومرتبة','VOD_UNKNOWN_GROUPED_SORTED',233)
	#addMenuItem('folder',menu_name+'قنوات مجهولة','LIVE_UNKNOWN_SORTED',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'القنوات الأصلية بدون تغيير','LIVE_ORIGINAL',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'الفيديوهات الأصلية بدون تغيير','VOD_ORIGINAL',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة من أسمائها ومرتبة','LIVE_FROM_NAME_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مصنفة من أسمائها ومرتبة','VOD_FROM_NAME_SORTED',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة من أقسامها ومرتبة','LIVE_FROM_GROUP_SORTED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مصنفة من أقسامها ومرتبة','VOD_FROM_GROUP_SORTED',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'إضافة اشتراك IPTV','',231)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'جلب ملفات IPTV','',232)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'مسح ملفات IPTV','',237)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'تغيير IPTV User-Agent','',280)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return

def GROUPS(TYPE,GROUP,website=''):
	if website=='': show = True
	else: show = False
	if not isIPTVFiles(show): return
	results = READ_FROM_SQL3('IPTV_GROUPS',[TYPE,GROUP,website])
	if results: menuItemsLIST[:] = menuItemsLIST+results ; return
	else: previous_menuItemsLIST = menuItemsLIST[:] ; menuItemsLIST[:] = []
	#xbmcgui.Dialog().ok(TYPE,'')
	streams = READ_FROM_SQL3('IPTV_STREAMS',TYPE)
	groups,unique,logos = [],[],[]
	for dict in streams:
		groups.append(dict['group'])
		logos.append(dict['img'])
	if website!='':
		website2 = website.split('::')[0]
		website2 = website2.replace('_RANDOM','').replace('_LIVE','')
		menu_name2 = ',[COLOR FFC89008]'+website2+':[/COLOR] '
	else: menu_name2 = menu_name
	z = zip(groups,logos)
	z = sorted(z, reverse=False, key=lambda key: key[0])
	if '____' in GROUP: MAINGROUP,SUBGROUP = GROUP.split('____')
	else: MAINGROUP,SUBGROUP = GROUP,''
	if len(z)>0:
		for group,img in z:
			if '____' in group: maingroup,subgroup = group.split('____')
			else: maingroup,subgroup = group,''
			#if GROUP=='' and TYPE!='VOD_ORIGINAL': img = ''
			#if maingroup=='!!__UNKNOWN__!!': img = ''
			if GROUP=='':
				if maingroup in unique: continue
				unique.append(maingroup)
				if 'RANDOM' in website: addMenuItem('folder',menu_name2+maingroup,TYPE,167,img,'',group)
				elif 'SERIES' in TYPE: addMenuItem('folder',menu_name2+maingroup,TYPE,233,'','',group)
				else: addMenuItem('folder',menu_name2+maingroup,TYPE,234,'','',group)
			elif 'SERIES' in TYPE and maingroup==MAINGROUP:
				if subgroup in unique: continue
				unique.append(subgroup)
				if 'RANDOM' in website: addMenuItem('folder',menu_name2+subgroup,TYPE,167,img,'',group)
				else: addMenuItem('folder',menu_name2+subgroup,TYPE,234,img,'',group)
	else:
		addMenuItem('link',menu_name2+'هذه الخدمة غير موجودة في اشتراكك','',9999)
		addMenuItem('link',menu_name2+'أو رابط IPTV الذي أنت أضفته غير صحيح','',9999)
	WRITE_TO_SQL3('IPTV_GROUPS',[TYPE,GROUP,website],menuItemsLIST,VERY_LONG_CACHE)
	menuItemsLIST[:] = previous_menuItemsLIST+menuItemsLIST
	return

def ITEMS(TYPE,GROUP):
	if not isIPTVFiles(True): return
	#xbmcgui.Dialog().ok(TYPE,GROUP)
	#LOG_THIS('NOTICE','before DATABASE')
	results = READ_FROM_SQL3('IPTV_ITEMS',[TYPE,GROUP])
	if results: menuItemsLIST[:] = menuItemsLIST+results ; return
	else: previous_menuItemsLIST = menuItemsLIST[:] ; menuItemsLIST[:] = []
	streams = READ_FROM_SQL3('IPTV_STREAMS',TYPE)
	if '____' in GROUP: MAINGROUP,SUBGROUP = GROUP.split('____')
	else: MAINGROUP,SUBGROUP = GROUP,''
	#xbmcgui.Dialog().ok(MAINGROUP,SUBGROUP)
	for dict in streams:
		group = dict['group']
		if '____' in group: maingroup,subgroup = group.split('____')
		else: maingroup,subgroup = group,''
		cond1 = ('GROUPED' in TYPE or TYPE=='ALL') and group==GROUP
		cond2 = ('GROUPED' not in TYPE and TYPE!='ALL') and maingroup==MAINGROUP
		if cond1 or cond2:
			title = dict['title']
			url = dict['url']
			img = dict['img']
			if   'ARCHIVED' in TYPE: addMenuItem('folder',menu_name+' '+title,url,238,img,'','archive')
			elif 'EPG' in TYPE: addMenuItem('folder',menu_name+' '+title,url,238,img,'','full_epg')
			elif 'TIMESHIFT' in TYPE: addMenuItem('folder',menu_name+' '+title,url,238,img,'','timeshift')
			elif 'LIVE' in TYPE: addMenuItem('live',menu_name+' '+title,url,235,img)
			else: addMenuItem('video',menu_name+' '+title,url,235,img)
	#xbmcgui.Dialog().ok('OUT',str(menuItemsLIST))
	WRITE_TO_SQL3('IPTV_ITEMS',[TYPE,GROUP],menuItemsLIST,VERY_LONG_CACHE)
	menuItemsLIST[:] = previous_menuItemsLIST+menuItemsLIST
	return

def EPG_ITEMS(url,function):
	if not isIPTVFiles(True): return
	url_parts = url.split('/')
	stream_id = url_parts[-1].replace('.ts','').replace('.m3u8','')
	server = url_parts[0]+'//'+url_parts[2]
	username = url_parts[3]
	password = url_parts[4]
	settings = xbmcaddon.Addon(id=addon_id)
	if function in ['timeshift']:
		timestamp = settings.getSetting('iptv.timestamp')
		if timestamp=='' or now-int(timestamp)>24*HOUR:
			info_url = server+'/player_api.php?username='+username+'&password='+password
			html = openURL_cached(NO_CACHE,info_url,'',headers,'','IPTV-EPG_ITEMS-1st')
			#LOG_THIS('NOTICE',html)
			iptv_info = EVAL(html)
			time_now = iptv_info['server_info']['time_now']
			struct = time.strptime(time_now,'%Y-%m-%d %H:%M:%S')
			timestamp = int(time.mktime(struct))
			timediff = int(now-timestamp)
			# normalizing to the closest half hour with 15 minutes error range
			timediff = int((timediff+900)/1800)*1800
			settings.setSetting('iptv.timestamp',str(now))
			settings.setSetting('iptv.timediff',str(timediff))
		else: timediff = int(settings.getSetting('iptv.timediff'))
	#xbmcgui.Dialog().ok(str(timediff),str(timestamp))
	if function=='short_epg': url_action = 'get_short_epg'
	else: url_action = 'get_simple_data_table'
	epg_url = server+'/player_api.php?username='+username+'&password='+password+'&action='+url_action+'&stream_id='+stream_id
	html = openURL_cached(NO_CACHE,epg_url,'',headers,'','IPTV-EPG_ITEMS-2nd')
	archive_files = EVAL(html)
	#xbmcgui.Dialog().ok('',str(archive_files))
	#with open('S:\\00iptv.txt','w') as f: f.write(html)
	all_epg = archive_files['epg_listings']
	epg_items = []
	if function in ['archive','timeshift']:
		addMenuItem('link',menu_name+'الملفات الأولي بالقائمة قد لا تعمل','',9999)
		for dict in all_epg:
			if dict['has_archive']==1:
				epg_items.append(dict)
				if function in ['timeshift']: break
		if not epg_items: return
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
	if function=='short_epg': selection = xbmcgui.Dialog().contextmenu(epg_list)
	return epg_list

def PLAY(url,type):
	if headers['User-Agent']!='': url = url+'|User-Agent='+headers['User-Agent']
	PLAY_VIDEO(url,script_name,type)
	return

def ADD_USERAGENT():
	settings = xbmcaddon.Addon(id=addon_id)
	xbmcgui.Dialog().ok('رسالة من المبرمج','تحذير مهم وهام جدا . يرجى عدم تغييره إذا كنت لا تعرف ما هو .  وعدم تغييره إلا عند الضرورة القصوى . الحاجة لهذا التغيير هي فقط إذا طلبت منك شركة IPTV أن تعمل هذا التغيير . وفقط عندما تستخدم خدمة IPTV تحتاج User-Agent خاص')
	useragent = settings.getSetting('iptv.useragent')
	answer = xbmcgui.Dialog().yesno(useragent,'هذا هو IPTV User-Agent المسجل في البرنامج . هل تريد تعديله أم تريد مسحه . للعلم عند المسح سوف يعود إلى الأصلي الذي يناسب جميع شركات IPTV ؟!','','','مسح القديم','تعديل القديم')
	if answer:
		useragent = KEYBOARD('أكتب IPTV User-Agent جديد',useragent)
		if useragent=='': return
	else: useragent = ''
	answer = xbmcgui.Dialog().yesno(useragent,'هل تريد استخدام هذا IPTV User-Agent بدلا من  القديم ؟','','','كلا','نعم')
	if not answer:
		xbmcgui.Dialog().ok('رسالة من المبرمج','تم الإلغاء')
		return
	settings.setSetting('iptv.useragent',useragent)
	xbmcgui.Dialog().ok(useragent,'تم تغيير IPTV User-Agent إلى هذا الجديد')
	CREATE_STREAMS()
	return

def ADD_ACCOUNT():
	settings = xbmcaddon.Addon(id=addon_id)
	answer = xbmcgui.Dialog().yesno('رسالة من المبرمج','البرنامج يحتاج اشتراك IPTV من نوع رابط التحميل m3u من أي شركة IPTV والأفضل أن يحتوي الرابط في نهايته على هذه الكلمات\n\r&type=m3u_plus\n\rهل تريد تغيير الرابط الآن ؟','','','كلا','نعم')
	if not answer: return
	iptvURL = settings.getSetting('iptv.url')
	if iptvURL!='':
		answer = xbmcgui.Dialog().yesno(iptvURL,'هذا هو رابط IPTV المسجل في البرنامج ... هل تريد تعديله أم تريد كتابة رابط جديد ؟!','','','كتابة جديد','تعديل القديم')
		if not answer: iptvURL = ''
	iptvURL = KEYBOARD('اكتب رابط IPTV كاملا',iptvURL)
	if iptvURL=='': return
	else:
		answer = xbmcgui.Dialog().yesno(iptvURL,'هل تريد استخدام هذا الرابط بدلا من الرابط القديم ؟','','','كلا','نعم')
		if not answer:
			xbmcgui.Dialog().ok('رسالة من المبرمج','تم الإلغاء')
			return
	settings.setSetting('iptv.url',iptvURL)
	xbmcgui.Dialog().ok(iptvURL,'تم تغير رابط اشتراك IPTV إلى هذا الرابط الجديد')
	CREATE_STREAMS()
	return

def SEARCH(search=''):
	if '::' in search:
		if not isIPTVFiles(False): return
		search = search.split('::')[0]
		exit = False
		TYPE = 'VOD_FROM_NAME_SORTED'
	else:
		if not isIPTVFiles(True): return
		if search=='': search = KEYBOARD()
		if search == '': return
		exit = True
		searchTitle = ['الكل','قنوات','أفلام','مسلسلات','أخرى']
		typeList = ['ALL','LIVE_GROUPED_SORTED','VOD_MOVIES_GROUPED_SORTED','VOD_SERIES_GROUPED_SORTED','VOD_UNKNOWN_GROUPED_SORTED']
		selection = xbmcgui.Dialog().select('أختر البحث المناسب', searchTitle)
		if selection == -1: return
		TYPE = typeList[selection]
	streams = READ_FROM_SQL3('IPTV_STREAMS',TYPE)
	searchLower = search.lower()
	uniqueLIST = []
	for dict in streams:
		title = dict['title']
		group = dict['group']
		img = dict['img']
		if '____' in group: maingroup,subgroup = group.split('____')
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
			if '.mp4' in url or '.mkv' in url or '.avi' in url or '.mp3' in url:
				addMenuItem('video',menu_name+title,url,235,img)
			else: addMenuItem('live',menu_name+title,url,235,img)
	menuItemsLIST[:] = sorted(menuItemsLIST, reverse=False, key=lambda key: key[1])
	return

def CLEAN_NAME(title):
	title = title.replace('  ',' ').replace('  ',' ').replace('  ',' ')
	title = title.replace('||','|').replace('::',':').replace('--','-')
	title = title.replace('[[','[').replace(']]',']')
	title = title.replace('((','(').replace('))',')')
	title = title.replace('<<','<').replace('>>','>')
	#title = title.strip(' ').strip('|').strip('-').strip(':').strip('(').strip('[')
	return title

def SPLIT_NAME(title):
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

def CREATE_STREAMS(ask_dialog=True):
	xbmcgui.Dialog().notification('IPTV','جلب ملفات جديدة')
	BUSY_DIALOG('start')
	#LOG_THIS('NOTICE','EMAD 111')
	if ask_dialog:
		answer = xbmcgui.Dialog().yesno('رسالة من المبرمج','هل تريد أن تجلب الآن ملفات IPTV جديدة ؟','','','كلا','نعم')
		if not answer:
			BUSY_DIALOG('stop')
			return
	settings = xbmcaddon.Addon(id=addon_id)
	iptvURL = settings.getSetting('iptv.url')
	try:
		if iptvURL=='': a = error
		m3u_text = openURL_cached(SHORT_CACHE,iptvURL,'',headers,'','IPTV-CREATE_STREAMS-1st')
		#m3u_filename = 'iptv_'+str(int(now))+'_.m3u'
		#iptvfile = os.path.join(addoncachefolder,m3u_filename)
		#with open(iptvfile,'w') as f: f.write(m3u_text)
		#xbmcgui.Dialog().ok(iptvURL,m3u_text)
	except:
		xbmcgui.Dialog().ok('رسالة من المبرمج','فشل بسحب ملفات IPTV . أحتمال رابط IPTV غير صحيح أو انت لم تستخدم سابقا خدمة IPTV الموجودة بالبرنامج . هذه الخدمة تحتاج اشتراك مدفوع وصحيح ويجب أن تضيفه بنفسك للبرنامج باستخدام قائمة IPTV الموجودة بهذا البرنامج')
		if iptvURL=='': LOG_THIS('ERROR',LOGGING(script_name)+'   No IPTV url found to download IPTV files')
		else: LOG_THIS('ERROR',LOGGING(script_name)+'   Failed to download IPTV files')
		BUSY_DIALOG('stop')
		return
	m3u_text = m3u_text.replace('"tvg-','" tvg-')
	m3u_text = m3u_text.replace('َ','').replace('ً','').replace('ُ','').replace('ٌ','')
	m3u_text = m3u_text.replace('ّ','').replace('ِ','').replace('ٍ','').replace('ْ','')
	m3u_text = m3u_text.replace('group-title=','group=')
	m3u_text = m3u_text.replace('tvg-','')
	username = re.findall('username=(.*?)&',iptvURL+'&',re.DOTALL)
	password = re.findall('password=(.*?)&',iptvURL+'&',re.DOTALL)
	live_archived_channels,live_epg_channels = [],[]
	if username and password:
		username = username[0]
		password = password[0]
		url_parts = iptvURL.split('/')
		server = url_parts[0]+'//'+url_parts[2]
		url = server+'/player_api.php?username='+username+'&password='+password+'&action=get_series_categories'
		html = openURL_cached(SHORT_CACHE,url,'',headers,'','IPTV-CREATE_STREAMS-2nd')
		series_groups = re.findall('category_name":"(.*?)"',html,re.DOTALL)
		#xbmcgui.Dialog().ok('','')
		for group in series_groups:
			group = group.replace('\/','/').decode('unicode_escape').encode('utf8')
			m3u_text = m3u_text.replace('group="'+group+'"','group="__SERIES__'+group+'"')
		url = server+'/player_api.php?username='+username+'&password='+password+'&action=get_vod_categories'
		html = openURL_cached(SHORT_CACHE,url,'',headers,'','IPTV-CREATE_STREAMS-3rd')
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
	#LOG_THIS('NOTICE','EMAD 222')
	lines = re.findall('#EXTINF(.*?)[\n\r]+(.*?)[\n\r]+',m3u_text+'\n',re.DOTALL)
	#LOG_THIS('NOTICE','EMAD 333')
	streams_not_sorted = []
	for line,url in lines:
		dict = {}
		dict['url'] = url
		if '",' in line:
			line,title = line.rsplit('",',1)
			line = line+'"'
		else: line,title = line.rsplit('1,',1)
		params = re.findall(' (.*?)="(.*?)"',line,re.DOTALL)
		for key,value in params:
			key = key.replace('"','').strip(' ')
			dict[key] = value.strip(' ')
		dict['org_title'] = title
		if title=='':
			if 'name' in dict.keys(): title = dict['name']
			else: title = '!!__UNKNOWN__!!'
		dict['title'] = title.strip(' ').replace('  ',' ').replace('  ',' ')
		if 'logo' in dict.keys():
			dict['img'] = dict['logo']
			del dict['logo']
		else: dict['img'] = ''
		group = ''
		if 'group' in dict.keys(): group = dict['group']
		if group=='': group = '!!__UNKNOWN__!!'
		dict['org_group'] = group
		if '.mp4' in url or '.mkv' in url or '.avi' in url or '.mp3' in url or '__SERIES__' in group or '__MOVIES__' in group:
			type = 'VOD'
			if '__SERIES__' in group: type = type+'_SERIES'
			elif '__MOVIES__' in group: type = type+'_MOVIES'
			else: type = type+'_UNKNOWN'
			group = group.replace('__SERIES__','').replace('__MOVIES__','')
		else:
			type = 'LIVE'
			if group=='': type = type+'_UNKNOWN'
			if title in live_epg_channels: type = type+'_EPG'
			if title in live_archived_channels: type = type+'_ARCHIVED'
		dict['type'] = type
		group = group.strip(' ').replace('  ',' ').replace('  ',' ').upper()
		#if group=='': group = type
		if type in ['LIVE','LIVE_UNKNOWN','VOD_MOVIES']: group = group+'____'
		elif type=='VOD_UNKNOWN': group = '!!__UNKNOWN__!!'+'____'
		elif type=='VOD_SERIES':
			series_title = re.findall('(.*?) [Ss]\d+ +[Ee]\d+',dict['title'],re.DOTALL)
			if series_title: group = group+'____'+series_title[0]
			else: group = group+'____'+'!!__UNKNOWN__!!'
		dict['group'] = group
		if 'id' in dict.keys(): del dict['id']
		if 'ID' in dict.keys(): del dict['ID']
		if 'name' in dict.keys(): del dict['name']
		title = dict['title']
		if '\u' in title.lower(): title = title.decode('unicode_escape')
		title = CLEAN_NAME(title)
		country = SPLIT_NAME(title)
		language = SPLIT_NAME(group)
		dict['title'] = title.upper()
		dict['country'] = country.upper()
		dict['language'] = language.upper()
		#if 'AL - ' in dict['title']: dict['title'] = dict['title'].replace('AL - ','AL ')
		#if 'EL - ' in dict['title']: dict['title'] = dict['title'].replace('EL - ','EL ')
		streams_not_sorted.append(dict)
	#LOG_THIS('NOTICE','EMAD 444')
	#with open('S:\\0iptvemad.m3u','w') as f: f.write(str(streams_not_sorted).replace("},","}\n,"))
	streams_sorted = sorted(streams_not_sorted, reverse=False, key=lambda key: key['title'].lower())
	grouped_streams = {}
	types = ['VOD_UNKNOWN_GROUPED','LIVE_GROUPED','VOD_SERIES_GROUPED','VOD_MOVIES_GROUPED','ALL','LIVE_ORIGINAL','VOD_ORIGINAL','LIVE_FROM_NAME_SORTED','VOD_FROM_NAME_SORTED','LIVE_GROUPED_SORTED','LIVE_UNKNOWN','VOD_MOVIES_GROUPED_SORTED','VOD_SERIES_GROUPED_SORTED','VOD_UNKNOWN_GROUPED_SORTED','DUMMY','LIVE_FROM_GROUP_SORTED','VOD_FROM_GROUP_SORTED','LIVE_ARCHIVED_GROUPED_SORTED','LIVE_EPG_GROUPED_SORTED','LIVE_TIMESHIFT_GROUPED_SORTED']
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
	grouped_streams['LIVE_TIMESHIFT_GROUPED_SORTED'] = grouped_streams['LIVE_ARCHIVED_GROUPED_SORTED']
	for dict in streams_not_sorted:
		type = dict['type']
		dict2 = {'group':dict['group'],'title':dict['title'],'url':dict['url'],'img':dict['img']}
		if   'LIVE' 		in type: grouped_streams['LIVE_GROUPED'].append(dict2)
		elif 'LIVE_UNKNOWN' in type: grouped_streams['LIVE_UNKNOWN'].append(dict2)
		elif 'VOD_MOVIES' 	in type: grouped_streams['VOD_MOVIES_GROUPED'].append(dict2)
		elif 'VOD_SERIES' 	in type: grouped_streams['VOD_SERIES_GROUPED'].append(dict2)
		elif 'VOD_UNKNOWN' 	in type: grouped_streams['VOD_UNKNOWN_GROUPED'].append(dict2)
		if   'LIVE' 		in type: grouped_streams['LIVE_ORIGINAL'].append(dict2)
		elif 'VOD' 			in type: grouped_streams['VOD_ORIGINAL'].append(dict2)
	grouped_streams['DUMMY'].append('')
	#LOG_THIS('NOTICE','EMAD 666 CREATE STREAMS FINISHED')
	DELETE_IPTV_FILES(False)
	for TYPE in types:
		WRITE_TO_SQL3('IPTV_STREAMS',TYPE,grouped_streams[TYPE],VERY_LONG_CACHE)
	with open(dummyiptvfile,'w') as f: f.write('')
	BUSY_DIALOG('stop')
	xbmcgui.Dialog().ok('رسالة من المبرمج','تم جلب ملفات IPTV جديدة')
	return

def DELETE_IPTV_FILES(show=True):
	if show:
		yes = xbmcgui.Dialog().yesno('مسح ملفات IPTV','تستطيع في أي وقت الدخول إلى قائمة IPTV وجلب ملفات IPTV جديدة .. هل تريد الآن مسح الملفات القديمة المخزنة في البرنامج ؟!','','','كلا','نعم')
		if not yes: return
	else: yes = False
	if isIPTVFiles(False): os.remove(dummyiptvfile)
	DELETE_FROM_SQL3('IPTV_ITEMS')
	DELETE_FROM_SQL3('IPTV_GROUPS')
	DELETE_FROM_SQL3('IPTV_STREAMS')
	#DELETE_FROM_SQL3('IMPORT_SECTIONS','LIVE')
	#CLEAN_KODI_CACHE_FOLDER()
	settings = xbmcaddon.Addon(id=addon_id)
	timestamp = settings.setSetting('iptv.timestamp','')
	timestamp = settings.setSetting('iptv.timediff','')
	if show: xbmcgui.Dialog().ok('رسالة من المبرمج','تم مسح جميع ملفات IPTV')
	return yes

def isIPTVFiles(show_msg=True):
	list = str(os.listdir(addoncachefolder))
	filename = dummyiptvfile.split('/')[-1].split('\\')[-1]
	if filename in list: return True
	#streams = READ_FROM_SQL3('IPTV_STREAMS','DUMMY')
	#if streams: return True
	if show_msg: xbmcgui.Dialog().ok('رسالة من المبرمج','انت بحاجة إلى الذهاب إلى قائمة IPTV ثم . أولا اضغط على "إضافة اشتراك IPTV المدفوع" (من أي شركة IPTV) . ثم ثانيا اضغط على جلب ملفات IPTV')
	return False

"""
def SAVE_STREAMS_TO_DISK(grouped_streams,types):
	filesLIST = []
	filesLIST.append('iptv_'+str(int(now))+'_.m3u')
	filename = 'iptv_'+str(int(now))+'__TYPE__.streams'
	settings = xbmcaddon.Addon(id=addon_id)
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
	xbmcgui.Dialog().ok('IPTV','تم جلب ملفات IPTV جديدة')
	return

def GET_STREAMS_FROM_DISK(TYPE):
	settings = xbmcaddon.Addon(id=addon_id)
	filename = settings.getSetting('iptv.file')
	filename = filename.replace('__TYPE__','_'+TYPE+'_')
	iptvFile = os.path.join(addoncachefolder,filename)
	f = open(iptvFile,'rb')
	streams_text = f.read()
	streams = EVAL(streams_text)
	return streams
"""



