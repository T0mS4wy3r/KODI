# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='IPTV'
menu_name='_IPT_'

def MAIN(mode,url,text):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if mode==230: MAIN_MENU()
	elif mode==231: ADD_ACCOUNT()
	elif mode==232: CREATE_ALL_FILES()
	elif mode==233: GROUPS(url,text)
	elif mode==234: ITEMS(url,text)
	elif mode==235: PLAY(url,'LIVE')
	elif mode==236: PLAY(url,'VOD')
	elif mode==239: SEARCH(text)
	return

def MAIN_MENU():
	addDir(menu_name+'اضافة اشتراك IPTV','',231)
	addDir(menu_name+'جلب ملفات IPTV','',232)
	addDir(menu_name+'بحث في ملفات IPTV','',239)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addDir(menu_name+'قنوات مصنفة ومرتبة','LIVE_GROUPED',233)
	addDir(menu_name+'أفلام مصنفة ومرتبة','VOD_MOVIES',233)
	addDir(menu_name+'مسلسلات مصنفة ومرتبة','VOD_SERIES',233)
	#addDir(menu_name+'قنوات مجهولة','LIVE_UNKNOWN',233)
	addDir(menu_name+'فيديوهات مجهولة','VOD_UNKNOWN',233)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addDir(menu_name+'قنوات مصنفة من أسمائها','LIVE',233)
	addDir(menu_name+'فيديوهات مصنفة من أسمائها','VOD',233)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addDir(menu_name+'قنوات بدون تغيير','LIVE_NOT_SORTED',233)
	addDir(menu_name+'فيديوهات بدون تغيير','VOD_NOT_SORTED',233)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def GROUPS(TYPE,GROUP):
	#xbmcgui.Dialog().textviewer('',str(categories))
	streams = GET_STREAMS(TYPE)
	if streams=='EXIT': return
	groups,unique,logos = [],[],[]
	for dict in streams:
		if TYPE in ['LIVE','VOD']: groups.append(dict['lang'])
		else: groups.append(dict['group'])
		logos.append(dict['img'])
	z = zip(groups,logos)
	z = sorted(z, reverse=False, key=lambda key: key[0])
	for group,img in z:
		if '____' in group: title2,group2 = group.split('____')
		else: title2,group2 = '',group
		if TYPE=='VOD_SERIES' and GROUP=='':
			title = title2
			if title in unique: continue
			unique.append(title)
			addDir(menu_name+title,TYPE,233,'','',group)
		else:
			title = group2
			if title in unique: continue
			unique.append(title)
			if GROUP=='' and TYPE!='VOD_NOT_SORTED': img = ''
			if title=='!!__UNKNOWN__!!': img = ''
			if TYPE!='VOD_SERIES' or GROUP=='' or title2 in GROUP:
				addDir(menu_name+title,TYPE,234,img,'',group)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def ITEMS(TYPE,GROUP):
	#xbmcgui.Dialog().ok(TYPE,GROUP)
	streams = GET_STREAMS(TYPE)
	for dict in streams:
		if TYPE in ['LIVE','VOD']: group = dict['lang']
		else: group = dict['group']
		if group==GROUP:
			title = dict['title']
			url = dict['url']
			img = dict['img']
			if 'LIVE' in TYPE: addLink(menu_name+title,url,235,img,'','IsPlayable=no')
			else: addLink(menu_name+title,url,236,img,'','IsPlayable=yes')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url,type):
	#xbmcgui.Dialog().ok(url,'')
	if 'LIVE' in type: PLAY_VIDEO(url,script_name,'no')
	else: PLAY_VIDEO(url,script_name,'yes')
	return

def ADD_ACCOUNT():
	settings = xbmcaddon.Addon(id=addon_id)
	xbmcgui.Dialog().ok('IPTV','البرنامج يحتاج اشتراك IPTV من نوع رابط التحميل m3u من اي شركة IPTV والافضل ان يحتوي الرابط في نهايته على هذه الكلمات','&type=m3u_plus')
	iptvURL = settings.getSetting('iptv.url')
	if iptvURL!='':
		answer = xbmcgui.Dialog().yesno(iptvURL,'هذا هو رابط IPTV المسجل في البرنامج هل تريد تغييره ؟')
		if not answer: return
	iptvURL = KEYBOARD('اكتب رابط IPTV كاملا')
	if iptvURL=='': return
	else:
		answer = xbmcgui.Dialog().yesno(iptvURL,'هل تريد استخدام هذا الرابط بدلا من الرابط القديم ؟')
		if not answer: return
	settings.setSetting('iptv.url',iptvURL)
	xbmcgui.Dialog().ok(iptvURL,'تم تغير رابط اشتراك IPTV الى هذا الرابط الجديد')
	CREATE_ALL_FILES()
	return

