"""   This script would send message from one device to other device"""

# Import Session

from GlobalVariable_Utility import *
from VMP_Device_Utility import *
from ABPhone_Utility import *



class CallData (object):
    
    IPAssignedToSender = None
    IPAssignedToRecipient = None
    SenderVCSLoginID = None
    SenderMacID = None
    SenderVoiceID = None
    RecipientVCSLoginID = None
    RecipientMacID = None
    RecipientVoiceID = None
    VMPRecipentID = None
    CallDuration = None
    LogAgent = None
    
    
    
    def __init__(self):
        
        """ Initialize the data """
        self.IPAssignedToSender = sys.argv[1]
        self.IPAssignedToRecipient = sys.argv[2]
        self.SenderVCSLoginID = sys.argv[3]      
        self.SenderMacID =  sys.argv[4]
        self.SenderVoiceID =  sys.argv[5] 
        self.RecipientVCSLoginID =  sys.argv[6]
        self.RecipientMacID =  sys.argv[7]
        self.RecipientVoiceID =  sys.argv[8]
        self.VMPRecipentID =  sys.argv[9]
        self.CallDuration =  sys.argv[10] 
        

        # Log the data set 
        MasterRun.Agent.Log.info("Initialize_Data_for_Call_Scenario : SenderVCSLoginID :"+str(self.SenderVCSLoginID)+"RecipientVCSLoginID :"+str(self.RecipientVCSLoginID))
        

        
        
        
TestData = CallData()

#print TestData.IPAssignedToSender 
#print TestData.IPAssignedToRecipient
#print TestData.SenderVCSLoginID 
#print TestData.SenderMacID
#print TestData.SenderVoiceID
#print TestData.RecipientVCSLoginID
#print TestData.RecipientMacID
#print TestData.RecipientVoiceID
#print TestData.VMPRecipentID
#print TestData.CallDuration
    


# Create SIP or HttpClient connection for First user 
# Do Device login for first user 
Phone1 = AutoPhone(TestData.IPAssignedToSender)

#print Phone1.Agent.DeviceIP

Phone1.Agent.ClientMacID = TestData.SenderMacID
Phone1.AbCmd.WaitTimeAfterCall = TestData.CallDuration
Phone1.EstablishSIPConnection()
time.sleep(4)
Phone1.EstablishHttpClientConnection()

#print Phone1.HttpClientPid
#print Phone1.ABRunPid

   
Phone2 = AutoPhone(TestData.IPAssignedToRecipient)
Phone2.Agent.ClientMacID = TestData.RecipientMacID
Phone2.AbCmd.WaitTime = int (TestData.CallDuration) +  10
#print Phone2.Agent.DeviceIP
Phone2.EstablishSIPConnection()
time.sleep(4)
Phone2.EstablishHttpClientConnection()
#print Phone2.HttpClientPid


VSOne = VS()
time.sleep(1)
VSOne.UserID = TestData.SenderVoiceID


VMPOne = VMP()

time.sleep(1)
#print VMPOne.DevicePIN
VMPOne.UserLoginID = TestData.SenderVCSLoginID
VMPOne.MAC = TestData.SenderMacID
VMPOne.DeviceLogin()
time.sleep(.5)
#print VMPOne.MessageHistory
VMPOne.GetHistory()
time.sleep(.5)
VMPOne.GetTemplate()
time.sleep(.5)
VMPOne.GetSubscription()
time.sleep(.5)
VMPOne.GetContacts()
time.sleep(.5)
VMPOne.GetFavorites()
time.sleep(.5)
VMPOne.VoiceLogin()
time.sleep(1)




VSTwo = VS()
time.sleep(1)
VSTwo.UserID = TestData.RecipientVoiceID


VMPTwo = VMP()

time.sleep(1)
#print VMPTwo.DevicePIN
VMPTwo.UserLoginID = TestData.RecipientVCSLoginID
VMPTwo.MAC = TestData.RecipientMacID
VMPTwo.DeviceLogin()
time.sleep(.5)
#print VMPOne.MessageHistory
VMPTwo.GetHistory()
time.sleep(.5)
VMPTwo.GetTemplate()
time.sleep(.5)
VMPTwo.GetSubscription()
time.sleep(.2)
VMPTwo.GetContacts()
time.sleep(.2)
VMPTwo.GetFavorites()
time.sleep(.5)
VMPTwo.VoiceLogin()
time.sleep(.5)

VMPOne.RecipentVoceraUserID = TestData.RecipientVoiceID
VMPOne.RecipientID = TestData.VMPRecipentID
VMPOne.GetAvailabilityStatus()
time.sleep(.5)
VMPOne.Call()

time.sleep(2)


    

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
            MasterRun.Agent.Log.info(" Kill the ProcessID : "+str(Phone1.HttpClientPid))
        
            try:
                #print cmd 
                os.system(cmd)
                flag1 = True
            except:
                print sys.exc_info()
                sys.exc_clear()
        
        if psutil.pid_exists(int(Phone2.ABRunPid)):
            print "The process id: "+ str(Phone2.ABRunPid) + " is running"
            
        else:
            cmd = "TASKKILL /F /FI \"PID eq "+str(Phone2.HttpClientPid)+"\""
            MasterRun.Agent.Log.info(" Kill the ProcessID : "+str(Phone2.HttpClientPid))
        
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
    