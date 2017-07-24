
""" Include Section """
import os,sys
import time
from GlobalVariable_Utility import *
from Badge_Utility import *
from IPManeger_Utility import *


class BadgeCallData (object):
    
    IPAssignedToSender = None
    IPAssignedToRecipient = None
    ReciverLastName = None
    ReciverFirstName = None
    ReciverMacID = None
    SenderLastName = None
    SenderFirstName = None
    SenderMacID = None
    CallDuration = None
    
     
    def __init__(self):
        
        """ Initialize the data """
        self.IPAssignedToSender = sys.argv[1]
        self.IPAssignedToRecipient = sys.argv[2]
        self.ReciverLastName = sys.argv[3]
        self.ReciverFirstName = sys.argv[4]
        self.ReciverMacID = sys.argv[5]
        self.SenderLastName = sys.argv[6]
        self.SenderFirstName = sys.argv[7]
        self.SenderMacID = sys.argv[8]
        self.CallDuration = sys.argv[9]
        # Log the data set 
      
      
# First Badge do  Autologin via mac
TestData = BadgeCallData()
Badge1 = AutoBadge(TestData.IPAssignedToRecipient)    

# assign the Mac 
Badge1.DeviceMac = str(TestData.ReciverMacID)
MasterRun.Agent.Log.info("Reciver LastName :"+str(TestData.ReciverLastName)+" ReciverFirstName :"+str(TestData.ReciverFirstName)+\
                         "ReciverMacID :"+str(TestData.ReciverMacID))
    
# Just wait after login
Badge1.AbCmd.UntilWait = int(TestData.CallDuration) + 20
Badge1.Wait()


MasterRun.Agent.Log.info("Sender LastName :"+str(TestData.SenderLastName)+" SenderFirstName :"+str(TestData.SenderFirstName)+\
                         "SenderMacID :"+str(TestData.SenderMacID))
Badge2 = AutoBadge(TestData.IPAssignedToSender)

Badge2.DeviceMac =  TestData.SenderMacID

Badge2.CallIntervalTime = TestData.CallDuration

# Initialize the wait time after call
Badge2.AbCmd.WaitTime = 5
MasterRun.Agent.Log.info("Calling To "+TestData.ReciverFirstName + TestData.ReciverLastName)
Badge2.Call(TestData.ReciverFirstName+"+"+TestData.ReciverLastName)
# delay to stable and sync the run
time.sleep(2)



