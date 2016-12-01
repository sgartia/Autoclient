""" This modules contains the utility classes for Server functionality test which would be used across files"""

""" Include Section""" 

from AbCmdStore_Utility import *
import time
import os
import socket

# Global Constant session 
JAVA_HOME = "C:\\jre\\bin\\"
HOME_DIR = "C:\\Autoclient\\"
AB_HOME = HOME_DIR+"ab\\"
TEST_DATA = HOME_DIR +"testdata\\"


""" Global data for AB script run """
########################################################################
class GlobalCount :
    ObjectCount = 0
    IPStatus = {}
    BadgeIP = None
########################################################################
class IPManager:
    """ This class would manage the Virtual IP of the Machine where the script would be running"""

    @classmethod
    def Initialize_IP_Address(self):
        """initialize all the parameter"""
        IPAdresses = socket.gethostbyname_ex(socket.gethostname())[2]
        print IPAdresses
        
        # exclude the first IP from the list
        IPAdresses.pop(0)
        count = 0

        # Create the global hash to monitor the IP usages
        for IP in IPAdresses:
            count = count + 1
            GlobalCount.IPStatus[count] = {'IP': IP , 'AllocateStatus':False}     
        


   
    @classmethod
    def allocate_IP_address(self):
        """ This function would dynamically allocate the IP address"""
        GlobalCount.ObjectCount = GlobalCount.ObjectCount + 1

        GlobalCount.BadgeIP = GlobalCount.IPStatus[GlobalCount.ObjectCount ]['IP']
        GlobalCount.IPStatus[GlobalCount.ObjectCount ]['AllocateStatus'] = True 

    @classmethod
    def deallocate_IP_address(self):
        """ This function would dynamically allocate the IP address"""

        GlobalCount.BadgeIP = GlobalCount.IPStatus[GlobalCount.ObjectCount ]['IP']
        GlobalCount.IPStatus[GlobalCount.ObjectCount ]['AllocateStatus'] = False 

        
# Call The IP Manager class one 
IPManager.Initialize_IP_Address()







class AutoPhoneGlobal:
    """ These global data would be initialize before the execution of ABPhone scripts"""


    JavaPath =  None  
    ABHome = None
    ABLib = None
    GenScriptName = None
    AbPhoneLog = None
    WorkingDir = None
    WavDir = None
    JarList = None
    ServerIP = None
    OtherServerIPList = None
    DeviceIP = None        
    ApMac = None
    ClientMacID = None    
    VcgIP = None
    HttpClientHomeDir = None
    HttpClientJavaPath = None
    HttpClientLibPath = None
    HttpCientJarList = None    
    HttpClientConfigFilePath = None
    
    
    
    
    
    def __init__(self):
        """ Initialize all the Parameter """
        self.JavaPath = JAVA_HOME + "java -Xms24m -Xmx24m -Xrs128m -classpath "
        self.ABHome = AB_HOME
        self.ABLib = self.ABHome + "lib"
        self.JarList = ['slf4j-api-1.7.14.jar','logback-classic-1.1.3.jar','logback-core-1.1.3.jar']
        
        # Initialize the IP Address
        IPManager.allocate_IP_address()
        self.DeviceIP = GlobalCount.BadgeIP 
        self.ClientMacID = ''
        self.GenScriptName = self.ABHome+self.DeviceIP+"_"+self.ClientMacID+".txt"
        self.AbPhoneLog = self.ABHome+self.DeviceIP+"_"+self.ClientMacID+".csv"
        self.WorkingDir = self.ABHome+"ABJob"
        self.WavDir = self.ABHome+""
        self.ServerIP = "172.30.29.100"
        self.OtherServerIPList = self.ServerIP
        self.ApMac = "f07f06f3244f"
        self.VcgIP = "172.30.29.102"
        
        # Initialize the HttpClient paramater
        self.HttpClientJavaPath = JAVA_HOME + "java.exe -classpath "
        self.HttpClientHomeDir = HOME_DIR+"httpclient\\"
        self.HttpClientLibPath = self.HttpClientHomeDir + "lib\\"
        self.HttpClientConfigFilePath = self.HttpClientHomeDir + "config.txt"
        self.HttpCientJarList = ['server.jar','logi.crypto1.1.2.jar','httpclient-4.2.2.jar','httpcore-4.2.2.jar','httpmime-4.2.2.jar','kxml2-2.3.0.jar','commons-logging-1.1.1.jar']
       
        




   
