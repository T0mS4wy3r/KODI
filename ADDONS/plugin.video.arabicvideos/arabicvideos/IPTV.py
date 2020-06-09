# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='IPTV'
menu_name='_IPT_'

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	#LOG_THIS('NOTICE','start')
	if   mode==230: results = MENU()
	elif mode==231: results = ADD_ACCOUNT()
	elif mode==232: results = CREATE_STREAMS()
	elif mode==233: results = GROUPS(url,text,'')
	elif mode==234: results = ITEMS(url,text)
	elif mode==235: results = PLAY(url,'LIVE')
	elif mode==236: results = PLAY(url,'VOD')
	elif mode==237: results = DELETE_IPTV_FROM_SQL3(True)
	#elif mode==238: results = ITEMS(url,text)
	elif mode==239: results = SEARCH(text)
	else: results = False
	#LOG_THIS('NOTICE','end')
	return results

def MENU():
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'بحث في ملفات IPTV','',239)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'اضافة اشتراك IPTV','',231)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'جلب ملفات IPTV','',232)
	addMenuItem('link','[COLOR FFC89008]IPT  [/COLOR]'+'مسح ملفات IPTV','',237)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة ومرتبة','LIVE_GROUPED',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'أفلام مصنفة ومرتبة','VOD_MOVIES',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'مسلسلات مصنفة ومرتبة','VOD_SERIES',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مجهولة','VOD_UNKNOWN',233)
	#addMenuItem('folder',menu_name+'قنوات مجهولة','LIVE_UNKNOWN',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة من أسمائها','LIVE_FROM_NAME',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مصنفة من أسمائها','VOD_FROM_NAME',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة من أقسامها','LIVE_FROM_GROUP',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مصنفة من أقسامها','VOD_FROM_GROUP',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'القنوات الاصلية بدون تغيير','LIVE_ORIGINAL',233)
	addMenuItem('folder','[COLOR FFC89008]IPT  [/COLOR]'+'الفيديوهات الاصلية بدون تغيير','VOD_ORIGINAL',233)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return

def GROUPS(TYPE,GROUP,website):
	results = READ_FROM_SQL3('IPTV_GROUPS',[TYPE,GROUP,website])
	if results: menuItemsLIST[:] = menuItemsLIST+results ; return
	else: previous_menuItemsLIST = menuItemsLIST[:] ; menuItemsLIST[:] = []
	if website=='': show = True
	else: show = False
	if not isIPTVFiles(show): return
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
	for group,img in z:
		if '____' in group: title2,group2 = group.split('____')
		else: title2,group2 = '',group
		if TYPE=='VOD_SERIES' and GROUP=='':
			title = title2
			if title in unique: continue
			unique.append(title)
			if 'RANDOM' in website: addMenuItem('folder',menu_name2+title,TYPE,167,'','',group)
			else: addMenuItem('folder',menu_name2+title,TYPE,233,'','',group)
		else:
			title = group2
			if title in unique: continue
			unique.append(title)
			if GROUP=='' and TYPE!='VOD_ORIGINAL': img = ''
			if title=='!!__UNKNOWN__!!': img = ''
			if TYPE!='VOD_SERIES' or GROUP=='' or title2 in GROUP:
				if 'RANDOM' in website: addMenuItem('folder',menu_name2+title,TYPE,167,img,'',group)
				else: addMenuItem('folder',menu_name2+title,TYPE,234,img,'',group)
	WRITE_TO_SQL3('IPTV_GROUPS',[TYPE,GROUP,website],menuItemsLIST,UNLIMITED_CACHE)
	menuItemsLIST[:] = previous_menuItemsLIST+menuItemsLIST
	return

def ITEMS(TYPE,GROUP):
	#LOG_THIS('NOTICE','before DATABASE')
	results = READ_FROM_SQL3('IPTV_ITEMS',[TYPE,GROUP])
	if results: menuItemsLIST[:] = menuItemsLIST+results ; return
	else: previous_menuItemsLIST = menuItemsLIST[:] ; menuItemsLIST[:] = []
	streams = READ_FROM_SQL3('IPTV_STREAMS',TYPE)
	for dict in streams:
		group = dict['group']
		if group==GROUP:
			title = dict['title']
			url = dict['url']
			img = dict['img']
			if 'LIVE' in TYPE: addMenuItem('live',menu_name+' '+title,url,235,img)
			else: addMenuItem('video',menu_name+' '+title,url,236,img)
	#xbmcgui.Dialog().ok('OUT',str(menuItemsLIST))
	WRITE_TO_SQL3('IPTV_ITEMS',[TYPE,GROUP],menuItemsLIST,UNLIMITED_CACHE)
	menuItemsLIST[:] = previous_menuItemsLIST+menuItemsLIST
	return

