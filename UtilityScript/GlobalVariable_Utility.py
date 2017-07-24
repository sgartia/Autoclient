"""   This module would contains all the global and constant and include session"""

# import Session
import sys
import time
import os
import socket
from datetime import datetime
import psutil
import pypyodbc
import string
import random
import ConfigParser
import uuid
import string
import random
import requests
import datetime
import time
import StringIO
import zipfile
import gzip
from random import randint

# Common module in the framework
from Logging_Utility import *
from Common_Utility import *
global MasterRun

class ControlRun():
    Agent = None
    
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        if (isinstance(self.Agent,TestRunLog) == True):
            print "It is instantiated"
        else:
            self.Agent = TestRunLog()

# Intialize the Logging  
MasterRun = ControlRun()

# Global Initilization
global PRIME_IP
global VMP_IP 
global VS_IP     
global VCG_IP
global VMP_DB_SERVER_IP
global JAVA_HOME
global PYTHON_PATH
global VMPSQLSERVER
global VMP_SQL_DB
global VMP_SQL_DB_USER
global VMP_SQL_DB_USER_PASSWORD


# Global Constant session 
MAIN_DIR = "Autoclient"
HOME_DIR = str(os.path.dirname(os.path.realpath(__file__))).split(MAIN_DIR)[0]+MAIN_DIR+"\\"
ENVIRONMENT_CONFIG_INI = HOME_DIR+"EnvironmentConfig.ini"


# assign the value of all the server and path
Handle = ConfigParser.ConfigParser()
Handle.optionxform = str
Handle.read(ENVIRONMENT_CONFIG_INI)        
  

#  Initialize All Server
VMP_IP = str(Handle.get('Environment_Setting',"VMP_IP")).strip()
VS_IP = str(Handle.get('Environment_Setting',"VS_IP")).strip()
VCG_IP = str(Handle.get('Environment_Setting',"VCG_IP")).strip()
VMP_DB_SERVER_IP = str(Handle.get('Environment_Setting',"VMP_DB_SERVER_IP")).strip()
JAVA_HOME = str(Handle.get('Environment_Setting',"JAVA_HOME")).strip()
PYTHON_PATH = str(Handle.get('Environment_Setting',"PYTHON_PATH")).strip()+" "
VMP_SQL_DB_NAME = str(Handle.get('Environment_Setting',"VMP_SQL_DB")).strip()
VMP_SQL_DB_USER = str(Handle.get('Environment_Setting',"VMP_SQL_DB_USER")).strip()
VMP_SQL_DB_USER_PASSWORD = str(Handle.get('Environment_Setting',"VMP_SQL_DB_USER_PASSWORD")).strip()
LOCAL_VM_IP_TO_REMOTE  =  str(Handle.get('Environment_Setting',"LOCAL_VM_IP_TO_REMOTE")).strip()

MasterRun.Agent.Log.info(" VMP_IP :"+VMP_IP+" VS_IP :"+VS_IP+" VCG_IP :"+VCG_IP+" VMP_DB_SERVER_IP :"+VMP_DB_SERVER_IP+" JAVA_HOME :"+JAVA_HOME+" PYTHON_PATH :"+PYTHON_PATH+" VMP_SQL_DB_NAME :"+VMP_SQL_DB_NAME+" TEST VM IP :" +LOCAL_VM_IP_TO_REMOTE+"")
                         
TEST_DATA = HOME_DIR +"testdata\\"
USER_INFO = HOME_DIR+ "UserInfo\\"
TOOL_DIR = HOME_DIR +"TOOL\\"
AB_HOME = TOOL_DIR+"ab\\"
VMI_TOOL = TOOL_DIR + "VMI\\"

SERVER_PORT = 8079
SCRIPT_DIR = HOME_DIR+"UtilityScript\\"
TEMP_DIR = HOME_DIR +"Temp\\"
RESULT_DIR = HOME_DIR+"Result\\"
LOG_DIR  = RESULT_DIR +"Log\\"


HOST_NAME = socket.gethostname()

# Get the PrimeIP 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
try:
    MasterRun.Agent.Log.info("Assigning the prime IP via network socket connection")
    s.connect(('google.com', 0))
    PRIME_IP =  s.getsockname()[0]
    s.close()
    
