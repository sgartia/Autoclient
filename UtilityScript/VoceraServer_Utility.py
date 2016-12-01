"""  This module would contains all the method related to VMP """

import requests
import urllib
import urllib2
import sys

values = {'login' : 'Administrator',
                 'password' : 'admin'
                  }
      
try:            
    data = urllib.urlencode(values)
    req = urllib2.Request("http://172.30.29.100/console/adminindex.jsp", data)
    check = str(urllib2.urlopen(req).read())
    print check
    
    if ( check == -1):
        print "yes"
    elif (check > 0):
        print "NO"              
        
except:
    print ";lj;ljj"
    print sys.exc_info()
    if (str(sys.exc_type).find('urllib2.URLError') > 0):
        print  "You have enter Wrong Server URL"
        sys.exc_clear()
        print "nothing"





exit ()
class VSEnvClass(object):
    
    VmpEndpoint = None
    headers = {}
    
    def __init__(self):
        """ Assign the parameter"""
        
          
        headers = {
                    'Referer': 'http://172.30.29.100/console/adminindex.jsp',
                    'Accept-Language': 'en-US',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/html, application/xhtml+xml, */*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Pragma':'no-cache',
                    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0'
            }
        
class VS(object):
    """  This class contains all the method related to VMP"""
   
    WebLoginURL = None
    MaintainSessionIDUrl = None
    ContinueSessionIDUrl = None 
    SendMessageUrl = None
    VSEnv = None

    
    Sid = None
    TimeZone = None
    SessionID = None    
    VSSend = None

    def __init__(self):
        """  this method would initialize the VMP parameter """
     
        self.WebLoginURL = 'http://172.30.29.100/console/AdminController'
        self.VSEnv = VSEnvClass()

        

    def WebLogin(self):
        
        Session =  requests.session()
        
        self.VSSend = requests.post(
                    self.WebLoginURL,
                    data={   
                            'login':'Administrator',    #'testone',
                            'password':'admin',  #'vocera',
                            'sessionid':Session
                            
                           
                         },
                    headers=self.VSEnv.headers,
                    verify=False)
        print "Status: %s" %self.VSSend.status_code
        if (self.VSSend.status_code == 200):
            #LoadRun.Log.info( "Autheticated to VMP webconsole successfully Username : "+str(self.SenderLogin))
            print self.VSSend.content            
            
           
            #self.SessionID = str(str(str(self.VmpSend.text).split(",")[0]).split(":")[1]).strip("\"")
            #print message
            return True
        else:
            
            #LoadRun.Log.info( "It failed to login VMP Web Console for the user : "+str(self.SenderLogin))
            return False
      

# Example of use
Test = VS()
Test.WebLogin()