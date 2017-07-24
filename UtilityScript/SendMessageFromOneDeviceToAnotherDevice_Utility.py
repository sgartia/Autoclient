"""   This script would send message from one device to other device"""

# Import Session
from GlobalVariable_Utility import *
from VMP_Device_Utility import *
from ABPhone_Utility import *
from datetime import datetime

class DataSet (object):
    
    IPAssignedToSender = None
    IPAssignedToRecipient = None
    SenderVCSLoginID = None
    SenderMacID = None
    SenderVMPID = None
    RecipientVCSLoginID = None
    RecipientMacID = None
    RecipientVMPID = None
    
    
    def __init__(self):
        
        """ Initialize the data """
        
        self.IPAssignedToSender = sys.argv[1]
        self.IPAssignedToRecipient = sys.argv[2]
        self.SenderVCSLoginID = sys.argv[3]
        self.SenderMacID = sys.argv[4]
        self.SenderVMPID = sys.argv[5]
        self.RecipientVCSLoginID = sys.argv[6]
        self.RecipientMacID = sys.argv[7]
        self.RecipientVMPID = sys.argv[8]
           
        #print self.IPAssignedToSender 
        #print self.IPAssignedToRecipient
        #print self.SenderVCSLoginID
        #print self.SenderMacID
        #print self.SenderVMPID
        #print self.RecipientVCSLoginID
        #print self.RecipientMacID
        #print self.RecipientVMPID    


# Initialize the dataset         
TestData = DataSet()

# Do Device login for first user 
Phone1 = AutoPhone(TestData.IPAssignedToSender)

# Assign Mac ID to Sender 
Phone1.Agent.ClientMacID = TestData.SenderMacID

# Create SIP or HttpClient connection for First user 
Phone1.AbCmd.WaitTime = 40
Phone1.EstablishSIPConnection()
time.sleep(4)
Phone1.EstablishHttpClientConnection()

# Do Device login for second user 
Phone2 = AutoPhone(TestData.IPAssignedToRecipient)

# Assign Mac ID to Recipient 
Phone2.Agent.ClientMacID = TestData.RecipientMacID

# Create SIP or HttpClient connection for second user 
Phone2.AbCmd.WaitTime = 40
Phone2.EstablishSIPConnection()
time.sleep(4)
Phone2.EstablishHttpClientConnection()


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

# Get Voice login for first user 
User1.VoiceLogin()
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

# Get Voice login for Second user 
User2.VoiceLogin()
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

# Wait some time to complete all the process

#Close all the Http Client 

flag1 = False
flag2 = False
flag = True
#print Phone1.ABRunPid
#print Phone2.ABRunPid
#print Phone1.HttpClientPid
#print Phone2.HttpClientPid

while(flag):    

        if psutil.pid_exists(int(Phone1.ABRunPid)):
            print "The process id: "+ str(Phone1.ABRunPid) + " is running"
            
        else:
            cmd = "TASKKILL /F /FI \"PID eq "+str(Phone1.HttpClientPid)+"\""
        
            try:
                print cmd 
                os.system(cmd)
                flag1 = True
            except:
                print sys.exc_info()
                sys.exc_clear()
        
        if psutil.pid_exists(int(Phone2.ABRunPid)):
            print "The process id: "+ str(Phone2.ABRunPid) + " is running"
            
        else:
            cmd = "TASKKILL /F /FI \"PID eq "+str(Phone2.HttpClientPid)+"\""
        
            try:
                print cmd 
                os.system(cmd)
                flag2 = True
            except:
                print sys.exc_info()
                sys.exc_clear()
                
        
        if (flag1 == True) and (flag2 == True):
            flag = False
        else:
            print "I am waiting for 20 sec"
            time.sleep(20)
     


