"""  this module would perform all the operation for VMI tool """

# Import session
from GlobalVariable_Utility import *


########################################################################
class VMI(object):
    """  Interface for VMI"""
    VMIExe = None
    ClientID = None
    VSIP = None
    BadgeLoginID = None
    MessageText = None
    CmdLineForMesseging = None
    NumberOfVMIMessagePerUser = None
    IntervalBetweenTwoMessage = None
    
        
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        # Initialize the path 
        self.VMIExe = VMI_TOOL + "vmitest.exe"
        self.ClientID = "SSL"
        self.VSIP = VS_IP        
        self.MessageText = "I am doing good"
        
    
        
    def SendMessage(self):
        """  This method would send the VMI Message to the Badge User"""
        
        self.CmdLineForMesseging = self.VMIExe +" -ClientID "+ self.ClientID + " -Server " + self.VSIP + " -LoginID  "+ self.BadgeLoginID+ " -Text \"" + self.MessageText+ "\""
        
        os.system(self.CmdLineForMesseging)
        time.sleep(1) #  delay for messaging stabilizaion
        
        
        
    
## Example of use 

##Agent = VMI()

##Agent.BadgeLoginID = "BJ2"

### send the number of message 
##Agent.SendMessage()
