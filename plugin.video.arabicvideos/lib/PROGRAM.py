# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='PROGRAM'

def MAIN(mode,text=''):
	if (mode==0 or mode==1): FIX_KEYBOARD(mode,text)
	elif mode==2: SEND_MESSAGE()
	elif mode==3: DMCA()
	elif mode==4: HTTPS_TEST()
	elif mode==5: SERVERS_TYPE()
	elif mode==6: GLOBAL_SEARCH()
	elif mode==9: TESTINGS()
	return

def FIX_KEYBOARD(mode,text):
	keyboard=text
	if keyboard=='': return
	if mode==1:
		try:
			window_id = xbmcgui.getCurrentWindowDialogId()
			window = xbmcgui.Window(window_id)
			keyboard = mixARABIC(keyboard)
			window.getControl(311).setLabel(keyboard)
		except: pass
	elif mode==0:
		ttype='X'
		check=isinstance(keyboard, unicode)
		if check==True: ttype='U'
		new1=str(type(keyboard))+' '+keyboard+' '+ttype+' '
		for i in range(0,len(keyboard),1):
			new1 += hex(ord(keyboard[i])).replace('0x','')+' '
		keyboard = mixARABIC(keyboard)
		ttype='X'
		check=isinstance(keyboard, unicode)
		if check==True: ttype='U'
		new2=str(type(keyboard))+' '+keyboard+' '+ttype+' '
		for i in range(0,len(keyboard),1):
			new2 += hex(ord(keyboard[i])).replace('0x','')+' '
		xbmcgui.Dialog().ok(new1,new2)
	return

def SEND_MESSAGE():
	xbmcgui.Dialog().ok('المبرمج لا يعلم الغيب','اذا كانت لديك مشكلة فاذن أقرأ قسم المشاكل والحلول واذا لم تجد الحل هناك فاذن اكتب رسالة عن المكان والوقت والحال الذي تحدث فيه المشكلة واكتب جميع التفاصيل لان المبرمج لا يعلم الغيب')
	xbmcgui.Dialog().ok('عنوان الايميل','اذا كنت تريد ان تسأل وتحتاج جواب من المبرمج فاذن يجب عليك اضافة عنوان البريد الالكتروني email الخاص بك الى رسالتك لانها الطريقة الوحيدة للوصول اليك')
	search = KEYBOARD('Write a message   اكتب رسالة')
	if search == '': return
	message = search
	subject = 'Message: From Arabic Videos'
	result = SEND_EMAIL(subject,message,'yes','','EMAIL-FROM-USERS')

	#	url = 'my API and/or SMTP server'
	#	payload = '{"api_key":"MY API KEY","to":["me@email.com"],"sender":"me@email.com","subject":"From Arabic Videos","text_body":"'+message+'"}'
	#	#auth=("api", "my personal api key"),
	#	#response = requests.request('POST',url, data=payload, headers='', auth='')
	#	response = requests.post(url, data=payload, headers='', auth='')
	#	if response.status_code == 200:
	#		xbmcgui.Dialog().ok('تم الارسال بنجاح','')
	#	else:
	#		xbmcgui.Dialog().ok('خطأ في الارسال','Error {}: {!r}'.format(response.status_code, response.content))

	#	FROMemailAddress = 'me@email.com'
	#	TOemailAddress = 'me@email.com'
	#	header = ''
	#	#header += 'From: ' + FROMemailAddress
	#	#header += '\nTo: ' + emailAddress
	#	#header += '\nCc: ' + emailAddress
	#	header += '\nSubject: من كودي الفيديو العربي'
	#	server = smtplib.SMTP('smtp-server',25)
	#	#server.starttls()
	#	server.login('username','password')
	#	response = server.sendmail(FROMemailAddress,TOemailAddress, header + '\n' + message)
	#	server.quit()
	#	xbmcgui.Dialog().ok('Response',str(response))
	return

def DMCA():
	text = ' نفي: البرنامج لا يوجد له اي سيرفر يستضيف اي محتويات. البرنامج يستخدم روابط وتضمين لمحتويات مرفوعة على سيرفرات خارجية. البرنامج غير مسؤول عن اي محتويات تم تحميلها على سيرفرات ومواقع خارجية "مواقع طرف 3". جميع الاسماء والماركات والصور والمنشورات هي خاصة باصحابها. البرنامج لا ينتهك حقوق الطبع والنشر وقانون الألفية للملكية الرقمية DMCA اذا كان لديك شكوى خاصة بالروابط والتضامين الخارجية فالرجاء التواصل مع ادارة هذه السيرفرات والمواقع الخارجية'
	xbmcgui.Dialog().textviewer('حقوق الطبع والنشر وقانون الألفية للملكية الرقمية',text)
	text = 'Disclaimer: The program does not host any content on any server. The program just use linking to or embedding content that was uploaded to popular Online Video hosting sites. All trademarks, Videos, trade names, service marks, copyrighted work, logos referenced herein belong to their respective owners/companies. The program is not responsible for what other people upload to 3rd party sites. We urge all copyright owners, to recognize that the links contained within this site are located somewhere else on the web or video embedded are from other various site. If you have any legal issues please contact appropriate media file owners/hosters.'
	xbmcgui.Dialog().textviewer('Digital Millennium Copyright Act (DMCA)',text)
	return

