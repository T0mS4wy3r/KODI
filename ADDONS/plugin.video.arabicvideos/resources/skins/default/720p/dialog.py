# -*- coding: utf-8 -*-
from LIBRARY import *


text1 = 'test 1234 test 1234 test 1234 test 1234 test 1234'
text2 = 'test 1234 test 1234 test \r\n 1234 test 1234 test 1234\r\n test'
text2 = text2+text2

dialog = xbmcgui.WindowXMLDialog('DialogTextViewer22.xml', xbmcaddon.Addon().getAddonInfo('path').decode('utf-8'), 'Default', '720p')
dialog.show()
dialog.getControl(1).setLabel(text1)
dialog.getControl(5).setText(text2)


height = xbmcgui.getScreenHeight()
width = xbmcgui.getScreenWidth()
#XBMCGUI_DIALOG_OK(str(height),str(width))

dialog.getControl(99991).setPosition(0,0)




#control = dialog.getFocusId()
#control.setPosition(200,200)
#dialog.getControl(control).setPosition(200,200)


#dialog.doModal()
#dialog.getControl(61).setPosition(0,0)


#dialog.getControl(99961).setPosition(0,0)
#dialog.getControl(99961).setWidth(width)
#dialog.getControl(61).setHeight(height-40)



dialog.doModal()
del dialog





"""
#height = xbmc.getInfoLabel('System.ScreenHeight')
#width = xbmc.getInfoLabel('System.ScreenWidth')
#XBMCGUI_DIALOG_OK(str(height),str(width))


#dialog.getControl(99991).setWidth(width)
#dialog.getControl(99991).setHeight(height)


window = xbmcgui.Window(10147)
control_1 = xbmcgui.ControlTextBox(20,20,width-40, height-40, textColor='0xFFFFFF00')
control_2 = xbmcgui.ControlLabel(0, 0, 1080, 720, textColor='0xFFFFFFFF',label='11 22 33 44')
window.addControl(control_1)
window.addControl(control_2)
window.show()
window.doModal()
"""


from LIBRARY import *

#MAIN()

#sys.exit(0)

#import TEST

#XBMCGUI_DIALOG_OK(str('__init__'),str(''))

#window = xbmcgui.WindowXMLDialog('DialogKeyboard22.xml',addonfolder,'default','720p')

#id = xbmcgui.getCurrentWindowId()
#XBMCGUI_DIALOG_OK('window id',str(id))





class MyWindow(xbmcgui.WindowXMLDialog):

	def onInit(self):
		self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
		self.window.setProperty('MyAddonIsRunning', 'true')

	def onClick(self, controlId):
		LOG_THIS('NOTICE','EMAD EMAD KEY: '+str(controlId))
		#XBMCGUI_DIALOG_OK("test", controlId.__str__())
		if controlId == 300:
			self.close()

tb = MyWindow("DialogKeyboard22.xml",addonfolder,'default','720')
tb.doModal()
del tb


sys.exit()



"""
window = xbmcgui.Window(xbmcgui.getCurrentWindowId())

for i in range(5):
	if window.getProperty('MyAddonIsRunning') != 'true':
		mydisplay = MyWindow()
		mydisplay .doModal()
		del mydisplay
		window.setProperty('MyAddonIsRunning', 'false')
		break
	time.sleep(1)
"""
	
	
	




"""
class MyWindow(xbmcgui.Window):
    def __init__(self):
        self = xbmcgui.Window(10103)

    def onClick( self, controlId ):            
        LOG_THIS('NOTICE','EMAD EMAD '+str(controlId)+': '+str(controlId.__str__()))
		#XBMCGUI_DIALOG_OK("test", controlId.__str__())

window = MyWindow()
window.show()
#window.getControl(101).setLabel('a')

for i in range(5):
	#key = window.onClick(101)
	time.sleep(1)
"""
	

"""
window.show()
window.getControl(101).setLabel('a')
window.getControl(102).setLabel('b')
window.getControl(103).setLabel('c')
window.getControl(104).setLabel('d')
window.getControl(312).setLabel('test')
window.getControl(311).setLabel('1234')
window.getControl(300).setLabel('Enter')

window.setProperty('status','test')

#win = xbmcgui.Window(xbmcgui.getCurrentWindowId())

#window.doModal()
#time.sleep(5)
#window.close()

for i in range(10):
	key = window.onClick(101)
	LOG_THIS('NOTICE','EMAD EMAD '+str(i)+': '+str(key))
	time.sleep(1)
"""



"""
time.sleep(5)


win2 = win.getProperty('status')


new1 = window.getProperty('status')

XBMCGUI_DIALOG_OK(new1,win2)
"""

#new1 = window.getControl(300).getLabel()


#while True: time.sleep(1)

#for i in range(5):	time.sleep(1)


