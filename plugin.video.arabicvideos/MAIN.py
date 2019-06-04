# -*- coding: utf-8 -*-
from lib.LIBRARY import *

label = xbmc.getInfoLabel('ListItem.Label').replace('[COLOR FFC89008]','').replace('[/COLOR]','')
if label=='': label = 'Main menu'
addonVersion = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
kodiVersion = xbmc.getInfoLabel( "System.BuildVersion" )	
xbmc.log('['+addon_id+']:  Version:['+addonVersion+']   Kodi:['+kodiVersion+']', level=xbmc.LOGNOTICE)
#addon_path = xbmc.getInfoLabel( "ListItem.FolderPath" )
path = unquote(addon_path)
xbmc.log('['+addon_id+']:  Starting menu item:  Label:['+label+']   Path:['+path+']', level=xbmc.LOGNOTICE)

def MAIN():
	#addLink('Testing - watched enabled','',179,'','','yes','','','IsPlayable=yes')
	#addLink('Testing - watched disabled','',179,'','','no','','','IsPlayable=no')

	addLink('ابلاغ المبرمج عن مشكلة'+'  .1','',2,'','','IsPlayable=no,problem=yes')
	addLink('فحص الاصدار الاخير والتحديثات'+'  .2','',7,'','','IsPlayable=no')
	addDir('بحث في جميع مواقع البرنامج'+'  .3','',6)
	addDir('مشاهدة فيدوهات عشوائية'+'  .4','',8)
	addLink('=========================','',9999,'','','IsPlayable=no')

	addLink('[COLOR FFC89008]مواقع سيرفرات خاصة - قليلة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('5.  [COLOR FFC89008]YUT  [/COLOR]'+'موقع يوتيوب (مشفر)','',140)
	addDir('6.  [COLOR FFC89008]SHF  [/COLOR]'+'موقع شوف ماكس (مشفر)','',50)
	addDir('7.  [COLOR FFC89008]EGB  [/COLOR]'+'موقع ايجي بيست (مشفر)','',5)  #120
	addDir('8.  [COLOR FFC89008]KLA   [/COLOR]'+'موقع كل العرب (مشفر)','',10)
	addDir('9.  [COLOR FFC89008]PNT   [/COLOR]'+'موقع بانيت','',30)
	addDir('10. [COLOR FFC89008]IFL     [/COLOR]'+'موقع قناة اي فيلم','',20)
	addDir('11. [COLOR FFC89008]KWT  [/COLOR]'+'موقع قناة الكوثر','',130)
	addDir('12. [COLOR FFC89008]MRF  [/COLOR]'+'موقع قناة المعارف','',40)
	addDir('13. [COLOR FFC89008]FTM  [/COLOR]'+'موقع المنبر الفاطمي','',60)
	addLink('=========================','',9999,'','','IsPlayable=no')

	addLink('[COLOR FFC89008]مواقع سيرفرات خاصة وعامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('14.  [COLOR FFC89008]MVZ   [/COLOR]'+'موقع موفيزلاند اونلاين','',180)
	addDir('15.  [COLOR FFC89008]AKM  [/COLOR]'+'موقع اكوام (مشفر)','',70)
	addDir('16.  [COLOR FFC89008]HEL   [/COLOR]'+'موقع هلال يوتيوب (مشفر)','',90)
	addLink('=========================','',9999,'','','IsPlayable=no')

	addLink('[COLOR FFC89008]مواقع سيرفرات عامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addDir('17.  [COLOR FFC89008]SHA   [/COLOR]'+'موقع شاهد فوريو (مشفر)','',110)
	addDir('18.  [COLOR FFC89008]HLA   [/COLOR]'+'موقع هلا سيما (مشفر)','',80)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')

	addDir('19.  [COLOR FFC89008]TV1   [/COLOR]'+'قنوات تلفزونية','',100)
	addDir('20.  [COLOR FFC89008]TV2   [/COLOR]'+'قنوات تلفزونية خاصة','',101)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')

	addLink('ـMessage to developer    رسالة الى المبرمج'+'  .21','',2,'','','IsPlayable=no,problem=no')
	addDir('ـProblems & Solutions    مشاكل وحلول'+'  .22','',150)
	addLink('ـ DMCA     قانون الألفية للملكية الرقمية'+'  .23','',3,'','','IsPlayable=no')
	addLink('فحص الاتصال بالمواقع المشفرة'+'  .24','',4,'','','IsPlayable=no')
	xbmcplugin.endOfDirectory(addon_handle)
	return ''

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

url=''
mode=''
page=''
text=''
params=get_params()
try: mode=int(params["mode"])
except: pass
try: url=urllib2.unquote(params["url"])
except: pass
try: page=urllib2.unquote(params["page"])
except: pass
try: text=urllib2.unquote(params["text"])
except: pass

result = ''

if not mode: MAIN()
elif mode>=0 and mode<=9: from lib.PROGRAM import MAIN ; MAIN(mode,text)
elif mode>=10 and mode<=19: from lib.ALARAB import MAIN ; MAIN(mode,url,text)
elif mode>=20 and mode<=29: from lib.IFILM import MAIN ; MAIN(mode,url,page,text)
elif mode>=30 and mode<=39: from lib.PANET import MAIN ; MAIN(mode,url,page,text)
elif mode>=40 and mode<=49: from lib.ALMAAREF import MAIN ; MAIN(mode,url,text)
elif mode>=50 and mode<=59: from lib.SHOOFMAX import MAIN ; MAIN(mode,url,text)
elif mode>=60 and mode<=69: from lib.ALFATIMI import MAIN ; MAIN(mode,url,text)
elif mode>=70 and mode<=79: from lib.AKOAM import MAIN ; MAIN(mode,url,text)
elif mode>=80 and mode<=89: from lib.HALACIMA import MAIN ; MAIN(mode,url,page,text)
elif mode>=90 and mode<=99: from lib.HELAL import MAIN ; MAIN(mode,url,text)
elif mode>=100 and mode<=109: from lib.TV import MAIN ; MAIN(mode,url)
elif mode>=110 and mode<=119: from lib.SHAHID4U import MAIN ; MAIN(mode,url,text)
elif mode>=120 and mode<=129: from lib.EGYBEST import MAIN ; MAIN(mode,url,page,text)
elif mode>=130 and mode<=139: from lib.ALKAWTHAR import MAIN ; MAIN(mode,url,page,text)
elif mode>=140 and mode<=149: from lib.YOUTUBE import MAIN ; result = MAIN(mode,url,text)
elif mode>=150 and mode<=159: from lib.PROBLEMS import MAIN ; MAIN(mode)
elif mode>=160 and mode<=169: from lib.RESOLVERS import MAIN ; MAIN(mode,url,text)
elif mode>=170 and mode<=179: from lib.PROGRAM import MAIN ; MAIN(mode,text)
elif mode>=180 and mode<=189: from lib.MOVIZLAND import MAIN ; MAIN(mode,url,text)



#if label!='':
#if addon_handle > -1:
#xbmcplugin.endOfDirectory(addon_handle)
#xbmc.Player().play()
#xbmcgui.Dialog().ok('النتيجة',result)

#xbmc.log('['+addon_id+']:  Result:  '+result, level=xbmc.LOGNOTICE)
#xbmc.log('['+addon_id+']:  Finished menu item:  Label:['+label+']   Path:['+path+']', level=xbmc.LOGNOTICE)