def PLAY(url,type):
	#xbmcgui.Dialog().ok(url,'')
	if 'LIVE' in type: PLAY_VIDEO(url,script_name,'live')
	else: PLAY_VIDEO(url,script_name,'video')
	return

def ADD_ACCOUNT():
	settings = xbmcaddon.Addon(id=addon_id)
	xbmcgui.Dialog().ok('IPTV','البرنامج يحتاج اشتراك IPTV من نوع رابط التحميل m3u من اي شركة IPTV والافضل ان يحتوي الرابط في نهايته على هذه الكلمات','&type=m3u_plus')
	iptvURL = settings.getSetting('iptv.url')
	if iptvURL!='':
		answer = xbmcgui.Dialog().yesno(iptvURL,'هذا هو رابط IPTV المسجل في البرنامج ... هل تريد تعديله أم تريد كتابة رابط جديد ؟!','','','كتابة جديد','تعديل القديم')
		if not answer: iptvURL = ''
	iptvURL = KEYBOARD('اكتب رابط IPTV كاملا',iptvURL)
	iptvURL = iptvURL.strip(' ')
	if iptvURL=='': return
	else:
		answer = xbmcgui.Dialog().yesno(iptvURL,'هل تريد استخدام هذا الرابط بدلا من الرابط القديم ؟','','','كلا','نعم')
		if not answer: return
	settings.setSetting('iptv.url',iptvURL)
	xbmcgui.Dialog().ok(iptvURL,'تم تغير رابط اشتراك IPTV الى هذا الرابط الجديد')
	CREATE_STREAMS()
	return

def SEARCH(search=''):
	if '::' in search:
		if not isIPTVFiles(False): return
		search = search.split('::')[0]
		exit = False
		TYPE = 'VOD_FROM_NAME'
	else:
		if not isIPTVFiles(True): return
		exit = True
		searchTitle = ['الكل','قنوات','أفلام','مسلسلات','أخرى']
		typeList = ['ALL','LIVE_GROUPED','VOD_MOVIES','VOD_SERIES','VOD_UNKNOWN']
		selection = xbmcgui.Dialog().select('أختر البحث المناسب', searchTitle)
		if selection == -1: return
		TYPE = typeList[selection]
	if search=='': search = KEYBOARD()
	if search == '': return
	streams = READ_FROM_SQL3('IPTV_STREAMS',TYPE)
	searchLower = search.lower()
	uniqueLIST = []
	for dict in streams:
		title = dict['title']
		group = dict['group']
		img = dict['img']
		if searchLower in group.lower():
			if group not in uniqueLIST:
				uniqueLIST.append(group)
				if '____' in group: group2 = group.split('____',1)[1]
				else: group2 = group
				addMenuItem('folder',menu_name+group2,TYPE,234,img,'',group)
		elif searchLower in title.lower():
			url = dict['url']
			if '.mp4' in url or '.mkv' in url or '.avi' in url or '.mp3' in url:
				if '!!__UNKNOWN__!!' in group: group2 = ''
				else: group2 = group+' '
				addMenuItem('video',menu_name+group2+title,url,236,img)
			else: addMenuItem('live',menu_name+group+title,url,235,img)
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

