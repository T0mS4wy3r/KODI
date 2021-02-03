from LIBRARY import *


LOG_THIS('NOTICE','================================================================================================================================================================')


DIALOG_BUSY('start')


try: MAIN()
except Exception as error: HANDLE_EXIT_ERRORS(error)


DIALOG_BUSY('stop')




