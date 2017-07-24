"""   this module is to create a socket listener to listen the command from the test controller """

from GlobalVariable_Utility import *

class ServerSocket (object):
    """  This class would create the socket server  and listening the port"""
    Port = None
    NumberOfConnection = None
    IP = None
    ServerSocket = None
    buf = None
    RunCmd = None
    OwnPythonPID = None
   
        
    
    def __init__(self,ip,port,NumberOfConnection = 1000):
        """  constructor initialize the socket server """
        self.IP = ip
        self.Port = port
        self.NumberOfConnection = NumberOfConnection
        self.RunCmd = "start "+PYTHON_PATH+" "+SCRIPT_DIR+"RunManager_Utility.py "
        
        # Get the own pid 
        self.OwnPythonPID = os.getpid() 
        
        # Write the PID in file 
        Test = RemeberPID(self.OwnPythonPID)
        Test.AppendMe()
               
        

        # Create the server socket 
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSocket.bind((self.IP, self.Port))
        self.ServerSocket.listen(5) # become a server socket, maximum 5 connections
        
        MasterRun.Agent.Log.info("Created a server socket Listener :"+str(self.IP)+" PID :"+str(self.OwnPythonPID))
        
        count = 0
        
        while True:
            connection, address = self.ServerSocket.accept()
            
            try :
                print connection
                print address
                self.buf = connection.recv(1028)
                
                
                if len(self.buf) > 0:
                    temp = self.RunCmd+self.buf
                    print temp
                    MasterRun.Agent.Log.info("Command to socket Listener : " + str(temp))
                    
                    # clean All the temp file before run and handle exception 
                    
                    if (str(self.buf).find("StopAndReset.py") != -1):
                        
                        # Kill all the Python, Java, cmd line 
                        self.KillAllJavaPythonCmdProcess()
                    
                    else:                        
                        count = count + 1
                        os.system(temp)
                        
                        if (count > self.NumberOfConnection):
                            break
            except:
                print sys.exc_info()

    
        
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
        #print AllPid
        
        MasterRun.Agent.Log.info(" Initiating a Clean State of the TestVM ")
        
        # Remove the own Python ID and Cmd Pid from the list
        if (self.OwnPythonPID in AllPid):
            AllPid.remove(self.OwnPythonPID)
       
        for item in  AllPid:
            print psutil.pid_exists(item)
            try:
                if (psutil.pid_exists(item)):                    
                    cmd = "TASKKILL /F /FI \"PID eq "+str(item)+"\""
                    MasterRun.Agent.Log.info(" Killing PID :"+ str(item)+"")
                
                    os.system(cmd)
                    time.sleep(2)
                
            except:
                MasterRun.Agent.Log.info(" Exception occured in Killing PID :"+ str(item)+"")
                sys.exc_clear()
                
    def KillAllJavaPythonCmdProcess(self):
        """  Call __CleanAndResetVM """
        
        # clean all Java process
        self.__CleanAndResetVM('java.exe')
        
        # clean all Python Process
        self.__CleanAndResetVM('python.exe')
        
        # clean all cmd.exe Process
        self.__CleanAndResetVM('cmd.exe')
        
        
        
    


    

# Example of use 
#print PRIME_IP
#print LOCAL_VM_IP_TO_REMOTE

if (LOCAL_VM_IP_TO_REMOTE == PRIME_IP):
       
    Sever = ServerSocket(PRIME_IP,SERVER_PORT)
else:
    
    Sever = ServerSocket(LOCAL_VM_IP_TO_REMOTE,SERVER_PORT)
    
