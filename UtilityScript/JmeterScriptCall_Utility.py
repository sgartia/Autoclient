"""   This module would call the jmater script and pass the parameter based on the requirement """

# Import session 
from GlobalVariable_Utility import *

class CallJmeterScript(object):
    """ This contains all the method related to Jmeter script execution"""
    
    HomeDir =  None
    ToolDir =  None
    JmeterDir = None
    JmaterPath = None
    ResultFilePath = None
    
    # Related to project parameter
    JmeterScriptDir = None
    ScriptName = None
    ScriptParameterDic = {}
    
    CommandParam = None
   

    #----------------------------------------------------------------------
    def __init__(self,ScriptName):
        """Constructor"""
        self.HomeDir =  str(os.path.dirname(os.path.realpath(__file__))).split(MAIN_DIR)[0]+MAIN_DIR+"\\"
        self.ToolDir = self.HomeDir+"TOOL\\"
        self.JmeterDir = self.ToolDir+"jmeter\\apache\\bin\\"
        self.JmaterPath = self.JmeterDir+"jmeter "
        self.ResultFilePath = self.HomeDir+"Result\\"
        self.JmeterScriptDir = self.HomeDir+"JmeterScript\\"
        
        # assign the script name 
        self.ScriptName = ScriptName
        
        
        
    #----------------------------------------------------------------------
    def ExecuteTheScript(self):
        """  This method run the expected script"""
        
        self.CommandParam = ""
        
        # Construct the Argument
        PropertySet = "  -Jjmeter.save.saveservice.timestamp_format=\"yyyy/MM/dd HH:mm:ss.SSS\""
        
        TempTime = datetime.datetime.now()   
        FileTime = str(TempTime.strftime("%H_%M_%S"))
        TempFileName = str(TempTime.strftime("%Y_%m_%d"))
        
        ResultFileCmd = str(" -l "+ self.ResultFilePath+TempFileName+"\\"+str(self.ScriptName).split(".")[0]+"_"+FileTime+".csv")
        LogFileCmd = str("  -j "+ self.ResultFilePath+TempFileName+"\\"+str(self.ScriptName).split(".")[0]+"_"+FileTime+"_JmeterLog.txt")
    
        self.JmeterCommand = str(self.JmaterPath +"-n -t "+self.JmeterScriptDir+self.ScriptName)  
                
    
        for keys in self.ScriptParameterDic:
            self.CommandParam = self.CommandParam + "  -J"+keys+"="+str(self.ScriptParameterDic[keys])+" "
           
            
        self.Cmdline = self.JmeterCommand + self.CommandParam + ResultFileCmd +LogFileCmd+PropertySet
        print self.Cmdline
        
        # Execute the cmd 
        
## Example of use 
#JmeterAgent = CallJmeterScript("VSTUserRespondingLatestMessageRecived.jmx")
#JmeterAgent.ScriptParameterDic['uniqueId']= str(uuid.uuid4())


## initialize the parameter

## assign The script name
#JmeterAgent.ExecuteTheScript()