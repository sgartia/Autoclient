""" This modules contains the utility classes for Server functionality test which would be used across files"""

""" Include Section""" 

from GlobalVariable_Utility import *
from BadgeCmdStore_Utility import *

class MultiRunController :
    
    ControlID = None

""" Global data for AB script run """
########################################################################
class AutoBadgeGlobal(object):
    """ These global data would be initialize before the execution of AB scripts"""
    JavaPath = None  
    ServerIP = None
    OtherServerIPList = None         
    ABHome = None
    ABJar = None    
    WavDirPATH = None
    TemABFile = None
    ApMac = None    
    TempLogDir = None
    
    
    
    
    
    #----------------------------------------------------------------------
    def __init__(self):
	"""initialize parameter"""


	self.JavaPath = JAVA_HOME+"java  -classpath "  
	self.ServerIP = VS_IP
	self.OtherServerIPList = VS_IP	       
	self.ABHome = TOOL_DIR+"AB5\\"
	self.ABJar = self.ABHome+"ab.jar"	
	self.WavDirPATH = AB_HOME+"WavFiles"	
	self.ApMac = " -apMac ff11111111ff " 	
	self.TempLogDir = AB_HOME+"Temp\\"


########################################################################
class AutoBadge(object):
    """ This class would set up the framework and avail the ab integration for the automation script """

    # Member data for AB runs
    TestScriptName = None
    temp = None
    AbLogName = None
    ListOfABScriptCmd = []
    ExpectedLinesInlogs = []
    SelfID = None
    BadgeIP = None
    AbCmd = None
    ABGlobal = None   
    WaitTimeAfterLogin = None
    CallIntervalTime = None
    ABRunPid = 0
    ABCmdTimeOut = None
    DeviceMac = None
    
    

    def  __init__(self,IP):
        """ This constructor would verify the required environment setup"""
	
	## Initiate this object for all prompt and command 
	self.ABGlobal = AutoBadgeGlobal()
	
	## logic needs to put to find server version and accordlying initialize
	self.AbCmd = ABCmdSet()
	
	# Initialize object ID 
	self.SelfID = id(self)
	MultiRunController.ControlID = self.SelfID
	
	        
        # Assign the globalbatch to local class attribute
        self.BadgeIP = IP
	
	# Change the tempAb file
	self.ABGlobal.TemABFile = self.ABGlobal.TempLogDir+str(IP)+"_"+"TempAb.ab"
	
	# Initialize the call waiting time and Time Interval
	self.WaitTimeAfterLogin = 60
	self.CallIntervalTime = 40
	self.ABCmdTimeOut = 250
	
    
        
    def StartABRun (self):
        """ This methods create Required AB code in a temp AB file""" 

        # Initiate and generate unique log file based on AB test case
        temp = datetime.datetime.now()
        self.AbLogName = self.ABGlobal.TempLogDir + self.BadgeIP+"_"+ temp.strftime("%Y_%m_%d_%H_%M")+".out"
	# Create AB file and print the contain from the listOfABScriptCmd
	ABfile = self.ABGlobal.TemABFile
	HAbFile = open(ABfile, "w")
	
	 # Write the contains of the AB file
	for cmd in self.ListOfABScriptCmd:
	    HAbFile.write(cmd)
	    HAbFile.write("\n")
	    


	# Close the file        
	HAbFile.close()

	# Create cmd line and execute the cmd
	CmdLine = self.GenerateABCmd()
	print CmdLine
	
	if ( self.ABRunPid == 0):
	    os.system("start \""+str(self.BadgeIP)+"\" cmd /c "+ CmdLine )
	    time.sleep(2)
	else:
	    counter = 0
	    flag = True
	    while ( flag == True) and (counter < self.ABCmdTimeOut):
		if psutil.pid_exists(int(self.ABRunPid)):
		    flag = True
		    time.sleep(10)
		    counter = counter + 10
		    print " I am waiting "+ str(counter)+" sec"
		    
		else:
		    flag = False
		    os.system("start \""+str(self.BadgeIP)+"\" cmd /c "+ CmdLine )
		    time.sleep(2)
		
		
