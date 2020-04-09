# -*- coding: utf-8 -*-
from LIBRARY import *


script_name = 'MAIN'


LOG_THIS('NOTICE','============================================================================================')


if 'mode' not in addon_path:
	message = 'Version: [ '+addon_version+' ]   Kodi: [ '+kodi_version+' ]'
	#message += '\n'+'Label:['+menu_label+']   Path:['+menu_path+']'
	LOG_THIS('NOTICE',LOGGING(script_name)+'   '+message)


#t1 =time.time()

#response = openURL_requests('GET','http://example.com||MyDNSUrl=')
#html = response.text
#xbmcgui.Dialog().ok('',str(html))
#html = openURL('http://example.com||MyProxyUrl=http://198.50.147.158:3128')
#xbmcgui.Dialog().ok('',str(html))
#html = openURL('http://example.com||MyProxyUrl=')
#xbmcgui.Dialog().ok('',str(html))
#xbmcgui.Dialog().ok('','shutdown the proxy')
#html = openURL('https://google.com||MyDNSUrl=')
#xbmcgui.Dialog().ok('',str(html))
#html = openURL('http://google.com')
#xbmcgui.Dialog().ok('',str(html))



#DELETE_DATABASE_FILES()
if not os.path.exists(addoncachefolder):
	os.makedirs(addoncachefolder)
if not os.path.exists(dbfile):
	DELETE_DATABASE_FILES()
	newdb = True
else: newdb = False


conn = sqlite3.connect(dbfile)
c = conn.cursor()
if newdb:
	c.execute('PRAGMA auto_vacuum = FULL')
	c.execute('CREATE TABLE htmlcache (expiry,url,data,headers,source,html)')
	c.execute('CREATE TABLE responsecache (expiry,url,data,headers,allow_redirects,source,response)')
	c.execute('CREATE TABLE serverscache (expiry,linkLIST,serversLIST,urlLIST)')
else:
	c.execute('DELETE FROM htmlcache WHERE expiry<'+str(now))
	c.execute('DELETE FROM responsecache WHERE expiry<'+str(now))
	c.execute('DELETE FROM serverscache WHERE expiry<'+str(now))
conn.commit()
conn.close()


if newdb:# or 1==1:
	import SERVICES
	SERVICES.KODI_SKIN()
	allFiles = str(os.listdir(addoncachefolder))
	if 'iptv_' in allFiles and '_.streams' in allFiles:
		xbmcgui.Dialog().ok('IPTV','تم مسح الكاش أو تم تحديث البرنامج فاذا كنت تستخدم خدمة IPTV فاذن انت تحتاج ان تجلب ملفات IPTV جديدة')
		import IPTV
		IPTV.CREATE_ALL_FILES()


args = { 'mode':'MAIN_MENU' , 'url':'' , 'text':'' , 'page':'' }
line = addon_path
if '?' in line:
	params = line[1:].split('&')
	for param in params:
		key,value = param.split('=',1)
		args[key] = value
mode = args['mode']
if mode.isdigit(): mode = int(mode)
url = urllib2.unquote(args['url'])
text = urllib2.unquote(args['text'])
page = urllib2.unquote(args['page'])
#xbmcgui.Dialog().ok('args',str(args))


