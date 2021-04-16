# -*- coding: utf-8 -*-
from LIBRARY import *


LOG_THIS('NOTICE','================================================================================================================================================================')


#a = READ_FROM_SQL3('MISC','USERAGENT123')
#DIALOG_OK(str(a),str(a))


DIALOG_BUSY('start')


try: MAIN()
except Exception as error: HANDLE_EXIT_ERRORS(error)


DIALOG_BUSY('stop')