# 
	# Get the pid of the window
        #try:
            #tempvalue = ""
            ##self.ABRunPid = str(str(str(os.popen("TASKLIST /FI \"WINDOWTITLE eq "+str(self.Agent.ClientMacID)+"\"").read()).split("cmd.exe")[1]).split("RDP-Tcp#0")[0]).strip()
            #tempvalue = str(os.popen("TASKLIST /FI \"WINDOWTITLE eq "+str(self.BadgeIP)+"\"").read()).split("cmd.exe")[1]
            ##MasterRun.Agent.Log.info(str(tempvalue))
            #if (str(tempvalue).find("RDP-Tcp#0") != -1):
                #self.ABRunPid = str(str(tempvalue).split("RDP-Tcp#0")[0]).strip()
                #MasterRun.Agent.Log.info("AB PID :" + str(self.ABRunPid))
            #elif (str(tempvalue).find("Console") != -1):
                #self.ABRunPid = str(str(tempvalue).split("Console")[0]).strip()
                #MasterRun.Agent.Log.info("AB PID :" + str(self.ABRunPid))
        
        #except:
            #print sys.exc_info()
            #sys.exc_clear()
	#print self.ABRunPid

 



    def GenerateABCmd(self):
        """ This method would generate whole set of AB cmd"""
    
	return self.ABGlobal.JavaPath +  self.ABGlobal.ABJar + "; ab.Ab " + " -ipServer "+ self.ABGlobal.ServerIP + " -ip " + self.BadgeIP \
	       + " -cmd " + self.ABGlobal.TemABFile + " -out " + self.AbLogName + " -dir " + self.ABGlobal.ABHome + " -log 5 -wavdir " + \
	       self.ABGlobal.WavDirPATH + self.ABGlobal.ApMac + " -mac "+self.DeviceMac+"  -rtp " # " -logout"   
                    
	       
	       
    def CompareLogs(self):
        """ This methods would verify the log with expected value"""
        LengthOfExpectedCmdList=  len(self.ExpectedLinesInlogs)
        index = 0
        MatchCount = 0
        ActualMatch = []
        #print self.AbLogName
        # Open the log file 
        ReadLog = open (self.ABGlobal.ABHome + "\\" +self.AbLogName,"r")

        # Read the log file and Store contain in array
        for line in ReadLog.readlines ():

            if (index < LengthOfExpectedCmdList):

                # match the pattern
                m = re.search(self.ExpectedLinesInlogs[index], line, re.IGNORECASE)
		
                # Check if it not matched  
                if m != None:
                    ActualMatch.append(self.ExpectedLinesInlogs[index])
                    index = index + 1
                    MatchCount = MatchCount + 1

        # Close the file handle    
        ReadLog.close ()
        return ActualMatch
    
    
    
    
  
    def Login(self): 
	
		
	# do login, accept call, 
	self.ListOfABScriptCmd = self.AbCmd.UntillPrompt(Prompt.dummy_foo1,self.WaitTimeAfterLogin) 
	self.StartABRun()
    
    def Wait (self):
	
	self.ListOfABScriptCmd = self.AbCmd.Untill() 
	self.StartABRun()
    
    
    
    def Call(self,CalleeName):
	
	
	# Do log out if its already login then do login   make call to another user and Wait for some time 
	self.ListOfABScriptCmd = self.AbCmd.CallUser(CalleeName) + self.AbCmd.UntillPrompt(Prompt.dummy_foo1,self.CallIntervalTime)  + self.AbCmd.Call + self.AbCmd.UntillPrompt(Prompt.dummy_foo1,self.AbCmd.WaitTime)
	self.StartABRun()	
    
    def LoginWaitAndPlayTextMessage (self):
	
	# Do log out if its already login then do login   make call to another user and Wait for some time 
	self.ListOfABScriptCmd = self.AbCmd.UntillPrompt(Prompt.dummy_foo1,self.WaitTimeAfterLogin) +self.AbCmd.Call + self.AbCmd.Play(WavfileFor.PlayTextMessages)+self.AbCmd.UntillPrompt(Prompt.dummy_foo1,self.AbCmd.WaitTime)
	self.StartABRun()
	
  
    def LogOut(self):
	"""Do log out"""
	self.ListOfABScriptCmd = self.AbCmd.LogOut
	self.StartABRun()