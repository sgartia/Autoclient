"""  This Script would send VMI Message to badge"""

from GlobalVariable_Utility import *
from Badge_Utility import *
from VMI_Utility import *

class DataSet (object):
    
    IPAssignedToBadge = None    
    BadgeUserID = None
    BadgeMacID = None
    NumberOfVMIMessage = 5
    
    
    
    
    def __init__(self):
        
        """ Initialize the data """
        self.IPAssignedToBadge = sys.argv[1]
        self.BadgeUserID = sys.argv[2]
        self.BadgeMacID = sys.argv[3]

        # Log the data set 
        MasterRun.Agent.Log.info("Initialize_Data_for_VMI_Messagging")
        

        
        
Data = DataSet()

# Login in Badge and send VMI message and The badge should play the message after recive the message.
Badge = AutoBadge(Data.IPAssignedToBadge)
Badge.DeviceMac = Data.BadgeMacID
Badge.WaitTimeAfterLogin = 10

# Do log out if its already login then do login   make call to another user and Wait for some time 
Badge.ListOfABScriptCmd = Badge.AbCmd.UntillPrompt(Prompt.dummy_foo1,Badge.WaitTimeAfterLogin) 
for item in range(1,Data.NumberOfVMIMessage,1):
    Badge.AbCmd.WaitTime = str(10)
    Badge.ListOfABScriptCmd = Badge.ListOfABScriptCmd +Badge.AbCmd.Call +\
     Badge.AbCmd.Play(WavfileFor.PlayTextMessages,7)+Badge.AbCmd.UntillPrompt(Prompt.dummy_foo1,Badge.AbCmd.WaitTime)
    
Badge.StartABRun()

time.sleep(5)  # Wait till the Ab started 

Agent = VMI()

Agent.BadgeLoginID = Data.BadgeUserID

# send the number of message 
for item in range(1,Data.NumberOfVMIMessage,1):    
    Agent.SendMessage()
    time.sleep(10)  # Wait till the Ab started 
