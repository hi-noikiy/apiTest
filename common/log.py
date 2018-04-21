import logging
import time
import os
import threading
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class Log:

    def __init__(self):

        global logger, resultPath, logPath
        resultPath =PATH("../logs")
        logPath = os.path.join(resultPath, (time.strftime('%Y%m%d%H%M%S', time.localtime())))
        if os.path.exists(logPath) == False:
            os.makedirs(logPath)
        self.checkNo = 0
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        #create handler,write log
        fh = logging.FileHandler(os.path.join(logPath, "outPut.log" ))
        #Define the output format of formatter handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)
        logger.info('info message')


        # logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename= '..\logs\meijian %s.log',
#                     filemode='w')
#
# #########################################################################################################################
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter()
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)
#
# logging.debug('This is debug message.')
# logging.info('This is info message.')
# logging.warning('This is warning message.')
# logging.error('This is error message.')
# logging.critical('This is critical message.')