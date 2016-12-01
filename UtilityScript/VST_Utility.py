"""  This module would contains all the utility function related to VST  """
# Import Session
from GlobalInterOps import *
from JmeterScriptCall_Utility import *
import uuid

null = None
        
    
    

class VST(object):
    """  This class would  contains all the utility method for VST load"""
    
    DeviceAuthenticateURL = None
    ReceiveMessageURL = None
    SentReplyToRecentMessageSenderURL = None
    
    Headers = None    
    DeviceLoginName = None
    DeviceLoginPin = None    
    Response = None
    Request = None
    RecentMessageRecived = None
    VMPMessage = None
    MessageDeliveredTime = None
    MessageRespondTime = None
    VSTUserID = None 
    SenderID = None
    MessageThreadID = None
    LastMessageIndex = None
    CurrentMessageIndex = None    
    XPranaToken = None
    JmeterAgent = None
    ReplyMessage = None
    UniqueId = None
    ThreadSubject = None
    MCRResponses = None
    ReplyMCRResponseMessage = None
    ReplyMCRResponseID = None
    SecureTextId = None
    responseChoiceId = None
    

    
    def __init__(self):
        """ this method would initiate the parameter"""
        
        self.DeviceAuthenticateURL = VSTGlobalEnv.VSTEndpoint+'/security/authenticate'
        self.ReceiveMessageURL = VSTGlobalEnv.VSTEndpoint+'/secure-texts.json'
        self.SentReplyToRecentMessageSenderURL = VSTGlobalEnv.VSTEndpoint+'/secure-text.json?api=2&_text=1'

        self.LastMessageIndex = 0
        
        #Initialize the login name and password        
        self.DeviceLoginName = 'LoadH043545@gmail.com'
        self.DeviceLoginPin = '1234'
        
        

    def DeviceAuthenticate(self):
        """  This method would authenticate the device """
        try:
            self.Request = requests.post( self.DeviceAuthenticateURL,
                
                data={
                        'username': self.DeviceLoginName,
                        'pin': self.DeviceLoginPin
                     })
    
            self.Response = self.Request.json()
            self.XPranaToken = self.Response['response']['token']
            print self.XPranaToken
            self.Headers = {'x-prana-token': self.XPranaToken }
            LoadRun.Log.info("Successfully    authenticated in a device with Username : "+str(self.DeviceLoginName) +"")
            return True
        except KeyError as ke:
            LoadRun.Log.info ("Authentication Failed for user name : "+str(self.DeviceLoginName)+"" )
            return False

    def CheckForNewMessage (self):
        
        
        self.Request = requests.get(self.ReceiveMessageURL,
                
                params={
                        'type': '2'
                     },
                     headers=self.Headers)
        print "Status: %s" %self.Request.status_code
        if (self.Request.status_code == 200):
            self.Response =  self.Request.json()
            print self.Response

                
                
            self.CurrentMessageIndex = str(self.Response['texts']['totalItems'])

            LoadRun.Log.info (" Total Number of message for the user :"+str(self.DeviceLoginName)+" ="+str(self.CurrentMessageIndex))

            # Get the Recent Message it recived
            self.RecentMessageRecived = str(self.Response['texts']['items'][0]['message'])                        
            
            # Get the own VST User ID
            self.VSTUserID = str(self.Response['texts']['items'][0]['owner'])
            
            # Get the message sender Id 
            self.SenderID = str(self.Response['texts']['items'][0]['from'])
           
            # Get the Message thread ID
            self.MessageThreadID = self.Response['texts']['items'][0]['threadID']
            self.ThreadSubject = self.Response['texts']['items'][0]['threadSubject']
            self.ReplyMessage = 'Yes'
            
            # Get the message secure ID 
            self.SecureTextId = self.Response['texts']['items'][0]['secureTextId']
            
            
            
    def GetMCRResponse(self):
        """  this would get the mcr response text"""
        self.MCRResponses = self.Response['texts']['items'][0]['metadata']['responseChoices']
        for item in self.MCRResponses:
            for key in item:
                if item[key] == str(self.ReplyMessage):                    
                    self.ReplyMCRResponseID = str(item['onPremMCRId'])

    def LogMessageDeliveredTime(self):
        """  This method would log the message delivered time """
        
            
        if dict(self.Response['texts']['items'][0]).has_key('delivered') == True:
            
            # Get the Message deliverable time 
            self.MessageDeliveredTime = str(self.Response['texts']['items'][0]['delivered'])
            self.VMPMessage = self.RecentMessageRecived
            LoadRun.Log.info (" Message_Reached_On_DEVICE_Time :"+str(self.RecentMessageRecived)+" ="+str(self.MessageDeliveredTime))
            LoadRun.Log.info (" Message_Details :"+str(self.RecentMessageRecived)+" ## ThreadID :"+str(self.MessageThreadID) +" ## SenderID :" +str(self.SenderID))
                    
        
            
        elif dict(self.Response['texts']['items'][0]).has_key('sent') == True:
            
            # Get the respond time 
            self.MessageRespondTime = str(self.Response['texts']['items'][0]['sent'])
            self.VMPMessage = self.RecentMessageRecived
            LoadRun.Log.info (" Message_Reached_On_DEVICE_Time :"+str(self.RecentMessageRecived)+" ="+str(self.MessageRespondTime))
            LoadRun.Log.info (" Message_Details :"+str(self.RecentMessageRecived)+" ## ThreadID :"+str(self.MessageThreadID) +" ## SenderID :" +str(self.SenderID))
                

    def LogMessageRespondTime(self):
        """  This method would log the message Respond time by the VST"""
        
            
        if dict(self.Response['texts']['items'][0]).has_key('delivered') == True:
            
            # Get the Message deliverable time 
            self.MessageDeliveredTime = str(self.Response['texts']['items'][0]['delivered'])
            LoadRun.Log.info (" Message_Respond_By_VSTUser_Time :"+str(self.VMPMessage)+" ="+str(self.MessageDeliveredTime))
            
        
            
        elif dict(self.Response['texts']['items'][0]).has_key('sent') == True:
            
            # Get the respond time 
            self.MessageRespondTime = str(self.Response['texts']['items'][0]['sent'])
            LoadRun.Log.info (" Message_Respond_By_VSTUser_Time :"+str(self.VMPMessage)+" ="+str(self.MessageRespondTime))
    
        
        
    def SentReplyToRecentMessageSender(self):
        """  Send message to recent message sender """
        self.Headers = {'Connection': 'keep-alive','Accept-Language':'en-IN;q=1','Content-Type':'application/json; charset=utf-8',\
                        'x-prana-version':'3','x-prana-token': self.XPranaToken,\
                        'Accept-Encoding':'gzip, deflate','Accept':'application/json','User-Agent':'vocera-vcc-enterprise/2.1.0.133 (iPad; iOS 8.1; Scale/2.00)',\
                        'Content-Length': '283','Host': 'load-vst-api.vocera.com'\

                        }
        self.Request = requests.get(self.SentReplyToRecentMessageSenderURL,
                
                data={
                        "message":"Test",
                        "threadID":1476378,
                        "metadata":{},
                        "uniqueId":str(uuid.uuid4()),
                        "from":"38105",
                        "tags":'',
                        "source":"IOSWEB",
                        "scheduled":'',
                        "priority":"0",
                        "responseChoiceId":'',
                        "attachments":[],
                        "threadSubject":"jhfhjf",
                        "secureTextReplyId":'',
                        "to":"38260"
                    
                        #"message":"\""+self.ReplyMessage+"\"",
                        #"threadID":self.MessageThreadID,
                        #"metadata":{},
                        #"uniqueId":"\""+str(uuid.uuid4()).upper()+"\"",
                        #"from":"\""+self.SelfStaffID+"\"",
                        #"tags":'',
                        #"source":"IOSWEB",
                        #"scheduled":'null',
                        #"priority":"0",
                        #"responseChoiceId":'null',
                        #"attachments":[],
                        #"threadSubject":"jhfhjf",
                        #"secureTextReplyId":'null',
                        #"to":"\""+self.SenderID+"\""
                     },
                     headers=self.Headers)
        
        print "Status: %s" %self.Request.status_code
        if (self.Request.status_code == 200):
            self.Response =  self.Request.json()
            print self.Response
            
           
            
            return 0
        else:
            return False

    def SendRespondToLatestMCRMessageViaJmeterScript(self):
        """  This method would send message to latest message recived"""
        self.ReplyMessage = 'Yes'
        
        # Create a object 
        self.JmeterAgent = CallJmeterScript("VSTUserRespondingMCRMessageRecived.jmx")
        
        # Initialize the parameter
        self.JmeterAgent.ScriptParameterDic['uniqueId'] = "'"+str(uuid.uuid4())+"'"    
        self.JmeterAgent.ScriptParameterDic['threadID'] = self.MessageThreadID
        self.JmeterAgent.ScriptParameterDic['from'] = "'"+str(self.VSTUserID)+"'"
        self.JmeterAgent.ScriptParameterDic['Recipient'] = str(self.SenderID)
        self.JmeterAgent.ScriptParameterDic['x-prana-token'] = self.XPranaToken
        self.JmeterAgent.ScriptParameterDic['Message'] = str(self.ReplyMessage)
        self.JmeterAgent.ScriptParameterDic['ThreadSubject'] = "'"+self.ThreadSubject+"'"
        self.JmeterAgent.ScriptParameterDic['responseChoiceId'] = str(self.ReplyMCRResponseID)
        self.JmeterAgent.ScriptParameterDic['replyId'] = str(self.SecureTextId)
       
        
        # Call the jmeter script 
        self.JmeterAgent.ExecuteTheScript()
        
        #print self.JmeterAgent.Cmdline
        
        os.system(self.JmeterAgent.Cmdline)
        
    def SendRespondToLatestMessageRecivedViaJmeterScript(self):
        """  This method would send message to latest message recived"""
        
        
        # Create a object 
        self.JmeterAgent = CallJmeterScript("VSTUserRespondingLatestMessageRecived.jmx")
        
        # Initialize the parameter
        self.JmeterAgent.ScriptParameterDic['uniqueId'] = "'"+str(uuid.uuid4())+"'"    
        self.JmeterAgent.ScriptParameterDic['threadID'] = self.MessageThreadID
        self.JmeterAgent.ScriptParameterDic['from'] = "'"+str(self.VSTUserID)+"'"
        self.JmeterAgent.ScriptParameterDic['Recipient'] = str(self.SenderID)
        self.JmeterAgent.ScriptParameterDic['x-prana-token'] = self.XPranaToken
        self.JmeterAgent.ScriptParameterDic['Message'] = str(self.ReplyMessage)
        self.JmeterAgent.ScriptParameterDic['ThreadSubject'] = "'"+self.ThreadSubject+"'"
       
        
        # Call the jmeter script 
        self.JmeterAgent.ExecuteTheScript()
        
        #print self.JmeterAgent.Cmdline
        
        os.system(self.JmeterAgent.Cmdline)
       
        
       
