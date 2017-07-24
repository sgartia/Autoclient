"""   This module would create log for various script and libary file"""

# import Session 
import logging
import os
import datetime

MAIN_DIR = "Autoclient"
HOME_DIR = str(os.path.dirname(os.path.realpath(__file__))).split(MAIN_DIR)[0]+MAIN_DIR+"\\"
RESULT_DIR = HOME_DIR+"Result\\"
LOG_DIR  = RESULT_DIR +"Log\\"



class TestRunLog (object):
    """  This class would introduce the logging"""
    
    LogDir = None
    LogfileName = None
    LogFilePath = None
    Log = None
    ScriptName = None
    LogFileAlreadyExists = None
    
    def __init__(self):
        
        
        self.LogDir =  LOG_DIR
        
        # Check if the log Dir does not exists then creat it 
        if (os.path.exists(LOG_DIR) == False):
            os.makedirs(LOG_DIR)
            
        
        
        self.Log = logging.getLogger('myapp')  
        
        self.LogfileName = "Log"+str(datetime.datetime.now().strftime('_%Y_%m_%d_%H'))+".txt"
            
        self.LogfilePath = self.LogDir +self.LogfileName
        
        # check if log file exists or new 
        if (os.path.exists(self.LogfilePath)):
            self.LogFileAlreadyExists = True
        else:
            self.LogFileAlreadyExists = False
            
        hdlr = logging.FileHandler(self.LogfilePath)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.Log.addHandler(hdlr) 
        self.Log.setLevel(logging.INFO)
        

#Example of use
        
## Initiate the log file 
#LoadRun = TestRunLog()
#LoadRun.Log.info("Checking the loggin mechanism  ")
        

