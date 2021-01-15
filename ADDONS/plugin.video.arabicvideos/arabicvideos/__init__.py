from LIBRARY import *

DIALOG_BUSY('start')

try: MAIN()
except Exception as error: HANDLE_EXIT_ERRORS(error)

DIALOG_BUSY('stop')


"""
existing_proxy = getConfiguredProxy()
new_proxy = '5.9.81.243:3128:0'		# ip:port:0 	# :0 means HTTP proxy
setKodiProxy(new_proxy)
setKodiProxy(existing_proxy)
"""


"""
Test using SERVICES file
function TESTINGS123()

because PLAY_VIDEO()
does not work without menu items

enable the testing using MENUS file
"""

