# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='PROGRAM'

def MAIN(mode,text=''):
	if (mode==0 or mode==1):
		keyboard=text
		if keyboard=='': return
		if mode==1:
			window_id = xbmcgui.getCurrentWindowDialogId()
			window = xbmcgui.Window(window_id)
			keyboard = mixARABIC(keyboard)
			window.getControl(311).setLabel(keyboard)
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
	elif mode==2:
		#xbmcgui.Dialog().ok('step3',text)
		window_id = xbmcgui.getCurrentWindowDialogId()
		window = xbmcgui.Window(window_id)
		url=text
		window.getControl(1112).setLabel(url)
	return
