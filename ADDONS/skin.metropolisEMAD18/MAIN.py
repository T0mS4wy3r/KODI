# -*- coding: utf-8 -*-

"""
# -*- coding: utf-8 -*-
from lib.LIBRARY import *

url=''
mode=''
page=''
category=''
text=''
params=get_params()
try: mode=int(params["mode"])
except: pass
try: url=urllib2.unquote(params["url"])
except: pass
try: page=int(params["page"])
except: pass
try: category=params["category"]
except: pass
try: text=params["text"]
except: pass

text=unquote(sys.argv[2])
if 'text=' in text:
	text=text.split('text=')[1]
#if 'url=' in text:
#	text=text.split('url=')[1]

#xbmcgui.Dialog().ok(text,str(mode))

if mode=='': pass
elif mode>=0 and mode<=9: from lib.PROGRAM import MAIN ; MAIN(mode,text)
"""









import sys,urllib2,xbmcgui,unicodedata,xbmc,json


#xbmc.log('EMAD111::EMAD111::'+str(sys.argv), level=xbmc.LOGERROR)


def mixARABIC(string):
	#if '\u' in string:
	#	string = string.decode('unicode_escape')
	#	unicode_strings=re.findall(r'\u[0-9A-F]',string)	
	#	for unicode in unicode_strings
	#		char = unichar(
	#		replace(    , char)
	string = string.decode('utf8')
	new_string = ''
	for letter in string:
		#xbmcgui.Dialog().ok(unicodedata.decomposition(letter),hex(ord(letter)))
		if ord(letter) < 256: unicode_letter = '\u00'+hex(ord(letter)).replace('0x','')
		elif ord(letter) < 4096: unicode_letter = '\u0'+hex(ord(letter)).replace('0x','')
		else: unicode_letter = '\u'+unicodedata.decomposition(letter).split(' ')[1]
		new_string += unicode_letter
	new_string = new_string.replace('\u06CC','\u0649')
	new_string = new_string.decode('unicode_escape')
	new_string = new_string.encode('utf-8')
	return new_string

args = {'mode':'','text':''}
line = sys.argv[2]
if '?' in line:
	params = line[1:].split('&')
	for param in params:
		key,value = param.split('=',1)
		args[key] = value
mode = args['mode']
if mode.isdigit(): mode = int(mode)
text = urllib2.unquote(args['text'])

#xbmcgui.Dialog().ok('args',str(args))

"""
if mode==0 and text!='':
	keyboard = text
	ttype = 'X'
	check = isinstance(keyboard, unicode)
	if check==True: ttype='U'
	new1 = str(type(keyboard))+' '+keyboard+' '+ttype+' '
	for i in range(0,len(keyboard),1):
		new1 += hex(ord(keyboard[i])).replace('0x','')+' '
	keyboard = mixARABIC(keyboard)
	ttype = 'X'
	check = isinstance(keyboard, unicode)
	if check==True: ttype = 'U'
	new2 = str(type(keyboard))+' '+keyboard+' '+ttype+' '
	for i in range(0,len(keyboard),1):
		new2 += hex(ord(keyboard[i])).replace('0x','')+' '
	#xbmcgui.Dialog().ok(new1,new2)
"""


if mode==1 and text!='':
	keyboard = text
	"""
	keyboard = 'emad444'
	json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Input.SendText","params":{"text":"'+keyboard+'","done":false},"id":1}')
	json.loads(json_query)
	#method="Input.SendText"
	#params='{"text":"%s", "done":false}' % keyboard
	#json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "%s", "params": %s, "id": 1}' % (method, params))
	"""
	try:
		#xbmc.log('EMAD333::EMAD333::'+keyboard, level=xbmc.LOGERROR)
		#window_id = xbmcgui.getCurrentWindowDialogId()
		window_id = 10103
		#xbmc.log('EMAD444::EMAD444::'+str(window_id)+'::'+str(type(window_id)), level=xbmc.LOGERROR)
		window = xbmcgui.Window(window_id)
		#xbmc.log('EMAD555::EMAD555::'+str(window), level=xbmc.LOGERROR)
		window.getControl(311).setLabel(keyboard)
		#xbmc.log('EMAD666::EMAD666::'+'DONE', level=xbmc.LOGERROR)
	except: pass

"""
elif mode==2:
	window_id = xbmcgui.getCurrentWindowDialogId()
	window = xbmcgui.Window(window_id)
	url = text
	window.getControl(1112).setLabel(url)
"""


