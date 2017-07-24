"""  This module would able run from any machine and initiate the run in remote machine, this machine also would understand the user input"""


# Import session 
import ConfigParser
import socket
import time
import sys

# Global file section
USERCONFIG_INI = "ScalabilityRunConfig.ini"
SERVER_PORT = 8079

########################################################################
class  Controller(object):
    """   this class would initiate and controll all run"""
    UserInputSectionList = None
    ScriptList = []    
    ScriptNameVsVMList = None
    ScriptNameVsWaitTimeOnEachIteration = None
    ScriptNameVsTotalDurationRun = None
    ClientSocket = None

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        # initialize the attribute
       
        self.ScriptNameVsVMList = {}
        self.ScriptNameVsWaitTimeOnEachIteration = {}
        self.ScriptNameVsTotalDurationRun = {}
        
        # Read the User config file 
        Fh = ConfigParser.ConfigParser() 
        Fh.read(USERCONFIG_INI)      
        
        # Get the list of section from userinput file 
        self.UserInputSectionList = str(str(Fh.get('Run_VM_Setting','scriptindexlist'))).split(",")
        
        # Get the Script Name and their 
        for item in self.UserInputSectionList:
            scriptname = str(Fh.get(item,'ScriptName'))
            vmlist = str(Fh.get(item,'VMList')).split(",")
            waittime = str(Fh.get(item,'WaitTimeOnEachIteration'))
            totalduration = str(Fh.get(item,'TotalDurationRunInSec'))
            
            # Add the script name 
            self.ScriptList.append(scriptname)
                                   
            self.ScriptNameVsWaitTimeOnEachIteration[scriptname] = waittime
            self.ScriptNameVsTotalDurationRun[scriptname] = totalduration
            self.ScriptNameVsVMList[scriptname] = vmlist
            
       
            
            
    def InitiateRun(self,AgentVMIP,ScriptName,Duration,WaitTime):
        """  initiate the run """
        
        # Connect the machine 
        try:
            # initiate the socket connection 
            self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # connect the socket if the exception than check the machine
            self.ClientSocket.connect ((AgentVMIP,SERVER_PORT))
            
            # Send the cmd to initiate the run in Agent machine (
            cmd = ScriptName +" "+str(Duration)+" "+str(WaitTime)
            
            self.ClientSocket.send(cmd)
        except:
            print sys.exc_info()
            sys.exc_clear()
        
       
    
# Example of use
Test = Controller()
print Test.UserInputSectionList
print Test.ScriptList
print Test.ScriptNameVsWaitTimeOnEachIteration
print Test.ScriptNameVsVMList


#loop for each script
for script in Test.ScriptList:
    
    # loop for each target machine
    for vm in Test.ScriptNameVsVMList[script]:
        
        #get the wait time 
        wtime = Test.ScriptNameVsWaitTimeOnEachIteration[script]
        duration = Test.ScriptNameVsTotalDurationRun [script]
        print "\n***********\n"
        print script
        print wtime
        print duration
        print vm
        
        # initiate the run 
        Test.InitiateRun(vm,script,duration,wtime)
        time.sleep(2)
        print "\n****** End******\n"
        
    
