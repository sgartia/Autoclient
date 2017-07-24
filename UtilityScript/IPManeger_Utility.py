"""  This module would manage the IP"""

# Import session 
from GlobalVariable_Utility import *




class IPManager(object):
    """ This class would manage the Virtual IP of the Machine where the script would be running"""
    
    Counter = None    
    PrimeIP = None    
    AvailableIP = None
    AssignedIP = None
    NumberOfIPNeedForRun = None
    TotalNumberOfIP = None
    NumberOfReserveredIP = None
    ReserveIPList = []
    OtherIP = None
    

    
    def __init__(self):
        """initialize all the parameter"""   
        
        self.AvailableIP = []
        self.AssignedIP = ""
        self.NumberOfIPNeedForRun = 2
        self.Counter = 0
        self.CheckMaxNumber = 0
        self.NumberOfReserveredIP = 0
        
        # assign the PrimeIP
        self.PrimeIP = PRIME_IP
        self.OtherIP = []
        self.OtherIP = socket.gethostbyname_ex(socket.gethostname())[2]
        
        #Exclude the primeIP from the list
        self.OtherIP.remove(self.PrimeIP)
        
    #----------------------------------------------------------------------
    def CalculateAvailableIP(self):
        """"""
          
            
        # Intially All the IP are available 
        self.AvailableIP = self.OtherIP[self.NumberOfReserveredIP:]
        self.ReserveIPList = self.OtherIP[:self.NumberOfReserveredIP]
        
        # calculate max allocation can be done
        self.TotalNumberOfIP = len(self.AvailableIP) 
        #print "Total Number OF IP :" + str(self.TotalNumberOfIP)
        
        
    def AllocateIPAddress(self):
        """ This function would allocate the IP address"""
        self.AssignedIP = ""
        self.CalculateAvailableIP()
        
       
        # Refresh if counter touch to max limit
        
        if (self.Counter >= self.TotalNumberOfIP):
            print "Refressing List and counter"
            self.RefreshIPList()        
        
        
        # allocate the ip    
        for item in range(0,self.NumberOfIPNeedForRun,1):            
            try:
                self.AssignedIP = self.AssignedIP +" "+self.AvailableIP[self.Counter] 
                MasterRun.Agent.Log.info(" allocating IP list: "+self.AssignedIP)
                self.Counter = self.Counter + 1
                
            except IndexError:
                MasterRun.Agent.Log.info("IP address are not added hence run can n't be perform add IP and give run")
                sys.exc_clear()
                
                # Terminate the run
                self.RefreshIPList()
                
            
            
      
    def RefreshIPList(self):
        """ This function would reset the IPList"""   
        
        self.Counter = 0   
        self.AssignedIP = ""
        

## Example of Use 
#Test = IPManager()

#Test.AllocateIPAddress()
#print Test.AssignedIP

#print Test.TotalNumberOfIP

#Test.AllocateIPAddress()

#print Test.AssignedIP
#Test.AllocateIPAddress()
#print Test.AssignedIP

#print Test.AvailableIP

#Test.AllocateIPAddress()

#print Test.AssignedIP

#Test.AllocateIPAddress()

#print Test.AssignedIP                   
