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
        
        
        print "i am good"
        
        #""" Initialize the data """
        self.IPAssignedToSender = "172.30.26.141"
        #self.IPAssignedToRecipient = sys.argv[2]
        self.SenderVCSLoginID = "saroj1" 
        self.SenderMacID =  'aaaa11111111'
        #self.SenderVoiceID =  sys.argv[5] 
        #self.RecipientVCSLoginID =  sys.argv[6]
        #self.RecipientMacID =  sys.argv[7]
        #self.RecipientVoiceID =  sys.argv[8]
        #self.VMPRecipentID =  sys.argv[9]
        #self.CallDuration =  sys.argv[10] 
        

        ## Log the data set 
        #MasterRun.Agent.Log.info("Initialize_Data_for_Call_Scenario : SenderVCSLoginID :"+str(self.SenderVCSLoginID)+"RecipientVCSLoginID :"+str(self.RecipientVCSLoginID))
        

        
        
        
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
#time.sleep(4)
Phone1.EstablishHttpClientConnection()


VMPOne = VMP()
VMPOne.Proto = '6D'

time.sleep(1)
#print VMPOne.DevicePIN
VMPOne.UserLoginID = TestData.SenderVCSLoginID
VMPOne.MAC = TestData.SenderMacID
VMPOne.LoginPassword = "vocera"
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
time.sleep(25)
VMPOne.GetPushData()
time.sleep(25)
VMPOne.GetPushData()