if mode=='MAIN_MENU':
	#addLink('Testing - watched enabled','',179,'','','IsPlayable=yes')
	#addLink('Testing - watched disabled','',179,'','','IsPlayable=no')
	addDir(' [COLOR FFC89008] 1.  [/COLOR]'+'للتواصل مع المبرمج','',196)
	addDir(' [COLOR FFC89008] 2.  [/COLOR]'+'تقرير عن استخدام البرنامج','',176)
	addDir(' [COLOR FFC89008] 3.  [/COLOR]'+'لماذا بعض المواقع لا تعمل','',195)
	#addDir('[COLOR FFC89008] 2.  [/COLOR]'+'ـ Services Menu  قائمة الخدمات','',172)
	addDir(' [COLOR FFC89008]ـ Services Menu  قائمة الخدمات  .4 [/COLOR]','',150)
	addLink(' [COLOR FFC89008]'+' البرنامج اصدار رقم ('+addon_version+')  .5 [/COLOR]','',7,'','','IsPlayable=no')
	addDir(' [COLOR FFC89008] 6.  [/COLOR]'+'قنوات تلفزونية وبث حي','',170)
	addDir(' [COLOR FFC89008] 7.  [/COLOR]'+'بحث بجميع مواقع البرنامج','',6)
	addDir(' [COLOR FFC89008] 8.  [/COLOR]'+'مشاهدة فيدوهات عشوائية','',8)
	addLink('  [COLOR FFC89008]مواقع سيرفرات خاصة - قليلة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('  9.  [COLOR FFC89008]IFL    [/COLOR]'+'موقع قناة اي فيلم','',20)
	addDir('10.  [COLOR FFC89008]MRF  [/COLOR]'+'موقع قناة المعارف','',40)
	addDir('11.  [COLOR FFC89008]KWT  [/COLOR]'+'موقع قناة الكوثر','',130)
	addDir('12.  [COLOR FFC89008]FTM  [/COLOR]'+'موقع المنبر الفاطمي','',60)
	addDir('13.  [COLOR FFC89008]IPT    [/COLOR]'+'خدمة IPTV','',230)
	addDir('14.  [COLOR FFC89008]YUT  [/COLOR]'+'موقع يوتيوب','',140)
	addDir('15.  [COLOR FFC89008]KLA  [/COLOR]'+'موقع كل العرب','',10)
	addDir('16.  [COLOR FFC89008]PNT  [/COLOR]'+'موقع بانيت','',30)
	addDir('17.  [COLOR FFC89008]SHF  [/COLOR]'+'موقع شوف ماكس','',50)
	addDir('18.  [COLOR FFC89008]AKW [/COLOR]'+'موقع أكوام الجديد','',240)
	addLink('[COLOR FFC89008]مواقع سيرفرات خاصة وعامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('19.  [COLOR FFC89008]AKO  [/COLOR]'+'موقع أكوام القديم','',70)
	addDir('20.  [COLOR FFC89008]EG4  [/COLOR]'+'موقع ايجي فور بيست','',220)    # 220
	addDir('21.  [COLOR FFC89008]ARS  [/COLOR]'+'موقع عرب سييد','',250)
	addLink('[COLOR FFC89008]مواقع سيرفرات عامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('22.  [COLOR FFC89008]HEL  [/COLOR]'+'موقع هلال يوتيوب','',90)
	addDir('23.  [COLOR FFC89008]SHA  [/COLOR]'+'موقع شاهد فوريو','',110)
	addDir('24.  [COLOR FFC89008]ARL   [/COLOR]'+'موقع عرب ليونز','',200)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	#addDir('25.  [COLOR FFC89008]HLA  [/COLOR]'+'موقع هلا سيما','',88) # 80
	#addDir('26.  [COLOR FFC89008]SFW  [/COLOR]'+'موقع سيريس فور وتش','',218)  # 210
	#addDir('27.  [COLOR FFC89008]MVZ  [/COLOR]'+'موقع موفيزلاند اونلاين','',188) # 180
	#addDir('28.  [COLOR FFC89008]EGB  [/COLOR]'+'موقع ايجي بيست','',128) # 120
	xbmcplugin.endOfDirectory(addon_handle)

elif mode>=0 and mode<=9: import SERVICES ; SERVICES.MAIN(mode,text)
elif mode>=10 and mode<=19: import ALARAB ; ALARAB.MAIN(mode,url,text)
elif mode>=20 and mode<=29: import IFILM ; IFILM.MAIN(mode,url,page,text)
elif mode>=30 and mode<=39: import PANET ; PANET.MAIN(mode,url,page,text)
elif mode>=40 and mode<=49: import ALMAAREF ; ALMAAREF.MAIN(mode,url,text)
elif mode>=50 and mode<=59: import SHOOFMAX ; SHOOFMAX.MAIN(mode,url,text)
elif mode>=60 and mode<=69: import ALFATIMI ; ALFATIMI.MAIN(mode,url,text)
elif mode>=70 and mode<=79: import AKOAM ; AKOAM.MAIN(mode,url,text)
elif mode>=80 and mode<=89: import HALACIMA ; HALACIMA.MAIN(mode,url,page,text)
elif mode>=90 and mode<=99: import HELAL ; HELAL.MAIN(mode,url,text)
elif mode>=100 and mode<=109: import LIVETV ; LIVETV.MAIN(mode,url)
elif mode>=110 and mode<=119: import SHAHID4U ; SHAHID4U.MAIN(mode,url,text)
elif mode>=120 and mode<=129: import EGYBEST ; EGYBEST.MAIN(mode,url,page,text)
elif mode>=130 and mode<=139: import ALKAWTHAR ; ALKAWTHAR.MAIN(mode,url,page,text)
elif mode>=140 and mode<=149: import YOUTUBE ; result = YOUTUBE.MAIN(mode,url,text)
elif mode>=150 and mode<=159: import SERVICES ; SERVICES.MAIN(mode)
elif mode>=160 and mode<=169: import RESOLVERS ; RESOLVERS.MAIN(mode,url,text)
elif mode>=170 and mode<=179: import SERVICES ; SERVICES.MAIN(mode,text)
elif mode>=180 and mode<=189: import MOVIZLAND ; MOVIZLAND.MAIN(mode,url,text)
elif mode>=190 and mode<=199: import SERVICES ; SERVICES.MAIN(mode)
elif mode>=200 and mode<=209: import ARABLIONZ ; ARABLIONZ.MAIN(mode,url,text)
elif mode>=210 and mode<=219: import SERIES4WATCH ; SERIES4WATCH.MAIN(mode,url,text)
elif mode>=220 and mode<=229: import EGY4BEST ; EGY4BEST.MAIN(mode,url,page,text)
elif mode>=230 and mode<=239: import IPTV ; IPTV.MAIN(mode,url,text)
elif mode>=240 and mode<=249: import AKWAM ; AKWAM.MAIN(mode,url,text)
elif mode>=250 and mode<=259: import ARABSEED ; ARABSEED.MAIN(mode,url,text)


#xbmc.log('99  11', level=xbmc.LOGNOTICE)

#if addon_handle > -1:
#	xbmcplugin.endOfDirectory(addon_handle)

#xbmc.Player().play()
#raise SystemExit
#try: xbmcplugin.endOfDirectory(addon_handle)
#except: pass
#sys.exit(0)


#if mode==1:
#	xbmcplugin.endOfDirectory(addon_handle)


#xbmc.log('AA  11', level=xbmc.LOGNOTICE)


"""
worked,result = True,''
if mode in [10,50,70,80,90,110,120,140,180,19,59,79,89,99,119,129,149,189]:
	worked = HTTPS(False)
	if not worked:
		xbmcgui.Dialog().ok('هذا الموقع لا يعمل عندك لانه مشفر','جرب موقع غير مشفر')
		import SERVICES
		SERVICES.MAIN(152)

#if worked:
"""


#t2 =time.time()
#if menu_label=='Main Menu':
#	xbmcgui.Dialog().ok('main menu took',str(int(t2-t1))+' ms')


#xbmcgui.Dialog().ok('main exit','')


#if label!='':
#if addon_handle > -1:
#xbmcplugin.endOfDirectory(addon_handle)
#xbmc.Player().play()

#xbmc.log(LOGGING(script_name)+'   Finished menu item   Label:['+menu_label+']   Path:['+menu_path+']', level=xbmc.LOGNOTICE)








