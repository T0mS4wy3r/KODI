# -*- coding: utf-8 -*-

from LIBRARY import *

script_name='FAVOURITES'

def MAIN(mode,favourite):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==270: results = MENU(favourite)
	#elif mode==271: results = DELETE_FAVOURITES(favourite)
	else: results = False
	return results

def MENU(favouriteID):
	favouritesDICT = GET_ALL_FAVOURITES()
	if favouriteID in favouritesDICT.keys():
		#addMenuItem('folder','مسح هذه القائمة','',271,'','','',favouriteID)
		#addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
		menuLIST = favouritesDICT[favouriteID]
		context = favouriteID
		for type,name,url,mode,image,page,text in menuLIST:
			addMenuItem(type,name,url,mode,image,page,text,context)
	return

def FAVOURITES_DISPATCHER(context):
	if context=='': return
	if '_' in context: favouriteID,context2 = context.split('_',1)
	else: favouriteID,context2 = context,''
	#DIALOG_OK(favouriteID,context)
	if   context2=='UP1'	: MOVE_FAVOURITES(favouriteID,True,1)
	elif context2=='DOWN1'	: MOVE_FAVOURITES(favouriteID,False,1)
	elif context2=='UP4'	: MOVE_FAVOURITES(favouriteID,True,4)
	elif context2=='DOWN4'	: MOVE_FAVOURITES(favouriteID,False,4)
	elif context2=='ADD1'	: ADD_TO_FAVOURITES(favouriteID)
	elif context2=='REMOVE1': REMOVE_FROM_FAVOURITES(favouriteID)
	elif context2=='DELETELIST': DELETE_FAVOURITES(favouriteID)
	return

def MOVE_FAVOURITES(favouriteID,move_up,repeat):
	type,name,url,mode,image,page,text,context = EXTRACT_KODI_PATH()
	menuItem = (type,name,url,mode,image,page,text)
	favouritesDICT = GET_ALL_FAVOURITES()
	if favouriteID in favouritesDICT.keys():
		oldLIST = favouritesDICT[favouriteID]
		size = len(oldLIST)
		for i in range(0,repeat):
			old_index = oldLIST.index(menuItem)
			if move_up: new_index = old_index-1
			else: new_index = old_index+1
			if new_index>=size: new_index = new_index-size
			if new_index<0: new_index = new_index+size
			oldLIST.insert(new_index, oldLIST.pop(old_index))
		favouritesDICT[favouriteID] = oldLIST
		newFILE = str(favouritesDICT)
		with open(favouritesfile,'w') as f: f.write(newFILE)
	return

def ADD_TO_FAVOURITES(favouriteID):
	type,name,url,mode,image,page,text,context = EXTRACT_KODI_PATH()
	newItem = (type,name,url,mode,image,page,text)
	oldFILE = GET_ALL_FAVOURITES()
	newFILE = {}
	for ID in oldFILE.keys():
		if ID!=favouriteID: newFILE[ID] = oldFILE[ID]
		else:
			if name!='..' and name!='':
				oldLIST = oldFILE[ID]
				if newItem in oldLIST:
					index = oldLIST.index(newItem)
					del oldLIST[index]
				newLIST = oldLIST+[newItem]
				newFILE[ID] = newLIST
			else: newFILE[ID] = oldFILE[ID]
	if favouriteID not in newFILE.keys(): newFILE[favouriteID] = [newItem]
	newFILE = str(newFILE)
	with open(favouritesfile,'w') as f: f.write(newFILE)
	return

def REMOVE_FROM_FAVOURITES(favouriteID):
	type,name,url,mode,image,page,text,context = EXTRACT_KODI_PATH()
	menuItem = (type,name,url,mode,image,page,text)
	favouritesDICT = GET_ALL_FAVOURITES()
	if favouriteID in favouritesDICT.keys() and menuItem in favouritesDICT[favouriteID]:
		favouritesDICT[favouriteID].remove(menuItem)
		newFILE = str(favouritesDICT)
		with open(favouritesfile,'w') as f: f.write(newFILE)
	return

