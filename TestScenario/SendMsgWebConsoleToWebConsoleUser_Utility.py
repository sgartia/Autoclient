"""   This script would send message from Web console user to another web console user"""

# Import Session
from VMP_WebConsole_Utility import *
from datetime import datetime

class DataSet (object):
    

    SenderWebConsoleLoginID = None
    RecipientVMPID = None
    
    
    def __init__(self):
        
        """ Initialize the data """
        
       
        self.SenderWebConsoleLoginID = str(sys.argv[1])
        self.RecipientVMPID = "U"+str(sys.argv[6])
        
     

# Initialize the dataset         
TestData = DataSet()

# Example of use

VMPAgent = VMP()

# define User name and password
VMPAgent.SenderLogin = TestData.SenderWebConsoleLoginID
VMPAgent.SenderPassword = 'vocera'


# authenticate the web console 
VMPAgent.WebLogin()

# Maintained and continue the session ID
VMPAgent.MaintainSessionID()
VMPAgent.ContinueSessionID()

# Initialize the value 
CurrentTime = datetime.now().strftime('%m%d%H%M%S')
VMPAgent.RecipientID = TestData.RecipientVMPID
VMPAgent.MessageText = "MessageFrom"+VMPAgent.SenderLogin+str(CurrentTime)
VMPAgent.ThreadMessageSubject = "TestSubjectfrom"+VMPAgent.SenderLogin+"_"+str(CurrentTime)

#Create a new message conversion 
VMPAgent.CreateNewConversation()


# Get the conversion ID to send message
VMPAgent.MessageText = "Hi How are you"



#print VMPAgent.SessionID
## Send message 
time.sleep(10)
VMPAgent.SendMessage()
time.sleep(10)

# Send message 
VMPAgent.SendMessageMCRMessage()
time.sleep(10)


## Do logout from the user 
VMPAgent.Logout()



