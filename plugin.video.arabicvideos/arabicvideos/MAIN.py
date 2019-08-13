# -*- coding: utf-8 -*-
from LIBRARY import *


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

newline = '\r                               '
message = '[ '+addon_id+' ]'
message += newline+'Version:[ '+addonVersion+' ]'
message += newline+'Kodi:[ '+kodiVersion+' ]'
message += newline+'Label:[ '+menulabel+' ]'
message += newline+'Path:[ '+menupath+' ]'
xbmc.log(message, level=xbmc.LOGNOTICE)


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


args = { 'mode':-1 , 'url':'' , 'text':'' , 'page':'' }
line = sys.argv[2]
if '?' in line:
	params = line[1:].split('&')
	for param in params:
		key,value = param.split('=',1)
		args[key] = value
mode=int(args['mode'])
url=urllib2.unquote(args['url'])
text=urllib2.unquote(args['text'])
page=urllib2.unquote(args['page'])
#xbmcgui.Dialog().ok('args',str(args))


if mode==-1:
	#addLink('Testing - watched enabled','',179,'','','yes','','','IsPlayable=yes')
	#addLink('Testing - watched disabled','',179,'','','no','','','IsPlayable=no')
	addDir('[COLOR FFC89008] 1.  [/COLOR]'+'لماذا لا تعمل جميع المواقع','',195)
	#addDir('[COLOR FFC89008] 2.  [/COLOR]'+'ـ Services Menu  قائمة الخدمات','',172)
	addDir('[COLOR FFC89008]ـ Services Menu  قائمة الخدمات  .2 [/COLOR]','',172)
	addLink('[COLOR FFC89008]'+' البرنامج اصدار رقم ('+addonVersion+')  .3 [/COLOR]','',7,'','','IsPlayable=no')
	addDir('[COLOR FFC89008] 4.  [/COLOR]'+'قنوات تلفزونية وبث حي','',170)
	addDir('[COLOR FFC89008] 5.  [/COLOR]'+'بحث بجميع مواقع البرنامج','',6)
	addDir('[COLOR FFC89008] 6.  [/COLOR]'+'مشاهدة فيدوهات عشوائية','',8)
	addLink('[COLOR FFC89008]مواقع سيرفرات خاصة - قليلة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir(' 7.  [COLOR FFC89008]YUT  [/COLOR]'+'موقع يوتيوب','',140)
	addDir(' 8.  [COLOR FFC89008]SHF  [/COLOR]'+'موقع شوف ماكس','',50)
	addDir(' 9.  [COLOR FFC89008]KLA  [/COLOR]'+'موقع كل العرب','',10)
	addDir('10. [COLOR FFC89008]PNT  [/COLOR]'+'موقع بانيت','',30)
	addDir('11. [COLOR FFC89008]EG4  [/COLOR]'+'موقع ايجي فور بيست','',220)    # 220
	addDir('12. [COLOR FFC89008]IFL    [/COLOR]'+'موقع قناة اي فيلم','',20)
	addDir('13. [COLOR FFC89008]MRF  [/COLOR]'+'موقع قناة المعارف','',40)
	addDir('14. [COLOR FFC89008]KWT  [/COLOR]'+'موقع قناة الكوثر','',130)
	addDir('15. [COLOR FFC89008]FTM  [/COLOR]'+'موقع المنبر الفاطمي','',60)
	addLink('[COLOR FFC89008]مواقع سيرفرات خاصة وعامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('16. [COLOR FFC89008]MVZ  [/COLOR]'+'موقع موفيزلاند اونلاين','',180)
	addDir('17. [COLOR FFC89008]AKM  [/COLOR]'+'موقع اكوام','',70)
	addDir('18. [COLOR FFC89008]EGB  [/COLOR]'+'موقع ايجي بيست','',120)    # 5
	addLink('[COLOR FFC89008]مواقع سيرفرات عامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('19. [COLOR FFC89008]HEL  [/COLOR]'+'موقع هلال يوتيوب','',90)
	addDir('20. [COLOR FFC89008]HLA  [/COLOR]'+'موقع هلا سيما','',80)
	addDir('21. [COLOR FFC89008]SHA  [/COLOR]'+'موقع شاهد فوريو','',110)
	addDir('22. [COLOR FFC89008]ARL   [/COLOR]'+'موقع عرب ليونز','',200)
	addDir('23. [COLOR FFC89008]SFW  [/COLOR]'+'موقع سيريس فور وتش','',210)
	#addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	xbmcplugin.endOfDirectory(addon_handle)


elif mode>=0 and mode<=9: import PROGRAM ; PROGRAM.MAIN(mode,text)
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
elif mode>=150 and mode<=159: import PROBLEMS ; PROBLEMS.MAIN(mode)
elif mode>=160 and mode<=169: import RESOLVERS ; RESOLVERS.MAIN(mode,url,text)
elif mode>=170 and mode<=179: import PROGRAM ; PROGRAM.MAIN(mode,text)
elif mode>=180 and mode<=189: import MOVIZLAND ; MOVIZLAND.MAIN(mode,url,text)
elif mode>=190 and mode<=199: import PROBLEMS ; PROBLEMS.MAIN(mode)
elif mode>=200 and mode<=209: import ARABLIONZ ; ARABLIONZ.MAIN(mode,url,text)
elif mode>=210 and mode<=219: import SERIES4WATCH ; SERIES4WATCH.MAIN(mode,url,text)
elif mode>=220 and mode<=229: import EGY4BEST ; EGY4BEST.MAIN(mode,url,page,text)


"""
worked,result = True,''
if mode in [10,50,70,80,90,110,120,140,180,19,59,79,89,99,119,129,149,189]:
	worked = HTTPS(False)
	if not worked:
		xbmcgui.Dialog().ok('هذا الموقع لا يعمل عندك لانه مشفر','جرب موقع غير مشفر')
		import PROBLEMS
		PROBLEMS.MAIN(152)

#if worked:
"""


#t2 =time.time()
#if menulabel=='Main Menu':
#	xbmcgui.Dialog().ok('main menu took',str(int(t2-t1))+' ms')


#xbmcgui.Dialog().ok('main exit','')


#if label!='':
#if addon_handle > -1:
#xbmcplugin.endOfDirectory(addon_handle)
#xbmc.Player().play()

#xbmc.log('[ '+addon_id+' ]:   Finished menu item   Label:[ '+menulabel+' ]   Path:[ '+menupath+' ]', level=xbmc.LOGNOTICE)




"""
t1=time.time()
a,b = TEST_HTTPS_PROXIES()
t2=time.time()
xbmcgui.Dialog().ok('testing all proxies',str(t2-t1))
"""



"""
ip = RESOLVE_DNS('emad123.com')
xbmcgui.Dialog().ok(str(ip),'111')

#url = 'http://www.google.com||MyDNSUrl='
url = 'http://emad123.com'
headers = { 'User-Agent' : '' }
html = openURL(url,'',headers,'','')
xbmcgui.Dialog().ok(str(len(html)),html)
"""


