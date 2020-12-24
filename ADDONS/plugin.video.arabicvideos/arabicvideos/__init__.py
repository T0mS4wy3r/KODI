from LIBRARY import *

DIALOG_BUSY('start')


try: MAIN()
except Exception as error: HANDLE_EXIT_ERRORS(error)


DIALOG_BUSY('stop')


"""
Test using SERVICES file
function TESTINGS123()

because PLAY_VIDEO()
does not work without menu items

enable the testing using MENUS file
"""