except:
    MasterRun.Agent.Log.info("It got exception in getting the prime IP via network socket connection")
    MasterRun.Agent.Log.info("Assigning the first IP as the PrimeIP")
    PRIME_IP = socket.gethostbyname(socket.gethostname())
    print sys.exc_info()
    sys.exc_clear()

                            

# Constant file path 
FILE_VMPUserName = USER_INFO+"VMPUserName.csv"
FILE_VSUserLogin = USER_INFO+"VSUserLogin.csv"
FILE_SampleData = USER_INFO+"SampleTestDataFile.csv"


SCRIPT_NAME_AND_DATA_FILE = {"CallOneDeviceToAnotherDevice_Utility.py":"SampleDataFileForCallingScenario",\
                             "SendMessageFromOneDeviceToAnotherDevice_Utility.py":"SampleDataSendingMessageFromDeviceToDevice",\
                             "SendMCRMsgDeviceToDevice_Utility.py":"SampleDataSendingMCR",\
                             "SendMsgWebConsoleToWebConsoleUser_Utility.py":"SampleDataSendingMessageWebConsoleToWebConsole",\
                             "DeviceLoggingExprience_Utility.py":"SampleDataLoginExprience",\
                             "BadgeCall_Utility.py":"SampleDataFileForBadgeToBadgeCall", \
                             "SendMessageDeviceToDeviceNoVoiceLogin_Utility.py":"SampleDataMessagingNoVoiceLogin",\
                             "SendMCRMsgDeviceToDeviceNoVoiceLogin_Utility.py":"SampleDataMCRMessingNoVoiceLogin",\
                             "SendExternalMessagesToDL_Utility.py":"SampleDataSendingMessageToDL",\
                             "SendVMIMessageToBadge_Utility.py":"SampleDataSendingMessageToBadge"\
                             }

SCRIPT_NAME_AND_IP_REQUIREMENT = {"CallOneDeviceToAnotherDevice_Utility.py":2,"SendMessageFromOneDeviceToAnotherDevice_Utility.py":2,\
                                  "SendMCRMsgDeviceToDevice_Utility.py":2,"SendMsgWebConsoleToWebConsoleUser_Utility.py":0,\
                                  "DeviceLoggingExprience_Utility.py":0,"BadgeCall_Utility.py":2, "SendMessageDeviceToDeviceNoVoiceLogin_Utility.py":0,\
                                  "SendMCRMsgDeviceToDeviceNoVoiceLogin_Utility.py":0,"SendExternalMessagesToDL_Utility.py":0,\
                                  "SendVMIMessageToBadge_Utility.py":1}



SCRIPT_NAME_AND_MAXRUN_NONSTOP = {"CallOneDeviceToAnotherDevice_Utility.py":35,"SendMessageFromOneDeviceToAnotherDevice_Utility.py":35,\
                                  "SendMCRMsgDeviceToDevice_Utility.py":35,"SendMsgWebConsoleToWebConsoleUser_Utility.py":50,\
                                  "DeviceLoggingExprience_Utility.py":100,"BadgeCall_Utility.py":40,"SendMessageDeviceToDeviceNoVoiceLogin_Utility.py":45,\
                                  "SendMCRMsgDeviceToDeviceNoVoiceLogin_Utility.py":45,"SendExternalMessagesToDL_Utility.py":50,"SendVMIMessageToBadge_Utility.py":50}


SCRIPT_NAME_AND_WAITTIME_KILLPID = {"CallOneDeviceToAnotherDevice_Utility.py":50,"SendMessageFromOneDeviceToAnotherDevice_Utility.py":50,\
                                  "SendMCRMsgDeviceToDevice_Utility.py":50,"SendMsgWebConsoleToWebConsoleUser_Utility.py":30,\
                                  "DeviceLoggingExprience_Utility.py":40,"BadgeCall_Utility.py":30,"SendMessageDeviceToDeviceNoVoiceLogin_Utility.py":30,\
                                  "SendMCRMsgDeviceToDeviceNoVoiceLogin_Utility.py":30,"SendExternalMessagesToDL_Utility.py":30,"SendVMIMessageToBadge_Utility.py":30}

def list_difference(list1, list2):
    """uses list1 as the reference, returns list of items not in list2"""

    diff_list = []
    for item in list1:
        if not item in list2:
            diff_list.append(item)
    return diff_list