def DELETE_FAVOURITES(favouriteID):
	yes = DIALOG_YESNO('رسالة من المبرمج','هل تريد فعلا مسح جميع محتويات قائمة المفضلة '+favouriteID+' ؟!','','','كلا','نعم')
	if yes!=1: return
	favouritesDICT = GET_ALL_FAVOURITES()
	if favouriteID in favouritesDICT.keys():
		del favouritesDICT[favouriteID]
		newFILE = str(favouritesDICT)
		with open(favouritesfile,'w') as f: f.write(newFILE)
		DIALOG_OK('رسالة من المبرمج','تم مسح جميع محتويات قائمة المفضلة '+favouriteID)
	return

def GET_ALL_FAVOURITES():
	if os.path.exists(favouritesfile):
		with open(favouritesfile,'r') as f: oldFILE = f.read()
		favouritesDICT = eval(oldFILE)
	else: favouritesDICT = {}
	return favouritesDICT

def GET_FAVOURITES_CONTEXT_MENU(path):
	contextMenu = []
	menuItem = EXTRACT_KODI_PATH(path)
	type,name,url,mode,image,page,text,context = menuItem
	#if context not in ['','1','2','3','4','5']: context = '_'+context
	favouritesDICT = GET_ALL_FAVOURITES()
	if mode=='270':
		if context in favouritesDICT.keys() and len(favouritesDICT[context])>0:
			contextMenu.append(('مسح قائمة مفضلة '+context,'XBMC.RunPlugin('+path+'&context='+context+'_DELETELIST'+')'))
	else:
		menuItem = menuItem[:-1]
		menuItem = tuple(menuItem)
		contextMenu1 = CREATE_ONE_CONTEXT_MENU('1',context,path,menuItem,favouritesDICT)
		contextMenu2 = CREATE_ONE_CONTEXT_MENU('2',context,path,menuItem,favouritesDICT)
		contextMenu3 = CREATE_ONE_CONTEXT_MENU('3',context,path,menuItem,favouritesDICT)
		contextMenu4 = CREATE_ONE_CONTEXT_MENU('4',context,path,menuItem,favouritesDICT)
		contextMenu5 = CREATE_ONE_CONTEXT_MENU('5',context,path,menuItem,favouritesDICT)
		contextMenu = contextMenu1+contextMenu2+contextMenu3+contextMenu4+contextMenu5
	contextMenuNEW = []
	for i1,i2 in contextMenu:
		#i1 = '[COLOR FFFFFF00][B]'+i1+'[/B][/COLOR]'
		i1 = '[COLOR FFFFFF00]'+i1+'[/COLOR]'
		contextMenuNEW.append((i1,i2,))
	return contextMenuNEW

def CREATE_ONE_CONTEXT_MENU(favouriteID,context,path,menuItem,favouritesDICT):
	contextMenu = []
	if favouriteID in favouritesDICT.keys() and menuItem in favouritesDICT[favouriteID]:
		contextMenu.append(('مسح من مفضلة '+favouriteID,'XBMC.RunPlugin('+path+'&context='+favouriteID+'_REMOVE1)'))
		if context==favouriteID:
			count = len(favouritesDICT[favouriteID])
			if count>1: contextMenu.append(('تحريك 1 للأعلى','XBMC.RunPlugin('+path+'&context='+favouriteID+'_UP1)'))
			if count>4: contextMenu.append(('تحريك 4 للأعلى','XBMC.RunPlugin('+path+'&context='+favouriteID+'_UP4)'))
			if count>1: contextMenu.append(('تحريك 1 للأسفل','XBMC.RunPlugin('+path+'&context='+favouriteID+'_DOWN1)'))
			if count>4: contextMenu.append(('تحريك 4 للأسفل','XBMC.RunPlugin('+path+'&context='+favouriteID+'_DOWN4)'))
	else: contextMenu.append(('إضافة إلى مفضلة '+favouriteID,'XBMC.RunPlugin('+path+'&context='+favouriteID+'_ADD1)'))
	return contextMenu


