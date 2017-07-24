"""  This module would contains all the method related to VMP """
from GlobalVariable_Utility import *

class VMPEnvForWebConsole(object):
    
    VmpEndpoint = None
    headers = {}
    
    def __init__(self):
        """ Assign the parameter"""
        
        self.VmpEndpoint = "http://"+VMP_IP    
        headers = {
                    'Referer': self.VmpEndpoint,
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Origin': self.VmpEndpoint,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
            }
VMPGlobalEnv = VMPEnvForWebConsole()

class VMP(object):
    """  This class contains all the method related to VMP"""
   
    WebLoginURL = None
    MaintainSessionIDUrl = None
    ContinueSessionIDUrl = None 
    SendMessageUrl = None
    SendMCRUrl = None
    MCRResponses = None
    LogoutUrl = None
    TempUrl = None
    
    SenderLogin = None
    SenderPassword = None
    RecipientID = None
    DistributionListID = None
    ConvId = None
    ThreadMessageSubject = None
    MessageText = None
    MessageSeverity = None
    SrvID = None
    
    Sid = None
    TimeZone = None
    SessionID = None    
    VmpSend = None
    
    LogAgent = None

    def __init__(self):
        """  this method would initialize the VMP parameter """
        # Create log agent to log all action by the VMP_WebConsole_Utility
        self.LogAgent = TestRunLog()
       
        self.Sid = 'MAIN'
        self.TimeZone = '-330'
        
        self.MessageSeverity = '0'
        
        self.WebLoginURL = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=Session&action=Login'
        self.MaintainSessionIDUrl = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=Session&action=Init'
        self.ContinueSessionIDUrl = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=App&action=Init' 
        self.SendMessageUrl = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=Messages.Messages&action=SendText'
        self.SendMCRUrl = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=Messages.Messages&action=SendMcr'
        self.LogoutUrl = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=Session&action=Logout'
        

    def WebLogin(self):
        
        self.VmpSend = requests.get(
                    self.WebLoginURL,
                    data={   
                            'login':self.SenderLogin,    #'testone',
                            'password':self.SenderPassword,  #'vocera',
                            'sid':self.Sid,
                           
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
        print "Status: %s" %self.VmpSend.status_code
        if (self.VmpSend.status_code == 200):
            print "Autheticated to VMP webconsole successfully Username : "+str(self.SenderLogin)
            print self.VmpSend.text  
            self.LogAgent.Log.info("Autheticated_VMP_Webconsole_Username : "+str(self.SenderLogin))
            
           
            self.SessionID = str(str(str(self.VmpSend.text).split(",")[0]).split(":")[1]).strip("\"")
            #print message
            return True
        else:
            
            print "It failed to login VMP Web Console for the user : "+str(self.SenderLogin)
            self.LogAgent.Log.info("Failed_Autheticated_VMP_Webconsole_Username : "+str(self.SenderLogin))
            return False
      
    
    def MaintainSessionID(self):
       
        self.VmpSend = requests.post(self.MaintainSessionIDUrl,                    
                    params={   
                            'sessionID':self.SessionID,
                            'url':VMPGlobalEnv.VmpEndpoint,
                            'tz':self.TimeZone,
                            
                         },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
      
        if (self.VmpSend.status_code == 200):
            print "Maintained  the Session ID "
            self.LogAgent.Log.info("Maintained_SessionID _Webconsole_Username : "+str(self.SenderLogin))
            #print self.VmpSend.text           
            return True
        else:
            print "failed to Maintained  the Session ID Status for the user : "+str(self.SenderLogin)
            return False
      
    ############################################################################
    
    def ContinueSessionID(self):
      
        
        self.VmpSend = requests.get( self.ContinueSessionIDUrl,
                    
                     params={
                         'sessionID':self.SessionID,
                        
                     },
                    headers=VMPGlobalEnv.headers,
                    verify=False)
       
        if (self.VmpSend.status_code == 200):
            print "Continue  the Session ID "
            #print self.VmpSend.text            
            return True
        else:
            print "failed to continue  the Session ID Status: %s" %self.VmpSend.status_code
            return False
        
    
    def CreateNewConversation(self):
        
            self.TempUrl = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=Messages.Compose&action=Init'
            
            self.VmpSend = requests.post( self.TempUrl,                    
                         params={
                            'sessionID':self.SessionID
                         },
                         headers=VMPGlobalEnv.headers,
                        verify=False) 
            print self.VmpSend.status_code 
            
            if (self.VmpSend.status_code == 200):
                print " Successfully Open the compose message window: "
                print " Successfully Open the compose message window by the user: "+str(self.SenderLogin)
                #print self.VmpSend.text 
                self.SrvID = str(str(str(self.VmpSend.text).split(",")[0]).split(":")[1]).strip("")
                print self.SrvID
                self.LogAgent.Log.info("OpenTheNewComposeMessage_Webconsole_Username : "+str(self.SenderLogin))
                
            else:
                print "failed to Open the compose message window: %s" %self.VmpSend.status_code
                print " failed to Successfully Open the compose message window by the user: "+str(self.SenderLogin)
    
    
            self.TempUrl = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=Messages.Compose&action=GetTemplates'
            
            self.VmpSend = requests.post( self.TempUrl,                    
                         params={
                            'pagingType': '2',                            
                            'pageNumber':'0',
                            'pageSize': '50',                            
                            'filterText':'',
                            'sessionID': self.SessionID                           
                         
                         },
                         headers=VMPGlobalEnv.headers,
                        verify=False) 
            print self.VmpSend.status_code 
            if (self.VmpSend.status_code == 200):
                print " Successfully Get a template: "+str(self.SenderLogin)
                print " Successfully Get the template by the user: "+str(self.SenderLogin)  
                print self.VmpSend.text
                
            else:
                print "failed to Get a template:: %s" %self.VmpSend.status_code
                print " Failed to Get a template: for the user :"+str(self.SenderLogin) 
               
            self.TempUrl = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=Messages.Compose&action=AddRecipient'
            self.VmpSend = requests.post( self.TempUrl,                    
                         params={
                            'sessionID': self.SessionID,
                            'srvID': self.SrvID,                            
                            'siteIDs[]':'1',
                            'recipientID':self.RecipientID                          
                            
                         
                         },
                         headers=VMPGlobalEnv.headers,
                        verify=False) 
            print self.VmpSend.status_code 
            
            if (self.VmpSend.status_code == 200):
                print " Successfully Added the recipient: "+str(self.SenderLogin)
                print " Successfully Add Recipient by the user: "+str(self.SenderLogin) 
                print self.VmpSend.text
                
            else:
                print "failed to added the recipient: %s" %self.VmpSend.status_code
                print " Failed to add the recipient :"+str(self.SenderLogin)
                
            
            self.TempUrl = VMPGlobalEnv.VmpEndpoint+'/Api.ashx?c=Messages.Compose&action=StartConversation'
            
            self.VmpSend = requests.post( self.TempUrl,                    
                         params={
                            'srvID': self.SrvID,
                            'text': self.MessageText,                            
                            'severity':'0',
                            'type': 'chat',
                            'subject': self.ThreadMessageSubject,
                            'sessionID': self.SessionID
                          
                         },
                         headers=VMPGlobalEnv.headers,
                        verify=False) 
            print self.VmpSend.status_code 
            if (self.VmpSend.status_code == 200):
                print " Successfully start the conversion: "+str(self.SenderLogin)
                print " Successfully start the conversion: "+str(self.SenderLogin) 
                print self.VmpSend.text
                self.ConvId = str(str(str(self.VmpSend.text).split(",\"creatorID\"")[0]).split("\"id\":")[1]).strip("")
                print self.ConvId
                self.LogAgent.Log.info("StartTheNewConversion_Webconsole_Username : "+str(self.SenderLogin)+" ConversionID:"+str(self.ConvId))
                return True
            else:
                print "failed to start the conversion : %s" %self.VmpSend.status_code
                print " Successfully Added the recipient :"+str(self.SenderLogin)
                return False
            return 0
            
    def CreateNewConversationForDL(self):
        """  this method created a new conversion to DistList"""
        
        
        # assign the Distribution List to Recipent ID and call the Same method it would create a 
        # compose message for distribution LIST 
        self.RecipientID = self.DistributionListID
        
        # Call the create New conversation method 
        self.CreateNewConversation()
        
        
    def SendMessage(self):
    
        try:
            self.VmpSend = requests.post( self.SendMessageUrl,                    
                         params={
                            'convID': self.ConvId,
                            'text':self.MessageText,
                            'severity':self.MessageSeverity,
                            'sessionID':self.SessionID
                         },
                         headers=VMPGlobalEnv.headers,
                        verify=False) 
            print self.VmpSend.status_code 
            if (self.VmpSend.status_code == 200):
                print " Successfully Send the message by the user: "+str(self.SenderLogin)
                print " Successfully Send the message by the user: "+str(self.SenderLogin)
                self.LogAgent.Log.info("SendMessage_Successfully_Webconsole_Username : "+str(self.SenderLogin)+" ConversionID:"+str(self.ConvId))
                return True
            else:
                print "failed to Send the message Status: %s" %self.VmpSend.status_code
                print " failed to Send the message Status for the user :"+str(self.SenderLogin)
                return False
        except:
            print sys.exc_info()
    
    def SendMessageMCRMessage(self):
        
        # Initializing the MCR Response 
        self.MCRResponses = ("Yes","No","DontKnow")
    
        try:
            self.VmpSend = requests.post( self.SendMCRUrl,                    
                         params={
                            'convID': self.ConvId,
                            'text':self.MessageText,
                            'severity':self.MessageSeverity,
                            'MCR':'true', 
                            'type': 'responses',
                            'notify':'0',
                            'expiration':'5',                            
                            'responses[]':self.MCRResponses,               
                            'sessionID':self.SessionID
                            
                         },
                         headers=VMPGlobalEnv.headers,
                        verify=False) 
            print self.VmpSend.status_code 
            if (self.VmpSend.status_code == 200):
                print " Successfully Send MCR Message  by the user: "+str(self.SenderLogin)
                #print " Successfully Send the message by the user: "+str(self.SenderLogin)  
                self.LogAgent.Log.info("SendMCRMessage_Successfully_Webconsole_Username : "+str(self.SenderLogin)+" ConversionID:"+str(self.ConvId))
                return True
            else:
                print "failed to Send the MCR message Status: %s" %self.VmpSend.status_code
                #print " failed to Send the message Status for the user :"+str(self.SenderLogin) 
                return False
        except:
            print sys.exc_info()
                    
    def Logout(self):
    
        
        self.VmpSend = requests.post(self.LogoutUrl,
                    
                     params={
                        'sessionID':self.SessionID
                     },
                     headers=VMPGlobalEnv.headers,
                    verify=False) 
        
        if (self.VmpSend.status_code == 200):
            print "Successfully Logout by the user" +str(self.SenderLogin)   
            self.LogAgent.Log.info("Logout_Successfully_Webconsole_Username : "+str(self.SenderLogin))
            return True
        else:
            print "failed to Logout: %s" %self.VmpSend.status_code
            return False
        

        
## Example of use

#VMPAgent = VMP()

## define User name and password
#VMPAgent.SenderLogin = '1111'
#VMPAgent.SenderPassword = 'vocera'


## authenticate the web console 
#VMPAgent.WebLogin()

## Maintained and continue the session ID
#VMPAgent.MaintainSessionID()
#VMPAgent.ContinueSessionID()

## Initialize the value 

#VMPAgent.RecipientID = 'U99'
#VMPAgent.MessageText = 'I need 11111'
#VMPAgent.ThreadMessageSubject = 'saas11111'

##Create a new message conversion 
#VMPAgent.CreateNewConversation()


## Get the conversion ID to send message
#VMPAgent.MessageText = "test me09097097"

## Send message 
##time.sleep(5)
##VMPAgent.SendMessageMCRMessage()
##time.sleep(5)

##print VMPAgent.SessionID
### Send message 
#time.sleep(10)
#VMPAgent.SendMessage()
#time.sleep(10)

### Do logout from the user 
#VMPAgent.Logout()