#window2 = xbmcgui.Window(909090)
#new2 = window2.getControl(300).getLabel()



"""
for i in range(10):
	status = window.getControl(300).getLabel()
	LOG_THIS('NOTICE','EMAD EMAD '+str(status))
	if status!='running':
		XBMCGUI_DIALOG_OK('worked','')
		break
	#if window.isConfirmed(): text = window.getText()
	time.sleep(1)
"""

#id = xbmcgui.getCurrentWindowId()
#XBMCGUI_DIALOG_OK('window id',str(id))


#LOG_THIS('NOTICE','EMAD EMAD WIDNOW EXIT')

#text = window.getControl(312).getLabel()

#XBMCGUI_DIALOG_OK('failed','')



#window = xbmcgui.WindowXMLDialog('DialogKeyboard22.xml',addonfolder,'default','720p')

#id = xbmcgui.getCurrentWindowId()
#XBMCGUI_DIALOG_OK('window id',str(id))



#textbox = xbmcgui.ControlTextBox(100, 250, 300, 300, textColor='0xFFFFFFFF')
#window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
#window.addControl(textbox)
#textbox.setText("My Text Box")
#textbox.scroll()






#win = xbmcgui.WindowDialog(10103)
#win = xbmcgui.Window(10103)
#win.doModal()
#time.sleep(5)
#sys.exit()





class MyWindow(xbmcgui.WindowXMLDialog):
	def onClick(self, controlId):
		LOG_THIS('NOTICE','EMAD EMAD KEY: '+str(controlId))
		#XBMCGUI_DIALOG_OK("test", controlId.__str__())
		if controlId == 300: self.close()

window = MyWindow('',addonfolder,'default','720p')

textbox = xbmcgui.ControlTextBox(200, 200, 200, 200, textColor='0xFFFFFFFF')
window.addControl(textbox)

window.show()
window.getControl(100).setLabel('q')
window.getControl(101).setLabel('w')
window.getControl(102).setLabel('r')
window.getControl(120).setLabel('a')
window.getControl(121).setLabel('s')
window.getControl(122).setLabel('d')
window.getControl(312).setLabel('test')
window.getControl(311).setLabel('1234')
window.doModal()
del window

sys.exit()



"""
window = xbmcgui.Window(xbmcgui.getCurrentWindowId())

for i in range(5):
	if window.getProperty('MyAddonIsRunning') != 'true':
		mydisplay = MyWindow()
		mydisplay .doModal()
		del mydisplay
		window.setProperty('MyAddonIsRunning', 'false')
		break
	time.sleep(1)
"""
	
	
	




"""
class MyWindow(xbmcgui.Window):
    def __init__(self):
        self = xbmcgui.Window(10103)

    def onClick( self, controlId ):            
        LOG_THIS('NOTICE','EMAD EMAD '+str(controlId)+': '+str(controlId.__str__()))
		#XBMCGUI_DIALOG_OK("test", controlId.__str__())

window = MyWindow()
window.show()
#window.getControl(101).setLabel('a')

for i in range(5):
	#key = window.onClick(101)
	time.sleep(1)
"""
	

"""
window.show()
window.getControl(101).setLabel('a')
window.getControl(102).setLabel('b')
window.getControl(103).setLabel('c')
window.getControl(104).setLabel('d')
window.getControl(312).setLabel('test')
window.getControl(311).setLabel('1234')
window.getControl(300).setLabel('Enter')

window.setProperty('status','test')

#win = xbmcgui.Window(xbmcgui.getCurrentWindowId())

#window.doModal()
#time.sleep(5)
#window.close()

for i in range(10):
	key = window.onClick(101)
	LOG_THIS('NOTICE','EMAD EMAD '+str(i)+': '+str(key))
	time.sleep(1)
"""



"""
time.sleep(5)


win2 = win.getProperty('status')


new1 = window.getProperty('status')

XBMCGUI_DIALOG_OK(new1,win2)
"""

#new1 = window.getControl(300).getLabel()


#while True: time.sleep(1)

#for i in range(5):	time.sleep(1)


#window2 = xbmcgui.Window(909090)
#new2 = window2.getControl(300).getLabel()



"""
for i in range(10):
	status = window.getControl(300).getLabel()
	LOG_THIS('NOTICE','EMAD EMAD '+str(status))
	if status!='running':
		XBMCGUI_DIALOG_OK('worked','')
		break
	#if window.isConfirmed(): text = window.getText()
	time.sleep(1)
"""

#id = xbmcgui.getCurrentWindowId()
#XBMCGUI_DIALOG_OK('window id',str(id))


#LOG_THIS('NOTICE','EMAD EMAD WIDNOW EXIT')

#text = window.getControl(312).getLabel()

#XBMCGUI_DIALOG_OK('failed','')




