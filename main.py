import core
import os
import traceback
import sys

if __name__ == "__main__":
    rem=os.fork()
    if rem == 0:
        os.setsid()
        sys.stdout.close()
        try:
            core.main()
        except Exception:
            core.logger(core.FATAL,"FATAL ERROR, View Below")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type,exc_value,exc_traceback,file=core.logger_)
            
else:
    sys.exit(0)


