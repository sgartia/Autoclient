"""    This would create VS user list to import """
from GlobalVariable_Utility import *
from SQLDB_Utility  import *


########################################################################
class  CreateUser(object):
    """"""
    FirstName = None
    LastName = None
    LastNamePreFix = None
    UserId = None
    Password = None
    EmailID = None
    Site = None  
    PrefixMac = None
    BadgeID =  None
    HomeDir = None 
    DataDir = None
    
    NumberOfUserTobeCreate = None    
    UserDetails = None
    UserLoginCSVFilePath = None
    VSAndMACIDFilePath = None
    VMPAndIDFilePAth = None
    FinalDataFile = None
    SampleDataFileForCallingScenario = None
    
    MapVSAndVMPUserDetails = {}
    
  
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.HomeDir =  HOME_DIR
        self.DataDir =  USER_INFO
        
        self.Password = "vocera"        
        self.UserLoginCSVFilePath = self.DataDir+"UserLogin.csv"
        self.FirstName = "Test"
        self.LastNamePreFix = ""
        self.PrefixMac = ""
        self.Site = "Global"
        
        # initilize the file         
        self.VMPAndIDFilePAth = self.DataDir+"VMPUserName.csv"
        self.FinalDataFile = self.DataDir+"FinalDataFile.csv"
        self.SampleDataFileForCallingScenario = self.DataDir+"SampleDataFileForCallingScenario.csv"
        
        FinalCallingDataList = []
        
        
        
    def GenerateVSUserDetails(self):
        
        Fh = open(self.UserLoginCSVFilePath,'w')
        
        for item in range(1,self.NumberOfUserTobeCreate,1):            
            self.LastName = self.LastNamePreFix+str(item)
            self.UserId = str(self.FirstName+self.LastName)
            self.EmailID = self.UserId+"@vocera.com"
            tempBadgeID = self.PrefixMac[:-len(str(item))]            
            self.BadgeID = str(tempBadgeID)+str(item)     
            temp = self.UserId+","+self.LastName +","+self.FirstName+",,"+self.EmailID+",,,,,,,"+self.BadgeID+",,,,,"+self.Site+",,,,\n"
            
            
            # Write in a file 
            Fh.write(temp)
       
      
        # Close the file handle
        Fh.close()
    
    def MapVMPAndVSUser(self):
        """   this method would map the VCS and VS user"""
        # create  a VSVSAndMACIDFile  from the UserLogin.csv file  first 
        
      
        vsdetails = {}
        vsname = None
        fh = open(self.UserLoginCSVFilePath,'r')
        alllines = fh.readlines()
        for item in alllines:
            temp  = str(item).split(",")
            vsname = temp[0]
            macid = str(temp[11]).strip("\n")
            self.MapVSAndVMPUserDetails [vsname] = {}
            self.MapVSAndVMPUserDetails[vsname]['MacId'] = macid
            
            
        print self.MapVSAndVMPUserDetails
        vmpdetails = {}
        vcsusename = None
        VMPLoginId = None
        
        fh = open(self.VMPAndIDFilePAth,'r')
        alllines = fh.readlines()
        for item in alllines:
            temp  = str(item).split(",")
            vcsusename = temp[0]
            vmpid = str(temp[1]).strip("\n")
            print vcsusename
            print vmpid
            
            if dict(self.MapVSAndVMPUserDetails).has_key(vcsusename):
                self.MapVSAndVMPUserDetails[vcsusename]['vmpid'] = vmpid
                
                
        # write the all details in file 
        FH = open(self.FinalDataFile,"w")
        for key in self.MapVSAndVMPUserDetails:
            try:
                FH.write(key+","+str(self.MapVSAndVMPUserDetails[key]['MacId'])+","+str(self.MapVSAndVMPUserDetails[key]['vmpid'])+"\n")
            except:
                sys.exc_clear()
            
            
        return 0    
            
           
    #----------------------------------------------------------------------
    def CreateDataSetForCallingScenario(self):
        """  this method is to create data set for the calling scenario"""
        
        # Read the VMP DB 
        SQLAgent = SQLServer()
        SQLAgent.ConnectToDB()
        
        # Assign the first name of the user 
        SQLAgent.VMPUserFirstName = self.FirstName
        
        # Get the VCS and VS ID and VMP ID
        SQLAgent.GetVCSUserLoginVSIDAndVMPIDForCalling()
        
        # Close the connection
        SQLAgent.CloseConnection()
        
        print GlobalDBVariable.VmpIdVSIdVCSLogin
        
        # Read the final document that contains VCS login , MAC ID and VMP ID
        fh = open(self.FinalDataFile,'r')
        AllData = fh.readlines()
        fh.close()
        
        VCSIdAndMac = {}
        for item in AllData:
            temp = str(item).split(",")
            VCSIdAndMac[temp[0]] = temp[1]
        
        # Prepare calling sample set 
        Test = GlobalDBVariable.VmpIdVSIdVCSLogin
        for key in Test:
            try:
                GlobalDBVariable.VmpIdVSIdVCSLogin[key]['MAC'] = VCSIdAndMac[GlobalDBVariable.VmpIdVSIdVCSLogin[key]['VCSlogin'] ]
            except:
                sys.exc_clear()
            
            
            
        # Write the sample data in a file 
        FH = open(self.SampleDataFileForCallingScenario,'w')
        for key in GlobalDBVariable.VmpIdVSIdVCSLogin:
            if dict(GlobalDBVariable.VmpIdVSIdVCSLogin[key]).has_key('MAC'):
                line = GlobalDBVariable.VmpIdVSIdVCSLogin[key]['VCSlogin']+","+GlobalDBVariable.VmpIdVSIdVCSLogin[key]['MAC']+\
                     ","+GlobalDBVariable.VmpIdVSIdVCSLogin[key]['VSID']+","+str(GlobalDBVariable.VmpIdVSIdVCSLogin[key]['VMPID'])+"\n"
                FH.writelines(line)
                
        FH.close()       
        
            

        
                
        
        
