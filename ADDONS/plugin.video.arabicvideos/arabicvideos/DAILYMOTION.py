# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='DAILYMOTION'
menu_name='_DLM_'
website0a = WEBSITES[script_name][0]
website0b = WEBSITES[script_name][1]

def MAIN(mode,url,text,type,page):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if	 mode==400: results = MENU(url)
	elif mode==401: results = EXTRACT_PLAYLIST(url,text)
	elif mode==402: results = CHANNELS_SUBMENU(url,text)
	elif mode==403: results = PLAY(url,text)
	elif mode==404: results = SEARCH_FOR_VIDEOS(text,page)
	elif mode==405: results = SEARCH_FOR_PLAYLISTS(text,page)
	elif mode==406: results = SEARCH_FOR_CHANNELS(text,page)
	elif mode==407: results = GET_CHANNEL_PLAYLISTS(url,page)
	elif mode==408: results = GET_CHANNEL_VIDEOS(url,page)
	elif mode==409: results = SEARCH(text,page)
	elif mode==411: a = 0
	elif mode==412: a = 0
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',409,'','','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'بحث عن فيديوهات','',409,'','videos?sortBy=','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'بحث عن آخر الفيديوهات','',409,'','videos?sortBy=RECENT','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'بحث عن الفيديوهات الأكثر مشاهدة','',409,'','videos?sortBy=VIEW_COUNT','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'بحث عن قوائم التشغيل','',409,'','playlists','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'بحث عن القنوات','',409,'','channels','_REMEMBERRESULTS_')
	return

def CHANNELS_SUBMENU(url,ownerNAME):
	#DIALOG_OK(url,ownerNAME)
	if '/dm_' in url:
		response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url,'','',False,'','DAILYMOTION-CHANNELS_SUBMENU-1st',False,False)
		headers = response.headers
		if 'Location' in headers.keys(): url = website0a+headers['Location']
	ownerNAME = '[COLOR FFC89008]'+ownerNAME+'[/COLOR]'
	ownerNAME = escapeUNICODE(ownerNAME)
	addMenuItem('folder',menu_name+' - آخر الفيديوهات'+ownerNAME,url+'/videos',408)
	addMenuItem('folder',menu_name+' - اكثر الفيديوهات مشاهدة'+ownerNAME,url+'/videos?sort=visited',408)
	addMenuItem('folder',menu_name+' - آخر قوائم التشغيل'+ownerNAME,url+'/playlists',407)
	addMenuItem('folder',menu_name+' - قوائم التشغيل ابجدية'+ownerNAME,url+'/playlists?sort=alphaaz',407)
	return

def PLAY(url,owner):
	import RESOLVERS
	errormsg,titleLIST,linkLIST = RESOLVERS.DAILYMOTION(url)
	if errormsg:
		DIALOG_OK('رسالة من الموقع',errormsg)
		return
	link = linkLIST[0]
	titleLIST2,linkLIST2 = EXTRACT_M3U8(link)
	owner_id,owner_name = owner.split('::',1)
	owner_url = website0a+'/'+owner_id
	titleLIST = ['[COLOR FFC89008]OWNER:  '+owner_name+'[/COLOR]']+titleLIST2
	linkLIST = [owner_url]+linkLIST2
	selection = DIALOG_SELECT('اختر الملف المناسب: ('+str(len(linkLIST)-1)+' ملف)',titleLIST)
	if selection==-1: return
	elif selection==0:
		new_path = sys.argv[0]+'?type=folder&mode=402&url='+owner_url+'&text='+owner_name
		xbmc.executebuiltin("Container.Update("+new_path+")")
		return
	link =  linkLIST[selection]
	PLAY_VIDEO(link,script_name,'video')
	return

