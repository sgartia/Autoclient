"""   This module control the run in VM manage IP and process """

from GlobalVariable_Utility import *
from IPManeger_Utility import *
from ABPhone_Utility import *

########################################################################
class  RunManager(object):
    """This module control the run in VM manage IP and process"""
    
    
    IPAgent = None
    ScriptName = None
    IntervalOnEachRecordRun = None
    DataFileName = None
    AllRecordInfo = None
    CurrentRecord = None
    LongCmd = None
    TotalRunDuration = None   
    NumberOfIterationForEachRecord = None
    TotalNoOfRecord = None    
    TotalRecordToCompleteRun = None
    DelayAfterEachIteratioRunToStableSysytem = None
    IteratorHandleForDataSet = None
    CounterForCleanState = None
    OwnPythonID = None
    AgentListenerAndRunManagerPIDList = None
    PidMonitor = None
    
    
    
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        # Get the PID 
        self.OwnPythonID = os.getpid() 
        # Add Me in the file 
        self.PidMonitor = RemeberPID(self.OwnPythonID)
        self.PidMonitor.AppendMe()
        MasterRun.Agent.Log.info(" Added My PID in Monitor file :"+str(self.OwnPythonID))
        
        
        # Intialize the Script needs to run 
        #print sys.argv
        self.ScriptName = sys.argv[1]
        self.TotalRunDuration = int(sys.argv[2])
        self.IntervalOnEachRecordRun = int(sys.argv[3])
        
        
        
        # Initiate the IPmanager class
        self.IPAgent = IPManager()
        self.IPAgent.NumberOfIPNeedForRun = SCRIPT_NAME_AND_IP_REQUIREMENT[self.ScriptName]
        
        
        # Get the data file for the script
        path = TEST_DATA + SCRIPT_NAME_AND_DATA_FILE[self.ScriptName]+"_"+HOST_NAME+".csv"
        
        if (os.path.exists(path)):             
            self.DataFileName = TEST_DATA + SCRIPT_NAME_AND_DATA_FILE[self.ScriptName]+"_"+HOST_NAME+".csv"
        else:
            self.DataFileName = TEST_DATA + SCRIPT_NAME_AND_DATA_FILE[self.ScriptName]+".csv"
        
        
        # Get the number of record available 
        fh = open(self.DataFileName,'r')
        self.AllRecordInfo = fh.readlines()
        fh.close()
        
        # pop up the header 
        self.AllRecordInfo.pop(0)
        self.TotalNoOfRecord = len(self.AllRecordInfo)
        
        # Initialize the record set 
        self.TotalRecordToCompleteRun = (self.TotalRunDuration / int(self.IntervalOnEachRecordRun)) + 1
        self.IteratorHandleForDataSet = iter(self.AllRecordInfo)
        self.CounterForCleanState = 0

    def __GetProcessList(self,process_name):
        temp = []
        for item in os.popen('tasklist').read().splitlines()[4:]:
            val = item.split()
            if process_name in val:
                temp.append(int(val[1]))   
        return temp
                
    
    def __CleanAndResetVM(self,process_name):
        """  Kill all the Java and python process"""      
      
        AllPid = []
        
        
        AllPid = self.__GetProcessList(process_name)
        
        
        MasterRun.Agent.Log.info(" Initiating a Clean State of the TestVM ")
        
        # Remove the own Python ID and Cmd Pid from the list
        self.AgentListenerAndRunManagerPIDList = self.PidMonitor.GetAllPIDList()
        #print "*************"
        #print AllPid
        #print self.AgentListenerAndRunManagerPIDList
        #print "*************"
        
        for item in self.AgentListenerAndRunManagerPIDList:
            if int(item) in AllPid:
                print "yes"
                AllPid.remove(int(item))
                    
        for item in  AllPid:
            #print psutil.pid_exists(item)
            try:
                if (psutil.pid_exists(item)):                    
                    cmd = "TASKKILL /F /FI \"PID eq "+str(item)+"\""
                    MasterRun.Agent.Log.info(" Killing PID :"+ str(item)+"")
                
                    os.system(cmd)
                    time.sleep(2)
                
            except:
                print "exception in killing pid:"+ str(sys.exc_info())
                sys.exc_clear()
                
    def KillAllJavaPythonCmdProcess(self):
        """  Call __CleanAndResetVM """
        
        # clean all Java process
        self.__CleanAndResetVM('java.exe')
        
        # clean all Python Process
        self.__CleanAndResetVM('python.exe')
        
        # clean all Javaerror Process
        self.__CleanAndResetVM('WerFault.exe')
        
        

        
    def GetCurrentDataRecord(self):
            
        try:
            data = next(self.IteratorHandleForDataSet)
            
        except StopIteration:
            
            # Delete the current object and refresh the list
            del self.IteratorHandleForDataSet
            
            self.IteratorHandleForDataSet = iter(self.AllRecordInfo)
            
            # Point the record set from the beginning
            data = next(self.IteratorHandleForDataSet)
            
            # Clean the exception 
            sys.exc_clear()
                
        
            
        # Process the record set and split it indiviusal argument
        temp = str(data).strip("\n").split(",")              
        self.CurrentRecord = ""
        for item in temp:
            self.CurrentRecord = self.CurrentRecord + item + " "
        
    
    def GenerateAndExcuteCmd (self):
        
        # Check if clean state is needed or not
        if (self.CounterForCleanState > SCRIPT_NAME_AND_MAXRUN_NONSTOP[self.ScriptName]):
            
            print "Waiting to clean all the process "
            time.sleep(SCRIPT_NAME_AND_WAITTIME_KILLPID[self.ScriptName])
            
            self.KillAllJavaPythonCmdProcess()
            
            # Wait till all the process get kill
            print "Waiting to statble run "
            time.sleep(SCRIPT_NAME_AND_WAITTIME_KILLPID[self.ScriptName])
            
            # Initialize the counter to o 
            self.CounterForCleanState = 0
        
        
        # initiate the run 
        self.IPAgent.AllocateIPAddress() 
       
        self.LongCmd = "start " +PYTHON_PATH+ SCRIPT_DIR + self.ScriptName +" "+ self.IPAgent.AssignedIP + " " + self.CurrentRecord
        print self.LongCmd
        
        # Execute the cmd 
        os.system(self.LongCmd)
        self.CounterForCleanState = self.CounterForCleanState + 1
        
     
        
    def UpdateFrameworkAndTool(self):
        
        # Update the config file for http client 
        TestAgent = AutoPhone(PRIME_IP)
        TestAgent.UpdateTheVSIPinConfigFile()  
        
    def LoopForAllTheRecord(self):
        """  This would loop all record for all iterations"""
        
        # loop for Number of iteration 
        for iterationloop in range(0,self.TotalRecordToCompleteRun,1):            
            
                
                # Get the current data set 
                self.GetCurrentDataRecord()
                    
                # Execute the script 
                self.GenerateAndExcuteCmd()
                
                # Wait interval between two record run 
                time.sleep(self.IntervalOnEachRecordRun)
            
            
   
        
    def __del__(self):
        """destructor"""
        self.PidMonitor.RemoveMe()
        MasterRun.Agent.Log.info(" Removing My PID in Monitor file :"+str(self.OwnPythonID))
        
        


# Example of use
Test = RunManager()

print Test.TotalRecordToCompleteRun

Test.LoopForAllTheRecord()
    
        
        
        
    
    