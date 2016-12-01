"""   This module would create log for various script and libary file"""

import os
import sys
import time
import datetime
import requests
global VMPGlobalEnv
global VSTGlobalEnv
import logging
from LoadLogicCalculate import *

class TestRunLog (object):
    
    HomeDir = None
    LogDir = None
    LogfileName = None
    LogFilePath = None
    Log = None
    ScriptName = None
    LogFileAlreadyExists = None
    
    def __init__(self, LogFileName):
        
        self.HomeDir =  str(os.path.dirname(os.path.realpath(__file__))).split("VMPScalability")[0]+"VMPScalability\\"
        self.LogDir = "\\\\172.30.28.5\\ScalabilityLogs\\"  
        #self.HomeDir+"LoadRunLog\\"
        
        self.Log = logging.getLogger('myapp')  
        
        self.LogfileName = LogFileName
            
        self.LogfilePath = self.LogDir + datetime.datetime.now().strftime('%Y_%m_%d_')+self.LogfileName
        
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
        


        
# Initiate the log file 
LoadRun = TestRunLog("VMPUserSendMessageToVSTUserAndItRespond.log")
        


# Example of use 
LoadTest = LoadLogic()

LoadTest.CalculateExtimatedTimeToCompleteAllIteration()

if (LoadRun.LogFileAlreadyExists == False):
    print "Load Required: " + str( LoadTest.LOAD_Required)+  " message / hr"
    LoadRun.Log.info( "Load Required: " + str( LoadTest.LOAD_Required)+  " message / hr") 

# Assign Number of message each VMP user would send to one VST user 
NUMBER_OF_VMP_MESSAGE_TO_VST_USER = LoadTest.NumberOfMessageEachVMPUserSent
if (LoadRun.LogFileAlreadyExists == False):
    # Number of message each VMP user would send to one VST user 
    print "Number Of Message EachUser Send  : " + str( LoadTest.NumberOfMessageEachVMPUserSent)
    LoadRun.Log.info("Number Of Message EachUser Send  : " + str( LoadTest.NumberOfMessageEachVMPUserSent))



# Time Interval between two VMP message send by one user 
TIME_INTERVAL_ON_EACH_MESSAGE_SEND_FOR_A_USER_IN_SEC = LoadTest.TimeIntervalOnEachMessageSendByAUserInSec

if (LoadRun.LogFileAlreadyExists == False):
    print "Time Interval On Each Message Send By A User In Sec  : " + str( LoadTest.TimeIntervalOnEachMessageSendByAUserInSec)
    LoadRun.Log.info("Time Interval On Each Message Send By A User In Sec  : " + str( LoadTest.TimeIntervalOnEachMessageSendByAUserInSec))

# Number of time we would check the message arrival in VST Device after in send by the VMP user
NUMBER_OF_TRY_TO_CHECK_MESSAGE_ARRIVED = LoadTest.NumberOfTryToCheckMessageArrived

if (LoadRun.LogFileAlreadyExists == False):
    print "Number of time we would check the message arrival in VST Device : " + str( LoadTest.NumberOfTryToCheckMessageArrived)
    LoadRun.Log.info("Number of time we would check the message arrival in VST Device : " + str( LoadTest.NumberOfTryToCheckMessageArrived))


    
# Wait time to check the Message arrival in device in a loop
TIME_INTERVAL_ON_MESSAGE_ARRIVAL_CHECK = LoadTest.TimeIntervalOnMessageArrivalCheck

if (LoadRun.LogFileAlreadyExists == False):
    print "Time interval to check the  message arrival in VST Device : " + str( LoadTest.TimeIntervalOnMessageArrivalCheck)
    LoadRun.Log.info("Time interval to check the  message arrival in VST Device : " + str( LoadTest.TimeIntervalOnMessageArrivalCheck))

# Number of time the complete data set iterate for the load run
TOTAL_TIME_ITERATION = 2

# Time interval between each record in data set to execute 
TIME_INTERVAL_ON_EACH_NEW_THREAD = LoadTest.TimeIntervalOnEachNewThread
if (LoadRun.LogFileAlreadyExists == False):
    print "Time interval between each record in data set to execute  : " + str( LoadTest.TimeIntervalOnEachNewThread)
    LoadRun.Log.info("Time interval between each record in data set to execute  : " + str( LoadTest.TimeIntervalOnEachNewThread))

# Time Interval on each iteration so give maximum time (wait to complete the message sent by VMP user in loop)
TIME_INTERVAL_ON_EACH_ITEARATION = LoadTest.ExpectedTimeToCompleteAllIteration

LoadTest.CalculateServerLoadPerSec()

if (LoadRun.LogFileAlreadyExists == False):
    print "Time to complete one iteration: " + str( LoadTest.ExpectedTimeToCompleteOneIteration)+  " sec"
    print "Time to complete all iteration: " +str( LoadTest.ExpectedTimeToCompleteAllIteration) + " sec"
    print "Server Load: "+str(LoadTest.ServerLoadPerSec)+" Message / sec"
    LoadRun.Log.info("Time to complete one iteration: " + str( LoadTest.ExpectedTimeToCompleteOneIteration)+  " sec")
    LoadRun.Log.info("Time to complete all iteration: " +str( LoadTest.ExpectedTimeToCompleteAllIteration) + " sec")
    LoadRun.Log.info("Server Load: "+str(LoadTest.ServerLoadPerSec)+" Message / sec")
    




