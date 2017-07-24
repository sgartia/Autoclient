"""   This script would send message from one device to other device"""

# Import Session

from GlobalVariable_Utility import *
from VMP_Device_Utility import *
from ABPhone_Utility import *



class LoginData (object):
    
    
    SenderVCSLoginID = None
    SenderMacID = None
    SenderVoiceID = None
    PersonalDevice = None
    WaitTime = None
    
    
    
    
    def __init__(self):
        
        """ Initialize the data """
        self.SenderVCSLoginID = sys.argv[1]      
        self.SenderMacID =  sys.argv[2]
        self.SenderVoiceID =  sys.argv[3] 
        self.PersonalDevice =  sys.argv[4]
        self.WaitTime = sys.argv[5]
       
        # Log the data set 
        MasterRun.Agent.Log.info("Initialize_Data_for_Login_Scenario : SenderVCSLoginID :"+str(self.SenderVCSLoginID)+"")
        

        
        
        
TestData = LoginData()


print TestData.SenderVCSLoginID 
print TestData.SenderMacID
print TestData.SenderVoiceID
print TestData.PersonalDevice
print TestData.WaitTime



VSOne = VS()
time.sleep(1)
VSOne.UserID = TestData.SenderVoiceID


VMPOne = VMP()

time.sleep(1)
print VMPOne.DevicePIN

# Check for Personal device and Shared device 
if (str(TestData.PersonalDevice).upper().find("YES") != -1):
    VMPOne.SharedDevice = 'Y'
else :
    VMPOne.SharedDevice = 'N'
    
# Assign the login ID and Mac ID for VCS user
VMPOne.UserLoginID = TestData.SenderVCSLoginID
VMPOne.MAC = TestData.SenderMacID

# Enter  LoginID and Password
VMPOne.DeviceLogin()
time.sleep(.5)

# Get History for the user 
VMPOne.GetHistory()
time.sleep(.5)

# Get Template for the user
VMPOne.GetTemplate()
time.sleep(.5)

# Get Subscription for the user 
VMPOne.GetSubscription()
time.sleep(.5)

# Get Contacts for the user 
VMPOne.GetContacts()
time.sleep(.5)

# Get Favorites for the user 
VMPOne.GetFavorites()
time.sleep(.5)


# Do a Get push data for VMP user 
counter = int(TestData.WaitTime) / 10
for i in range(0,counter,1):
    VMPOne.PushIDReturnFilePath = TEMP_DIR+"Login_"+VMPOne.UserLoginID+".txt"
    VMPOne.GetPushData()
    
    # interval between each Get push request 
    time.sleep(10)


# Do Logout
VMPOne.LogOut()