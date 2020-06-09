# -*- coding: utf-8 -*-

from LIBRARY import *

script_name='FAVOURITES'

def MAIN(mode,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==270: results = MENU(text)
	else: results = False
	return results

def MENU(favouriteID):
	favouritesDICT = GET_ALL_FAVOURITES()
	if favouriteID in favouritesDICT.keys():
		menuLIST = favouritesDICT[favouriteID]
		for type,name,url,mode,image,page,text in menuLIST:
			addMenuItem(type,name,url,mode,image,page,text)
	return

def FAVOURITES_DISPATCHER(favourite):
	if favourite=='': return
	favouriteID = favourite[0]
	if   'ADD'		in favourite: ADD_TO_FAVOURITES(favouriteID)
	elif 'REMOVE'	in favourite: REMOVE_FROM_FAVOURITES(favouriteID)
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
	for TYPE in oldFILE.keys():
		if TYPE!=favouriteID: newFILE[TYPE] = oldFILE[TYPE]
		else:
			if name!='..' and name!='':
				oldLIST = oldFILE[TYPE]
				if newItem in oldLIST:
					index = oldLIST.index(newItem)
					del oldLIST[index]
				newLIST = [newItem]+oldLIST
				newLIST = newLIST[:25]
				newFILE[TYPE] = newLIST
			else: newFILE[TYPE] = oldFILE[TYPE]
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
	favouritesDICT = GET_ALL_FAVOURITES()
	menuItem = menuItem[:-1]
	menuItem = tuple(menuItem)
	#LOG_THIS('NOTICE','============')
	#LOG_THIS('NOTICE',str(menuItem))
	#LOG_THIS('NOTICE',str(favouritesDICT))
	if '1' in favouritesDICT.keys() and menuItem in favouritesDICT['1']:
		contextMenu.append(('مسح من مفضلة 1','XBMC.RunPlugin('+path+'&favourite=1_REMOVE'+')',))
		contextMenu.append(('تحريك 1 إلى الأعلى مفضلة 1','XBMC.RunPlugin('+path+'&favourite=1_UP1'+')',))
		contextMenu.append(('تحريك 4 إلى الأعلى مفضلة 1','XBMC.RunPlugin('+path+'&favourite=1_UP4'+')',))
		contextMenu.append(('تحريك 1 إلى الأسفل مفضلة 1','XBMC.RunPlugin('+path+'&favourite=1_DOWN1'+')',))
		contextMenu.append(('تحريك 4 إلى الأسفل مفضلة 1','XBMC.RunPlugin('+path+'&favourite=1_DOWN4'+')',))
	else: contextMenu.append(('إضافة إلى مفضلة 1','XBMC.RunPlugin('+path+'&favourite=1_ADD'+')',))
	if '2' in favouritesDICT.keys() and menuItem in favouritesDICT['2']:
		contextMenu.append(('مسح من مفضلة 2','XBMC.RunPlugin('+path+'&favourite=2_REMOVE'+')',))
		contextMenu.append(('تحريك 1 إلى الأعلى مفضلة 2','XBMC.RunPlugin('+path+'&favourite=2_UP1'+')',))
		contextMenu.append(('تحريك 4 إلى الأعلى مفضلة 2','XBMC.RunPlugin('+path+'&favourite=2_UP4'+')',))
		contextMenu.append(('تحريك 1 إلى الأسفل مفضلة 2','XBMC.RunPlugin('+path+'&favourite=2_DOWN1'+')',))
		contextMenu.append(('تحريك 4 إلى الأسفل مفضلة 2','XBMC.RunPlugin('+path+'&favourite=2_DOWN4'+')',))
	else: contextMenu.append(('إضافة إلى مفضلة 2','XBMC.RunPlugin('+path+'&favourite=2_ADD'+')',))
	if '3' in favouritesDICT.keys() and menuItem in favouritesDICT['3']:
		contextMenu.append(('مسح من مفضلة 3','XBMC.RunPlugin('+path+'&favourite=3_REMOVE'+')',))
		contextMenu.append(('تحريك 1 إلى الأعلى مفضلة 3','XBMC.RunPlugin('+path+'&favourite=3_UP1'+')',))
		contextMenu.append(('تحريك 4 إلى الأعلى مفضلة 3','XBMC.RunPlugin('+path+'&favourite=3_UP4'+')',))
		contextMenu.append(('تحريك 1 إلى الأسفل مفضلة 3','XBMC.RunPlugin('+path+'&favourite=3_DOWN1'+')',))
		contextMenu.append(('تحريك 4 إلى الأسفل مفضلة 3','XBMC.RunPlugin('+path+'&favourite=3_DOWN4'+')',))
	else: contextMenu.append(('إضافة إلى مفضلة 3','XBMC.RunPlugin('+path+'&favourite=3_ADD'+')',))
	return contextMenu



