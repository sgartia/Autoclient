"""  This module would contain all the Method for VMP device opeartion"""

from GlobalVariable_Utility import *
from JmeterScriptCall_Utility import *



class VS(object):
    """  This class contains all the method related to VS"""
   
    # Vocera server  Information 
    VSURL = None    

    # User information
    UserID = None
    LoginPassword = None
    VSSendHandle = None 
   
    # Environment variable
    CurrentTime = None
    AuthDateTime  = None
    Nonce = None
    MAC = None
    DeviceType = None
    
    Headers = None
    


    def __init__(self):
        """  this method would initialize the VMP parameter """      

        # initializing the URL
        self.VSURL = "http://"+VS_IP+":80" + "/console/UnifiedSmartphoneService"
        
                
        
        ## Initialize the User name and password
        #self.UserLoginID = 'TestH035324'
        self.LoginPassword = 'vocera'
        self.DeviceType = 'iOS'
        
        
        # Initialize Mac ID 
        self.MAC = 'aaa000000002'
        
     
    def GetCurrentTime(self):
        """  This method generate the current time"""
        
        # initialize the Current time 
        self.CurrentTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
   
        
    def InitializeHeader (self):
        """   This method is to initialize the header """
        self.Nonce = ''.join(random.choice(string.digits) for _ in range (9))
        self.AuthDateTime = datetime.datetime.now().strftime('%m%d%H%M%S')
        
        
        
        self.Headers = {
                   
                   'Accept-Language': 'en-US',  
                   'nonce': self.Nonce,  
                   'Accept': '*/*',     
                   'authdatetime': self.AuthDateTime,  
                   'Keep-Alive': 'timeout=1, max=1',  
                   'user': self.UserID, 
                   'Accept-Encoding': 'gzip, deflate',
                   'User-Agent': 'VCS/3.0.3.524 (iOS 9.3.5)'
                   }
        
        
        
    
       
    def PingVS(self):
        """  This request ping the vocera server"""
        
        # Intialize the Header
        self.InitializeHeader()
      
        
        # Get the options
        self.VSSendHandle = requests.get(
                    self.VSURL,
                    params ={                              
                            'userid':self.UserID,                               
                            'formAction':'ping', 
                            'appid':'VB',                               
                            'appVersion':'3.0', 
                            'deviceType':self.DeviceType,                               
                            'deviceID':self.MAC                            
                            
                         },
                    headers=self.Headers,
                    verify=False)
        print "Status: %s" %self.VSSendHandle.status_code
        if (self.VSSendHandle.status_code == 200):
            print  " successfully ping the vocera server "
            print self.VSSendHandle.text
            
            return True
        else:
            
            print "It failed to successfully ping the vocera server "
            return False

    
    def CloseCometConnection(self):
        """  This request ping the vocera server"""
        
        # Intialize the Header
        self.InitializeHeader()
      
        
        # Get the options
        self.VSSendHandle = requests.get(
                    self.VSURL,
                    params ={                              
                            'userid':self.UserID,                               
                            'formAction':'closeCometConnection', 
                            'appid':'VB',                               
                            'appVersion':'3.0', 
                            'deviceType':self.DeviceType,                               
                            'deviceID':self.MAC                            
                            
                         },
                    headers=self.Headers,
                    verify=False)
        print "Status: %s" %self.VSSendHandle.status_code
        if (self.VSSendHandle.status_code == 200):
            print  " successfully close the comet connection of the vocera server "
            print self.VSSendHandle.text   
            
            return True
        else:
            
            print "It failed to close the comet connection of the vocera server "
            return False


##Example of use

#VSAgent = VS()
#time.sleep(1)
#VSAgent.UserID = "u-00_0"
#VSAgent.PingVS()
#VSAgent.CloseCometConnection()