def CREATE_STREAMS():
	BUSY_DIALOG('start') ; 
	#LOG_THIS('NOTICE','EMAD 111')
	answer = xbmcgui.Dialog().yesno('IPTV','هل تريد أن تجلب الان ملفات IPTV جديدة ؟','','','كلا','نعم')
	if not answer:
		BUSY_DIALOG('stop')
		return
	settings = xbmcaddon.Addon(id=addon_id)
	iptvURL = settings.getSetting('iptv.url')
	headers = { 'User-Agent' : '' }
	try: m3u_text = openURL_cached(REGULAR_CACHE,iptvURL,'',headers,'','IPTV-CREATE_STREAMS-1st')
	except:
		xbmcgui.Dialog().ok('فشل في جلب ملفات IPTV','قد يكون السبب هو عدم وجود اشتراك IPTV أو رابط الاشتراك غير صحيح','جرب إضافة الاشتراك مرة اخرى من قائمة ال IPTV')
		LOG_THIS('ERROR',LOGGING(script_name)+'   No IPTV files could be downloaded')
		BUSY_DIALOG('stop')
		return
	#m3u_filename = 'iptv_'+str(int(now))+'_.m3u'
	#iptvFile = os.path.join(addoncachefolder,m3u_filename)
	#file = open(iptvFile, 'wb')
	#file.write(m3u_text)
	#file.close()
	m3u_text = m3u_text.replace('"tvg-','" tvg-')
	m3u_text = m3u_text.replace('َ','').replace('ً','').replace('ُ','').replace('ٌ','')
	m3u_text = m3u_text.replace('ّ','').replace('ِ','').replace('ٍ','').replace('ْ','')
	m3u_text = m3u_text.replace('group-title=','group=')
	m3u_text = m3u_text.replace('tvg-','')
	username = re.findall('username=(.*?)&',iptvURL+'&',re.DOTALL)
	password = re.findall('password=(.*?)&',iptvURL+'&',re.DOTALL)
	if username and password: 
		username = username[0]
		password = password[0]
		url_parts = iptvURL.split('/')
		server = url_parts[0]+'//'+url_parts[2]
		seriesCategoriesURL = server+'/player_api.php?username='+username+'&password='+password+'&action=get_series_categories'
		series_groups = openURL_cached(REGULAR_CACHE,seriesCategoriesURL,'',headers,'','IPTV-CREATE_STREAMS-2nd')
		series_groups = re.findall('category_name":"(.*?)"',series_groups,re.DOTALL)
		if series_groups:
			#xbmcgui.Dialog().ok('','')
			for group in series_groups:
				group = group.replace('\/','/').decode('unicode_escape').encode('utf8')
				m3u_text = m3u_text.replace('group="'+group+'"','group="__SERIES__'+group+'"')
		vodCategoriesURL = server+'/player_api.php?username='+username+'&password='+password+'&action=get_vod_categories'
		vod_groups = openURL_cached(REGULAR_CACHE,vodCategoriesURL,'',headers,'','IPTV-CREATE_STREAMS-3rd')
		vod_groups = re.findall('category_name":"(.*?)"',vod_groups,re.DOTALL)
		if vod_groups:
			for group in vod_groups:
				group = group.replace('\/','/').decode('unicode_escape').encode('utf8')
				m3u_text = m3u_text.replace('group="'+group+'"','group="__MOVIES__'+group+'"')
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
			if '__SERIES__' in group: type = 'VOD_SERIES'
			elif '__MOVIES__' in group: type = 'VOD_MOVIES'
			else: type = 'VOD_UNKNOWN'
			group = group.replace('__SERIES__','').replace('__MOVIES__','')
		else:
			if group=='': type = 'LIVE_UNKNOWN'
			else: type = 'LIVE_GROUPED'
		dict['type'] = type
		if group=='': group = type
		if dict['type']=='VOD_SERIES':
			series_title = re.findall('(.*?) [Ss]\d+ +[Ee]\d+',dict['title'],re.DOTALL)
			group = group+'____'
			if series_title: group = group+series_title[0]
			else: group = group+'!!__UNKNOWN__!!'
		dict['group'] = group.strip(' ').replace('  ',' ').replace('  ',' ').upper()
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
	streams_sorted = sorted(streams_not_sorted, reverse=False, key=lambda key: key['title'].lower())
	grouped_streams = {}
	types = ['ALL','LIVE_ORIGINAL','VOD_ORIGINAL','LIVE_FROM_NAME','VOD_FROM_NAME','LIVE_GROUPED','LIVE_UNKNOWN','VOD_MOVIES','VOD_SERIES','VOD_UNKNOWN','DUMMY','LIVE_FROM_GROUP','VOD_FROM_GROUP']
	for type in types: grouped_streams[type] = []
	#LOG_THIS('NOTICE','EMAD 444 CREATE STREAMS START creating 1st STREAMS dictionary')
	for dict in streams_sorted:
		type = dict['type']
		dict2 = {'group':dict['group'],'title':dict['title'],'url':dict['url'],'img':dict['img']}
		dict3 = {'group':dict['country'],'title':dict['title'],'url':dict['url'],'img':dict['img']}
		dict4 = {'group':dict['language'],'title':dict['title'],'url':dict['url'],'img':dict['img']}
		grouped_streams['ALL'].append(dict)
		grouped_streams[type].append(dict2)
		if  'LIVE' in type: grouped_streams['LIVE_FROM_NAME'].append(dict3)
		elif 'VOD' in type: grouped_streams['VOD_FROM_NAME'].append(dict3)
		if  'LIVE' in type: grouped_streams['LIVE_FROM_GROUP'].append(dict4)
		elif 'VOD' in type: grouped_streams['VOD_FROM_GROUP'].append(dict4)
	#LOG_THIS('NOTICE','EMAD 555 CREATE STREAMS finished 1st and START creating 2nd STREAMS dictionary')
	for dict in streams_not_sorted:
		type = dict['type']
		dict2 = {'group':dict['group'],'title':dict['title'],'url':dict['url'],'img':dict['img']}
		if 'LIVE' in type: grouped_streams['LIVE_ORIGINAL'].append(dict2)
		elif 'VOD' in type: grouped_streams['VOD_ORIGINAL'].append(dict2)
	grouped_streams['DUMMY'].append('')
	#LOG_THIS('NOTICE','EMAD 666 CREATE STREAMS FINISHED')
	DELETE_IPTV_FROM_SQL3(False)
	for TYPE in types:
		WRITE_TO_SQL3('IPTV_STREAMS',TYPE,grouped_streams[TYPE],UNLIMITED_CACHE)
	xbmcgui.Dialog().ok('IPTV','تم جلب ملفات IPTV جديدة')
	BUSY_DIALOG('stop')
	return

