"""   This script would send message from one device to other device"""

# Import Session
from VMP_Device_Utility import *
from ABPhone_Utility import *
from datetime import datetime


RunMaster = {}    # This variable contains all info in row 

# Read the data file
FH = open("SampleTestDataFile.csv",'r')
allData = FH.readlines()
FH.close()
count = 1
temp = None
for row in allData:
    print row
    

    
    RunMaster[count] = {}
    temp = str(row).split(',')
    RunMaster[count]['Sender'] = str(temp[0])
    RunMaster[count]['SenderMacId'] = str(temp[1])
    RunMaster[count]['SenderId'] = str(temp[2])
    RunMaster[count]['Recipent'] = str(temp[3])
    RunMaster[count]['RecipentMacId'] = str(temp[4])
    RunMaster[count]['RecipentId'] = str(temp[5]).strip("\n")
    count = count + 1
    

#print RunMaster

    
for item in RunMaster:
    

    # Example of use
    # Create SIP or HttpClient connection for one user 
    # Do Device login for first user 
    Phone1 = AutoPhone()
    Phone1.Agent.ClientMacID = RunMaster[item]['SenderMacId']
    
    Phone1.EstablishSIPConnection()
    Phone1.EstablishHttpClientConnection()
    
    
    
    # Create SIP or HttpClient connection for second user 
    # Do Device login for second user 
    
    Phone2 = AutoPhone()
    Phone2.Agent.ClientMacID = RunMaster[item]['RecipentMacId']
    
    Phone2.EstablishSIPConnection()
    Phone2.EstablishHttpClientConnection()
    
    
    # Do Device login with the user 0000
    VMP1 = VMP()
    time.sleep(5)
    print VMP1.DevicePIN
    VMP1.UserLoginID = RunMaster[item]['Sender']
    VMP1.DeviceLogin()
    VMP1.GetHistory()
    VMP1.GetHistory()
    VMP1.GetTemplate()
    time.sleep(.2)
    VMP1.GetContacts()
    time.sleep(.2)
    VMP1.GetFavorites()
    time.sleep(.5)
    VMP1.VoiceLogin()
    time.sleep(.5)
    
    
    # Do Device login with the user 1111
    VMP2 = VMP()
    VMP2.UserLoginID = RunMaster[item]['Recipent']
    VMP2.DeviceLogin()
    CurrentTime = datetime.now().strftime('%m%d%H%M%S')
    VMP1.PushIDReturnFilePath = TEST_DATA+"Sender_"+VMP1.UserLoginID+"_"+str(CurrentTime)+".txt"
    VMP1.GetPushData()
    time.sleep(2)
    
    VMP1.RecipientID = RunMaster[item]['RecipentId']
    VMP1.ThreadMessageSubject = "TeamSSL"+str(CurrentTime)
    VMP1.MessageText = "MessageFrom"+VMP1.UserLoginID+str(CurrentTime)
    VMP1.SendMessageViaJmeterScript()
    
    CurrentTime = datetime.now().strftime('%m%d%H%M%S')
    VMP2.PushIDReturnFilePath = TEST_DATA+"Reciver_"+VMP2.UserLoginID+"_"+str(CurrentTime)+".txt"        
    VMP2.GetPushData()
    time.sleep(3)
    CurrentTime = datetime.now().strftime('%m%d%H%M%S')
    VMP2.PushIDReturnFilePath = TEST_DATA+"Reciver_"+VMP2.UserLoginID+"_"+str(CurrentTime)+".txt"        
    VMP2.GetPushData()
    time.sleep(3)
    CurrentTime = datetime.now().strftime('%m%d%H%M%S')
    VMP2.PushIDReturnFilePath = TEST_DATA+"Reciver_"+VMP2.UserLoginID+"_"+str(CurrentTime)+".txt"        
    VMP2.GetPushData()
    time.sleep(2)
    CurrentTime = datetime.now().strftime('%m%d%H%M%S')
    VMP2.PushIDReturnFilePath = TEST_DATA+"Reciver_"+VMP2.UserLoginID+"_"+str(CurrentTime)+".txt"        
    VMP2.GetPushData()
    time.sleep(2)
   
    VMP2.SendAcknowledgedViaJmeterScript()
    
    
    # 