# first send a message as MCR Message from the VMP webConsole Utility Then test the reply by VST 
        
        
# Example of use 
VSTAgent = VST()

# Do login in a device 
VSTAgent.DeviceAuthenticate()
VSTAgent.CheckForNewMessage()


#print VSTAgent.CurrentMessageIndex
#print VSTAgent.SenderID
#print VSTAgent.VSTUserID
#print VSTAgent.MessageThreadID
#print VSTAgent.ReplyMessage
#print VSTAgent.ThreadSubject
#print VSTAgent.RecentMessageRecived
#print VSTAgent.SecureTextId

#VSTAgent.GetMCRResponse()


## Send Respond to MCR Respond 
#VSTAgent.SendRespondToLatestMCRMessageViaJmeterScript()

###print VSTAgent.XPranaToken
#VSTAgent.SendRespondToLatestMessageRecivedViaJmeterScript() 

## Do a checking if the message sent 
#VSTAgent.CheckForNewMessage()

#if ( VSTAgent.SenderID == VSTAgent.VSTUserID):
    #print "The Message has been sent from VST User as a respond "

#print VSTAgent.CurrentMessageIndex
#print VSTAgent.SenderID
#print VSTAgent.VSTUserID
#print VSTAgent.MessageThreadID
#print VSTAgent.ReplyMessage
#print VSTAgent.ThreadSubject
#print VSTAgent.RecentMessageRecived


####print VSTAgent.Response   
###VSTAgent.SentReplyToRecentMessageSender()  # Not working 