def isIPTVFiles(show_msg=True):
	streams = READ_FROM_SQL3('IPTV_STREAMS','DUMMY')
	#xbmcgui.Dialog().ok('DUMMY',str(streams))
	if streams: return True
	if show_msg: xbmcgui.Dialog().ok('جهازك لا يحتوي على ملفات IPTV','انت بحاجة إلى الذهاب إلى قائمة IPTV ثم . أولا اضغط على "إضافة اشتراك IPTV المدفوع" (من أي شركة IPTV) . ثم ثانيا اضغط على جلب ملفات IPTV')
	return False

def DELETE_IPTV_FROM_SQL3(show=True):
	if show:
		yes = xbmcgui.Dialog().yesno('مسح ملفات IPTV','تستطيع في أي وقت الدخول إلى قائمة IPTV وجلب ملفات IPTV جديدة .. هل تريد الآن مسح الملفات القديمة المخزنة في البرنامج ؟!','','','كلا','نعم')
		if not yes: return
	else: yes = False
	DELETE_FROM_SQL3('IPTV_ITEMS')
	DELETE_FROM_SQL3('IPTV_GROUPS')
	DELETE_FROM_SQL3('IPTV_STREAMS')
	#DELETE_FROM_SQL3('IMPORT_SECTIONS','LIVE')
	#CLEAN_KODI_CACHE_FOLDER()
	if show: xbmcgui.Dialog().ok('IPTV','تم مسح جميع ملفات IPTV')
	return yes

"""
def isIPTVFiles_Disk(show_msg=True):
	settings = xbmcaddon.Addon(id=addon_id)
	filename = settings.getSetting('iptv.file')
	list = str(os.listdir(addoncachefolder))
	if filename in list: return True
	if show_msg: xbmcgui.Dialog().ok('جهازك لا يحتوي على ملفات IPTV','انت بحاجة إلى الذهاب الى قائمة IPTV ثم:','أولا اضف اشتراكك المدفوع (من أي شركة IPTV)','ثم ثانيا أجلب ملفات IPTV')
	return False

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
	streams_text = streams_text.replace('u\'','\'')
	streams = eval(streams_text)
	return streams
"""