def HTTPS_TEST():
	html = openURL('https://www.google.com','','','','PROGRAM-1st')
	#xbmcgui.Dialog().ok('Checking SSL',html)
	if 'html' in html:
		xbmcgui.Dialog().ok('الاتصال المشفر','جيد جدا ... الاتصال المشفر (الربط المشفر) يعمل على جهازك ... وجهازك قادر على استخدام المواقع المشفرة')
	else:
		xbmcgui.Dialog().ok('الاتصال المشفر','مشكلة ... الاتصال المشفر (الربط المشفر) لا يعمل على جهازك ... وجهازك غير قادر على استخدام المواقع المشفرة')
		from PROBLEMS import MAIN as PROBLEMS_MAIN
		PROBLEMS_MAIN(1002)
	return

def SERVERS_TYPE():
	text = 'السيرفرات العامة هي سيرفرات خارجية وغير جيدة لان الكثير منها ممنوع او محذوف او خطأ بسبب حقوق الطبع وحقوق الالفية الرقمية ولا توجد طريقة لفحصها او اصلاحها \n\n السيرفرات الخاصة هي سيرفرات يتحكم فيها الموقع الاصلي وهي جيدة نسبيا ولا توجد طريقة لفحصها او اصلاحها \n\n الرجاء قبل الاعتراض على السيرفرات وقبل مراسلة المبرمج افحص الفيديو والسيرفر على الموقع الاصلي'
	xbmcgui.Dialog().textviewer('مواقع تستخدم سيرفرات عامة',text)
	return

def GLOBAL_SEARCH():
	search = KEYBOARD()
	if search == '': return
	addDir('1.  [COLOR FFC89008]SHF  [/COLOR]'+'موقع شوف ماكس','',59,'','','',search)
	addDir('2.  [COLOR FFC89008]EGB  [/COLOR]'+'موقع ايجي بيست','',129,'','','',search)
	addDir('3.  [COLOR FFC89008]KLA  [/COLOR]'+'موقع كل العرب','',19,'','','',search)
	addDir('4.  [COLOR FFC89008]PNT  [/COLOR]'+'موقع بانيت','',39,'','','',search)
	addDir('5.  [COLOR FFC89008]IFL    [/COLOR]'+'موقع قناة اي فيلم','',29,'','','',search)
	addDir('6.  [COLOR FFC89008]KWT  [/COLOR]'+'موقع قناة الكوثر','',139,'','','',search)
	addDir('7.  [COLOR FFC89008]MRF  [/COLOR]'+'موقع قناة المعارف','',49,'','','',search)
	addDir('8.  [COLOR FFC89008]FTM  [/COLOR]'+'موقع المنبر الفاطمي','',69,'','','',search)
	addDir('=========================','',9999)
	addDir('9.   [COLOR FFC89008]AKM  [/COLOR]'+'موقع اكوام','',79,'','','',search)
	addDir('10.  [COLOR FFC89008]HEL  [/COLOR]'+'موقع هلال يوتيوب','',99,'','','',search)
	addDir('=========================','',9999)
	addDir('11.  [COLOR FFC89008]SHA  [/COLOR]'+'موقع شاهد فوريو','',119,'','','',search)
	addDir('12.  [COLOR FFC89008]HLA  [/COLOR]'+'موقع هلا سيما','',89,'','','',search)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TESTINGS():
	#import xbmcaddon
	#settings = xbmcaddon.Addon(id=addon_id)
	#settings.setSetting('test1','hello test1')
	#var = settings.getSetting('test2')
	#xbmc.log('EMAD11 ' + str(var) + ' 11EMAD',level=xbmc.LOGNOTICE)
	#import subprocess
	#var = subprocess.check_output('wmic csproduct get UUID')
	#xbmc.log('EMAD11 ' + str(var) + ' 11EMAD',level=xbmc.LOGNOTICE)
	#import os
	#var = os.popen("wmic diskdrive get serialnumber").read()
	#xbmc.log('EMAD11 ' + str(var) + ' 11EMAD',level=xbmc.LOGNOTICE)

	#import requests
	#var = dummyClientID(32)
	#xbmcgui.Dialog().ok(var,'')
	#xbmc.log('EMAD11' + html + '11EMAD',level=xbmc.LOGNOTICE)
	url = ''
	urllist = [
		''
		]

	#play_item = xbmcgui.ListItem(path=url, thumbnailImage='')
	#play_item.setInfo(type="Video", infoLabels={"Title":''})
	# Pass the item to the Kodi player.
	#xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	# directly play the item.
	#xbmc.Player().play(url, play_item) 

	#import RESOLVERS
	#url = RESOLVERS.PLAY(urllist,script_name,'no')



	#PLAY_VIDEO(url,script_name,'yes')
	return
