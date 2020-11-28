# -*- coding: utf-8 -*-
from LIBRARY import *



DIALOG_NOTIFICATION('TEST','TEST')

#url = 'C:\\Portable Programs\\KODI_v18_64bit\\Kodi\\portable_data\\cache\\plugin.video.arabicvideos\\file_0896_SHV_زيارة_الرسول_الأعظم_(ص)_(أباذر_الحلواجي).mp3'

#url = 'c:\\asdf.mp3'
#url = 'C:\\TEMP\\temp\\asdf.mp3'
#url = 'C:\\TEMP\\temp\\aa bb\\asdf.mp3'


url = 'C:\\TEMP\\temp\\aa bb\\فحص.mp3'

url = 'C:\\TEMP\\temp\\aa bb\\file_4834_SHV_زيارة_الرسول_الأعظم_(ص)_(أباذر_الحلواجي).mp3'


#url = url.decode('utf8')



xbmc.Player().play(url)