def CREATE_ALL_FILES():
	answer = xbmcgui.Dialog().yesno('IPTV','هل تريد تغير ملفات IPTV الان وجلب ملفات جديدة ؟')
	if not answer: return
	settings = xbmcaddon.Addon(id=addon_id)
	iptvFile = settings.getSetting('iptv.file')
	iptvURL = settings.getSetting('iptv.url')
	try: m3u_text = openURL_cached(REGULAR_CACHE,iptvURL,'','','','IPTV-CREATE_ALL_FILES-1st')
	except:
		xbmcgui.Dialog().ok('IPTV','جهازك لا يحتوي على ملفات IPTV','يجب عليك: اولا الضغط على رابط اضافة حسابك ثم ثانيا الضغط على رابط جلب الملفات')
		LOG_THIS('ERROR',LOGGING(script_name)+'   No IPTV files')
		return
	filesLIST = []
	filename = 'iptv_'+str(int(now))+'_.m3u'
	filesLIST.append(filename)
	iptvFile = os.path.join(addoncachefolder,filename)
	file = open(iptvFile, 'wb')
	file.write(m3u_text)
	file.close()
	m3u_text = m3u_text.replace('َ','').replace('ً','').replace('ُ','').replace('ٌ','')
	m3u_text = m3u_text.replace('ّ','').replace('ِ','').replace('ٍ','').replace('ْ','')
	username = re.findall('username=(.*?)&',iptvURL+'&',re.DOTALL)[0]
	password = re.findall('password=(.*?)&',iptvURL+'&',re.DOTALL)[0]
	host = re.findall('(http.*?://.*?)[:/\?]',iptvURL,re.DOTALL)[0]
	port = re.findall(':(\d+)[/\?]',iptvURL,re.DOTALL)
	if port: port = port[0]
	else: port = '80'
	seriesCategoriesURL = host+':'+port+'/player_api.php?username='+username+'&password='+password+'&action=get_series_categories'
	series_groups = openURL_cached(REGULAR_CACHE,seriesCategoriesURL,'','','','IPTV-CREATE_ALL_FILES-2nd')
	series_groups = re.findall('category_name":"(.*?)"',series_groups,re.DOTALL)
	m3u_text = m3u_text.replace('group-title=','group=')
	m3u_text = m3u_text.replace('tvg-','')
	if series_groups:
		#xbmcgui.Dialog().ok('','')
		for group in series_groups:
			group = group.replace('\/','/').decode('unicode_escape').encode('utf8')
			m3u_text = m3u_text.replace('group="'+group+'"','group="__SERIES__'+group+'"')
	vodCategoriesURL = host+':'+port+'/player_api.php?username='+username+'&password='+password+'&action=get_vod_categories'
	vod_groups = openURL_cached(REGULAR_CACHE,vodCategoriesURL,'','','','IPTV-CREATE_ALL_FILES-3rd')
	vod_groups = re.findall('category_name":"(.*?)"',vod_groups,re.DOTALL)
	if vod_groups:
		for group in vod_groups:
			group = group.replace('\/','/').decode('unicode_escape').encode('utf8')
			m3u_text = m3u_text.replace('group="'+group+'"','group="__MOVIES__'+group+'"')
	streams_not_sorted = CREATE_STREAMS(m3u_text)
	streams_sorted = sorted(streams_not_sorted, reverse=False, key=lambda key: key['title'].lower())
	grouped_streams = {}
	types = ['ALL','LIVE_NOT_SORTED','VOD_NOT_SORTED','LIVE','VOD','LIVE_GROUPED','LIVE_UNKNOWN','VOD_MOVIES','VOD_SERIES','VOD_UNKNOWN']
	for type in types: grouped_streams[type] = []
	for dict in streams_sorted:
		dict2 = dict.copy()
		type = dict2['type']
		del dict2['type']
		grouped_streams['ALL'].append(dict2)
		if 'LIVE' in type: grouped_streams['LIVE'].append(dict2)
		elif 'VOD' in type: grouped_streams['VOD'].append(dict2)
		grouped_streams[type].append(dict2)
		#if 'AWALEM KHAFIYA S01 E03' in dict2['title']:
		#	xbmcgui.Dialog().ok(dict2['title'],'')
	for dict in streams_not_sorted:
		type = dict['type']
		del dict['type']
		if 'LIVE' in type: grouped_streams['LIVE_NOT_SORTED'].append(dict)
		elif 'VOD' in type: grouped_streams['VOD_NOT_SORTED'].append(dict)
	"""
	for dict in streams_sorted:
		dict3 = dict.copy()
		del dict3['group2']
		if dict3['type']=='VOD_SERIES':
			title = dict3['title']
			series_title = re.findall('(.*?) [Ss]\d+ +[Ee]\d+',title,re.DOTALL)
			if series_title: dict3['group'] = series_title[0]
			else: dict3['group'] = '!!__UNKNOWN__!!'
			dict3['type'] = 'VOD_EPISODES'
			grouped_streams['VOD_EPISODES'].append(dict3)
	"""
	#for dict in grouped_streams['VOD']:
	#	if 'AWALEM KHAFIYA S01 E03' in dict['title']:
	#		xbmcgui.Dialog().ok(dict['title'],dict['title'][0:3])
	filename = 'iptv_'+str(int(now))+'__TYPE__.streams'
	for type in types:
		new_streams = str(grouped_streams[type])
		new_streams = new_streams.replace('},','},\n')
		new_filename = filename.replace('__TYPE__','_'+type+'_')
		iptvFile = os.path.join(addoncachefolder,new_filename)
		file = open(iptvFile, 'wb')
		file.write(new_streams)
		file.close()
		filesLIST.append(new_filename)
	xbmcgui.Dialog().ok('IPTV','تم جلب ملفات IPTV جديدة')
	settings.setSetting('iptv.file',filename)
	for filename in os.listdir(addoncachefolder):
		cond1 = ('_.streams' in filename or '_.m3u' in filename)
		if 'iptv_' in filename and cond1 and filename not in filesLIST:
			iptvOldFile = os.path.join(addoncachefolder,filename)
			os.remove(iptvOldFile)
	return

