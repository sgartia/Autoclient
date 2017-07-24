""" This modules contains the utility classes for Server functionality test which would be used across files"""

""" Include Section""" 
from GlobalVariable_Utility import *
from AbCmdStore_Utility import *
from IPManeger_Utility import *



class AutoPhoneGlobal:
    """ These global data would be initialize before the execution of ABPhone scripts"""


    JavaPath =  None  
    ABHome = None
    ABLib = None
    ABTempDir = None
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
    
    
    
    
    
    def __init__(self,BadgeIP):
        """ Initialize all the Parameter """
        self.JavaPath = JAVA_HOME + "java -Xms24m -Xmx24m -Xrs128m -classpath "
        self.ABHome = AB_HOME
        self.ABTempDir = self.ABHome + "Temp\\"
        self.ABLib = self.ABHome + "lib"
        self.JarList = ['slf4j-api-1.7.14.jar','logback-classic-1.1.3.jar','logback-core-1.1.3.jar']
        
        # Initialize the IP Address
        
        self.DeviceIP = BadgeIP
        self.ClientMacID = ''
        self.GenScriptName = self.ABTempDir+self.DeviceIP+"_"+self.ClientMacID+".txt"
        self.AbPhoneLog = self.ABTempDir+self.DeviceIP+"_"+self.ClientMacID+".csv"
        self.WorkingDir = self.ABHome+"ABJob"
        self.WavDir = self.ABHome+"WavFiles"
        self.ServerIP = VS_IP
        self.OtherServerIPList = self.ServerIP
        self.ApMac = "f07f06f3244f"
        self.VcgIP = VCG_IP
        
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
    HttpClientPid = None
    ABRunPid = None
    
    


    def  __init__(self,IP):
        """ This constructor create instance of the AutoPhoneGlobal and initialize other variable"""
        self.Agent = AutoPhoneGlobal(IP)
        
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
        fh = open("testme.txt",'a')
        fh.write("\n")
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
        os.system("start \""+str(self.Agent.ClientMacID)+"\" cmd /c "+ BatFileName )
        
        # Make the application stable
        time.sleep(1)
        
        # Get the pid of the window
        try:
            tempvalue = ""
            #self.ABRunPid = str(str(str(os.popen("TASKLIST /FI \"WINDOWTITLE eq "+str(self.Agent.ClientMacID)+"\"").read()).split("cmd.exe")[1]).split("RDP-Tcp")[0]).strip()
            
            MasterRun.Agent.Log.info("CommandTogetPID:" + "TASKLIST /FI \"WINDOWTITLE eq "+str(self.Agent.ClientMacID)+"\"")                                     
            tempvalue = str(os.popen("TASKLIST /FI \"WINDOWTITLE eq "+str(self.Agent.ClientMacID)+"\"").read()).split("cmd.exe")[1]
            print tempvalue
            MasterRun.Agent.Log.info(str(tempvalue))
            if (str(tempvalue).find("RDP-Tcp") != -1):
                self.ABRunPid = str(str(tempvalue).split("RDP-Tcp")[0]).strip()
                MasterRun.Agent.Log.info("AB PID :" + str(self.ABRunPid))
            elif (str(tempvalue).find("Console") != -1):
                self.ABRunPid = str(str(tempvalue).split("Console")[0]).strip()
                MasterRun.Agent.Log.info("AB PID :" + str(self.ABRunPid))
        
        except:
            print sys.exc_info()
            sys.exc_clear()
        
    def UpdateTheVSIPinConfigFile(self):
        """This methods would update the config file for http client connection  """
        PatternForUrl = "COMETURL.0.urlPath=http://"
        
                
        # read the file and get the  ip Need to be replace
        with open(self.Agent.HttpClientConfigFilePath,'r') as f:
            newlines = []
            for line in f.readlines():
                #print line
                if (str(line).find(PatternForUrl) != -1):
                    existingIP = str(str(line).split(PatternForUrl)[1]).split("/")[0]
                    newlines.append(line.replace(existingIP, VS_IP))
                else:
                    newlines.append(line)
        
        # Update the file with new IP and other data 
        with open(self.Agent.HttpClientConfigFilePath, 'w') as f:
            for line in newlines:
                f.write(line)
        
        # Log the update the config file for http client connection 
        MasterRun.Agent.Log.info("Update the VS server IP in config file of http client connection tool")
        
      

    def EstablishSIPConnection(self):
        """This methods login with the Virtual auto phone  """

        # allocate the login status
        #IPManager.add_login_status(self.SelfID)

        
        self.ListOfABScriptCmd = self.AbCmd.WaitUntill


        # Start the AB script run 
        self.StartABRun()
        
        # Establish SIP Connection   
        MasterRun.Agent.Log.info("Establish SIP Connection for Mac ID : "+str(self.Agent.ClientMacID)+" ProcessID :"+str(self.ABRunPid))
        


    def EstablishSIPConnectionAndHandleCalling(self):
        """This methods login with the Virtual auto phone and handle calling """


        
        self.ListOfABScriptCmd = self.AbCmd.CallAndWait


        # Start the AB script run 
        self.StartABRun()
        
        # Establish SIP Connection
        MasterRun.Agent.Log.info("Establish SIP Connection for calling for MacID : "+str(self.Agent.ClientMacID)+" ProcessID :"+str(self.ABRunPid))

    def DisConnectSIPConnection(self):
        """ This methods Disconnect the SIP connection"""	
        
        # command to logout
        print "yes"
        
        # Disconnect SIP Connection
        MasterRun.Agent.Log.info("Disconnect SIP Connection for MacID : "+str(self.Agent.ClientMacID)) 
        
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
      
        fh = open("testme.txt",'a')
        fh.write("\n\n")
        fh.write(self.CmdLine)
        fh.close()
        
        # Execute the cmd
        os.system("start \""+self.Agent.DeviceIP+"\" "+self.CmdLine)
        time.sleep(.5)
        
        # Get the pid of the window
        try:
            MasterRun.Agent.Log.info("CommandTogetPIDofIP:" + "TASKLIST /FI \"WINDOWTITLE eq "+str(self.Agent.DeviceIP)+"\"")  
            value = ""
            value = str(os.popen("TASKLIST /FI \"WINDOWTITLE eq "+str(self.Agent.DeviceIP)+"\"").read()).split("java.exe")[1]
            #print value
            MasterRun.Agent.Log.info("value: " + str(value))
            if (str(value).find("RDP-Tcp") != -1):
                MasterRun.Agent.Log.info("I am spliting with RDP-Tcp")
                self.HttpClientPid = str(str(value).split("RDP-Tcp")[0]).strip()
                MasterRun.Agent.Log.info("Http Client Pid : " + str(self.HttpClientPid))
            elif (str(value).find("Console") != -1):
                self.HttpClientPid = str(str(value).split("Console")[0]).strip()
                MasterRun.Agent.Log.info("Http Client Pid : " + str(self.HttpClientPid))
                
        
        except:
            print sys.exc_info()
            sys.exc_clear()
        
        # Establish Http Client Connection 
        MasterRun.Agent.Log.info("HttpClient Connection for MacID : "+str(self.Agent.ClientMacID)+" ProcessID :"+str(self.HttpClientPid))
        time.sleep(.5)
    
    
        
        
## Example of use

## Example to update the config file
#Phone1 = AutoPhone(GlobalCount.BadgeIP)
##Phone1.UpdateTheVSIPinConfigFile()


##IPManager.Initialize_IP_Address()
##IPManager.allocate_IP_address()
###GlobalCount.BadgeIP = '172.30.26.140'
###Phone1 = AutoPhone('172.30.26.140')
##
##
###print Phone1.Agent.DeviceIP
###Phone1.Agent.ClientMacID = 'aaa033333333'
###Phone1.EstablishSIPConnection()
###Phone1.EstablishHttpClientConnection()
##print "I am end"

##exit ()



        