########################################################################
class AutoPhone(object):    
    """ This class would set up the framework and avail the ab integration for the automation script"""

        # Member data for AB runs

    
    ListOfABScriptCmd = [] 
    AbCmd = None
    Agent = None
    HCmdFile = None
    ExecutionDir  = None
    CmdLine = None
    


    def  __init__(self):
        """ This constructor create instance of the AutoPhoneGlobal and initialize other variable"""
        self.Agent = AutoPhoneGlobal()
        
        # Initialize the HCmdFile
        self.HCmdFile = self.Agent.GenScriptName
        
        #Initialize the AbCmd
        self.AbCmd = ABCmdSet()
        

        


    def StartABRun (self):
        """ This methods create Required AB code in a temp AB file""" 
        
        # Open the new File in write mode 
        self.HCmdFile = open(self.Agent.GenScriptName, "w")

        
        # Write the contains of the AB file
        for cmd in self.ListOfABScriptCmd:
            self.HCmdFile.write(cmd)
            self.HCmdFile.write("\n")


        # Close the file        
        self.HCmdFile.close()

        # Create cmd line and execute the cmd
        self.CmdLine = self.GenerateABCmd()
        #print CmdLine
        
        # Assign the Expected dir
        self.ExecutionDir = AB_HOME
        
        
        #os.chdir(self.Agent.ABHome)
        fh = open("c:\\testme.txt",'a')
        fh.write(self.CmdLine)
        fh.write("\n")
        fh.close()
        

        # Execute the Ab cmd
        self.ExcuteCmd()

        # Make the application stable
        time.sleep(4)
        


    def GenerateABCmd(self):
        """ This method would generate whole set of AB cmd"""

        # Create Libary path 
        TempJarPath = ""
        OptionParam = ""
        
        for item in self.Agent.JarList:
            TempJarPath = TempJarPath + self.Agent.ABLib + "\\"+item+";"
         
        # Add the  ab.jar and server.jar in the list 
        TempJarPath = self.Agent.ABHome + "ab.jar;"+self.Agent.ABLib+"\\;"+TempJarPath+self.Agent.ABLib + "\\server.jar ab.Ab " 
        
        # Add the server name and other option 
        OptionParam = '-ipServer ' + self.Agent.ServerIP + ' -ip ' + self.Agent.DeviceIP +'  -cmd '  + self.Agent.GenScriptName\
                    + ' -csv ' + self.Agent.AbPhoneLog + ' -dir ' + self.Agent.WorkingDir + ' -wavdir ' + self.Agent.WavDir\
                    +' -apMac ' + self.Agent.ApMac + ' -mac ' + self.Agent.ClientMacID + ' -ignoreSiteResult -rtp -vcg ' + self.Agent.VcgIP \
                    + ' -phonelogdir ' + self.Agent.WorkingDir + ' -phone'
                    
        
        Cmd = self.Agent.JavaPath + TempJarPath + OptionParam
        

        return Cmd

    def ExcuteCmd (self):
        """   This method would execute the cmd in respective required folder """
        # Check for the temp folder or create one
        tempDir = HOME_DIR+"Temp"
        
        # Create if folder not present 
        if (os.path.exists (tempDir) != True):
            os.mkdir(tempDir)
        
        
        BatFileName = tempDir+"\\RunCmd.bat"
        # Create and overwrite a RunCmd.bat file 
        FH = open(BatFileName, 'w')
        FH.writelines("cd "+self.ExecutionDir+"\n")
        
        # write the cmd 
        FH.write(self.CmdLine)
        
        # close the file handle 
        FH.close()
        
        # Execute the bat file 
        os.system("start "+ BatFileName )
        
        # Make the application stable
        time.sleep(1)
        
        

    def EstablishSIPConnection(self):
        """This methods login with the Virtual auto phone  """

        # allocate the login status
        #IPManager.add_login_status(self.SelfID)

        
        self.ListOfABScriptCmd = self.AbCmd.WaitUntill


        # Start the AB script run 
        self.StartABRun()




    def DisConnectSIPConnection(self):
        """ This methods Disconnect the SIP connection"""	
        
        # command to logout
        print "yes"
        
        # This would remove the login status after logged out verification
        #IPManager.remove_login_status(self.SelfID)   
        
    def EstablishHttpClientConnection (self):
        """  This method would update the http client connection"""
        
      
        # Generate the cmd line                 
        TempJarPath = ""
        OptionParam = ""
        
        for item in self.Agent.HttpCientJarList:
            TempJarPath = TempJarPath + self.Agent.HttpClientLibPath +item+";"
            
        
        # Added the vocerahttpclient.jar
        TempJarPath = TempJarPath + self.Agent.HttpClientLibPath + "vocerahttpclient.jar message.client.VoceraHttpClient "
        
        # Add the option
        OptionParam = '-serverip ' + self.Agent.ServerIP + ' -deviceip ' + self.Agent.DeviceIP +'  -urlfilepath '  + self.Agent.HttpClientConfigFilePath
        
        # Create the complete cmd
        self.CmdLine = self.Agent.HttpClientJavaPath + TempJarPath + OptionParam
        
        # Change the dir 
        self.ExecutionDir = HOME_DIR
      
        fh = open("c:\\testme.txt",'a')
        fh.write("\n\n")
        fh.write(self.CmdLine)
        fh.close()
        
        # Execute the cmd
        os.system("start "+self.CmdLine)

        # Make the application stable
        time.sleep(2)
        

        



    
    
    
##Example of use 
#Phone1 = AutoPhone()

#print Phone1.Agent.DeviceIP

#Phone2 = AutoPhone()

#print Phone2.Agent.DeviceIP
#Phone1.EstablishSIPConnection()
#Phone1.EstablishHttpClientConnection()
#
#   


        

