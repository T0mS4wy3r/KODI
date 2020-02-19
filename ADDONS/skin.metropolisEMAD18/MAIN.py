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



