"""   This script would send message from one device to other device"""

# Import Session

from GlobalVariable_Utility import *
from VMP_Device_Utility import *



class LoginData (object):
    
    
    SenderVCSLoginID = None
    WaitTime = None
    
     
    def __init__(self):
        
        """ Initialize the data """
        self.SenderVCSLoginID = sys.argv[1] 
        self.WaitTime = 40
       
        # Log the data set 
        MasterRun.Agent.Log.info("Initialize_LoginFor_ListOfUsers ")
        

        
        
# Get the TestData        
TestData = LoginData()

print TestData.SenderVCSLoginID 
print TestData.WaitTime


VMPOne = VMP()
time.sleep(1)
print VMPOne.DevicePIN


    
# Assign the login ID and Mac ID for VCS user
VMPOne.UserLoginID = TestData.SenderVCSLoginID

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
counter = int(TestData.WaitTime) / 5
for i in range(0,counter,1):
    VMPOne.PushIDReturnFilePath = TEMP_DIR+"Login_"+VMPOne.UserLoginID+".txt"
    VMPOne.GetPushData()
    
    # interval between each Get push request 
    time.sleep(5)


# Do Logout
VMPOne.LogOut()
