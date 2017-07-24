"""    This module is developed for various server logparsing """
import sys
########################################################################

    
class LogParser(object):
    """"""
    LogDir = None
    LogFilePathList = None
    CurrentLogFilePath = None
    VMPLogDic = None
    VMPExpLogPatternList = None
    PatternListNeedToMatch = []
    PatternVSScenarioName = {}
    MessageSeqnoAndDuration = {}
    MasterDic = {}
    
    

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        #Initialize all the path 
        self.LogDir = "C:\\Autoclient\\UtilityScript\\"  
        self.CurrentLogFilePath = self.LogDir+"WDE_v5.2.1.1464_17_03_30 00-00-18.log"
        self.VMPLogStartingPatternList = {'tmsend':'query=tmsend','getpushdata':'query=getpushdata'}
        self.VMPLogEndingPatternList = {'tmsend':'End executing WICService','getpushdata':'End executing WICService'}
        self.VMPLogScenarioVSSequenceNumberExists = {'tmsend':True,'getpushdata':True}
        
        
        # Prepare the PatternListNeedToMatch
        for keys in self.VMPLogStartingPatternList:
            self.PatternListNeedToMatch.append(self.VMPLogStartingPatternList[keys])
            
            # Also initialize the MasterDic dictionary 
            self.PatternVSScenarioName[self.VMPLogStartingPatternList[keys]] = keys
            self.MasterDic[keys] = {}
            self.MasterDic[keys]['SearchPattern'] = self.VMPLogStartingPatternList[keys]
            self.MasterDic[keys]['NumberOfOccurance'] = 0
            
    def __GetTimeFromLogLine (self,templine):
        """  Thsi """
        return str(templine).split()[2]
    
    def __GetSeqNoFromLogLine (self,templine):
        return str(str(templine).split()[4]).strip('{}')

    def CalculateDuration(self,starttime,endtime):
        
        temp1 = str(str(starttime).replace(".",":")).split(":")
        StartTime = ((int(temp1[0]) * 3600 + int(temp1[1]) * 60 + int(temp1[2]))* 1000) + int(temp1[3])
        
        temp2 = str(str(endtime).replace(".",":")).split(":")
        EndTime = ((int(temp2[0]) * 3600 + int(temp2[1]) * 60 + int(temp2[2]))* 1000) + int(temp2[3])
        
        return (EndTime - StartTime)
    #----------------------------------------------------------------------
    def ProcessVMPLogFile(self):
        """"""
        
        # Process the log file 
        fh = open(self.CurrentLogFilePath,'r')
        AllData = fh.readlines()
        fh.close()
        
        # Check all the pattern in all the line 
        StartAndEndFlag = None
        ScenarioName = None
        index = 0
        
        for line in AllData:
            for item in self.PatternListNeedToMatch:

                
                if (str(line).find(item) != -1):
                    
                    # Get the scenario Name 
                    ScenarioName = self.PatternVSScenarioName[item]
                    self.MasterDic[ScenarioName]['NumberOfOccurance'] = self.MasterDic[ScenarioName]['NumberOfOccurance'] + 1
                    index = self.MasterDic[ScenarioName]['NumberOfOccurance']
                    self.MasterDic[ScenarioName][index] = {}
                    
                    # Get the starting time of the scenario
                    self.MasterDic[ScenarioName][index]['StartTime'] = self.__GetTimeFromLogLine(line)
                    
                    # Get the Sequnce number if it exists 
                    if (self.VMPLogScenarioVSSequenceNumberExists[ScenarioName] == True):
                        self.MasterDic[ScenarioName][index]['SequenceNumber'] = self.__GetSeqNoFromLogLine(line)
                    else:
                        self.MasterDic[ScenarioName][index]['SequenceNumber'] = None
                        
                      
                    StartAndEndFlag = True
                    
                  
                # Check for the end flag
                if (StartAndEndFlag == True):
                    pattern = self.VMPLogEndingPatternList[ScenarioName]
                    
                    if (str(line).find(pattern) != -1):
                        self.MasterDic[ScenarioName][index]['EndTime'] = self.__GetTimeFromLogLine(line)
                        StartAndEndFlag = False
                        
                    

                    
        
        
        
        
        
# Example of use
Test = LogParser()
Test.ProcessVMPLogFile()
for keys in Test.MasterDic['tmsend']:
    try: 
        Test.MessageSeqnoAndDuration[Test.MasterDic['tmsend'][keys]['SequenceNumber']] = Test.CalculateDuration(Test.MasterDic['tmsend'][keys]['StartTime'],Test.MasterDic['tmsend'][keys]['EndTime'])
    except:
        sys.exc_clear()
        
print "Total Number of message: " + str(len(Test.MessageSeqnoAndDuration) )   
print Test.MessageSeqnoAndDuration
        
    
    