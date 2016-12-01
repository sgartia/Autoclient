"""  This module would contain all the Method for VMP device opeartion"""
import pypyodbc
import string
import random
import requests
import datetime
import time
from JmeterScriptCall_Utility import *
import StringIO
import zipfile
import gzip

import string

########################################################################
class VMPEnv(object):
    
    VmpEndpoint = None
    headers = {}
    
    def __init__(self):
        """ Assign the parameter"""
        
        self.VmpEndpoint = "http://172.30.29.101"    
        headers = {
                    
                    'Accept-Language': 'en-US',               
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept': '*/*',                    
                    'User-Agent': 'VCS/3.0.3.524 (iOS 9.3.5)'
            }
       

VMPGlobalEnv =    VMPEnv()    
        
    
    

class VMP(object):
    """  This class contains all the method related to VMP"""
   
    # Device Information 
    DeviceLoginURL = None    
    DevicePIN = None
    Token = None
    SendMessageURL = None
   
    # User information
    UserLoginID = None
    LoginPassword = None
    
    RecipientID = None
    ConvId = None
    ThreadMessageSubject = None
    MessageText = None
    MessageSeverity = None
    PushID = None
    PushIDReturnFilePath = "C:\\testdata\\test.txt"
    
    # environment variable
    CurrentTime = None
    MAC = None
    MessageHistory = None
    CreatorMessageID = None
    MaxConversations = None
    
    #Real Device Login 
    PhysicalDevicePIN = None
    ContactImages = None


    def __init__(self):
        """  this method would initialize the VMP parameter """      

        # initializing the URL
        self.DeviceLoginURL = VMPGlobalEnv.VmpEndpoint+'/WIC'
        
        
        ## Initialize the User name and password
        #self.UserLoginID = 'TestH035324'
        self.LoginPassword = 'vocera'
        
        # Initialize Mac ID 
        self.MAC = 'aaa000000001'
        self.MaxConversations = '10'
     
    def GetCurrentTime(self):
        """  This method generate the current time"""
        
        # initialize the Current time 
        self.CurrentTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        
    def GeneratePIN (self):
        """  This method generate the PIN"""
        
        self.DevicePIN = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range (31))
        #self.DevicePIN = "8P01IA3ZJC74P9N7BSUN6MLDL68QNN1"
        self.Token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range (64))

    def DeviceLogin(self):
        
        # Generate the device PIN 
        self.GeneratePIN()
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Do the login 
        self.VmpSend = requests.post(
                    self.DeviceLoginURL,
                    params ={   
                            'PIN':self.DevicePIN,                               
                            'compression':'N',  
                            'query':'auth',
                            'ver':'3.0.3.524 iOS',    
                            'proto':'2A',  
                            'CurrentTime':"'"+self.CurrentTime+"'",
                            'Login':self.UserLoginID,    
                            'Password':self.LoginPassword, 
                            'Shared':'Y',
                           
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  "Autheticated to VCS device successfully Username : "
            print self.VmpSend.text            

        else:
            
            print "It failed to VCS device for the user : "
       
        time.sleep(.2)
        # Set the token ID 
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={  
                            'query':'setpushtoken',
                            'PIN':self.DevicePIN,                               
                            'Token':self.Token,                              
                                                       
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully set push token after login: "
            print self.VmpSend.text            

        else:
            
            print "It failed to set push token after login : "
      
               
       
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'getoptions',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'2A',                               
                            'CurrentTime':self.CurrentTime, 
                            
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully Do getoption after login: "
            print self.VmpSend.text            

            return True
        else:
            
            print "It failed Do getoption after login : "
            return False

   
    def GetHistory(self):
        """  This request call the tmhistory after login"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'tmhistory',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'2A',                               
                            'CurrentTime':self.CurrentTime, 
                            'MaxConversations':self.MaxConversations, 
                            
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the history after login: "
            self.MessageHistory = self.VmpSend.text   
            
            return True
        else:
            
            print "It failed to get the history  after login : "
            return False

    def GetTemplate(self):
        """  This request call the tmtemplates after login"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'tmtemplates',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'2A',                               
                            'CurrentTime':self.CurrentTime, 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the template after login: "
            #print self.VmpSend.text            

            return True
        else:
            
            print "It failed to get the template after login : "
            return False  

    def GetSubscription(self):
        """  This request call the getsubscription after login"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'getsubscription',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'2A',                               
                            'CurrentTime':self.CurrentTime, 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the subscription after login: "
            #print self.VmpSend.text            

            return True
        else:
            
            print "It failed to get the subscription after login : "
            return False  

    def GetContacts(self):
        """  This request call the Get contacts after login"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'Y', 
                            'query':'getcontacts',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'2A',                               
                            'CurrentTime':"'"+self.CurrentTime+"'", 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the contacts after login: "
            print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')        

            return True
        else:
            
            print "It failed to get the contacts after login : "
            return False  
    
    
    def GetContactsAfterVoiceLogin(self):
        """  This request call the Get contacts after voice login"""
        
        # Get the current time 
        self.GetCurrentTime()
        self.ContactImages = 'E'
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'Y', 
                            'query':'getcontacts',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'4A',                               
                            'CurrentTime':"'"+self.CurrentTime+"'", 
                            'ContactImages':self.ContactImages
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the contacts after login: "
            print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')        

            return True
        else:
            
            print "It failed to get the contacts after login : "
            return False  
    def GetFavorites(self):
        """  This request call the Get Favourites after login"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'Y', 
                            'query':'getfavorites',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'2A',                               
                            'CurrentTime':self.CurrentTime, 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the Favorites after login: "
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')      

            return True
        else:
            
            print "It failed to get the Favorites after login : "
            return False  

    def GetAvailabilityStatus(self):
        """  This request call the Get Available status after voice login"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'Y', 
                            'query':'getavailabilitystatus',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'4A',                               
                            'CurrentTime':self.CurrentTime, 
                            'ID':'1'
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the Availability Status: "
            print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')      

            return True
        else:
            
            print "It failed to get the Availability Status : "
            return False  

    
    
    
    def VoiceLogin(self):
        """  This request call the Get contacts after login"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.post(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'voicelogin',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'2A',                               
                            'CurrentTime':self.CurrentTime, 
                            'MAC':self.MAC, 
                            'Force':'Y',                 
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully do Voice Login after login: "
            print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')      

            return True
        else:
            
            print "It failed to Voice Login after login device : "
            return False  

        
        
    def GetPushData(self):
        """  This request call the Get Push data after login"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'getpushdata',                               
                            'ver':'3.0.3.524 iOS', 
                            'proto':'2A',                               
                            'CurrentTime':self.CurrentTime, 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False,stream=True)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            #print "######################"
            #print  " successfully call the get the Pushdata for the User:\n"
            
            ##print self.VmpSend.content        

            #print "\n"
            test = open(self.PushIDReturnFilePath,"w")
            test.write(self.VmpSend.content)
            test.close()
            
           
            #print "######################"

            return True
        else:
            
            print "It failed to call the get the Pushdata for the User: "
            return False  
   
    def SendAcknowledgedViaJmeterScript(self):
        """  This method would send Ack to latest push data"""
        
        # read the latest getpushdata responses
        fh = open(self.PushIDReturnFilePath,'r')
        allLines = fh.readlines()
        

        tempList = []
        for item in  allLines:
            if (str(item).find("$PushID") != -1):
                data = str(item).replace("$PushID=","").strip("\n")
                tempList.append(data)
        
        self.PushID = max(tempList)
        
        # Initialize the time
        self.GetCurrentTime()
        
        
        # Create a object 
        self.JmeterAgent = CallJmeterScript("SendAcknowledge_VMPUtility.jmx")
        
        # Initialize the parameter
        self.JmeterAgent.ScriptParameterDic['PIN'] = self.DevicePIN 
        self.JmeterAgent.ScriptParameterDic['CurrentTime'] = self.CurrentTime
        self.JmeterAgent.ScriptParameterDic['PushId'] = self.PushID
        
       
        
        # Call the jmeter script 
        self.JmeterAgent.ExecuteTheScript()
        
        #print self.JmeterAgent.Cmdline
        
        os.system(self.JmeterAgent.Cmdline)
        
    def SendMessage(self):
        """  This request call the Get Push data after login"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        self.SendMessageURL = VMPGlobalEnv.VmpEndpoint+'/WIC?PIN='+self.DevicePIN+'&compression=N&query=tmsend&ver=3.0.3.524%20iOS&proto=2A&CurrentTime='+self.CurrentTime+''
        
        # Get the options
        self.VmpSend = requests.get(
                    self.SendMessageURL,
                    params ={                              
                             
                             },
                    data = {
                            "data":{
                             '$REC_TYPE':'TEXTCONVERSATION',
                             'Subject':self.ThreadMessageSubject,
                             'Users':self.RecipientID,
                             'Terminated':'N'
                             },
                    
                            '$REC_TYPE':'TEXTMESSAGE',
                            'Severity':'0',
                            'CreatorMessageID':'1028',
                            'Body':self.MessageText,
                            'MCR':'N'


                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully call the get the Send Mail for the User:"
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')      

            return True
        else:
            
            print "It failed to call the get the Pushdata for the User: "
            return False  
            
    def SendMessageViaJmeterScript(self):
        """  This method would send message to latest message recived"""
        
        # Initialize the time
        self.GetCurrentTime()
        #self.RecipientID = 136
        
        # Create a object 
        self.JmeterAgent = CallJmeterScript("SendTextMessage_VMPUtility.jmx")
        
        # Initialize the parameter
        self.JmeterAgent.ScriptParameterDic['PIN'] = self.DevicePIN 
        self.JmeterAgent.ScriptParameterDic['CurrentTime'] = self.CurrentTime
        self.JmeterAgent.ScriptParameterDic['Subject'] = self.ThreadMessageSubject
        self.JmeterAgent.ScriptParameterDic['UserID'] = str(self.RecipientID)
        self.JmeterAgent.ScriptParameterDic['Messagebody'] = self.MessageText
       
       
        
        # Call the jmeter script 
        self.JmeterAgent.ExecuteTheScript()
        
        #print self.JmeterAgent.Cmdline
        
        os.system(self.JmeterAgent.Cmdline)
    
    def SendMCRMessageViaJmeterScript(self):
        """  This method would send message to latest message recived"""
        
        # Initialize the time
        self.GetCurrentTime()

        
        # Create a object 
        self.JmeterAgent = CallJmeterScript("SendMCRMessage_VMPUtility.jmx")
        
        # Initialize the parameter
        self.JmeterAgent.ScriptParameterDic['PIN'] = self.DevicePIN 
        self.JmeterAgent.ScriptParameterDic['CurrentTime'] = self.CurrentTime
        self.JmeterAgent.ScriptParameterDic['Subject'] = self.ThreadMessageSubject
        self.JmeterAgent.ScriptParameterDic['UserID'] = str(self.RecipientID)
        self.JmeterAgent.ScriptParameterDic['Messagebody'] = self.MessageText
       
       
        
        # Call the jmeter script 
        self.JmeterAgent.ExecuteTheScript()
        
        #print self.JmeterAgent.Cmdline
        
        os.system(self.JmeterAgent.Cmdline)
            
    def SendAttachmentMessageViaJmeterScript(self):
        """  This method would send message to latest message recived"""
        
        # Initialize the time
        self.GetCurrentTime()
        self.CreatorMessageID  = None
        self.ConvId = 10828
        
        
        # Create a object 
        self.JmeterAgent = CallJmeterScript("SendMessageWithAttachment_VMPUtility.jmx")
        
        # Initialize the parameter
        self.JmeterAgent.ScriptParameterDic['PIN'] = self.DevicePIN 
        self.JmeterAgent.ScriptParameterDic['CurrentTime'] = self.CurrentTime
        self.JmeterAgent.ScriptParameterDic['CreatorMessageID'] = self.CreatorMessageID
        self.JmeterAgent.ScriptParameterDic['ConversationID'] = self.ConvId
        
       
       
        
        # Call the jmeter script 
        self.JmeterAgent.ExecuteTheScript()
        
        #print self.JmeterAgent.Cmdline
        
        os.system(self.JmeterAgent.Cmdline)    


##Example of use

#VMPAgent = VMP()

#time.sleep(1)
#print VMPAgent.DevicePIN
#VMPAgent.UserLoginID = "0000"
#VMPAgent.DeviceLogin()
#VMPAgent.GetHistory()
##print VMPAgent.MessageHistory
#VMPAgent.GetHistory()
#VMPAgent.GetTemplate()
#VMPAgent.GetSubscription()
#time.sleep(.2)
#VMPAgent.GetContacts()
#time.sleep(.2)
#VMPAgent.GetFavorites()
#time.sleep(.5)
#VMPAgent.VoiceLogin()
#time.sleep(.5)
#VMP2 = VMP()
#VMP2.UserLoginID = "1111"
#VMP2.DeviceLogin()

#VMPAgent.PushIDReturnFilePath = "C:\\testdata\\test.txt"
#VMPAgent.GetPushData()
#time.sleep(2)

#VMPAgent.RecipientID = '1005'
#VMPAgent.ThreadMessageSubject = "Testiscorrect"
#VMPAgent.MessageText = "ITestFirst"
#VMPAgent.SendMessageViaJmeterScript()

#VMP2.PushIDReturnFilePath = "C:\\testdata\\test2.txt"
#VMP2.GetPushData()
#time.sleep(2)
#VMP2.PushIDReturnFilePath = "C:\\testdata\\test3.txt"
#VMP2.GetPushData()
#time.sleep(2)
#VMP2.PushIDReturnFilePath = "C:\\testdata\\test4.txt"
#VMP2.GetPushData()
#time.sleep(2)
#VMP2.PushIDReturnFilePath = "C:\\testdata\\test5.txt"
#VMP2.GetPushData()
#time.sleep(2)
#VMP2.PushIDReturnFilePath = "C:\\testdata\\test6.txt"
#VMP2.GetPushData()
#time.sleep(2)
#VMP2.SendAcknowledgedViaJmeterScript()
##VMPAgent.SendMCRMessageViaJmeterScript()

##VMPAgent.GetAvailabilityStatus()


##VMPAgent.VoiceLogin()
##VMPAgent.GetContactsAfterVoiceLogin()
#exit()
#VMPAgent.SendMessage()

#exit()
##VMPAgent.MaxConversations = 20
##VMPAgent.GetHistory()
##print VMPAgent.MessageHistory

#VMPAgent1 = VMP()
#VMPAgent1.UserLoginID = "TestH102602"
#VMPAgent1.DeviceLogin()
#VMPAgent1.RecipientID = '123'

#VMPAgent1.ThreadMessageSubject = "Venki43434"
#VMPAgent1.MessageText = "Venki23232"

#VMPAgent1.SendMessageViaJmeterScript()


#VMPAgent2 = VMP()
#VMPAgent2.UserLoginID = "TestH111876"
#VMPAgent2.DeviceLogin()
#VMPAgent1.RecipientID = '123'
#time.sleep(2)
#VMPAgent2.ThreadMessageSubject = "Venki43434"
#VMPAgent2.MessageText = "Venki23232"



##VMPAgent2.SendMessageViaJmeterScript()



#exit()