def SEARCH_FOR_VIDEOS(search,page=''):
	#DIALOG_OK(search,page)
	if page=='': page = '1'
	if 'sortBy=' in search: sort = search.split('sortBy=')[1].split('&')[0]
	else: sort = ''
	search = search.split('/videos')[0]
	request = '{"operationName":"SEARCH_QUERY","variables":{"query":"mysearchwords","shouldIncludeChannels":false,"shouldIncludePlaylists":false,"shouldIncludeVideos":true,"page":mypagenumber,"limit":mypagelimitmysortmethod},"query":"fragment VIDEO_BASE_FRAGMENT on Video {\n  id\n  xid\n  title\n  createdAt\n  stats {\n    views {\n      total\n      __typename\n    }\n    __typename\n  }\n  channel {\n    id\n    xid\n    name\n    displayName\n    accountType\n    __typename\n  }\n  duration\n  thumbnailx60: thumbnailURL(size: \"x60\")\n  thumbnailx120: thumbnailURL(size: \"x120\")\n  thumbnailx240: thumbnailURL(size: \"x240\")\n  thumbnailx720: thumbnailURL(size: \"x720\")\n  __typename\n}\n\nfragment VIDEO_WATCH_LATER_FRAGMENT on Video {\n  id\n  isInWatchLater\n  __typename\n}\n\nfragment CHANNEL_BASE_FRAG on Channel {\n  accountType\n  id\n  xid\n  name\n  displayName\n  isFollowed\n  thumbnailx60: logoURL(size: \"x60\")\n  thumbnailx120: logoURL(size: \"x120\")\n  thumbnailx240: logoURL(size: \"x240\")\n  thumbnailx720: logoURL(size: \"x720\")\n  __typename\n}\n\nfragment PLAYLIST_BASE_FRAG on Collection {\n  id\n  xid\n  name\n  channel {\n    id\n    xid\n    name\n    displayName\n    accountType\n    __typename\n  }\n  description\n  thumbnailx60: thumbnailURL(size: \"x60\")\n  thumbnailx120: thumbnailURL(size: \"x120\")\n  thumbnailx240: thumbnailURL(size: \"x240\")\n  thumbnailx720: thumbnailURL(size: \"x720\")\n  stats {\n    videos {\n      total\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery SEARCH_QUERY($query: String!, $shouldIncludeVideos: Boolean!, $shouldIncludeChannels: Boolean!, $shouldIncludePlaylists: Boolean!, $page: Int, $limit: Int, $sortByVideos: SearchVideoSort, $durationMinVideos: Int, $durationMaxVideos: Int, $createdAfterVideos: DateTime) {\n  search {\n    id\n    videos(query: $query, first: $limit, page: $page, sort: $sortByVideos, durationMin: $durationMinVideos, durationMax: $durationMaxVideos, createdAfter: $createdAfterVideos) @include(if: $shouldIncludeVideos) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      totalCount\n      edges {\n        node {\n          id\n          ...VIDEO_BASE_FRAGMENT\n          ...VIDEO_WATCH_LATER_FRAGMENT\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    channels(query: $query, first: $limit, page: $page) @include(if: $shouldIncludeChannels) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      totalCount\n      edges {\n        node {\n          id\n          ...CHANNEL_BASE_FRAG\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    playlists: collections(query: $query, first: $limit, page: $page) @include(if: $shouldIncludePlaylists) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      totalCount\n      edges {\n        node {\n          id\n          ...PLAYLIST_BASE_FRAG\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}'
	request = request.replace('mysearchwords',search)
	request = request.replace('mypagelimit','40')
	request = request.replace('mypagenumber',page)
	if sort=='': request = request.replace('mysortmethod','')
	else: request = request.replace('mysortmethod',',"sortByVideos":"'+sort+'"')
	url = website0a+'/search/'+search+'/videos'
	html = GET_PAGEDATA(request)
	html_blocks = re.findall('"videos"(.*?)"VideoConnection"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('"node".*?"xid": (.*?),.*?"title": (.*?),.*?"name": (.*?),.*?"displayName": (.*?),.*?"duration": (.*?),.*?"thumbnailx240": (.*?),',block,re.DOTALL)
		for id,title,ownerID,ownerNAME,duration,img in items:
			if '"' in id: id = id.replace('"','')
			if '"' in title: title = title.replace('"','')
			if '"' in img: img = img.replace('"','')
			if '"' in duration: duration = duration.replace('"','')
			if '"' in ownerID: ownerID = ownerID.replace('"','')
			if '"' in ownerNAME: ownerNAME = ownerNAME.replace('"','')
			link = website0a+'/video/'+id
			title = title.rstrip('\\').strip(' ')
			title = escapeUNICODE(title)
			owner = ownerID+'::'+ownerNAME
			addMenuItem('video',menu_name+title,link,403,img,duration,owner)
		if '"hasNextPage": true,' in html:
			page = str(int(page)+1)
			addMenuItem('folder',menu_name+'صفحة '+page,url,404,'',page,search)
	return

def SEARCH_FOR_PLAYLISTS(search,page=''):
	if page=='': page = '1'
	request = '{"operationName":"SEARCH_QUERY","variables":{"query":"mysearchwords","shouldIncludeChannels":false,"shouldIncludePlaylists":true,"shouldIncludeVideos":false,"page":mypagenumber,"limit":mypagelimit},"query":"fragment VIDEO_BASE_FRAGMENT on Video {\n  id\n  xid\n  title\n  createdAt\n  stats {\n    views {\n      total\n      __typename\n    }\n    __typename\n  }\n  channel {\n    id\n    xid\n    name\n    displayName\n    accountType\n    __typename\n  }\n  duration\n  thumbnailx60: thumbnailURL(size: \"x60\")\n  thumbnailx120: thumbnailURL(size: \"x120\")\n  thumbnailx240: thumbnailURL(size: \"x240\")\n  thumbnailx720: thumbnailURL(size: \"x720\")\n  __typename\n}\n\nfragment VIDEO_WATCH_LATER_FRAGMENT on Video {\n  id\n  isInWatchLater\n  __typename\n}\n\nfragment CHANNEL_BASE_FRAG on Channel {\n  accountType\n  id\n  xid\n  name\n  displayName\n  isFollowed\n  thumbnailx60: logoURL(size: \"x60\")\n  thumbnailx120: logoURL(size: \"x120\")\n  thumbnailx240: logoURL(size: \"x240\")\n  thumbnailx720: logoURL(size: \"x720\")\n  __typename\n}\n\nfragment PLAYLIST_BASE_FRAG on Collection {\n  id\n  xid\n  name\n  channel {\n    id\n    xid\n    name\n    displayName\n    accountType\n    __typename\n  }\n  description\n  thumbnailx60: thumbnailURL(size: \"x60\")\n  thumbnailx120: thumbnailURL(size: \"x120\")\n  thumbnailx240: thumbnailURL(size: \"x240\")\n  thumbnailx720: thumbnailURL(size: \"x720\")\n  stats {\n    videos {\n      total\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery SEARCH_QUERY($query: String!, $shouldIncludeVideos: Boolean!, $shouldIncludeChannels: Boolean!, $shouldIncludePlaylists: Boolean!, $page: Int, $limit: Int, $sortByVideos: SearchVideoSort, $durationMinVideos: Int, $durationMaxVideos: Int, $createdAfterVideos: DateTime) {\n  search {\n    id\n    videos(query: $query, first: $limit, page: $page, sort: $sortByVideos, durationMin: $durationMinVideos, durationMax: $durationMaxVideos, createdAfter: $createdAfterVideos) @include(if: $shouldIncludeVideos) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      totalCount\n      edges {\n        node {\n          id\n          ...VIDEO_BASE_FRAGMENT\n          ...VIDEO_WATCH_LATER_FRAGMENT\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    channels(query: $query, first: $limit, page: $page) @include(if: $shouldIncludeChannels) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      totalCount\n      edges {\n        node {\n          id\n          ...CHANNEL_BASE_FRAG\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    playlists: collections(query: $query, first: $limit, page: $page) @include(if: $shouldIncludePlaylists) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      totalCount\n      edges {\n        node {\n          id\n          ...PLAYLIST_BASE_FRAG\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}'
	request = request.replace('mysearchwords',search)
	request = request.replace('mypagelimit','40')
	request = request.replace('mypagenumber',page)
	url = website0a+'/search/'+search+'/playlists'
	html = GET_PAGEDATA(request)
	items = re.findall('"node".*?"xid": (.*?),.*?"name": (.*?),.*?"xid": (.*?),.*?"name": (.*?),.*?"displayName": (.*?),.*?"thumbnailx240": (.*?),.*?"total": (.*?),',html,re.DOTALL)
	for id,name,ownerXID,ownerID,ownerNAME,img,count in items:
		if '"' in ownerXID: ownerXID = ownerXID.replace('"','')
		if '"' in ownerID: ownerID = ownerID.replace('"','')
		if '"' in ownerNAME: ownerNAME = ownerNAME.replace('"','')
		if '"' in id: id = id.replace('"','')
		if '"' in name: name = name.replace('"','')
		if '"' in img: img = img.replace('"','')
		if '"' in count: count = count.replace('"','')
		link = website0a+'/playlist/'+id
		title = 'LIST'+count+':  '+name
		title = title.rstrip('\\').strip(' ')
		title = escapeUNICODE(title)
		owner = ownerID+'::'+ownerNAME
		#DIALOG_OK('',owner)
		addMenuItem('folder',menu_name+title,link,401,img,'',owner)
	if '"hasNextPage": true,' in html:
		page = str(int(page)+1)
		addMenuItem('folder',menu_name+'صفحة '+page,url,405,'',page,search)
	return

def SEARCH_FOR_CHANNELS(search,page=''):
	if page=='': page = '1'
	request = '{"operationName":"SEARCH_QUERY","variables":{"query":"mysearchwords","shouldIncludeChannels":true,"shouldIncludePlaylists":false,"shouldIncludeVideos":false,"page":mypagenumber,"limit":mypagelimit},"query":"fragment VIDEO_BASE_FRAGMENT on Video {\n  id\n  xid\n  title\n  createdAt\n  stats {\n    views {\n      total\n      __typename\n    }\n    __typename\n  }\n  channel {\n    id\n    xid\n    name\n    displayName\n    accountType\n    __typename\n  }\n  duration\n  thumbnailx60: thumbnailURL(size: \"x60\")\n  thumbnailx120: thumbnailURL(size: \"x120\")\n  thumbnailx240: thumbnailURL(size: \"x240\")\n  thumbnailx720: thumbnailURL(size: \"x720\")\n  __typename\n}\n\nfragment VIDEO_WATCH_LATER_FRAGMENT on Video {\n  id\n  isInWatchLater\n  __typename\n}\n\nfragment CHANNEL_BASE_FRAG on Channel {\n  accountType\n  id\n  xid\n  name\n  displayName\n  isFollowed\n  thumbnailx60: logoURL(size: \"x60\")\n  thumbnailx120: logoURL(size: \"x120\")\n  thumbnailx240: logoURL(size: \"x240\")\n  thumbnailx720: logoURL(size: \"x720\")\n  __typename\n}\n\nfragment PLAYLIST_BASE_FRAG on Collection {\n  id\n  xid\n  name\n  channel {\n    id\n    xid\n    name\n    displayName\n    accountType\n    __typename\n  }\n  description\n  thumbnailx60: thumbnailURL(size: \"x60\")\n  thumbnailx120: thumbnailURL(size: \"x120\")\n  thumbnailx240: thumbnailURL(size: \"x240\")\n  thumbnailx720: thumbnailURL(size: \"x720\")\n  stats {\n    videos {\n      total\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery SEARCH_QUERY($query: String!, $shouldIncludeVideos: Boolean!, $shouldIncludeChannels: Boolean!, $shouldIncludePlaylists: Boolean!, $page: Int, $limit: Int, $sortByVideos: SearchVideoSort, $durationMinVideos: Int, $durationMaxVideos: Int, $createdAfterVideos: DateTime) {\n  search {\n    id\n    videos(query: $query, first: $limit, page: $page, sort: $sortByVideos, durationMin: $durationMinVideos, durationMax: $durationMaxVideos, createdAfter: $createdAfterVideos) @include(if: $shouldIncludeVideos) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      totalCount\n      edges {\n        node {\n          id\n          ...VIDEO_BASE_FRAGMENT\n          ...VIDEO_WATCH_LATER_FRAGMENT\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    channels(query: $query, first: $limit, page: $page) @include(if: $shouldIncludeChannels) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      totalCount\n      edges {\n        node {\n          id\n          ...CHANNEL_BASE_FRAG\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    playlists: collections(query: $query, first: $limit, page: $page) @include(if: $shouldIncludePlaylists) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      totalCount\n      edges {\n        node {\n          id\n          ...PLAYLIST_BASE_FRAG\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}'
	request = request.replace('mysearchwords',search)
	request = request.replace('mypagelimit','40')
	request = request.replace('mypagenumber',page)
	url = website0a+'/search/'+search+'/channels'
	html = GET_PAGEDATA(request)
	html_blocks = re.findall('"channels"(.*?)"ChannelConnection"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('"node".*?"name": (.*?),.*?"displayName": (.*?),.*?"thumbnailx240": (.*?),',block,re.DOTALL)
		for id,name,img in items:
			if '"' in id: id = id.replace('"','')
			if '"' in name: name = name.replace('"','')
			if '"' in img: img = img.replace('"','')
			link = website0a+'/'+id
			title = 'CHNL:  '+name
			title = title.rstrip('\\').strip(' ')
			title = escapeUNICODE(title)
			addMenuItem('folder',menu_name+title,link,402,img,'',name)
		if '"hasNextPage": true,' in html:
			page = str(int(page)+1)
			addMenuItem('folder',menu_name+'صفحة '+page,url,406,'',page,search)
	return

def EXTRACT_PLAYLIST(url,owner):
	#DIALOG_OK(url,owner)
	id = url.split('/')[-1]
	ownerID,ownerNAME = owner.split('::',1)
	link = website0a+'/'+ownerID
	title = '[COLOR FFC89008]OWNER:  '+ownerNAME+'[/COLOR]'
	title = escapeUNICODE(title)
	addMenuItem('folder',menu_name+title,link,402,'','',ownerNAME)
	request = '{"operationName":"DISCOVERY_QUEUE_QUERY","variables":{"collectionXid":"myplaylistid","videoXid":"x7s7qbn"},"query":"query DISCOVERY_QUEUE_QUERY($videoXid: String!, $collectionXid: String, $device: String, $videoCountPerSection: Int) {\n  views {\n    id\n    neon {\n      id\n      sections(device: $device, space: \"watching\", followingChannelXids: [], followingTopicXids: [], watchedVideoXids: [], context: {mediaXid: $videoXid, collectionXid: $collectionXid}, first: 20) {\n        edges {\n          node {\n            id\n            name\n            groupingType\n            relatedComponent {\n              ... on Channel {\n                __typename\n                id\n                xid\n                name\n                displayName\n                logoURL(size: \"x60\")\n                logoURLx25: logoURL(size: \"x25\")\n              }\n              ... on Topic {\n                __typename\n                id\n                xid\n                name\n                names {\n                  edges {\n                    node {\n                      id\n                      name\n                      language {\n                        id\n                        codeAlpha2\n                        __typename\n                      }\n                      __typename\n                    }\n                    __typename\n                  }\n                  __typename\n                }\n              }\n              ... on Collection {\n                __typename\n                id\n                xid\n                name\n              }\n              __typename\n            }\n            components(first: $videoCountPerSection) {\n              metadata {\n                algorithm {\n                  name\n                  version\n                  uuid\n                  __typename\n                }\n                __typename\n              }\n              edges {\n                node {\n                  ... on Video {\n                    __typename\n                    id\n                    xid\n                    title\n                    duration\n                    thumbnailx60: thumbnailURL(size: \"x60\")\n                    thumbnailx120: thumbnailURL(size: \"x120\")\n                    thumbnailx240: thumbnailURL(size: \"x240\")\n                    thumbnailx720: thumbnailURL(size: \"x720\")\n                    channel {\n                      id\n                      xid\n                      accountType\n                      displayName\n                      logoURLx25: logoURL(size: \"x25\")\n                      logoURL(size: \"x60\")\n                      __typename\n                    }\n                  }\n                  ... on Channel {\n                    __typename\n                    id\n                    xid\n                    name\n                    displayName\n                    accountType\n                    logoURL(size: \"x60\")\n                  }\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}'
	request = request.replace('myplaylistid',id)
	html = GET_PAGEDATA(request)
	html_blocks = re.findall('"collection_videos"(.*?)"SectionEdge"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('"node".*?"xid": (.*?),.*?"title": (.*?),.*?"duration": (.*?),.*?"thumbnailx240": (.*?),.*?"xid": (.*?),.*?"displayName": (.*?),',block,re.DOTALL)
		#DIALOG_OK(str(len(items)),str(items))
		for id,title,duration,img,ownerID,ownerNAME in items:
			if '"' in id: id = id.replace('"','')
			if '"' in title: title = title.replace('"','')
			if '"' in img: img = img.replace('"','')
			if '"' in duration: duration = duration.replace('"','')
			if '"' in ownerID: ownerID = ownerID.replace('"','')
			if '"' in ownerNAME: ownerNAME = ownerNAME.replace('"','')
			link = website0a+'/video/'+id
			title = title.rstrip('\\').strip(' ')
			title = escapeUNICODE(title)
			owner = ownerID+'::'+ownerNAME
			addMenuItem('video',menu_name+title,link,403,img,duration,owner)
	return

def GET_CHANNEL_PLAYLISTS(url,page=''):
	#DIALOG_OK(url,'')
	if page=='': page = '1'
	id2 = url.split('/')[-2]
	if 'sort=' in url: sort = url.split('sort=')[1].split('&')[0]
	else: sort = 'recent'
	request = '{"operationName":"CHANNEL_COLLECTIONS_QUERY","variables":{"channel_xid":"mychannelid","sort":"mysortmethod","page":mypagenumber},"query":"fragment CHANNEL_BASE_FRAGMENT on Channel {\n  id\n  xid\n  name\n  displayName\n  isArtist\n  logoURL(size: \"x60\")\n  isFollowed\n  accountType\n  __typename\n}\n\nfragment CHANNEL_IMAGES_FRAGMENT on Channel {\n  id\n  coverURLx375: coverURL(size: \"x375\")\n  __typename\n}\n\nfragment CHANNEL_UPDATED_FRAGMENT on Channel {\n  id\n  isFollowed\n  stats {\n    views {\n      total\n      __typename\n    }\n    followers {\n      total\n      __typename\n    }\n    videos {\n      total\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CHANNEL_COMPLETE_FRAGMENT on Channel {\n  id\n  ...CHANNEL_BASE_FRAGMENT\n  ...CHANNEL_IMAGES_FRAGMENT\n  ...CHANNEL_UPDATED_FRAGMENT\n  description\n  coverURL1024x: coverURL(size: \"1024x\")\n  coverURL1920x: coverURL(size: \"1920x\")\n  externalLinks {\n    facebookURL\n    twitterURL\n    websiteURL\n    instagramURL\n    __typename\n  }\n  __typename\n}\n\nfragment CHANNEL_FRAGMENT on Channel {\n  accountType\n  id\n  xid\n  name\n  displayName\n  isArtist\n  logoURL(size: \"x60\")\n  coverURLx375: coverURL(size: \"x375\")\n  isFollowed\n  stats {\n    views {\n      total\n      __typename\n    }\n    followers {\n      total\n      __typename\n    }\n    videos {\n      total\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery CHANNEL_COLLECTIONS_QUERY($channel_xid: String!, $sort: String, $page: Int!) {\n  channel(xid: $channel_xid) {\n    id\n    ...CHANNEL_COMPLETE_FRAGMENT\n    channel_playlist_collections: collections(sort: $sort, page: $page, first: mypagelimit) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      edges {\n        node {\n          id\n          xid\n          updatedAt\n          name\n          description\n          thumbURLx240: thumbnailURL(size: \"x240\")\n          thumbURLx360: thumbnailURL(size: \"x360\")\n          thumbURLx480: thumbnailURL(size: \"x480\")\n          stats {\n            videos {\n              total\n              __typename\n            }\n            __typename\n          }\n          channel {\n            id\n            ...CHANNEL_FRAGMENT\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}'
	request = request.replace('mychannelid',id2)
	request = request.replace('mypagelimit','40')
	request = request.replace('mypagenumber',page)
	request = request.replace('mysortmethod',sort)
	html = GET_PAGEDATA(request)
	html_blocks = re.findall('"channel_playlist_collections"(.*?)"CollectionConnection"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('"node".*?"xid": (.*?),.*?"name": (.*?),.*?"thumbURLx240": (.*?),.*?"total": (.*?),.*?"xid": (.*?),.*?"name": (.*?),.*?"displayName": (.*?),',block,re.DOTALL)
		#DIALOG_OK(str(len(items)),str(items))
		for id,name,img,count,ownerXID,ownerID,ownerNAME in items:
			if '"' in id: id = id.replace('"','')
			if '"' in name: name = name.replace('"','')
			if '"' in img: img = img.replace('"','')
			if '"' in count: count = count.replace('"','')
			if '"' in ownerXID: ownerXID = ownerXID.replace('"','')
			if '"' in ownerID: ownerID = ownerID.replace('"','')
			if '"' in ownerNAME: ownerNAME = ownerNAME.replace('"','')
			link = website0a+'/playlist/'+id
			title = 'LIST'+count+':  '+name
			title = title.rstrip('\\').strip(' ')
			title = escapeUNICODE(title)
			owner = ownerID+'::'+ownerNAME
			addMenuItem('folder',menu_name+title,link,401,img,'',owner)
		if '"hasNextPage": true,' in html:
			page = str(int(page)+1)
			addMenuItem('folder',menu_name+'صفحة '+page,url,407,'',page)
	return

def GET_CHANNEL_VIDEOS(url,page=''):
	#DIALOG_OK(url,'')
	if page=='': page = '1'
	id2 = url.split('/')[-2]
	if 'sort=' in url: sort = url.split('sort=')[1].split('&')[0]
	else: sort = 'recent'
	request = '{"operationName":"CHANNEL_VIDEOS_QUERY","variables":{"channel_xid":"mychannelid","sort":"mysortmethod","page":mypagenumber},"query":"fragment CHANNEL_BASE_FRAGMENT on Channel {\n  id\n  xid\n  name\n  displayName\n  isArtist\n  logoURL(size: \"x60\")\n  isFollowed\n  accountType\n  __typename\n}\n\nfragment CHANNEL_IMAGES_FRAGMENT on Channel {\n  id\n  coverURLx375: coverURL(size: \"x375\")\n  __typename\n}\n\nfragment CHANNEL_UPDATED_FRAGMENT on Channel {\n  id\n  isFollowed\n  stats {\n    views {\n      total\n      __typename\n    }\n    followers {\n      total\n      __typename\n    }\n    videos {\n      total\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CHANNEL_COMPLETE_FRAGMENT on Channel {\n  id\n  ...CHANNEL_BASE_FRAGMENT\n  ...CHANNEL_IMAGES_FRAGMENT\n  ...CHANNEL_UPDATED_FRAGMENT\n  description\n  coverURL1024x: coverURL(size: \"1024x\")\n  coverURL1920x: coverURL(size: \"1920x\")\n  externalLinks {\n    facebookURL\n    twitterURL\n    websiteURL\n    instagramURL\n    __typename\n  }\n  __typename\n}\n\nfragment CHANNEL_FRAGMENT on Channel {\n  accountType\n  id\n  xid\n  name\n  displayName\n  isArtist\n  logoURL(size: \"x60\")\n  coverURLx375: coverURL(size: \"x375\")\n  isFollowed\n  stats {\n    views {\n      total\n      __typename\n    }\n    followers {\n      total\n      __typename\n    }\n    videos {\n      total\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VIDEO_FRAGMENT on Video {\n  id\n  xid\n  title\n  viewCount\n  duration\n  createdAt\n  isInWatchLater\n  channel {\n    id\n    ...CHANNEL_FRAGMENT\n    __typename\n  }\n  thumbURLx240: thumbnailURL(size: \"x240\")\n  thumbURLx360: thumbnailURL(size: \"x360\")\n  thumbURLx480: thumbnailURL(size: \"x480\")\n  thumbURLx720: thumbnailURL(size: \"x720\")\n  __typename\n}\n\nquery CHANNEL_VIDEOS_QUERY($channel_xid: String!, $sort: String, $page: Int!) {\n  channel(xid: $channel_xid) {\n    id\n    ...CHANNEL_COMPLETE_FRAGMENT\n    channel_videos_all_videos: videos(sort: $sort, page: $page, first: mypagelimit) {\n      pageInfo {\n        hasNextPage\n        nextPage\n        __typename\n      }\n      edges {\n        node {\n          id\n          ...VIDEO_FRAGMENT\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}'
	request = request.replace('mychannelid',id2)
	request = request.replace('mypagelimit','40')
	request = request.replace('mypagenumber',page)
	request = request.replace('mysortmethod',sort)
	html = GET_PAGEDATA(request)
	#DIALOG_OK(str(len(html)),str(html))
	html_blocks = re.findall('"channel_videos_all_videos"(.*?)"VideoConnection"',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('"node".*?"xid": (.*?),.*?"title": (.*?),.*?"duration": (.*?),.*?"name": (.*?),.*?"displayName": (.*?),.*?"thumbURLx240": (.*?),',block,re.DOTALL)
		#DIALOG_OK(str(len(items)),str(items))
		for id,title,duration,ownerID,ownerNAME,img in items:
			if '"' in id: id = id.replace('"','')
			if '"' in title: title = title.replace('"','')
			if '"' in img: img = img.replace('"','')
			if '"' in duration: duration = duration.replace('"','')
			if '"' in ownerID: ownerID = ownerID.replace('"','')
			if '"' in ownerNAME: ownerNAME = ownerNAME.replace('"','')
			link = website0a+'/video/'+id
			title = escapeUNICODE(title)
			owner = ownerID+'::'+ownerNAME
			addMenuItem('video',menu_name+title,link,403,img,duration,owner)
		if '"hasNextPage": true,' in html:
			page = str(int(page)+1)
			addMenuItem('folder',menu_name+'صفحة '+page,url,408,'',page)
	return

def GET_PAGEDATA(request):
	# for testing the json query
	# data = '{"operationName":"BEHAVIOR_QUERY","query":"query BEHAVIOR_QUERY {\n      behavior {\n        matchedFeatures {\n          edges {\n            node {\n              name\n            }\n          }\n        }\n        matchedExperiments {\n          edges {\n            node {\n              id\n              name\n              variation\n            }\n          }\n        }\n      }\n    }"}'
	request = request.replace(' \"',' \\"')
	request = request.replace('\", ','\\", ')
	request = request.replace('\n','\\n')
	request = request.replace('")','\\")')
	authorization = GET_AUTHINTICATION()
	headers = {"Authorization":authorization, "Origin":website0a}
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST',website0b,request,headers,'','','DAILYMOTION-SEARCH_FOR_PLAYLISTS-1st')
	html = response.content
	return html

def GET_AUTHINTICATION():
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',website0a,'','','','','DAILYMOTION-GET_AUTHINTICATION-1st')
	html = response.content
	auth = re.findall('"auth_url":"(.*?)","client_id":"(.*?)","client_secret":"(.*?)"',html,re.DOTALL)
	auth_url,client_id,client_secret = auth[0]
	auth_url = auth_url.replace('\\','')
	grant_type = 'client_credentials'
	cookies = response.cookies.get_dict()
	traffic_segment = cookies['ts']
	data = {'client_id':client_id,'client_secret':client_secret,'grant_type':grant_type,'traffic_segment':traffic_segment}
	headers = {'Content-Type':'application/x-www-form-urlencoded'}
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'POST',auth_url,data,headers,'','','DAILYMOTION-SEARCH-2nd')
	html = response.content
	auth = re.findall('"access_token": "(.*?)".*?"token_type": "(.*?)"',html,re.DOTALL)
	access_token,token_type = auth[0]
	authorization = token_type+" "+access_token
	return authorization

def SEARCH(search,type):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if type=='':
		searchType = ['بحث عن فيديوهات','بحث عن آخر الفيديوهات','بحث عن الفيديوهات الاكثر مشاهدة','(جيد للمسلسلات) بحث عن قوائم تشغيل','بحث عن قنوات']
		selection = DIALOG_SELECT('اختر البحث المناسب:',searchType)
		if selection==-1: return
		elif selection==0: type = 'videos?sortBy='
		elif selection==1: type = 'videos?sortBy=RECENT'
		elif selection==2: type = 'videos?sortBy=VIEW_COUNT'
	elif type=='videos?sortBy=': selection = 0
	elif type=='videos?sortBy=RECENT': selection = 1
	elif type=='videos?sortBy=VIEW_COUNT': selection = 2
	elif type=='playlists': selection = 3
	elif type=='channels': selection = 4
	if search=='':
		if search=='': search = KEYBOARD()
		if search=='': return
	#search = search.replace(' ','%20')
	#search = 'car'
	if   selection in [0,1,2]: SEARCH_FOR_VIDEOS(search+'/'+type)
	elif selection==3: SEARCH_FOR_PLAYLISTS(search)
	elif selection==4: SEARCH_FOR_CHANNELS(search)
	return