def CREATE_STREAMS(m3u_text):
	lines = re.findall('#EXTINF(.*?)[\n\r]+(.*?)[\n\r]+',m3u_text+'\n',re.DOTALL)
	streams = []
	for line,url in lines:
		dict = {}
		dict['url'] = url
		#xbmcgui.Dialog().ok(line,title)
		if '",' in line:
			line,title = line.rsplit('",',1)
			line = line+'"'
		else: line,title = line.rsplit('1,',1)
		params = re.findall(' (.*?)="(.*?)"',line,re.DOTALL)
		for key,value in params:
			key = key.replace('"','').strip(' ')
			dict[key] = value.strip(' ')
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
		if '\u' in dict['title'].lower(): dict['title'] = dict['title'].decode('unicode_escape')
		title = dict['title'].replace('||','|').replace('::',':').replace('--','-')
		title = title.replace('[[','[').replace(']]',']')
		title = title.replace('((','(').replace('))',')')
		title0 = title[0]
		title2 = title[1:].strip(' ')
		if title0==':' or title0=='|' or title0=='-' or title0=='[' or title0=='(': title0 = ''
		separator = re.findall('[\:\|\-\]\)]',title2,re.DOTALL)
		if separator:
			separator = separator[0]
			part1,part2 = title2.split(separator,1)
			part1 = title0+part1
			dict['title'] = part1.strip(' ').upper()+' '+separator+' '+part2.strip(' ')#.title()
			dict['lang'] = part1.strip(' ').upper()
		else:
			dict['title'] = title#.title()
			dict['lang'] = '!!__UNKNOWN__!!'
		streams.append(dict)
	return streams

def GET_STREAMS(TYPE):
	settings = xbmcaddon.Addon(id=addon_id)
	filename = settings.getSetting('iptv.file')
	filename = filename.replace('__TYPE__','_'+TYPE+'_')
	iptvFile = os.path.join(addoncachefolder,filename)
	try:
		f = open(iptvFile,'rb')
		streams_text = f.read()
		streams_text = streams_text.replace('u\'','\'')
		streams = eval(streams_text)
		return streams
	except:
		xbmcgui.Dialog().ok('جهازك لا يحتوي على ملفات IPTV','يجب عليك:','اولا اضافة اشتراكك في خدمة IPTV','ثم ثانيا جلب ملفات IPTV')
		return 'EXIT'

def SEARCH(search=''):
	searchTitle = ['بحث في جميع ملفات IPTV','بحث عن قنوات IPTV','بحث عن فيديوهات IPTV']
	typeList = ['ALL','LIVE','VOD']
	selection = xbmcgui.Dialog().select('أختر البحث المناسب', searchTitle)
	if selection == -1: return
	type = typeList[selection]
	if search=='': search = KEYBOARD()
	if search == '': return
	settings = xbmcaddon.Addon(id=addon_id)
	filename = settings.getSetting('iptv.file')
	filename = filename.replace('__TYPE__','_'+type+'_')
	iptvFile = os.path.join(addoncachefolder,filename)
	f = open(iptvFile,'rb')
	streams_text = f.read()
	streams_text = streams_text.replace('u\'','\'')
	streams = eval(streams_text)
	searchLower = search.lower()
	for dict in streams:
		title = dict['title']
		if searchLower in title.lower():
			url = dict['url']
			img = dict['img']
			if '.mp4' in url or '.mkv' in url or '.avi' in url or '.mp3' in url:
				#type = 'VOD'
				addLink(menu_name+title,url,236,img,'','IsPlayable=yes')
			else:
				#type = 'LIVE'
				addLink(menu_name+title,url,235,img,'','IsPlayable=no')
	xbmcplugin.endOfDirectory(addon_handle)
	return




