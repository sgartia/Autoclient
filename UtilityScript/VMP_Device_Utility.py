"""  This module would contain all the Method for VMP device opeartion"""

from GlobalVariable_Utility import *
from JmeterScriptCall_Utility import *
from VS_Utility import *


########################################################################
class VMPEnvForDevice(object):
    
    VmpEndpoint = None
    headers = {}
    
    def __init__(self):
        """ Assign the parameter"""
        
        self.VmpEndpoint = "http://"+VMP_IP   
        headers = {
                    
                    'Accept-Language': 'en-US',               
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept': '*/*',                    
                    'User-Agent': 'VCS/3.0.3.524 (iOS 9.3.5)'
            }
       

VMPGlobalEnv =    VMPEnvForDevice()    
        
    
    

class VMP(object):
    """  This class contains all the method related to VMP"""
   
    # Device Information 
    DeviceLoginURL = None    
    DevicePIN = None
    Token = None
    SendMessageURL = None
    AppVersion = None
    Proto = None
   
    # User information
    UserLoginID = None
    LoginPassword = None
    
    RecipentVoceraUserID = None
    RecipientID = None
    ConvId = None
    ThreadMessageSubject = None
    MessageText = None
    MessageSeverity = None
    PushID =None
    ConversationID = None
    SharedDevice = None
    
    PushIDReturnFilePath = None
    PushFirstTry = None
    PushConfirmToken = None
    PushMaxNumberTry = None
    PushCounter = None
    PushWaitTimeIntervalInSec = None
    
    # environment variable
    CurrentTime = None
    MAC = None
    APMAC = None
    MessageHistory = None
    CreatorMessageID = None
    MaxConversations = None
    
    #Real Device Login 
    PhysicalDevicePIN = None
    ContactImages = None
    
    # Other Parameter of Vocera Server
    VoceraGroupName = None
    
    
    # Parameter for vocera 3rd party Message.
    VMPAdmin = None
    VMPAdminPassword = None
    ExternalMessageText = None
    ExternalMessageID = None
    ExternalMessageSubject = None
    FileContainsMessageExternalID = None
    
    # Distribution List details
    PublicDLID = None
    
    
    
    
   


    def __init__(self):
        """  this method would initialize the VMP parameter """  
        
       

        # initializing the URL
        self.DeviceLoginURL = VMPGlobalEnv.VmpEndpoint+'/WIC'
        
        
        ## Initialize the User name and password
        #self.UserLoginID = 'TestH035324'
        self.LoginPassword = 'vocera'
        self.PushFirstTry = True
        self.PushMaxNumberTry = 5
        self.PushConfirmToken = "$PushID"
        self.PushWaitTimeIntervalInSec = 4
        
        # Initialize Mac ID 
        self.MAC = 'aaa'
        self.MaxConversations = '10'
        
        # Assign CreatorMessageID
        self.CreatorMessageID = randint(1000,9999)
        
        # initialize the version of App
        self.AppVersion = '3.1.1.643%20iOS'
        if (self.AppVersion == '3.1.1.643%20iOS'):
            self.Proto = '4A'
        else:
            self.Proto = '2A'
            
        # For example initialize vocera parameter
        self.VoceraGroupName = 'test'
        
        # Default 'Y' it is a shared device or else for personal device set the value 'N'
        self.SharedDevice = 'Y'
        
        # initialize all the External Message Parameter
        self.VMPAdmin = "admin"
        self.VMPAdminPassword = "Vocera@123"        
        self.ExternalMessageSubject = "External Message"
        self.FileContainsMessageExternalID = TOOL_DIR+"ExternalMessage.txt"
        
     
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
                            'ver':self.AppVersion,    
                            'proto':self.Proto,  
                            'CurrentTime':"'"+self.CurrentTime+"'",
                            'Login':self.UserLoginID,    
                            'Password':self.LoginPassword, 
                            'Shared':self.SharedDevice,
                           
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  "Autheticated to VCS device successfully Username : "
            MasterRun.Agent.Log.info("Autheticated_VCS_Device_Username :"+str(self.UserLoginID)+"")
            MasterRun.Agent.Log.info("VCS_Device_Username :"+str(self.UserLoginID)+" Device_PIN :"+str(self.DevicePIN)+"")
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
            MasterRun.Agent.Log.info("SetPushToken_Username :"+str(self.UserLoginID)+"")
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
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                            
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully Do getoption after login: "
            MasterRun.Agent.Log.info("GetOptions_Username :"+str(self.UserLoginID)+"")
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
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                            'MaxConversations':self.MaxConversations, 
                            
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the history after login: "
            self.MessageHistory = self.VmpSend.text  
            MasterRun.Agent.Log.info("TmHistory_Username :"+str(self.UserLoginID)+"")
            
            
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
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the template after login: "
            MasterRun.Agent.Log.info("TmTemplates_Username :"+str(self.UserLoginID)+"")
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
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the subscription after login: "
            MasterRun.Agent.Log.info("GetSubscription_Username :"+str(self.UserLoginID)+"")
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
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':"'"+self.CurrentTime+"'", 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the contacts after login: "
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii') 
            MasterRun.Agent.Log.info("GetContacts_Username :"+str(self.UserLoginID)+"")

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
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':"'"+self.CurrentTime+"'", 
                            'ContactImages':self.ContactImages
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the contacts after login: "
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')              
            MasterRun.Agent.Log.info("GetContactsAfterVoiceLogin_Username :"+str(self.UserLoginID)+"")

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
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the Favorites after login: "
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')  
            MasterRun.Agent.Log.info("GetFavorites_Username :"+str(self.UserLoginID)+"")

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
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                            'ID':self.RecipientID
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully get the Availability Status: "
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')  
            MasterRun.Agent.Log.info("GetAvailabilityStatus_Username :"+str(self.UserLoginID)+"")

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
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                            'MAC':self.MAC, 
                            'Force':'Y',                 
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully do Voice Login after login: "
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')
            MasterRun.Agent.Log.info("VoiceLogin_Username :"+str(self.UserLoginID)+"")

            return True
        else:
            
            print "It failed to Voice Login after login device : "
            return False  

    
    
    def UrgentCall(self):
        """  This request Urgent call Vocera user"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.post(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'thirdPartyCall',                               
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                            'recipientID':self.RecipentVoceraUserID, 
                            'callType':'UrgentCall',                 
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully UrgentCalling the vocera user "
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii') 
            MasterRun.Agent.Log.info("UrgentCall_CallerName :"+str(self.UserLoginID)+"")

            return True
        else:
            
            print "It failed to Urgent call Voice Login : "
            return False  
        
    def Call(self):
        """  This request call Vocera user"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.post(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'thirdPartyCall',                               
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                            'recipientID':self.RecipentVoceraUserID, 
                            'callType':'Call',                 
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully Calling the vocera user "
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii') 
            MasterRun.Agent.Log.info("Call_CallerName :"+str(self.UserLoginID)+"")

            return True
        else:
            
            print "It failed to Voice Login after login device : "
            return False      
        
    def LogOut(self):
        """  This request logout user from the app"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.post(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'logout',                               
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                            'MAC':self.MAC, 
                            'Shared':'Y',                 
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully Calling the vocera user "
            MasterRun.Agent.Log.info("LogOut_UserName :"+str(self.UserLoginID)+"")
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')      

            return True
        else:
            
            print "It failed to Voice Login after login device : "
            return False          
         
    def GetVCGAddress(self):
        """  This request to get the VCG Address"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'getvcgaddresses',                               
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                            'APMAC':self.APMAC, 
                                           
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully Calling the vocera user "
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii') 
            MasterRun.Agent.Log.info("GetVcgAddresses_UserName :"+str(self.UserLoginID)+"")

            return True
        else:
            
            print "It failed to Voice Login after login device : "
            return False   
        
    def GetGroupMemberDetails(self):
        """  This request to get the GetGroupMemberDetails"""
        
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            'compression':'N', 
                            'query':'getvoicedlmembers',                               
                            'ver':self.AppVersion, 
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                            'VoceraID':'g-'+self.VoceraGroupName, 
                                           
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully Getting member infomation within the group "
            ReturnText = self.VmpSend.text.encode('ascii', 'ignore').decode('ascii') 
            MasterRun.Agent.Log.info("GetVoicedlmembers_UserName :"+str(self.UserLoginID)+"")
            #print ReturnText
            #fh = open("E:\\Testvink.txt",'a')
            #fh.writelines("\n***********\n")
            #fh.writelines(ReturnText)
            #fh.writelines("\n***********\n")   
            #fh.close()

            return True
        else:
            
            print "successfully Getting member infomation within the group failed "
            return False      
  
    def __GetPushDataRequestProceess(self):
        # Get the current time 
        self.GetCurrentTime()
        
        # Get the options
        self.VmpSend = requests.get(
                    self.DeviceLoginURL,
                    params ={                              
                            'PIN':self.DevicePIN,                               
                            #'compression':'N', 
                            'compression':'N', 
                            'query':'getpushdata',                               
                            'ver':self.AppVersion,                              
                            'proto':self.Proto,                               
                            'CurrentTime':self.CurrentTime, 
                                                        
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False,stream=True)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            #print "######################"
            print  " successfully call the get the Pushdata for the User:\n"
            MasterRun.Agent.Log.info("GetPushData_UserName :"+str(self.UserLoginID)+"")
            
            
            print self.VmpSend.content        

            #print "\n"
            test = open(self.PushIDReturnFilePath,"w")
            test.write(self.VmpSend.content)
            test.close()
            
           
            #print "######################"

            return True
        else:
            
            print "It failed to call the get the Pushdata for the User: "
            return False  
        
    def GetPushData(self):
        """  This request call the Get Push data after login"""
        
        # for first time process the Request 
        if (self.PushFirstTry == True) :
            self.__GetPushDataRequestProceess()
            self.PushFirstTry = False
            self.PushCounter = 1
            
       
        while ( self.PushCounter < self.PushMaxNumberTry):
            
            # read the latest getpushdata responses
            fh = open(self.PushIDReturnFilePath,'r')
            allLines = fh.readlines()
            fh.close()            
        
           
            for item in  allLines:
                
                # Check the pattern is present 
                if (str(item).find(self.PushConfirmToken) != -1):
                    return True
                
            self.__GetPushDataRequestProceess()
            self.PushCounter = self.PushCounter + 1
            
            # Wait till the push wait time
            time.sleep(self.PushWaitTimeIntervalInSec)
            
                
            
            
   
    def SendAcknowledgedViaJmeterScript(self):
        """  This method would send Ack to latest push data"""
        
        # read the latest getpushdata responses
        fh = open(self.PushIDReturnFilePath,'r')
        allLines = fh.readlines()
        

        tempList = []
        for item in  allLines:
            if (str(item).find(self.PushConfirmToken) != -1):
                data = str(item).replace(self.PushConfirmToken,"").strip("\n")
                tempList.append(data)
        
        try :
            self.PushID = max(tempList)
            
            # Initialize the time
            self.GetCurrentTime()
            
            
            # Create a object 
            self.JmeterAgent = CallJmeterScript("SendAcknowledge_VMPUtility.jmx")
            
            # Initialize the parameter
            
            self.JmeterAgent.ScriptParameterDic['VMPSERVER'] = VMP_IP
            self.JmeterAgent.ScriptParameterDic['PIN'] = self.DevicePIN 
            self.JmeterAgent.ScriptParameterDic['CurrentTime'] = self.CurrentTime
            self.JmeterAgent.ScriptParameterDic['PushId'] = self.PushID
            
           
            
            # Call the jmeter script 
            self.JmeterAgent.ExecuteTheScript()
            
            #print self.JmeterAgent.Cmdline
            
            os.system(self.JmeterAgent.Cmdline)
            MasterRun.Agent.Log.info("SendAcknowledgment_UserName :"+str(self.UserLoginID)+"")
        except:
            print sys.exc_info()
            
            # Clear the exception 
            sys.exc_clear()
        
        
   
            
    def SendMessageViaJmeterScript(self):
        """  This method would send message to latest message recived"""
        
        # Initialize the time
        self.GetCurrentTime()
        #self.RecipientID = 136
       
        
        # Create a object 
        self.JmeterAgent = CallJmeterScript("SendTextMessage_VMPUtility.jmx")
        
        # Initialize the parameter
        
        self.JmeterAgent.ScriptParameterDic['VMPSERVER'] = VMP_IP
        self.JmeterAgent.ScriptParameterDic['PIN'] = self.DevicePIN 
        self.JmeterAgent.ScriptParameterDic['CurrentTime'] = self.CurrentTime
        self.JmeterAgent.ScriptParameterDic['Subject'] = self.ThreadMessageSubject
        self.JmeterAgent.ScriptParameterDic['UserID'] = str(self.RecipientID)
        self.JmeterAgent.ScriptParameterDic['Messagebody'] = self.MessageText
        self.JmeterAgent.ScriptParameterDic['CreatorMessageID'] = self.CreatorMessageID
       
       
        
        # Call the jmeter script 
        self.JmeterAgent.ExecuteTheScript()
        
        #print self.JmeterAgent.Cmdline
        
        os.system(self.JmeterAgent.Cmdline)
        MasterRun.Agent.Log.info("SendMessage_UserName :"+str(self.UserLoginID)+"")
    
    def SendSubsequentMessageViaJmeterScript(self):
        """  This method would send Ack to latest push data"""
        
        # read the latest getpushdata responses
        fh = open(self.PushIDReturnFilePath,'r')
        allLines = fh.readlines()
        

        tempList = []
        for item in  allLines:
            if (str(item).find("ConversationID") != -1):
                data = str(item).replace("ConversationID=","").strip("\n")
                tempList.append(data)
        
        self.ConversationID = max(tempList)
        
        self.GetCurrentTime() 
        
        
        # Create a object 
        self.JmeterAgent = CallJmeterScript("SendSubSequentMessageInSameThread.jmx")
        
        # Initialize the parameter
        self.CreatorMessageID = str(int(self.CreatorMessageID) + 1)
        self.JmeterAgent.ScriptParameterDic = {}        
        self.JmeterAgent.ScriptParameterDic['VMPSERVER'] = VMP_IP
        self.JmeterAgent.ScriptParameterDic['PIN'] = self.DevicePIN 
        self.JmeterAgent.ScriptParameterDic['ConvID'] = self.ConversationID
        self.JmeterAgent.ScriptParameterDic['CurrentTime'] = self.CurrentTime
        self.JmeterAgent.ScriptParameterDic['Messagebody'] = self.MessageText
        self.JmeterAgent.ScriptParameterDic['CreatorMessageID'] = self.CreatorMessageID
        
       
        
        # Call the jmeter script 
        self.JmeterAgent.ExecuteTheScript()
        
        print self.JmeterAgent.Cmdline
        
        os.system(self.JmeterAgent.Cmdline)
        MasterRun.Agent.Log.info("SubsequentMessage_UserName :"+str(self.UserLoginID)+"")
        
    def SendMCRMessageViaJmeterScript(self):
        """  This method would send message to latest message recived"""
        
        # Initialize the time
        self.GetCurrentTime()

        
        # Create a object 
        self.JmeterAgent = CallJmeterScript("SendMCRMessage_VMPUtility.jmx")
        
        # Initialize the parameter
        self.JmeterAgent.ScriptParameterDic['VMPSERVER'] = VMP_IP
        self.JmeterAgent.ScriptParameterDic['PIN'] = self.DevicePIN 
        self.JmeterAgent.ScriptParameterDic['CurrentTime'] = self.CurrentTime
        self.JmeterAgent.ScriptParameterDic['Subject'] = self.ThreadMessageSubject
        self.JmeterAgent.ScriptParameterDic['UserID'] = str(self.RecipientID)
        self.JmeterAgent.ScriptParameterDic['Messagebody'] = self.MessageText
       
       
        
        # Call the jmeter script 
        self.JmeterAgent.ExecuteTheScript()
        
        #print self.JmeterAgent.Cmdline
        
        os.system(self.JmeterAgent.Cmdline)
        MasterRun.Agent.Log.info("SendMCRMessage_UserName :"+str(self.UserLoginID)+"")
            
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
        MasterRun.Agent.Log.info("SendAttachmentMessage_UserName :"+str(self.UserLoginID)+"")
        
        
        
    #----------------------------------------------------------------------
    def Send3rdPartyMessageToUser(self):
        """  This method act like sending message from 3rd party"""
        # Get the options
        Url = VMPGlobalEnv.VmpEndpoint + '/wic.asmx'
        
        self.ExternalMessageText = "TestExternalMessage"
        
        # Get the value of the ExternalMessage ID from the file
        FH = open(self.FileContainsMessageExternalID,"r")
        self.ExternalMessageID = str(FH.readline().strip())
        FH.close()
        print self.ExternalMessageID
        
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"\
        xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\
        <soap:Body><Paging_SendAlert xmlns=\"http://wicservices.wallacewireless.com/\"><guid>MAIN</guid>\
        <user>"+self.VMPAdmin+"</user><password>"+self.VMPAdminPassword+"</password><message><ExternalID>"+self.ExternalMessageID+"</ExternalID>\
        <Subject>"+self.ExternalMessageSubject+"</Subject>\
        <Body>"+self.ExternalMessageText+"</Body><Severity>0</Severity><OverridePersonalAlarmSettings>false</OverridePersonalAlarmSettings>\
        <ResponseType>None</ResponseType><AllowResponseComment>false</AllowResponseComment><Callable>false</Callable></message>\
        <responses /><users><PagingAlertUserRef><VoceraID>u-tme1</VoceraID></PagingAlertUserRef></users><dls /></Paging_SendAlert></soap:Body>\
        </soap:Envelope>"
        self.VmpSend = requests.post(
                    Url,
                    data = body,
                    headers={
                    
                    'Expect': '100-continue',               
                    'SOAPAction': "http://wicservices.wallacewireless.com/Paging_SendAlert",
                    'Content-Type': 'text/xml; charset=utf-',
                    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; MS Web Services Client Protocol 2.0.50727.5485)'                   
                    
            },
       
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully Sendimg the message 3rd party message the vocera user "
            MasterRun.Agent.Log.info("LogOut_UserName :"+str(self.UserLoginID)+"")
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')  
            
            # Update the file containing the external message ID
            # Get the value of the ExternalMessage ID from the file
            FH = open(self.FileContainsMessageExternalID,"w")
            FH.write(str(int(self.ExternalMessageID)+1))
            FH.close()

            return True
        else:
            
            print "It failed to essage 3rd party message  : "
            return False          
        
       
    def Send3rdPartyMessageToUserToDL(self,PublicId):
        """  This method act like sending message from 3rd party"""
        # Get the options
        Url = VMPGlobalEnv.VmpEndpoint + '/wic.asmx'
        self.GetCurrentTime()
        
        self.ExternalMessageText = "TestExternalMessage"+str(self.CurrentTime)
        
        # Get the value of the ExternalMessage ID from the file
        FH = open(self.FileContainsMessageExternalID,"r")
        self.ExternalMessageID = str(FH.readline().strip())
        FH.close()
        print self.ExternalMessageID
        self.PublicDLID = str(PublicId)
        
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\
        xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><soap:Body><Paging_SendAlert xmlns=\"http://wicservices.wallacewireless.com/\"><guid>MAIN</guid>\
        <user>"+self.VMPAdmin+"</user><password>"+self.VMPAdminPassword+"</password><message><ExternalID>"+self.ExternalMessageID+"</ExternalID>\
        <Subject>"+self.ExternalMessageSubject+"</Subject><Body>"+self.ExternalMessageText+"</Body><Severity>0</Severity><OverridePersonalAlarmSettings>\
        false</OverridePersonalAlarmSettings><ResponseType>None</ResponseType><AllowResponseComment>false</AllowResponseComment><Callable>false</Callable>\
        </message><responses /><users /><dls><string>"+self.PublicDLID+"</string></dls><callbackInfo><Protocol>HTTP</Protocol><Format>WIC_GENERIC</Format>\
        <Address>http://127.0.0.1:8081/</Address></callbackInfo></Paging_SendAlert></soap:Body></soap:Envelope>"
        self.VmpSend = requests.post(
                    Url,
                    data = body,
                    headers={
                    
                    'Expect': '100-continue',               
                    'SOAPAction': "http://wicservices.wallacewireless.com/Paging_SendAlert",
                    'Content-Type': 'text/xml; charset=utf-',
                    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; MS Web Services Client Protocol 2.0.50727.5485)'                   
                    
            },
       
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print  " successfully Sendimg the message 3rd party message the vocera user "
            MasterRun.Agent.Log.info("LogOut_UserName :"+str(self.UserLoginID)+"")
            #print self.VmpSend.text.encode('ascii', 'ignore').decode('ascii')  
            
            # Update the file containing the external message ID
            # Get the value of the ExternalMessage ID from the file
            FH = open(self.FileContainsMessageExternalID,"w")
            FH.write(str(int(self.ExternalMessageID)+1))
            FH.close()

            return True
        else:
            
            print "It failed to essage 3rd party message  : "
            return False          
       

#Example of use
#VSAgent = VS()
#time.sleep(1)
#VSAgent.UserID = "TestMe1"


#VMPAgent = VMP()
#VMPAgent.Send3rdPartyMessageToUserToDL()
#VMPAgent.Send3rdPartyMessage()

#time.sleep(1)
#print VMPAgent.DevicePIN
#VMPAgent.UserLoginID = "TestMe1"
#VMPAgent.MAC = 'bbbb00000001'
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

#for item in range( 1, 100 ,1):
    #VMPAgent.GetGroupMemberDetails()
    #time.sleep(10)


#exit()
#VMPAgent.RecipentVoceraUserID = 'u-11_1'
#VMPAgent.RecipientID = "1"
#VMPAgent.GetAvailabilityStatus()
#time.sleep(.5)
#VMPAgent.UrgentCall()
#time.sleep(.5)
#VSAgent.PingVS()
#time.sleep(.5)
#VMPAgent.PushIDReturnFilePath = "testmenow.txt"
#VMPAgent.GetPushData()

#for i in range(1,4,1):
    #time.sleep(10)
    #VSAgent.PingVS()
    
#VMPAgent.GetPushData()
#VMPAgent.LogOut()
#VSAgent.CloseCometConnection()



#VSAgent = VS()
#time.sleep(1)
#VSAgent.UserID = "u-22_2"




#VMPAgent.UrgentCall()
#time.sleep(20)
#VMP2 = VMP()
#VMP2.UserLoginID = "1111"
#VMP2.DeviceLogin()

#VMPAgent.PushIDReturnFilePath = "C:\\testdata\\test.txt"
#VMPAgent.GetPushData()
#time.sleep(2)

#VMPAgent.RecipientID = '1'
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
###VMPAgent.SendMCRMessageViaJmeterScript()

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