##Example of use 

## Step 1  :   This is  step to create VS user import file 
## step 1 :    starts here - uncomment the below code 
#data = CreateUser()
#data.PrefixMac = "aaa000880000"
             
 
#data.FirstName = "DL"
#data.LastNamePreFix = ""

## Uncomment to generate Import file for VS
#data.NumberOfUserTobeCreate = 25
#data.GenerateVSUserDetails()
## step 1 :    Ends here - ***********
## step 1 :    Ends here - ***********

## Step 2 :   Manually import the .C:\Autoclient\UserInfo\UserLogin.csv file in Vocera server and check the VMP user \
## Step 2 :   Synchronization happens 

## Step 3 :   This code would create the VMP login to all the VS user 
## Step 3 :   Synchronization happens 

## Connect the SQL Server 
#SQLAgent = SQLServer()
#SQLAgent.ConnectToDB()

## Initialize the user first name and number of user
#SQLAgent.VMPUserFirstName = "DL"
#SQLAgent.VMPUserLastNamePrefix = ""
#SQLAgent.NumberOfRowNeedToUpdate = 25

## Call this method after sync the data 
## Method to creae VMP Login After VS user got sync
#SQLAgent.CreateVMPLogin ()

## Close the connection 
#SQLAgent.CloseConnection()

## step 3 :    Ends here - ***********
## step 3 :    Ends here - ***********

##Step 4 :   This code would update the permission of chat and call and notification stuff
##Step 4 :   starts here - uncomment the below code 
##Step 4 :   starts here - uncomment the below code 

## Connect the SQL Server 
#SQLAgent = SQLServer()
#SQLAgent.ConnectToDB()

## Initialize the user first name and number of user
#SQLAgent.VMPUserFirstName = "DL"
#SQLAgent.VMPUserLastNamePrefix = ""

## Method to create the Update Chat Msg Notification Call Permission
#SQLAgent.UpdateChatMsgNotificationCallPermission()
#SQLAgent.CloseConnection()
## Initialize the class to use method
#data = CreateUser()

## Create a data file containing VMPUser Name and ID
#fh = open(data.VMPAndIDFilePAth,'w')
    
#for keys in  GlobalDBVariable.VCSUserNameAndID:
    #fh.write(keys+","+str(GlobalDBVariable.VCSUserNameAndID[keys])+"\n")
#fh.close()
	    
## This code would MAP the VMP login User with VS user and create a data Set File for various test data sample
## Basically getting data from Db and writedown in file for Testdata for execution of automation script
#time.sleep(5)  # Wait timefor IO


## step 4 :    Ends here - *********** 
## step 4 :    Ends here - ***********   

## Step 5 :   This code would create data set for calling scenario
## Step 5 :   starts here - uncomment the below code 
## Step 5 :   starts here - uncomment the below code 


## Initialize the class to use method
#data = CreateUser()

###Run this method to create Finaldata set that contain login ID and mac ID 
#data.MapVMPAndVSUser()


#data.FirstName = "DL"

##run the  CreateDataSetForCallingScenario  () to sample data for calling scenario
#data.CreateDataSetForCallingScenario()

##step 5 :    Ends here - *********** 
##step 5 :    Ends here - ***********   
    
    