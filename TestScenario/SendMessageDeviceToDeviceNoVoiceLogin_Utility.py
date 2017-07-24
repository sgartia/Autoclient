"""   This script would send message from one device to other device"""

# Import Session
from GlobalVariable_Utility import *
from VMP_Device_Utility import *
from datetime import datetime

class DataSet (object):
    
    SenderVCSLoginID = None
    SenderMacID = None
    SenderVMPID = None
    RecipientVCSLoginID = None
    RecipientMacID = None
    RecipientVMPID = None
    
    
    def __init__(self):
        
        """ Initialize the data """
        
        self.SenderVCSLoginID = sys.argv[1]
        self.SenderMacID = sys.argv[2]
        self.SenderVMPID = sys.argv[3]
        self.RecipientVCSLoginID = sys.argv[4]
        self.RecipientMacID = sys.argv[5]
        self.RecipientVMPID = sys.argv[6]

        #print self.SenderVCSLoginID
        #print self.SenderMacID
        #print self.SenderVMPID
        #print self.RecipientVCSLoginID
        #print self.RecipientMacID
        #print self.RecipientVMPID    


# Initialize the dataset         
TestData = DataSet()


# First user do device login 
User1 = VMP()
time.sleep(5)
#print User1.DevicePIN

# Assign the user login ID
User1.UserLoginID = TestData.SenderVCSLoginID

# Do a device login in for first user 
User1.DeviceLogin()
time.sleep(.5)

# Get History for first user 
User1.GetHistory()
time.sleep(.5)

# Get Template for first user 
User1.GetTemplate()
time.sleep(.5)

# Get Contacts for first user 
User1.GetContacts()
time.sleep(.5)

# Get Favourites for first user 
User1.GetFavorites()
time.sleep(.5)


# Do Device login for Second User
User2 = VMP()
User2.UserLoginID = TestData.RecipientVCSLoginID
User2.DeviceLogin()

# Get History for Second user 
User2.GetHistory()
time.sleep(.5)

# Get Template for Second user 
User2.GetTemplate()
time.sleep(.5)

# Get Contacts for Second user 
User2.GetContacts()
time.sleep(.5)

# Get Favourites for Second user 
User2.GetFavorites()
time.sleep(.5)

# Do a Get push data for first user 

User1.PushIDReturnFilePath = TEMP_DIR+"Sender_"+User1.UserLoginID+".txt"
User1.GetPushData()
time.sleep(2)

# Intialize the Recipient ID and send Message 
CurrentTime = datetime.now().strftime('%m%d%H%M%S')
User1.RecipientID = TestData.RecipientVMPID
User1.ThreadMessageSubject = "TeamSSL"+str(CurrentTime)
User1.MessageText = "MessageFrom"+User1.UserLoginID+str(CurrentTime)
User1.SendMessageViaJmeterScript()

# Do a Get push data for Second user 
User2.PushIDReturnFilePath = TEMP_DIR+"Reciver_"+User2.UserLoginID+".txt" 
print User2.PushIDReturnFilePath
User2.GetPushData()
time.sleep(4)


# Do a acknowledgement  for Second user 
User2.SendAcknowledgedViaJmeterScript()

#print "\n***********\n"
#print User1.CreatorMessageID
#print User2.CreatorMessageID
#print "\n***********\n"   

time.sleep(4)

# Second user would send a reply message to same thread
CurrentTime = datetime.now().strftime('%m%d%H%M%S')
User2.MessageText = "Reply1from_" +User2.UserLoginID+str(CurrentTime)
User2.SendSubsequentMessageViaJmeterScript()

time.sleep(4)

CurrentTime = datetime.now().strftime('%m%d%H%M%S')
User2.MessageText = "Reply2from_" +User2.UserLoginID+str(CurrentTime)
User2.SendSubsequentMessageViaJmeterScript()

# Do a Get push data for first user 

User1.PushIDReturnFilePath = TEMP_DIR+"Sender_"+User1.UserLoginID+".txt"
User1.GetPushData()
time.sleep(2)

# Do a acknowledgement  for First user 
User1.SendAcknowledgedViaJmeterScript()


