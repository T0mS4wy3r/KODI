# -*- coding: utf-8 -*-

from LIBRARY import *

script_name='FAVOURITES'

def MAIN(mode,favourite):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==270: results = MENU(favourite)
	else: results = False
	return results

def MENU(favouriteID):
	favouritesDICT = GET_ALL_FAVOURITES()
	if favouriteID in favouritesDICT.keys():
		menuLIST = favouritesDICT[favouriteID]
		for type,name,url,mode,image,page,text in menuLIST:
			addMenuItem(type,name,url,mode,image,page,text,favouriteID)
	return

def FAVOURITES_DISPATCHER(favourite):
	if favourite=='': return
	favouriteID = favourite[0]
	if   'ADD1'		in favourite: ADD_TO_FAVOURITES(favouriteID)
	elif 'REMOVE1'	in favourite: REMOVE_FROM_FAVOURITES(favouriteID)
	elif 'UP1'		in favourite: MOVE_FAVOURITES(favouriteID,True,1)
	elif 'DOWN1'	in favourite: MOVE_FAVOURITES(favouriteID,False,1)
	elif 'UP4'		in favourite: MOVE_FAVOURITES(favouriteID,True,4)
	elif 'DOWN4'	in favourite: MOVE_FAVOURITES(favouriteID,False,4)
	return

def MOVE_FAVOURITES(favouriteID,move_up,repeat):
	type,name,url,mode,image,page,text,favourite = EXTRACT_KODI_PATH()
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
	type,name,url,mode,image,page,text,favourite = EXTRACT_KODI_PATH()
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
	type,name,url,mode,image,page,text,favourite = EXTRACT_KODI_PATH()
	menuItem = (type,name,url,mode,image,page,text)
	favouritesDICT = GET_ALL_FAVOURITES()
	if favouriteID in favouritesDICT.keys() and menuItem in favouritesDICT[favouriteID]:
		favouritesDICT[favouriteID].remove(menuItem)
		newFILE = str(favouritesDICT)
		with open(favouritesfile,'w') as f: f.write(newFILE)
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
	type,name,url,mode,image,page,text,favourite = menuItem
	if mode!='270':
		if favourite not in ['','1','2','3','4','NOREFRESH']: favourite = '_'+favourite
		favouritesDICT = GET_ALL_FAVOURITES()
		menuItem = menuItem[:-1]
		menuItem = tuple(menuItem)
		contextMenu1 = CREATE_ONE_CONTEXT_MENU('1',favourite,path,menuItem,favouritesDICT)
		contextMenu2 = CREATE_ONE_CONTEXT_MENU('2',favourite,path,menuItem,favouritesDICT)
		contextMenu3 = CREATE_ONE_CONTEXT_MENU('3',favourite,path,menuItem,favouritesDICT)
		contextMenu4 = CREATE_ONE_CONTEXT_MENU('4',favourite,path,menuItem,favouritesDICT)
		contextMenu = contextMenu1+contextMenu2+contextMenu3+contextMenu4
	contextMenuNEW = []
	for i1,i2 in contextMenu:
		#i1 = '[COLOR FFFFFF00][B]'+i1+'[/B][/COLOR]'
		i1 = '[COLOR FFFFFF00]'+i1+'[/COLOR]'
		contextMenuNEW.append((i1,i2,))
	return contextMenuNEW

def CREATE_ONE_CONTEXT_MENU(favouriteID,favourite,path,menuItem,favouritesDICT):
	contextMenu = []
	if favouriteID in favouritesDICT.keys() and menuItem in favouritesDICT[favouriteID]:
		contextMenu.append(('مسح من مفضلة '+favouriteID,'XBMC.RunPlugin('+path+'&favourite='+favouriteID+'_REMOVE1'+favourite+')',))
		if favourite==favouriteID:
			contextMenu.append(('تحريك 1 للأعلى مفضلة '+favouriteID,'XBMC.RunPlugin('+path+'&favourite='+favouriteID+'_UP1'+favourite+')',))
			contextMenu.append(('تحريك 4 للأعلى مفضلة '+favouriteID,'XBMC.RunPlugin('+path+'&favourite='+favouriteID+'_UP4'+favourite+')',))
			contextMenu.append(('تحريك 1 للأسفل مفضلة '+favouriteID,'XBMC.RunPlugin('+path+'&favourite='+favouriteID+'_DOWN1'+favourite+')',))
			contextMenu.append(('تحريك 4 للأسفل مفضلة '+favouriteID,'XBMC.RunPlugin('+path+'&favourite='+favouriteID+'_DOWN4'+favourite+')',))
	else: contextMenu.append(('إضافة إلى مفضلة '+favouriteID,'XBMC.RunPlugin('+path+'&favourite='+favouriteID+'_ADD1'+favourite+')',))
	return contextMenu


